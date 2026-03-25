#!/bin/bash
# ============================================
# Ubuntu Server 迁移 - 全量备份脚本
# ============================================
# 用法：./backup-all.sh [备份目录]
# 示例：./backup-all.sh /mnt/usb-drive/backups
# ============================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 备份目录
BACKUP_DIR="${1:-$HOME/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="openclaw_backup_${TIMESTAMP}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ubuntu Server 迁移 - 全量备份脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}备份目录：${BACKUP_DIR}${NC}"
echo -e "${YELLOW}备份名称：${BACKUP_NAME}${NC}"
echo ""

# 创建备份目录
mkdir -p "${BACKUP_DIR}/${BACKUP_NAME}"
cd "${BACKUP_DIR}/${BACKUP_NAME}"

# ============================================
# 1. 系统配置备份
# ============================================
echo -e "${GREEN}[1/8] 备份系统配置...${NC}"

mkdir -p system
ip addr show > system/network.txt 2>&1
cat /etc/resolv.conf > system/dns.txt 2>&1
cat /etc/hostname > system/hostname.txt 2>&1
cat /etc/hosts > system/hosts.txt 2>&1
df -h > system/disk.txt 2>&1
free -h > system/memory.txt 2>&1
uname -a > system/kernel.txt 2>&1
lsblk > system/storage.txt 2>&1

echo -e "${GREEN}✅ 系统配置备份完成${NC}"

# ============================================
# 2. OpenClaw 数据备份
# ============================================
echo -e "${GREEN}[2/8] 备份 OpenClaw 数据...${NC}"

if [ -d "/openclaw_data" ]; then
    tar -czf openclaw_data.tar.gz \
        --exclude='node_modules' \
        --exclude='backups' \
        --exclude='*.log' \
        /openclaw_data/
    echo -e "${GREEN}✅ OpenClaw 数据备份完成${NC}"
else
    echo -e "${RED}⚠️  /openclaw_data 不存在${NC}"
fi

# ============================================
# 3. OpenClaw 配置备份
# ============================================
echo -e "${GREEN}[3/8] 备份 OpenClaw 配置...${NC}"

mkdir -p config
if [ -f "/openclaw_data/config/config.json" ]; then
    cp /openclaw_data/config/config.json config/
    echo -e "${GREEN}✅ config.json 已备份${NC}"
else
    echo -e "${YELLOW}⚠️  config.json 不存在${NC}"
fi

if [ -f "/openclaw_data/config/models.json" ]; then
    cp /openclaw_data/config/models.json config/
    echo -e "${GREEN}✅ models.json 已备份${NC}"
fi

# ============================================
# 4. Workspace 备份
# ============================================
echo -e "${GREEN}[4/8] 备份 Workspace...${NC}"

if [ -d "/openclaw_data/.openclaw/workspace" ]; then
    tar -czf workspace.tar.gz \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='*.log' \
        /openclaw_data/.openclaw/workspace/
    echo -e "${GREEN}✅ Workspace 备份完成${NC}"
else
    echo -e "${RED}⚠️  workspace 不存在${NC}"
fi

# ============================================
# 5. RAG 知识库备份
# ============================================
echo -e "${GREEN}[5/8] 备份 RAG 知识库...${NC}"

RAG_DIR="/openclaw_data/.openclaw/workspace-coder/projects/personal-kb"
if [ -d "$RAG_DIR" ]; then
    tar -czf rag-knowledge.tar.gz \
        --include='knowledge/**' \
        --include='kb.json' \
        --include='server.js' \
        --exclude='node_modules' \
        -C "$RAG_DIR" .
    echo -e "${GREEN}✅ RAG 知识库备份完成${NC}"
else
    echo -e "${YELLOW}⚠️  RAG 目录不存在${NC}"
fi

# ============================================
# 6. 技能备份
# ============================================
echo -e "${GREEN}[6/8] 备份 Skills...${NC}"

SKILLS_DIR="/openclaw_data/.openclaw/workspace/skills"
if [ -d "$SKILLS_DIR" ]; then
    tar -czf skills.tar.gz -C "$SKILLS_DIR" .
    echo -e "${GREEN}✅ Skills 备份完成${NC}"
else
    echo -e "${YELLOW}⚠️  Skills 目录不存在${NC}"
fi

# ============================================
# 7. 记忆文件备份
# ============================================
echo -e "${GREEN}[7/8] 备份记忆文件...${NC}"

MEMORY_DIR="/openclaw_data/.openclaw/workspace/memory"
if [ -d "$MEMORY_DIR" ]; then
    tar -czf memory.tar.gz -C "$MEMORY_DIR" .
    echo -e "${GREEN}✅ 记忆文件备份完成${NC}"
else
    echo -e "${YELLOW}⚠️  Memory 目录不存在${NC}"
fi

# ============================================
# 8. 创建备份清单
# ============================================
echo -e "${GREEN}[8/8] 创建备份清单...${NC}"

cat > MANIFEST.txt << EOF
# OpenClaw 迁移备份清单
# 生成时间：$(date)
# 主机名：$(hostname)
# 用户：$(whoami)

## 系统信息
$(uname -a)

## 内存信息
$(free -h)

## 磁盘信息
$(df -h)

## 备份文件列表
$(ls -lh)

## 网络配置
$(ip addr show)

## DNS 配置
$(cat /etc/resolv.conf)
EOF

echo -e "${GREEN}✅ 备份清单创建完成${NC}"

# ============================================
# 完成
# ============================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ 备份完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}备份位置：${BACKUP_DIR}/${BACKUP_NAME}${NC}"
echo -e "${YELLOW}备份大小：$(du -sh "${BACKUP_DIR}/${BACKUP_NAME}" | cut -f1)${NC}"
echo ""
echo -e "${GREEN}下一步:${NC}"
echo "1. 验证备份文件：ls -lh ${BACKUP_DIR}/${BACKUP_NAME}/"
echo "2. 复制备份到外部存储（推荐）"
echo "3. 准备 Ubuntu Server 安装介质"
echo ""

# 显示备份文件列表
echo -e "${BLUE}备份文件列表:${NC}"
ls -lh
