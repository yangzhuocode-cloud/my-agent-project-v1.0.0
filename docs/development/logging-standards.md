# Agent 项目日志规范

## 概述

本文档定义了 Agent 项目的日志标准和最佳实践。良好的日志系统是 Agent 自动化、调试和优化的基础。

## 设计原则

1. **可观测性优先**：关键路径必须有日志
2. **结构化优先**：便于 AI 解析和分析
3. **分级管理**：不同环境不同详细程度
4. **性能友好**：日志不应显著影响性能
5. **便于调试**：出问题时能快速定位

## 日志级别定义

### DEBUG（调试）
- **用途**：详细的调试信息
- **内容**：变量值、中间状态、循环迭代
- **场景**：开发和调试阶段
- **示例**：
  ```python
  logger.debug(f"处理消息 {i}/{total}: role={msg['role']}, length={len(msg['content'])}")
  ```

### INFO（信息）
- **用途**：关键流程节点
- **内容**：函数入口/出口、状态变更、重要操作
- **场景**：生产环境默认级别
- **示例**：
  ```python
  logger.info(f"API 调用成功: {response.status_code}, tokens={total_tokens}")
  ```

### WARNING（警告）
- **用途**：异常但可恢复的情况
- **内容**：接近阈值、重复错误、降级处理
- **场景**：需要关注但不影响运行
- **示例**：
  ```python
  logger.warning(f"Token 使用率达到 {usage_ratio:.1%}，接近阈值")
  ```

### ERROR（错误）
- **用途**：错误但程序继续
- **内容**：API 失败、解析错误、异常捕获
- **场景**：需要人工介入或自动重试
- **示例**：
  ```python
  logger.error(f"API 调用失败: {str(e)}", exc_info=True)
  ```

### CRITICAL（致命）
- **用途**：致命错误，程序无法继续
- **内容**：初始化失败、配置错误、资源耗尽
- **场景**：程序即将退出
- **示例**：
  ```python
  logger.critical(f"配置文件加载失败: {config_path}")
  ```


## 渐进式日志策略

### 阶段 1: 初始开发（关键路径日志）

**目标**：确保关键流程可追踪

**必须记录的节点**：
1. 函数入口和出口
2. 外部调用（API、数据库、文件 I/O）
3. 状态变更（上下文裁剪、配置更新）
4. 异常捕获
5. 关键决策点

**示例**：
```python
def call_api(self, user_input):
    """调用 API"""
    logger.info(f"API 调用开始: {user_input[:50]}...")
    
    try:
        # 构建请求
        payload = self._build_payload(user_input)
        logger.debug(f"请求体构建完成: {len(payload['messages'])} 条消息")
        
        # 发送请求
        response = requests.post(url, json=payload)
        logger.info(f"API 响应: {response.status_code}")
        
        # 处理响应
        result = self._parse_response(response)
        logger.info(f"API 调用成功: {len(result)} 字符")
        
        return result
        
    except Exception as e:
        logger.error(f"API 调用失败: {str(e)}", exc_info=True)
        return None
```

**日志配置**：
```python
# 控制台：INFO
# 文件：DEBUG
```

### 阶段 2: 问题调试（增强日志）

**目标**：快速定位问题

**临时增加的日志**：
1. 详细的变量值
2. 循环中的每次迭代
3. 条件判断的结果
4. 中间计算结果

**示例**：
```python
def _smart_trim(self):
    """智能裁剪"""
    logger.info("=" * 60)
    logger.info("开始智能裁剪")
    
    # 增加详细日志
    logger.debug(f"当前状态:")
    logger.debug(f"  - recent: {len(self.context['recent'])} 条")
    logger.debug(f"  - errors: {len(self.context['important']['errors'])} 个")
    logger.debug(f"  - milestones: {len(self.context['important']['milestones'])} 个")
    
    # 详细记录每条消息
    for i, msg in enumerate(self.context["recent"]):
        logger.debug(f"消息 {i}: role={msg['role']}, "
                    f"priority={msg['priority']}, "
                    f"length={len(msg['content'])}, "
                    f"timestamp={msg['timestamp']}")
    
    # ... 裁剪逻辑
    
    logger.info(f"裁剪完成: 删除 {removed_count} 条")
    logger.info("=" * 60)
```

**日志配置**：
```python
# 控制台：DEBUG（临时）
# 文件：DEBUG
```

### 阶段 3: 生产稳定（精简日志）

**目标**：保持可观测性，减少噪音

**保留的日志**：
1. 关键流程节点（INFO）
2. 错误和警告（WARNING/ERROR）
3. 性能指标
4. 结构化事件日志

**移除的日志**：
1. 详细的变量值（DEBUG）
2. 循环迭代细节（DEBUG）
3. 中间状态（DEBUG）

**示例**：
```python
def _smart_trim(self):
    """智能裁剪"""
    logger.info(f"触发裁剪: {len(self.context['recent'])} 条消息")
    
    # ... 裁剪逻辑（移除详细 debug 日志）
    
    logger.info(f"裁剪完成: 删除 {removed_count} 条，保留 {len(self.context['recent'])} 条")
```

**日志配置**：
```python
# 控制台：INFO
# 文件：INFO
# 事件日志：结构化 JSON
```


## 日志系统实现

### 基础配置

```python
import logging
import sys
from pathlib import Path

def setup_logger(name, log_dir="logs", console_level=logging.INFO, file_level=logging.DEBUG):
    """
    设置日志系统
    
    Args:
        name: 日志器名称
        log_dir: 日志目录
        console_level: 控制台日志级别
        file_level: 文件日志级别
    
    Returns:
        配置好的 logger
    """
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 创建日志目录
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # 控制台 Handler（INFO 级别）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # 文件 Handler（DEBUG 级别）
    file_handler = logging.FileHandler(
        f"{log_dir}/{name}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # 添加 handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

### 使用示例

```python
class APIModelAgent:
    def __init__(self):
        # 初始化日志
        self.logger = setup_logger('APIAgent')
        self.logger.info("Agent 初始化开始")
        
        # ... 初始化逻辑
        
        self.logger.info("Agent 初始化完成")
    
    def call_api(self, user_input):
        """调用 API"""
        self.logger.info(f"API 调用: {user_input[:50]}...")
        
        try:
            # ... API 调用逻辑
            self.logger.info(f"API 成功: {tokens} tokens")
            return result
        except Exception as e:
            self.logger.error(f"API 失败: {e}", exc_info=True)
            return None
```


## Agent 特有：结构化事件日志

### 为什么需要结构化日志？

1. **便于 AI 解析**：JSON 格式易于程序处理
2. **便于统计分析**：可以查询、聚合、可视化
3. **便于问题复现**：完整记录上下文状态
4. **便于性能优化**：精确的性能指标

### 事件日志格式

使用 JSON Lines 格式（每行一个 JSON 对象）：

```python
import json
import time
from pathlib import Path

class EventLogger:
    """结构化事件日志"""
    
    def __init__(self, log_file="logs/events.jsonl"):
        self.log_file = log_file
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    def log_event(self, event_type, data):
        """记录事件"""
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "data": data
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

### 关键事件类型

#### 1. API 调用事件

```python
def log_api_call(self, request, response, duration):
    """记录 API 调用"""
    self.event_logger.log_event("api_call", {
        "request": {
            "messages_count": len(request["messages"]),
            "estimated_tokens": self._estimate_tokens(request["messages"])
        },
        "response": {
            "status_code": response.status_code,
            "actual_tokens": response.json().get("usage", {}).get("total_tokens", 0),
            "reply_length": len(response.json()["choices"][0]["message"]["content"])
        },
        "duration_ms": duration * 1000
    })
```

#### 2. 上下文裁剪事件

```python
def log_trim_event(self, before, after, removed_count):
    """记录裁剪事件"""
    self.event_logger.log_event("context_trim", {
        "before": {
            "recent_count": before["recent_count"],
            "estimated_tokens": before["estimated_tokens"],
            "usage_ratio": before["usage_ratio"]
        },
        "after": {
            "recent_count": after["recent_count"],
            "estimated_tokens": after["estimated_tokens"],
            "usage_ratio": after["usage_ratio"]
        },
        "removed_count": removed_count,
        "removed_priorities": after["removed_priorities"]
    })
```

#### 3. 错误事件

```python
def log_error_event(self, error_type, error_message, context):
    """记录错误事件"""
    self.event_logger.log_event("error", {
        "error_type": error_type,
        "error_message": error_message,
        "context": {
            "function": context.get("function"),
            "recent_count": len(self.context["recent"]),
            "last_operation": context.get("last_operation")
        }
    })
```

#### 4. 性能指标事件

```python
def log_performance(self, operation, duration_ms, details=None):
    """记录性能指标"""
    self.event_logger.log_event("performance", {
        "operation": operation,
        "duration_ms": duration_ms,
        "details": details or {}
    })
```

### 事件日志示例

```json
{"timestamp": 1774027085.123, "event_type": "api_call", "data": {"request": {"messages_count": 3, "estimated_tokens": 82}, "response": {"status_code": 200, "actual_tokens": 318, "reply_length": 115}, "duration_ms": 1234.56}}
{"timestamp": 1774027086.456, "event_type": "context_trim", "data": {"before": {"recent_count": 16, "estimated_tokens": 7895, "usage_ratio": 0.031}, "after": {"recent_count": 10, "estimated_tokens": 5000, "usage_ratio": 0.020}, "removed_count": 6}}
{"timestamp": 1774027087.789, "event_type": "error", "data": {"error_type": "UnicodeEncodeError", "error_message": "gbk codec can't encode character", "context": {"function": "print_reply", "recent_count": 10}}}
```


## 上下文快照

### 为什么需要快照？

1. **问题复现**：保存出错时的完整状态
2. **调试分析**：离线分析上下文变化
3. **性能优化**：分析裁剪效果
4. **测试验证**：对比预期和实际状态

### 快照实现

```python
import json
from pathlib import Path
from datetime import datetime

class ContextSnapshot:
    """上下文快照管理"""
    
    def __init__(self, snapshot_dir="logs/snapshots"):
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    def save_snapshot(self, context, reason, metadata=None):
        """
        保存上下文快照
        
        Args:
            context: 上下文对象
            reason: 保存原因（如 "before_trim", "api_error"）
            metadata: 额外的元数据
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{reason}_{timestamp}.json"
        
        snapshot = {
            "timestamp": time.time(),
            "reason": reason,
            "metadata": metadata or {},
            "context": {
                "permanent": context["permanent"],
                "important": {
                    "errors_count": len(context["important"]["errors"]),
                    "errors": context["important"]["errors"][-5:],  # 最近 5 个
                    "milestones": context["important"]["milestones"]
                },
                "recent": {
                    "count": len(context["recent"]),
                    "messages": [
                        {
                            "role": msg["role"],
                            "content_length": len(msg["content"]),
                            "content_preview": msg["content"][:100],
                            "priority": msg["priority"],
                            "timestamp": msg["timestamp"]
                        }
                        for msg in context["recent"]
                    ]
                }
            }
        }
        
        filepath = self.snapshot_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
```

### 快照触发时机

```python
class APIModelAgent:
    def __init__(self):
        self.snapshot = ContextSnapshot()
    
    def _smart_trim(self):
        """智能裁剪"""
        # 裁剪前保存快照
        self.snapshot.save_snapshot(
            self.context,
            reason="before_trim",
            metadata={
                "trigger": "threshold_reached",
                "usage_ratio": self._get_usage_ratio()
            }
        )
        
        # ... 裁剪逻辑
        
        # 裁剪后保存快照
        self.snapshot.save_snapshot(
            self.context,
            reason="after_trim",
            metadata={
                "removed_count": removed_count,
                "usage_ratio": self._get_usage_ratio()
            }
        )
    
    def call_api(self, user_input):
        """调用 API"""
        try:
            # ... API 调用
            return result
        except Exception as e:
            # 出错时保存快照
            self.snapshot.save_snapshot(
                self.context,
                reason="api_error",
                metadata={
                    "error": str(e),
                    "user_input": user_input[:100]
                }
            )
            raise
```


## 性能监控

### 装饰器方式

```python
import time
from functools import wraps

def log_performance(logger):
    """性能监控装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start = time.time()
            try:
                result = func(self, *args, **kwargs)
                duration = time.time() - start
                
                logger.info(f"{func.__name__} 耗时: {duration*1000:.2f}ms")
                
                # 记录到事件日志
                if hasattr(self, 'event_logger'):
                    self.event_logger.log_event("performance", {
                        "function": func.__name__,
                        "duration_ms": duration * 1000,
                        "success": True
                    })
                
                return result
            except Exception as e:
                duration = time.time() - start
                logger.error(f"{func.__name__} 失败 (耗时 {duration*1000:.2f}ms): {e}")
                
                if hasattr(self, 'event_logger'):
                    self.event_logger.log_event("performance", {
                        "function": func.__name__,
                        "duration_ms": duration * 1000,
                        "success": False,
                        "error": str(e)
                    })
                
                raise
        return wrapper
    return decorator
```

### 使用示例

```python
class APIModelAgent:
    @log_performance(logger)
    def _smart_trim(self):
        """智能裁剪"""
        # ... 裁剪逻辑
    
    @log_performance(logger)
    def call_api(self, user_input):
        """调用 API"""
        # ... API 调用逻辑
```

## 日志分析工具

### 查询事件日志

```python
import json
from datetime import datetime

def query_events(log_file, event_type=None, start_time=None, end_time=None):
    """
    查询事件日志
    
    Args:
        log_file: 日志文件路径
        event_type: 事件类型过滤
        start_time: 开始时间（timestamp）
        end_time: 结束时间（timestamp）
    
    Returns:
        符合条件的事件列表
    """
    events = []
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)
            
            # 时间过滤
            if start_time and event["timestamp"] < start_time:
                continue
            if end_time and event["timestamp"] > end_time:
                continue
            
            # 类型过滤
            if event_type and event["event_type"] != event_type:
                continue
            
            events.append(event)
    
    return events

# 使用示例
api_calls = query_events("logs/events.jsonl", event_type="api_call")
print(f"总 API 调用次数: {len(api_calls)}")

total_tokens = sum(e["data"]["response"]["actual_tokens"] for e in api_calls)
print(f"总 token 消耗: {total_tokens}")

avg_duration = sum(e["data"]["duration_ms"] for e in api_calls) / len(api_calls)
print(f"平均响应时间: {avg_duration:.2f}ms")
```

### 统计分析

```python
def analyze_performance(log_file):
    """分析性能指标"""
    events = query_events(log_file, event_type="performance")
    
    # 按函数分组
    by_function = {}
    for event in events:
        func = event["data"]["function"]
        if func not in by_function:
            by_function[func] = []
        by_function[func].append(event["data"]["duration_ms"])
    
    # 统计
    print("性能统计:")
    for func, durations in by_function.items():
        avg = sum(durations) / len(durations)
        max_d = max(durations)
        min_d = min(durations)
        print(f"  {func}:")
        print(f"    调用次数: {len(durations)}")
        print(f"    平均耗时: {avg:.2f}ms")
        print(f"    最大耗时: {max_d:.2f}ms")
        print(f"    最小耗时: {min_d:.2f}ms")
```


## 最佳实践清单

### ✅ 必须做

1. **关键路径日志**
   - [ ] 函数入口和出口
   - [ ] API 调用前后
   - [ ] 状态变更（裁剪、配置更新）
   - [ ] 异常捕获

2. **日志级别正确**
   - [ ] DEBUG: 调试信息
   - [ ] INFO: 关键流程
   - [ ] WARNING: 异常但可恢复
   - [ ] ERROR: 错误但继续
   - [ ] CRITICAL: 致命错误

3. **结构化事件日志**
   - [ ] API 调用事件
   - [ ] 上下文裁剪事件
   - [ ] 错误事件
   - [ ] 性能指标事件

4. **上下文快照**
   - [ ] 裁剪前后
   - [ ] API 错误时
   - [ ] 异常状态时

### ⚠️ 应该做

1. **性能监控**
   - [ ] 关键函数添加性能装饰器
   - [ ] 记录耗时超过阈值的操作

2. **日志轮转**
   - [ ] 按日期或大小轮转日志文件
   - [ ] 定期清理旧日志

3. **敏感信息脱敏**
   - [ ] API 密钥不记录完整值
   - [ ] 用户输入截断或脱敏

### ❌ 不要做

1. **过度日志**
   - ❌ 循环中每次迭代都打 INFO 日志
   - ❌ 记录大量无用信息
   - ❌ 在生产环境开启 DEBUG

2. **性能杀手**
   - ❌ 同步写入大量日志
   - ❌ 在热路径打日志
   - ❌ 记录超大对象

3. **安全风险**
   - ❌ 记录完整的 API 密钥
   - ❌ 记录用户敏感信息
   - ❌ 日志文件权限过宽

## 日志文件组织

```
logs/
├── agent.log              # 主日志文件（文本格式）
├── events.jsonl           # 事件日志（JSON Lines）
├── snapshots/             # 上下文快照
│   ├── before_trim_20260321_143022.json
│   ├── after_trim_20260321_143023.json
│   └── api_error_20260321_143045.json
└── archive/               # 归档日志
    ├── agent.log.2026-03-20
    └── events.jsonl.2026-03-20
```

## 配置示例

### 开发环境

```python
# 控制台：DEBUG
# 文件：DEBUG
# 事件日志：开启
# 快照：开启

logger = setup_logger(
    'APIAgent',
    console_level=logging.DEBUG,
    file_level=logging.DEBUG
)
```

### 生产环境

```python
# 控制台：INFO
# 文件：INFO
# 事件日志：开启
# 快照：仅错误时

logger = setup_logger(
    'APIAgent',
    console_level=logging.INFO,
    file_level=logging.INFO
)
```

## 参考资料

- [Python logging 官方文档](https://docs.python.org/3/library/logging.html)
- [JSON Lines 格式](https://jsonlines.org/)
- [12-Factor App: Logs](https://12factor.net/logs)
- [Structured Logging Best Practices](https://www.structlog.org/)

## 相关文档

- [开发规范](./contributing.md)
- [Git 工作流](./git-workflow.md)
- [编码规范](../.kiro/instructions/coding-standards.md)

---

**版本**: 1.0  
**更新日期**: 2026-03-21  
**维护者**: 项目团队
