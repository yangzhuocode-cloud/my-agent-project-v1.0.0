# Trae 规则与技能总索引

> 单一入口：Trae 检索的唯一元数据入口

## 全局核心规则（启动强制加载）

| 规则 ID | 路径 | 描述 |
|--------|------|------|
| core-rules | ./core_rules.md | 项目全局必守规则 |

## 技能（Skills）索引

| 优先级 | 技能 ID | 路径 | 加载时机 | 标签 |
|--------|--------|------|----------|------|
| critical | branch-management | ../skills/critical/branch-management/SKILL.md | 启动强制加载 | Git、Worktree、分支管理 |
| critical | core-boundaries | ../skills/critical/core-boundaries/SKILL.md | 启动强制加载 | 边界、安全、核心约束 |
| high | coding-standards | ../skills/high/coding-standards/SKILL.md | 代码编写场景触发 | 代码规范、Python、PEP8 |
| high | workflow | ../skills/high/workflow/SKILL.md | 开发流程场景触发 | 工作流程、自动化 |
| normal | logging | ../skills/normal/logging/SKILL.md | 显式调用时加载 | 日志、调试、监控 |

## 索引说明

1. **critical**：启动时强制加载，包含核心规则和不可缺失的 Skill
2. **high**：触发「代码编写/流程执行」场景时自动加载
3. **normal**：仅当用户显式请求「日志调试」时加载

## 关联文档

- [项目结构说明](../../docs/understanding/project-structure.md)
- [问题索引](../../docs/issues/INDEX-AI.md)
