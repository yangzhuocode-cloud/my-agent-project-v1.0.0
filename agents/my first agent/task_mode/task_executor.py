#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务执行器 - 分步执行任务，支持重试和状态回检
"""

import time
from .task_state import TaskState, TaskStatus


DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1


class TaskExecutor:
    def __init__(self, max_retries=DEFAULT_MAX_RETRIES, retry_delay=DEFAULT_RETRY_DELAY):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.tool_map = {}
        self.llm_call_func = None

    def set_tool_map(self, tool_map):
        """设置工具映射表"""
        self.tool_map = tool_map

    def set_llm_call(self, llm_call_func):
        """设置 LLM 调用函数"""
        self.llm_call_func = llm_call_func

    def execute_task(self, steps, user_input):
        """
        执行完整任务
        
        Args:
            steps: 步骤列表
            user_input: 用户原始需求
            
        Returns:
            TaskState: 任务执行状态
        """
        task_state = TaskState(user_input)
        task_state.set_steps(steps)
        
        print(f"\n{'='*60}")
        print(f"开始执行任务模式")
        print(f"{'='*60}")
        
        for step_index, step_desc in enumerate(steps):
            result = self._execute_single_step(step_index, step_desc, task_state)
            
            if task_state.status == TaskStatus.FAILED:
                print(f"\n❌ 任务终止于第 {step_index + 1} 步")
                break
            
            print(f"\n✅ 第 {step_index + 1}/{len(steps)} 步完成")
        
        if task_state.status != TaskStatus.FAILED:
            task_state.complete_task()
            print(f"\n🎉 任务全部完成！")
        
        return task_state

    def _execute_single_step(self, step_index, step_desc, task_state):
        """
        执行单个步骤
        
        Args:
            step_index: 步骤索引
            step_desc: 步骤描述
            task_state: 任务状态对象
            
        Returns:
            str: 步骤执行结果
        """
        task_state.start_step(step_index)
        
        print(f"\n🔹 执行第 {step_index + 1}/{len(task_state.steps)} 步: {step_desc}")
        
        retry_count = 0
        last_error = None
        
        while retry_count < self.max_retries:
            try:
                result = self._run_step(step_desc, task_state.context)
                task_state.complete_step(step_index, result)
                return result
                
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                print(f"❌ 第 {retry_count} 次尝试失败: {e}")
                
                if retry_count < self.max_retries:
                    print(f"⏳ {self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
        
        task_state.fail_step(step_index, last_error)
        return None

    def _run_step(self, step_desc, context):
        """
        运行单个步骤
        
        根据步骤描述自动匹配并调用工具
        
        Args:
            step_desc: 步骤描述
            context: 上下文数据（包含前序步骤结果）
            
        Returns:
            str: 执行结果
        """
        matched_tool = self._match_tool(step_desc)
        
        if matched_tool:
            tool_name, tool_func = matched_tool
            print(f"🔧 调用工具: {tool_name}")
            
            try:
                result = tool_func(context)
                return str(result) if result is not None else "执行完成"
            except Exception as e:
                raise Exception(f"工具 {tool_name} 执行失败: {e}")
        
        if self.llm_call_func:
            print(f"🤖 使用 LLM 执行步骤")
            result = self.llm_call_func(step_desc)
            return result
        
        return f"步骤已完成: {step_desc}"

    def _match_tool(self, step_desc):
        """
        根据步骤描述匹配工具
        
        Args:
            step_desc: 步骤描述
            
        Returns:
            tuple: (工具名, 工具函数) 或 None
        """
        tool_keywords = {
            "数据": "get_data",
            "查询": "query",
            "获取": "fetch",
            "分析": "analyze",
            "生成": "generate",
            "制作": "create",
            "PPT": "create_ppt",
            "表格": "create_table",
            "报告": "create_report",
            "保存": "save",
            "写入": "write",
            "读取": "read",
            "删除": "delete",
            "清洗": "clean",
            "处理": "process",
            "计算": "calculate",
            "统计": "statistics",
            "导出": "export",
            "转换": "convert",
            "验证": "validate",
            "校验": "validate",
        }
        
        matched_tools = []
        for keyword, tool_name in tool_keywords.items():
            if keyword in step_desc and tool_name in self.tool_map:
                matched_tools.append((tool_name, self.tool_map[tool_name]))
        
        if matched_tools:
            return matched_tools[0]
        
        return None


def execute_task_with_tools(steps, user_input, tool_map, llm_call_func):
    """
    便捷函数：使用工具执行任务
    
    Args:
        steps: 步骤列表
        user_input: 用户原始需求
        tool_map: 工具映射表 {工具名: 函数}
        llm_call_func: LLM 调用函数
        
    Returns:
        TaskState: 任务执行状态
    """
    executor = TaskExecutor()
    executor.set_tool_map(tool_map)
    executor.set_llm_call(llm_call_func)
    
    return executor.execute_task(steps, user_input)
