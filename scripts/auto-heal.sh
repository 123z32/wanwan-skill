#!/bin/bash
# ============================================
# OpenClaw 自动恢复脚本
# ============================================
# 功能：
# 1. 检查 Gateway 进程
# 2. 检查网络连通性
# 3. 自动重启 Gateway
# 4. 必要时从 Git 恢复配置
# ============================================

set -e

WORKSPACE="/home/node/.openclaw/workspace"
LOG_FILE="/home/node/.openclaw/workspace/logs/auto-heal.log"
GIT_REMOTE="https://github.com/123z32/wanwan-skill.git"
MAX_RETRY=3

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

# ============================================
# 1. 检查 Gateway 进程
# ============================================
check_gateway() {
    log "${BLUE}📋 检查 Gateway 进程...${NC}"
    
    if pgrep -f "openclaw-gateway" > /dev/null; then
        PID=$(pgrep -f "openclaw-gateway" | head -1)
        log "${GREEN}✅ Gateway 运行中 (PID: $PID)${NC}"
        return 0
    else
        log "${RED}❌ Gateway 进程不存在${NC}"
        return 1
    fi
}

# ============================================
# 2. 检查网络连通性
# ============================================
check_network() {
    log "${BLUE}📋 检查网络连通性...${NC}"
    
    # 测试 GitHub 连接
    if curl -s --connect-timeout 5 https://github.com > /dev/null; then
        log "${GREEN}✅ GitHub 可访问${NC}"
        return 0
    else
        log "${RED}❌ GitHub 不可访问${NC}"
        return 1
    fi
}

# ============================================
# 3. 重启 Gateway
# ============================================
restart_gateway() {
    log "${YELLOW}🔄 重启 Gateway...${NC}"
    
    # 停止旧进程
    pkill -f "openclaw-gateway" 2>/dev/null || true
    sleep 2
    
    # 启动新进程
    cd "$WORKSPACE"
    openclaw gateway &
    
    # 等待启动
    for i in {1..15}; do
        sleep 1
        if pgrep -f "openclaw-gateway" > /dev/null; then
            log "${GREEN}✅ Gateway 重启成功${NC}"
            return 0
        fi
    done
    
    log "${RED}❌ Gateway 重启失败${NC}"
    return 1
}

# ============================================
# 4. 从 Git 恢复配置
# ============================================
restore_from_git() {
    log "${YELLOW}📦 从 Git 恢复配置...${NC}"
    
    cd "$WORKSPACE"
    
    # 检查是否是 Git 仓库
    if [ ! -d ".git" ]; then
        log "${YELLOW}⚠️  不是 Git 仓库，重新克隆...${NC}"
        cd /home/node/.openclaw/
        rm -rf workspace
        git clone "$GIT_REMOTE" workspace
        cd "$WORKSPACE"
    else
        # 重置到最新
        git fetch origin 2>/dev/null || {
            log "${RED}❌ Git fetch 失败${NC}"
            return 1
        }
        git reset --hard origin/main 2>/dev/null || {
            log "${YELLOW}⚠️  Git reset 失败，尝试 checkout${NC}"
            git checkout main 2>/dev/null || return 1
        }
    fi
    
    log "${GREEN}✅ Git 恢复完成${NC}"
    return 0
}

# ============================================
# 主流程
# ============================================
main() {
    log "${BLUE}========================================${NC}"
    log "${BLUE}  OpenClaw 自动恢复检查${NC}"
    log "${BLUE}========================================${NC}"
    
    RETRY=0
    
    while [ $RETRY -lt $MAX_RETRY ]; do
        # 检查 Gateway
        if check_gateway; then
            log "${GREEN}✅ 系统正常${NC}"
            exit 0
        fi
        
        # Gateway 异常，尝试恢复
        RETRY=$((RETRY + 1))
        log "${YELLOW}⚠️  尝试恢复 (第 $RETRY 次)...${NC}"
        
        # 检查网络
        if ! check_network; then
            log "${YELLOW}⚠️  网络不可用，等待 30 秒...${NC}"
            sleep 30
            continue
        fi
        
        # 尝试重启 Gateway
        if restart_gateway; then
            sleep 5
            if check_gateway; then
                log "${GREEN}✅ 恢复成功${NC}"
                exit 0
            fi
        fi
        
        # 重启失败，尝试 Git 恢复
        if [ $RETRY -ge 2 ]; then
            log "${YELLOW}⚠️  尝试从 Git 恢复...${NC}"
            if restore_from_git; then
                if restart_gateway; then
                    sleep 5
                    if check_gateway; then
                        log "${GREEN}✅ Git 恢复成功${NC}"
                        exit 0
                    fi
                fi
            fi
        fi
        
        sleep 10
    done
    
    log "${RED}❌ 恢复失败，已达到最大重试次数${NC}"
    exit 1
}

# 执行
main
