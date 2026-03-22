---
skill_id: workflow
version: 1.0.0
description: AI 助手工作流程
tags: [工作流程, 自动化, 文档同步]
priority: high
dependencies: [core-rules, core-boundaries, branch-management]
---

# AI 助手工作流程

> 🤖 **目标读者**: AI 助手  
> 🎯 **文档类型**: 执行指令

本文件定义 AI 助手在开发过程中的自动化工作流程。

## 核心工作流程

当用户要求修改代码或添加功能时，按以下步骤执行：

### 1. 执行用户请求

- 理解用户需求
- 修改或创建代码
- 添加中文注释和文档字符串
- 保持代码简洁清晰

### 2. 判断是否需要更新文档

根据修改类型，判断需要更新哪些文档：

#### 更新 `docs/understanding/project-structure.md`（如适用）
- 新增或删除目录 → 更新完整目录树
- 调整目录层级 → 更新目录结构
- 修改文件职责 → 更新职责说明
- 新增文件类型 → 更新扩展规范

**重要**：`docs/understanding/project-structure.md` 是项目结构的单一数据源，其他文档不应重复维护项目结构树形图。

#### 文档中的项目结构引用规范

当需要在文档中提及项目结构时：

**禁止**：
- ❌ 在文档中复制粘贴完整的项目结构树形图
- ❌ 在多个文档中维护相同的目录结构说明
- ❌ 创建简化版的项目结构展示
- ❌ 创建示例性的树形结构（即使是局部示例也不行）
- ❌ 使用 `├──`、`└──`、`│` 等符号展示任何目录结构

**唯一例外**：
- ✅ 只有 `docs/understanding/project-structure.md` 可以包含项目结构树形图

**正确做法**：
- ✅ 使用文字引用：`完整的项目结构请参考：[项目结构说明](./docs/understanding/project-structure.md)`
- ✅ 用列表说明相关文件，不展示树形结构
- ✅ 用文字描述目录用途和包含的文件

#### 更新其他相关文档（如适用）
- 配置参数变更 → `docs/guides/configuration.md`
- 使用流程变更 → `docs/guides/quick-start.md`
- Git 工作流程变更 → `docs/development/git-workflow.md`
- 新增常见问题 → `docs/reference/faq.md`

### 3. 自动记录问题（如遇到）

执行过程中遇到错误或问题时：

#### 查重流程
1. 提取问题关键词（2-4 个英文词）
2. 生成 slug（小写，连字符连接）
3. 使用 `fileSearch` 搜索 `docs/issues/problems/ai/{slug}.md`
4. 判断：
   - 找到 → 更新文档，添加"重复发生记录"
   - 未找到 → 创建新文档

#### 创建新问题文档
- 文件名：`docs/issues/problems/ai/{slug}.md`
- 必须包含完整的 YAML 头文件
- 必须包含所有必填章节
- `occurrences` 初始值为 1
- `first_occurred` 和 `last_updated` 设置为当前日期

#### 更新已有问题文档
- 在"重复发生记录"章节末尾添加新记录
- 更新 YAML 中的 `last_updated` 为当前日期
- 更新 `occurrences` 数值加 1

### 4. 响应用户记录请求

用户明确要求记录时：

- 记录问题 → `docs/issues/problems/user/YYYYMMDD_描述.md`
- 记录笔记 → `docs/issues/notes/user/YYYYMMDD_描述.md`
- 记录想法 → `docs/issues/ideas/user/YYYYMMDD_描述.md`

### 5. 提交变更

#### 分支判断规则

提交代码前，必须判断应该提交到哪个分支：

**提交到 master 分支**（框架级别）：
- 项目文档更新（`docs/` 下的通用文档）
- 框架配置文件（`.trae/`、`.gitignore`、`README.md` 等）
- 共享资源（`prompts/`、`scripts/`）
- Git 工作流程相关（`docs/development/git-workflow.md`）
- 学习笔记（`docs/issues/python-learning/`、`docs/issues/git-learning/`）
- 项目结构文档（`docs/understanding/project-structure.md`）

**提交到 feature 分支**（Agent 级别）：
- Agent 代码（`agents/{agent-name}/main.py`）
- Agent 配置（`agents/{agent-name}/config.json`）
- Agent 提示词（`agents/{agent-name}/prompts/`）
- Agent 文档（`docs/agents/{agent-name}.md`）
- Agent 特定的问题记录

**判断逻辑**：
1. 如果用户明确指定分支 → 使用指定分支
2. 如果修改的是 `agents/{agent-name}/` 下的文件 → 使用对应的 feature 分支
3. 如果修改的是框架文件或通用文档 → 使用 master 分支
4. 如果同时修改了框架和 Agent → 分两次提交

**当前项目的 Worktree 结构**：
```
my-agent-project-v1.0.0/              ← master 分支（主目录）
└── worktrees/
    └── my-first-agent/               ← feature/my-first-agent 分支
```

**提交位置**：
- master 分支：在主目录 `my-agent-project-v1.0.0/` 提交
- feature 分支：在 `worktrees/my-first-agent/` 提交

#### 提交规范

- 使用规范的中文提交信息（Angular 规范）
- 提交信息必须用双引号包裹
- 引用 `#[[prompt:git_commit_angular_001]]` 规范

## 新增 Agent 流程

完整的新增 Agent 流程：

### 1. 创建 Agent 目录结构

创建标准的 Agent 目录，包含以下必需文件：
- `main.py` - Agent 主程序
- `config.json` - 运行时配置
- `.export.json` - 导出配置
- `prompts/agent.md` - Agent 主提示词

完整的目录结构和文件说明请参考：[项目结构说明](../../../docs/understanding/project-structure.md)

### 2. 实现 Agent 核心功能
- 编写 `main.py`
- 配置 `config.json`
- 创建主提示词 `agent.md`

### 3. 创建使用文档
- 在 `docs/agents/{agent-name}.md` 创建详细文档
- 包含功能介绍、使用方法、配置说明

### 4. 更新项目文档
- 更新 `README.md` 的"当前 Agents"章节
- 更新 `docs/understanding/project-structure.md`（如有新目录类型）

### 5. 提交变更
- 使用 `feat(agent): 添加 {agent-name}` 格式提交

## 文档同步规范

### 核心原则

- **`.trae/skills/`**：给 AI 助手读的开发指令总入口
- **`docs/`**：给人类开发者读的理解性文档
- **`README.md`**：项目门户和快速导航

### 同步触发条件

| 修改类型 | 需要同步的文档 |
|---------|---------------|
| 新增/删除目录 | `docs/understanding/project-structure.md` |
| 新增/删除 Agent | `README.md`, `docs/agents/{name}.md` |
| 修改配置参数 | `docs/guides/configuration.md` |
| 修改使用流程 | `docs/guides/quick-start.md` |

## 问题记录规范

### AI 问题文档格式

```yaml
---
slug: 问题的唯一标识符
keywords: [关键词1, 关键词2]
first_occurred: YYYY-MM-DD
last_updated: YYYY-MM-DD
occurrences: N
---

# 问题标题

## 问题描述
详细说明问题现象

## 问题原因分析
分析根本原因

## 解决方案
具体解决方法

## 重复发生记录

### 第 1 次：YYYY-MM-DD HH:MM
- **场景**：具体场景
- **处理**：如何解决

### 第 2 次：YYYY-MM-DD HH:MM
- **场景**：具体场景
- **处理**：如何解决
- **反思**：为什么再次发生
```

### 触发条件

自动创建或更新问题文档的情况：

1. **命令执行失败**
   - Git 命令报错
   - Shell 命令执行失败
   - API 调用失败

2. **重复性错误**
   - 同一错误在本次会话中第二次出现
   - 更新已有文档，添加重复记录

3. **配置或环境问题**
   - 依赖缺失
   - 配置错误
   - 权限问题

## Prompts 引用处理

### 开发时引用解析

```
读取 agent.md
    ↓
发现 #[[prompt:id]]
    ↓
在 agents/{name}/prompts/ 中查找
    ↓ (未找到)
在项目 prompts/ 中查找
    ↓ (找到)
加载并使用
```

### 导出时引用处理

由导出脚本自动处理：
1. 扫描所有 Prompt 文件
2. 提取 `#[[prompt:xxx]]` 引用
3. 复制被引用的共享 Prompts
4. 保持引用语法不变
