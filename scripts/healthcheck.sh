#!/bin/bash
# ============================================
# OpenClaw 健康检查脚本
# ============================================
# 用于 systemd 服务健康检查
# ============================================

set -e

LOG_FILE="/home/node/.openclaw/workspace/logs/healthcheck.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 1. 检查 Gateway 进程
if ! pgrep -f "openclaw-gateway" > /dev/null; then
    log "❌ Gateway 进程不存在"
    exit 1
fi

# 2. 检查端口监听
if ! ss -tlnp | grep -q ":18789"; then
    log "❌ Gateway 端口未监听"
    exit 1
fi

# 3. 检查 OpenClaw 状态
if ! openclaw status > /dev/null 2>&1; then
    log "❌ OpenClaw status 检查失败"
    exit 1
fi

log "✅ 健康检查通过"
exit 0
