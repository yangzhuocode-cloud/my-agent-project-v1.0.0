#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务状态管理 - 管理任务的执行状态和上下文
"""

import time
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskState:
    def __init__(self, user_input):
        self.user_input = user_input
        self.steps = []
        self.step_results = {}
        self.step_status = {}
        self.current_step_index = 0
        self.status = TaskStatus.PENDING
        self.start_time = time.time()
        self.end_time = None
        self.error_message = None
        self.context = {}

    def set_steps(self, steps):
        """设置任务步骤"""
        self.steps = steps
        self.step_status = {i: TaskStatus.PENDING for i in range(len(steps))}

    def get_current_step(self):
        """获取当前步骤"""
        if self.current_step_index < len(self.steps):
            return self.current_step_index, self.steps[self.current_step_index]
        return None, None

    def start_step(self, step_index):
        """开始执行某步骤"""
        self.step_status[step_index] = TaskStatus.EXECUTING
        self.status = TaskStatus.EXECUTING

    def complete_step(self, step_index, result):
        """完成某步骤"""
        self.step_results[step_index] = result
        self.step_status[step_index] = TaskStatus.COMPLETED
        self.context[f"step_{step_index}"] = result
        self.current_step_index = step_index + 1

    def fail_step(self, step_index, error):
        """步骤执行失败"""
        self.step_status[step_index] = TaskStatus.FAILED
        self.error_message = error
        self.status = TaskStatus.FAILED

    def complete_task(self):
        """完成任务"""
        self.status = TaskStatus.COMPLETED
        self.end_time = time.time()

    def fail_task(self, error):
        """任务失败"""
        self.status = TaskStatus.FAILED
        self.error_message = error
        self.end_time = time.time()

    def cancel_task(self):
        """取消任务"""
        self.status = TaskStatus.CANCELLED
        self.end_time = time.time()

    def get_progress(self):
        """获取任务进度"""
        total = len(self.steps)
        completed = sum(1 for s in self.step_status.values() if s == TaskStatus.COMPLETED)
        return completed, total

    def get_duration(self):
        """获取任务耗时"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def get_summary(self):
        """获取任务摘要"""
        completed, total = self.get_progress()
        duration = self.get_duration()
        
        summary = {
            "user_input": self.user_input,
            "status": self.status.value,
            "progress": f"{completed}/{total}",
            "duration": f"{duration:.1f}s",
            "steps": []
        }
        
        for i, step in enumerate(self.steps):
            step_info = {
                "index": i + 1,
                "description": step,
                "status": self.step_status[i].value,
                "result": self.step_results.get(i, "")[:100] if i in self.step_results else ""
            }
            summary["steps"].append(step_info)
        
        if self.error_message:
            summary["error"] = self.error_message
        
        return summary

    def format_for_display(self):
        """格式化显示任务状态"""
        completed, total = self.get_progress()
        duration = self.get_duration()
        
        lines = []
        lines.append(f"📋 任务状态: {self.status.value}")
        lines.append(f"📊 进度: {completed}/{total} 步骤")
        lines.append(f"⏱️ 耗时: {duration:.1f}秒")
        lines.append("")
        lines.append("步骤详情:")
        
        for i, step in enumerate(self.steps):
            status_icon = self._get_status_icon(self.step_status[i])
            result_preview = ""
            if i in self.step_results:
                result = self.step_results[i]
                if len(result) > 30:
                    result_preview = f" → {result[:30]}..."
                else:
                    result_preview = f" → {result}"
            lines.append(f"  {status_icon} {i+1}. {step}{result_preview}")
        
        if self.error_message:
            lines.append(f"\n❌ 错误: {self.error_message}")
        
        return "\n".join(lines)

    @staticmethod
    def _get_status_icon(status):
        """获取状态图标"""
        icons = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.PLANNING: "🔄",
            TaskStatus.EXECUTING: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.CANCELLED: "🚫"
        }
        return icons.get(status, "❓")
