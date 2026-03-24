# ADR-001: OpenAI 协议兼容

## 状态
已接受

## 背景

在开发 My First Agent 时，需要选择与 LLM 服务通信的协议格式。主要考虑的选项有：

1. 使用 API 提供商的原生 API 格式
2. 使用 OpenAI 协议格式（兼容）
3. 自定义协议格式

关键需求：
- 需要获取精确的 Token 使用统计
- 需要支持上下文管理
- 希望代码具有可移植性
- 希望有良好的生态支持

## 决策

我们决定使用 **OpenAI 协议格式**与 API 服务通信。

具体实现：
```python
# 使用 OpenAI 兼容的端点
BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"

# 使用标准的 OpenAI 消息格式
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]

# 调用标准的 chat/completions 端点
response = requests.post(
    url=f"{BASE_URL}/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"model": MODEL, "messages": messages}
)
```

## 后果

### 正面影响

1. **标准化**：使用业界标准协议，代码易于理解和维护
2. **可移植性**：可以轻松切换到其他支持 OpenAI 协议的服务（OpenAI、Azure OpenAI 等）
3. **生态支持**：可以使用 OpenAI 生态的工具和库（如 tiktoken）
4. **Token 统计**：可以从标准的 `usage` 字段获取精确的 Token 统计
5. **文档丰富**：OpenAI 协议有大量文档和示例代码

### 负面影响

1. **协议依赖**：依赖服务商对 OpenAI 协议的兼容性
   - 缓解措施：大多数 API 提供商声明兼容 OpenAI 协议
   
2. **特性限制**：无法使用特定 API 提供商特有的功能
   - 缓解措施：当前需求不涉及特有功能
   
3. **兼容性风险**：如果服务商的 OpenAI 协议实现不完整，可能遇到问题
   - 缓解措施：实现降级策略，当 `usage` 字段缺失时使用估算

### 技术债务

1. 需要实现降级策略处理非标准协议的服务
2. 需要文档说明对 OpenAI 协议的依赖

## 替代方案

### 方案1：使用 API 提供商原生 API

**优点**：
- 可以使用所有 API 提供商特有功能
- 不依赖协议兼容性

**缺点**：
- 代码与特定 API 提供商强耦合，难以迁移
- 需要学习特有的 API 格式
- 生态支持较少

**为什么不选**：可移植性差，不符合长期发展需求

### 方案2：自定义协议格式

**优点**：
- 完全控制协议格式
- 可以针对需求优化

**缺点**：
- 需要为每个 LLM 服务编写适配器
- 维护成本高
- 没有生态支持

**为什么不选**：过度设计，维护成本过高

## 实现细节

### Token 统计的实现

依赖 OpenAI 协议的 `usage` 字段：

```python
response = {
    "choices": [...],
    "usage": {
        "prompt_tokens": 1234,
        "completion_tokens": 567,
        "total_tokens": 1801
    }
}
```

### 降级策略

当 `usage` 字段缺失时：

```python
if "usage" not in result:
    print("⚠️ [警告] 当前模型 API 未返回 usage 信息（非标准 OpenAI 协议）")
    print("⚠️ [警告] 将使用估算值，可能不准确")
    # 使用估算值
```

## 验证

通过以下方式验证决策的正确性：

1. ✅ 成功调用 API 并获取响应
2. ✅ 成功从 `usage` 字段获取 Token 统计
3. ✅ 消息格式与 OpenAI 官方文档一致
4. ✅ 可以使用 OpenAI 生态的工具（如 tiktoken）

## 参考资料

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [OpenAI 协议规范](https://github.com/openai/openai-openapi)
