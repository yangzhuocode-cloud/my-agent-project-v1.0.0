# 配置说明

本文档说明各个 Agent 的配置参数和调整方法。

## My First Agent 配置

### API 配置

在 `agents/my first agent/main.py` 的 `VolcArkDoubaoConfig` 类中配置：

```python
class VolcArkDoubaoConfig:
    # API 认证
    API_KEY = "你的API Key"
    BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"
    MODEL = "Doubao-Seed-2.0-pro"
```

### 模型参数

```python
# 生成参数
TEMPERATURE = 0.7    # 随机性控制（0-1）
MAX_TOKENS = 2000    # 最大回复长度
TOP_P = 0.9          # 采样阈值
STREAM = False       # 是否启用流式输出
```

#### 参数说明

- **TEMPERATURE**：控制回复的随机性和创造性
  - 0.0：确定性强，回复更保守
  - 1.0：随机性强，回复更有创意
  - 推荐：0.7（平衡）

- **MAX_TOKENS**：单次回复的最大 Token 数
  - 建议范围：1000-4000
  - 默认：2000

- **TOP_P**：核采样阈值
  - 控制词汇选择的多样性
  - 推荐：0.9

### 上下文配置

```python
# 上下文管理
SYSTEM_PROMPT = "你是一个专业的AI助手，基于豆包模型提供回答"
CONTEXT_MAX_LENGTH = 10  # 最大保留对话轮数
```

#### 参数说明

- **SYSTEM_PROMPT**：定义 Agent 的角色和行为
  - 可自定义为特定领域专家
  - 示例：`"你是一个 Python 编程专家"`

- **CONTEXT_MAX_LENGTH**：保留的对话历史轮数
  - 默认：10 轮
  - 增加会占用更多 Token，但保持更长的记忆

## 通用配置建议

### 对话场景

- **闲聊对话**：TEMPERATURE=0.8, MAX_TOKENS=1500
- **技术问答**：TEMPERATURE=0.5, MAX_TOKENS=2500
- **代码生成**：TEMPERATURE=0.3, MAX_TOKENS=3000
- **创意写作**：TEMPERATURE=0.9, MAX_TOKENS=2000

### 性能优化

- 减少 `CONTEXT_MAX_LENGTH` 可降低 API 调用成本
- 减少 `MAX_TOKENS` 可加快响应速度
- 关闭 `STREAM` 可简化错误处理

## 获取 API Key

1. 访问 [火山方舟控制台](https://console.volcengine.com/ark)
2. 创建或选择应用
3. 在 API 管理中获取 API Key
4. 复制 Key 并配置到项目中
