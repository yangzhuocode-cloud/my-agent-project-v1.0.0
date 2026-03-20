# Git 工作流程

本文档定义了项目的 Git 分支管理和工作流程规范。

## 分支策略

### 主分支（master）

主分支只包含项目框架和通用内容：

- 项目文档结构
- 通用配置文件
- README.md、CHANGELOG.md
- 共享的提示词和工具

### Agent 开发分支

每个新 Agent 在独立分支开发，开发完成后合并到主分支。

## Git Worktree 工作模式

为了避免频繁切换分支，本项目使用 Git Worktree 实现多分支并行开发。

### 目录结构

```
my-agent-project-v1.0.0/              ← master 分支（主目录）
├── .git/                             ← Git 仓库
├── worktrees/                        ← 存放所有 agent 开发分支
│   ├── my-first-agent/               ← feature/my-first-agent 分支
│   └── another-agent/                ← feature/another-agent 分支
├── agents/
├── docs/
└── README.md
```

### 工作原理

- 主目录固定在 master 分支，用于框架开发
- 每个 agent 分支在 `worktrees/` 下有独立的工作目录
- 所有目录共享同一个 Git 仓库（`.git/`）
- 不需要切换分支，可以同时编辑多个分支

### 创建新 Agent 的 Worktree

```bash
# 在主目录执行
git worktree add worktrees/<agent-name> feature/<agent-name>

# 示例
git worktree add worktrees/translator feature/translator
```

### 查看所有 Worktree

```bash
git worktree list
```

### 删除 Worktree

```bash
# Agent 开发完成并合并后，可以删除 worktree
git worktree remove worktrees/<agent-name>
```

### 自动同步 Master 更新

当在 master 分支提交框架更新后，需要同步到所有 agent 分支：

```bash
# Windows (PowerShell)
.\scripts\sync-master-to-worktrees.ps1

# Linux/Mac (Bash)
bash scripts/sync-master-to-worktrees.sh
```

脚本会自动：
1. 检查所有 worktree
2. 将 master 的更新合并到每个分支
3. 报告成功和失败的情况
4. 如果有冲突，提示手动解决

## 分支命名规范

### 推荐格式

```
feature/agent-<agent-name>
```

### 命名示例

- `feature/agent-git-commit` - Git 提交信息生成 Agent
- `feature/agent-code-review` - 代码审查 Agent
- `feature/agent-translator` - 翻译 Agent
- `feature/agent-doc-generator` - 文档生成 Agent

### 命名规则

1. 使用小写字母
2. 单词之间用短横线（-）连接
3. Agent 名称要简洁明确
4. 避免使用特殊字符

## 开发工作流程

### 方式 A：使用 Worktree（推荐）

#### 1. 创建新 Agent 分支和 Worktree

```bash
# 在主目录（master 分支）创建新分支
git checkout -b feature/translator

# 为新分支创建 worktree
git worktree add worktrees/translator feature/translator

# 切回 master
git checkout master
```

#### 2. 在 Worktree 中开发 Agent

```bash
# 进入 agent 的工作目录
cd worktrees/translator

# 创建 Agent 文件
mkdir -p "agents/translator"
# 编写代码...

# 提交更改
git add .
git commit -m "feat(agent): 添加翻译 Agent 基础功能"
git push -u origin feature/translator
```

#### 3. 在主目录开发框架

```bash
# 在主目录（master 分支）
cd ../../  # 回到主目录

# 修改框架文档
vim README.md

# 提交框架更新
git add README.md
git commit -m "docs: 更新框架文档"
git push
```

#### 4. 同步 Master 更新到 Agent 分支

```bash
# 在主目录执行同步脚本
.\scripts\sync-master-to-worktrees.ps1  # Windows
# 或
bash scripts/sync-master-to-worktrees.sh  # Linux/Mac
```

#### 5. 合并 Agent 到 Master

```bash
# 在主目录（master 分支）
git merge feature/translator
git push

# 删除 worktree（可选）
git worktree remove worktrees/translator
```

### 方式 B：传统分支切换（不推荐）

#### 1. 创建新 Agent 分支

```bash
# 确保主分支是最新的
git checkout master
git pull origin master

# 创建并切换到新分支
git checkout -b feature/translator
```

#### 2. 开发 Agent

在分支上进行开发：

```bash
# 创建 Agent 目录和文件
mkdir -p "agents/translator"
# 编写代码...

# 提交更改（遵循提交规范）
git add .
git commit -m "feat(agent): 添加翻译 Agent 基础功能"
```

#### 3. 推送到远程仓库

```bash
# 首次推送需要设置上游分支
git push -u origin feature/translator

# 后续推送
git push
```

#### 4. 合并到主分支

开发完成并测试通过后：

```bash
# 切换到主分支
git checkout master

# 拉取最新代码
git pull origin master

# 合并 Agent 分支
git merge feature/translator

# 推送到远程
git push origin master
```

#### 5. 分支管理

```bash
# 保留分支用于后续维护
git push origin feature/translator

# 或删除已合并的本地分支
git branch -d feature/translator

# 删除远程分支（可选）
git push origin --delete feature/translator
```

## 提交规范

详细的提交规范请参考：

- [贡献指南 - Git 提交规范](./contributing.md)
- 项目使用 Angular 提交规范

### 快速参考

```
<type>(<scope>): <subject>
```

常用类型：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档变更
- `refactor`: 重构
- `chore`: 构建或辅助工具变动

## 最佳实践

### 分支管理

1. 每个 Agent 使用独立分支开发
2. 定期从 main 分支同步更新
3. 合并前确保代码已测试
4. 保持分支命名一致性

### 提交管理

1. 提交信息清晰明确
2. 每次提交只做一件事
3. 提交前检查代码质量
4. 遵循项目提交规范

### 合并策略

1. 合并前先更新主分支
2. 解决所有冲突
3. 确保测试通过
4. 更新相关文档

## 常见场景

### 场景 1：开发新 Agent（使用 Worktree）

```bash
# 1. 创建分支和 worktree
git checkout -b feature/new-agent
git worktree add worktrees/new-agent feature/new-agent
git checkout master

# 2. 在 worktree 中开发
cd worktrees/new-agent
# 开发...
git add .
git commit -m "feat(agent): 添加新功能"
git push -u origin feature/new-agent

# 3. 回到主目录
cd ../..
```

### 场景 2：框架更新后同步到所有 Agent

```bash
# 1. 在主目录提交框架更新
git add README.md
git commit -m "docs: 更新框架文档"
git push

# 2. 自动同步到所有 worktree
.\scripts\sync-master-to-worktrees.ps1
```

### 场景 3：修复 Agent Bug

```bash
# 直接在对应的 worktree 中修复
cd worktrees/my-first-agent
# 修复...
git add .
git commit -m "fix(agent): 修复某个问题"
git push
```

### 场景 4：在 VS Code 中同时编辑多个分支

```bash
# 方式 1：打开多个窗口
code .                           # 主目录（master）
code worktrees/my-first-agent    # agent 分支

# 方式 2：添加到工作区
# File → Add Folder to Workspace → 选择 worktrees/my-first-agent
```

### 场景 5：合并 Agent 到 Master

```bash
# 在主目录
git merge feature/my-first-agent
git push

# 可选：删除 worktree
git worktree remove worktrees/my-first-agent
```

## 相关文档

- [贡献指南](./contributing.md) - 代码规范和提交规范
- [快速开始](../guides/quick-start.md) - 项目快速上手指南
