#!/bin/bash
# OpenClaw Gateway 重启脚本
# 用法：./restart-gateway.sh [--port 18789]

PORT=18789
GATEWAY_NAME="openclaw-gateway"
LOG_FILE="/openclaw_data/.openclaw/workspace/logs/gateway-restart.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 1. 检查旧进程
log "${YELLOW}📋 检查 Gateway 进程...${NC}"
OLD_PID=$(pgrep -f "$GATEWAY_NAME" | head -1)

if [ -n "$OLD_PID" ]; then
    log "${YELLOW}⚠️  发现旧进程 (PID: $OLD_PID)，正在停止...${NC}"
    pkill -f "$GATEWAY_NAME"
    
    # 等待进程完全停止（最多等 10 秒）
    for i in {1..10}; do
        if ! pgrep -f "$GATEWAY_NAME" > /dev/null; then
            log "${GREEN}✅ 旧进程已停止${NC}"
            break
        fi
        sleep 1
    done
    
    # 如果还在运行，强制杀死
    if pgrep -f "$GATEWAY_NAME" > /dev/null; then
        log "${RED}⚠️  旧进程未停止，强制杀死...${NC}"
        pkill -9 -f "$GATEWAY_NAME"
        sleep 2
    fi
else
    log "${GREEN}✅ 没有运行中的 Gateway 进程${NC}"
fi

# 2. 清理残留端口
log "${YELLOW}📋 检查端口 $PORT 占用...${NC}"
if command -v ss &> /dev/null; then
    PORT_PID=$(ss -tlnp | grep ":$PORT " | awk '{print $7}' | grep -oP 'pid=\K[0-9]+' | head -1)
    if [ -n "$PORT_PID" ]; then
        log "${YELLOW}⚠️  端口 $PORT 被占用 (PID: $PORT_PID)，释放中...${NC}"
        kill -9 $PORT_PID 2>/dev/null
        sleep 2
    fi
fi

# 3. 验证配置
log "${YELLOW}📋 验证配置文件...${NC}"
if openclaw config validate > /dev/null 2>&1; then
    log "${GREEN}✅ 配置验证通过${NC}"
else
    log "${RED}❌ 配置验证失败！请检查配置${NC}"
    openclaw config validate
    exit 1
fi

# 4. 启动新 Gateway
log "${YELLOW}🚀 启动 Gateway (端口：$PORT)...${NC}"
openclaw gateway --port "$PORT" &
NEW_PID=$!

# 5. 等待启动完成（最多等 15 秒）
log "${YELLOW}⏳ 等待 Gateway 启动...${NC}"
for i in {1..15}; do
    sleep 1
    if openclaw status > /dev/null 2>&1; then
        log "${GREEN}✅ Gateway 启动成功！${NC}"
        break
    fi
    
    if [ $i -eq 15 ]; then
        log "${RED}❌ Gateway 启动超时！${NC}"
        exit 1
    fi
done

# 6. 显示状态
log "${YELLOW}📊 Gateway 状态：${NC}"
openclaw status 2>&1 | grep -E "Gateway|reachable|Agents" | head -5

# 7. 记录新 PID
NEW_PID=$(pgrep -f "$GATEWAY_NAME" | head -1)
log "${GREEN}✅ 重启完成！新进程 PID: $NEW_PID${NC}"

exit 0
