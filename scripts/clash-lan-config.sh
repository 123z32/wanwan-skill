#!/bin/bash
# ============================================
# Clash LAN 访问配置脚本
# ============================================
# 功能：
# 1. 配置代理环境变量
# 2. 配置 NO_PROXY（LAN 直连）
# 3. 测试网络连通性
# ============================================

set -e

# 代理服务器（Tailscale 网络中的 Clash 节点）
PROXY_SERVER="100.82.227.79:7890"

# LAN 网段（不经过代理）
LAN_NETWORKS="100.64.0.0/10,100.100.0.0/16,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,localhost,127.0.0.1"

# 导出代理配置
export HTTP_PROXY="http://${PROXY_SERVER}"
export HTTPS_PROXY="http://${PROXY_SERVER}"
export http_proxy="http://${PROXY_SERVER}"
export https_proxy="http://${PROXY_SERVER}"

# 配置 NO_PROXY（LAN 直连）
export NO_PROXY="${LAN_NETWORKS}"
export no_proxy="${LAN_NETWORKS}"

echo "✅ 代理配置完成"
echo ""
echo "📊 配置信息:"
echo "  代理服务器：${PROXY_SERVER}"
echo "  HTTP_PROXY: ${HTTP_PROXY}"
echo "  HTTPS_PROXY: ${HTTPS_PROXY}"
echo "  NO_PROXY: ${NO_PROXY}"
echo ""

# 测试网络连通性
echo "🔍 测试网络连通性..."
echo ""

# 测试外网（通过代理）
if curl -s --connect-timeout 3 --proxy "${HTTP_PROXY}" https://www.google.com > /dev/null; then
    echo "✅ 外网访问：正常（通过代理）"
else
    echo "❌ 外网访问：失败"
fi

# 测试 GitHub（通过代理）
if curl -s --connect-timeout 5 --proxy "${HTTP_PROXY}" https://api.github.com > /dev/null; then
    echo "✅ GitHub 访问：正常（通过代理）"
else
    echo "❌ GitHub 访问：失败"
fi

# 测试 Tailscale 网络（直连，不经过代理）
echo ""
echo "🔍 测试 Tailscale 网络（直连）..."

# 测试 AGX Thor Ollama
if curl -s --connect-timeout 3 --noproxy '*' http://100.100.145.74:11434/api/tags > /dev/null 2>&1; then
    echo "✅ AGX Thor Ollama: 可访问"
else
    echo "⚠️  AGX Thor Ollama: 不可访问（可能是 Tailscale 未连接）"
fi

echo ""
echo "💡 提示："
echo "  - 外网和 GitHub 通过代理访问"
echo "  - LAN/Tailscale 网络直连（不经过代理）"
echo "  - 使用 'source scripts/clash-lan-config.sh' 加载配置"
echo ""
