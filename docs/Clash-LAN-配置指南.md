# 🌐 Clash LAN 配置指南

*最后更新：2026-04-01*

---

## 📋 概述

本配置用于在 OpenClaw 容器内配置 Clash 代理和 LAN 访问。

**代理服务器**: `100.82.227.79:7890`（Tailscale 网络中的 Clash 节点）

**LAN 网段**: Tailscale 网络（100.64.0.0/10）直连，不经过代理

---

## 🚀 快速配置

### 方法 1: 临时配置（当前会话）

```bash
# 加载代理配置
export HTTP_PROXY=http://100.82.227.79:7890
export HTTPS_PROXY=http://100.82.227.79:7890
export NO_PROXY="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
```

### 方法 2: 使用配置脚本

```bash
# 加载配置
source /home/node/.openclaw/workspace/scripts/clash-lan-config.sh

# 或者
bash /home/node/.openclaw/workspace/scripts/clash-lan-config.sh
```

### 方法 3: 永久配置（添加到 bashrc）

```bash
# 添加到 ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# Clash LAN 代理配置
export HTTP_PROXY=http://100.82.227.79:7890
export HTTPS_PROXY=http://100.82.227.79:7890
export http_proxy=http://100.82.227.79:7890
export https_proxy=http://100.82.227.79:7890
export NO_PROXY="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
export no_proxy="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
EOF

# 重新加载
source ~/.bashrc
```

---

## ✅ 测试配置

```bash
# 测试外网访问（通过代理）
curl --proxy http://100.82.227.79:7890 https://www.google.com

# 测试 GitHub 访问（通过代理）
curl --proxy http://100.82.227.79:7890 https://api.github.com

# 测试 Tailscale 网络（直连）
curl --noproxy '*' http://100.100.145.74:11434/api/tags
```

---

## 🔧 OpenClaw 配置

### 配置 Git 使用代理

```bash
# Git HTTP 代理
git config --global http.proxy http://100.82.227.79:7890
git config --global https.proxy http://100.82.227.79:7890

# Git 对 LAN 不使用代理
git config --global http.100.64.0.0/10.proxy ""
git config --global http.100.100.0.0/16.proxy ""
```

### 配置 NPM 使用代理

```bash
npm config set proxy http://100.82.227.79:7890
npm config set https-proxy http://100.82.227.79:7890
npm config set strict-ssl false
```

### 配置 Pip 使用代理

```bash
# 创建 pip 配置
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
proxy = http://100.82.227.79:7890
index-url = https://pypi.org/simple
trusted-host = pypi.org
EOF
```

---

## 📊 网络架构

```
┌─────────────────────┐
│  OpenClaw 容器       │
│  (树莓派 5)         │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌──────────────┐
│ 外网     │ │ Tailscale    │
│ (代理)   │ │ LAN (直连)   │
│ :7890   │ │ 100.x.x.x    │
└─────────┘ └──────────────┘
    │               │
    ▼               ▼
┌─────────┐  ┌──────────────┐
│ GitHub  │  │ AGX Thor     │
│ Google  │  │ Ollama       │
└─────────┘  └──────────────┘
```

---

## 🎯 配置说明

### 代理服务器

| 配置项 | 值 |
|--------|-----|
| 地址 | 100.82.227.79 |
| 端口 | 7890 |
| 协议 | HTTP |
| 位置 | Tailscale 网络 |

### NO_PROXY（直连网段）

| 网段 | 用途 |
|------|------|
| 100.64.0.0/10 | Tailscale CGNAT |
| 100.100.0.0/16 | Tailscale 子网 |
| 10.0.0.0/8 | 内网 |
| 172.16.0.0/12 | 内网 |
| 192.168.0.0/16 | 内网 |
| localhost | 本地 |
| 127.0.0.1 | 本地 |

---

## 🛠️ 故障排查

### 问题 1: 代理不可用

**症状**: `curl --proxy http://100.82.227.79:7890 https://www.google.com` 超时

**排查步骤**:
```bash
# 1. 检查代理服务器是否在线
curl -I http://100.82.227.79:7890

# 2. 检查 Tailscale 连接
tailscale status

# 3. 测试其他代理节点
# (如果有多个 Clash 节点)
```

**解决方案**:
```bash
# 重启 Clash（在宿主机上）
systemctl restart clash

# 或者切换到其他代理节点
```

---

### 问题 2: LAN 无法直连

**症状**: 访问 Tailscale 设备时经过代理导致失败

**排查步骤**:
```bash
# 检查 NO_PROXY 配置
echo $NO_PROXY

# 测试直连
curl --noproxy '*' http://100.100.145.74:11434
```

**解决方案**:
```bash
# 确保 NO_PROXY 包含 Tailscale 网段
export NO_PROXY="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
```

---

### 问题 3: Git 推送失败

**症状**: `git push` 超时或失败

**排查步骤**:
```bash
# 检查 Git 代理配置
git config --global --get http.proxy
git config --global --get https.proxy

# 测试 Git 连接
curl --proxy http://100.82.227.79:7890 https://api.github.com
```

**解决方案**:
```bash
# 重新配置 Git 代理
git config --global http.proxy http://100.82.227.79:7890
git config --global https.proxy http://100.82.227.79:7890

# 或者临时禁用代理
git -c http.proxy= -c https.proxy= push
```

---

## 📝 环境变量参考

```bash
# 基本代理配置
export HTTP_PROXY=http://100.82.227.79:7890
export HTTPS_PROXY=http://100.82.227.79:7890
export http_proxy=http://100.82.227.79:7890
export https_proxy=http://100.82.227.79:7890

# LAN 直连配置
export NO_PROXY="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
export no_proxy="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"

# 完整配置（复制粘贴用）
export HTTP_PROXY=http://100.82.227.79:7890
export HTTPS_PROXY=http://100.82.227.79:7890
export http_proxy=http://100.82.227.79:7890
export https_proxy=http://100.82.227.79:7890
export NO_PROXY="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
export no_proxy="100.64.0.0/10,100.100.0.0/16,localhost,127.0.0.1"
```

---

## 🔒 安全注意事项

1. **代理服务器位置**: 代理服务器在 Tailscale 私有网络中，外部不可访问
2. **认证**: 当前配置无需认证（基于 Tailscale 身份验证）
3. **加密**: HTTPS 流量端到端加密，代理仅转发

---

## 📞 支持

- **详细文档**: `docs/自动恢复系统配置.md`
- **GitHub 仓库**: https://github.com/123z32/wanwan-skill
- **Tailscale 文档**: https://tailscale.com/kb/

---

*维护者：绾绾*
*最后更新：2026-04-01*
