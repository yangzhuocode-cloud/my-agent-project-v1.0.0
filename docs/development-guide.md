# 开发规范（已废弃）

> ⚠️ **注意**: 本文档已被拆分为多个更专注的文档。

本文档的内容已经重新组织到以下位置：

## 给人类开发者

- **设计理念** → [docs/understanding/design-philosophy.md](./understanding/design-philosophy.md)
- **贡献指南** → [docs/development/contributing.md](./development/contributing.md)
- **Git 工作流程** → [docs/development/git-workflow.md](./development/git-workflow.md)

## 给 AI 助手

- **代码规范** → [.kiro/steering/coding-standards.md](../.kiro/steering/coding-standards.md)
- **工作流程** → [.kiro/steering/workflow.md](../.kiro/steering/workflow.md)
- **开发边界** → [.kiro/steering/boundaries.md](../.kiro/steering/boundaries.md)

## 为什么拆分？

原来的 `development-guide.md` 混合了给人类看的理解性内容和给 AI 看的执行性指令，导致：
- 内容冗余，难以维护
- 目标读者不清晰
- 文档职责混乱

现在按照"人机分离"的原则重新组织：
- 人类文档在 `docs/` 下，解释"为什么"和"怎么理解"
- AI 指令在 `.kiro/steering/` 下，定义"怎么做"和"边界规则"

请使用新的文档结构。本文件将在下一个版本中删除。
