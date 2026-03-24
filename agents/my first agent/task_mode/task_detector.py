#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务检测器 - 判断用户输入是否为复杂任务
"""

TASK_KEYWORDS = [
    "分析", "生成", "制作", "总结", "查询", "导出", "统计", "报告", "PPT", "表格",
    "处理", "转换", "整理", "提取", "对比", "评估", "优化", "构建", "实现", "开发",
    "批量", "自动", "执行", "完成", "创建", "修改", "删除", "重命名", "移动"
]

MIN_TASK_LENGTH = 10


def is_complex_task(text):
    """
    判断用户输入是否为复杂任务
    
    判断依据：
    1. 包含任务关键词
    2. 输入长度超过阈值
    
    Args:
        text: 用户输入文本
        
    Returns:
        bool: True 表示复杂任务，False 表示简单对话
    """
    if not text or not text.strip():
        return False
    
    has_keyword = any(kw in text for kw in TASK_KEYWORDS)
    is_long = len(text.strip()) > MIN_TASK_LENGTH
    
    return has_keyword or is_long


def get_detection_reason(text):
    """
    获取检测原因（用于调试）
    
    Args:
        text: 用户输入文本
        
    Returns:
        str: 检测原因描述
    """
    reasons = []
    
    if not text or not text.strip():
        return "输入为空"
    
    matched_keywords = [kw for kw in TASK_KEYWORDS if kw in text]
    if matched_keywords:
        reasons.append(f"包含关键词: {', '.join(matched_keywords[:3])}")
    
    if len(text.strip()) > MIN_TASK_LENGTH:
        reasons.append(f"输入长度({len(text.strip())})超过阈值({MIN_TASK_LENGTH})")
    
    if reasons:
        return "; ".join(reasons)
    else:
        return "简单对话"
