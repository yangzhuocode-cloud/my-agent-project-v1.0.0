---
slug: git-worktree-commit-reset
keywords: [git, worktree, commit, reset, 分支, 提交]
first_occurred: 2026-03-24
last_updated: 2026-03-24
occurrences: 1
---

# Git Worktree 子分支提交后分支引用自动重置问题

**问题类型**：Git 引用管理异常  
**严重程度**：高（导致提交无法正常保存）

---

## 问题描述

在 Git Worktree 环境中，对子分支（如 `feature/my-first-agent`）执行 `git commit` 操作后，虽然提交对象（commit object）成功创建，但分支引用（branch ref）会被自动重置回原来的位置，导致提交无法在分支中保存。

## 问题现象

### 1. 提交命令执行成功

执行 `git commit -m "..."` 后，命令输出显示提交成功：

```
[feature/my-first-agent 6a395f3] feat: 添加环境变量配置模板和依赖文件
 3 files changed, 33 insertions(+), 7 deletions(-)
```

### 2. 分支引用被重置

但立即检查状态时，分支仍然指向原来的提交：

```
$ git log --oneline -3
31f0fa9 (HEAD -> feature/my-first-agent, origin/feature/my-first-agent) feat: 实现 API 连接测试功能
...

$ git status
On branch feature/my-first-agent
Your branch is up to date with 'origin/feature/my-first-agent'.
(nothing to commit)
```

### 3. 提交对象实际存在

通过 reflog 可以看到提交确实创建了：

```
$ git reflog -5
6a395f3 HEAD@{0}: commit: feat: 添加环境变量配置模板和依赖文件
...
```

## 问题原因分析

### 1. Git 分支引用存储机制

Git 分支引用可以存储在两个位置：

1. **单独的 ref 文件**：`.git/refs/heads/<branch-name>`
2. **打包的 ref 文件**：`.git/packed-refs`

当分支引用只存在于 `packed-refs` 中时，某些情况下可能导致引用更新失败。

### 2. 可能的根本原因

经过多种方式排查，未能找到确定原因。可能的原因包括：

#### 2.1 Trae IDE 内部机制

- Trae 在执行 git 命令后可能自动调用了某些操作
- 可能是 Trae 的 git 集成模块的某种行为

#### 2.2 Git for Windows 特殊行为

- 某些 Git 版本在 worktree 环境下的特殊行为
- 打包引用（packed-refs）与单独引用的优先级问题

#### 2.3 Shell 环境差异

- PowerShell 执行 git 命令时的特殊行为
- trae-sandbox 环境的某种保护机制

### 3. Reflog 中的异常

从 reflog 中观察到异常模式：

```
16: 31f0fa9... -> 8459f2d...  (提交创建)
17: 31f0fa9... -> 8459f2d...  (无操作描述，但分支被重置)
```

**每次提交后，在同一秒内分支引用被重置，但没有记录具体是什么操作！**

## 排查方式记录

### 1. Git Hooks 检查

- **检查位置**：`.git/hooks/` 目录
- **结果**：只有 `.sample` 模板文件，无实际可执行脚本
- **结论**：排除 hooks 导致的问题

### 2. VS Code/Trae 配置检查

- **检查位置**：`.vscode/settings.json`
- **结果**：项目中不存在此文件
- **结论**：未发现相关 Git 配置

### 3. Git 全局配置检查

- **检查命令**：`git config --list --show-origin`
- **结果**：未发现 `core.hooksPath` 或其他可疑配置
- **结论**：排除全局 hooks 设置

### 4. Git 引用存储分析

- **检查位置**：`.git/packed-refs`、`.git/refs/heads/`
- **发现**：`feature/my-first-agent` 分支只存在于 `packed-refs` 中
- **结论**：packed-refs 的优先级可能与问题相关

### 5. Reflog 深度分析

- **检查位置**：`.git/worktrees/my-first-agent/logs/HEAD`
- **发现**：每次提交后都有无操作描述的重置记录
- **结论**：确认存在自动重置行为，但无法确定触发者

## 解决方案

### 临时解决方案：创建单独的 ref 文件

通过创建单独的 ref 文件来覆盖 `packed-refs` 中的引用：

```bash
# 创建单独的 ref 文件
echo "6a395f308ab66b3ed870ae99d6e404c2ebcad70c" > .git/refs/heads/feature/my-first-agent
```

### 验证结果

```
$ git log --oneline -3
6a395f3 (HEAD -> feature/my-first-agent) feat: 添加环境变量配置模板和依赖文件
31f0fa9 (origin/feature/my-first-agent) feat: 实现 API 连接测试功能
...

$ git status
On branch feature/my-first-agent
Your branch is ahead of 'origin/feature/my-first-agent' by 1 commit.
```

## 后续建议

### 1. 进一步排查

- 在不使用 Trae 的情况下（直接在命令行）执行 git commit，验证是否还会出现同样问题
- 检查 Trae 的相关配置或文档
- 尝试更新或降级 Git 版本

### 2. 长期方案

- 考虑将所有分支引用从 `packed-refs` 迁移到单独的 ref 文件
- 或在项目中添加文档说明此问题的临时解决方案

### 3. 预防措施

- 在进行重要提交后，立即检查 `git log --oneline -3` 确认提交是否保存
- 定期检查 reflog 发现异常重置

---

## 重复发生记录

### 第 1 次：2026-03-24 23:00

- **场景**：在 worktree 目录中对 feature/my-first-agent 分支进行提交
- **涉及文件**：`.env.example`、`requirements.txt`、`agents/my first agent/main.py`
- **处理**：创建单独的 ref 文件解决
- **状态**：暂时解决，根本原因未确定

---

## 参考资源

- [Git 内部原理 - Pack 引用](https://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-Pack-%E5%BC%95%E7%94%A8)
- [Git Worktree 文档](https://git-scm.com/docs/git-worktree)
- [Git 引用规范](https://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-Git-%E5%BC%95%E7%94%A8%E8%A7%84%E8%8C%83)
