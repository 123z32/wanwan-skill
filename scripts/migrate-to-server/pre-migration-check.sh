#!/bin/bash
# ============================================
# Ubuntu Server 迁移 - 迁移前检查
# ============================================
# 用法：./pre-migration-check.sh
# ============================================

echo "=========================================="
echo "  迁移前系统检查"
echo "=========================================="
echo ""

# 系统信息
echo "## 系统信息"
echo "主机名：$(hostname)"
echo "系统：$(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "内核：$(uname -r)"
echo ""

# 内存
echo "## 内存状态"
free -h
echo ""

# 磁盘
echo "## 磁盘状态"
df -h /
echo ""

# 网络
echo "## 网络配置"
ip addr show | grep -E "inet |link/"
echo ""

# 关键服务
echo "## 关键服务状态"
systemctl is-active docker 2>/dev/null && echo "✅ Docker 运行中" || echo "❌ Docker 未运行"
systemctl is-active openclaw-gateway 2>/dev/null && echo "✅ OpenClaw Gateway 运行中" || echo "⚠️  OpenClaw Gateway 未运行"
echo ""

# OpenClaw 检查
echo "## OpenClaw 检查"
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw 已安装：$(openclaw --version)"
else
    echo "❌ OpenClaw 未安装"
fi
echo ""

# 关键文件
echo "## 关键文件检查"
[ -f "/openclaw_data/config/config.json" ] && echo "✅ config.json 存在" || echo "❌ config.json 不存在"
[ -d "/openclaw_data/.openclaw/workspace" ] && echo "✅ Workspace 存在" || echo "❌ Workspace 不存在"
[ -d "/openclaw_data/.openclaw/workspace/memory" ] && echo "✅ Memory 目录存在" || echo "❌ Memory 目录不存在"
echo ""

# 备份检查
echo "## 备份建议"
echo "⚠️  请确保已运行 ./backup-all.sh"
echo "⚠️  备份文件应复制到外部存储"
echo ""

echo "=========================================="
echo "检查完成！"
echo "=========================================="
echo ""
echo "如果以上检查都通过，可以开始迁移。"
echo "否则请先解决标记为 ❌ 的问题。"
echo ""
