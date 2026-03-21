---
name: relay-control
description: |
  Control GPIO LED and light sensor via Feishu messages. 
  Activate when user mentions LED, 灯，光敏电阻，打开 (turn on), 关闭 (turn off), 开关 (switch).
---

# LED 控制技能

## 用途

通过飞书消息控制树莓派 GPIO LED，并读取光敏电阻状态。

## 硬件配置

| 组件 | GPIO 引脚 | 类型 |
|------|----------|------|
| LED | GPIO 17 | 输出 |
| 光敏电阻 | GPIO 27 | 输入 |

## 命令

用户可以通过以下飞书消息控制：

### LED 控制
- "打开 LED" / "开灯" → 打开
- "关闭 LED" / "关灯" → 关闭
- "切换 LED" → 切换状态
- "LED 状态" → 查看状态
- "LED 闪烁" → 闪烁 3 次

### 光敏电阻读取
- "光敏电阻" / "光线强度" / "读取光敏" → 读取环境光状态

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

**LED 控制成功**：
```
💡 LED 已打开
```

**光敏电阻读取成功**：
```
📊 光敏电阻 (GPIO 27): ☀️ 亮 (HIGH)
```

**失败**：
```
❌ 失败：无法连接到 GPIO 服务
```

## API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/led/on` | POST | 打开 LED |
| `/led/off` | POST | 关闭 LED |
| `/led/toggle` | POST | 切换状态 |
| `/led/status` | GET | 获取状态 |
| `/led/pulse` | POST | 闪烁 |
| `/sensor/light` | GET | 读取光敏电阻 |

## 安全限制

1. 只允许授权用户控制
2. 每次操作记录日志
3. 防止频繁切换（可添加延时保护）

## 扩展

可以添加：
- 自动模式（天黑自动开灯）
- 定时任务（每天早上 8 点开灯）
- 亮度阈值调节
- 语音控制（通过飞书语音消息）
