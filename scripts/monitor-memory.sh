#!/bin/bash
# 内存监控脚本 - 记录 Gateway 内存使用情况

LOG_FILE="/openclaw_data/.openclaw/workspace/memory/gateway-memory.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# 获取 Gateway 进程内存 (KB)
GATEWAY_PID=$(pgrep -f openclaw-gateway | head -1)
if [ -n "$GATEWAY_PID" ]; then
    RSS_KB=$(ps -o rss= -p $GATEWAY_PID 2>/dev/null)
    RSS_MB=$((RSS_KB / 1024))
    
    # 获取系统内存状态
    MEM_TOTAL=$(free -m | awk '/^Mem:/ {print $2}')
    MEM_USED=$(free -m | awk '/^Mem:/ {print $3}')
    MEM_FREE=$(free -m | awk '/^Mem:/ {print $4}')
    MEM_AVAILABLE=$(free -m | awk '/^Mem:/ {print $7}')
    SWAP_TOTAL=$(free -m | awk '/^Swap:/ {print $2}')
    SWAP_USED=$(free -m | awk '/^Swap:/ {print $3}')
    
    # 记录日志
    echo "[$DATE] Gateway: ${RSS_MB}MB | 系统：${MEM_USED}/${MEM_TOTAL}MB | 可用：${MEM_AVAILABLE}MB | Swap: ${SWAP_USED}/${SWAP_TOTAL}MB" >> "$LOG_FILE"
    
    # 显示最新状态
    echo "📊 [$DATE]"
    echo "   Gateway: ${RSS_MB} MB"
    echo "   系统内存：${MEM_USED}/${MEM_TOTAL} MB (${MEM_AVAILABLE} MB 可用)"
    echo "   Swap: ${SWAP_USED}/${SWAP_TOTAL} MB"
    echo ""
else
    echo "[$DATE] Gateway 进程未找到" >> "$LOG_FILE"
    echo "❌ Gateway 进程未找到"
fi

# 保留最近 1000 条记录
if [ -f "$LOG_FILE" ]; then
    tail -n 1000 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi
