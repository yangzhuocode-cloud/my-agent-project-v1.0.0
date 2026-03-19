# AI Agents 项目

一个灵活、可扩展的 AI Agent 开发框架，支持快速创建、管理和导出 AI Agent。

## 项目愿景

构建一个开发者友好的 AI Agent 框架，让开发者能够：
- 快速创建和部署 AI Agent
- 通过引用机制复用 Prompts 和配置
- 将 Agent 导出为完全独立的可运行包
- 记录和沉淀开发过程中的知识

## 核心特性

- **单一数据源** - 共享 Prompts 只维护一份，通过引用使用
- **开发与导出分离** - 开发时灵活引用，导出后完全独立
- **人机分离的文档** - 人类看理解性文档，AI 看执行性指令
- **知识沉淀机制** - 自动记录问题、笔记和想法

## 项目结构

```
AI-Agents/
├── agents/           # AI Agent 代码
├── prompts/          # 项目级 Prompts（单一数据源）
├── docs/             # 人类文档
│   ├── understanding/    # 理解项目
│   ├── guides/          # 使用指南
│   ├── development/     # 开发指南
│   └── reference/       # 参考资料
└── .kiro/steering/   # AI 指令
```

完整的项目结构和设计理念请参考：
- [项目结构说明](./docs/understanding/project-structure.md)
- [设计理念](./docs/understanding/design-philosophy.md)
- [架构设计](./docs/understanding/architecture.md)

## 当前 Agents

### 1. My First Agent

一个基于火山方舟豆包模型的对话 Agent 示例，展示了基本的 API 调用和上下文管理。

- **位置**：`agents/my first agent/`
- **功能**：智能对话、上下文管理、多轮对话
- **文档**：[查看详细文档](./docs/agents/my-first-agent.md)

## 快速开始

```bash
# 1. 安装依赖
pip install requests

# 2. 运行示例 Agent
cd "agents/my first agent"
python main.py
```

详细说明请参考：[快速开始指南](./docs/guides/quick-start.md)

## Agent 导出

将 Agent 导出为完全独立的可运行包：

```bash
python scripts/export-agent.py "my first agent"
```

导出的 Agent 包含所有必需的代码、配置和 Prompts，可直接分享和运行。

详细说明：[Agent 导出指南](./docs/guides/agent-export-guide.md)

## 文档导航

📖 **[完整文档索引](./docs/INDEX.md)**

### 理解项目
- [设计理念](./docs/understanding/design-philosophy.md) - 为什么这样设计
- [架构设计](./docs/understanding/architecture.md) - 技术架构和组件
- [项目结构](./docs/understanding/project-structure.md) - 目录结构详解

### 使用指南
- [快速开始](./docs/guides/quick-start.md) - 快速上手
- [配置说明](./docs/guides/configuration.md) - 参数配置
- [Prompts 管理](./docs/guides/prompts-guide.md) - Prompts 使用
- [Agent 导出](./docs/guides/agent-export-guide.md) - 导出独立包

### 开发指南
- [贡献指南](./docs/development/contributing.md) - 如何贡献
- [Git 工作流程](./docs/development/git-workflow.md) - 分支和提交

### 参考资料
- [Prompt 元数据规范](./docs/reference/prompt-metadata-spec.md) - 元数据定义
- [开发记录指南](./docs/reference/issues-guide.md) - 问题记录
- [常见问题](./docs/reference/faq.md) - FAQ

## 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md) 了解项目的所有重要变更。
