# AI Agents 项目

一个通用的 AI Agent 开发和管理项目，用于构建、组织和维护各类 AI Agent。

## 项目简介

本项目提供了一个灵活的框架，用于开发和管理不同类型的 AI Agent。每个 Agent 都是独立的模块，可以根据具体需求进行定制和扩展。

## 项目结构

```
AI-Agents/
├── agents/                    # AI Agent 代码目录
│   └── my first agent/       # 示例对话 Agent
│       ├── main.py           # Agent 主程序
│       ├── docs/             # Agent 运行资源
│       └── references/       # Agent 特定参考项目（可选）
├── docs/                     # 项目文档目录
│   ├── agents/               # Agent 使用文档
│   └── issues/               # 开发过程记录
├── references/               # 项目级通用参考资源
│   └── ollama-python/        # Ollama Python SDK
└── .kiro/                    # Kiro IDE 配置
```

完整的项目结构和文件职责说明请参考：[项目结构说明](./docs/project-structure.md)

## 当前 Agents

### 1. My First Agent

一个基于火山方舟豆包模型的对话 Agent 示例，展示了基本的 API 调用和上下文管理。

- **位置**：`agents/my first agent/`
- **功能**：智能对话、上下文管理、多轮对话
- **文档**：[查看详细文档](./docs/agents/my-first-agent.md)

## 快速开始

详细的安装、配置和使用说明，请参考：

- [快速开始指南](./docs/quick-start.md)
- [开发规范](./docs/development-guide.md)
- [配置说明](./docs/configuration.md)

## Agent 导出功能

项目提供了 Agent 导出功能，可以将开发的 Agent 导出为完全独立的包：

```bash
python scripts/export-agent.py "my first agent"
```

导出的 Agent 包含所有必需的代码、配置和 Prompts，无需修改即可运行。

详细说明请参考：[Agent 导出功能使用指南](./docs/agent-export-guide.md)

## 文档

📖 **[完整文档索引](./docs/INDEX.md)** - 快速查找所有文档

### 快速入门
- [快速开始](./docs/quick-start.md) - 环境配置和基本使用
- [配置说明](./docs/configuration.md) - 参数配置详解

### 开发指南
- [开发规范](./docs/development-guide.md) - 代码规范和提交规范
- [项目结构说明](./docs/project-structure.md) - 目录结构和文件职责
- [Prompts 管理指南](./docs/prompts-guide.md) - Prompts 组织和使用
- [Prompt 元数据规范](./docs/prompt-metadata-spec.md) - 元数据字段定义

### 工作流程
- [Git 工作流程](./docs/git-workflow.md) - 分支管理和工作流程
- [开发过程记录指南](./docs/issues-guide.md) - 问题、笔记和想法记录

### 其他
- [常见问题](./docs/faq.md) - 问题排查和解决方案

## 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md) 了解项目的所有重要变更。
