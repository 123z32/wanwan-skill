#!/bin/bash
# ============================================
# Ubuntu Server 迁移 - 迁移后检查
# ============================================
# 用法：./post-migration-check.sh
# ============================================

echo "=========================================="
echo "  迁移后系统检查"
echo "=========================================="
echo ""

# 系统信息
echo "## 系统信息"
echo "主机名：$(hostname)"
echo "系统：$(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "内核：$(uname -r)"
echo ""

# 内存（重点检查）
echo "## 内存状态（目标：<3GB 已用）"
free -h
USED_MEM=$(free | grep Mem | awk '{print $3}')
TOTAL_MEM=$(free | grep Mem | awk '{print $2}')
echo ""

# 磁盘
echo "## 磁盘状态"
df -h /
echo ""

# 网络
echo "## 网络配置"
ip addr show | grep "inet " | head -2
echo ""

# Docker
echo "## Docker 状态"
systemctl is-active docker && echo "✅ Docker 运行中" || echo "❌ Docker 未运行"
docker ps | head -5
echo ""

# OpenClaw
echo "## OpenClaw 状态"
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw: $(openclaw --version)"
    openclaw status 2>/dev/null || echo "⚠️  OpenClaw 状态检查失败"
else
    echo "❌ OpenClaw 未安装"
fi
echo ""

# RAG 服务
echo "## RAG 服务状态"
curl -s http://localhost:9900/api/health | jq . 2>/dev/null || echo "⚠️  RAG 服务未运行"
echo ""

# 关键文件
echo "## 关键文件检查"
[ -f "/openclaw_data/config/config.json" ] && echo "✅ config.json" || echo "❌ config.json"
[ -d "/openclaw_data/.openclaw/workspace" ] && echo "✅ Workspace" || echo "❌ Workspace"
[ -d "/openclaw_data/.openclaw/workspace/memory" ] && echo "✅ Memory" || echo "❌ Memory"
[ -d "/openclaw_data/.openclaw/workspace-coder/projects/personal-kb" ] && echo "✅ RAG" || echo "❌ RAG"
echo ""

# 测试消息
echo "## 功能测试"
echo "请发送一条飞书消息测试..."
echo "等待 10 秒..."
sleep 10
echo ""

echo "=========================================="
echo "检查完成！"
echo "=========================================="
echo ""
echo "成功标准："
echo "✅ 内存使用 < 3GB"
echo "✅ Docker 运行正常"
echo "✅ OpenClaw 运行正常"
echo "✅ RAG 服务响应正常"
echo "✅ 飞书消息收发正常"
echo ""
