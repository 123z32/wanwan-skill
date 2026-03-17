# 🏭 SCADA 系统 - 树莓派从站

**版本**: 1.0  
**日期**: 2026-03-17  
**作者**: 绾绾

---

## 📋 系统架构

```
┌──────────────────┐
│   监控层 (PC)     │  ← LabVIEW 2022 (Modbus TCP 主站)
│  LabVIEW 2022    │
└────────┬─────────┘
         │ Tailscale 虚拟局域网
         │ Modbus TCP (端口 502)
┌────────┴─────────┐
│   控制层 (树莓派)  │  ← SCADA 从站服务
│  树莓派 5         │
│  Ubuntu 24.04    │
└────────┬─────────┘
         │ GPIO + I2C
┌────────┴─────────┐
│   执行层          │
│  继电器 (GPIO2)   │  ← 高电平触发
│  AHT20 传感器     │  ← I2C (0x38)
│  LED 指示灯       │
└──────────────────┘
```

---

## 📦 安装步骤

### 1️⃣ 复制文件到树莓派

```bash
# 在你的电脑上
scp -r scada/ pi@树莓派IP:/tmp/

# 在树莓派上
sudo mv /tmp/scada /opt/scada
sudo chmod +x /opt/scada/install.sh
```

### 2️⃣ 运行安装脚本

```bash
cd /opt/scada
sudo ./install.sh
```

### 3️⃣ 重启树莓派

```bash
sudo reboot
```

### 4️⃣ 启动服务

```bash
sudo systemctl start scada-controller
sudo systemctl enable scada-controller  # 开机自启
```

### 5️⃣ 查看状态

```bash
sudo systemctl status scada-controller
sudo journalctl -u scada-controller -f  # 实时日志
```

---

## 🔌 硬件接线

### 继电器模块 (高电平触发)

| 继电器引脚 | 树莓派引脚 | GPIO 编号 | 说明 |
|-----------|-----------|----------|------|
| VCC | 物理引脚 4 | - | 5V 电源 |
| GND | 物理引脚 6 | - | 地 |
| IN | 物理引脚 3 | GPIO2 | 控制信号 |

### AHT20/BHT80 传感器 (I2C)

| 传感器引脚 | 树莓派引脚 | 说明 |
|-----------|-----------|------|
| VCC | 物理引脚 1 | 3.3V 电源 |
| GND | 物理引脚 9 | 地 |
| SDA | 物理引脚 3 | I2C 数据 (GPIO2) |
| SCL | 物理引脚 5 | I2C 时钟 (GPIO3) |

⚠️ **注意**：继电器和传感器都使用 GPIO2/3，可能需要调整引脚！

**建议方案**：
- 继电器改用 GPIO17 (物理引脚 11)
- 传感器保持 I2C (GPIO2/3)

修改 `scada_controller.py` 中的：
```python
RELAY_PIN = 17  # 改为 GPIO17
```

---

## 📡 Modbus TCP 地址映射

### 线圈 (Coils) - 读写

| 地址 | 名称 | 功能 | 值 |
|------|------|------|-----|
| 0x0000 | Relay_Control | 继电器控制 | 0=OFF, 1=ON |
| 0x0001 | Relay_Toggle | 继电器切换 | 0=无操作，1=切换 |

### 离散输入 (Discrete Inputs) - 只读

| 地址 | 名称 | 说明 |
|------|------|------|
| 0x0000 | Relay_Status | 继电器状态 (0=OFF, 1=ON) |

### 保持寄存器 (Holding Registers) - 读写

| 地址 | 名称 | 说明 | 范围 |
|------|------|------|------|
| 0x0000 | Temperature | 温度 (×100) | -5000~15000 (-50°C~150°C) |
| 0x0001 | Humidity | 湿度 (×100) | 0~10000 (0%~100%) |

**示例**：
- 温度 25.5°C → 寄存器值 2550
- 湿度 60.2% → 寄存器值 6020

---

## 🖥️ LabVIEW 连接示例

### 1️⃣ 安装 Modbus 库

使用 **NI Modbus Library** 或 **Datalogger Toolkit**

### 2️⃣ 连接配置

```
Protocol: Modbus TCP
IP Address: 100.93.35.112  (树莓派 Tailscale IP)
Port: 502
Slave ID: 1
```

### 3️⃣ 控制继电器 (写线圈)

```labview
Modbus Write Coil
├─ IP: 100.93.35.112
├─ Port: 502
├─ Slave ID: 1
├─ Address: 0
└─ Value: True/False
```

### 4️⃣ 读取传感器 (读寄存器)

```labview
Modbus Read Holding Registers
├─ IP: 100.93.35.112
├─ Port: 502
├─ Slave ID: 1
├─ Address: 0
├─ Quantity: 2
└─ Output: [温度×100, 湿度×100]
```

---

## 🧪 测试命令

### 使用 modbus-cli 测试

```bash
# 安装
sudo apt-get install -y modbus-cli

# 读取继电器状态
modbus tcp 100.93.35.112 read discrete 0 1

# 打开继电器
modbus tcp 100.93.35.112 write coil 0 1

# 关闭继电器
modbus tcp 100.93.35.112 write coil 0 0

# 读取温度
modbus tcp 100.93.35.112 read holding 0 1
# 输出除以 100 得到实际温度

# 读取湿度
modbus tcp 100.93.35.112 read holding 1 1
# 输出除以 100 得到实际湿度
```

### 使用 Python 测试

```python
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('100.93.35.112', port=502)
client.connect()

# 打开继电器
client.write_coil(0, True, slave=1)

# 读取温度
result = client.read_holding_registers(0, 1, slave=1)
temp = result.registers[0] / 100.0
print(f"温度：{temp}°C")

client.close()
```

---

## 📊 日志查看

```bash
# 实时日志
sudo journalctl -u scada-controller -f

# 最近 100 条
sudo journalctl -u scada-controller -n 100

# 查看特定时间
sudo journalctl -u scada-controller --since "2026-03-17 10:00:00"
```

---

## 🔧 故障排查

### 问题 1: 服务无法启动

```bash
# 查看详细错误
sudo journalctl -u scada-controller -n 50 --no-pager

# 检查端口占用
sudo netstat -tlnp | grep 502

# 手动运行测试
cd /opt/scada
sudo ./venv/bin/python3 scada_controller.py
```

### 问题 2: I2C 传感器无响应

```bash
# 检测 I2C 设备
sudo i2cdetect -y 1

# 应该看到 0x38 地址
```

### 问题 3: GPIO 权限问题

```bash
# 添加用户到 gpio 组
sudo usermod -a -G gpio $USER

# 重新登录
```

---

## 📝 待办事项

- [ ] 添加更多传感器支持 (光照、CO2 等)
- [ ] 实现数据记录到数据库
- [ ] 添加 Web 界面
- [ ] 实现报警功能 (温度/湿度阈值)
- [ ] 添加 MQTT 支持

---

## 📞 技术支持

有问题随时找绾绾～ 😊

---

*最后更新：2026-03-17*
