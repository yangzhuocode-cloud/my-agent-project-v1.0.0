#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务规划器 - 将用户需求拆解为可执行的步骤
"""

PLANNER_PROMPT_TEMPLATE = """你是任务规划助手。请把用户需求拆成【可执行、有序、带工具】的步骤。

要求：
1. 每个步骤必须是可执行的具体动作
2. 步骤按逻辑顺序排列
3. 每个步骤描述控制在 20 字以内
4. 只输出步骤列表，不要其他内容
5. 如果无法拆解，直接返回原需求

用户需求：{user_input}

请按以下格式输出：
1. [步骤1描述]
2. [步骤2描述]
3. [步骤3描述]
..."""


def plan_task(user_input, llm_call_func):
    """
    将用户需求拆解为步骤
    
    Args:
        user_input: 用户需求
        llm_call_func: LLM 调用函数，接受 prompt 返回响应
        
    Returns:
        list: 步骤列表，每项为字符串
    """
    prompt = PLANNER_PROMPT_TEMPLATE.format(user_input=user_input)
    
    try:
        result = llm_call_func(prompt)
        steps = _parse_steps(result)
        
        if not steps:
            return [user_input]
        
        return steps
        
    except Exception as e:
        print(f"⚠️ 任务规划失败: {e}")
        return [user_input]


def _parse_steps(llm_output):
    """
    解析 LLM 输出的步骤列表
    
    Args:
        llm_output: LLM 返回的原始文本
        
    Returns:
        list: 步骤列表
    """
    steps = []
    lines = llm_output.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line[0].isdigit() and "." in line[:5]:
            step = line.split(".", 1)[1].strip()
            if step:
                steps.append(step)
        elif line.startswith("-") or line.startswith("•"):
            step = line[1:].strip()
            if step:
                steps.append(step)
    
    return steps


def format_steps_for_display(steps):
    """
    格式化步骤为可读形式
    
    Args:
        steps: 步骤列表
        
    Returns:
        str: 格式化后的步骤字符串
    """
    if not steps:
        return "无步骤"
    
    lines = []
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    
    return "\n".join(lines)
