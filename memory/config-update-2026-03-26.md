# OpenClaw 配置更新总结 — 2026-03-26

*更新时间：2026-03-26 13:35 北京时间*

---

## ✅ 已完成配置

### 1. 本地 Embedding (Memory Search)

**配置位置**: `agents.defaults.memorySearch`

```json5
{
  "enabled": true,
  "provider": "ollama",
  "model": "nomic-embed-text",
  "remote": {
    "baseUrl": "http://100.100.145.74:11434/api/embeddings",
    "apiKey": "ollama-local"
  }
}
```

**状态**: ✅ 配置完成，等待 AGX Thor 上 Ollama 服务响应

**说明**: 
- 使用 AGX Thor (100.100.145.74) 的 Ollama 服务
- 需要确保 Ollama 上有 `nomic-embed-text` 模型
- 如果模型不存在，需要运行 `ollama pull nomic-embed-text`

---

### 2. 多智能体路由 (Bindings)

**配置位置**: `bindings[]`

**当前绑定**:
```
coder <- feishu accountId=wanwan
```

**说明**:
- 婳婳 (coder) 绑定到飞书 wanwan 账号
- 所有 wanwan 账号的消息（包括私聊和群组）都会路由到婳婳
- 群组消息需要 @婳婳 才会响应（requireMention: true）

**CLI 管理**:
```bash
# 查看绑定
openclaw agents bindings

# 添加绑定
openclaw agents bind --agent coder --bind feishu:wanwan

# 移除绑定
openclaw agents unbind --agent coder --bind feishu:wanwan
```

---

### 3. Nodes (移动设备连接)

**配置位置**: `gateway.nodes`

**配置内容**:
```json5
{
  "allowCommands": [
    "canvas.*",
    "device.*",
    "notifications.*",
    "system.*",
    "camera.snap",
    "camera.clip"
  ],
  "denyCommands": [
    "screen.record",
    "contacts.add",
    "calendar.add",
    "reminders.add",
    "sms.send"
  ]
}
```

**状态**: ✅ 配置完成，等待设备配对

**当前状态**:
```
Known: 0 · Paired: 0 · Connected: 0
```

---

## 📱 手机连接步骤

### iOS / Android 设备连接流程：

1. **在手机上安装 OpenClaw Companion App**
   - iOS: App Store 搜索 "OpenClaw"
   - Android: Google Play 或 GitHub Releases 下载 APK

2. **获取 Gateway 连接信息**
   - Gateway 地址：需要配置远程访问（Tailscale 或公网 IP）
   - 端口：18789
   - Token: 在 `/openclaw_data/config/config.json` 的 `gateway.auth.token`

3. **在手机上连接**
   - 打开 App，输入 Gateway 地址和 Token
   - 或者扫描二维码（如果 Gateway 提供）

4. **在 Gateway 上批准配对**
   ```bash
   # 查看待批准的配对请求
   openclaw devices list
   
   # 批准配对
   openclaw devices approve <requestId>
   
   # 查看节点状态
   openclaw nodes status
   ```

5. **测试连接**
   ```bash
   # 查看节点详情
   openclaw nodes describe --node <id-or-name>
   
   # 调用节点命令
   openclaw nodes invoke --node <id> --command device.info
   ```

---

## ⚠️ 待处理事项

### 1. AGX Thor Ollama 服务检查
需要确认：
- Ollama 服务是否运行在 100.100.145.74:11434
- 是否有 `nomic-embed-text` 模型
- 网络是否可达（树莓派 → AGX Thor）

**测试命令**:
```bash
curl http://100.100.145.74:11434/api/tags
```

### 2. Gateway 远程访问配置
目前 Gateway 绑定在 loopback (127.0.0.1)，手机无法直接连接。

**解决方案**:
- **方案 A**: 使用 Tailscale（推荐）
  - 在树莓派上运行 Tailscale
  - 手机也安装 Tailscale
  - 通过 Tailscale IP 连接
  
- **方案 B**: 修改 Gateway 绑定地址
  ```json5
  gateway: {
    bind: "0.0.0.0"  // 监听所有接口
  }
  ```
  - 需要配置防火墙规则
  - 需要配置 `gateway.remote.token` 用于远程认证

### 3. 飞书插件权限
警告信息：`plugins.allow is empty`

**建议修复**:
```json5
plugins: {
  allow: ["feishu", "qwen-portal-auth", "google"]
}
```

---

## 📊 系统状态总览

| 项目 | 状态 | 备注 |
|------|------|------|
| OpenClaw 版本 | ✅ 2026.3.24 | 最新版 |
| Gateway | ✅ 正常运行 | port 18789 |
| 飞书集成 | ✅ 正常 | 5 个工具已加载 |
| 记忆搜索 | ⚠️ 配置完成，待测试 | 需要 Ollama embedding |
| 多智能体路由 | ✅ 已配置 | coder <- feishu:wanwan |
| Nodes | ✅ 配置完成 | 等待设备配对 |
| 远程访问 | ❌ 未配置 | 需要 Tailscale 或改绑定 |

---

## 🔧 配置文件备份

- 原始配置：`/openclaw_data/config/config.json.broken-2026-03-26`
- 升级前备份：`/openclaw_data/config/config.json.backup-2026-03-26`
- CLI 自动备份：`/openclaw_data/config/config.json.bak`

---

*下次检查：2026-04-02*
