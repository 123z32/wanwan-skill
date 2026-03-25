#!/bin/bash
# ============================================
# Ubuntu Server 迁移 - 依赖安装脚本
# ============================================
# 用法：sudo ./install-dependencies.sh
# ============================================

set -e

echo "=========================================="
echo "  Ubuntu Server - 依赖安装脚本"
echo "=========================================="
echo ""

# 更新包列表
echo "[1/10] 更新包列表..."
sudo apt update -qq

# 安装基础工具
echo "[2/10] 安装基础工具..."
sudo apt install -y \
    git \
    curl \
    wget \
    vim \
    htop \
    net-tools \
    jq \
    unzip \
    build-essential \
    -qq

# 安装 Node.js 22
echo "[3/10] 安装 Node.js 22..."
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs -qq

# 安装 Docker
echo "[4/10] 安装 Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
echo "[5/10] 安装 Docker Compose..."
sudo apt install -y docker-compose -qq

# 安装 Python3-venv
echo "[6/10] 安装 Python 虚拟环境..."
sudo apt install -y python3.11-venv python3-pip -qq

# 安装系统服务
echo "[7/10] 配置系统服务..."
sudo systemctl enable docker
sudo systemctl start docker

# 安装 OpenClaw（如果未安装）
echo "[8/10] 检查 OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    echo "OpenClaw 未安装，跳过（需手动安装）"
else
    echo "✅ OpenClaw 已安装"
fi

# 清理
echo "[9/10] 清理缓存..."
sudo apt autoremove -y -qq
sudo apt clean -qq

# 验证
echo "[10/10] 验证安装..."
echo ""
echo "Node.js: $(node -v)"
echo "npm: $(npm -v)"
echo "Docker: $(docker --version)"
echo "Git: $(git --version)"
echo ""

echo "=========================================="
echo "✅ 依赖安装完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 重新登录以应用 Docker 组权限"
echo "2. 恢复 OpenClaw 数据"
echo "3. 配置 OpenClaw Gateway"
echo ""
