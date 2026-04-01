#!/bin/bash
# ============================================
# OpenClaw 启动脚本（Gateway + 健康检查）
# ============================================
# 用法：./start-all.sh
# ============================================

set -e

WORKSPACE="/home/node/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/start-all.log"
SUPERVISOR="$WORKSPACE/scripts/supervisor.sh"
HEALTHCHECK_DAEMON="$WORKSPACE/scripts/healthcheck-daemon.js"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log "${BLUE}========================================${NC}"
log "${BLUE}  OpenClaw 启动脚本${NC}"
log "${BLUE}========================================${NC}"

# 1. 启动 Gateway
log "${YELLOW}📋 启动 Gateway...${NC}"
bash "$SUPERVISOR" start

# 2. 等待 Gateway 启动
log "${YELLOW}⏳ 等待 Gateway 启动...${NC}"
sleep 5

# 3. 验证 Gateway 状态
if bash "$SUPERVISOR" status > /dev/null 2>&1; then
    log "${GREEN}✅ Gateway 启动成功${NC}"
else
    log "${RED}❌ Gateway 启动失败${NC}"
    exit 1
fi

# 4. 启动健康检查守护进程
log "${YELLOW}📋 启动健康检查守护进程...${NC}"
nohup node "$HEALTHCHECK_DAEMON" > "$WORKSPACE/logs/healthcheck-daemon.log" 2>&1 &
HC_PID=$!
echo "$HC_PID" > /tmp/openclaw-healthcheck.pid

log "${GREEN}✅ 健康检查守护进程启动 (PID: $HC_PID)${NC}"

# 5. 显示状态
log "${BLUE}========================================${NC}"
log "${GREEN}✅ 启动完成！${NC}"
log "${BLUE}========================================${NC}"
log ""
log "📊 服务状态:"
log "  - Gateway: 运行中"
log "  - 健康检查：运行中 (每 5 分钟检查)"
log ""
log "📁 日志文件:"
log "  - Gateway: $WORKSPACE/logs/gateway.log"
log "  - 健康检查：$WORKSPACE/logs/cron-healthcheck.log"
log ""
log "🛑 停止服务:"
log "  bash $SUPERVISOR stop"
log "  kill \$(cat /tmp/openclaw-healthcheck.pid)"
log ""
