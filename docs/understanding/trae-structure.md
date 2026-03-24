# Trae 配置目录结构说明

> 🤖 目标读者: AI 助手和开发者 | 🎯 文档类型: 架构说明

本文档详细说明 `.trae/` 目录的结构设计，包括规则（Rules）和技能（Skills）的组织方式。

## 设计原则

### 核心理念

1. **单一入口原则**：Trae 仅需加载 `rules/index.md`，即可索引所有规则和 Skill
2. **规则与 Skill 解耦**：
   - Rule（规则）：定义「能做什么/不能做什么」（边界约束）
   - Skill（技能）：定义「具体怎么做」（执行细则）
3. **优先级分层加载**：按 critical → high → normal 顺序按需加载
4. **关联引用**：通过 `dependencies` 字段和 `#[[file:xxx]]` 实现关联

## 目录结构

```
.trae/
├── rules/                        # 规则目录
│   ├── index.md                  # 唯一入口：所有Rule/Skill的总索引
│   ├── core_rules.md             # 全局核心规则（详细版）
│   └── project_rules.md          # 项目规则入口（Trae自动加载）
└── skills/                       # 技能目录
    ├── critical/                 # 启动必加载的Skill
    │   ├── branch-management/    # Git分支管理规则
    │   │   └── SKILL.md
    │   └── core-boundaries/      # 核心操作边界约束
    │       └── SKILL.md
    ├── high/                     # 场景触发加载的Skill
    │   ├── coding-standards/     # 代码规范
    │   │   └── SKILL.md
    │   └── workflow/             # 工作流程
    │       └── SKILL.md
    └── normal/                   # 显式调用加载的Skill
        └── logging/              # 日志规范
            └── SKILL.md
```

## 文件职责

### 规则文件（Rules）

| 文件 | 职责 | 加载时机 |
|------|------|----------|
| `project_rules.md` | Trae 自动加载的入口文件，包含核心约束摘要 | 启动强制加载 |
| `index.md` | 完整的规则与技能索引表 | 通过引用加载 |
| `core_rules.md` | 详细的核心规则定义 | 通过引用加载 |

### 技能文件（Skills）

| 优先级 | 技能 ID | 职责 | 加载时机 |
|--------|--------|------|----------|
| critical | branch-management | Git Worktree 多分支并行开发规则 | 启动强制加载 |
| critical | core-boundaries | 核心操作边界执行细则 | 启动强制加载 |
| high | coding-standards | 代码规范和编码标准 | 代码编写场景触发 |
| high | workflow | AI 助手工作流程 | 开发流程场景触发 |
| normal | logging | 日志规范和调试指南 | 显式调用时加载 |

## 优先级说明

### critical（启动强制加载）

包含核心规则和不可缺失的 Skill，保障基础运行：

- **branch-management**：分支管理是项目开发的基础，必须始终遵守
- **core-boundaries**：边界约束是安全底线，必须始终生效

### high（场景触发加载）

触发「代码编写/流程执行」场景时自动加载：

- **coding-standards**：编写代码时自动应用规范
- **workflow**：执行开发任务时遵循工作流程

### normal（显式调用加载）

仅当用户显式请求时加载，减少启动负载：

- **logging**：需要调试或查看日志规范时才加载

## 文件格式规范

### 规则文件格式

```yaml
---
rule_id: core-rules
version: 1.0.0
priority: critical
---

# 规则标题

> 目标读者和文档类型说明

## 规则内容

...
```

### 技能文件格式

```yaml
---
skill_id: branch-management
version: 1.0.0
description: Git Worktree 多分支并行开发规则
tags: [Git, Worktree, 分支管理]
priority: critical
dependencies: [core-rules]
---

# 技能标题

> 目标读者和文档类型说明

## 执行细则

...
```

### 关键字段说明

| 字段 | 适用范围 | 说明 |
|------|----------|------|
| `rule_id` | Rules | 规则唯一标识符 |
| `skill_id` | Skills | 技能唯一标识符 |
| `version` | 两者 | 版本号，语义化版本 |
| `priority` | 两者 | 优先级：critical/high/normal |
| `description` | Skills | 简短描述 |
| `tags` | Skills | 标签列表，便于检索 |
| `dependencies` | Skills | 依赖的其他规则或技能 |

## 引用机制

### 规则引用 Skill

在规则文件中引用相关的 Skill：

```markdown
## 关联技能

核心规则依赖以下 Skill 补充细节：
- #[[file:../skills/critical/core-boundaries/SKILL.md]]（核心边界约束）
- #[[file:../skills/critical/branch-management/SKILL.md]]（分支管理规则）
```

### Skill 引用规则

在 Skill 文件中声明依赖：

```yaml
---
skill_id: workflow
dependencies: [core-rules, core-boundaries, branch-management]
---
```

### 索引引用

在入口文件中统一索引：

```markdown
## 技能（Skills）索引

| 优先级 | 技能 ID | 路径 | 加载时机 | 标签 |
|--------|--------|------|----------|------|
| critical | branch-management | ../skills/critical/branch-management/SKILL.md | 启动强制加载 | Git、Worktree、分支管理 |
```

## 与其他配置的关系

### 与 `.kiro/` 的区别

| 目录 | 用途 | 目标读者 |
|------|------|----------|
| `.trae/` | Trae IDE 的规则和技能配置 | AI 助手 |
| `.kiro/` | Kiro IDE 的开发指令 | AI 助手 |

**注意**：本项目使用 Trae IDE，`.kiro/` 目录为历史遗留，可忽略。

### 与 `prompts/` 的关系

| 目录 | 用途 | 内容类型 |
|------|------|----------|
| `.trae/skills/` | AI 助手的执行指令 | 开发规范、工作流程 |
| `prompts/` | Agent 运行时的提示词 | Agent 行为定义 |

**区别**：
- `.trae/skills/` 是给 AI 助手（Trae）看的，指导开发行为
- `prompts/` 是给 Agent 运行时用的，定义 Agent 的角色和行为

## 维护指南

### 新增 Skill

1. 确定优先级（critical/high/normal）
2. 在对应目录下创建 `{skill-name}/SKILL.md`
3. 添加完整的 YAML 元数据
4. 在 `rules/index.md` 中添加索引条目
5. 如有依赖，在 `dependencies` 中声明

### 更新 Skill

1. 修改 SKILL.md 内容
2. 更新 `version` 字段
3. 检查依赖的规则是否需要同步更新

### 删除 Skill

1. 确认没有其他 Skill 或规则依赖它
2. 删除目录
3. 从 `rules/index.md` 中移除索引条目

## 相关文档

- [项目结构说明](./project-structure.md) - 项目整体目录结构
- [设计理念](./design-philosophy.md) - 项目设计理念
- [Prompts 管理指南](../guides/prompts-guide.md) - Prompts 目录说明
