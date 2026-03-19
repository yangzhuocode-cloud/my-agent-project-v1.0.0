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

**重要**：项目结构信息已集中管理在 `docs/project-structure.md`，其他文档使用简化版本+引用链接的方式。

#### 1. `docs/project-structure.md` - 项目结构集中文档

**何时更新：**
- 新增或删除目录
- 调整目录层级结构
- 修改文件职责说明
- 新增或删除文件类型

**更新内容：**
- 完整的项目目录树
- 各目录和文件的职责说明
- 命名规范和扩展规范

#### 2. `.kiro/steering/main.md` - AI 助手开发指令

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

#### 3. `README.md` - 项目说明文档

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

#### 4. `docs/agents/{agent-name}.md` - Agent 详细文档

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

#### 5. 其他配置文档

- `docs/configuration.md` - 配置参数变更时更新
- `docs/quick-start.md` - 使用流程变更时更新
- `docs/development-guide.md` - 开发规范变更时更新
- `docs/git-workflow.md` - Git 分支管理和工作流程变更时更新
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

### 项目结构概览

```
AI-Agents/
├── agents/                    # AI Agent 代码目录
│   └── [agent-name]/         # 各 Agent 实现
├── docs/                     # 项目文档目录
│   ├── agents/               # Agent 使用文档
│   └── issues/               # 开发过程记录
└── .kiro/                    # Kiro IDE 配置
```

完整的项目结构和文件职责说明请参考：[项目结构说明](./docs/project-structure.md)

### 文件职责说明

- `agents/{agent-name}/docs/` - 存放 Agent 运行时需要的资源文件（如 prompt 模板）
- `agents/{agent-name}/references/` - 存放参考的其他 Agent 项目和代码示例（可选）
- `docs/agents/{agent-name}.md` - 存放面向用户的使用文档和说明
- `docs/issues/problems/` - 存放开发过程中遇到的问题和解决方案
- `docs/issues/notes/` - 存放知识笔记、学习记录和技术理解
- `docs/issues/ideas/` - 存放新想法、优化思路和未来规划

### References 目录使用规范

每个 Agent 可以有自己的 `references/` 目录，用于存放参考的其他 Agent 项目和代码示例。

**使用方法**：
1. 在 Agent 目录下创建 `references/` 目录
2. 使用 `git clone` 克隆参考项目到该目录
3. 在 `references/README.md` 中记录项目信息和参考价值
4. 学习笔记记录在 `docs/issues/notes/user/` 目录下

**示例**：
```bash
cd "agents/my first agent/references"
git clone https://github.com/example/agent-project.git
```

### 开发记录文件命名规范

#### User 文档命名（给人类看）

在 `docs/issues/problems/user/`、`docs/issues/notes/user/`、`docs/issues/ideas/user/` 下：

**格式**：`YYYYMMDD_简短描述.md`

**示例**：
- `20260319_API调用超时问题.md`
- `20260319_Python装饰器理解.md`
- `20260320_新Agent开发计划.md`

#### AI 文档命名（给 AI 看）

在 `docs/issues/problems/ai/`、`docs/issues/notes/ai/`、`docs/issues/ideas/ai/` 下：

**格式**：`{关键词-slug}.md`

**Slug 生成规则**：
1. 提取问题核心关键词（2-4 个英文词）
2. 转换为小写
3. 用连字符（-）连接
4. 使用英文描述（便于搜索和去重）

**示例**：
- Git 提交信息未加引号 → `git-commit-quote-error.md`
- API 调用超时 → `api-timeout.md`
- Python 依赖安装失败 → `python-dependency-install.md`
- 上下文管理优化 → `context-management-optimization.md`

### AI 问题文档格式要求

AI 创建的问题文档必须包含以下结构：

#### 1. YAML 头文件（必填）

```yaml
---
slug: 问题的唯一标识符（与文件名一致）
keywords: [关键词1, 关键词2, ...]  # 用于搜索和分类
first_occurred: YYYY-MM-DD  # 首次发生日期
last_updated: YYYY-MM-DD    # 最后更新日期
occurrences: N              # 发生次数
---
```

#### 2. 文档正文（必填章节）

- **标题**：问题的完整描述
- **问题描述**：详细说明问题现象
- **问题原因分析**：分析问题的根本原因
- **解决方案**：提供具体的解决方法
- **重复发生记录**：记录每次发生的时间、场景和处理方式
- **预防措施**（可选）：如何避免问题再次发生
- **相关知识点**（可选）：扩展知识
- **参考资源**（可选）：相关文档链接

#### 3. 重复发生记录格式

```markdown
## 重复发生记录

### 第 1 次：YYYY-MM-DD HH:MM
- **场景**：具体场景描述
- **错误信息**：错误输出（如有）
- **处理**：如何解决

### 第 2 次：YYYY-MM-DD HH:MM
- **场景**：具体场景描述
- **处理**：如何解决
- **反思**：为什么再次发生，如何改进
```

### AI 自动记录问题的触发条件

AI 助手在以下情况下应自动创建或更新问题文档：

#### 触发条件

1. **命令执行失败**
   - Git 命令报错
   - Shell 命令执行失败
   - API 调用失败

2. **重复性错误**
   - 同一个错误在本次会话中第二次出现
   - 需要更新已有问题文档，添加"重复发生记录"

3. **配置或环境问题**
   - 依赖缺失
   - 配置错误
   - 权限问题

4. **代码执行异常**
   - 语法错误
   - 运行时错误
   - 逻辑错误

#### 查重流程

在创建新问题文档前，必须先查重：

1. **提取关键词**：从错误信息中提取 2-4 个核心关键词
2. **生成 slug**：将关键词转换为小写，用连字符连接
3. **搜索已有文档**：使用 `fileSearch` 或 `grepSearch` 在 `docs/issues/problems/ai/` 目录下搜索 slug
4. **判断处理**：
   - 如果找到匹配文档 → 更新文档，在"重复发生记录"章节添加新记录，更新 `last_updated` 和 `occurrences`
   - 如果未找到 → 创建新文档，使用 slug 作为文件名

#### 创建新文档的要求

- 文件名：`{slug}.md`
- 必须包含完整的 YAML 头文件
- 必须包含所有必填章节
- `occurrences` 初始值为 1
- `first_occurred` 和 `last_updated` 设置为当前日期

#### 更新已有文档的要求

- 在"重复发生记录"章节末尾添加新记录
- 更新 YAML 头文件中的 `last_updated` 为当前日期
- 更新 `occurrences` 数值加 1
- 如有新的解决方案或反思，补充到对应章节

## AI 助手工作流程

当用户要求修改代码或添加功能时，按以下步骤执行：

1. **修改代码或添加功能**
   - 保持代码简洁清晰
   - 添加中文注释和文档字符串

2. **判断并更新 `docs/project-structure.md`**（如适用）
   - 新增或删除目录 → 更新完整目录树
   - 调整目录层级 → 更新目录结构
   - 修改文件职责 → 更新职责说明
   - 新增文件类型 → 更新扩展规范

3. **判断并更新 `.kiro/steering/main.md`**（如适用）
   - 新增或修改了开发规范 → 更新"代码规范"章节
   - 新增或修改了工作流程 → 更新"AI 助手工作流程"章节
   - 新增或修改了目录结构 → 更新"目录结构规范"章节
   - 新增或修改了文档同步规则 → 更新"文档同步规范"章节

4. **判断并更新 `README.md`**（如适用）
   - 新增或删除 Agent → 更新"当前 Agents"章节
   - Agent 功能重大变化 → 更新对应 Agent 描述
   - 项目定位调整 → 更新"项目简介"章节
   - 任何重要变更 → 更新"更新日志"章节

5. **同步更新 `docs/agents/{agent-name}.md`**
   - 更新功能特性说明
   - 更新使用方法和示例
   - 更新配置参数说明
   - 更新扩展开发指南

6. **根据需要更新其他相关配置文档**
   - 配置参数变更 → `docs/configuration.md`
   - 使用流程变更 → `docs/quick-start.md`
   - 开发规范变更 → `docs/development-guide.md`
   - Git 工作流程变更 → `docs/git-workflow.md`
   - 新增常见问题 → `docs/faq.md`

7. **自动记录问题（如遇到）**
   - 执行过程中遇到错误或问题 → 先查重，再决定创建或更新
   - 查重流程：
     1. 提取问题关键词，生成 slug
     2. 使用 `fileSearch` 搜索 `docs/issues/problems/ai/{slug}.md`
     3. 找到 → 更新文档，添加"重复发生记录"
     4. 未找到 → 创建新文档 `docs/issues/problems/ai/{slug}.md`
   - 文档必须包含完整的 YAML 头文件和所有必填章节
   - 同一个问题不重复创建文档，只更新重复记录

8. **响应用户记录请求**
   - 用户要求记录问题 → 在 `docs/issues/problems/user/` 下创建，使用时间前缀命名
   - 用户要求记录笔记 → 在 `docs/issues/notes/user/` 下创建，使用时间前缀命名
   - 用户要求记录想法 → 在 `docs/issues/ideas/user/` 下创建，使用时间前缀命名
   - 文件命名格式：`YYYYMMDD_简短描述.md`

9. **提交变更**
   - 使用规范的中文提交信息（Angular 规范）
   - 提交信息必须用双引号包裹

## 新增 Agent 流程

1. 在 `agents/` 目录下创建新的 Agent 文件夹
2. 实现 Agent 核心功能（main.py）
3. 在 `agents/{agent-name}/docs/` 下创建 prompt 模板（如需要）
4. 在 `docs/agents/` 下创建详细使用文档
5. 更新 `docs/project-structure.md` 中的目录结构（如有新的目录类型）
6. 在 README.md 的"当前 Agents"部分添加说明
7. 更新 README.md 的更新日志
