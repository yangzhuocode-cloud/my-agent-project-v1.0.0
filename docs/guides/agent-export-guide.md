# Agent 导出功能使用指南

本文档详细说明如何使用 Agent 导出功能，将项目中的 Agent 导出为独立可运行的包。

---

## 功能概述

Agent 导出功能允许你将项目中开发的 Agent 导出为完全独立的包，导出的 Agent：

- ✅ 包含所有必需的代码和配置文件
- ✅ 包含所有被引用的共享 Prompts
- ✅ 无需修改任何代码即可运行
- ✅ 完全独立，不依赖项目环境

---

## 快速开始

### 基本用法

```bash
python scripts/export-agent.py "my first agent"
```

导出的 Agent 将保存在 `exports/my-first-agent/` 目录。

### 指定导出目录

```bash
python scripts/export-agent.py "my first agent" --output ./my-exports
```

---

## 导出流程

### 1. 准备工作

确保你的 Agent 符合以下结构：

```
agents/my first agent/
├── config.json          # 运行时配置
├── .export.json         # 导出配置（可选）
├── main.py              # Agent 主程序
├── prompts/
│   └── agent.md         # Agent 主提示词
└── references/          # 参考资料（可选）
```

### 2. 执行导出

运行导出命令：

```bash
python scripts/export-agent.py "my first agent"
```

### 3. 查看输出

导出过程会显示详细信息：

```
📦 开始导出 Agent: my first agent
📂 导出到: D:\...\exports\my-first-agent

📋 复制 Agent 文件:
  ✓ config.json
  ✓ main.py
  ✓ prompts\agent.md
  ✓ references\README.md

🔍 分析 Prompt 引用:
  📎 agent.md 引用: git_commit_angular_001

📄 复制被引用的 Prompt 文件:
  ✓ 复制引用的 prompt: git_commit_angular_001.md (scope: shared)

✅ 导出完成: D:\...\exports\my-first-agent
```

### 4. 验证导出

检查导出目录的结构：

```
exports/my-first-agent/
├── config.json
├── main.py
├── prompts/
│   ├── agent.md
│   └── git_commit_angular_001.md  ← 自动复制的共享 Prompt
└── references/
    └── README.md
```

---

## 导出配置

### .export.json 文件

在 Agent 目录下创建 `.export.json` 文件来配置导出行为：

```json
{
  "exclude_patterns": [
    ".export.json",
    "__pycache__",
    "*.pyc",
    "*.log"
  ]
}
```

**字段说明**：
- `exclude_patterns`：导出时排除的文件模式（支持通配符）

**默认排除**：
- `.export.json` - 导出配置文件本身
- `__pycache__` - Python 缓存目录
- `*.pyc` - Python 编译文件

---

## Prompt 引用机制

### 虚拟路径引用

在 Agent 的 Prompt 文件中使用虚拟路径引用共享 Prompts：

```markdown
# agents/my first agent/prompts/agent.md

你是 Git Commit 助手

## 遵循的规范

#[[prompt:git_commit_angular_001]]

## 你的任务
...
```

### 引用语法

```
#[[prompt:prompt_id]]
```

- `prompt_id`：Prompt 文件的唯一标识符（在元数据中定义）
- 不需要文件扩展名
- 不需要路径

### 工作原理

**开发时**（项目内）：
1. AI 读取 `agents/my first agent/prompts/agent.md`
2. 发现 `#[[prompt:git_commit_angular_001]]` 引用
3. 在当前目录查找 → 未找到
4. 向上查找到项目根目录 `prompts/git_commit_angular_001.md` → 找到 ✅

**导出后**（独立 Agent）：
1. AI 读取 `my-first-agent/prompts/agent.md`
2. 发现 `#[[prompt:git_commit_angular_001]]` 引用
3. 在当前目录查找 → 找到 ✅（导出脚本已复制）

**关键**：引用语法保持不变，AI 自动处理路径解析。

---

## Prompt 元数据

### Scope 控制导出行为

导出脚本根据 Prompt 文件的 `scope` 字段决定是否导出：

```yaml
---
prompt_id: git_commit_angular_001
scope: shared              # 控制导出行为
agents: ["*"]
version: 1.0.0
---
```

### Scope 类型

| Scope | 说明 | 导出行为 |
|-------|------|----------|
| `shared` | 全局共享 | ✅ 被引用时自动导出 |
| `private` | 项目私有 | ❌ 不导出 |
| `selective` | 选择性共享 | ✅ 根据 `agents` 字段决定 |
| `agent_private` | Agent 私有 | ✅ 随 Agent 一起导出 |

### 示例

**共享 Prompt**（会被导出）：
```yaml
---
prompt_id: git_commit_angular_001
scope: shared
agents: ["*"]
---
```

**项目私有 Prompt**（不会被导出）：
```yaml
---
prompt_id: internal_tool_001
scope: private
agents: []
---
```

**选择性共享 Prompt**（只给特定 Agent）：
```yaml
---
prompt_id: auth_handler_001
scope: selective
agents: ["auth-agent", "user-agent"]
---
```

---

## 导出脚本技术细节

### 核心功能

#### 1. 文件复制
- 复制 Agent 目录下的所有文件
- 排除 `.export.json` 和配置的排除模式
- 保留文件元数据（修改时间等）

#### 2. 引用解析
- 扫描 `prompts/` 目录下的所有 `.md` 文件
- 使用正则表达式提取 `#[[prompt:xxx]]` 引用
- 收集所有被引用的 prompt_id

#### 3. 元数据解析
- 读取 Prompt 文件的 YAML front matter
- 提取 `scope`、`agents` 等字段
- 判断是否应该导出

#### 4. 智能复制
- 只复制 `scope: shared` 或 `scope: selective` 的 Prompts
- 从项目根目录 `prompts/` 复制到导出目录的 `prompts/`
- 保持文件名不变

### 正则表达式

**提取引用**：
```python
pattern = r'#\[\[prompt:([^\]]+)\]\]'
matches = re.findall(pattern, content)
# 结果: ['git_commit_angular_001', 'other_prompt']
```

**解析元数据**：
```python
pattern = r'^---\s*\n(.*?)\n---\s*\n'
match = re.match(pattern, content, re.DOTALL)
```

### 文件操作

**复制文件**：
```python
import shutil
shutil.copy2(source_file, dest_file)  # 保留元数据
```

**创建目录**：
```python
from pathlib import Path
dest_file.parent.mkdir(parents=True, exist_ok=True)
```

---

## 常见场景

### 场景 1：导出简单 Agent

**Agent 结构**：
```
agents/simple-agent/
├── config.json
├── main.py
└── prompts/
    └── agent.md  ← 无引用
```

**导出命令**：
```bash
python scripts/export-agent.py "simple-agent"
```

**结果**：
```
exports/simple-agent/
├── config.json
├── main.py
└── prompts/
    └── agent.md
```

### 场景 2：导出带引用的 Agent

**Agent 结构**：
```
agents/my-agent/
├── config.json
├── main.py
└── prompts/
    └── agent.md  ← 引用 #[[prompt:git_commit_angular_001]]
```

**导出命令**：
```bash
python scripts/export-agent.py "my-agent"
```

**结果**：
```
exports/my-agent/
├── config.json
├── main.py
└── prompts/
    ├── agent.md
    └── git_commit_angular_001.md  ← 自动复制
```

### 场景 3：导出带多个引用的 Agent

**Agent 结构**：
```
agents/complex-agent/
├── config.json
├── main.py
└── prompts/
    └── agent.md  ← 引用多个 Prompts
```

**agent.md 内容**：
```markdown
#[[prompt:git_commit_angular_001]]
#[[prompt:code_review_001]]
#[[prompt:api_design_001]]
```

**导出结果**：
```
exports/complex-agent/
├── config.json
├── main.py
└── prompts/
    ├── agent.md
    ├── git_commit_angular_001.md
    ├── code_review_001.md
    └── api_design_001.md
```

---

## 故障排查

### 问题 1：找不到 Agent

**错误信息**：
```
❌ 错误: Agent 不存在: agents/xxx
```

**解决方法**：
- 检查 Agent 名称是否正确（区分大小写）
- 确认 Agent 目录存在于 `agents/` 下

### 问题 2：引用的 Prompt 不存在

**警告信息**：
```
⚠ 警告: 引用的 prompt 文件不存在: prompts/xxx.md
```

**解决方法**：
- 检查 prompt_id 是否正确
- 确认 Prompt 文件存在于项目根目录 `prompts/` 下
- 检查文件名是否匹配（`{prompt_id}.md`）

### 问题 3：Prompt 未被导出

**可能原因**：
- Prompt 的 `scope` 设置为 `private`
- Prompt 的 `scope` 为 `selective`，但 `agents` 列表中没有当前 Agent

**解决方法**：
- 检查 Prompt 文件的元数据
- 修改 `scope` 为 `shared`
- 或在 `agents` 列表中添加当前 Agent 名称

### 问题 4：Python 版本问题

**错误信息**：
```
No global/local python version has been set yet
```

**解决方法**：
```bash
pyenv global 3.7.4
# 或
pyenv local 3.7.4
```

---

## 最佳实践

### 1. 导出前检查

- ✅ 确认 Agent 能够正常运行
- ✅ 检查所有引用的 Prompts 是否存在
- ✅ 验证元数据是否完整

### 2. 命名规范

- Agent 名称使用小写字母和空格
- 导出后自动转换为 kebab-case（如 `my-first-agent`）

### 3. 版本管理

- 在 Prompt 元数据中记录版本号
- 重大变更时更新版本
- 考虑使用 Git 标签标记导出版本

### 4. 测试导出

- 导出后在独立环境中测试
- 验证所有功能是否正常
- 检查引用是否正确解析

---

## 高级用法

### 自定义导出目录

```bash
python scripts/export-agent.py "my-agent" --output /path/to/exports
```

### 批量导出（未来）

```bash
python scripts/export-all-agents.py
```

### 导出验证（未来）

```bash
python scripts/export-agent.py "my-agent" --validate
```

---

## 相关文档

- [Agent 导出设计文档](./issues/notes/user/20260319_Agent导出设计文档.md) - 设计方案和技术细节
- [Prompts 管理指南](./prompts-guide.md) - Prompts 的组织和使用
- [Prompt 元数据规范](./prompt-metadata-spec.md) - 元数据字段定义
- [项目结构说明](./project-structure.md) - 目录结构说明

---

## 总结

Agent 导出功能通过以下机制实现了无缝导出：

1. **虚拟路径引用**：`#[[prompt:id]]` 语法在开发和导出后都能正确工作
2. **元数据驱动**：通过 `scope` 字段控制导出行为
3. **自动依赖解析**：自动发现和复制所有被引用的 Prompts
4. **智能过滤**：只导出必需的文件，排除开发配置

使用这个功能，你可以轻松地将项目中的 Agent 打包分发，无需任何手动操作。
