# Prompts 管理指南

本文档说明项目中 Prompts 的组织结构、命名规范和使用方式。

完整的项目结构说明请参考：[项目结构说明](../understanding/project-structure.md)

## Prompts 目录组织

项目中的 Prompts 分为两个层级：
- **项目级 Prompts** (`prompts/`) - 单一数据源，可被多个 Agent 共享
- **Agent 级 Prompts** (`agents/{agent_name}/prompts/`) - Agent 专属的提示词

## Prompt 文件命名规范

### 1. 项目级 Prompts (`prompts/`)

**命名格式**：`{功能描述}_{版本号}.md`

**示例**：
- `git_commit_angular_001.md` - Git Commit 规范（Angular 风格）
- `code_review_001.md` - 代码审查规范
- `api_design_001.md` - API 设计规范

**用途**：
- 存放可被多个 Agent 共享的 Prompts
- 存放项目级别的规范和标准
- 作为单一数据源，避免重复维护

---

### 2. Agent 级 Prompts (`agents/{agent_name}/prompts/`)

#### 主提示词：`agent.md`（必需）

每个 Agent 必须有一个 `agent.md` 文件，作为该 Agent 的主提示词。

**内容结构**：
```markdown
---
prompt_id: agent
scope: agent_private
version: 1.0.0
description: {Agent 名称} 的主提示词
created: YYYY-MM-DD
---

# {Agent 角色名称}

你是一个...

## 引用的规范

#[[prompt:git_commit_angular_001]]

## 你的核心任务

1. ...
2. ...
```

#### 其他 Prompts：`{功能描述}.md`（可选）

Agent 私有的其他提示词文件。

**示例**：
- `error_handling.md` - 错误处理规范
- `response_format.md` - 响应格式规范

---

## Prompt 元数据规范

每个 Prompt 文件必须包含 YAML front matter 元数据：

```yaml
---
prompt_id: {唯一标识符}
scope: shared | private | selective | agent_private
agents: ["*"] | [] | ["agent1", "agent2"]
version: 1.0.0
description: {简短描述}
tags: ["tag1", "tag2"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**详细的字段定义和使用说明，请参考：[Prompt 元数据规范](../prompts/METADATA-SPEC.md)**

### 字段说明（简要）

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `prompt_id` | ✅ | 唯一标识符 | `git_commit_angular_001` |
| `scope` | ✅ | 共享范围 | `shared`, `private`, `selective`, `agent_private` |
| `agents` | ❌ | 适用的 Agent 列表 | `["*"]`, `[]`, `["agent1"]` |
| `version` | ✅ | 版本号 | `1.0.0` |
| `description` | ✅ | 简短描述 | `用于生成 Git Commit 消息` |
| `tags` | ❌ | 标签 | `["git", "commit"]` |
| `created` | ✅ | 创建日期 | `2026-03-19` |
| `updated` | ❌ | 更新日期 | `2026-03-19` |

### Scope 类型说明

| Scope | 说明 | 导出行为 |
|-------|------|----------|
| `shared` | 全局共享，所有 Agent 可用 | ✅ 导出时自动复制到 Agent |
| `private` | 项目私有，不导出到任何 Agent | ❌ 不导出 |
| `selective` | 选择性共享，只给特定 Agent | ✅ 根据 `agents` 字段决定 |
| `agent_private` | Agent 私有，只属于该 Agent | ✅ 随 Agent 一起导出 |

---

## Prompt 引用语法

在 Prompt 文件中引用其他 Prompt，使用虚拟路径语法：

```markdown
#[[prompt:prompt_id]]
```

### 示例

```markdown
# agents/my first agent/prompts/agent.md

你是一个 Git Commit 助手。

## 遵循的规范

请严格遵循以下规范：

#[[prompt:git_commit_angular_001]]

## 你的任务

根据用户提供的代码变更，生成符合上述规范的 commit 消息。
```

### 引用解析规则

**开发时**（项目内运行 Agent）：
1. AI 读取 `agents/{agent_name}/prompts/agent.md`
2. 发现 `#[[prompt:git_commit_angular_001]]` 引用
3. 先在 `agents/{agent_name}/prompts/` 中查找 → 未找到
4. 向上查找到项目根目录 `prompts/git_commit_angular_001.md` → 找到 ✅

**导出后**（独立 Agent）：
1. AI 读取 `agent/prompts/agent.md`
2. 发现 `#[[prompt:git_commit_angular_001]]` 引用
3. 在 `agent/prompts/` 中查找 → 找到 ✅（导出脚本已复制）

**关键**：引用语法在开发和导出后保持不变，AI 自动处理路径解析。

---

## Agent 导出流程

### 导出命令

```bash
python scripts/export-agent.py "my first agent"
```

### 导出脚本工作流程

1. **复制 Agent 文件**
   - 复制 `agents/{agent_name}/` 下的所有文件
   - 排除 `.export.json`、`__pycache__` 等配置文件

2. **分析 Prompt 引用**
   - 扫描 `prompts/` 目录下的所有 `.md` 文件
   - 提取所有 `#[[prompt:xxx]]` 引用

3. **复制被引用的 Prompts**
   - 从项目根目录 `prompts/` 读取被引用的文件
   - 检查元数据中的 `scope` 字段
   - 只复制 `scope: shared` 或 `scope: selective` 的文件
   - 复制到导出目录的 `prompts/` 文件夹

4. **生成独立 Agent**
   - 导出的 Agent 包含所有必需的 Prompts
   - 引用语法保持不变
   - 完全独立，可直接运行

### 导出前后对比

**开发时结构**：
```
agents/my first agent/
  └── prompts/
      └── agent.md  ← 引用 #[[prompt:git_commit_angular_001]]

prompts/
  └── git_commit_angular_001.md  ← 被引用的文件
```

**导出后结构**：
```
my-first-agent/
  └── prompts/
      ├── agent.md                    ← 引用保持不变
      └── git_commit_angular_001.md   ← 自动复制过来
```

---

## 最佳实践

### 1. 单一数据源原则

- 共享的 Prompts 只在项目根目录 `prompts/` 维护一份
- 通过引用语法在 Agent 中使用
- 避免在多个地方复制相同内容

### 2. 合理使用 Scope

- **通用规范** → `scope: shared`（如 Git Commit 规范、代码审查标准）
- **项目工具** → `scope: private`（如 Prompt 生成器）
- **特定 Agent** → `scope: selective`（如只给某几个 Agent 用的规范）
- **Agent 专属** → `scope: agent_private`（如 Agent 的主提示词）

### 3. 版本管理

- 使用语义化版本号：`1.0.0`
- 重大变更时更新版本号
- 在 `updated` 字段记录更新日期

### 4. 清晰的命名

- 使用描述性的文件名
- 添加版本号后缀（如 `_001`）
- 便于后续扩展和维护

---

## 常见问题

### Q1: 如何添加新的共享 Prompt？

1. 在 `prompts/` 目录创建新文件
2. 添加完整的元数据（设置 `scope: shared`）
3. 在 Agent 的 `agent.md` 中使用 `#[[prompt:xxx]]` 引用
4. 导出时会自动复制

### Q2: Agent 私有的 Prompt 需要设置元数据吗？

需要。所有 Prompt 文件都应该包含元数据，设置 `scope: agent_private`。

### Q3: 如何更新共享 Prompt？

直接修改 `prompts/` 目录下的文件即可。所有引用该 Prompt 的 Agent 会自动使用最新版本。

### Q4: 导出后的 Agent 如何更新 Prompt？

导出后的 Agent 是独立的，需要手动更新其 `prompts/` 目录下的文件，或重新导出。

---

## 相关文档

- [Prompt 元数据规范](../../prompts/METADATA-SPEC.md) - 元数据字段的权威定义
- [项目结构说明](../understanding/project-structure.md) - 项目目录结构
- [Agent 导出指南](./agent-export-guide.md) - Agent 导出说明
