# 🎨 LabVIEW 2022 SCADA 示例

**目标**: 在 LabVIEW 中创建简单的 SCADA 界面，控制树莓派继电器和读取温湿度

---

## 📦 前置要求

### 1️⃣ 安装 Modbus 库

**选项 A: NI Modbus Library** (推荐)
- 下载地址：NI 官网
- 支持：Modbus TCP/IP

**选项 B: Datalogger Toolkit**
- 包含 Modbus 功能
- 更强大但更复杂

**选项 C: 开源库**
- LAVA Modbus Library: https://forums.ni.com/t5/LAVA/Modbus-Library/ta-p/3519936

---

## 🖥️ 前面板设计

### 控件布局

```
┌─────────────────────────────────────────┐
│  SCADA 监控系统 - 树莓派继电器控制       │
├─────────────────────────────────────────┤
│                                         │
│  连接状态：[● 已连接]                   │
│  IP 地址：[100.93.35.112]  端口：[502]  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │     继电器控制                   │   │
│  │                                  │   │
│  │   [打开]  [关闭]  [切换]        │   │
│  │                                  │   │
│  │   状态：[● ON / ○ OFF]          │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │     温湿度传感器                 │   │
│  │                                  │   │
│  │   温度：[25.5] °C               │   │
│  │   湿度：[60.2] %                │   │
│  │                                  │   │
│  │   [刷新]  [自动更新：✓]         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │     日志                         │   │
│  │  [10:23:45] 连接成功            │   │
│  │  [10:23:46] 继电器：ON          │   │
│  │  [10:23:47] 温度：25.5°C        │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔧 VI 编程步骤

### 1️⃣ 创建主 VI

1. **新建 VI**: `File → New VI`
2. **保存为**: `SCADA_Main.vi`

### 2️⃣ 前面板控件

#### 连接部分
- **IP 地址**: String Control (默认值 "100.93.35.112")
- **端口**: Numeric Control (默认值 502)
- **连接状态**: Round LED (绿色=已连接，红色=断开)

#### 继电器控制
- **打开按钮**: Push Button
- **关闭按钮**: Push Button
- **切换按钮**: Push Button
- **状态指示**: Round LED 或 Text Indicator

#### 温湿度显示
- **温度**: Numeric Indicator (保留 2 位小数)
- **湿度**: Numeric Indicator (保留 2 位小数)
- **刷新按钮**: Push Button
- **自动更新**: Checkbox

#### 日志
- **日志显示**: String Indicator (多行)

### 3️⃣ 程序框图

#### 初始化连接

```
┌─────────────────┐
│ Modbus Open     │
│ TCP Client      │
└────────┬────────┘
         │
    Connection ID
```

#### 继电器控制逻辑

```labview
Event Structure
├─ Event: 打开按钮
│   └─ Modbus Write Coil (地址 0, 值 True)
│
├─ Event: 关闭按钮
│   └─ Modbus Write Coil (地址 0, 值 False)
│
└─ Event: 切换按钮
    └─ Modbus Write Coil (地址 1, 值 True)
```

#### 传感器读取循环

```
While Loop (1 秒间隔)
├─ Modbus Read Holding Registers
│   ├─ 地址：0
│   ├─ 数量：2
│   └─ 输出：[温度寄存器，湿度寄存器]
│
├─ 除以 100.0 (温度)
├─ 除以 100.0 (湿度)
│
├─ 绑定到前面板指示器
│
└─ 等待 (1000ms)
```

### 4️⃣ 完整代码结构

```
┌──────────────────────────────────────┐
│ 初始化 (Flat Sequence Structure)     │
│  └─ Modbus Open TCP Client           │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│ While Loop (主循环)                  │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ Event Structure                │ │
│  │  ├─ 打开按钮 → 写线圈 0        │ │
│  │  ├─ 关闭按钮 → 写线圈 1        │ │
│  │  └─ 切换按钮 → 写线圈 2        │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ 定时循环 (1 秒)                 │ │
│  │  ├─ 读保持寄存器 (地址 0,2)    │ │
│  │  ├─ 转换为温度/湿度            │ │
│  │  └─ 更新前面板                 │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ 日志更新                        │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│ 清理 (Flat Sequence Structure)       │
│  └─ Modbus Close                     │
└──────────────────────────────────────┘
```

---

## 📝 关键代码片段

### Modbus 写线圈 (控制继电器)

```labview
Modbus Write Coil.vi
├─ Connection ID: (from Modbus Open)
├─ Slave Address: 1
├─ Coil Address: 0
├─ Value: True/False
└─ Error Out
```

### Modbus 读寄存器 (传感器数据)

```labview
Modbus Read Holding Registers.vi
├─ Connection ID: (from Modbus Open)
├─ Slave Address: 1
├─ Starting Address: 0
├─ Quantity: 2
├─ Register Values: [Temp×100, Hum×100]
│
└─ Divide by 100.0 → Temperature (°C)
└─ Divide by 100.0 → Humidity (%)
```

---

## 🧪 测试步骤

### 1️⃣ 连接测试

1. 运行树莓派 SCADA 服务
2. 在 LabVIEW 中输入 IP: `100.93.35.112`
3. 点击"连接"
4. 连接状态 LED 应变绿

### 2️⃣ 继电器测试

1. 点击"打开"按钮
2. 继电器应吸合（听到"吧嗒"声）
3. 状态 LED 变绿
4. 点击"关闭"按钮
5. 继电器应释放

### 3️⃣ 传感器测试

1. 等待 1 秒（自动刷新）
2. 温度/湿度应显示当前值
3. 用手靠近传感器，温度应上升

---

## 💾 保存的 VI 文件

建议保存以下文件：

```
SCADA_LabVIEW/
├── SCADA_Main.vi          # 主程序
├── SCADA_Modbus_Init.vi   # Modbus 初始化子 VI
├── SCADA_Relay_Control.vi # 继电器控制子 VI
├── SCADA_Sensor_Read.vi   # 传感器读取子 VI
└── SCADA_Config.ini       # 配置文件 (IP、端口等)
```

---

## 🔧 故障排查

### 问题 1: 连接失败

**检查**:
- 树莓派 IP 是否正确
- 端口 502 是否开放
- 防火墙是否阻止

**测试**:
```bash
ping 100.93.35.112
telnet 100.93.35.112 502
```

### 问题 2: 读不到传感器数据

**检查**:
- 树莓派日志：`sudo journalctl -u scada-controller -f`
- I2C 检测：`sudo i2cdetect -y 1`

### 问题 3: 继电器无响应

**检查**:
- GPIO 引脚是否正确
- 继电器模块是否供电
- 接线是否牢固

---

## 📚 参考资源

- NI Modbus 文档：https://www.ni.com/docs/
- LAVA 论坛：https://forums.ni.com/t5/LAVA/bd-p/220
- Modbus 协议：https://modbus.org/

---

*绾绾制作 · 2026-03-17*
