# 上下文管理策略

本文档详细说明 My First Agent 的上下文管理设计和实现。

## 设计目标

为工程化的自动迭代代码执行场景设计上下文管理策略，需要满足：

1. **任务连贯性**：始终记住用户的原始任务
2. **错误追溯**：保留关键错误信息，避免重复尝试
3. **状态可恢复**：记录文件状态、执行结果等关键信息
4. **自动压缩**：智能删除不重要的历史记录
5. **循环友好**：适合多次迭代执行

## 架构设计

### 分层存储结构

```python
context = {
    # 第1层：永久保留（不参与裁剪）
    "permanent": {
        "system": "系统提示词",
        "task": "用户原始任务描述"
    },
    
    # 第2层：重要信息（压缩保留）
    "important": {
        "errors": [
            {
                "signature": "NameError:x",
                "message": "NameError: name 'x' is not defined",
                "timestamp": 1234567890,
                "count": 3  # 重复次数
            }
        ],
        "milestones": [
            "成功创建 main.py",
            "修复了语法错误"
        ]
    },
    
    # 第3层：滚动窗口（完整保留最近N条）
    "recent": [
        {
            "role": "user",
            "content": "执行 python main.py",
            "priority": 5,
            "timestamp": 1234567890
        },
        {
            "role": "assistant",
            "content": "执行结果：...",
            "priority": 8,
            "timestamp": 1234567891
        }
    ]
}
```

### 与 OpenAI 协议的转换

发送给 API 时，需要转换为标准格式：

```python
def build_api_messages(self):
    """构建发送给 API 的消息列表"""
    messages = []
    
    # 1. 添加 system prompt
    messages.append({
        "role": "system",
        "content": self.context["permanent"]["system"]
    })
    
    # 2. 添加任务描述
    messages.append({
        "role": "user",
        "content": f"任务：{self.context['permanent']['task']}"
    })
    
    # 3. 添加错误历史摘要（如果有）
    if self.context["important"]["errors"]:
        error_summary = self._format_error_summary()
        messages.append({
            "role": "assistant",
            "content": error_summary
        })
    
    # 4. 添加里程碑摘要（如果有）
    if self.context["important"]["milestones"]:
        milestone_summary = "\n".join([
            f"- {m}" for m in self.context["important"]["milestones"]
        ])
        messages.append({
            "role": "assistant",
            "content": f"已完成的操作：\n{milestone_summary}"
        })
    
    # 5. 添加最近的对话
    messages.extend(self.context["recent"])
    
    return messages
```

## 优先级系统

### 优先级定义

```python
class MessagePriority:
    CRITICAL = 10   # 永不删除
    HIGH = 8        # 尽量保留
    MEDIUM = 5      # 可压缩
    LOW = 2         # 可删除
```

### 优先级计算规则

```python
def calculate_priority(self, content, role):
    """计算消息优先级"""
    
    # 规则1：System prompt - 永不删除
    if role == "system":
        return MessagePriority.CRITICAL
    
    # 规则2：原始任务 - 永不删除
    if content.startswith("任务："):
        return MessagePriority.CRITICAL
    
    # 规则3：错误信息 - 高优先级
    if self._is_error(content):
        # 检查是否是重复错误
        if self._is_duplicate_error(content):
            return MessagePriority.MEDIUM  # 降低优先级
        return MessagePriority.HIGH
    
    # 规则4：文件操作 - 高优先级
    if self._is_file_operation(content):
        return MessagePriority.HIGH
    
    # 规则5：成功操作 - 中优先级
    if "成功" in content or "完成" in content:
        return MessagePriority.MEDIUM
    
    # 规则6：思考过程 - 低优先级
    if any(kw in content for kw in ["让我想想", "分析", "考虑"]):
        return MessagePriority.LOW
    
    # 默认优先级
    return MessagePriority.MEDIUM
```

### 自动标记

在添加消息时自动计算并标记优先级：

```python
def add_message(self, role, content):
    """添加消息并自动标记优先级"""
    message = {
        "role": role,
        "content": content,
        "priority": self.calculate_priority(content, role),
        "timestamp": time.time(),
        "metadata": self._extract_metadata(content)
    }
    self.context["recent"].append(message)
    
    # 检查是否需要裁剪
    self._check_and_trim()
```

## 重复错误检测

### 错误签名生成

```python
def get_error_signature(self, error_text):
    """生成错误签名用于去重"""
    import re
    import hashlib
    
    # 1. 提取错误类型
    error_type_match = re.search(r'(\w+Error|\w+Exception)', error_text)
    error_type = error_type_match.group(1) if error_type_match else ""
    
    # 2. 提取关键变量/文件名（忽略行号）
    normalized = re.sub(r'line \d+', '', error_text)
    normalized = re.sub(r'\d{4}-\d{2}-\d{2}', '', normalized)
    
    # 3. 提取引号中的内容（变量名、文件名等）
    key_info = re.findall(r"'([^']*)'", normalized)
    
    # 4. 生成签名
    signature = f"{error_type}:{':'.join(key_info)}"
    return signature
```

### 重复检测逻辑

```python
def is_duplicate_error(self, error_text):
    """判断是否是重复错误"""
    new_signature = self.get_error_signature(error_text)
    
    # 检查错误历史
    for error_record in self.context["important"]["errors"]:
        if error_record["signature"] == new_signature:
            # 更新重复次数
            error_record["count"] += 1
            error_record["last_seen"] = time.time()
            return True
    
    # 新错误，添加到历史
    self.context["important"]["errors"].append({
        "signature": new_signature,
        "message": error_text[:200],  # 只保留前200字符
        "timestamp": time.time(),
        "count": 1
    })
    return False
```

### 错误历史格式化

```python
def _format_error_summary(self):
    """格式化错误历史为摘要"""
    errors = self.context["important"]["errors"]
    
    if not errors:
        return ""
    
    summary_lines = ["历史错误记录："]
    for error in errors[-5:]:  # 只显示最近5个
        if error["count"] > 1:
            summary_lines.append(
                f"- {error['signature']} (出现 {error['count']} 次)"
            )
        else:
            summary_lines.append(f"- {error['message'][:100]}")
    
    return "\n".join(summary_lines)
```

## 智能裁剪

### 触发时机

```python
def _check_and_trim(self):
    """检查并触发裁剪"""
    current_tokens = self._estimate_tokens()
    usage_ratio = current_tokens / self.max_tokens
    
    print(f"Token 使用率: {usage_ratio:.1%}")
    
    # 达到 80% 时触发裁剪
    if usage_ratio >= 0.80:
        print("⚠️ 触发智能裁剪")
        self._smart_trim()
```

### 裁剪策略

```python
def _smart_trim(self):
    """智能裁剪上下文"""
    
    # 1. 永久层不参与裁剪
    # permanent 层始终保留
    
    # 2. 保留最近 N 轮对话（完整）
    recent_keep_count = 6  # 3轮对话 = 6条消息
    must_keep = self.context["recent"][-recent_keep_count:]
    
    # 3. 对更早的消息按优先级排序
    older = self.context["recent"][:-recent_keep_count]
    older.sort(key=lambda x: x["priority"], reverse=True)
    
    # 4. 计算可用空间
    target_tokens = int(self.max_tokens * 0.60)  # 裁剪到 60%
    current_tokens = self._estimate_permanent_tokens()
    current_tokens += self._estimate_messages_tokens(must_keep)
    
    # 5. 从旧消息中选择高优先级的，直到填满空间
    selected = []
    for msg in older:
        msg_tokens = self._estimate_messages_tokens([msg])
        if current_tokens + msg_tokens <= target_tokens:
            selected.append(msg)
            current_tokens += msg_tokens
        elif msg["priority"] >= MessagePriority.HIGH:
            # 高优先级消息，压缩后保留
            compressed = self._compress_message(msg)
            compressed_tokens = self._estimate_messages_tokens([compressed])
            if current_tokens + compressed_tokens <= target_tokens:
                selected.append(compressed)
                current_tokens += compressed_tokens
    
    # 6. 重新组装（按时间顺序）
    selected.sort(key=lambda x: x["timestamp"])
    self.context["recent"] = selected + must_keep
    
    removed_count = len(older) - len(selected)
    print(f"✂️ 裁剪了 {removed_count} 条消息")
```

### 消息压缩

```python
def _compress_message(self, message):
    """压缩消息内容"""
    content = message["content"]
    
    # 根据内容类型压缩
    if self._is_error(content):
        # 错误信息：保留错误类型和关键信息
        compressed = f"[错误] {content[:150]}..."
    elif self._is_file_operation(content):
        # 文件操作：保留操作类型和文件名
        compressed = f"[文件操作] {content[:100]}..."
    elif "成功" in content:
        # 成功操作：保留简要描述
        compressed = f"[成功] {content[:80]}..."
    else:
        # 其他：保留摘要
        compressed = f"[操作] {content[:50]}..."
    
    return {
        **message,
        "content": compressed,
        "compressed": True
    }
```

## Token 估算

### 估算方法

```python
def _estimate_tokens(self):
    """估算当前总 token 数"""
    # 永久层
    total = self._estimate_permanent_tokens()
    
    # 重要信息层
    total += self._estimate_important_tokens()
    
    # 最近对话层
    total += self._estimate_messages_tokens(self.context["recent"])
    
    return total

def _estimate_permanent_tokens(self):
    """估算永久层 token"""
    system_tokens = len(self.context["permanent"]["system"]) * 1.2
    task_tokens = len(self.context["permanent"]["task"]) * 1.2
    return int(system_tokens + task_tokens)

def _estimate_important_tokens(self):
    """估算重要信息层 token"""
    error_summary = self._format_error_summary()
    milestone_summary = "\n".join(self.context["important"]["milestones"])
    total_chars = len(error_summary) + len(milestone_summary)
    return int(total_chars * 1.2)

def _estimate_messages_tokens(self, messages):
    """估算消息列表 token"""
    total_chars = sum(len(m["content"]) for m in messages)
    return int(total_chars * 1.2)
```

## 使用示例

### 初始化

```python
agent = VolcArkDoubaoAgent()
agent.set_task("创建一个 Python 计算器程序")
```

### 添加执行结果

```python
# 成功操作
agent.add_message("assistant", "成功创建了 calculator.py 文件")

# 错误信息
agent.add_message("assistant", "错误：NameError: name 'add' is not defined")

# 再次相同错误（会被标记为重复）
agent.add_message("assistant", "错误：NameError: name 'add' is not defined")
```

### 查看上下文状态

```python
print(f"Token 使用率: {agent.get_usage_ratio():.1%}")
print(f"错误历史: {len(agent.context['important']['errors'])} 个")
print(f"最近对话: {len(agent.context['recent'])} 条")
```

## 性能考虑

1. **Token 估算精度**：使用简单的字符数估算，速度快但不够精确
2. **裁剪频率**：只在达到阈值时触发，避免频繁计算
3. **错误历史大小**：限制最多保留 20 个不同的错误签名
4. **里程碑数量**：限制最多保留 10 个里程碑事件

## 未来优化

1. 使用 tiktoken 库进行精确的 token 计算
2. 实现基于语义相似度的智能压缩
3. 支持用户自定义优先级规则
4. 添加上下文持久化和恢复功能
5. 实现更智能的错误分类和聚合
