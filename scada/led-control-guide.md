# LED 控制指南

## 📖 概述

通过飞书消息控制树莓派 GPIO LED，架构与继电器控制完全相同。

## 🏗️ 架构

```
┌─────────────────┐      HTTP:5001      ┌─────────────────┐
│  OpenClaw 容器   │ ───────────────→   │  树莓派宿主机    │
│ feishu_led_control.py │                │ led_http_service.py │
│  (请求发送方)    │      100.93.35.112   │  (GPIO 控制方)    │
└─────────────────┘                     └─────────────────┘
```

## 🎯 飞书命令

| 消息 | 功能 |
|------|------|
| `打开 LED` | 打开 LED |
| `关闭 LED` | 关闭 LED |
| `切换 LED` | 切换状态 |
| `LED 状态` | 查看状态 |
| `LED 闪烁` | 闪烁 3 次 |
| `开灯` | 打开 LED |
| `关灯` | 关闭 LED |

## 🚀 启动服务

### 步骤 1：宿主机启动 LED 服务

在**树莓派宿主机**运行：

```bash
cd /openclaw_data/.openclaw/workspace/scada
sudo python3 led_http_service.py &
```

### 步骤 2：验证服务

```bash
curl http://localhost:5001/health
# 应返回：{"status":"ok","service":"led-http"}
```

### 步骤 3：测试控制

```bash
# 在容器内测试
python3 /openclaw_data/.openclaw/workspace/scada/feishu_led_control.py on
```

## 🔌 GPIO 接线

默认配置：
- **GPIO 芯片**: `gpiochip4`
- **GPIO 引脚**: `GPIO 27` (物理引脚 13)

如需修改，编辑 `led_http_service.py`:

```python
GPIO_CHIP = 4  # 芯片编号
GPIO_LINE = 27 # GPIO 引脚号
```

### 树莓派 GPIO 引脚图

```
GPIO 27 → 物理引脚 13 → LED 正极
GND     → 物理引脚 14 → LED 负极 (串联 220Ω电阻)
```

## 📝 与继电器控制的区别

| 项目 | 继电器 | LED |
|------|--------|-----|
| 服务端口 | 5000 | 5001 |
| GPIO 引脚 | GPIO 17 | GPIO 27 |
| 服务名 | `gpio_http_service.py` | `led_http_service.py` |
| 控制脚本 | `feishu_relay_control.py` | `feishu_led_control.py` |

## 🔧  systemd 服务（可选）

创建 `/etc/systemd/system/led-http.service`:

```ini
[Unit]
Description=LED HTTP Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /openclaw_data/.openclaw/workspace/scada/led_http_service.py
WorkingDirectory=/openclaw_data/.openclaw/workspace/scada
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

启用：
```bash
sudo systemctl enable led-http
sudo systemctl start led-http
sudo systemctl status led-http
```

## 🎨 扩展功能

可以添加：
- **呼吸灯效果** - PWM 调光
- **颜色控制** - RGB LED
- **定时任务** - 每天自动开关
- **传感器联动** - 光线暗自动开灯
