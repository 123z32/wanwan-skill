# 💓 心跳监控 Cron 设置指南

## 📋 已创建文件

```
/openclaw_data/.openclaw/workspace/scripts/
├── message-heartbeat.js          # 监控脚本
├── message-heartbeat.service     # systemd 服务
├── message-heartbeat.timer       # systemd 定时器（每 10 分钟）
└── SETUP-CRON.md                 # 本文件
```

---

## 🚀 设置方法（2 选 1）

### 方法 1：systemd 定时器（推荐 ⭐⭐⭐⭐⭐）

**在宿主机（树莓派）执行**：

```bash
# 1. 复制文件到 systemd 目录
sudo cp /openclaw_data/.openclaw/workspace/scripts/message-heartbeat.* /etc/systemd/system/

# 2. 重新加载 systemd
sudo systemctl daemon-reload

# 3. 启用并启动定时器
sudo systemctl enable message-heartbeat.timer
sudo systemctl start message-heartbeat.timer

# 4. 验证状态
sudo systemctl list-timers | grep message-heartbeat
sudo systemctl status message-heartbeat.timer
```

**预期输出**：
```
NEXT                        LEFT          LAST                        PASSED       UNIT                         SERVICE
Thu 2026-03-26 10:30:00 UTC 5min left     Thu 2026-03-26 10:20:00 UTC 2min ago     message-heartbeat.timer      message-heartbeat.service
```

---

### 方法 2：传统 crontab

**在宿主机（树莓派）执行**：

```bash
# 编辑 crontab
crontab -e

# 添加以下行：
*/10 * * * * cd /openclaw_data/.openclaw/workspace && node scripts/message-heartbeat.js --check >> memory/message-heartbeat.log 2>&1

# 保存退出
# 验证
crontab -l
```

---

## 📊 验证

### 检查定时器状态
```bash
sudo systemctl list-timers | grep message-heartbeat
```

### 查看日志
```bash
tail -f /openclaw_data/.openclaw/workspace/memory/message-heartbeat.log
```

### 手动测试
```bash
cd /openclaw_data/.openclaw/workspace
node scripts/message-heartbeat.js --check
```

---

## 📝 日志示例

```
[2026-03-26T02:50:00Z] === 消息心跳检查 ===
[2026-03-26T02:50:01Z] 检查聊天：oc_d77a50191711fcda0c3fab1a2d0e910c
[2026-03-26T02:50:01Z] 最后用户消息：2026-03-26T02:45:00Z (5 分钟前)
[2026-03-26T02:50:01Z] ✅ 所有消息已回复
```

或

```
[2026-03-26T03:00:00Z] === 消息心跳检查 ===
[2026-03-26T03:00:01Z] 检查聊天：oc_d77a50191711fcda0c3fab1a2d0e910c
[2026-03-26T03:00:01Z] 最后用户消息：2026-03-26T02:50:00Z (10 分钟前)
[2026-03-26T03:00:01Z] ⚠️ 发现未回复消息！
[2026-03-26T03:00:01Z] 消息内容："RAG 系统如何"
[2026-03-26T03:00:01Z] 📢 已通知绾绾处理
```

---

## ⚠️ 注意事项

### 容器 vs 宿主机

**重要**：cron 需要在**宿主机**（树莓派）上设置，不是在容器内！

**原因**：
- 容器可能重启，cron 会丢失
- 宿主机 cron 更稳定
- 容器内可能没有 cron 服务

### 执行方式

**如果脚本需要在容器内运行**：

```bash
# crontab 改为：
*/10 * * * * docker exec openclaw node /openclaw_data/.openclaw/workspace/scripts/message-heartbeat.js --check >> /openclaw_data/.openclaw/workspace/memory/message-heartbeat.log 2>&1
```

---

## 🔧 故障排除

### 定时器未运行
```bash
# 检查状态
sudo systemctl status message-heartbeat.timer

# 查看日志
journalctl -u message-heartbeat.service -n 20
```

### 脚本执行失败
```bash
# 手动测试
node /openclaw_data/.openclaw/workspace/scripts/message-heartbeat.js --check

# 检查 node 路径
which node
# 输出：/usr/bin/node 或 /usr/local/bin/node
```

### 权限问题
```bash
# 确保脚本可执行
chmod +x /openclaw_data/.openclaw/workspace/scripts/message-heartbeat.js

# 确保日志文件可写
touch /openclaw_data/.openclaw/workspace/memory/message-heartbeat.log
chmod 666 /openclaw_data/.openclaw/workspace/memory/message-heartbeat.log
```

---

## ✅ 完成检查清单

- [ ] 选择设置方法（systemd 或 crontab）
- [ ] 在宿主机执行设置命令
- [ ] 验证定时器状态
- [ ] 手动测试脚本
- [ ] 检查日志输出
- [ ] 等待 10 分钟，确认自动执行

---

*设置完成后，系统将每 10 分钟自动检查未回复消息！* 🚀
