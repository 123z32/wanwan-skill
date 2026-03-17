# 🔌 树莓派继电器控制操作流程

**版本**: 1.0  
**日期**: 2026-03-17  
**适用系统**: 树莓派 5 + Ubuntu 24.04  
**硬件**: 继电器模块 (高电平触发) + 物理引脚 11 (GPIO17)

---

## 📋 目录

1. [硬件准备](#1-硬件准备)
2. [系统要求](#2-系统要求)
3. [快速测试](#3-快速测试)
4. [HTTP 服务部署](#4-http-服务部署)
5. [API 使用指南](#5-api-使用指南)
6. [开机自启](#6-开机自启)
7. [故障排查](#7-故障排查)

---

## 1. 硬件准备

### 1.1 所需材料

| 材料 | 数量 | 说明 |
|------|------|------|
| 树莓派 5 | 1 | Ubuntu 24.04 系统 |
| 继电器模块 | 1 | 高电平触发，5V |
| 杜邦线 | 3 | 母对母 |
| LED 灯 + 电阻 | 1 套 | 可选，用于测试 |

### 1.2 接线图

```
继电器模块          树莓派 5
-----------          ----------
VCC        ──────→   物理引脚 2 (5V)
GND        ──────→   物理引脚 6 (GND)
IN         ──────→   物理引脚 11 (GPIO17)
```

### 1.3 接线步骤

1. **断电** - 拔掉树莓派电源
2. **接 VCC** - 继电器 VCC → 树莓派 物理引脚 2 (红色线)
3. **接 GND** - 继电器 GND → 树莓派 物理引脚 6 (黑色线)
4. **接 IN** - 继电器 IN → 树莓派 物理引脚 11 (黄色线)
5. **检查** - 确认接线牢固
6. **通电** - 插上树莓派电源

---

## 2. 系统要求

### 2.1 系统检查

```bash
# 检查系统版本
cat /etc/os-release
# 应该显示 Ubuntu 24.04 或 Debian 12

# 检查树莓派型号
cat /proc/device-tree/model
# 应该显示 Raspberry Pi 5 Model B

# 检查 GPIO 设备
ls -la /dev/gpiochip*
# 应该显示 gpiochip0-4
```

### 2.2 确认 GPIO 映射

```bash
# 查看 GPIO 信息
sudo gpioinfo | grep -A 2 "GPIO17"

# 应该看到:
# gpiochip4 - 54 lines:
#   line  17:     "GPIO17"       unused   input  active-high
```

如果 `gpioinfo` 命令不存在：

```bash
sudo apt-get update
sudo apt-get install -y gpiod
```

---

## 3. 快速测试

### 3.1 方法一：使用 periphery 库（推荐）

```bash
# 1. 安装依赖
sudo apt-get update
sudo apt-get install -y python3-periphery

# 2. 创建测试脚本
cat > /tmp/relay_test.py << 'EOF'
#!/usr/bin/env python3
from periphery import GPIO
import time

print("初始化 GPIO17...")
relay = GPIO("/dev/gpiochip4", 17, "out")

print("打开继电器 (3 秒)...")
relay.write(True)
time.sleep(3)

print("关闭继电器...")
relay.write(False)
time.sleep(1)

relay.close()
print("测试完成！")
EOF

# 3. 运行测试
sudo python3 /tmp/relay_test.py
```

**预期输出**:
```
初始化 GPIO17...
打开继电器 (3 秒)...
关闭继电器...
测试完成！
```

应该能听到继电器"吧嗒"声。

### 3.2 方法二：使用 sysfs 接口

```bash
# 1. 导出 GPIO
echo 17 > /sys/class/gpio/export 2>/dev/null || true

# 2. 设置为输出模式
echo out > /sys/class/gpio/gpio17/direction

# 3. 打开继电器
echo 1 > /sys/class/gpio/gpio17/value
echo "继电器已打开"

# 4. 等待 3 秒
sleep 3

# 5. 关闭继电器
echo 0 > /sys/class/gpio/gpio17/value
echo "继电器已关闭"

# 6. 清理
echo 17 > /sys/class/gpio/unexport
```

### 3.3 方法三：使用命令行工具

```bash
# 安装 gpiod
sudo apt-get install -y gpiod

# 设置 GPIO17 为输出模式
sudo gpioctl set-output --consumer=myrelay gpiochip4 17

# 打开继电器
sudo gpioctl set gpiochip4 17

# 关闭继电器
sudo gpioctl clear gpiochip4 17

# 查看状态
sudo gpioctl get gpiochip4 17
```

---

## 4. HTTP 服务部署

### 4.1 为什么使用 HTTP 服务？

**优点**:
- ✅ 可以从容器、远程电脑、手机控制
- ✅ 不需要给每个程序 GPIO 权限
- ✅ 支持多用户并发访问
- ✅ 可以添加认证、日志、限流等功能
- ✅ 易于集成到现有系统

### 4.2 安装依赖

```bash
cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada

# 安装 Flask
sudo apt-get update
sudo apt-get install -y python3-flask python3-requests
```

### 4.3 启动服务

```bash
# 方法一：前台运行（测试用）
sudo python3 gpio_http_service.py

# 方法二：后台运行（生产环境）
sudo nohup python3 gpio_http_service.py > /tmp/gpio_service.log 2>&1 &

# 方法三：使用 systemd（推荐）
sudo systemctl enable gpio-service
sudo systemctl start gpio-service
```

### 4.4 验证服务

```bash
# 健康检查
curl http://localhost:5000/health

# 应该返回:
# {"service":"gpio-http","status":"ok"}

# 查看状态
curl http://localhost:5000/relay/status

# 打开继电器
curl -X POST http://localhost:5000/relay/on

# 关闭继电器
curl -X POST http://localhost:5000/relay/off
```

### 4.5 查看日志

```bash
# 实时日志
tail -f /tmp/gpio_service.log

# 或者使用 journalctl（如果用 systemd）
sudo journalctl -u gpio-service -f
```

---

## 5. API 使用指南

### 5.1 API 端点

| 端点 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/health` | GET | 健康检查 | 无 |
| `/relay/on` | POST | 打开继电器 | 无 |
| `/relay/off` | POST | 关闭继电器 | 无 |
| `/relay/toggle` | POST | 切换状态 | 无 |
| `/relay/status` | GET | 获取状态 | 无 |
| `/relay/pulse` | POST | 脉冲输出 | `count`, `interval` |

### 5.2 使用示例

#### 5.2.1 使用 curl

```bash
# 打开继电器
curl -X POST http://100.93.35.112:5000/relay/on

# 关闭继电器
curl -X POST http://100.93.35.112:5000/relay/off

# 切换状态
curl -X POST http://100.93.35.112:5000/relay/toggle

# 查看状态
curl http://100.93.35.112:5000/relay/status

# 脉冲输出（闪烁 5 次，每次 0.5 秒）
curl -X POST http://100.93.35.112:5000/relay/pulse \
  -H "Content-Type: application/json" \
  -d '{"count": 5, "interval": 0.5}'
```

#### 5.2.2 使用 Python

```python
import requests

BASE_URL = "http://100.93.35.112:5000"

# 打开继电器
requests.post(f"{BASE_URL}/relay/on")

# 关闭继电器
requests.post(f"{BASE_URL}/relay/off")

# 获取状态
r = requests.get(f"{BASE_URL}/relay/status")
print(f"继电器状态：{r.json()['state']}")

# 脉冲输出
requests.post(f"{BASE_URL}/relay/pulse", json={
    "count": 3,
    "interval": 0.5
})
```

#### 5.2.3 使用 Node.js

```javascript
const axios = require('axios');

const BASE_URL = 'http://100.93.35.112:5000';

// 打开继电器
axios.post(`${BASE_URL}/relay/on`);

// 切换状态
axios.post(`${BASE_URL}/relay/toggle`)
  .then(res => console.log(res.data));

// 获取状态
axios.get(`${BASE_URL}/relay/status`)
  .then(res => console.log(`状态：${res.data.state}`));
```

#### 5.2.4 使用 Postman

1. **新建请求**
   - Method: POST
   - URL: `http://100.93.35.112:5000/relay/on`

2. **发送请求**
   - 点击 "Send"
   - 查看响应

3. **保存为 Collection**
   - 添加到 "Relay Control" 集合
   - 方便重复使用

---

## 6. 开机自启

### 6.1 创建 systemd 服务

```bash
# 创建服务文件
sudo nano /etc/systemd/system/gpio-service.service
```

**服务内容**:
```ini
[Unit]
Description=GPIO HTTP Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/mnt/ssd/openclaw_data/.openclaw/workspace/scada
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/usr/bin/python3 /mnt/ssd/openclaw_data/.openclaw/workspace/scada/gpio_http_service.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=gpio-service

[Install]
WantedBy=multi-user.target
```

### 6.2 启用服务

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable gpio-service

# 启动服务
sudo systemctl start gpio-service

# 查看状态
sudo systemctl status gpio-service
```

### 6.3 管理命令

```bash
# 启动
sudo systemctl start gpio-service

# 停止
sudo systemctl stop gpio-service

# 重启
sudo systemctl restart gpio-service

# 查看日志
sudo journalctl -u gpio-service -f

# 禁用开机自启
sudo systemctl disable gpio-service
```

---

## 7. 故障排查

### 7.1 继电器无反应

**症状**: 运行脚本但继电器不动作

**检查步骤**:
```bash
# 1. 检查接线
# - 确认 VCC 接 5V
# - 确认 GND 接地
# - 确认 IN 接 GPIO17

# 2. 检查 GPIO 输出
sudo gpioctl get gpiochip4 17

# 3. 手动控制测试
echo 17 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio17/direction
echo 1 > /sys/class/gpio/gpio17/value  # 应该听到"吧嗒"声

# 4. 检查继电器类型
# - 高电平触发：GPIO 输出 HIGH 时吸合
# - 低电平触发：GPIO 输出 LOW 时吸合
```

### 7.2 HTTP 服务无法启动

**症状**: `sudo systemctl start gpio-service` 失败

**检查步骤**:
```bash
# 1. 查看详细错误
sudo journalctl -u gpio-service -n 50 --no-pager

# 2. 检查端口占用
sudo netstat -tlnp | grep 5000

# 3. 手动运行测试
cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada
sudo python3 gpio_http_service.py

# 4. 检查依赖
python3 -c "import flask; print(flask.__version__)"

# 5. 重新安装依赖
sudo apt-get install --reinstall python3-flask
```

### 7.3 API 请求超时

**症状**: `curl http://localhost:5000/health` 超时

**检查步骤**:
```bash
# 1. 检查服务是否运行
sudo systemctl status gpio-service

# 2. 检查防火墙
sudo ufw status
sudo ufw allow 5000/tcp

# 3. 检查网络监听
sudo netstat -tlnp | grep 5000

# 4. 本地测试
curl http://127.0.0.1:5000/health

# 5. 查看日志
tail -f /tmp/gpio_service.log
```

### 7.4 GPIO 权限错误

**症状**: `Permission denied` 或 `Exporting GPIO: Invalid argument`

**解决方案**:
```bash
# 方法 1: 使用 sudo
sudo python3 gpio_http_service.py

# 方法 2: 添加用户到 gpio 组
sudo usermod -a -G gpio $USER
# 需要重新登录

# 方法 3: 使用 udev 规则
echo 'KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"' | \
  sudo tee /etc/udev/rules.d/99-gpio.rules
sudo udevadm control --reload-rules
```

### 7.5 常见问题 FAQ

**Q: 继电器一直响怎么办？**  
A: 检查代码逻辑，避免频繁切换。可以添加延时保护：
```python
time.sleep(1)  # 两次操作间隔至少 1 秒
```

**Q: 可以控制多个继电器吗？**  
A: 可以，修改代码添加更多 GPIO 引脚：
```python
RELAY_1 = 17  # GPIO17
RELAY_2 = 27  # GPIO27
```

**Q: 如何添加密码保护？**  
A: 在 Flask 中添加认证中间件：
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    return username == "admin" and password == "your_password"

@app.route('/relay/on', methods=['POST'])
@auth.login_required
def relay_on():
    ...
```

---

## 8. 安全注意事项

### 8.1 电气安全

⚠️ **警告**:
- 继电器控制强电时，确保弱电/强电隔离
- 不要超过继电器额定电流/电压
- 接线时务必断电操作
- 使用合适的保险丝

### 8.2 网络安全

- 不要将 GPIO 服务暴露在公网
- 使用防火墙限制访问 IP
- 添加认证机制
- 定期更新系统和依赖

### 8.3 代码安全

- 验证所有输入参数
- 限制请求频率
- 记录所有操作日志
- 添加异常处理

---

## 9. 进阶应用

### 9.1 定时任务

```bash
# 每天早上 8 点打开继电器
crontab -e

# 添加:
0 8 * * * curl -X POST http://localhost:5000/relay/on

# 每天晚上 6 点关闭
0 18 * * * curl -X POST http://localhost:5000/relay/off
```

### 9.2 温度联动

```python
# 温度超过 30°C 自动开风扇
while True:
    temp = read_temperature()  # 读取温度传感器
    if temp > 30:
        requests.post("http://localhost:5000/relay/on")
    else:
        requests.post("http://localhost:5000/relay/off")
    time.sleep(60)  # 每分钟检查一次
```

### 9.3 Web 界面

使用 Flask + HTML 创建简单的 Web 控制界面：

```python
@app.route('/')
def index():
    return '''
    <html>
      <h1>继电器控制</h1>
      <button onclick="fetch('/relay/on', {method:'POST'})">打开</button>
      <button onclick="fetch('/relay/off', {method:'POST'})">关闭</button>
    </html>
    '''
```

---

## 10. 参考资源

- [树莓派 GPIO 文档](https://www.raspberrypi.org/documentation/usage/gpio/)
- [Ubuntu for Raspberry Pi](https://ubuntu.com/raspberry-pi)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [periphery 库文档](https://github.com/vsergeev/python-periphery)
- [Modbus 协议规范](https://modbus.org/)

---

## 11. 联系支持

遇到问题？

- 📧 邮件：支持@example.com
- 💬 飞书：联系绾绾
- 📚 文档：`/mnt/ssd/openclaw_data/.openclaw/workspace/scada/README.md`

---

*最后更新：2026-03-17*  
*版本：1.0*
