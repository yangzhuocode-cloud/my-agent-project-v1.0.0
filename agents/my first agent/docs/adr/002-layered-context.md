# ADR-002: 分层上下文存储架构

## 状态
已接受

## 背景

初始版本使用简单的列表存储上下文：

```python
self.context = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
```

这种方式存在以下问题：

1. **无法区分重要性**：所有消息平等对待，可能删除重要信息
2. **任务丢失风险**：滑动窗口可能删除用户的原始任务
3. **重复错误浪费**：相同错误重复保存，占用大量 token
4. **不适合迭代**：工程化场景需要记住任务目标和执行状态

使用场景：
- Agent 需要自动迭代执行代码
- 需要记住任务目标、错误历史、文件状态
- 需要智能裁剪，避免 token 浪费

## 决策

我们决定采用 **分层上下文存储架构**，将上下文分为三层：

```python
context = {
    # 第1层：永久保留（不参与裁剪）
    "permanent": {
        "system": "系统提示词",
        "task": "用户原始任务"
    },
    
    # 第2层：重要信息（压缩保留）
    "important": {
        "errors": [],      # 错误历史（去重）
        "milestones": []   # 里程碑事件
    },
    
    # 第3层：滚动窗口（完整保留最近N条）
    "recent": [
        {
            "role": "user",
            "content": "...",
            "priority": 5,
            "timestamp": 1234567890
        }
    ]
}
```

### 核心特性

1. **分层管理**：不同重要性的信息存储在不同层
2. **优先级标记**：每条消息自动标记优先级
3. **智能去重**：重复错误自动检测和合并
4. **自动压缩**：低优先级消息自动压缩或删除

## 后果

### 正面影响

1. **任务不丢失**：原始任务永远保留在 permanent 层
2. **错误可追溯**：错误历史单独管理，支持去重
3. **智能裁剪**：基于优先级裁剪，保留重要信息
4. **适合迭代**：记住任务目标和执行状态
5. **节省 token**：重复信息压缩，提高 token 利用率

### 负面影响

1. **复杂度增加**：代码结构更复杂，需要维护多层数据
   - 缓解措施：提供清晰的文档和示例代码
   
2. **转换开销**：需要将分层结构转换为 OpenAI 协议格式
   - 缓解措施：转换逻辑封装在 `build_api_messages()` 方法中
   
3. **调试困难**：分层结构不如列表直观
   - 缓解措施：提供 `debug_context()` 方法查看完整状态

### 技术债务

1. 需要实现完整的优先级计算逻辑
2. 需要实现错误签名生成和去重
3. 需要实现消息压缩算法
4. 需要编写单元测试验证裁剪逻辑

## 替代方案

### 方案1：继续使用简单列表 + 优先级标记

```python
self.context = [
    {"role": "system", "content": "...", "priority": 10},
    {"role": "user", "content": "...", "priority": 5}
]
```

**优点**：
- 结构简单，易于理解
- 与 OpenAI 协议格式接近

**缺点**：
- 无法保证任务不被删除
- 错误历史无法去重
- 裁剪逻辑复杂

**为什么不选**：无法满足工程化场景的需求

### 方案2：使用摘要压缩策略

将旧对话总结成摘要，替换原始内容。

**优点**：
- 保留语义信息
- 大幅减少 token

**缺点**：
- 需要额外 API 调用（成本高）
- 摘要可能丢失细节
- 实现复杂

**为什么不选**：成本高，实现复杂，不适合初期版本

### 方案3：使用向量数据库

将历史对话存储在向量数据库，根据相似度检索。

**优点**：
- 可以检索任意历史信息
- 不受 token 限制

**缺点**：
- 需要额外的向量数据库服务
- 需要 embedding 模型
- 复杂度极高

**为什么不选**：过度设计，不适合当前阶段

## 实现细节

### 优先级计算

```python
def calculate_priority(self, content, role):
    if role == "system":
        return 10  # CRITICAL
    if self._is_error(content):
        return 9 if not self._is_duplicate_error(content) else 3
    if self._is_file_operation(content):
        return 8  # HIGH
    if "成功" in content:
        return 5  # MEDIUM
    return 5  # DEFAULT
```

### 错误去重

```python
def get_error_signature(self, error_text):
    # 提取错误类型
    error_type = extract_error_type(error_text)
    # 提取关键信息
    key_info = extract_key_info(error_text)
    # 生成签名
    return f"{error_type}:{key_info}"
```

### 转换为 API 格式

```python
def build_api_messages(self):
    messages = []
    # 1. System prompt
    messages.append({"role": "system", "content": self.context["permanent"]["system"]})
    # 2. 任务描述
    messages.append({"role": "user", "content": f"任务：{self.context['permanent']['task']}"})
    # 3. 错误摘要
    if self.context["important"]["errors"]:
        messages.append({"role": "assistant", "content": self._format_error_summary()})
    # 4. 最近对话
    messages.extend(self.context["recent"])
    return messages
```

## 迁移计划

从简单列表迁移到分层结构：

### 阶段1：保持兼容（当前）
- 保留现有的列表结构
- 添加优先级标记
- 实现基本的优先级裁剪

### 阶段2：引入分层（下一步）
- 实现分层存储结构
- 实现转换逻辑
- 保持 API 调用接口不变

### 阶段3：完善功能
- 实现错误去重
- 实现消息压缩
- 添加单元测试

### 阶段4：优化性能
- 优化 token 估算
- 优化裁剪算法
- 添加性能监控

## 验证标准

通过以下标准验证架构的有效性：

1. ✅ 原始任务在任何情况下都不会丢失
2. ✅ 重复错误能够正确检测和去重
3. ✅ 高优先级消息优先保留
4. ✅ Token 使用率控制在目标范围内
5. ✅ 转换后的消息格式符合 OpenAI 协议

## 性能考虑

1. **Token 估算**：使用简单的字符数估算，避免复杂计算
2. **裁剪频率**：只在达到阈值时触发，避免频繁裁剪
3. **错误历史大小**：限制最多 20 个不同错误
4. **里程碑数量**：限制最多 10 个里程碑

## 参考资料

- [AutoGPT 的上下文管理](https://github.com/Significant-Gravitas/AutoGPT)
- [LangChain Agent Memory](https://python.langchain.com/docs/modules/memory/)
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- 项目内部文档：[上下文管理策略](../context-management.md)
