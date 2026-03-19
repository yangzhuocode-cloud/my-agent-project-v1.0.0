# ADR-0003: Agent 导出机制

**状态**: 已采纳  
**日期**: 2026-03-19  
**决策者**: 项目团队

## 背景和问题

项目需要支持将单个 agent 导出为独立的可分发包。导出的 agent 应该：

1. **完全独立** - 包含所有运行所需的文件
2. **包含共享资源** - 自动包含引用的共享 prompt
3. **配置分离** - 区分运行时配置和构建时配置

面临的问题：

1. **配置文件职责混淆**
   - agent 需要运行时配置（model、baseUrl 等）
   - 导出需要构建时配置（shared_prompts、exclude_patterns 等）
   - 如果混在一起，导出的 agent 会包含不必要的构建配置

2. **共享资源管理**
   - 如何声明 agent 依赖哪些共享 prompt？
   - 如何在导出时自动复制这些文件？

3. **导出后的清洁性**
   - 导出的 agent 不应包含构建时的元数据
   - 只保留运行必需的文件

## 考虑的方案

### 方案 1: 单一配置文件

**描述**: 使用一个 `config.json` 包含所有配置

```json
{
  "name": "my first agent",
  "model": "qwen2.5:14b",
  "baseUrl": "http://localhost:11434",
  "shared_prompts": ["git_commit_angular_001"],
  "exclude_patterns": [".export.json", "__pycache__"]
}
```

**优点**:
- 简单，只有一个配置文件
- 易于理解

**缺点**:
- 职责混淆，运行时和构建时配置混在一起
- 导出的 agent 会包含不必要的构建配置
- 不符合单一职责原则

### 方案 2: 配置分离 + 导出时排除（推荐）

**描述**: 使用两个配置文件，职责清晰分离

```
agents/my first agent/
├── config.json       ← 运行时配置（导出✅）
└── .export.json      ← 导出配置（导出❌）
```

**config.json** - 运行时配置：
```json
{
  "name": "my first agent",
  "model": "qwen2.5:14b",
  "baseUrl": "http://localhost:11434",
  "temperature": 0.7,
  "coordination": {
    "role": "git_commit_generator",
    "dependencies": []
  }
}
```

**.export.json** - 导出配置：
```json
{
  "shared_prompts": ["git_commit_angular_001"],
  "shared_docs": [],
  "exclude_patterns": [
    ".export.json",
    "__pycache__",
    "*.pyc"
  ]
}
```

**优点**:
- 职责清晰，运行时和构建时配置分离
- 导出的 agent 只包含运行必需的文件
- `.` 开头的文件自然表示元数据/配置
- 符合单一职责原则

**缺点**:
- 需要维护两个配置文件
- 稍微增加了复杂度

### 方案 3: 脚本参数配置

**描述**: 不使用配置文件，通过脚本参数指定

```bash
python scripts/export-agent.py "my first agent" \
  --shared-prompts git_commit_angular_001 \
  --exclude __pycache__
```

**优点**:
- 不需要额外的配置文件
- 灵活，可以随时调整

**缺点**:
- 命令行参数过多时难以管理
- 不便于版本控制
- 每次导出都需要重新输入参数

## 决策

选择方案 2：配置分离 + 导出时排除

**理由**:

1. **职责清晰**
   - `config.json` = 运行时配置（agent 运行必需）
   - `.export.json` = 构建时配置（仅导出脚本使用）

2. **导出干净**
   - `.export.json` 不会出现在导出包中
   - 导出的 agent 只包含运行必需的文件

3. **易于维护**
   - 开发时只维护一份共享文件
   - 通过 `.export.json` 声明依赖关系

4. **符合惯例**
   - `.` 开头的文件通常是元数据/配置
   - 导出时自动排除很自然

## 影响

**正面影响**:

1. **配置清晰**
   - 运行时和构建时配置分离
   - 每个文件职责明确

2. **导出可靠**
   - 自动处理共享资源复制
   - 自动排除构建时文件

3. **易于扩展**
   - 可以添加更多导出配置选项
   - 不影响运行时配置

**负面影响**:

1. **文件数量增加**
   - 每个 agent 需要两个配置文件
   - 需要理解两者的区别

2. **学习成本**
   - 需要知道何时修改哪个配置文件

**需要的工作**:

1. 为所有 agent 创建 `config.json` 和 `.export.json`
2. 编写导出脚本 `export-agent.py`
3. 实现虚拟路径引用解析
4. 实现共享资源自动复制
5. 编写使用文档

## 实现细节

### 导出流程

```python
def export_agent(agent_name, output_dir="exports"):
    """导出 agent 为独立包"""
    
    # 1. 读取导出配置
    export_config = read_json(f"agents/{agent_name}/.export.json")
    
    # 2. 创建导出目录
    export_path = f"{output_dir}/{agent_name}"
    create_directory(export_path)
    
    # 3. 复制 agent 文件（排除 .export.json 等）
    copy_agent_files(
        source=f"agents/{agent_name}",
        dest=export_path,
        exclude=export_config['exclude_patterns']
    )
    
    # 4. 处理 prompt 引用
    main_prompt = read_file(f"{export_path}/prompts/main_prompt.md")
    prompt_refs = extract_prompt_references(main_prompt)
    
    # 5. 复制引用的共享 prompts
    for prompt_id in prompt_refs:
        source = f"prompts/{prompt_id}.md"
        dest = f"{export_path}/prompts/{prompt_id}.md"
        copy_file(source, dest)
    
    # 6. 复制声明的共享 prompts（兼容旧方式）
    for prompt_id in export_config.get('shared_prompts', []):
        source = f"prompts/{prompt_id}.md"
        dest = f"{export_path}/prompts/{prompt_id}.md"
        if not file_exists(dest):
            copy_file(source, dest)
    
    print(f"✅ 导出完成: {export_path}")
```

### 导出后的结构

```
exports/my-first-agent/
├── config.json              ← 保留（运行时需要）
├── main.py
├── prompts/
│   ├── main_prompt.md       ← 包含 #[[prompt:xxx]] 引用（不变）
│   └── git_commit_angular_001.md  ← 自动复制的共享文件
└── references/
    └── README.md
```

### 使用方法

```bash
# 基本用法
python scripts/export-agent.py "my first agent"

# 指定导出目录
python scripts/export-agent.py "my first agent" --output ./my-exports
```

## 相关决策

- [ADR-0001: 虚拟路径引用机制](./0001-虚拟路径引用机制.md) - 定义了如何引用 prompt
- [ADR-0002: Prompts 分离架构](./0002-Prompts分离架构.md) - 定义了 prompt 的组织方式

## 参考资料

- [Agent 导出指南](../../guides/agent-export-guide.md)
- [配置文件说明](../../guides/configuration.md)
