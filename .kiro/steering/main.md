---
inclusion: auto
---

# Kiro AI 开发指令总入口

> 🤖 **目标读者**: AI 助手  
> 🎯 **文档类型**: 执行指令

本文件是 AI 助手的开发指令总入口，通过引用其他指令文件组织完整的开发规范。

## 语言要求

- 所有对话和交流必须使用中文
- 代码注释使用中文
- 文档和说明使用中文

## 核心开发指令

以下是你必须遵守的核心指令，详细内容请参考对应文件：

### 分支管理规则（⚠️ 必读）
#[[file:.kiro/instructions/branch-management.md]]

### 开发边界
#[[file:.kiro/instructions/boundaries.md]]

### 工作流程
#[[file:.kiro/instructions/workflow.md]]

### 代码规范
#[[file:.kiro/instructions/coding-standards.md]]

### 日志规范（⚠️ 必读）
#[[file:.kiro/instructions/logging.md]]

## 提交规范

项目使用 Angular 提交规范：

#[[prompt:git_commit_angular_001]]

## 快速参考

### 问题与知识库索引

在开发过程中，如果遇到相关问题或需要查找已有知识，请参考：

#[[file:../docs/issues/INDEX-AI.md]]

**使用场景**：
- 遇到 token、上下文长度等大模型相关问题
- 需要查找 Git 提交、文档管理等已解决的问题
- 查找 Agent 开发的最佳实践和经验总结

### 常用提交类型

### 文档同步原则

- `.kiro/steering/` - 给 AI 读的执行指令
- `docs/` - 给人类读的理解性文档
- `README.md` - 项目门户和快速导航

详细的文档同步规则请参考 `workflow.md`。

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档变更
- `refactor`: 重构
- `chore`: 构建工具或辅助工具变动
