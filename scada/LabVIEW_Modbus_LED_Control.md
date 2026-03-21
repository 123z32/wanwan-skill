# 💡 LabVIEW Modbus TCP LED + 光敏电阻控制

**版本**: 1.0  
**日期**: 2026-03-21  
**目标**: 使用 LabVIEW 2022 通过 Modbus TCP 控制树莓派 LED 和读取光敏电阻

---

## 📦 系统架构

```
┌──────────────────┐
│   上位机 (PC)     │  ← LabVIEW 2022 (Modbus TCP 主站)
│  LabVIEW 2022    │
│  NI Modbus Lib   │
└────────┬─────────┘
         │ 局域网 / Tailscale
         │ Modbus TCP (端口 502)
┌────────┴─────────┐
│   树莓派 5        │  ← Modbus TCP 从站
│  modbus_slave.py │
│  (端口 502)      │
└────────┬─────────┘
         │ HTTP (端口 5000)
┌────────┴─────────┐
│   宿主机服务      │  ← gpio_http_service.py
│  gpio_http_      │
│  service.py      │
└────────┬─────────┘
         │ GPIO
┌────────┴─────────┐
│   硬件            │
│  LED: GPIO 17    │  ← 输出
│  光敏电阻：GPIO 27│  ← 输入
└──────────────────┘
```

---

## 📋 Modbus 寄存器映射

### 从站信息
| 参数 | 值 |
|------|-----|
| **IP 地址** | `192.168.1.13` (局域网) 或 `100.93.35.112` (Tailscale) |
| **端口** | `5020` (标准 502 需要 root，开发用 5020) |
| **从站地址 (Unit ID)** | `1` |

### 寄存器表

#### 1️⃣ 线圈 (Coils) - 功能码 01/05/15

| 地址 | 名称 | 读写 | 说明 | 值 |
|------|------|------|------|-----|
| `0x0000` | LED_Control | 读写 | LED 控制 | `1`=ON, `0`=OFF |

**LabVIEW 操作**:
- 写线圈 `0x0000` = `True` → LED 打开
- 写线圈 `0x0000` = `False` → LED 关闭
- 读线圈 `0x0000` → 获取 LabVIEW 写入的值

---

#### 2️⃣ 离散输入 (Discrete Inputs) - 功能码 02

| 地址 | 名称 | 读写 | 说明 | 值 |
|------|------|------|------|-----|
| `0x0000` | LED_Status | 只读 | LED 实际状态 | `1`=ON, `0`=OFF |
| `0x0001` | Light_Status | 只读 | 光敏电阻状态 | `1`=亮，`0`=暗 |

**LabVIEW 操作**:
- 读离散输入 `0x0000` → LED 实际状态反馈
- 读离散输入 `0x0000-0x0001` → 同时读取 LED 和光敏电阻

---

#### 3️⃣ 保持寄存器 (Holding Registers) - 功能码 03/06/16

| 地址 | 名称 | 读写 | 说明 | 范围 |
|------|------|------|------|------|
| `0x0000` | Light_Value | 只读 | 光敏电阻原始值 | `0`=LOW, `1`=HIGH |
| `0x0001` | Uptime_Low | 只读 | 运行时间低 16 位 | 0-65535 秒 |

**LabVIEW 操作**:
- 读保持寄存器 `0x0000` → 光敏电阻值
- 读保持寄存器 `0x0000-0x0001` → 同时读取光敏电阻和运行时间

---

#### 4️⃣ 输入寄存器 (Input Registers) - 功能码 04

| 地址 | 名称 | 读写 | 说明 | 范围 |
|------|------|------|------|------|
| `0x0000` | Light_Value | 只读 | 光敏电阻原始值 | `0`=LOW, `1`=HIGH |
| `0x0001` | Uptime_Low | 只读 | 运行时间低 16 位 | 0-65535 秒 |

---

## 🖥️ LabVIEW 前面板设计

### 布局示意图

```
┌─────────────────────────────────────────────────────┐
│  Modbus TCP LED + 光敏电阻控制                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  连接配置                                    │   │
│  │  IP: [192.168.1.13]  端口：[502]            │   │
│  │  从站地址：[1]                               │   │
│  │  状态：[● 已连接]  [连接/断开]              │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  💡 LED 控制                                 │   │
│  │                                              │   │
│  │   [打开]  [关闭]  [切换]                    │   │
│  │                                              │   │
│  │   写入状态：[● ON / ○ OFF]                  │   │
│  │   反馈状态：[● ON / ○ OFF]                  │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  📊 光敏电阻传感器                           │   │
│  │                                              │   │
│  │   环境光：[☀️ 亮 / 🌙 暗]                   │   │
│  │   电平值：[1 / 0]                           │   │
│  │   GPIO 引脚：[27]                           │   │
│  │                                              │   │
│  │   [读取]  [自动刷新：✓]  间隔：[1] 秒       │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  📋 通信日志                                 │   │
│  │  [10:23:45] Modbus 连接成功                 │   │
│  │  [10:23:46] 写线圈 0x0000=1 → LED ON        │   │
│  │  [10:23:47] 读离散输入：LED=ON, 光=亮       │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 LabVIEW 前面板控件清单

### 连接配置
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `IP_Address` | String Control | "192.168.1.13" | 树莓派 IP |
| `Port` | Numeric Control (U16) | 5020 | Modbus 端口 (开发用) |
| `Slave_ID` | Numeric Control (U8) | 1 | 从站地址 |
| `Connection_Status` | Round LED | 红色 | 绿=已连接，红=断开 |
| `Connect_Button` | Push Button | - | 连接/断开 |
| `Connected?` | Boolean Indicator | False | 连接状态 |

### LED 控制
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `LED_On` | Push Button | - | 打开 LED |
| `LED_Off` | Push Button | - | 关闭 LED |
| `LED_Toggle` | Push Button | - | 切换状态 |
| `LED_Write_Status` | Round LED | 红色 | LabVIEW 写入的状态 |
| `LED_Read_Status` | Round LED | 红色 | 树莓派反馈的实际状态 |

### 光敏电阻
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `Light_State_Text` | String Indicator | "-" | "☀️ 亮" 或 "🌙 暗" |
| `Light_Value` | Numeric Indicator (U16) | 0 | 原始值 (0 或 1) |
| `GPIO_Pin` | Numeric Indicator | 27 | 引脚号 |
| `Read_Light_Button` | Push Button | - | 手动读取 |
| `Auto_Refresh` | Checkbox | True | 自动刷新 |
| `Refresh_Interval` | Numeric Control (DBL) | 1.0 | 刷新间隔 (秒) |

### 日志
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `Log_Display` | String Indicator | "" | 多行文本，显示通信日志 |

---

## 📊 LabVIEW 程序框图

### 主程序架构

```
┌──────────────────────────────────────────────┐
│ 初始化                                       │
│  ├─ 初始化 Modbus 连接引用 = None             │
│  ├─ 初始化 Connected = False                 │
│  └─ 初始化日志 = ""                          │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ While Loop (主循环)                          │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ Event Structure                        │ │
│  │                                        │ │
│  │ Event: Connect_Button                  │ │
│  │   └─ Case Structure (Connected?)       │ │
│  │       ├─ True → Modbus Close           │ │
│  │       └─ False → Modbus Open TCP       │ │
│  │           ├─ IP: IP_Address            │ │
│  │           ├─ Port: Port                │ │
│  │           └─ 成功 → Connected = True   │ │
│  │                                        │ │
│  │ Event: LED_On                          │ │
│  │   └─ Modbus Write Coil                 │ │
│  │       ├─ Coil Address: 0               │ │
│  │       ├─ Value: True                   │ │
│  │       └─ 更新 LED_Write_Status = ON    │ │
│  │                                        │ │
│  │ Event: LED_Off                         │ │
│  │   └─ Modbus Write Coil                 │ │
│  │       ├─ Coil Address: 0               │ │
│  │       ├─ Value: False                  │ │
│  │       └─ 更新 LED_Write_Status = OFF   │ │
│  │                                        │ │
│  │ Event: LED_Toggle                      │ │
│  │   └─ 读取当前线圈状态 → 取反 → 写入     │ │
│  │                                        │ │
│  │ Event: Read_Light_Button               │ │
│  │   └─ Modbus Read Discrete Inputs       │ │
│  │       ├─ Start Address: 0              │ │
│  │       ├─ Quantity: 2                   │ │
│  │       └─ 解析 [LED_Status, Light]      │ │
│  │                                        │ │
│  │ Event: Auto_Refresh (Value Change)     │ │
│  │   └─ 启动/停止定时循环                  │ │
│  │                                        │ │
│  │ Event: Timeout (100ms)                 │ │
│  │   └─ 如果 Auto_Refresh = True          │ │
│  │       └─ 读取离散输入 + 更新显示        │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  └─ 停止条件：Stop_Button                   │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ 清理                                         │
│  └─ 如果 Connected → Modbus Close           │
└──────────────────────────────────────────────┘
```

---

## 🔌 LabVIEW Modbus 函数使用

### 1️⃣ 连接 (Modbus Open TCP)

```labview
Modbus Open TCP.vi
├─ IP Address: IP_Address (String)
├─ Port: Port (U16, 默认 5020)
├─ Slave ID: Slave_ID (U8)
├─ Timeout: 1000 (ms)
└─ Modbus Refnum → 传递给后续 VI
```

### 2️⃣ 写单个线圈 (功能码 05)

```labview
Modbus Write Single Coil.vi
├─ Modbus Refnum: (from Modbus Open)
├─ Coil Address: 0 (U16)
├─ Value: True/False (Boolean)
└─ Error Out
```

### 3️⃣ 读多个线圈 (功能码 01)

```labview
Modbus Read Coils.vi
├─ Modbus Refnum: (from Modbus Open)
├─ Start Address: 0 (U16)
├─ Quantity: 1 (U16)
└─ Coil Status: [Boolean] (Array)
```

### 4️⃣ 读离散输入 (功能码 02)

```labview
Modbus Read Discrete Inputs.vi
├─ Modbus Refnum: (from Modbus Open)
├─ Start Address: 0 (U16)
├─ Quantity: 2 (U16)
└─ Input Status: [Boolean] (Array)
    ├─ [0]: LED 状态
    └─ [1]: 光敏电阻状态
```

### 5️⃣ 读保持寄存器 (功能码 03)

```labview
Modbus Read Holding Registers.vi
├─ Modbus Refnum: (from Modbus Open)
├─ Start Address: 0 (U16)
├─ Quantity: 2 (U16)
└─ Register Values: [U16] (Array)
    ├─ [0]: 光敏电阻值
    └─ [1]: 运行时间
```

### 6️⃣ 读输入寄存器 (功能码 04)

```labview
Modbus Read Input Registers.vi
├─ Modbus Refnum: (from Modbus Open)
├─ Start Address: 0 (U16)
├─ Quantity: 2 (U16)
└─ Register Values: [U16] (Array)
```

### 7️⃣ 断开连接 (Modbus Close)

```labview
Modbus Close.vi
├─ Modbus Refnum: (from Modbus Open)
└─ Error Out
```

---

## 📝 完整 VI 编程步骤

### 步骤 1: 创建主 VI

1. 打开 LabVIEW 2022
2. `File → New VI`
3. 保存为 `Modbus_LED_Control.vi`

### 步骤 2: 设计前面板

按照控件清单添加所有控件

### 步骤 3: 编写连接逻辑

```labview
Event: Connect_Button
└─ Case Structure (Connected?)
    ├─ True (断开):
    │   └─ Modbus Close.vi
    │       └─ Connected = False
    │       └─ Connection_Status = 红色
    │       └─ 日志："断开连接"
    │
    └─ False (连接):
        └─ Modbus Open TCP.vi
            ├─ IP: IP_Address
            ├─ Port: Port
            ├─ Slave ID: Slave_ID
            ├─ Timeout: 1000
            │
            └─ Case Structure (Error?)
                ├─ 无错误:
                │   ├─ Connected = True
                │   ├─ Connection_Status = 绿色
                │   └─ 日志："Modbus 连接成功"
                │
                └─ 有错误:
                    └─ 日志："连接失败：" + Error Message
```

### 步骤 4: 编写 LED 控制逻辑

```labview
Event: LED_On
└─ Case Structure (Connected?)
    ├─ True:
    │   └─ Modbus Write Single Coil.vi
    │       ├─ Coil Address: 0
    │       ├─ Value: True
    │       └─ Case Structure (Error?)
    │           ├─ 无错误:
    │           │   ├─ LED_Write_Status = ON (绿色)
    │           │   └─ 日志："写线圈 0x0000=1 → LED ON"
    │           │
    │           └─ 有错误:
    │               └─ 日志："写入失败：" + Error Message
    │
    └─ False:
        └─ 日志："未连接，无法控制 LED"

Event: LED_Off
└─ 类似 LED_On，Value = False

Event: LED_Toggle
└─ Case Structure (Connected?)
    ├─ True:
    │   ├─ Modbus Read Coils.vi (Address=0, Quantity=1)
    │   ├─ 读取当前状态 → current_state
    │   ├─ new_state = NOT current_state[0]
    │   └─ Modbus Write Single Coil.vi
    │       ├─ Coil Address: 0
    │       └─ Value: new_state
    │
    └─ False:
        └─ 日志："未连接"
```

### 步骤 5: 编写光敏电阻读取逻辑

```labview
Event: Read_Light_Button
└─ Case Structure (Connected?)
    ├─ True:
    │   ├─ Modbus Read Discrete Inputs.vi
    │   │   ├─ Start Address: 0
    │   │   └─ Quantity: 2
    │   │
    │   ├─ 解析结果:
    │   │   ├─ led_feedback = Input_Status[0]
    │   │   └─ light_value = Input_Status[1]
    │   │
    │   ├─ LED_Read_Status = led_feedback
    │   ├─ Light_Value = light_value
    │   │
    │   └─ Case Structure (light_value)
    │       ├─ 1 (亮):
    │       │   └─ Light_State_Text = "☀️ 亮"
    │       │
    │       └─ 0 (暗):
    │           └─ Light_State_Text = "🌙 暗"
    │
    └─ False:
        └─ 日志："未连接"

定时循环 (Auto_Refresh = True)
└─ 等待 Refresh_Interval 秒
└─ 执行读取逻辑 (同上)
```

### 步骤 6: 日志功能

```labview
子 VI: Add_Log.vi
├─ 输入：Message (String)
├─ 获取当前时间：Format Date/Time String ("%H:%M:%S")
├─ 格式化："[HH:MM:SS] " + Message + "\n"
└─ 追加：Log_Display = Log_Display + New_Line
```

---

## 🧪 测试步骤

### 1️⃣ 启动树莓派服务

```bash
# 在树莓派宿主机上
cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada

# 先启动 GPIO HTTP 服务
sudo python3 gpio_http_service.py &

# 再启动 Modbus 从站
python3 modbus_slave.py
```

### 2️⃣ LabVIEW 连接测试

1. 运行 `Modbus_LED_Control.vi`
2. IP 输入：`192.168.1.13`
3. 端口：`502`
4. 从站地址：`1`
5. 点击"连接"
6. 连接状态 LED 应变绿
7. 日志显示："Modbus 连接成功"

### 3️⃣ LED 控制测试

1. 点击"打开"按钮
2. LED 应亮起 (GPIO 17 输出高电平)
3. 写入状态 LED 变绿
4. 反馈状态 LED 也应变绿
5. 日志显示："写线圈 0x0000=1 → LED ON"
6. 点击"关闭"按钮
7. LED 应熄灭
8. 两个状态 LED 都变红

### 4️⃣ 光敏电阻测试

1. 勾选"自动刷新"
2. 光敏电阻状态应每秒更新
3. 用手遮挡光敏电阻
4. 状态应从"☀️ 亮"变为"🌙 暗"
5. Light_Value 应从 `1` 变为 `0`

### 5️⃣ 使用 modbus-cli 验证

```bash
# 安装
sudo apt-get install -y modbus-cli

# 读 LED 状态 (线圈)
modbus tcp 192.168.1.13 read coils 0 1

# 写 LED ON
modbus tcp 192.168.1.13 write coil 0 1

# 写 LED OFF
modbus tcp 192.168.1.13 write coil 0 0

# 读离散输入 (LED + 光敏电阻)
modbus tcp 192.168.1.13 read discrete 0 2

# 读保持寄存器 (光敏电阻值 + 运行时间)
modbus tcp 192.168.1.13 read holding 0 2
```

---

## 🔧 故障排查

### 问题 1: 连接失败

**检查**:
```bash
# 在树莓派上检查 Modbus 服务
netstat -tlnp | grep 502

# 检查防火墙
sudo ufw status

# 测试连接
telnet 192.168.1.13 502
```

**LabVIEW**:
- 确认 IP 地址正确
- 确认端口 502 未被占用
- 检查网络连接

### 问题 2: 写线圈无响应

**检查**:
```bash
# 查看 Modbus 从站日志
# 应该看到 "LabVIEW 写入线圈=1 → LED ON"

# 手动测试
curl -X POST http://localhost:5000/led/on
curl http://localhost:5000/led/status
```

### 问题 3: 光敏电阻读数不变

**检查**:
```bash
# 手动读取
curl http://localhost:5000/sensor/light

# 检查 GPIO 连接
gpioinfo

# 测试光敏电阻
# 用手电筒照射或遮挡，观察值是否变化
```

---

## 📚 LabVIEW Modbus 错误代码

| 错误代码 | 说明 | 解决 |
|---------|------|------|
| **538** | Transaction ID 不匹配 | 检查 Modbus 从站响应 |
| **539** | 超时 | 增加 Timeout 或检查网络 |
| **540** | 连接失败 | 检查 IP/端口/防火墙 |
| **541** | 从站无响应 | 检查从站是否运行 |
| **542** | 功能码不支持 | 检查功能码是否正确 |

---

## 💾 保存的文件

```
LabVIEW_Modbus_LED/
├── Modbus_LED_Control.vi        # 主程序
├── Modbus_Connect.vi            # 连接子 VI
├── LED_Control.vi               # LED 控制子 VI
├── Light_Sensor_Read.vi         # 光敏电阻读取子 VI
├── Add_Log.vi                   # 日志子 VI
└── Config.ini                   # 配置文件
```

---

## 🎯 快速参考

### LabVIEW Modbus 函数速查

| 功能 | VI 名称 | 参数 |
|------|--------|------|
| 连接 | `Modbus Open TCP` | IP, Port, Slave ID |
| 断开 | `Modbus Close` | Modbus Refnum |
| 写线圈 | `Modbus Write Single Coil` | Address=0, Value=True/False |
| 读线圈 | `Modbus Read Coils` | Address=0, Quantity=1 |
| 读离散输入 | `Modbus Read Discrete Inputs` | Address=0, Quantity=2 |
| 读寄存器 | `Modbus Read Holding Registers` | Address=0, Quantity=2 |

### 寄存器地址速查

| 功能 | 区域 | 地址 | 功能码 |
|------|------|------|--------|
| LED 控制 | 线圈 | 0x0000 | 05 |
| LED 状态 | 离散输入 | 0x0000 | 02 |
| 光敏电阻 | 离散输入 | 0x0001 | 02 |
| 光敏电阻 | 保持寄存器 | 0x0000 | 03 |
| 运行时间 | 保持寄存器 | 0x0001 | 03 |

---

## 📞 技术支持

有问题随时找绾绾～ 😊

---

*绾绾制作 · 2026-03-21*
