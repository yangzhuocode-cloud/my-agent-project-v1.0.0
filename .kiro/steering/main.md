---
inclusion: auto
---

# Kiro IDE 开发规范

本文件是 Kiro IDE 的自动加载指令，用于指导 AI 助手在开发过程中遵守项目规范。

## 语言要求

- 所有对话和交流必须使用中文
- 代码注释使用中文
- 文档和说明使用中文

## 文档同步规范

### 核心原则

- **`.kiro/steering/main.md`**：给 AI 助手读的开发指令
- **`README.md`**：给人类开发者读的项目介绍

### 必须同步更新的文档

当项目发生任何修改时，根据修改类型同步更新对应文档：

#### 1. `.kiro/steering/main.md` - AI 助手开发指令

**何时更新：**
- 新增或修改开发规范（代码规范、命名规范等）
- 新增或修改工作流程（AI 执行任务的步骤）
- 新增或修改目录结构规范
- 新增或修改文档同步规则本身
- 新增 Agent 类型需要特殊处理流程时

**更新内容：**
- 代码规范细节
- AI 助手工作流程
- 目录结构和文件职责
- 文档同步规则
- 新增 Agent 的标准流程

#### 2. `README.md` - 项目说明文档

**何时更新：**
- 新增或删除 Agent
- Agent 功能发生重大变化
- 项目简介或定位调整
- 新增或删除文档类别

**更新内容：**
- 项目简介和愿景
- 当前 Agents 列表（名称、简介、文档链接）
- 文档导航链接
- 更新日志（记录重要变更）

#### 3. `docs/agents/{agent-name}.md` - Agent 详细文档

**何时更新：**
- Agent 功能特性变更
- 使用方法变更
- 配置参数变更
- 新增扩展开发示例

**更新内容：**
- 功能特性说明
- 使用方法和示例
- 配置参数说明
- 扩展开发指南

#### 4. 其他配置文档

- `docs/configuration.md` - 配置参数变更时更新
- `docs/quick-start.md` - 使用流程变更时更新
- `docs/development-guide.md` - 开发规范变更时更新
- `docs/faq.md` - 新增常见问题时更新

## 代码规范

- 保持代码简洁清晰
- 遵循 Python PEP 8 编码规范
- 函数和类必须添加中文文档字符串
- 重要逻辑添加中文注释说明

## 提交规范

- 使用 Angular 提交规范（详见 `docs/development-guide.md`）
- 提交信息使用中文描述
- 每次提交前确保相关文档已同步更新

## 目录结构规范

### Agent 组织方式

```
agents/{agent-name}/
├── main.py                    # Agent 主程序
└── docs/                      # Agent 运行资源（prompt 模板等）
    └── *.md                   # 各类 prompt 模板文件

docs/
├── agents/
│   └── {agent-name}.md       # Agent 使用文档（面向用户）
├── issues/                    # 开发过程记录
│   ├── problems/              # 问题记录
│   │   ├── user/              # 用户提出的问题
│   │   └── ai/                # AI 开发过程中的问题
│   ├── notes/                 # 知识笔记和理解
│   │   ├── user/              # 用户的学习笔记
│   │   └── ai/                # AI 的学习和成长记录
│   └── ideas/                 # 想法和思路
│       ├── user/              # 用户的想法和思路
│       └── ai/                # AI 的想法和优化思路
├── configuration.md           # 配置说明
├── development-guide.md       # 开发规范
├── quick-start.md            # 快速开始
└── faq.md                    # 常见问题
```

### 文件职责说明

- `agents/{agent-name}/docs/` - 存放 Agent 运行时需要的资源文件（如 prompt 模板）
- `docs/agents/{agent-name}.md` - 存放面向用户的使用文档和说明
- `docs/issues/problems/` - 存放开发过程中遇到的问题和解决方案
- `docs/issues/notes/` - 存放知识笔记、学习记录和技术理解
- `docs/issues/ideas/` - 存放新想法、优化思路和未来规划

### 开发记录文件命名规范

在 `docs/issues/` 下的所有文档文件应遵循以下命名规范：

**格式**：`YYYYMMDD_简短描述.md`

**示例**：
- `problems/user/20260319_API调用超时问题.md`
- `notes/user/20260319_Python装饰器理解.md`
- `notes/ai/20260319_上下文管理优化思路.md`
- `ideas/user/20260320_新Agent开发计划.md`

## AI 助手工作流程

当用户要求修改代码或添加功能时，按以下步骤执行：

1. **修改代码或添加功能**
   - 保持代码简洁清晰
   - 添加中文注释和文档字符串

2. **判断并更新 `.kiro/steering/main.md`**（如适用）
   - 新增或修改了开发规范 → 更新"代码规范"章节
   - 新增或修改了工作流程 → 更新"AI 助手工作流程"章节
   - 新增或修改了目录结构 → 更新"目录结构规范"章节
   - 新增或修改了文档同步规则 → 更新"文档同步规范"章节

3. **判断并更新 `README.md`**（如适用）
   - 新增或删除 Agent → 更新"当前 Agents"章节
   - Agent 功能重大变化 → 更新对应 Agent 描述
   - 项目定位调整 → 更新"项目简介"章节
   - 任何重要变更 → 更新"更新日志"章节

4. **同步更新 `docs/agents/{agent-name}.md`**
   - 更新功能特性说明
   - 更新使用方法和示例
   - 更新配置参数说明
   - 更新扩展开发指南

5. **根据需要更新其他相关配置文档**
   - 配置参数变更 → `docs/configuration.md`
   - 使用流程变更 → `docs/quick-start.md`
   - 开发规范变更 → `docs/development-guide.md`
   - 新增常见问题 → `docs/faq.md`

6. **提交变更**
   - 使用规范的中文提交信息（Angular 规范）

## 新增 Agent 流程

1. 在 `agents/` 目录下创建新的 Agent 文件夹
2. 实现 Agent 核心功能（main.py）
3. 在 `agents/{agent-name}/docs/` 下创建 prompt 模板（如需要）
4. 在 `docs/agents/` 下创建详细使用文档
5. 在 README.md 的"当前 Agents"部分添加说明
6. 更新 README.md 的更新日志
