#!/bin/bash
# 清理 Git 历史中的大文件（venv 和 PDF）

set -e

echo "⚠️  警告：此脚本将重写 Git 历史，移除大文件"
echo "📋 将移除以下内容："
echo "   - 所有 venv/ 目录"
echo "   - 所有 .pdf 文件"
echo ""
read -p "是否继续？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ 已取消"
    exit 1
fi

echo ""
echo "🧹 开始清理 Git 历史..."

# 使用 git filter-branch 移除大文件
git filter-branch --force --index-filter \
  'git rm -rf --cached --ignore-unmatch \
    L1-Agent/src/AgentPractice/第七章/venv \
    L1-Agent/src/AgentPractice/venv \
    L2-Business/落地案例分析/pdf/*.pdf \
    "*.pdf" \
    "**/venv/**" \
    "**/__pycache__/**" \
    "**/.DS_Store"' \
  --prune-empty --tag-name-filter cat -- --all

echo ""
echo "✅ 清理完成！"
echo ""
echo "📝 下一步操作："
echo "   1. 检查清理结果: git log --oneline"
echo "   2. 强制推送（需要权限）: git push origin --force --all"
echo "   3. 清理本地引用: git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin"
echo "   4. 清理和压缩: git reflog expire --expire=now --all && git gc --prune=now --aggressive"
echo ""
echo "⚠️  注意：强制推送会覆盖远程仓库历史，请确保团队成员已备份！"

