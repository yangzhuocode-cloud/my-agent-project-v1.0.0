# My First Agent

一个基于 OpenAI 兼容 API 的对话 Agent 示例。

## 概述

这是项目中的第一个示例 Agent，展示了如何使用兼容 OpenAI 协议的 API 构建一个具备上下文管理能力的对话 Agent。

## 功能特性

- **OpenAI 协议兼容**：使用标准的 OpenAI API 格式调用 API 服务
- **智能上下文管理**：基于 Token 数量动态管理对话历史
- **真实 Token 统计**：从 API 响应获取精确的 Token 使用情况
- **参数可配置**：温度、Token 数、采样阈值等参数灵活调整
- **错误处理**：完善的异常捕获和错误提示机制
- **自动裁剪**：基于 Token 限制自动清理旧对话

## 技术架构

### 核心类

#### APIModelConfig

配置类，管理所有 API 和模型参数：

```python
class APIModelConfig:
    API_KEY = "你的API Key"
    BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
    MODEL = "Doubao-Seed-2.0-pro"
    TEMPERATURE = 0.7
    MAX_TOKENS = 2000
    TOP_P = 0.9
    STREAM = False
    SYSTEM_PROMPT = "你是一个专业的AI助手"
    MODEL_MAX_TOKENS = 256000  # 256k 上下文窗口
    CONTEXT_SAFETY_RATIO = 0.80  # 保留 80% 给历史
    MAX_CONTEXT_TOKENS = int(MODEL_MAX_TOKENS * CONTEXT_SAFETY_RATIO)
```

#### APIModelAgent

Agent 核心类，负责 API 调用和上下文管理：

- `__init__()`: 初始化配置和上下文
- `_estimate_tokens(messages)`: 估算消息列表的 Token 数（中英文混合）
- `_trim_context()`: 基于 Token 数裁剪上下文，避免超长
- `call_api(user_input)`: 调用 API，显示真实 Token 使用情况

### 工作流程

1. 用户输入添加到上下文
2. 基于估算的 Token 数裁剪上下文（发送前预判）
3. 显示估算的上下文使用率
4. 构造请求头和请求体
5. 发送 POST 请求到 API
6. 解析响应并提取回复内容
7. 从 API 响应的 `usage` 字段获取真实 Token 使用情况
8. 显示精确的上下文使用率和 Token 消耗
9. 将回复添加到上下文
10. 返回回复给用户

### Token 统计机制

本 Agent 采用两阶段 Token 统计：

**发送前（估算）**：
- 使用字符数估算（中文 × 1.8，英文 × 0.25）
- 用于裁剪决策，避免发送超长请求
- 显示格式：`[发送中] 上下文: ~15.2% (~38912 tokens, 估算)`

**收到后（真实）**：
- 从 API 响应的 `usage` 字段提取真实值
- 显示精确的 Token 消耗和使用率
- 显示格式：
  ```
  [真实值] 上下文: 18.5% (47360/256000 tokens)
           本次回复: 280 tokens | 总消耗: 47640 tokens
  ```

### OpenAI 协议依赖

⚠️ **重要说明**：本项目依赖 OpenAI 协议的 `usage` 字段来获取精确的 Token 统计。

**兼容性要求**：
- ✅ 支持标准 OpenAI 协议的模型服务（如 OpenAI、Azure OpenAI 等）
- ✅ 非流式模式（`stream=false`）下，API 必须返回 `usage` 字段
- ⚠️ 非标准协议的模型可能无法正确获取 Token 统计

**降级策略**：
- 如果 API 未返回 `usage` 字段，系统会自动降级到估算模式
- 会显示明确警告：`⚠️ [警告] 当前模型 API 未返回 usage 信息（非标准 OpenAI 协议）`
- 降级模式下的 Token 统计可能不准确，影响上下文管理精度

**推荐的模型服务**：
- OpenAI GPT 系列（官方）
- Azure OpenAI Service
- 火山方舟豆包系列
- 其他声明完全兼容 OpenAI 协议的服务

## 使用方法

### 基本使用

```bash
cd "agents/my first agent"
python main.py
```

### 配置 API

编辑 `main.py`，修改配置：

```python
API_KEY = "你的API Key"
MODEL = "Doubao-Seed-2.0-pro"  # 或其他模型
```

### 自定义角色

修改系统提示词：

```python
SYSTEM_PROMPT = "你是一个 Python 编程专家，擅长解答编程问题"
```

## 配置参数

详细的参数说明请参考 [配置文档](../configuration.md)。

### 常用场景配置

**技术问答**：
```python
TEMPERATURE = 0.5
MAX_TOKENS = 2500
SYSTEM_PROMPT = "你是一个技术专家，提供准确的技术解答"
```

**创意对话**：
```python
TEMPERATURE = 0.9
MAX_TOKENS = 2000
SYSTEM_PROMPT = "你是一个富有创意的对话伙伴"
```

**代码助手**：
```python
TEMPERATURE = 0.3
MAX_TOKENS = 3000
SYSTEM_PROMPT = "你是一个代码助手，帮助用户编写和优化代码"
```

## 扩展开发

### 添加日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在关键位置添加日志
logger.info(f"用户输入：{user_input}")
logger.info(f"API 响应：{assistant_reply}")
```

### 实现上下文持久化

```python
import json

def save_context(self, filename='context.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(self.context, f, ensure_ascii=False, indent=2)

def load_context(self, filename='context.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            self.context = json.load(f)
    except FileNotFoundError:
        pass
```

### 添加命令支持

```python
def handle_command(self, user_input):
    if user_input == '/clear':
        self.context = [{"role": "system", "content": self.config.SYSTEM_PROMPT}]
        return "上下文已清空"
    elif user_input == '/save':
        self.save_context()
        return "上下文已保存"
    # 更多命令...
```

## 常见问题

参考 [常见问题文档](../faq.md) 中的相关章节。

## 文件位置

- 主程序：`agents/my first agent/main.py`
- Prompt 模板：`agents/my first agent/docs/`
- 参考项目：`agents/my first agent/references/`

## 参考项目

本 Agent 开发过程中参考了以下优秀项目：

1. **learn-claude-code** - 从零构建类似 Claude Code 的 Agent
2. **ai-agents-from-scratch** - 使用纯 Python 构建 AI Agent 的完整课程

详细信息请查看：`agents/my first agent/references/README.md`

## 依赖

- Python 3.7+
- requests

## 相关文档

- [快速开始](../guides/quick-start.md)
- [配置说明](../guides/configuration.md)
- [贡献指南](../development/contributing.md)
