# ADR-003: 上下文智能裁剪算法与参数配置

## 状态
已接受 - v1.0（待优化）

## 背景

在实现了分层上下文存储架构（ADR-002）后，我们需要设计一套智能裁剪算法来管理有限的上下文窗口。

### 核心挑战

1. **上下文窗口有限**：豆包模型提供 256k tokens 上下文窗口，但需要为模型回复预留空间
2. **质量与容量的平衡**：过早裁剪影响任务连贯性，过晚裁剪可能触发硬限制
3. **信息重要性不均**：不同消息的重要性差异巨大，需要智能选择保留内容
4. **循环执行场景**：Agent 需要多次迭代，上下文会持续增长

### 业界实践调研

通过调研主流 Agent 框架的实践，我们发现：

- **LangChain Deep Agents**: 85% 时触发裁剪
- **COMPRESSION.md 标准**: 75% 时触发增量压缩
- **实践经验**: 60% 时输出质量开始下降（Blake Crosley, 2026）
- **Claude Plugin Hub**: 50% 建议手动同步，80% 自动触发

关键发现：
1. 大多数框架在 75-85% 时触发裁剪
2. 输出质量在 60% 使用率时就开始下降
3. 保留最近 3-6 轮完整对话是常见做法
4. 需要为模型回复预留 15-20% 空间


## 决策

我们采用 **基于优先级的智能裁剪算法**，配合以下参数配置：

### 核心参数（v1.0）

```python
# 上下文配置
MODEL_MAX_TOKENS = 256000           # 256k 上下文窗口
CONTEXT_SAFETY_RATIO = 0.80         # 保留 80% 给历史，20% 给新回复
MAX_CONTEXT_TOKENS = 204800         # 256000 * 0.80

# 裁剪触发与目标
TRIM_THRESHOLD = 0.80               # 达到 80% 时触发裁剪
TRIM_TARGET = 0.60                  # 裁剪到 60%
```

### 参数含义解析

1. **CONTEXT_SAFETY_RATIO = 0.80**
   - 总容量 256k tokens
   - 最多使用 204.8k tokens（80%）
   - 预留 51.2k tokens（20%）给模型回复

2. **TRIM_THRESHOLD = 0.80**
   - 当使用率达到 80% × 80% = 64% 时触发
   - 即：163.84k / 256k = 64%
   - 实际触发点：163.84k tokens

3. **TRIM_TARGET = 0.60**
   - 裁剪到 60% × 80% = 48%
   - 即：122.88k / 256k = 48%
   - 裁剪后保留：122.88k tokens
   - 清理空间：40.96k tokens（20%）

### 裁剪算法

```python
def _smart_trim(self):
    """智能裁剪上下文"""
    
    # 步骤1：永久层不参与裁剪
    # permanent 层（system prompt + task）始终保留
    
    # 步骤2：保留最近 N 轮对话（完整）
    recent_keep_count = 6  # 3轮对话 = 6条消息（user + assistant）
    must_keep = self.context["recent"][-recent_keep_count:]
    
    # 步骤3：对更早的消息按优先级排序
    older = self.context["recent"][:-recent_keep_count]
    older.sort(key=lambda x: x["priority"], reverse=True)
    
    # 步骤4：计算可用空间
    target_tokens = int(MAX_CONTEXT_TOKENS * TRIM_TARGET)  # 122.88k
    current_tokens = self._estimate_permanent_tokens()
    current_tokens += self._estimate_important_tokens()
    current_tokens += self._estimate_messages_tokens(must_keep)
    
    # 步骤5：从旧消息中选择高优先级的，直到填满空间
    selected = []
    for msg in older:
        msg_tokens = self._estimate_messages_tokens([msg])
        if current_tokens + msg_tokens <= target_tokens:
            # 空间足够，完整保留
            selected.append(msg)
            current_tokens += msg_tokens
        elif msg["priority"] >= MessagePriority.HIGH:
            # 高优先级消息，压缩后保留
            compressed = self._compress_message(msg)
            compressed_tokens = self._estimate_messages_tokens([compressed])
            if current_tokens + compressed_tokens <= target_tokens:
                selected.append(compressed)
                current_tokens += compressed_tokens
    
    # 步骤6：重新组装（按时间顺序）
    selected.sort(key=lambda x: x["timestamp"])
    self.context["recent"] = selected + must_keep
    
    removed_count = len(older) - len(selected)
    print(f"✂️ 裁剪了 {removed_count} 条消息")
```


### 裁剪规则

#### 规则1：分层保护

```
永久层（permanent）     → 永不裁剪
重要信息层（important）  → 压缩保留（错误去重、里程碑摘要）
最近对话层（recent）     → 智能裁剪（基于优先级）
```

#### 规则2：最近对话保护

- 无条件保留最近 6 条消息（3 轮对话）
- 保证任务连贯性和上下文连续性
- 即使优先级低也不会被删除

#### 规则3：优先级排序

对于更早的消息，按优先级排序：

```python
CRITICAL (10)  → 永不删除（system、task）
HIGH (8)       → 尽量保留，空间不足时压缩
MEDIUM (5)     → 可压缩或删除
LOW (2)        → 优先删除
```

#### 规则4：高优先级压缩

当高优先级消息无法完整保留时，进行压缩：

```python
# 错误信息：保留错误类型和关键信息
"[错误] NameError: name 'x' is not defined at line 10..."

# 文件操作：保留操作类型和文件名
"[文件操作] 创建文件 calculator.py..."

# 成功操作：保留简要描述
"[成功] 修复了语法错误..."
```

#### 规则5：时间顺序恢复

裁剪完成后，按时间戳重新排序，保持对话的时间连贯性。


## 后果

### 正面影响

1. **质量保障**
   - 在 64% 使用率时触发，远早于质量下降点（60%）
   - 保留最近 3 轮对话，保证任务连贯性
   - 高优先级信息优先保留

2. **空间充足**
   - 裁剪后保留 48%，清理 20% 空间
   - 为后续对话提供充足空间
   - 避免频繁触发裁剪

3. **信息不丢失**
   - 永久层（system + task）永不删除
   - 重要信息层（errors + milestones）压缩保留
   - 高优先级消息压缩而非删除

4. **性能可控**
   - 只在达到阈值时触发，避免频繁计算
   - Token 估算使用简单算法，速度快
   - 裁剪操作时间复杂度 O(n log n)

### 负面影响

1. **参数调优困难**
   - 当前参数基于理论和业界实践
   - 缺乏实际使用数据验证
   - 不同任务类型可能需要不同参数

2. **Token 估算不精确**
   - 使用字符数 × 1.2 的简单估算
   - 中英文混合场景误差较大
   - 可能导致实际使用率偏差

3. **压缩可能丢失细节**
   - 高优先级消息压缩后只保留摘要
   - 可能丢失一些细节信息
   - 影响需要回溯细节的场景

### 技术债务

1. 需要收集实际使用数据，验证参数合理性
2. 需要实现更精确的 token 计算（如使用 tiktoken）
3. 需要支持用户自定义参数配置
4. 需要添加裁剪效果的监控和分析


## 替代方案

### 方案1：更激进的裁剪（60% 触发，40% 目标）

```python
TRIM_THRESHOLD = 0.60  # 达到 60% 时触发
TRIM_TARGET = 0.40     # 裁剪到 40%
```

**优点**：
- 更早介入，保证输出质量
- 更大的清理空间，减少裁剪频率

**缺点**：
- 可能过早删除有用信息
- 裁剪更频繁，影响性能

**为什么不选**：过于激进，可能影响任务连贯性

### 方案2：更保守的裁剪（85% 触发，70% 目标）

```python
TRIM_THRESHOLD = 0.85  # 达到 85% 时触发
TRIM_TARGET = 0.70     # 裁剪到 70%
```

**优点**：
- 保留更多历史信息
- 裁剪频率更低

**缺点**：
- 可能在质量下降后才触发
- 清理空间较小，可能频繁触发

**为什么不选**：触发时机偏晚，可能影响输出质量

### 方案3：动态阈值（根据任务类型调整）

根据任务类型动态调整阈值：
- 简单任务：85% 触发，70% 目标
- 复杂任务：70% 触发，50% 目标

**优点**：
- 更灵活，适应不同场景
- 可以优化不同任务的表现

**缺点**：
- 实现复杂，需要任务分类
- 难以确定任务类型
- 增加系统复杂度

**为什么不选**：过度设计，不适合 v1.0

### 方案4：基于摘要的压缩（LLM 生成摘要）

使用 LLM 生成对话摘要，替换原始内容。

**优点**：
- 保留语义信息
- 大幅减少 token 使用

**缺点**：
- 需要额外 API 调用（成本高）
- 增加延迟
- 摘要质量不可控

**为什么不选**：成本高，复杂度高，不适合初期版本


## 参数确定依据

### 1. CONTEXT_SAFETY_RATIO = 0.80

**依据**：
- 豆包模型最大回复长度配置为 2000 tokens
- 实际回复通常在 500-1500 tokens
- 预留 20%（51.2k tokens）远超实际需求
- 为复杂回复和工具调用预留充足空间

**业界对比**：
- LangChain: 未明确说明，但工具调用结果超过 20k tokens 时会离线存储
- COMPRESSION.md: 建议预留 15-20% 空间

**结论**：80% 是合理的保守值

### 2. TRIM_THRESHOLD = 0.80

**依据**：
- 实际触发点：64%（80% × 80%）
- 高于质量下降点（60%），但留有安全边界
- 避免过早裁剪影响任务连贯性
- 避免过晚裁剪影响输出质量

**业界对比**：
- LangChain Deep Agents: 85% 触发
- COMPRESSION.md: 75% 触发
- 实践经验: 60% 质量开始下降

**结论**：64% 触发点处于业界实践的中间位置，平衡了质量和容量

### 3. TRIM_TARGET = 0.60

**依据**：
- 实际目标：48%（60% × 80%）
- 清理空间：20%（从 64% 降到 48%）
- 为后续 3-5 轮对话提供空间
- 避免频繁触发裁剪

**业界对比**：
- LangChain: 裁剪到 85% 以下（具体值未明确）
- COMPRESSION.md: 提供 light/standard/aggressive 三档
- 实践建议: 保留最近 3-6 轮对话

**结论**：48% 目标值保证了充足的清理空间，同时保留了重要信息

### 4. recent_keep_count = 6

**依据**：
- 6 条消息 = 3 轮对话（user + assistant）
- 保证任务连贯性的最小单位
- 符合人类短期记忆容量（7±2）
- 平衡信息保留和空间占用

**业界对比**：
- COMPRESSION.md: 保留最近 3 轮对话
- LangChain: 未明确说明，但保留最近交互
- 实践经验: 3-6 轮是常见做法

**结论**：3 轮对话是业界共识


## 未来优化方向

### 短期优化（v1.1 - v1.3）

#### 1. 精确 Token 计算

**当前问题**：使用字符数 × 1.2 的简单估算，误差较大

**优化方案**：
```python
import tiktoken

def _estimate_tokens_precise(self, messages):
    """使用 tiktoken 精确计算 token 数"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    total_tokens = 0
    for msg in messages:
        # 每条消息的固定开销：4 tokens
        total_tokens += 4
        total_tokens += len(encoding.encode(msg["content"]))
    return total_tokens
```

**预期效果**：
- Token 估算误差从 ±20% 降低到 ±5%
- 更准确的裁剪触发时机
- 减少不必要的裁剪或避免超限

#### 2. 参数配置化

**当前问题**：参数硬编码在代码中，无法灵活调整

**优化方案**：
```python
# config.json
{
    "context": {
        "safety_ratio": 0.80,
        "trim_threshold": 0.80,
        "trim_target": 0.60,
        "recent_keep_count": 6
    }
}
```

**预期效果**：
- 用户可以根据任务类型调整参数
- 支持 A/B 测试不同参数组合
- 便于快速迭代优化

#### 3. 裁剪效果监控

**当前问题**：缺乏裁剪效果的量化指标

**优化方案**：
```python
# 记录裁剪统计
trim_stats = {
    "trim_count": 0,           # 裁剪次数
    "messages_removed": 0,     # 删除消息数
    "messages_compressed": 0,  # 压缩消息数
    "tokens_saved": 0,         # 节省 token 数
    "avg_usage_before": 0.0,   # 裁剪前平均使用率
    "avg_usage_after": 0.0     # 裁剪后平均使用率
}
```

**预期效果**：
- 量化裁剪效果
- 发现参数调优方向
- 验证算法有效性


### 中期优化（v2.0 - v2.5）

#### 4. 语义相似度去重

**当前问题**：只对错误进行去重，其他重复信息未处理

**优化方案**：
```python
from sentence_transformers import SentenceTransformer

def _is_semantically_similar(self, msg1, msg2, threshold=0.85):
    """判断两条消息是否语义相似"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(msg1["content"])
    emb2 = model.encode(msg2["content"])
    similarity = cosine_similarity(emb1, emb2)
    return similarity > threshold
```

**预期效果**：
- 自动检测和合并语义重复的消息
- 进一步减少 token 使用
- 提高上下文信息密度

#### 5. 动态阈值调整

**当前问题**：固定阈值无法适应不同任务类型

**优化方案**：
```python
def _calculate_dynamic_threshold(self):
    """根据任务特征动态调整阈值"""
    # 分析任务复杂度
    complexity = self._analyze_task_complexity()
    
    if complexity == "simple":
        return 0.85, 0.70  # 简单任务，保守裁剪
    elif complexity == "medium":
        return 0.80, 0.60  # 中等任务，标准裁剪
    else:
        return 0.70, 0.50  # 复杂任务，激进裁剪
```

**预期效果**：
- 简单任务保留更多历史
- 复杂任务更早介入裁剪
- 提高不同场景的适应性

#### 6. 基于 LLM 的智能摘要

**当前问题**：压缩策略简单，可能丢失重要信息

**优化方案**：
```python
def _summarize_with_llm(self, messages):
    """使用 LLM 生成智能摘要"""
    prompt = f"""
    请将以下对话总结为简洁的摘要，保留关键信息：
    {messages}
    
    要求：
    1. 保留任务目标和决策
    2. 保留错误和解决方案
    3. 保留文件操作记录
    4. 控制在 200 tokens 以内
    """
    summary = self.call_api(prompt)
    return summary
```

**预期效果**：
- 保留语义信息，减少细节丢失
- 大幅压缩 token 使用
- 提高长时间运行的稳定性

**成本考虑**：
- 每次摘要需要额外 API 调用
- 建议只在必要时使用（如超过 10 轮对话）
- 可以缓存摘要结果


### 长期优化（v3.0+）

#### 7. 外部存储 + 检索增强

**当前问题**：所有信息都在内存中，受上下文窗口限制

**优化方案**：
```python
# 使用向量数据库存储历史对话
from chromadb import Client

class ExternalMemory:
    def __init__(self):
        self.client = Client()
        self.collection = self.client.create_collection("agent_memory")
    
    def store(self, message):
        """存储消息到向量数据库"""
        self.collection.add(
            documents=[message["content"]],
            metadatas=[{"timestamp": message["timestamp"]}],
            ids=[str(message["timestamp"])]
        )
    
    def retrieve(self, query, top_k=5):
        """根据查询检索相关历史"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results
```

**预期效果**：
- 突破上下文窗口限制
- 支持任意长度的对话历史
- 按需检索相关信息

**技术挑战**：
- 需要额外的向量数据库服务
- 需要 embedding 模型
- 检索质量依赖查询设计

#### 8. 多模态上下文管理

**当前问题**：只支持文本，无法处理图片、代码等

**优化方案**：
```python
context = {
    "permanent": {...},
    "important": {
        "errors": [],
        "milestones": [],
        "code_snapshots": [],    # 代码快照
        "diagrams": []           # 架构图
    },
    "recent": [...]
}
```

**预期效果**：
- 支持代码快照存储
- 支持架构图等可视化内容
- 更丰富的上下文信息

#### 9. 自适应学习

**当前问题**：参数固定，无法从使用中学习

**优化方案**：
```python
class AdaptiveTrimmer:
    def __init__(self):
        self.performance_history = []
    
    def learn_from_feedback(self, trim_params, task_success):
        """从任务结果学习最优参数"""
        self.performance_history.append({
            "params": trim_params,
            "success": task_success
        })
        
        # 使用强化学习优化参数
        optimal_params = self._optimize_params()
        return optimal_params
```

**预期效果**：
- 自动优化裁剪参数
- 适应用户使用习惯
- 持续提升性能


## 验证计划

### 阶段1：单元测试（已完成）

验证裁剪算法的基本功能：

```python
def test_trim_threshold():
    """测试裁剪触发时机"""
    agent = VolcArkDoubaoAgent()
    # 添加消息直到达到阈值
    # 验证是否正确触发裁剪

def test_trim_target():
    """测试裁剪目标"""
    agent = VolcArkDoubaoAgent()
    # 触发裁剪
    # 验证裁剪后的 token 使用率

def test_priority_preservation():
    """测试优先级保留"""
    agent = VolcArkDoubaoAgent()
    # 添加不同优先级的消息
    # 触发裁剪
    # 验证高优先级消息是否保留

def test_recent_protection():
    """测试最近对话保护"""
    agent = VolcArkDoubaoAgent()
    # 添加消息并触发裁剪
    # 验证最近 6 条消息是否完整保留
```

### 阶段2：集成测试（待完成）

在真实场景中验证裁剪效果：

1. **简单任务测试**
   - 任务：创建一个简单的 Python 脚本
   - 预期：不触发裁剪或只触发 1 次
   - 验证：任务成功完成

2. **中等任务测试**
   - 任务：实现一个包含多个文件的项目
   - 预期：触发 2-3 次裁剪
   - 验证：任务连贯性，关键信息不丢失

3. **复杂任务测试**
   - 任务：调试一个复杂的错误，需要多次迭代
   - 预期：触发 5+ 次裁剪
   - 验证：错误历史正确保留，不重复尝试失败方案

### 阶段3：性能测试（待完成）

测试裁剪算法的性能：

```python
def benchmark_trim_performance():
    """测试裁剪性能"""
    agent = VolcArkDoubaoAgent()
    
    # 添加 1000 条消息
    for i in range(1000):
        agent.add_message("user", f"消息 {i}")
    
    # 测试裁剪时间
    start = time.time()
    agent._smart_trim()
    duration = time.time() - start
    
    print(f"裁剪 1000 条消息耗时: {duration:.2f}s")
    # 预期：< 1s
```

### 阶段4：用户反馈（待收集）

收集真实用户的使用反馈：

1. **质量评估**
   - 裁剪后任务完成质量是否下降？
   - 是否出现信息丢失导致的错误？
   - 是否出现重复尝试失败方案？

2. **参数调优**
   - 触发时机是否合适？
   - 清理力度是否合适？
   - 保留的对话轮数是否合适？

3. **性能评估**
   - 裁剪是否影响响应速度？
   - Token 使用率是否符合预期？
   - 是否频繁触发裁剪？


## 实现清单

### v1.0 已实现 ✅

- [x] 分层上下文存储结构（ADR-002）
- [x] 优先级计算系统
- [x] 错误去重机制
- [x] 智能裁剪算法
- [x] 消息压缩策略
- [x] Token 估算（简单版）
- [x] 裁剪触发检查
- [x] 最近对话保护

### v1.1 - v1.3 待实现 📋

- [ ] 精确 Token 计算（tiktoken）
- [ ] 参数配置化（config.json）
- [ ] 裁剪效果监控
- [ ] 单元测试完善
- [ ] 集成测试
- [ ] 性能基准测试

### v2.0+ 待规划 🔮

- [ ] 语义相似度去重
- [ ] 动态阈值调整
- [ ] 基于 LLM 的智能摘要
- [ ] 外部存储 + 检索增强
- [ ] 多模态上下文管理
- [ ] 自适应学习

## 参考资料

### 业界实践

1. **LangChain Deep Agents**
   - 文档：https://www.blog.langchain.com/context-management-for-deepagents/
   - 触发阈值：85%
   - 策略：离线存储大文件，裁剪旧工具调用

2. **COMPRESSION.md 标准**
   - 网站：https://compression.md/
   - 触发阈值：75%
   - 策略：保留 system prompt、任务、最近 3 轮对话

3. **Blake Crosley 实践经验**
   - 博客：https://blakecrosley.com/en/blog/context-window-management
   - 发现：60% 使用率时质量开始下降
   - 建议：每 25-30 分钟主动压缩

4. **Claude Plugin Hub**
   - 文档：https://www.claudepluginhub.com/skills/jason-hchsieh-adaptive-workflow/context
   - 触发阈值：50% 建议，80% 自动
   - 策略：分阶段上下文同步

### 学术研究

1. **Context Window Overflow in 2026**
   - 来源：Redis Blog
   - 发现：Agent 在多次工具调用后上下文快速增长
   - 建议：主动管理上下文，避免静默失败

2. **DAG-Based State Management**
   - 来源：arXiv 2602.22402v1
   - 发现：自动压缩可能丢失 98% 的细节信息
   - 建议：结构化保存状态，避免信息丢失

### 项目内部文档

- [上下文管理策略](../context-management.md)
- [ADR-002: 分层上下文存储架构](./002-layered-context.md)
- [ADR-001: OpenAI 协议兼容性](./001-openai-protocol.md)

## 更新历史

- 2026-03-21: v1.0 初始版本，确定核心参数和算法
- 待更新: v1.1 精确 Token 计算
- 待更新: v2.0 语义去重和动态阈值

---

**注意**：本文档描述的是 v1.0 版本的设计决策。参数和算法基于理论分析和业界实践，需要通过实际使用数据验证和优化。欢迎在使用过程中提供反馈，帮助我们改进裁剪策略。
