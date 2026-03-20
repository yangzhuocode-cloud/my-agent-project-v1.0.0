# 日志规范指令

## 核心原则

在编写和测试代码时，必须遵循渐进式日志策略，确保代码的可观测性和可调试性。

## 开发阶段日志要求

### 阶段 1: 初始开发

**必须添加的日志**：

1. **函数入口和出口**
   ```python
   def function_name(self, param):
       self.logger.info(f"开始执行 {function_name}: param={param}")
       # ... 逻辑
       self.logger.info(f"完成执行 {function_name}")
   ```

2. **外部调用**（API、数据库、文件）
   ```python
   self.logger.info(f"调用 API: {url}")
   response = requests.post(url, json=payload)
   self.logger.info(f"API 响应: {response.status_code}")
   ```

3. **状态变更**
   ```python
   self.logger.info(f"触发裁剪: {before_count} → {after_count} 条消息")
   ```

4. **异常捕获**
   ```python
   except Exception as e:
       self.logger.error(f"操作失败: {str(e)}", exc_info=True)
   ```

5. **关键决策点**
   ```python
   if usage_ratio >= threshold:
       self.logger.warning(f"使用率 {usage_ratio:.1%} 达到阈值")
   ```

### 阶段 2: 问题调试

**临时增加的日志**：

1. **详细变量值**
   ```python
   self.logger.debug(f"变量状态: x={x}, y={y}, z={z}")
   ```

2. **循环迭代**
   ```python
   for i, item in enumerate(items):
       self.logger.debug(f"处理第 {i} 项: {item}")
   ```

3. **条件判断**
   ```python
   self.logger.debug(f"条件检查: condition={condition}, result={result}")
   ```

**调试完成后**：移除或降级为 DEBUG 级别

### 阶段 3: 生产稳定

**保留的日志**：

1. INFO 级别的关键流程
2. WARNING/ERROR 级别的异常
3. 结构化事件日志
4. 性能指标

**移除的日志**：

1. 详细的 DEBUG 日志
2. 循环中的迭代日志
3. 临时调试日志


## 日志级别使用规则

### DEBUG
- **何时使用**: 开发和调试阶段
- **内容**: 变量值、中间状态、详细流程
- **示例**: `logger.debug(f"消息详情: {msg}")`

### INFO
- **何时使用**: 生产环境默认级别
- **内容**: 关键流程节点、重要操作
- **示例**: `logger.info(f"API 调用成功: {tokens} tokens")`

### WARNING
- **何时使用**: 异常但可恢复
- **内容**: 接近阈值、重复错误、降级处理
- **示例**: `logger.warning(f"Token 使用率 {ratio:.1%} 接近阈值")`

### ERROR
- **何时使用**: 错误但程序继续
- **内容**: API 失败、解析错误、异常捕获
- **示例**: `logger.error(f"API 失败: {e}", exc_info=True)`

### CRITICAL
- **何时使用**: 致命错误，程序无法继续
- **内容**: 初始化失败、配置错误
- **示例**: `logger.critical(f"配置加载失败: {path}")`

## 结构化事件日志

### 必须记录的事件

1. **API 调用**
   ```python
   self.event_logger.log_event("api_call", {
       "request": {"messages_count": count, "estimated_tokens": tokens},
       "response": {"status_code": code, "actual_tokens": tokens},
       "duration_ms": duration
   })
   ```

2. **上下文裁剪**
   ```python
   self.event_logger.log_event("context_trim", {
       "before": {"count": before_count, "tokens": before_tokens},
       "after": {"count": after_count, "tokens": after_tokens},
       "removed_count": removed
   })
   ```

3. **错误事件**
   ```python
   self.event_logger.log_event("error", {
       "error_type": type(e).__name__,
       "error_message": str(e),
       "context": {"function": func_name, "state": state}
   })
   ```

4. **性能指标**
   ```python
   self.event_logger.log_event("performance", {
       "operation": operation_name,
       "duration_ms": duration,
       "success": success
   })
   ```

## 上下文快照

### 必须保存快照的时机

1. **裁剪前后**
   ```python
   self.snapshot.save_snapshot(self.context, "before_trim")
   # ... 裁剪
   self.snapshot.save_snapshot(self.context, "after_trim")
   ```

2. **API 错误**
   ```python
   except Exception as e:
       self.snapshot.save_snapshot(self.context, "api_error", 
                                   metadata={"error": str(e)})
   ```

3. **异常状态**
   ```python
   if self._detect_anomaly():
       self.snapshot.save_snapshot(self.context, "anomaly")
   ```

## 性能监控

### 关键函数必须添加性能监控

```python
@log_performance(logger)
def critical_function(self):
    """关键函数"""
    # ... 逻辑
```

**必须监控的函数**：
- API 调用
- 上下文裁剪
- 消息构建
- Token 估算

## 代码审查检查项

在提交代码前，确保：

- [ ] 关键路径有 INFO 日志
- [ ] 外部调用有日志记录
- [ ] 异常有 ERROR 日志和 exc_info=True
- [ ] 状态变更有日志
- [ ] 没有过度的 DEBUG 日志（生产环境）
- [ ] 敏感信息已脱敏
- [ ] 结构化事件日志已添加
- [ ] 关键函数有性能监控

## 测试时的日志要求

### 单元测试
```python
def test_function():
    # 临时提升日志级别
    logger.setLevel(logging.DEBUG)
    
    # ... 测试逻辑
    
    # 验证日志
    assert "预期的日志消息" in caplog.text
```

### 集成测试
```python
def test_integration():
    # 检查事件日志
    events = query_events("logs/events.jsonl", event_type="api_call")
    assert len(events) > 0
    
    # 检查快照
    snapshots = list(Path("logs/snapshots").glob("*.json"))
    assert len(snapshots) > 0
```

## 常见错误

### ❌ 错误示例

```python
# 1. 循环中打 INFO 日志
for item in items:
    logger.info(f"处理 {item}")  # ❌ 应该用 DEBUG

# 2. 记录敏感信息
logger.info(f"API Key: {api_key}")  # ❌ 不应记录完整密钥

# 3. 没有异常信息
except Exception as e:
    logger.error("失败")  # ❌ 缺少 exc_info=True

# 4. 过度详细
logger.info(f"变量: {huge_object}")  # ❌ 对象太大
```

### ✅ 正确示例

```python
# 1. 循环用 DEBUG 或汇总
logger.debug(f"处理 {len(items)} 个项目")
for item in items:
    logger.debug(f"处理 {item}")

# 2. 脱敏敏感信息
logger.info(f"API Key: {api_key[:8]}***")

# 3. 包含异常信息
except Exception as e:
    logger.error(f"失败: {str(e)}", exc_info=True)

# 4. 适度详细
logger.info(f"对象: type={type(obj)}, size={len(obj)}")
```

## 快速参考

```python
# 初始化日志
from utils.logging import setup_logger, EventLogger, ContextSnapshot

self.logger = setup_logger('AgentName')
self.event_logger = EventLogger()
self.snapshot = ContextSnapshot()

# 基础日志
self.logger.info("关键操作")
self.logger.debug("调试信息")
self.logger.warning("警告")
self.logger.error("错误", exc_info=True)

# 事件日志
self.event_logger.log_event("event_type", {"key": "value"})

# 快照
self.snapshot.save_snapshot(self.context, "reason")

# 性能监控
@log_performance(self.logger)
def function(self):
    pass
```

## 相关文档

- 详细规范: [docs/development/logging-standards.md](../../docs/development/logging-standards.md)
- 编码规范: [coding-standards.md](./coding-standards.md)
- 工作流程: [workflow.md](./workflow.md)
