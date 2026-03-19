# Agent 参考项目

本目录存放 My First Agent 开发过程中参考的其他 Agent 项目和代码示例。

## 参考项目列表

### 1. learn-claude-code

**项目地址**：https://github.com/shareAI-lab/learn-claude-code

**简介**：Bash is all you need - A nano claude code–like 「agent harness」, built from 0 to 1

**参考价值**：
- 展示了如何从零构建一个类似 Claude Code 的 Agent
- 使用 Bash 脚本实现，简洁易懂
- 适合学习 Agent 的基本架构和工作流程

**克隆命令**：
```bash
git clone https://github.com/shareAI-lab/learn-claude-code.git
```

---

### 2. ai-agents-from-scratch

**项目地址**：https://github.com/the-ai-engineer/ai-agents-from-scratch

**简介**：A complete course on building AI agents from scratch in vanilla Python

**参考价值**：
- 完整的 AI Agent 开发课程
- 使用纯 Python 实现，无复杂依赖
- 从零开始构建，适合深入学习

**克隆命令**：
```bash
git clone https://github.com/the-ai-engineer/ai-agents-from-scratch.git
```

---

## 使用说明

### 如何添加新的参考项目

1. 在本目录下克隆项目：
   ```bash
   cd "agents/my first agent/references"
   git clone <项目地址>
   ```

2. 在本 README 中添加项目信息：
   - 项目地址
   - 简介
   - 参考价值
   - 克隆命令

### 目录结构

```
references/
├── README.md                           # 本文件
├── learn-claude-code/                  # 参考项目 1
└── ai-agents-from-scratch/             # 参考项目 2
```

## 注意事项

1. **版权声明**：这些项目仅供学习参考，请遵守各项目的开源协议
2. **更新维护**：定期拉取最新代码以获取更新
3. **学习记录**：学习过程中的笔记和心得可以记录在 `docs/issues/notes/user/` 目录下

## 相关文档

- [My First Agent 文档](../../../docs/agents/my-first-agent.md)
- [开发规范](../../../docs/development-guide.md)
- [学习笔记目录](../../../docs/issues/notes/user/)
