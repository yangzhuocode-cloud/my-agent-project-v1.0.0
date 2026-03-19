# 项目结构说明

本文档详细说明了 AI Agents 项目的完整目录结构和文件职责。

## 完整项目结构

```
AI-Agents/
├── .git/                      # Git 版本控制
├── .idea/                     # IDE 配置文件
├── .kiro/                     # Kiro IDE 配置
│   └── steering/
│       └── main.md            # AI 助手开发指令
├── agents/                    # AI Agent 代码目录
│   └── my first agent/        # 示例 Agent
│       ├── main.py            # Agent 主程序
│       ├── config.json        # Agent 运行时配置
│       ├── .export.json       # Agent 导出配置（不导出）
│       ├── prompts/           # Agent 的 Prompts 目录
│       │   ├── agent.md       # Agent 主提示词（必需）
│       │   └── *.md           # Agent 私有的其他 Prompts
│       └── references/        # Agent 特定参考项目（可选）
│           └── README.md      # 参考项目说明
├── docs/                      # 项目文档目录
│   ├── agents/                # 各 Agent 使用文档
│   │   └── my-first-agent.md  # My First Agent 使用说明
│   ├── issues/                # 开发过程记录
│   │   ├── problems/          # 问题记录
│   │   │   ├── user/          # 用户提出的问题
│   │   │   └── ai/            # AI 开发过程中的问题
│   │   ├── notes/             # 知识笔记和理解
│   │   │   ├── user/          # 用户的学习笔记
│   │   │   └── ai/            # AI 的学习记录
│   │   └── ideas/             # 想法和思路
│   │       ├── user/          # 用户的想法和思路
│   │       └── ai/            # AI 的想法和优化思路
│   ├── configuration.md       # 配置说明
│   ├── development-guide.md   # 开发规范
│   ├── faq.md                 # 常见问题
│   ├── git-workflow.md        # Git 工作流程
│   ├── issues-guide.md        # 开发过程记录指南
│   ├── project-structure.md   # 项目结构说明（本文档）
│   ├── prompts-guide.md       # Prompts 管理指南
│   └── quick-start.md         # 快速开始
├── prompts/                   # 项目级 Prompts（单一数据源）
│   ├── git_commit_angular_001.md    # 共享 Prompt
│   └── prompt_generator_001.md      # 项目私有 Prompt
├── references/                # 项目级通用参考资源
│   └── ollama-python/         # Ollama Python SDK
├── scripts/                   # 项目脚本
│   └── export-agent.py        # Agent 导出脚本
├── CHANGELOG.md               # 更新日志
└── README.md                  # 项目说明
```

## 目录职责说明

### 核心目录

#### `agents/` - AI Agent 代码目录
存放所有 AI Agent 的实现代码和运行资源。

**子目录结构：**
```
agents/{agent-name}/
├── main.py                    # Agent 主程序
├── config.json                # Agent 运行时配置
├── .export.json               # Agent 导出配置（不导出）
├── prompts/                   # Agent 的 Prompts 目录
│   ├── agent.md               # Agent 主提示词（必需）
│   └── *.md                   # Agent 私有的其他 Prompts
└── references/                # 参考项目和代码示例（可选）
    ├── README.md              # 参考项目说明
    └── {参考项目目录}/        # 克隆的参考项目
```

**职责：**
- 存放 Agent 的核心实现代码
- 存放 Agent 的配置文件（运行时配置和导出配置）
- 存放 Agent 的 Prompts（主提示词和私有 Prompts）
- 存放参考的其他 Agent 项目和代码示例（可选）
- 每个 Agent 独立一个子目录，便于管理和维护

**重要文件说明：**
- `agent.md`：每个 Agent 必须有的主提示词文件
- `config.json`：Agent 运行时配置（model、baseUrl 等）
- `.export.json`：导出配置，指定排除的文件模式

#### `prompts/` - 项目级 Prompts 目录
存放项目级别的 Prompts，作为单一数据源。

**职责：**
- 存放可被多个 Agent 共享的 Prompts（`scope: shared`）
- 存放项目级别的规范和标准
- 避免在多个 Agent 中重复维护相同内容

**使用方式：**
- Agent 通过 `#[[prompt:prompt_id]]` 语法引用
- 导出时自动复制到 Agent 的 `prompts/` 目录

**详细说明：** 参见 [Prompts 管理指南](./prompts-guide.md)

#### `docs/` - 项目文档目录
存放所有面向用户的文档和开发过程记录。

**子目录说明：**

##### `docs/agents/` - Agent 使用文档
存放面向用户的 Agent 使用说明和教程。

- **文件命名**：`{agent-name}.md`
- **内容**：功能介绍、使用方法、配置说明、示例代码
- **目标读者**：项目使用者和开发者

##### `docs/issues/` - 开发过程记录
记录开发过程中的问题、学习笔记和想法思路。

**子目录结构：**
```
docs/issues/
├── problems/              # 问题记录
│   ├── user/              # 用户提出的问题（时间前缀命名）
│   └── ai/                # AI 遇到的问题（slug 命名）
├── notes/                 # 学习笔记
│   ├── user/              # 用户的学习笔记（时间前缀命名）
│   └── ai/                # AI 的学习记录（slug 命名）
└── ideas/                 # 想法和思路
    ├── user/              # 用户的想法（时间前缀命名）
    └── ai/                # AI 的优化思路（slug 命名）
```

**命名规范：**
- **User 文档**：`YYYYMMDD_简短描述.md`
- **AI 文档**：`{关键词-slug}.md`

##### `agents/{agent-name}/references/` - Agent 特定参考项目（可选）
存放该 Agent 开发过程中参考的其他 Agent 项目和代码示例。

**使用场景：**
- 学习其他优秀的 Agent 实现
- 参考类似功能的代码示例
- 研究不同的技术方案

**使用方法：**
1. 在 Agent 目录下创建 `references/` 目录
2. 使用 `git clone` 克隆参考项目
3. 在 `references/README.md` 中记录项目信息和参考价值

**示例：**
```bash
cd "agents/my first agent/references"
git clone https://github.com/example/agent-project.git
```

**注意事项：**
- 参考项目仅供学习，请遵守各项目的开源协议
- 学习笔记记录在 `docs/issues/notes/user/` 目录下
- 定期更新参考项目以获取最新代码

#### `references/` - 项目级通用参考资源
存放项目级别的通用参考资源，如 SDK、库、工具等。

**与 Agent 特定参考项目的区别：**
- **顶级 `references/`**：存放通用的、多个 Agent 可能共用的参考资源
  - 示例：ollama-python SDK、通用工具库、框架代码
  - 特点：与具体 Agent 无关，项目级别的依赖和参考
  
- **`agents/{name}/references/`**：存放特定 Agent 的参考项目
  - 示例：learn-claude-code、ai-agents-from-scratch
  - 特点：与该 Agent 的实现直接相关，用于学习和参考

**使用方法：**
```bash
cd references
git clone https://github.com/ollama/ollama-python.git
```

**注意事项：**
- 评估参考资源的通用性，决定放在哪个 references 目录
- 项目级参考资源应该是多个 Agent 可能用到的
- 遵守各项目的开源协议

### 配置目录

#### `.kiro/` - Kiro IDE 配置
存放 Kiro IDE 的配置文件和开发指令。

- **`.kiro/steering/main.md`**：AI 助手开发指令，定义开发规范和工作流程

### 根目录文件

- **`README.md`**：项目说明文档，面向人类开发者
- **`CHANGELOG.md`**：项目更新日志
- **`.git/`**：Git 版本控制目录
- **`.idea/`**：IDE 配置文件目录

## 文件职责对比

| 文件类型 | 存放位置 | 目标读者 | 内容特点 |
|----------|----------|----------|----------|
| Agent 代码 | `agents/{name}/main.py` | 开发者 | 实现逻辑 |
| Agent 配置 | `agents/{name}/config.json` | Agent 运行时 | 运行时配置 |
| Agent 主提示词 | `agents/{name}/prompts/agent.md` | AI 系统 | Agent 核心提示词 |
| Agent 私有 Prompts | `agents/{name}/prompts/*.md` | AI 系统 | Agent 专属 Prompts |
| 共享 Prompts | `prompts/*.md` | AI 系统 | 多 Agent 共享 |
| Agent 参考 | `agents/{name}/references/` | 开发者 | Agent 特定参考 |
| Agent 文档 | `docs/agents/{name}.md` | 用户 | 使用说明 |
| 项目参考 | `references/` | 开发者 | 通用参考资源 |
| 开发指令 | `.kiro/steering/main.md` | AI 助手 | 开发规范 |
| 项目说明 | `README.md` | 人类开发者 | 项目介绍 |

## 扩展规范

### 新增 Agent 时的目录创建

1. 在 `agents/` 下创建 Agent 目录
2. 在 `docs/agents/` 下创建使用文档
3. 更新 `README.md` 中的 Agent 列表

### 新增文档类型时的目录规划

1. 评估是否属于现有分类
2. 如需新分类，在 `docs/` 下创建新子目录
3. 更新本文档的结构说明

## 维护说明

本文档是项目目录结构的单一数据源，当目录结构发生变更时：

1. **优先更新本文档**
2. **其他文档通过引用链接指向本文档**
3. **避免在多个文档中重复维护相同的结构信息**

这样确保了结构信息的一致性和维护效率。