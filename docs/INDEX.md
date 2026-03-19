# 文档索引

> 📖 **目标读者**: 人类开发者  
> 🎯 **文档类型**: 参考资料

本文档提供项目所有文档的快速索引和导航。

## 📚 文档结构

项目文档按照功能和目标读者分为不同类别，完整的目录结构和说明请参考：[项目结构说明](./understanding/project-structure.md)

主要文档分类：
- **agents/** - Agent 使用文档
- **understanding/** - 理解项目（设计理念、架构、结构）
- **guides/** - 使用指南（快速开始、配置、Prompts、导出）
- **development/** - 开发指南（贡献、Git 工作流程）
- **issues/** - 开发过程记录（问题、笔记、想法）

---

## � 理解项目

深入理解项目的设计理念和技术架构。

| 文档 | 说明 | 关键内容 |
|------|------|----------|
| [设计理念](./understanding/design-philosophy.md) | 为什么这样设计 | 单一数据源、开发与导出分离、人机分离文档 |
| [架构设计](./understanding/architecture.md) | 技术架构和组件 | 系统架构、核心组件、数据流 |
| [项目结构](./understanding/project-structure.md) | 目录结构详解 | 完整目录树、文件职责、扩展规范 |

---

## � 使用指南

如何使用项目的各项功能。

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [快速开始](./guides/quick-start.md) | 快速上手 | 第一次使用项目 |
| [配置说明](./guides/configuration.md) | 参数配置详解 | 调整 Agent 参数 |
| [Prompts 管理](./guides/prompts-guide.md) | Prompts 使用方式 | 创建和引用 Prompts |
| [Agent 导出](./guides/agent-export-guide.md) | 导出独立 Agent 包 | 分享和部署 Agent |

---

## � 开发指南

如何为项目做出贡献。

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [贡献指南](./development/contributing.md) | 如何贡献代码 | 参与项目开发 |
| [Git 工作流程](./development/git-workflow.md) | 分支管理和提交规范 | 提交代码前必读 |

---

## 📝 开发过程记录

记录开发过程中的问题、笔记和想法。

| 文档 | 说明 | 用途 |
|------|------|------|
| [开发记录指南](./issues/README.md) | 问题记录规范 | 记录问题和笔记 |

## 📐 规范文档

| 文档 | 说明 | 用途 |
|------|------|------|
| [Prompt 元数据规范](../prompts/METADATA-SPEC.md) | 元数据字段定义 | 创建 Prompt 时参考 |

---

## 🤖 AI 开发者文档

如果你是 AI 助手，以下是你的执行指令文档（位于 `.kiro/steering/`）：

| 文档 | 说明 |
|------|------|
| `main.md` | 总入口，引用其他指令 |
| `boundaries.md` | 开发边界和禁止事项 |
| `workflow.md` | 自动化工作流程 |
| `coding-standards.md` | 代码规范细节 |

---

## � 快速查找

### 我想了解...

| 需求 | 推荐文档 |
|------|----------|
| 项目是什么 | [README.md](../README.md) |
| 为什么这样设计 | [设计理念](./understanding/design-philosophy.md) |
| 如何快速开始 | [快速开始](./guides/quick-start.md) |
| 目录结构是什么 | [项目结构](./understanding/project-structure.md) |
| 如何管理 Prompts | [Prompts 管理](./guides/prompts-guide.md) |
| 如何导出 Agent | [Agent 导出](./guides/agent-export-guide.md) |
| 如何贡献代码 | [贡献指南](./development/contributing.md) |
| 如何提交代码 | [Git 工作流程](./development/git-workflow.md) |
| Prompt 元数据怎么写 | [Prompt 元数据规范](../prompts/METADATA-SPEC.md) |
| 如何记录问题 | [开发记录指南](./issues/README.md) |

### 我想做...

| 任务 | 推荐文档 |
|------|----------|
| 创建新 Agent | [项目结构](./understanding/project-structure.md) → [贡献指南](./development/contributing.md) |
| 创建新 Prompt | [Prompts 管理](./guides/prompts-guide.md) → [元数据规范](../prompts/METADATA-SPEC.md) |
| 导出 Agent | [Agent 导出](./guides/agent-export-guide.md) |
| 修改配置 | [配置说明](./guides/configuration.md) |
| 提交代码 | [Git 工作流程](./development/git-workflow.md) |
| 记录问题 | [开发记录指南](./issues/README.md) |

---

## 📊 文档关系图

```
README.md (项目门户)
    │
    ├─→ understanding/ (理解项目)
    │   ├─→ design-philosophy.md (为什么)
    │   ├─→ architecture.md (怎么做)
    │   └─→ project-structure.md (是什么)
    │
    ├─→ guides/ (使用指南)
    │   ├─→ quick-start.md
    │   ├─→ configuration.md
    │   ├─→ prompts-guide.md
    │   └─→ agent-export-guide.md
    │
    ├─→ development/ (开发指南)
    │   ├─→ contributing.md
    │   └─→ git-workflow.md
    │
    └─→ issues/ (开发过程记录)
        └─→ README.md
```

---

## 📌 文档维护

### 更新原则

1. 本索引文档应保持最新
2. 新增文档后必须更新本索引
3. 文档链接失效时及时修复
4. 定期检查文档的准确性

### 文档层级

- **理解文档** - 解释"为什么"和背景
- **指南文档** - 说明"怎么做"
- **参考文档** - 提供规范和快速查询

### 文档标签

每个文档都应包含：
- 📖 **目标读者** - 人类开发者 / AI 助手
- 🎯 **文档类型** - 理解 / 指南 / 参考

---

## 🔗 外部资源

- [项目 GitHub](https://github.com/your-repo/AI-Agents)
- [Kiro IDE 文档](https://kiro.ai/docs)
- [火山方舟文档](https://www.volcengine.com/docs/ark)

---

## 📝 反馈

如果你发现文档有问题或需要改进：

1. 在 GitHub 上提 Issue
2. 直接提交 PR 修改文档
3. 联系项目维护者

我们欢迎任何形式的文档改进建议！
