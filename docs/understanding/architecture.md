# 架构设计

> 📖 **目标读者**: 人类开发者  
> 🎯 **文档类型**: 理解

本文档说明 AI Agents 项目的技术架构和组件关系。

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agents 项目                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Agent 1    │  │   Agent 2    │  │   Agent N    │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤ │
│  │ main.py      │  │ main.py      │  │ main.py      │ │
│  │ config.json  │  │ config.json  │  │ config.json  │ │
│  │ prompts/     │  │ prompts/     │  │ prompts/     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                 │          │
│         └─────────────────┼─────────────────┘          │
│                           │                            │
│                  ┌────────▼────────┐                   │
│                  │  项目级 Prompts  │                   │
│                  │   (prompts/)    │                   │
│                  └─────────────────┘                   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              导出脚本 (scripts/)                  │  │
│  │  - 解析引用                                       │  │
│  │  - 复制文件                                       │  │
│  │  - 生成独立 Agent                                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘

                           │ 导出
                           ▼
                           
              ┌─────────────────────┐
              │   独立 Agent 包      │
              ├─────────────────────┤
              │ main.py             │
              │ config.json         │
              │ prompts/            │
              │   ├── agent.md      │
              │   └── shared_*.md   │
              └─────────────────────┘
```

## 核心组件

### 1. Agent 运行时

**职责**: 执行 Agent 的核心逻辑

**组成**:
- `main.py` - Agent 主程序
- `config.json` - 运行时配置
- `prompts/agent.md` - 主提示词

**工作流程**:
1. 加载配置
2. 读取主提示词
3. 解析 Prompt 引用
4. 调用 AI API
5. 处理响应

### 2. Prompts 管理系统

**职责**: 管理和解析 Prompts

**组成**:
- 项目级 Prompts (`prompts/`)
- Agent 级 Prompts (`agents/{name}/prompts/`)
- 引用解析机制

**引用解析流程**:
```
读取 agent.md
    ↓
发现 #[[prompt:id]]
    ↓
在 Agent prompts/ 中查找
    ↓ (未找到)
在项目 prompts/ 中查找
    ↓ (找到)
加载并替换引用
```

### 3. Agent 导出系统

**职责**: 将 Agent 导出为独立包

**工作流程**:
```
1. 复制 Agent 文件
   ├── main.py
   ├── config.json
   └── prompts/

2. 扫描 Prompt 引用
   └── 提取所有 #[[prompt:xxx]]

3. 解析引用
   ├── 读取被引用的 Prompt
   ├── 检查 scope 字段
   └── 判断是否需要导出

4. 复制共享 Prompts
   └── 复制到导出目录的 prompts/

5. 生成独立包
   └── 完整的、可运行的 Agent
```

### 4. 文档系统

**职责**: 提供人类和 AI 的文档支持

**组成**:
- `docs/` - 人类文档
  - understanding/ - 理解项目
  - guides/ - 使用指南
  - development/ - 开发指南
  - reference/ - 参考资料
  
- `.kiro/steering/` - AI 指令
  - boundaries.md - 开发边界
  - workflow.md - 工作流程
  - coding-standards.md - 代码规范

## 数据流

### 开发时数据流

```
开发者编写代码
    ↓
创建/修改 Agent
    ↓
引用项目级 Prompts
    ↓
运行 Agent
    ↓
AI 解析引用并加载 Prompts
    ↓
执行任务
```

### 导出时数据流

```
执行导出脚本
    ↓
扫描 Agent 文件
    ↓
解析 Prompt 引用
    ↓
复制必需文件
    ↓
生成独立 Agent 包
    ↓
可分发的完整包
```

## 扩展点

### 1. 新增 Agent 类型

在 `agents/` 下创建新目录，遵循标准结构：
```
agents/new-agent/
├── main.py
├── config.json
└── prompts/
    └── agent.md
```

### 2. 新增共享 Prompts

在 `prompts/` 下创建新文件，设置正确的元数据：
```yaml
---
prompt_id: new_prompt_001
scope: shared
version: 1.0.0
---
```

### 3. 自定义导出逻辑

修改 `scripts/export-agent.py`，调整：
- 文件过滤规则
- 引用解析逻辑
- 导出目录结构

## 技术栈

### 核心技术
- **Python 3.7+** - 主要编程语言
- **Markdown** - 文档和 Prompts 格式
- **YAML** - 元数据格式
- **JSON** - 配置文件格式

### 开发工具
- **Kiro IDE** - AI 辅助开发环境
- **Git** - 版本控制
- **pip** - 包管理

### AI 服务
- 火山方舟豆包 API
- 支持其他兼容 OpenAI API 的服务

## 性能考虑

### Prompt 加载优化
- 缓存已加载的 Prompts
- 避免重复解析引用
- 延迟加载非必需 Prompts

### 导出优化
- 只复制必需的文件
- 使用 .export.json 排除不必要的文件
- 支持增量导出

## 安全考虑

### API Key 管理
- 不在代码中硬编码 API Key
- 使用环境变量或配置文件
- .gitignore 排除敏感配置

### 导出安全
- 检查导出路径，避免覆盖重要文件
- 验证引用的 Prompts 存在
- 记录导出日志

## 相关文档

- [设计理念](./design-philosophy.md) - 设计原则和决策
- [项目结构说明](./project-structure.md) - 目录结构
- [Prompts 管理指南](../guides/prompts-guide.md) - Prompts 使用
