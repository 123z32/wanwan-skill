#!/bin/bash
# 每日备份脚本 - 自动总结 + Git 备份 + 晚安

set -e

WORKSPACE="/openclaw_data/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)
BACKUP_TAG="backup-$DATE"

cd "$WORKSPACE"

echo "📅 开始每日备份：$DATE"
echo ""

# 1. 检查 git 状态
echo "📊 检查 Git 状态..."
git status --short

# 2. 添加所有更改
echo ""
echo "📝 添加更改..."
git add -A

# 3. 提交
echo ""
echo "💾 提交更改..."
git commit -m "📝 Daily summary: $DATE" || echo "⚠️  没有更改需要提交"

# 4. 创建备份标签
echo ""
echo "🏷️  创建备份标签..."
git tag -a "$BACKUP_TAG" -m "Daily backup: $DATE" || echo "⚠️  标签已存在"

# 5. 清理旧标签（保留最近 3 个）
echo ""
echo "🧹 清理旧标签..."
TAG_COUNT=$(git tag -l | grep "^backup-" | wc -l)
if [ "$TAG_COUNT" -gt 3 ]; then
    git tag -l | grep "^backup-" | sort | head -n -3 | xargs git tag -d
    echo "✅ 已清理旧标签，保留最近 3 个"
else
    echo "✅ 标签数量：$TAG_COUNT (无需清理)"
fi

# 6. 推送到 GitHub
echo ""
echo "📤 推送到 GitHub..."
git push origin main --tags || echo "⚠️  推送失败（可能是网络问题）"

# 7. 显示提交历史
echo ""
echo "📜 最近提交:"
git log --oneline -5

echo ""
echo "✅ 备份完成！"
echo ""
echo "📊 备份信息"
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo "日期：$DATE"
echo "标签：$BACKUP_TAG"
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo ""
