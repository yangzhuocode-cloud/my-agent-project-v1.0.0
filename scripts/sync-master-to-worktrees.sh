#!/bin/bash
# 自动将 master 分支的更新合并到所有 worktree 分支
# 使用场景：在 master 分支提交框架更新后，自动同步到所有 agent 开发分支

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 开始同步 master 分支到所有 worktree...${NC}"
echo ""

# 检查当前是否在 master 分支
current_branch=$(git branch --show-current)
if [ "$current_branch" != "master" ]; then
    echo -e "${YELLOW}⚠️  警告：当前不在 master 分支（当前：$current_branch）${NC}"
    echo "建议在 master 分支执行此脚本"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 获取所有 worktree（排除主目录）
worktrees=$(git worktree list --porcelain | grep "^worktree" | awk '{print $2}' | tail -n +2)

if [ -z "$worktrees" ]; then
    echo -e "${YELLOW}⚠️  未找到任何 worktree，无需同步${NC}"
    exit 0
fi

# 记录成功和失败的 worktree
success_count=0
fail_count=0
failed_worktrees=()

# 遍历每个 worktree 并合并 master
while IFS= read -r worktree_path; do
    # 获取 worktree 的分支名
    branch=$(git -C "$worktree_path" branch --show-current)
    worktree_name=$(basename "$worktree_path")
    
    echo -e "${GREEN}📂 处理 worktree: ${worktree_name} (${branch})${NC}"
    
    # 检查是否有未提交的更改
    if ! git -C "$worktree_path" diff-index --quiet HEAD --; then
        echo -e "${YELLOW}   ⚠️  有未提交的更改，跳过合并${NC}"
        echo -e "${YELLOW}   提示：请先在该 worktree 中提交或 stash 更改${NC}"
        fail_count=$((fail_count + 1))
        failed_worktrees+=("$worktree_name (未提交的更改)")
        echo ""
        continue
    fi
    
    # 尝试合并 master
    if git -C "$worktree_path" merge master --no-edit; then
        echo -e "${GREEN}   ✅ 合并成功${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${RED}   ❌ 合并失败（可能有冲突）${NC}"
        echo -e "${YELLOW}   提示：请手动解决冲突${NC}"
        # 中止合并
        git -C "$worktree_path" merge --abort 2>/dev/null || true
        fail_count=$((fail_count + 1))
        failed_worktrees+=("$worktree_name (合并冲突)")
    fi
    echo ""
done <<< "$worktrees"

# 输出总结
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 同步完成${NC}"
echo -e "   成功: ${GREEN}${success_count}${NC}"
echo -e "   失败: ${RED}${fail_count}${NC}"

if [ $fail_count -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}失败的 worktree:${NC}"
    for failed in "${failed_worktrees[@]}"; do
        echo -e "   - $failed"
    done
fi

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

exit 0
