# 开发规范

本文档定义了项目的开发规范和最佳实践。

## 语言要求

- 所有代码注释使用中文
- 所有文档使用中文编写
- 对话和交流使用中文

## 代码规范

### Python 代码规范

遵循 PEP 8 编码规范：

- 使用 4 个空格缩进
- 类名使用大驼峰命名（CamelCase）
- 函数和变量使用小写下划线命名（snake_case）
- 常量使用全大写下划线命名（UPPER_CASE）

### 注释规范

```python
def call_api(user_input):
    """调用 API 接口
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        str: API 返回的回复内容
    """
    pass
```

### 文档字符串

- 所有函数和类必须添加中文文档字符串
- 说明功能、参数、返回值
- 重要逻辑添加行内注释

## Git 提交规范

项目使用 Angular 提交规范，详细的分支管理和工作流程请参考：

- [Git 工作流程](./git-workflow.md) - 分支管理和工作流程
- [Angular 提交规范详解](../agents/my%20first%20agent/docs/git_commit_angular_001.md) - 详细的提交规范说明

### 快速参考

提交格式：
```
<type>(<scope>): <subject>
```

常用类型：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档变更
- `style`: 代码格式调整
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建工具或辅助工具变动

示例：
```
feat(agent): 添加新的对话 Agent

实现基于 GPT-4 的对话功能，支持流式输出

Closes #10
```

## 文档同步规范

当项目发生任何修改时，必须同步更新以下文档：

1. **README.md** - 更新项目简介、Agent 列表、更新日志
2. **相关文档** - 更新对应的详细文档
3. **更新日志** - 在 README.md 中记录变更

## 项目结构规范

### 核心目录概览

```
AI-Agents/
├── agents/                    # AI Agent 代码目录
│   └── [agent-name]/         # 各 Agent 实现
├── docs/                     # 项目文档目录
│   ├── agents/               # Agent 使用文档
│   └── issues/               # 开发过程记录
└── .kiro/                    # Kiro IDE 配置
```

完整的项目结构和文件职责说明请参考：[项目结构说明](./project-structure.md)

## 开发工作流程

1. 创建新分支进行开发
2. 编写代码并添加中文注释
3. 更新相关文档
4. 同步更新 README.md
5. 提交代码（使用规范的提交信息）
6. 创建 Pull Request

## 新增 Agent 流程

1. 在 `agents/` 目录下创建新的 Agent 文件夹
2. 实现 Agent 核心功能
3. 在 `docs/agents/` 下创建详细文档
4. 在 README.md 的"当前 Agents"部分添加说明
5. 更新 README.md 的更新日志

## 最佳实践

- 保持代码简洁清晰
- 单一职责原则
- 完善的错误处理
- 合理的日志输出
- 编写可复用的工具函数
- 配置与代码分离
