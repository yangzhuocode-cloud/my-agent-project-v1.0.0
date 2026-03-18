# 更新日志

本文档记录项目的所有重要变更。

## 2026-03-19

### 新增

- 新增开发过程记录目录结构 `docs/issues/`
- 支持分类记录问题（problems）、笔记（notes）、想法（ideas）
- 区分用户和 AI 的记录内容
- 新增 `docs/issues-guide.md` 开发过程记录指南
- 新增 AI 问题文档格式规范（YAML 头文件 + 标准章节）

### 优化

- AI 问题文档使用 slug 命名（如 `git-commit-quote-error.md`），方便查询和去重
- User 文档使用时间前缀命名（如 `20260319_描述.md`），方便按时间查看
- 完善 `.kiro/steering/main.md` 中的 AI 工作流程和文档规范

### 文档

- 重构文档结构，明确 AI 指令与人类文档的职责分离
- 完善 `main.md` 同步规范
- 新增开发过程记录指南文档

## 2026-03-18

### 新增

- 初始化项目结构
- 添加第一个示例 Agent（火山方舟豆包）
- 建立项目开发规范和文档体系

### 文档

- 创建 `README.md` 项目说明
- 创建 `docs/quick-start.md` 快速开始指南
- 创建 `docs/configuration.md` 配置说明
- 创建 `docs/development-guide.md` 开发规范
- 创建 `docs/faq.md` 常见问题
- 创建 `.kiro/steering/main.md` AI 开发指令
