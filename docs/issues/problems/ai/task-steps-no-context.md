# 任务执行器步骤间无关联问题

> 创建时间: 2026-03-25
> 标签: task-mode, bug, design-issue

## 问题描述

在任务模式执行过程中，多个步骤之间没有关联性。每一步都是独立执行的，LLM 无法获取前序步骤的结果。

## 问题现象

用户输入：`帮我把最近几年GPT发展模型和时间列成一个表格给我。并做一定的分析。`

执行结果：
- 步骤1: 搜索"GPT模型发展时间线"获取关键信息 → LLM 回复"无法直接进行实时搜索"
- 步骤2: 整理模型名称、发布时间、参数量等数据 → LLM 回复"搜索GPT-1论文发布日期"
- 步骤3: 制作包含年份、模型名称、特点的表格 → LLM 回复"打开Excel或在线表格工具"

可以看到，每一步的回复都是独立的，步骤1的结果没有传递给步骤2。

## 原因分析

查看 `task_mode/task_executor.py` 第 108-111 行：

```python
if self.llm_call_func:
    print(f"🤖 使用 LLM 执行步骤")
    result = self.llm_call_func(step_desc)  # ← 只传了步骤描述，没传 context
    return result
```

### 代码现状

1. **context 变量存在**：每一步的结果会存储到 `task_state.context` 中
   ```python
   task_state.context[f"step_{step_index}"] = result
   ```

2. **context 未传递给 LLM**：但在调用 LLM 执行步骤时，只传递了 `step_desc`，没有传递 `context`

3. **工具调用有传递 context**：
   ```python
   result = tool_func(context)  # 工具函数会收到 context
   ```

### 影响

- LLM 不知道前一步做了什么
- 每一步都需要从头开始思考
- 无法基于上一步的结果进行下一步
- 任务的连贯性和准确性降低

## 解决方案

在调用 LLM 执行步骤时，将 `context`（前序步骤结果）一起传递：

```python
# 修改前
result = self.llm_call_func(step_desc)

# 修改后
context_info = "\n".join([f"步骤{i+1}: {v}" for i, v in task_state.context.items()])
prompt = f"前序步骤结果:\n{context_info}\n\n当前步骤: {step_desc}"
result = self.llm_call_func(prompt)
```

## 相关代码

- `task_mode/task_executor.py` - TaskExecutor._run_step() 方法
- `task_mode/task_state.py` - TaskState.context 属性
