# ADR-0002: Prompts 分离架构

**状态**: 已采纳  
**日期**: 2026-03-19  
**决策者**: 项目团队

## 背景和问题

项目中存在多种类型的 prompt 文件：

1. **共享 prompts** - 如 Git Commit 规范，多个 agent 都需要使用
2. **项目私有 prompts** - 如 prompt 生成器，只在项目内部使用
3. **Agent 私有 prompts** - 如 agent 的主 prompt，只属于特定 agent

面临的问题：

1. **单一数据源 vs 独立分发的矛盾**
   - 共享 prompt 需要只维护一份
   - 导出 agent 时又需要包含这些 prompt
   - 如果保存多份，更新时容易不一致

2. **目录结构不清晰**
   - 不知道哪些 prompt 是共享的
   - 不知道哪些 prompt 会被导出

3. **维护困难**
   - 修改共享 prompt 需要同步到多个 agent
   - 容易遗漏或出错

## 考虑的方案

### 方案 1: 文件夹区分

**描述**: 使用不同文件夹区分共享和私有 prompt

```
prompts/
├── shared/           ← 共享 prompts
│   └── git_commit_angular_001.md
└── private/          ← 项目私有 prompts
    └── prompt_generator_001.md
```

**优点**:
- 目录结构清晰，一眼看出哪些是共享的
- 简单直观，不需要解析文件内容
- 导出脚本逻辑简单

**缺点**:
- 不够灵活，无法表达"部分共享"（只给特定几个 agent）
- 移动文件需要改变目录结构
- 无法表达更复杂的关系（版本、依赖等）

### 方案 2: 元数据驱动（推荐）

**描述**: 所有 prompt 在同一目录，通过文件头部的元数据定义共享范围

```markdown
---
prompt_id: git_commit_angular_001
scope: shared              ← 共享范围
agents: ["*"]              ← 所有 agent 可用
version: 1.0.0
---

## 角色定位
...
```

**支持的共享范围**:
- `shared`: 全局共享，所有 agent 可用 (`agents: ["*"]`)
- `private`: 项目私有，不导出到任何 agent (`agents: []`)
- `selective`: 选择性共享，只给特定 agent (`agents: ["agent1", "agent2"]`)

**优点**:
- 极其灵活，支持复杂场景
- 所有 prompts 在同一目录，易于管理
- 元数据可扩展（标签、分类、作者、依赖等）
- 支持未来的高级功能（版本锁定、条件导出等）

**缺点**:
- 导出脚本需要解析 YAML front matter
- 需要维护元数据规范
- 初期稍微复杂一点

## 决策

选择方案 2：元数据驱动

**理由**:

1. **可扩展性强**
   - 未来可能出现的需求都能支持
   - 不需要重构目录结构

2. **符合行业最佳实践**
   - npm 的 package.json
   - Python 的 pyproject.toml
   - Markdown 的 front matter

3. **单一数据源**
   - 元数据和内容在同一文件
   - 不会出现不同步的问题

4. **查询友好**
   - 可以写工具扫描所有 prompts 的元数据
   - 生成报告或索引

## 影响

**正面影响**:

1. **灵活性提升**
   - 支持全局共享、项目私有、选择性共享
   - 支持版本管理和依赖关系

2. **维护简单**
   - 所有 prompts 在同一目录
   - 元数据和内容在同一文件

3. **可扩展性**
   - 可以添加更多元数据字段
   - 支持未来的高级功能

**负面影响**:

1. **学习成本**
   - 需要理解元数据规范
   - 需要遵循 YAML front matter 格式

2. **工具依赖**
   - 导出脚本需要解析 YAML
   - 需要验证元数据格式

**需要的工作**:

1. 定义元数据规范
2. 更新现有 prompt 文件添加元数据
3. 更新导出脚本支持元数据解析
4. 创建元数据验证工具
5. 编写使用文档

## 实现细节

### 元数据规范

```yaml
---
# 必填字段
prompt_id: git_commit_angular_001    # 唯一标识符
scope: shared | private | selective  # 共享范围
version: 1.0.0                       # 版本号

# 共享配置
agents: ["*"] | [] | ["agent1", "agent2"]  # 适用的 agent

# 可选字段
description: 用于生成符合 Angular 规范的 Git Commit 消息
tags: ["git", "commit", "angular"]
author: your-name
created: 2026-03-18
updated: 2026-03-19
depends_on: []                       # 依赖的其他 prompt
---
```

### 目录结构

```
prompts/
├── git_commit_angular_001.md    ← scope: shared, agents: ["*"]
├── prompt_generator_001.md      ← scope: private, agents: []
└── auth_handler_001.md          ← scope: selective, agents: ["auth-agent"]

agents/my first agent/
└── prompts/
    └── main_prompt.md           ← agent 私有，包含 #[[prompt:xxx]] 引用
```

### 导出脚本逻辑

```python
import yaml
import re

def parse_prompt_metadata(file_path):
    """解析 prompt 文件的元数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 YAML front matter
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None

def should_export_to_agent(prompt_metadata, agent_name):
    """判断 prompt 是否应该导出到指定 agent"""
    if prompt_metadata['scope'] == 'private':
        return False
    if prompt_metadata['scope'] == 'shared':
        return True
    if prompt_metadata['scope'] == 'selective':
        return agent_name in prompt_metadata['agents']
    return False
```

## 相关决策

- [ADR-0001: 虚拟路径引用机制](./0001-虚拟路径引用机制.md) - 定义了如何引用 prompt
- [ADR-0003: Agent 导出机制](./0003-Agent导出机制.md) - 定义了完整的导出流程

## 参考资料

- [Prompts 使用指南](../../guides/prompts-guide.md)
- [Prompt 元数据规范](../../reference/prompt-metadata-spec.md)
