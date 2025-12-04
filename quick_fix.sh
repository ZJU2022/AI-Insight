#!/bin/bash
# 快速修复：创建干净的提交，移除大文件

set -e

echo "🔧 快速修复 Git Push 问题"
echo ""
echo "此脚本将："
echo "  1. 创建一个新的干净提交"
echo "  2. 移除所有 venv 和 PDF 文件"
echo "  3. 保留所有代码和文档"
echo ""

# 检查当前状态
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"
echo ""

# 备份当前分支
BACKUP_BRANCH="backup-$(date +%Y%m%d-%H%M%S)"
echo "📦 创建备份分支: $BACKUP_BRANCH"
git branch "$BACKUP_BRANCH"

# 移除已跟踪的大文件
echo ""
echo "🧹 从 Git 中移除大文件（保留本地文件）..."
git rm -r --cached "L1-Agent/src/AgentPractice/第七章/venv" 2>/dev/null || true
git rm -r --cached "L1-Agent/src/AgentPractice/venv" 2>/dev/null || true
git rm --cached "L2-Business/落地案例分析/pdf/"*.pdf 2>/dev/null || true
git rm -r --cached "**/__pycache__" 2>/dev/null || true

# 添加 .gitignore（如果还没有）
if [ -f .gitignore ]; then
    git add .gitignore
fi

# 添加所有其他文件（.gitignore 会排除大文件）
echo ""
echo "📝 添加文件到暂存区..."
git add -A

# 检查暂存区大小
STAGED_SIZE=$(git diff --cached --numstat | awk '{sum+=$1+$2} END {print sum/1024/1024}')
echo "暂存区大小: ${STAGED_SIZE} MB"

# 提交
echo ""
echo "💾 创建提交..."
git commit -m "Remove large files (venv, PDFs) and add .gitignore" || {
    echo "⚠️  没有更改需要提交，可能文件已经被移除"
}

echo ""
echo "✅ 完成！"
echo ""
echo "📋 下一步："
echo "   由于历史中仍有大文件，你需要："
echo ""
echo "   选项 1：使用 git filter-repo 清理历史（推荐）"
echo "   brew install git-filter-repo"
echo "   git filter-repo --path-glob '*.pdf' --invert-paths"
echo "   git filter-repo --path 'L1-Agent/src/AgentPractice/第七章/venv' --invert-paths"
echo "   git push origin --force main"
echo ""
echo "   选项 2：创建新的干净仓库"
echo "   查看 fix_push_issue.md 了解详细步骤"
echo ""
echo "   备份分支: $BACKUP_BRANCH"

