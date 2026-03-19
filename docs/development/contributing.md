# 贡献指南

> 📖 **目标读者**: 人类开发者  
> 🎯 **文档类型**: 开发指南

本文档说明如何为 AI Agents 项目做出贡献。

## 开发环境准备

### 必需工具

- Python 3.7+
- Git
- Kiro IDE（推荐）或其他代码编辑器

### 安装依赖

```bash
pip install requests
```

## 开发流程

### 1. Fork 和 Clone

```bash
# Fork 项目到你的 GitHub 账号
# 然后 clone 到本地
git clone https://github.com/your-username/AI-Agents.git
cd AI-Agents
```

### 2. 创建分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name
```

分支命名规范：
- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `refactor/` - 代码重构

### 3. 进行开发

- 遵循 [代码规范](../understanding/design-philosophy.md)
- 添加中文注释和文档字符串
- 保持代码简洁清晰

### 4. 测试你的更改

```bash
# 运行你修改的 Agent
cd "agents/your-agent"
python main.py
```

### 5. 提交更改

```bash
# 添加文件
git add .

# 提交（使用 Angular 规范）
git commit -m "feat(agent): 添加新功能"
```

提交信息格式请参考：[Git 工作流程](./git-workflow.md)

### 6. 推送和创建 Pull Request

```bash
# 推送到你的 fork
git push origin feature/your-feature-name

# 在 GitHub 上创建 Pull Request
```

## 贡献类型

### 新增 Agent

1. 在 `agents/` 下创建新目录
2. 实现 Agent 功能
3. 创建使用文档 `docs/agents/{agent-name}.md`
4. 更新 `README.md`

详细流程请参考：[项目结构说明](../understanding/project-structure.md)

### 改进现有 Agent

1. 修改 Agent 代码
2. 更新对应的使用文档
3. 在 PR 中说明改进内容

### 文档改进

1. 修改或新增文档
2. 确保文档结构清晰
3. 使用正确的 Markdown 格式

### Bug 修复

1. 在 Issues 中描述 Bug
2. 创建修复分支
3. 提交修复并关联 Issue

## 代码审查

提交 PR 后，维护者会进行代码审查：

- 检查代码质量
- 验证功能正确性
- 确认文档完整性
- 测试运行效果

请及时响应审查意见并进行修改。

## 行为准则

- 尊重他人的贡献
- 保持友好和专业的沟通
- 接受建设性的反馈
- 遵守项目的开发规范

## 获取帮助

如果你在贡献过程中遇到问题：

1. 查看 [常见问题](../reference/faq.md)
2. 在 Issues 中提问
3. 联系项目维护者

## 相关文档

- [Git 工作流程](./git-workflow.md) - 分支管理和提交规范
- [设计理念](../understanding/design-philosophy.md) - 项目设计原则
- [项目结构说明](../understanding/project-structure.md) - 目录结构
