# 快速开始

本文档帮助你快速上手 AI Agents 项目。

## 环境要求

- Python 3.7+
- pip 包管理器

## 安装依赖

```bash
pip install requests
```

## 运行示例 Agent

### My First Agent（OpenAI 兼容）

1. 进入 Agent 目录：

```bash
cd "agents/my first agent"
```

2. 配置 API Key（编辑 `main.py`）：

```python
API_KEY = "你的API Key"
MODEL = "Doubao-Seed-2.0-pro"  # 或你的模型名称
```

3. 运行 Agent：

```bash
python main.py
```

4. 开始对话，输入"退出"结束会话。

## 基本使用

### 简单对话

```
你：你好
Agent：你好！有什么我可以帮助你的吗？
```

### 多轮对话

Agent 会自动记住对话历史，支持上下文连续对话：

```
你：我想学习 Python
Agent：Python 是一门很好的编程语言...

你：它有哪些应用场景？
Agent：基于之前提到的 Python，它的应用场景包括...
```

## 下一步

- 查看 [配置说明](./configuration.md) 了解参数调整
- 查看 [贡献指南](../development/contributing.md) 了解如何开发新的 Agent
- 查看 [Git 工作流程](../development/git-workflow.md) 了解分支管理和提交规范
