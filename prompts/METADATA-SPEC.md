# Prompt 元数据规范

本文档定义了 Prompt 文件的 YAML front matter 元数据规范，是项目中所有 Prompt 文件必须遵循的标准。

## 元数据格式

每个 Prompt 文件必须在文件开头包含 YAML front matter 元数据块：

```markdown
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

# Prompt 内容开始

...
```

## 字段定义

### 必填字段

#### `prompt_id`
- **类型**：字符串
- **必填**：✅ 是
- **说明**：Prompt 的唯一标识符，用于引用和识别
- **命名规范**：
  - 使用小写字母、数字和下划线
  - 项目级 Prompt：`{功能描述}_{版本号}`（如 `git_commit_angular_001`）
  - Agent 主提示词：固定为 `agent`
  - Agent 私有 Prompt：`{功能描述}`（如 `error_handling`）
- **示例**：
  ```yaml
  prompt_id: git_commit_angular_001
  prompt_id: agent
  prompt_id: error_handling
  ```

#### `scope`
- **类型**：枚举字符串
- **必填**：✅ 是
- **可选值**：
  - `shared` - 全局共享，所有 Agent 可用
  - `private` - 项目私有，不导出到任何 Agent
  - `selective` - 选择性共享，只给特定 Agent
  - `agent_private` - Agent 私有，只属于该 Agent
- **说明**：定义 Prompt 的共享范围和导出行为
- **导出行为**：

| Scope | 说明 | 导出行为 |
|-------|------|----------|
| `shared` | 全局共享 | ✅ 被引用时自动导出 |
| `private` | 项目私有 | ❌ 不导出 |
| `selective` | 选择性共享 | ✅ 根据 `agents` 字段决定 |
| `agent_private` | Agent 私有 | ✅ 随 Agent 一起导出 |

- **示例**：
  ```yaml
  scope: shared          # 所有 Agent 可用
  scope: private         # 项目内部使用
  scope: selective       # 特定 Agent 可用
  scope: agent_private   # Agent 专属
  ```

#### `version`
- **类型**：字符串（语义化版本号）
- **必填**：✅ 是
- **格式**：`MAJOR.MINOR.PATCH`
- **说明**：Prompt 的版本号，遵循语义化版本规范
- **版本规则**：
  - `MAJOR`：重大变更，不兼容的修改
  - `MINOR`：新增功能，向后兼容
  - `PATCH`：Bug 修复，向后兼容
- **示例**：
  ```yaml
  version: 1.0.0
  version: 2.1.3
  ```

#### `description`
- **类型**：字符串
- **必填**：✅ 是
- **长度**：建议 100 字以内
- **说明**：Prompt 的简短描述，说明其用途和功能
- **示例**：
  ```yaml
  description: 用于生成符合 Angular 规范的 Git Commit 消息模板
  description: My First Agent 的主提示词
  ```

#### `created`
- **类型**：日期字符串
- **必填**：✅ 是
- **格式**：`YYYY-MM-DD`
- **说明**：Prompt 的创建日期
- **示例**：
  ```yaml
  created: 2026-03-19
  ```

---

### 可选字段

#### `agents`
- **类型**：字符串数组
- **必填**：❌ 否（但 `scope: selective` 时建议填写）
- **说明**：指定哪些 Agent 可以使用此 Prompt
- **特殊值**：
  - `["*"]` - 所有 Agent（通常配合 `scope: shared` 使用）
  - `[]` - 无 Agent（通常配合 `scope: private` 使用）
- **示例**：
  ```yaml
  agents: ["*"]                          # 所有 Agent
  agents: []                             # 无 Agent
  agents: ["my first agent", "agent2"]   # 特定 Agent
  ```

#### `tags`
- **类型**：字符串数组
- **必填**：❌ 否
- **说明**：Prompt 的标签，用于分类和检索
- **示例**：
  ```yaml
  tags: ["git", "commit", "angular", "规范"]
  tags: ["error", "handling"]
  ```

#### `updated`
- **类型**：日期字符串
- **必填**：❌ 否
- **格式**：`YYYY-MM-DD`
- **说明**：Prompt 的最后更新日期
- **示例**：
  ```yaml
  updated: 2026-03-19
  ```

---

## 完整示例

### 示例 1：共享 Prompt

```yaml
---
prompt_id: git_commit_angular_001
scope: shared
agents: ["*"]
version: 1.0.0
description: 用于生成符合 Angular 规范的 Git Commit 消息模板，适配团队协作与版本管理场景
tags: ["git", "commit", "angular", "规范"]
created: 2026-03-18
updated: 2026-03-19
---

## 角色定位

你是一位精通 Git 版本控制和团队协作规范的技术专家...
```

### 示例 2：项目私有 Prompt

```yaml
---
prompt_id: prompt_generator_001
scope: private
agents: []
version: 1.0.0
description: 用于生成各类场景下可直接使用、结构清晰、效果稳定的Prompt
tags: ["prompt", "generator", "工具"]
created: 2026-03-18
updated: 2026-03-19
---

# 专业 Prompt 生成器

你现在是顶级 Prompt 工程师...
```

### 示例 3：Agent 主提示词

```yaml
---
prompt_id: agent
scope: agent_private
version: 1.0.0
description: My First Agent 的主提示词
created: 2026-03-19
---

# Git Commit 消息生成助手

你是一个专业的 Git Commit 消息生成助手...

## 遵循的规范

#[[prompt:git_commit_angular_001]]
```

### 示例 4：选择性共享 Prompt

```yaml
---
prompt_id: auth_handler_001
scope: selective
agents: ["auth-agent", "user-agent"]
version: 1.0.0
description: 用户认证和授权处理规范
tags: ["auth", "security"]
created: 2026-03-19
---

# 认证授权处理规范

...
```

---

## 验证规则

### 必填字段验证
- 所有必填字段必须存在
- 字段值不能为空

### 格式验证
- `version` 必须符合语义化版本格式
- `created` 和 `updated` 必须符合 `YYYY-MM-DD` 格式
- `scope` 必须是四个可选值之一

### 逻辑验证
- `scope: selective` 时，建议填写 `agents` 字段
- `scope: shared` 时，`agents` 通常为 `["*"]`
- `scope: private` 时，`agents` 通常为 `[]`
- `scope: agent_private` 时，不需要 `agents` 字段

---

## 使用场景

### 创建新的共享 Prompt
```yaml
---
prompt_id: new_feature_001
scope: shared
agents: ["*"]
version: 1.0.0
description: 新功能的描述
tags: ["feature"]
created: 2026-03-19
---
```

### 创建 Agent 主提示词
```yaml
---
prompt_id: agent
scope: agent_private
version: 1.0.0
description: {Agent 名称} 的主提示词
created: 2026-03-19
---
```

### 创建 Agent 私有 Prompt
```yaml
---
prompt_id: custom_feature
scope: agent_private
version: 1.0.0
description: Agent 专属功能
created: 2026-03-19
---
```

---

## 工具支持

### 导出脚本
导出脚本 (`scripts/export-agent.py`) 会读取元数据：
- 解析 `scope` 字段决定是否导出
- 使用 `prompt_id` 进行引用匹配
- 检查 `agents` 字段判断适用范围

### 未来扩展
元数据设计支持未来扩展：
- 版本锁定：指定 Agent 使用特定版本的 Prompt
- 依赖管理：`depends_on` 字段声明依赖关系
- 作者信息：`author` 字段记录作者
- 许可证：`license` 字段声明许可证

---

## 相关文档

- [Prompts 管理指南](../docs/guides/prompts-guide.md) - Prompts 的组织结构和使用方式
- [项目结构说明](../docs/understanding/project-structure.md) - 项目目录结构

---

## 维护说明

本文档是 Prompt 元数据的权威规范，任何元数据字段的变更必须：
1. 优先更新本文档
2. 更新相关示例文件
3. 更新导出脚本（如需要）
4. 通知所有开发者

这确保了元数据规范的一致性和可维护性。
