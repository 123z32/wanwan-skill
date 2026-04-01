#!/bin/bash
# ============================================
# OpenClaw Gateway 守护进程（容器版）
# ============================================
# 用法：./supervisor.sh [start|stop|restart|status]
# ============================================

set -e

WORKSPACE="/home/node/.openclaw/workspace"
PID_FILE="/tmp/openclaw-gateway.pid"
LOG_FILE="/home/node/.openclaw/workspace/logs/gateway.log"
HEAL_SCRIPT="$WORKSPACE/scripts/auto-heal.sh"

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

start() {
    log "${BLUE}🚀 启动 Gateway...${NC}"
    
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            log "${YELLOW}⚠️  Gateway 已在运行 (PID: $OLD_PID)${NC}"
            return 0
        fi
        rm -f "$PID_FILE"
    fi
    
    cd "$WORKSPACE"
    nohup openclaw gateway > "$LOG_FILE" 2>&1 &
    NEW_PID=$!
    echo "$NEW_PID" > "$PID_FILE"
    
    # 等待启动
    for i in {1..15}; do
        sleep 1
        if ps -p "$NEW_PID" > /dev/null 2>&1; then
            log "${GREEN}✅ Gateway 启动成功 (PID: $NEW_PID)${NC}"
            return 0
        fi
    done
    
    log "${RED}❌ Gateway 启动失败${NC}"
    return 1
}

stop() {
    log "${YELLOW}🛑 停止 Gateway...${NC}"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID" 2>/dev/null || true
            sleep 2
            if ps -p "$PID" > /dev/null 2>&1; then
                kill -9 "$PID" 2>/dev/null || true
            fi
            log "${GREEN}✅ Gateway 已停止${NC}"
        else
            log "${YELLOW}⚠️  进程不存在${NC}"
        fi
        rm -f "$PID_FILE"
    else
        # 尝试通过进程名查找
        pkill -f "openclaw-gateway" 2>/dev/null || true
        log "${GREEN}✅ Gateway 已停止${NC}"
    fi
}

restart() {
    stop
    sleep 2
    start
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            log "${GREEN}✅ Gateway 运行中 (PID: $PID)${NC}"
            return 0
        fi
    fi
    
    # 尝试通过进程名查找
    if pgrep -f "openclaw-gateway" > /dev/null; then
        PID=$(pgrep -f "openclaw-gateway" | head -1)
        log "${GREEN}✅ Gateway 运行中 (PID: $PID)${NC}"
        return 0
    fi
    
    log "${RED}❌ Gateway 未运行${NC}"
    return 1
}

# 自动监控模式（后台守护）
monitor() {
    log "${BLUE}👁️  启动监控模式...${NC}"
    
    while true; do
        sleep 60  # 每分钟检查一次
        
        if ! status > /dev/null 2>&1; then
            log "${YELLOW}⚠️  Gateway 异常，触发自动恢复...${NC}"
            bash "$HEAL_SCRIPT"
        fi
    done
}

case "${1:-status}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    monitor)
        monitor &
        echo $! > /tmp/openclaw-supervisor.pid
        log "${GREEN}✅ 监控进程启动 (PID: $!)${NC}"
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status|monitor}"
        exit 1
        ;;
esac
