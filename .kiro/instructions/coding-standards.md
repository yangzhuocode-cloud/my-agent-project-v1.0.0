# 代码规范

> 🤖 **目标读者**: AI 助手  
> 🎯 **文档类型**: 执行指令

本文件定义项目的代码规范，AI 助手必须严格遵守。

## Python 代码规范

### 命名规范

```python
# 类名：大驼峰命名
class VolcArkDoubaoAgent:
    pass

# 函数名：小写下划线命名
def call_api(user_input):
    pass

# 变量名：小写下划线命名
user_message = "Hello"
api_response = None

# 常量：全大写下划线命名
API_KEY = "your-key"
MAX_TOKENS = 2000
BASE_URL = "https://api.example.com"

# 私有成员：单下划线前缀
class Agent:
    def __init__(self):
        self._context = []
    
    def _internal_method(self):
        pass
```

### 代码格式

```python
# 缩进：4 个空格
def example_function():
    if condition:
        do_something()
    else:
        do_other_thing()

# 行长度：最大 88 字符（Black 标准）
# 如果超过，使用括号换行
result = some_function(
    parameter1="value1",
    parameter2="value2",
    parameter3="value3"
)

# 空行：
# - 类定义前后 2 个空行
# - 方法定义之间 1 个空行
# - 逻辑块之间 1 个空行

class MyClass:
    """类文档字符串"""
    
    def method1(self):
        """方法文档字符串"""
        pass
    
    def method2(self):
        """方法文档字符串"""
        pass


class AnotherClass:
    """另一个类"""
    pass
```

### 文档字符串

```python
def call_api(user_input, temperature=0.7):
    """调用 API 接口
    
    Args:
        user_input (str): 用户输入的文本
        temperature (float, optional): 温度参数，控制随机性。默认 0.7
        
    Returns:
        str: API 返回的回复内容
        
    Raises:
        APIError: 当 API 调用失败时
        ValueError: 当参数无效时
        
    Examples:
        >>> response = call_api("你好")
        >>> print(response)
        '你好！有什么可以帮助你的吗？'
    """
    pass


class Agent:
    """AI Agent 基类
    
    这个类提供了 Agent 的基本功能，包括：
    - API 调用
    - 上下文管理
    - 错误处理
    
    Attributes:
        api_key (str): API 密钥
        model (str): 使用的模型名称
        context (list): 对话上下文
    """
    
    def __init__(self, api_key, model):
        """初始化 Agent
        
        Args:
            api_key (str): API 密钥
            model (str): 模型名称
        """
        self.api_key = api_key
        self.model = model
        self.context = []
```

### 注释规范

```python
# 行内注释：解释为什么这样做，而不是做什么
temperature = 0.7  # 使用较高温度以获得更有创意的回复

# 块注释：解释复杂逻辑
# 这里需要特殊处理上下文长度
# 因为 API 有 token 限制，我们需要：
# 1. 计算当前上下文的 token 数
# 2. 如果超过限制，删除最早的消息
# 3. 保留系统提示词
if len(context) > MAX_CONTEXT_LENGTH:
    context = context[-MAX_CONTEXT_LENGTH:]

# TODO 注释：标记待办事项
# TODO: 添加重试机制
# FIXME: 修复上下文溢出问题
# NOTE: 这里的实现参考了 OpenAI 的最佳实践
```

### 导入规范

```python
# 导入顺序：
# 1. 标准库
# 2. 第三方库
# 3. 本地模块

# 标准库
import os
import sys
from typing import List, Dict, Optional

# 第三方库
import requests
from dotenv import load_dotenv

# 本地模块
from .config import Config
from .utils import format_message

# 避免使用 import *
# 错误示例：
# from module import *

# 正确示例：
from module import specific_function, SpecificClass
```

### 错误处理

```python
# 使用具体的异常类型
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"连接错误: {e}")
except requests.exceptions.Timeout as e:
    print(f"请求超时: {e}")
except Exception as e:
    print(f"未知错误: {e}")

# 自定义异常
class APIError(Exception):
    """API 调用错误"""
    pass

class ConfigError(Exception):
    """配置错误"""
    pass

# 使用上下文管理器
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

## 配置文件规范

### JSON 配置

```json
{
  "api_key": "your-api-key",
  "model": "Doubao-Seed-2.0-pro",
  "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9
  }
}
```

### YAML 元数据

```yaml
---
prompt_id: example_prompt_001
scope: shared
agents: ["*"]
version: 1.0.0
description: 示例 Prompt
tags: ["example", "demo"]
created: 2026-03-19
updated: 2026-03-19
---
```

## 文件组织规范

### Agent 文件结构

```
agents/agent-name/
├── main.py              # 主程序
├── config.json          # 配置文件
├── .export.json         # 导出配置
├── prompts/             # Prompts 目录
│   ├── agent.md         # 主提示词
│   └── custom.md        # 自定义 Prompts
└── references/          # 参考项目（可选）
    └── README.md
```

### 模块化组织

```python
# main.py - 主程序入口
from config import load_config
from agent import Agent

def main():
    config = load_config()
    agent = Agent(config)
    agent.run()

if __name__ == "__main__":
    main()


# config.py - 配置管理
import json

def load_config(path="config.json"):
    """加载配置文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# agent.py - Agent 实现
class Agent:
    """Agent 核心实现"""
    
    def __init__(self, config):
        self.config = config
    
    def run(self):
        """运行 Agent"""
        pass
```

## 代码质量检查

### 必须通过的检查

- 无语法错误
- 无未使用的导入
- 无未定义的变量
- 符合 PEP 8 规范

### 推荐的工具

```bash
# 代码格式化
black main.py

# 代码检查
flake8 main.py
pylint main.py

# 类型检查
mypy main.py
```

## 相关文档

- [开发边界](./boundaries.md) - 开发边界和禁止事项
- [工作流程](./workflow.md) - 自动化工作流程
