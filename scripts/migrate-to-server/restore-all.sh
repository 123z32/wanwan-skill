#!/bin/bash
# ============================================
# Ubuntu Server 迁移 - 数据恢复脚本
# ============================================
# 用法：sudo ./restore-all.sh [备份目录]
# 示例：sudo ./restore-all.sh /home/ubuntu/backups/openclaw_backup_20260325_183000
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BACKUP_DIR="$1"

if [ -z "$BACKUP_DIR" ]; then
    echo -e "${RED}用法：./restore-all.sh [备份目录]${NC}"
    echo "示例：./restore-all.sh /home/ubuntu/backups/openclaw_backup_20260325_183000"
    exit 1
fi

if [ ! -d "$BACKUP_DIR" ]; then
    echo -e "${RED}错误：备份目录不存在：${BACKUP_DIR}${NC}"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ubuntu Server 迁移 - 数据恢复脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}备份源：${BACKUP_DIR}${NC}"
echo ""

# 确认
echo -e "${YELLOW}⚠️  即将恢复数据到系统${NC}"
echo "此操作将覆盖现有数据（如果存在）"
echo ""
read -p "确认继续？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}已取消${NC}"
    exit 0
fi

# ============================================
# 1. 创建目录结构
# ============================================
echo -e "${GREEN}[1/6] 创建目录结构...${NC}"

sudo mkdir -p /openclaw_data/.openclaw/workspace
sudo mkdir -p /openclaw_data/.openclaw/workspace-coder/projects/personal-kb
sudo chown -R $USER:$USER /openclaw_data

echo -e "${GREEN}✅ 目录创建完成${NC}"

# ============================================
# 2. 恢复 OpenClaw 数据
# ============================================
echo -e "${GREEN}[2/6] 恢复 OpenClaw 数据...${NC}"

if [ -f "${BACKUP_DIR}/openclaw_data.tar.gz" ]; then
    sudo tar -xzf "${BACKUP_DIR}/openclaw_data.tar.gz" -C /
    echo -e "${GREEN}✅ OpenClaw 数据恢复完成${NC}"
else
    echo -e "${RED}⚠️  openclaw_data.tar.gz 不存在${NC}"
fi

# ============================================
# 3. 恢复配置
# ============================================
echo -e "${GREEN}[3/6] 恢复配置...${NC}"

if [ -f "${BACKUP_DIR}/config/config.json" ]; then
    sudo mkdir -p /openclaw_data/config
    sudo cp "${BACKUP_DIR}/config/config.json" /openclaw_data/config/
    echo -e "${GREEN}✅ config.json 恢复完成${NC}"
else
    echo -e "${YELLOW}⚠️  config.json 不存在，需手动配置${NC}"
fi

# ============================================
# 4. 恢复 Workspace
# ============================================
echo -e "${GREEN}[4/6] 恢复 Workspace...${NC}"

if [ -f "${BACKUP_DIR}/workspace.tar.gz" ]; then
    sudo tar -xzf "${BACKUP_DIR}/workspace.tar.gz" -C /openclaw_data/.openclaw/
    echo -e "${GREEN}✅ Workspace 恢复完成${NC}"
else
    echo -e "${RED}⚠️  workspace.tar.gz 不存在${NC}"
fi

# ============================================
# 5. 恢复 RAG 知识库
# ============================================
echo -e "${GREEN}[5/6] 恢复 RAG 知识库...${NC}"

if [ -f "${BACKUP_DIR}/rag-knowledge.tar.gz" ]; then
    sudo tar -xzf "${BACKUP_DIR}/rag-knowledge.tar.gz" -C /openclaw_data/.openclaw/workspace-coder/projects/personal-kb/
    echo -e "${GREEN}✅ RAG 知识库恢复完成${NC}"
else
    echo -e "${YELLOW}⚠️  rag-knowledge.tar.gz 不存在${NC}"
fi

# ============================================
# 6. 恢复记忆文件
# ============================================
echo -e "${GREEN}[6/6] 恢复记忆文件...${NC}"

if [ -f "${BACKUP_DIR}/memory.tar.gz" ]; then
    sudo tar -xzf "${BACKUP_DIR}/memory.tar.gz" -C /openclaw_data/.openclaw/workspace/memory/
    echo -e "${GREEN}✅ 记忆文件恢复完成${NC}"
else
    echo -e "${YELLOW}⚠️  memory.tar.gz 不存在${NC}"
fi

# ============================================
# 完成
# ============================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ 数据恢复完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "1. 检查配置：cat /openclaw_data/config/config.json"
echo "2. 启动 OpenClaw Gateway"
echo "3. 启动 RAG 服务"
echo "4. 运行测试"
echo ""
