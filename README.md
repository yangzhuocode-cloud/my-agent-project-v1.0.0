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
- **OpenAI 协议兼容** - 基于标准 OpenAI API 协议，支持主流模型服务

## 项目结构

完整的项目结构和目录说明请参考：[项目结构说明](./docs/understanding/project-structure.md)

## 当前 Agents

### 1. My First Agent

一个基于火山方舟豆包模型的对话 Agent 示例，展示了基本的 API 调用和上下文管理。

- **位置**：`agents/my first agent/`
- **功能**：智能对话、上下文管理、多轮对话
- **文档**：[查看详细文档](./docs/agents/my-first-agent.md)

## 快速开始

### 基础使用

```bash
# 1. 安装依赖
pip install requests

# 2. 运行示例 Agent
cd "agents/my first agent"
python main.py
```

### 使用 Git Worktree 开发

本项目使用 Git Worktree 实现多分支并行开发，避免频繁切换分支。

```bash
# 查看当前 worktree
git worktree list

# 在 worktree 中开发 agent
cd worktrees/my-first-agent
# 编辑代码...
git commit -m "feat(agent): 新功能"

# 在主目录开发框架
cd ../..
# 编辑框架代码...
git commit -m "docs: 更新文档"

# 同步 master 更新到所有 agent 分支
.\scripts\sync-master-to-worktrees.ps1  # Windows
bash scripts/sync-master-to-worktrees.sh  # Linux/Mac
```

详细说明请参考：[Git 工作流程](./docs/development/git-workflow.md)

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

## 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md) 了解项目的所有重要变更。

## 技术说明

### OpenAI 协议兼容性

本项目基于标准 OpenAI API 协议开发，依赖以下关键特性：

- **标准请求格式**：`/v1/chat/completions` 端点
- **usage 字段**：用于精确的 Token 统计和上下文管理
- **非流式模式**：`stream=false` 时返回完整响应

**兼容的模型服务**：
- ✅ OpenAI GPT 系列
- ✅ 火山方舟豆包系列
- ✅ Azure OpenAI Service
- ✅ 其他完全兼容 OpenAI 协议的服务

**潜在兼容性问题**：
- ⚠️ 非标准协议的模型可能无法返回 `usage` 字段
- ⚠️ 自定义 API 端点可能需要适配
- ⚠️ 流式模式下 `usage` 字段的返回时机可能不同

详细说明请参考：[My First Agent 文档](./docs/agents/my-first-agent.md#openai-协议依赖)
