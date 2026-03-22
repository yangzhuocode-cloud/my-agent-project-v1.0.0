---
inclusion: auto
---

# AI Agent 项目 - 核心规则

> 🤖 目标读者: AI 助手 | 🎯 文档类型: 项目规则（必读）

本文件为项目核心规则入口，Trae 每次对话自动加载。

## 基础约束（全局必守）

1. 所有输出（对话/注释/文档）均使用中文
2. 遵循「单一数据源/开发导出分离/人机文档分离/渐进式记录」4大设计原则

## 操作边界（核心）

✅ 允许自动执行：agents/、docs/、prompts/ 下文件的创建/修改
⚠️ 需要确认：删除文件/改结构/导出Agent/重大重构
🚫 禁止操作：修改.git/、.gitignore 排除项、提交敏感信息

## 提交规范（核心）

- 遵循 Angular 规范：#[[prompt:git_commit_angular_001]]
- 提交信息：中文 + 双引号包裹 + 无特殊字符

## 索引引用

完整规则与技能索引见：#[[file:index.md]]
问题索引见：#[[file:../../docs/issues/INDEX-AI.md]]
项目结构见：#[[file:../../docs/understanding/project-structure.md]]
