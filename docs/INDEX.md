# 文档索引

本文档提供项目所有文档的快速索引，方便查找和引用。

## 📚 核心文档

### 项目说明
- [README.md](../README.md) - 项目简介和快速导航
- [CHANGELOG.md](../CHANGELOG.md) - 项目更新日志

### 快速入门
- [快速开始](./quick-start.md) - 环境配置和基本使用
- [配置说明](./configuration.md) - 参数配置详解
- [常见问题](./faq.md) - 问题排查和解决方案

---

## 🏗️ 架构和结构

### 项目结构
- [项目结构说明](./project-structure.md) - 目录结构和文件职责的权威文档

### Prompts 管理
- [Prompts 管理指南](./prompts-guide.md) - Prompts 的组织结构和使用方式
- [Prompt 元数据规范](./prompt-metadata-spec.md) - **元数据字段的权威定义**（AI 必读）

### Agent 导出
- [Agent 导出功能使用指南](./agent-export-guide.md) - 如何导出 Agent 为独立包

---

## 💻 开发指南

### 开发规范
- [开发规范](./development-guide.md) - 代码规范、提交规范、Prompt 规范

### 工作流程
- [Git 工作流程](./git-workflow.md) - 分支管理和工作流程
- [开发过程记录指南](./issues-guide.md) - 问题、笔记和想法记录

---

## 🤖 Agent 文档

### Agent 使用文档
- [My First Agent](./agents/my-first-agent.md) - 示例 Agent 使用说明

### Agent 开发
- 创建新 Agent 请参考：[开发规范 - 新增 Agent 流程](./development-guide.md#新增-agent-流程)
- Agent 目录结构请参考：[项目结构说明 - agents 目录](./project-structure.md#agents---ai-agent-代码目录)

---

## 📝 Prompt 文档

### 项目级 Prompts
位于 `prompts/` 目录，详见 [Prompts 管理指南](./prompts-guide.md)

- [Git Commit 规范](../prompts/git_commit_angular_001.md) - Angular 提交规范（scope: shared）
- [Prompt 生成器](../prompts/prompt_generator_001.md) - Prompt 生成工具（scope: private）

### Agent Prompts
位于 `agents/{agent_name}/prompts/` 目录

- 每个 Agent 必须有 `agent.md` 主提示词
- Agent 私有 Prompts 存放在同一目录

---

## 🔧 脚本和工具

### 导出脚本
- [export-agent.py](../scripts/export-agent.py) - Agent 导出脚本
  - 用法：`python scripts/export-agent.py "agent name"`
  - 功能：自动解析引用、复制共享 Prompts、生成独立 Agent

---

## 📖 开发过程记录

### 问题记录
- [用户问题](./issues/problems/user/) - 用户提出的问题
- [AI 问题](./issues/problems/ai/) - AI 开发过程中的问题

### 学习笔记
- [用户笔记](./issues/notes/user/) - 用户的学习笔记
  - [单一数据源与共享资源管理设计](./issues/notes/user/20260319_单一数据源与共享资源管理设计.md)
  - [Agent 导出设计文档](./issues/notes/user/20260319_Agent导出设计文档.md)
- [AI 笔记](./issues/notes/ai/) - AI 的学习记录

### 想法和思路
- [用户想法](./issues/ideas/user/) - 用户的想法和思路
- [AI 想法](./issues/ideas/ai/) - AI 的想法和优化思路

---

## 🎯 快速查找

### 我想了解...

| 需求 | 推荐文档 |
|------|----------|
| 项目是什么 | [README.md](../README.md) |
| 如何开始使用 | [快速开始](./quick-start.md) |
| 目录结构是什么 | [项目结构说明](./project-structure.md) |
| 如何管理 Prompts | [Prompts 管理指南](./prompts-guide.md) |
| Prompt 元数据字段定义 | [Prompt 元数据规范](./prompt-metadata-spec.md) ⭐ |
| 如何导出 Agent | [Agent 导出功能使用指南](./agent-export-guide.md) ⭐ |
| 如何编写代码 | [开发规范](./development-guide.md) |
| 如何提交代码 | [Git 工作流程](./git-workflow.md) |
| 如何创建新 Agent | [开发规范 - 新增 Agent 流程](./development-guide.md#新增-agent-流程) |
| 遇到问题怎么办 | [常见问题](./faq.md) |

### AI 开发者必读

如果你是 AI 助手，正在帮助开发这个项目，以下文档是必读的：

1. **[Prompt 元数据规范](./prompt-metadata-spec.md)** ⭐⭐⭐
   - 所有 Prompt 文件的元数据字段定义
   - 创建或修改 Prompt 时必须参考

2. **[Prompts 管理指南](./prompts-guide.md)** ⭐⭐
   - Prompts 的组织结构
   - 引用语法和导出流程

3. **[Agent 导出功能使用指南](./agent-export-guide.md)** ⭐⭐
   - Agent 导出的完整流程
   - 引用机制和技术细节

4. **[项目结构说明](./project-structure.md)** ⭐⭐
   - 目录结构和文件职责
   - 新增文件时必须参考

5. **[开发规范](./development-guide.md)** ⭐
   - 代码规范和提交规范
   - 开发流程和最佳实践

### 设计文档（深入理解）

如果你想深入理解设计思路和决策过程：

- [单一数据源与共享资源管理设计](./issues/notes/user/20260319_单一数据源与共享资源管理设计.md)
- [Agent 导出设计文档](./issues/notes/user/20260319_Agent导出设计文档.md)

---

## 📌 文档维护

### 更新原则
1. 本索引文档应保持最新
2. 新增文档后必须更新本索引
3. 文档链接失效时及时修复

### 文档层级
- **权威文档**：定义规范和标准（如元数据规范）
- **指南文档**：说明使用方式（如 Prompts 管理指南）
- **参考文档**：提供示例和快速查询（如本索引）

### 相关文档
- [开发过程记录指南](./issues-guide.md) - 如何记录开发过程
- [项目结构说明 - 维护说明](./project-structure.md#维护说明) - 文档维护原则
