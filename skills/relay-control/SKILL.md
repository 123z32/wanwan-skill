---
name: relay-control
description: |
  Control GPIO relay via Feishu messages. 
  Activate when user mentions 继电器 (relay), 打开 (turn on), 关闭 (turn off), 开关 (switch).
---

# 继电器控制技能

## 用途

通过飞书消息控制树莓派 GPIO 继电器。

## 命令

用户可以通过以下飞书消息控制：

- "打开继电器" → 打开
- "关闭继电器" → 关闭
- "切换继电器" → 切换状态
- "继电器状态" → 查看状态
- "开灯" → 打开（如果继电器控制灯）
- "关灯" → 关闭

## 实现

### 前置条件

1. **宿主机 GPIO 服务运行中**
   ```bash
   # 在树莓派宿主机上
   cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada
   sudo python3 gpio_http_service.py &
   ```

2. **容器内 Python 环境**
   ```bash
   # 在容器里
   apt-get update
   apt-get install -y python3 python3-pip python3-requests
   ```

### 工具调用

```json
{
  "action": "execute",
  "command": "python3 /mnt/ssd/openclaw_data/.openclaw/workspace/scada/feishu_relay_control.py on"
}
```

### 响应格式

成功：
```
✅ 继电器已打开
```

失败：
```
❌ 失败：无法连接到 GPIO 服务
```

## 安全限制

1. 只允许授权用户控制
2. 每次操作记录日志
3. 防止频繁切换（可添加延时保护）

## 扩展

可以添加：
- 定时任务（每天早上 8 点开灯）
- 温度联动（温度过高自动开风扇）
- 语音控制（通过飞书语音消息）
