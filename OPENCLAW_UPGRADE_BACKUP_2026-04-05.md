# OpenClaw 配置说明 - 故障恢复指南

**备份时间**: 2026-04-05 18:22 UTC  
**备份版本**: OpenClaw 2026.3.28  
**升级目标**: OpenClaw 2026.4.2  
**升级原因**: 用户要求升级到最新版本

---

## 📦 备份文件位置

### 配置文件备份
```
/home/node/.openclaw/openclaw.json.pre-upgrade-2026-04-05
```

### 工作区
```
/home/node/.openclaw/workspace/
├── MEMORY.md          # 长期记忆
├── SOUL.md            # 助手身份
├── USER.md            # 用户信息
├── HEARTBEAT.md       # 心跳任务
├── IDENTITY.md        # 身份配置
├── TOOLS.md           # 工具说明
└── memory/            # 日志目录
```

---

## 🔧 当前配置详情

### 1. 模型配置 (models)

**提供商**: Qwen (硅基流动/DashScope)
```json
{
  "providers": {
    "qwen": {
      "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
      "apiKey": "sk-sp-339124a42b8c469e96aeb7a20a9d3653",
      "api": "openai-completions",
      "models": [
        {
          "id": "qwen3.5-plus",
          "name": "Qwen 3.5 Plus",
          "contextWindow": 131072,
          "maxTokens": 32768
        }
      ]
    }
  }
}
```

**关键点**:
- 使用 DashScope 阿里云 API
- 模型：qwen3.5-plus
- 上下文窗口：131K tokens

---

### 2. 飞书渠道配置 (channels.feishu)

```json
{
  "feishu": {
    "enabled": true,
    "domain": "feishu",
    "connectionMode": "websocket",
    "webhookPath": "/feishu/events",
    "dmPolicy": "pairing",
    "groupPolicy": "open",
    "reactionNotifications": "own",
    "typingIndicator": true,
    "resolveSenderNames": true,
    "appId": "cli_a93b96d250391bd4",
    "appSecret": "v4Clks3h8xwSNUZoNARFoZCIgXS8vgq0"
  }
}
```

**关键点**:
- WebSocket 连接模式
- 私聊需要配对 (dmPolicy: "pairing")
- 群聊开放 (groupPolicy: "open")
- App ID: cli_a93b96d250391bd4
- App Secret: v4Clks3h8xwSNUZoNARFoZCIgXS8vgq0

---

### 3. 插件配置 (plugins)

**已安装插件**:
```json
{
  "feishu": {
    "source": "npm",
    "spec": "@m1heng-clawd/feishu",
    "installPath": "/home/node/.openclaw/extensions/feishu",
    "version": "0.1.19"
  }
}
```

---

### 4. 网关配置 (gateway)

```json
{
  "gateway": {
    "mode": "local"
  }
}
```

**模式**: 本地模式（非远程）

---

### 5. 浏览器配置 (browser)

```json
{
  "browser": {
    "enabled": true,
    "headless": true,
    "noSandbox": true,
    "color": "#FF4500",
    "cdpPortRangeStart": 18800
  }
}
```

**注意**: 2026.4.2 版本移除了 `cdpPortRangeEnd` 参数，只保留 `cdpPortRangeStart`

---

### 6. 智能体默认配置 (agents.defaults)

```json
{
  "workspace": "/home/node/.openclaw/workspace",
  "compaction": {
    "mode": "safeguard"
  }
}
```

---

## 🚨 升级后可能的问题

### 问题 1: 配置迁移失败
**症状**: Gateway 无法启动，报错配置格式错误  
**解决**:
```bash
openclaw doctor --fix
```

### 问题 2: 飞书插件不兼容
**症状**: 飞书消息无法收发  
**解决**:
```bash
# 重新安装飞书插件
cd /home/node/.openclaw/extensions/feishu
npm install @m1heng-clawd/feishu@latest
```

### 问题 3: 浏览器配置错误
**症状**: browser 工具超时  
**解决**:
```bash
# 编辑配置文件，确保只有 cdpPortRangeStart
# 删除任何 cdpPortRangeEnd 参数
```

### 问题 4: 模型配置路径变更
**症状**: API 调用失败  
**解决**:
检查 `models.providers` 路径是否仍然是核心配置
2026.4.2 可能迁移到 `plugins.entries.*.config`

---

## 🔧 恢复步骤

### 完全恢复流程

1. **停止 Gateway**
   ```bash
   pkill -f openclaw-gateway
   ```

2. **恢复配置文件**
   ```bash
   cp /home/node/.openclaw/openclaw.json.pre-upgrade-2026-04-05 /home/node/.openclaw/openclaw.json
   ```

3. **重新安装 OpenClaw（如需要）**
   ```bash
   npm install -g openclaw@2026.3.28
   ```

4. **启动 Gateway**
   ```bash
   cd /home/node/.openclaw
   openclaw gateway --port 18789 --verbose
   ```

5. **验证飞书连接**
   ```bash
   openclaw status
   ```

---

## 📝 重要文件清单

| 文件 | 用途 | 位置 |
|------|------|------|
| 配置文件 | OpenClaw 主配置 | `/home/node/.openclaw/openclaw.json` |
| 配置备份 | 升级前备份 | `/home/node/.openclaw/openclaw.json.pre-upgrade-2026-04-05` |
| 工作区 | 用户文件/记忆 | `/home/node/.openclaw/workspace/` |
| 飞书插件 | 飞书集成 | `/home/node/.openclaw/extensions/feishu/` |
| 日志 | 系统日志 | `/home/node/.openclaw/logs/` |

---

## 🆘 紧急联系方式

**用户**: 张  
**飞书 ID**: ou_ae328677b7d00c73ec3bff84e95ceb84  
**时区**: UTC+8 (中国标准时间)

---

## 💡 升级命令

```bash
# 1. 备份配置（已完成）
cp /home/node/.openclaw/openclaw.json /home/node/.openclaw/openclaw.json.pre-upgrade-2026-04-05

# 2. 升级 OpenClaw
npm install -g openclaw@latest

# 3. 运行配置迁移
openclaw doctor --fix

# 4. 重启 Gateway
pkill -f openclaw-gateway
openclaw gateway --port 18789 --verbose &

# 5. 验证
openclaw status
```

---

*最后更新：2026-04-05 18:22 UTC*  
*如果升级失败，请按照恢复步骤操作*
