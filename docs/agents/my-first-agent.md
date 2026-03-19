# My First Agent

一个基于火山方舟豆包模型的对话 Agent 示例。

## 概述

这是项目中的第一个示例 Agent，展示了如何使用火山方舟平台的豆包模型构建一个具备上下文管理能力的对话 Agent。

## 功能特性

- **OpenAI 协议兼容**：使用标准的 OpenAI API 格式调用火山方舟服务
- **上下文管理**：自动维护对话历史，支持多轮连续对话
- **参数可配置**：温度、Token 数、采样阈值等参数灵活调整
- **错误处理**：完善的异常捕获和错误提示机制
- **自动裁剪**：超过最大轮数时自动清理旧对话

## 技术架构

### 核心类

#### VolcArkDoubaoConfig

配置类，管理所有 API 和模型参数：

```python
class VolcArkDoubaoConfig:
    API_KEY = "你的API Key"
    BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"
    MODEL = "Doubao-Seed-2.0-pro"
    TEMPERATURE = 0.7
    MAX_TOKENS = 2000
    TOP_P = 0.9
    STREAM = False
    SYSTEM_PROMPT = "你是一个专业的AI助手，基于豆包模型提供回答"
    CONTEXT_MAX_LENGTH = 10
```

#### VolcArkDoubaoAgent

Agent 核心类，负责 API 调用和上下文管理：

- `__init__()`: 初始化配置和上下文
- `_trim_context()`: 裁剪上下文，避免超长
- `call_volc_ark_api(user_input)`: 调用火山方舟 API

### 工作流程

1. 用户输入添加到上下文
2. 检查并裁剪上下文长度
3. 构造请求头和请求体
4. 发送 POST 请求到火山方舟 API
5. 解析响应并提取回复内容
6. 将回复添加到上下文
7. 返回回复给用户

## 使用方法

### 基本使用

```bash
cd "agents/my first agent"
python main.py
```

### 配置 API

编辑 `main.py`，修改配置：

```python
API_KEY = "你的火山方舟API Key"
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

- [快速开始](../quick-start.md)
- [配置说明](../configuration.md)
- [开发规范](../development-guide.md)
