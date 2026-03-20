# 项目级参考资源

本目录存放项目级别的通用参考资源，如 SDK、库、框架等。这些资源与具体 Agent 无关，可能被多个 Agent 共同使用。

## 与 Agent 特定参考项目的区别

- **顶级 `references/`**（本目录）：存放通用的、多个 Agent 可能共用的参考资源
  - 示例：ollama-python SDK、通用工具库、框架代码
  - 特点：与具体 Agent 无关，项目级别的依赖和参考
  
- **`agents/{name}/references/`**：存放特定 Agent 的参考项目
  - 示例：learn-claude-code、ai-agents-from-scratch
  - 特点：与该 Agent 的实现直接相关，用于学习和参考

## 参考资源列表

### 1. ollama-python

**项目地址**：https://github.com/ollama/ollama-python

**简介**：Ollama Python library

**参考价值**：
- Ollama 的官方 Python SDK
- 提供了与 Ollama API 交互的完整接口
- 包含丰富的示例代码，涵盖聊天、生成、工具调用等功能
- 适合学习如何与 LLM API 进行交互

**克隆命令**：
```bash
git clone https://github.com/ollama/ollama-python.git
```

---

## 使用说明

### 如何添加新的参考资源

1. 评估资源的通用性：
   - 如果是多个 Agent 可能用到的 SDK/库 → 放在本目录
   - 如果是特定 Agent 的学习参考项目 → 放在 `agents/{name}/references/`

2. 在本目录下克隆项目：
   ```bash
   cd references
   git clone <项目地址>
   ```

3. 在本 README 中添加资源信息：
   - 项目地址
   - 简介
   - 参考价值
   - 克隆命令

### 目录结构

当前 `references/` 目录包含：
- `README.md` - 本文件（参考资源说明）
- `ollama-python/` - Ollama Python SDK

完整的项目结构请参考：[项目结构说明](../docs/understanding/project-structure.md)

## 注意事项

1. **版权声明**：这些项目仅供学习参考，请遵守各项目的开源协议
2. **更新维护**：定期拉取最新代码以获取更新
3. **学习记录**：学习过程中的笔记和心得可以记录在 `docs/issues/notes/user/` 目录下

## 相关文档

- [项目结构说明](../docs/understanding/project-structure.md)
- [设计理念](../docs/understanding/design-philosophy.md)
- [学习笔记目录](../docs/issues/notes/user/)
