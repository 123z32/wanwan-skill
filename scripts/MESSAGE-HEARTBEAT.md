# 💓 消息心跳监控

## 功能
每 10 分钟检查是否有未回复的用户消息，如果有则提醒绾绾重新思考并回复。

## 配置
- **检查间隔**: 10 分钟
- **超时阈值**: 5 分钟（用户发消息后 5 分钟未回复则触发）
- **监控聊天**: 
  - 私聊：`oc_d77a50191711fcda0c3fab1a2d0e910c`
  - 群聊（张氏集团）: `oc_860db5e4fd90a53f2153619054abd26b`

## 使用方法

### 手动检查
```bash
cd /openclaw_data/.openclaw/workspace
node scripts/message-heartbeat.js --check
```

### 添加到 crontab（每 10 分钟）
```bash
crontab -e

# 每 10 分钟检查一次未回复消息
*/10 * * * * cd /openclaw_data/.openclaw/workspace && node scripts/message-heartbeat.js --check >> memory/message-heartbeat.log 2>&1
```

### 查看日志
```bash
tail -f memory/message-heartbeat.log
```

## 状态文件
`memory/message-heartbeat-state.json` - 记录最后检查时间和未回复消息计数

## 输出示例
```
[2026-03-25T18:10:00Z] === 消息心跳检查 ===
[2026-03-25T18:10:00Z] 检查聊天：oc_d77a50191711fcda0c3fab1a2d0e910c
[2026-03-25T18:10:01Z] 最后用户消息：2026-03-25T18:05:00Z (5 分钟前)
[2026-03-25T18:10:01Z] ✅ 所有消息已回复
```

或

```
[2026-03-25T18:10:00Z] === 消息心跳检查 ===
[2026-03-25T18:10:00Z] 检查聊天：oc_d77a50191711fcda0c3fab1a2d0e910c
[2026-03-25T18:10:01Z] 最后用户消息：2026-03-25T18:00:00Z (10 分钟前)
[2026-03-25T18:10:01Z] ⚠️ 发现未回复消息！聊天：oc_d77a50191711fcda0c3fab1a2d0e910c
[2026-03-25T18:10:01Z] 消息内容："RAG 费用呢"
[2026-03-25T18:10:01Z] 📢 已通知绾绾处理
```

## 注意事项
1. 需要飞书 API 权限（im:message, im:chat）
2. 首次运行会创建状态文件
3. 如果检测到未回复消息，会记录日志并通知主 agent
