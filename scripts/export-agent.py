#!/usr/bin/env python3
"""
Agent 导出脚本

用法:
    python scripts/export-agent.py "my first agent"
    python scripts/export-agent.py "my first agent" --output ./exports

功能:
    1. 复制 agent 文件到导出目录
    2. 解析 prompts 中的 #[[prompt:xxx]] 引用
    3. 自动从项目根目录复制被引用的 prompt 文件
    4. 读取 prompt 元数据，只复制 scope 为 shared 或 selective 的文件
"""

import os
import sys
import json
import shutil
import argparse
import re
from pathlib import Path
from fnmatch import fnmatch


def load_export_config(agent_path: Path) -> dict:
    """加载 agent 的导出配置"""
    config_path = agent_path / ".export.json"
    if not config_path.exists():
        return {
            "exclude_patterns": [".export.json", "__pycache__", "*.pyc"]
        }
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_prompt_metadata(prompt_path: Path) -> dict:
    """解析 prompt 文件的 YAML front matter 元数据"""
    if not prompt_path.exists():
        return {}
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 YAML front matter (--- ... ---)
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    
    yaml_content = match.group(1)
    metadata = {}
    
    # 简单解析 YAML（只处理 key: value 格式）
    for line in yaml_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # 处理数组格式 ["item1", "item2"]
            if value.startswith('[') and value.endswith(']'):
                value = [item.strip(' "\'') for item in value[1:-1].split(',')]
            # 处理字符串（去除引号）
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            metadata[key] = value
    
    return metadata


def extract_prompt_references(file_path: Path) -> list:
    """从文件中提取所有 #[[prompt:xxx]] 引用"""
    if not file_path.exists():
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 #[[prompt:xxx]]
    pattern = r'#\[\[prompt:([^\]]+)\]\]'
    matches = re.findall(pattern, content)
    
    return matches


def should_exclude(file_path: Path, exclude_patterns: list) -> bool:
    """检查文件是否应该被排除"""
    file_name = file_path.name
    for pattern in exclude_patterns:
        if fnmatch(file_name, pattern):
            return True
    return False


def copy_agent_files(agent_path: Path, export_path: Path, exclude_patterns: list):
    """复制 agent 文件到导出目录（排除指定文件）"""
    for item in agent_path.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(agent_path)
            
            # 检查是否应该排除
            if should_exclude(item, exclude_patterns):
                continue
            
            # 检查父目录是否应该排除
            skip = False
            for part in relative_path.parts:
                if should_exclude(Path(part), exclude_patterns):
                    skip = True
                    break
            if skip:
                continue
            
            # 复制文件
            dest_file = export_path / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_file)
            print(f"  ✓ {relative_path}")


def collect_prompt_references(agent_path: Path) -> set:
    """收集 agent 中所有 prompt 文件引用的 prompt_id"""
    prompt_refs = set()
    prompts_dir = agent_path / "prompts"
    
    if not prompts_dir.exists():
        return prompt_refs
    
    # 遍历所有 .md 文件
    for prompt_file in prompts_dir.glob("*.md"):
        refs = extract_prompt_references(prompt_file)
        prompt_refs.update(refs)
        if refs:
            print(f"  📎 {prompt_file.name} 引用: {', '.join(refs)}")
    
    return prompt_refs


def copy_referenced_prompts(prompt_refs: set, export_path: Path, project_root: Path):
    """从项目根目录复制被引用的 prompt 文件到导出目录"""
    if not prompt_refs:
        return
    
    prompts_dir = project_root / "prompts"
    export_prompts_dir = export_path / "prompts"
    export_prompts_dir.mkdir(parents=True, exist_ok=True)
    
    for prompt_id in prompt_refs:
        # 支持带扩展名或不带扩展名
        if not prompt_id.endswith('.md'):
            prompt_id = f"{prompt_id}.md"
        
        source_file = prompts_dir / prompt_id
        if not source_file.exists():
            print(f"  ⚠ 警告: 引用的 prompt 文件不存在: {source_file}")
            continue
        
        # 读取元数据，检查 scope
        metadata = parse_prompt_metadata(source_file)
        scope = metadata.get('scope', 'unknown')
        
        # 只复制 shared 或 selective 的 prompt
        if scope not in ['shared', 'selective']:
            print(f"  ⊘ 跳过 {prompt_id} (scope: {scope}，非共享)")
            continue
        
        dest_file = export_prompts_dir / prompt_id
        shutil.copy2(source_file, dest_file)
        print(f"  ✓ 复制引用的 prompt: {prompt_id} (scope: {scope})")


def export_agent(agent_name: str, output_dir: Path, project_root: Path):
    """导出指定的 agent"""
    agent_path = project_root / "agents" / agent_name
    
    if not agent_path.exists():
        print(f"❌ 错误: Agent 不存在: {agent_path}")
        sys.exit(1)
    
    # 加载导出配置
    export_config = load_export_config(agent_path)
    
    # 创建导出目录
    export_name = agent_name.replace(" ", "-").lower()
    export_path = output_dir / export_name
    
    if export_path.exists():
        print(f"🗑️  清理旧的导出目录: {export_path}")
        shutil.rmtree(export_path)
    
    export_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📦 开始导出 Agent: {agent_name}")
    print(f"📂 导出到: {export_path}\n")
    
    # 1. 复制 agent 文件（排除配置的文件）
    print("📋 复制 Agent 文件:")
    copy_agent_files(agent_path, export_path, export_config["exclude_patterns"])
    
    # 2. 收集 prompts 中的引用
    print("\n🔍 分析 Prompt 引用:")
    prompt_refs = collect_prompt_references(agent_path)
    
    # 3. 复制被引用的 prompt 文件
    if prompt_refs:
        print(f"\n📄 复制被引用的 Prompt 文件:")
        copy_referenced_prompts(prompt_refs, export_path, project_root)
    else:
        print("\n📄 没有发现 prompt 引用")
    
    print(f"\n✅ 导出完成: {export_path}")


def main():
    parser = argparse.ArgumentParser(description="导出 Agent 为独立包")
    parser.add_argument("agent_name", help="要导出的 Agent 名称")
    parser.add_argument(
        "--output", 
        default="./exports",
        help="导出目录 (默认: ./exports)"
    )
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 导出目录
    output_dir = Path(args.output).resolve()
    
    export_agent(args.agent_name, output_dir, project_root)


if __name__ == "__main__":
    main()
