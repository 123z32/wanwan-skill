#!/bin/bash
# 会话结束学习提醒脚本
# 在每次会话结束时运行，提醒记录学习

LEARNINGS_DIR="/openclaw_data/.openclaw/workspace/.learnings"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo ""
echo "📚 ========== 会话结束学习提醒 =========="
echo "时间：$DATE"
echo ""

# 检查是否有未解决的错误
if [ -f "$LEARNINGS_DIR/ERRORS.md" ]; then
    PENDING_ERRORS=$(grep -c "Status\*\*: pending" "$LEARNINGS_DIR/ERRORS.md" 2>/dev/null || echo "0")
    if [ "$PENDING_ERRORS" -gt 0 ]; then
        echo "⚠️  有 $PENDING_ERRORS 个未解决的错误待处理"
        echo "   查看：$LEARNINGS_DIR/ERRORS.md"
        echo ""
    fi
fi

# 检查是否有未处理的学习
if [ -f "$LEARNINGS_DIR/LEARNINGS.md" ]; then
    PENDING_LEARNINGS=$(grep -c "Status\*\*: pending" "$LEARNINGS_DIR/LEARNINGS.md" 2>/dev/null || echo "0")
    if [ "$PENDING_LEARNINGS" -gt 0 ]; then
        echo "📖 有 $PENDING_LEARNINGS 个未处理的学习待推广"
        echo "   查看：$LEARNINGS_DIR/LEARNINGS.md"
        echo ""
    fi
fi

# 提醒记录本次会话的学习
echo "💡 问题："
echo "   1. 本次会话遇到了什么错误？"
echo "   2. 学到了什么新知识？"
echo "   3. 有什么配置需要更新？"
echo ""
echo "📝 记录命令:"
echo "   # 记录错误"
echo "   nano $LEARNINGS_DIR/ERRORS.md"
echo ""
echo "   # 记录学习"
echo "   nano $LEARNINGS_DIR/LEARNINGS.md"
echo ""
echo "========================================"
echo ""
