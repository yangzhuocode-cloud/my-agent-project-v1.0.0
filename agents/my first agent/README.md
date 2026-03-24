# My First Agent

基于 OpenAI 兼容 API 的对话 Agent，支持多轮对话和智能任务规划。

## 功能特性

- OpenAI 协议兼容（支持火山方舟、OpenAI 等）
- 智能上下文管理（自动裁剪长对话）
- 多步任务规划（复杂任务自动拆分为多步骤执行）
- 失败重试机制

## 快速开始

### 1. 配置 API

复制配置文件并填入真实配置：

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

然后编辑 `.env` 文件：

```env
API_KEY=你的真实APIKey
MODEL=你的模型名称
```

### 2. 安装依赖

```bash
pip install requests
```

### 3. 启动 Agent

```bash
python main.py
```

## 配置说明

| 配置项 | 必须 | 说明 | 示例 |
|--------|------|------|------|
| `API_KEY` | ✅ | API 密钥 | `dc-xxxx-xxxx-xxxx` |
| `MODEL` | ✅ | 模型名称 | `doubao-pro-32k` |
| `BASE_URL` | - | API 端点（默认火山方舟） | `https://ark.cn-beijing.volces.com/api/v3` |
| `TEMPERATURE` | - | 随机性 0-1（默认 0.7） | `0.7` |
| `MAX_TOKENS` | - | 最大回复长度（默认 2000） | `2000` |

## 使用方式

### 对话模式

简单问答直接输入：

```
你：你好
Agent：你好！有什么可以帮你的？
```

### 任务模式

复杂任务会自动识别并分步执行：

```
你：分析近3个月销售数据并生成PPT报告

Agent：
🤖 （自动检测为复杂任务）

📝 正在规划任务步骤...

📋 任务步骤:
1. 获取销售数据
2. 数据清洗处理
3. 分析关键指标
4. 生成PPT报告
5. 校验内容完整性

============================================================
开始执行任务模式
============================================================

🔹 执行第 1/5 步: 获取销售数据
✅ 第1步完成

🔹 执行第 2/5 步: 数据清洗处理
✅ 第2步完成
...
```

## 项目结构

```
my first agent/
├── main.py              # 主程序入口
├── .env.example         # 配置示例
├── .env                 # 配置文件（不提交）
├── task_mode/           # 任务模式模块
│   ├── task_detector.py # 任务检测
│   ├── task_planner.py  # 步骤规划
│   ├── task_executor.py # 执行器
│   └── task_state.py    # 状态管理
├── prompts/             # 提示词
├── docs/                # 文档
└── references/          # 参考资料
```

## 文档

- [上下文管理](./docs/context-management.md)
- [开发日志](./docs/development-log.md)
