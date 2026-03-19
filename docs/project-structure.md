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
│       ├── docs/              # Agent 运行资源
│       │   ├── git_commit_angular_001.md
│       │   └── prompt_generator_001.md
│       └── references/        # 参考项目（可选）
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
│   └── quick-start.md         # 快速开始
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
├── config.py                  # 配置文件（可选）
├── utils.py                   # 工具函数（可选）
├── docs/                      # Agent 运行资源
│   └── *.md                   # prompt 模板等资源文件
└── references/                # 参考项目和代码示例（可选）
    ├── README.md              # 参考项目说明
    └── {参考项目目录}/        # 克隆的参考项目
```

**职责：**
- 存放 Agent 的核心实现代码
- 存放 Agent 运行时需要的资源文件（如 prompt 模板）
- 存放参考的其他 Agent 项目和代码示例（可选）
- 每个 Agent 独立一个子目录，便于管理和维护

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

##### `agents/{agent-name}/references/` - 参考项目目录（可选）
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
| Agent 资源 | `agents/{name}/docs/` | AI 系统 | 运行时资源 |
| Agent 参考 | `agents/{name}/references/` | 开发者 | 学习参考 |
| Agent 文档 | `docs/agents/{name}.md` | 用户 | 使用说明 |
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