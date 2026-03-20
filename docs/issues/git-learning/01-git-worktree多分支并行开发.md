# Git Worktree 多分支并行开发

## 学习日期
2026-03-20

## 问题背景

在开发 AI Agent 项目时，遇到以下痛点：
- 框架代码在 master 分支
- 每个 agent 在独立的 feature 分支开发
- 需要频繁在 master 和 feature 分支之间切换
- 每次切换都要 commit 或 stash，非常麻烦
- master 的更新需要手动合并到所有 feature 分支

## Git Worktree 是什么？

Git Worktree 允许你**同时检出多个分支到不同的目录**，每个目录固定在一个分支上，不需要切换。

### 传统方式 vs Worktree

**传统方式**（痛点）：
```bash
# 在 feature 分支工作
vim agents/my-agent/main.py
git stash                    # 必须先保存
git checkout master          # 切换分支
vim README.md
git commit -m "docs: 更新"
git checkout feature/my-agent
git merge master             # 合并更新
git stash pop                # 恢复工作
```

**Worktree 方式**（优雅）：
```bash
# 终端 1：在 master 目录工作
cd my-project
vim README.md
git commit -m "docs: 更新"

# 终端 2：在 feature 目录工作（同时进行！）
cd worktrees/my-agent
vim agents/my-agent/main.py
git commit -m "feat: 新功能"

# 合并更新
git merge master  # 只需这一步
```

## 实际操作

### 1. 目录结构设计

```
my-agent-project-v1.0.0/              ← master 分支（主目录）
├── .git/                             ← 真正的 Git 仓库
├── worktrees/                        ← 存放所有 worktree
│   ├── my-first-agent/               ← feature/my-first-agent 分支
│   └── another-agent/                ← feature/another-agent 分支
├── agents/
├── docs/
└── README.md
```

### 2. 创建 Worktree

```bash
# 语法
git worktree add <路径> <分支名>

# 示例：为 feature/my-first-agent 创建 worktree
git worktree add worktrees/my-first-agent feature/my-first-agent

# 查看所有 worktree
git worktree list
# 输出：
# D:/projects/my-agent-project-v1.0.0                           [master]
# D:/projects/my-agent-project-v1.0.0/worktrees/my-first-agent  [feature/my-first-agent]
```

### 3. 日常工作流程

**框架开发（主目录）**：
```bash
cd my-agent-project-v1.0.0
vim README.md
git add README.md
git commit -m "docs: 更新框架文档"
git push
```

**Agent 开发（worktree）**：
```bash
cd worktrees/my-first-agent
vim agents/my\ first\ agent/main.py
git add .
git commit -m "feat(agent): 新功能"
git push
```

**同步 master 更新**：
```bash
# 在主目录执行同步脚本
.\scripts\sync-master-to-worktrees.ps1  # Windows
bash scripts/sync-master-to-worktrees.sh  # Linux/Mac
```

### 4. 自动同步脚本

创建了自动同步脚本 `scripts/sync-master-to-worktrees.ps1`，功能：
- 自动检测所有 worktree
- 将 master 的更新合并到每个 feature 分支
- 检查未提交的更改
- 处理合并冲突
- 输出详细的成功/失败报告

## 关键知识点

### 1. Worktree 的物理结构

- **主目录**：包含真正的 `.git/` 目录（完整的 Git 仓库）
- **Worktree 目录**：包含一个 `.git` 文件（指向主仓库的链接）
- 所有 worktree 共享同一个 Git 历史和配置

### 2. 文件夹命名

- 主目录名字可以随意改
- Worktree 目录名字由创建时指定，完全自定义
- 可以放在任何位置（不一定在主目录下）

### 3. 分支限制

- 一个分支只能被一个 worktree 使用
- 如果主目录在 master 分支，就不能再创建 master 的 worktree
- 解决方案：主目录用 master，其他分支用 worktree

### 4. 删除 Worktree

```bash
# 删除 worktree（不删除分支）
git worktree remove worktrees/my-agent

# 清理无效的 worktree 记录
git worktree prune
```

## 在 VS Code 中使用

### 方式 1：多窗口
```bash
code .                           # 主目录（master）
code worktrees/my-first-agent    # agent 分支
```

### 方式 2：工作区
- File → Add Folder to Workspace
- 选择 `worktrees/my-first-agent`
- 可以在同一个窗口看到多个分支

## 优势总结

1. ✅ **不需要切换分支**：每个目录固定在一个分支
2. ✅ **可以同时编辑**：在不同终端或 VS Code 窗口并行工作
3. ✅ **不会互相干扰**：修改互不影响
4. ✅ **共享 Git 历史**：所有 worktree 共享同一个仓库
5. ✅ **提高效率**：不需要 stash，不需要等待切换

## 注意事项

1. **磁盘空间**：每个 worktree 会占用额外空间（文件是真实复制的）
2. **分支冲突**：一个分支只能被一个 worktree 使用
3. **提交位置**：要清楚当前在哪个目录（哪个分支）提交
4. **.gitignore**：需要忽略 `worktrees/` 目录，避免提交

## Worktree 与远程仓库

### 重要理解

**Worktree 只是本地工作方式**：
- ✅ 推送到远程的是**分支**（master、feature/xxx）
- ❌ `worktrees/` 目录**不会推送**（已在 .gitignore 中）
- ❌ 本地的文件夹结构**不会同步**到远程

### 远程仓库看到的

```
GitHub/GitLab 远程仓库
├── master 分支
├── feature/my-first-agent 分支
└── feature/another-agent 分支

❌ 没有 worktrees/ 目录
❌ 没有本地的多文件夹结构
```

### 其他开发者如何使用

**方式 1：使用 Worktree 模式（推荐）**

```bash
# 1. 克隆项目
git clone https://github.com/user/my-agent-project.git
cd my-agent-project

# 2. 运行自动设置脚本
.\scripts\setup-worktrees.ps1  # Windows
bash scripts/setup-worktrees.sh  # Linux/Mac

# 3. 脚本会自动：
#    - 检测所有远程 feature 分支
#    - 为每个分支创建 worktree
#    - 输出设置结果

# 4. 现在本地结构和原作者一样了
git worktree list
```

**方式 2：传统方式（不使用 Worktree）**

```bash
# 克隆后直接切换分支工作
git clone https://github.com/user/my-agent-project.git
cd my-agent-project

# 切换到 feature 分支
git checkout feature/my-first-agent
# 开发...

# 切回 master
git checkout master
```

### 自动设置脚本

项目提供了 `scripts/setup-worktrees.ps1` 和 `setup-worktrees.sh`：

**功能**：
- 自动检测所有远程 feature 分支
- 为每个分支创建对应的 worktree
- 跳过已存在的 worktree
- 输出详细的设置结果和使用提示

**示例输出**：
```
Setting up Git Worktree development environment...

Fetching remote branch information...
Found the following feature branches:
  - feature/my-first-agent
  - feature/another-agent

Creating worktrees...

CREATE: worktrees/my-first-agent (feature/my-first-agent)
CREATE: worktrees/another-agent (feature/another-agent)

========================================
Worktree setup completed

Current worktree structure:
D:/projects/my-agent-project  [master]
D:/projects/my-agent-project/worktrees/my-first-agent  [feature/my-first-agent]
D:/projects/my-agent-project/worktrees/another-agent  [feature/another-agent]
========================================
```

## 相关文档

- [Git 工作流程](../../development/git-workflow.md) - 完整的 Git 工作流程说明
- [同步脚本源码](../../../scripts/sync-master-to-worktrees.ps1) - 自动同步脚本

## 参考资料

- [Git Worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [Git Worktree 使用场景](https://stackoverflow.com/questions/31935776/what-would-i-use-git-worktree-for)
