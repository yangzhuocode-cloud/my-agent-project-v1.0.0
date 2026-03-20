#!/bin/bash
# 自动设置 Git Worktree 开发环境
# 使用场景：克隆项目后，快速设置 worktree 结构

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 设置 Git Worktree 开发环境${NC}"
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}错误：当前目录不是 Git 仓库${NC}"
    exit 1
fi

# 检查是否在 master 分支
current_branch=$(git branch --show-current)
if [ "$current_branch" != "master" ]; then
    echo -e "${YELLOW}警告：当前不在 master 分支（当前：$current_branch）${NC}"
    echo "建议切换到 master 分支后再运行此脚本"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 获取所有远程 feature 分支
echo -e "${BLUE}📡 获取远程分支信息...${NC}"
git fetch --all

remote_branches=$(git branch -r | grep "origin/feature/" | sed 's/origin\///' | sed 's/^[[:space:]]*//')

if [ -z "$remote_branches" ]; then
    echo -e "${YELLOW}未找到任何 feature 分支，无需设置 worktree${NC}"
    exit 0
fi

echo -e "${GREEN}找到以下 feature 分支：${NC}"
echo "$remote_branches" | while read branch; do
    echo "  - $branch"
done
echo ""

# 为每个 feature 分支创建 worktree
echo -e "${BLUE}📂 创建 worktree...${NC}"
echo ""

success_count=0
skip_count=0

echo "$remote_branches" | while read branch; do
    # 提取分支名（去掉 feature/ 前缀）
    branch_name=$(echo "$branch" | sed 's/feature\///')
    worktree_path="worktrees/$branch_name"
    
    # 检查 worktree 是否已存在
    if [ -d "$worktree_path" ]; then
        echo -e "${YELLOW}⏭️  跳过：$worktree_path 已存在${NC}"
        skip_count=$((skip_count + 1))
    else
        echo -e "${GREEN}➕ 创建：$worktree_path ($branch)${NC}"
        git worktree add "$worktree_path" "$branch"
        success_count=$((success_count + 1))
    fi
    echo ""
done

# 输出总结
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Worktree 设置完成${NC}"
echo ""
echo -e "${BLUE}📁 当前 worktree 结构：${NC}"
git worktree list
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}💡 使用提示：${NC}"
echo "  - 框架开发：在主目录工作（master 分支）"
echo "  - Agent 开发：在 worktrees/<agent-name>/ 工作"
echo "  - 同步更新：运行 ./scripts/sync-master-to-worktrees.sh"
echo ""

exit 0
