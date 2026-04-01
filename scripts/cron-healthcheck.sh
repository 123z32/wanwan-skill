#!/bin/bash
# ============================================
# 定时健康检查（cron 调用）
# ============================================
# 每 5 分钟检查一次系统状态
# ============================================

set -e

WORKSPACE="/home/node/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/cron-healthcheck.log"
HEAL_SCRIPT="$WORKSPACE/scripts/auto-heal.sh"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log "${BLUE}========================================${NC}"
log "${BLUE}  定时健康检查${NC}"
log "${BLUE}========================================${NC}"

# 1. 检查 Gateway
if pgrep -f "openclaw-gateway" > /dev/null; then
    log "${GREEN}✅ Gateway 运行正常${NC}"
else
    log "${RED}❌ Gateway 异常，触发自动恢复${NC}"
    bash "$HEAL_SCRIPT"
fi

# 2. 检查磁盘空间
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    log "${YELLOW}⚠️  磁盘使用率：${DISK_USAGE}%${NC}"
else
    log "${GREEN}✅ 磁盘使用率：${DISK_USAGE}%${NC}"
fi

# 3. 检查内存
MEM_AVAILABLE=$(free -m | awk '/^Mem:/ {print $7}')
if [ "$MEM_AVAILABLE" -lt 500 ]; then
    log "${YELLOW}⚠️  可用内存：${MEM_AVAILABLE}MB${NC}"
else
    log "${GREEN}✅ 可用内存：${MEM_AVAILABLE}MB${NC}"
fi

log "${GREEN}✅ 健康检查完成${NC}"
