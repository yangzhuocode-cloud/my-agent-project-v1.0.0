# Git 分支管理规则

> 🎯 **重要**: 本项目使用 Git Worktree 进行多分支并行开发

## 分支结构

### 主分支（master）
- **位置**: 项目根目录
- **用途**: 项目框架、通用文档、共享资源
- **包含内容**:
  - 项目结构文档
  - 通用开发指南
  - 共享的 Prompts
  - 项目级参考资源
  - 脚本工具

### Agent 子分支
- **位置**: `worktrees/{agent-name}/`
- **用途**: 单个 Agent 的开发和迭代
- **包含内容**:
  - Agent 代码实现
  - Agent 配置文件
  - Agent 开发文档
  - Agent 特定的 Prompts
  - Agent 参考项目

## 目录对应关系

### 主分支目录（项目根目录）

```
AI-Agents/                          # 主分支根目录
├── .kiro/                          # Kiro 配置（主分支）
├── docs/                           # 项目文档（主分支）
│   ├── agents/                     # Agent 使用文档（面向用户）
│   ├── understanding/              # 项目理解文档
│   ├── guides/                     # 使用指南
│   ├── development/                # 开发指南
│   └── issues/                     # 开发记录
├── prompts/                        # 共享 Prompts（主分支）
├── references/                     # 项目级参考资源（主分支）
├── scripts/                        # 项目脚本（主分支）
└── agents/                         # ⚠️ 主分支不包含 Agent 实现
    └── my first agent/             # ⚠️ 仅作为占位，实际开发在 worktree
        ├── .export.json            # 导出配置（主分支维护）
        └── config.json             # 基础配置（主分支维护）
```

### Agent 子分支目录（worktrees 下）

```
worktrees/my-first-agent/           # my-first-agent 分支根目录
├── .kiro/                          # Kiro 配置（继承自主分支）
├── docs/                           # 项目文档（继承自主分支）
├── prompts/                        # 共享 Prompts（继承自主分支）
├── references/                     # 项目级参考（继承自主分支）
├── scripts/                        # 项目脚本（继承自主分支）
└── agents/
    └── my first agent/             # ✅ Agent 实际开发目录
        ├── main.py                 # Agent 代码（子分支）
        ├── config.json             # 运行配置（子分支）
        ├── .export.json            # 导出配置（子分支）
        ├── docs/                   # ✅ Agent 开发文档（子分支）
        │   ├── README.md
        │   ├── development-log.md
        │   ├── context-management.md
        │   └── adr/
        ├── prompts/                # Agent Prompts（子分支）
        │   └── agent.md
        └── references/             # Agent 参考（子分支）
```

## 开发规则

### 规则 1: 主分支开发范围

**只在主分支修改以下内容**：
- ✅ 项目结构文档（`docs/understanding/project-structure.md`）
- ✅ 项目级开发指南（`docs/development/`）
- ✅ 项目级架构决策（`docs/understanding/adr/`）
- ✅ 共享 Prompts（`prompts/`）
- ✅ 项目脚本（`scripts/`）
- ✅ Kiro 配置（`.kiro/`）
- ✅ Agent 使用文档（`docs/agents/`，面向用户）

**不在主分支修改**：
- ❌ Agent 代码实现（`agents/{name}/main.py`）
- ❌ Agent 开发文档（`agents/{name}/docs/`）
- ❌ Agent 特定 Prompts（`agents/{name}/prompts/`）

### 规则 2: Agent 子分支开发范围

**只在 Agent 子分支修改以下内容**：
- ✅ Agent 代码（`agents/{name}/main.py`）
- ✅ Agent 配置（`agents/{name}/config.json`）
- ✅ Agent 开发文档（`agents/{name}/docs/`）
- ✅ Agent Prompts（`agents/{name}/prompts/`）
- ✅ Agent 参考项目（`agents/{name}/references/`）

**不在子分支修改**：
- ❌ 项目级文档（`docs/understanding/`、`docs/development/`）
- ❌ 共享 Prompts（`prompts/`）
- ❌ 项目脚本（`scripts/`）

### 规则 3: 特殊情况

**Agent 使用文档**（`docs/agents/{name}.md`）：
- 在子分支开发时更新
- 稳定后合并到主分支
- 面向用户，说明如何使用 Agent

## 工作流程

### 开发 Agent 功能

1. **切换到 Agent 子分支**
   ```bash
   cd worktrees/my-first-agent
   git status  # 确认在正确分支
   ```

2. **修改 Agent 代码和文档**
   ```bash
   # 修改代码
   vim agents/my\ first\ agent/main.py
   
   # 更新开发文档
   vim agents/my\ first\ agent/docs/development-log.md
   ```

3. **提交到子分支**
   ```bash
   git add agents/my\ first\ agent/
   git commit -m "feat(agent): 实现智能上下文裁剪"
   ```

### 更新项目文档

1. **切换到主分支**
   ```bash
   cd ../../  # 回到项目根目录
   git status  # 确认在 master 分支
   ```

2. **修改项目文档**
   ```bash
   vim docs/understanding/project-structure.md
   ```

3. **提交到主分支**
   ```bash
   git add docs/understanding/
   git commit -m "docs: 更新项目结构说明"
   ```

## 提交规范

### 主分支提交

```bash
# 项目文档
git commit -m "docs: 更新项目结构文档"

# 开发指南
git commit -m "docs: 添加分支管理规则"

# 共享资源
git commit -m "feat: 添加新的共享 Prompt"

# 项目脚本
git commit -m "feat: 添加 worktree 同步脚本"
```

### Agent 子分支提交

```bash
# Agent 功能
git commit -m "feat(agent): 实现分层上下文存储"

# Agent 文档
git commit -m "docs(agent): 记录上下文管理策略"

# Agent 配置
git commit -m "chore(agent): 更新模型配置"

# Agent 修复
git commit -m "fix(agent): 修复 token 估算错误"
```

## 检查清单

### 提交前检查

**在主分支提交前**：
- [ ] 确认当前在主分支（`git branch` 显示 `* master`）
- [ ] 确认修改的是项目级文件（不是 `agents/{name}/` 下的实现）
- [ ] 确认提交信息使用项目级前缀（`docs:`, `feat:`, `chore:`）

**在 Agent 子分支提交前**：
- [ ] 确认当前在正确的 worktree（`pwd` 显示 `worktrees/{agent-name}`）
- [ ] 确认修改的是 Agent 相关文件（`agents/{name}/` 下）
- [ ] 确认提交信息使用 Agent 前缀（`feat(agent):`, `docs(agent):`）

### 常见错误

❌ **错误 1**: 在主分支修改 Agent 代码
```bash
# 主分支
vim agents/my\ first\ agent/main.py  # ❌ 错误！
```

✅ **正确做法**:
```bash
cd worktrees/my-first-agent
vim agents/my\ first\ agent/main.py  # ✅ 正确
```

❌ **错误 2**: 在子分支修改项目文档
```bash
# worktree 中
vim docs/understanding/project-structure.md  # ❌ 错误！
```

✅ **正确做法**:
```bash
cd ../../  # 回到主分支
vim docs/understanding/project-structure.md  # ✅ 正确
```

## 分支同步

### 主分支更新同步到子分支

当主分支的共享资源更新后，需要同步到子分支：

```bash
# 在主分支
git commit -m "feat: 更新共享 Prompt"

# 同步到所有 worktree
./scripts/sync-master-to-worktrees.sh
```

### 子分支合并到主分支

当 Agent 开发完成，需要合并到主分支：

```bash
# 在主分支
git merge my-first-agent

# 解决冲突（如果有）
# 提交合并
```

## 快速参考

| 操作 | 主分支 | Agent 子分支 |
|------|--------|-------------|
| 位置 | 项目根目录 | `worktrees/{agent-name}/` |
| 修改项目文档 | ✅ | ❌ |
| 修改 Agent 代码 | ❌ | ✅ |
| 修改 Agent 文档 | ❌ | ✅ |
| 修改共享 Prompts | ✅ | ❌ |
| 修改项目脚本 | ✅ | ❌ |
| 提交前缀 | `docs:`, `feat:` | `feat(agent):`, `docs(agent):` |

## 相关文档

- [Git Worktree 工作流程](../../docs/development/git-workflow.md)
- [Git Worktree 多分支并行开发](../../docs/issues/git-learning/01-git-worktree多分支并行开发.md)
- [PR 工作流与分支同步](../../docs/issues/git-learning/02-PR工作流与分支同步.md)
