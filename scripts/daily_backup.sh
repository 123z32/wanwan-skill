#!/bin/bash
# 每日备份脚本 - 绾绾的自我备份
# 用法：./daily_backup.sh
# 功能：备份当前状态到 Git，保留最近 3 天的备份

set -e

BACKUP_DIR="/openclaw_data/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H-%M-%S)
BACKUP_BRANCH="backup-${DATE}"
MAX_BACKUPS=3

echo "🤖 绾绾每日备份"
echo "=============="
echo "日期：${DATE}"
echo "时间：${TIME}"
echo ""

cd "$BACKUP_DIR"

# 1. 更新 SELF_SUMMARY.md 的时间戳
echo "📝 更新技能总结..."
sed -i "s/\*\*最后更新\*\*: .*/\*\*最后更新\*\*: $(date +%Y-%m-%d)/" SELF_SUMMARY.md

# 2. 添加所有更改
echo "📦 添加文件到 Git..."
git add -A

# 3. 检查是否有更改
if git diff --staged --quiet; then
    echo "⚠️  没有更改，跳过备份"
    exit 0
fi

# 4. 创建提交
echo "💾 创建备份提交..."
git commit -m "📦 每日备份 - ${DATE} ${TIME}

🔄 自动备份
- 更新 SELF_SUMMARY.md
- 备份所有工作区文件
- 保留最近 ${MAX_BACKUPS} 个备份

绾绾 🤖"

# 5. 创建备份分支标签
echo "🏷️  创建备份标签..."
git tag -a "backup-${DATE}-${TIME}" -m "每日备份 - ${DATE} ${TIME}"

# 6. 清理旧备份（保留最近 3 天）
echo "🗑️  清理旧备份..."
# 获取所有 backup 开头的标签
OLD_BACKUPS=$(git tag -l "backup-*" | sort | head -n -${MAX_BACKUPS})

if [ -n "$OLD_BACKUPS" ]; then
    echo "删除旧备份标签:"
    echo "$OLD_BACKUPS" | while read -r tag; do
        echo "  - $tag"
        git tag -d "$tag"
    done
fi

# 7. 推送到 GitHub
echo "🚀 推送到 GitHub..."
git push origin master --tags

echo ""
echo "✅ 备份完成！"
echo "备份标签：backup-${DATE}-${TIME}"
echo "GitHub: https://github.com/123z32/wanwan-skill"
echo ""

# 8. 发送飞书消息汇报
echo "📱 发送飞书汇报..."
cat << EOF
🎉 **每日备份完成**

**日期**: ${DATE} ${TIME}
**状态**: ✅ 成功
**备份标签**: backup-${DATE}-${TIME}
**保留备份**: 最近 ${MAX_BACKUPS} 天

**备份内容**:
- ✅ 工作区所有文件
- ✅ SELF_SUMMARY.md (已更新时间戳)
- ✅ 所有技能和项目代码

**访问地址**: 
https://github.com/123z32/wanwan-skill

晚安张！🌙 明天见～
EOF
