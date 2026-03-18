# Git 工作流程

本文档定义了项目的 Git 分支管理和工作流程规范。

## 分支策略

### 主分支（main）

主分支只包含项目框架和通用内容：

- 项目文档结构
- 通用配置文件
- README.md、CHANGELOG.md
- 共享的提示词和工具

### Agent 开发分支

每个新 Agent 在独立分支开发，开发完成后合并到主分支。

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

### 1. 创建新 Agent 分支

```bash
# 确保主分支是最新的
git checkout main
git pull origin main

# 创建并切换到新分支
git checkout -b feature/agent-translator
```

### 2. 开发 Agent

在分支上进行开发：

```bash
# 创建 Agent 目录和文件
mkdir -p "agents/translator"
# 编写代码...

# 提交更改（遵循提交规范）
git add .
git commit -m "feat(agent): 添加翻译 Agent 基础功能"
```

### 3. 推送到远程仓库

```bash
# 首次推送需要设置上游分支
git push -u origin feature/agent-translator

# 后续推送
git push
```

### 4. 合并到主分支

开发完成并测试通过后：

```bash
# 切换到主分支
git checkout main

# 拉取最新代码
git pull origin main

# 合并 Agent 分支
git merge feature/agent-translator

# 推送到远程
git push origin main
```

### 5. 分支管理

```bash
# 保留分支用于后续维护
git push origin feature/agent-translator

# 或删除已合并的本地分支
git branch -d feature/agent-translator

# 删除远程分支（可选）
git push origin --delete feature/agent-translator
```

## 提交规范

详细的提交规范请参考：

- [开发规范 - Git 提交规范](./development-guide.md#git-提交规范)
- [Angular 提交规范详解](../agents/my%20first%20agent/docs/git_commit_angular_001.md)

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

### 场景 1：开发新 Agent

```bash
git checkout main
git pull
git checkout -b feature/agent-new-feature
# 开发...
git add .
git commit -m "feat(agent): 添加新功能"
git push -u origin feature/agent-new-feature
```

### 场景 2：修复 Bug

```bash
git checkout main
git pull
git checkout -b fix/agent-bug-description
# 修复...
git add .
git commit -m "fix(agent): 修复某个问题"
git push -u origin fix/agent-bug-description
```

### 场景 3：更新文档

```bash
git checkout main
# 修改文档...
git add docs/
git commit -m "docs: 更新 Agent 使用文档"
git push
```

## 相关文档

- [开发规范](./development-guide.md) - 代码规范和提交规范
- [快速开始](./quick-start.md) - 项目快速上手指南
