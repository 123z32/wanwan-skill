# 💡 LabVIEW LED + 光敏电阻控制程序

**版本**: 2.0  
**日期**: 2026-03-21  
**目标**: 使用 LabVIEW 2022 控制树莓派 LED (GPIO 17) 和读取光敏电阻 (GPIO 27)

---

## 📦 前置要求

### 1️⃣ 安装 LabVIEW Modbus 库

**推荐**: NI Modbus Library
- 下载：https://www.ni.com/docs/
- 支持：Modbus TCP/IP

**备选**: LAVA 开源库
- https://forums.ni.com/t5/LAVA/Modbus-Library/ta-p/3519936

### 2️⃣ 确认树莓派服务运行

```bash
# 在树莓派宿主机上检查
sudo systemctl status gpio_http_service
# 或手动运行
cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada
sudo python3 gpio_http_service.py &
```

**服务地址**: `http://192.168.1.13:5000`

---

## 🖥️ 前面板设计

### 布局示意图

```
┌─────────────────────────────────────────────────────┐
│  SCADA 监控系统 - LED & 光敏电阻控制                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  连接状态                                    │   │
│  │  IP: [192.168.1.13]  端口：[5000]           │   │
│  │  状态：[● 已连接]  [刷新]                   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  💡 LED 控制                                 │   │
│  │                                              │   │
│  │   [打开]  [关闭]  [切换]  [闪烁]            │   │
│  │                                              │   │
│  │   状态指示：[● ON / ○ OFF]                  │   │
│  │   闪烁次数：[3]  间隔 (秒): [0.5]           │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  📊 光敏电阻传感器                           │   │
│  │                                              │   │
│  │   环境光：[☀️ 亮 / 🌙 暗]                   │   │
│  │   电平值：[HIGH / LOW]                      │   │
│  │   GPIO 引脚：[27]                           │   │
│  │                                              │   │
│  │   [读取]  [自动刷新：✓]  刷新间隔：[1] 秒   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  📋 操作日志                                 │   │
│  │  [10:23:45] 连接成功                        │   │
│  │  [10:23:46] LED: ON                         │   │
│  │  [10:23:47] 光敏电阻：亮 (HIGH)             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 前面板控件清单

### 连接部分
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| IP_Address | String Control | "192.168.1.13" | 树莓派 IP |
| Port | Numeric Control | 5000 | HTTP 端口 |
| Connection_Status | Round LED | 红色 | 绿=已连接，红=断开 |
| Connect_Button | Push Button | - | 连接/断开 |
| Refresh_Button | Push Button | - | 刷新状态 |

### LED 控制部分
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| LED_On | Push Button | - | 打开 LED |
| LED_Off | Push Button | - | 关闭 LED |
| LED_Toggle | Push Button | - | 切换状态 |
| LED_Blink | Push Button | - | 闪烁 |
| LED_Status | Round LED | 红色 | 绿=ON，红=OFF |
| Blink_Count | Numeric Control | 3 | 闪烁次数 |
| Blink_Interval | Numeric Control | 0.5 | 闪烁间隔 (秒) |

### 光敏电阻部分
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| Light_State | String Indicator | "-" | ☀️ 亮 / 🌙 暗 |
| Light_Level | String Indicator | "-" | HIGH / LOW |
| GPIO_Pin | Numeric Indicator | 27 | 引脚号 |
| Read_Button | Push Button | - | 手动读取 |
| Auto_Refresh | Checkbox | True | 自动刷新 |
| Refresh_Interval | Numeric Control | 1 | 刷新间隔 (秒) |

### 日志部分
| 控件名称 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| Log_Display | String Indicator | "" | 多行文本显示日志 |

---

## 📊 程序框图结构

### 主程序架构

```
┌──────────────────────────────────────────────┐
│ 初始化 (Flat Sequence Structure - Frame 0)   │
│  └─ 初始化变量                               │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ While Loop (主循环)                          │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ Event Structure                        │ │
│  │  ├─ Connect_Button → HTTP 连接测试     │ │
│  │  ├─ LED_On → POST /led/on              │ │
│  │  ├─ LED_Off → POST /led/off            │ │
│  │  ├─ LED_Toggle → POST /led/toggle      │ │
│  │  ├─ LED_Blink → POST /led/pulse        │ │
│  │  ├─ Read_Button → GET /sensor/light    │ │
│  │  └─ Refresh_Button → 刷新所有状态      │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 条件循环 (自动刷新光敏电阻)             │ │
│  │  ├─ 检查 Auto_Refresh = True?          │ │
│  │  ├─ 等待 Refresh_Interval 秒            │ │
│  │  ├─ GET /sensor/light                  │ │
│  │  └─ 更新前面板                         │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ 日志更新                               │ │
│  │  └─ 追加新日志到 Log_Display           │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  └─ 等待 (100ms) - 防止 CPU 占用过高         │
└──────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────┐
│ 清理 (Flat Sequence Structure - Frame 1)     │
│  └─ 关闭 HTTP 连接                           │
└──────────────────────────────────────────────┘
```

---

## 🔌 HTTP 请求实现

### 使用 LabVIEW Web 服务 VI

#### 1️⃣ 连接测试 (GET /health)

```labview
HTTP Client
├─ URL: "http://" + IP_Address + ":" + Port + "/health"
├─ Method: GET
├─ Timeout: 5000ms
└─ Response → 解析 JSON
    └─ 如果 status = "ok" → 连接成功
```

#### 2️⃣ LED 控制 (POST)

```labview
HTTP Client
├─ URL: "http://" + IP_Address + ":" + Port + "/led/on"
├─ Method: POST
├─ Timeout: 5000ms
└─ Response → 解析 JSON
    ├─ 如果 success = true → 更新 LED_Status = ON
    └─ 添加日志："LED: ON"
```

**各动作 URL**:
| 动作 | URL | 方法 |
|------|-----|------|
| 打开 | `/led/on` | POST |
| 关闭 | `/led/off` | POST |
| 切换 | `/led/toggle` | POST |
| 闪烁 | `/led/pulse` | POST |
| 状态 | `/led/status` | GET |

#### 3️⃣ 读取光敏电阻 (GET)

```labview
HTTP Client
├─ URL: "http://" + IP_Address + ":" + Port + "/sensor/light"
├─ Method: GET
├─ Timeout: 5000ms
└─ Response → 解析 JSON
    ├─ value = 1 → Light_State = "☀️ 亮", Light_Level = "HIGH"
    └─ value = 0 → Light_State = "🌙 暗", Light_Level = "LOW"
```

---

## 📝 JSON 解析实现

### 使用 LabVIEW JSON 解析 VI

#### 响应解析模板

```labview
JSON Text → JSON Parse.vi → Variant
    ↓
Variant to Data (转换为 Cluster)
    ├─ success: Boolean
    ├─ state: String (可选)
    ├─ value: U8 (可选)
    └─ error: String (可选)
```

#### 示例代码结构

```
HTTP Response String
    ↓
JSON Parse.vi
    ↓
Unflatten from JSON.vi
    ↓
Cluster: {success: Bool, state: String, value: U8}
    ↓
Case Structure (根据 success)
    ├─ True → 更新前面板
    └─ False → 显示错误日志
```

---

## 🎯 完整 VI 编程步骤

### 步骤 1: 创建主 VI

1. 打开 LabVIEW 2022
2. `File → New VI`
3. 保存为 `LED_Light_Control.vi`

### 步骤 2: 设计前面板

按照上面的控件清单添加所有控件

### 步骤 3: 编写连接逻辑

```labview
Event: Connect_Button
└─ HTTP GET "http://{IP}:{Port}/health"
    ├─ 成功 → Connection_Status = 绿色
    ├─ 失败 → Connection_Status = 红色
    └─ 添加日志
```

### 步骤 4: 编写 LED 控制逻辑

```labview
Event: LED_On
└─ HTTP POST "http://{IP}:{Port}/led/on"
    ├─ 成功 → LED_Status = 绿色
    └─ 添加日志："LED: ON"

Event: LED_Off
└─ HTTP POST "http://{IP}:{Port}/led/off"
    ├─ 成功 → LED_Status = 红色
    └─ 添加日志："LED: OFF"

Event: LED_Toggle
└─ HTTP POST "http://{IP}:{Port}/led/toggle"
    ├─ 解析 response.state
    └─ 更新 LED_Status

Event: LED_Blink
└─ 构建 JSON: {"count": Blink_Count, "interval": Blink_Interval}
└─ HTTP POST "http://{IP}:{Port}/led/pulse"
    └─ 添加日志："LED 闪烁 {count} 次"
```

### 步骤 5: 编写光敏电阻读取逻辑

```labview
Event: Read_Button
└─ HTTP GET "http://{IP}:{Port}/sensor/light"
    ├─ 解析 response.value
    ├─ value = 1 → Light_State = "☀️ 亮", Light_Level = "HIGH"
    └─ value = 0 → Light_State = "🌙 暗", Light_Level = "LOW"

定时循环 (Auto_Refresh = True 时)
└─ 等待 Refresh_Interval 秒
└─ 执行读取逻辑
```

### 步骤 6: 日志功能

```labview
添加日志子 VI
├─ 输入：消息字符串
├─ 获取当前时间 (Format Date/Time String)
├─ 格式："[HH:MM:SS] 消息"
└─ 追加到 Log_Display (使用连接字符串)
```

---

## 💾 保存的文件结构

```
LabVIEW_LED_Control/
├── LED_Light_Control.vi       # 主程序
├── HTTP_Request.vi            # HTTP 请求子 VI
├── JSON_Parse_Response.vi     # JSON 解析子 VI
├── Add_Log.vi                 # 日志添加子 VI
├── LED_Control_Panel.ctl      # LED 控制面板类型定义
├── Sensor_Display.ctl         # 传感器显示类型定义
└── Config.ini                 # 配置文件
```

---

## 🧪 测试步骤

### 1️⃣ 连接测试

1. 运行树莓派 GPIO 服务
2. 在 LabVIEW 中输入 IP: `192.168.1.13`
3. 点击"连接"
4. 连接状态 LED 应变绿
5. 日志显示："连接成功"

### 2️⃣ LED 控制测试

1. 点击"打开"按钮
2. LED 应亮起 (GPIO 17 输出高电平)
3. 状态指示变绿
4. 日志显示："LED: ON"
5. 点击"关闭"按钮
6. LED 应熄灭
7. 状态指示变红

### 3️⃣ 光敏电阻测试

1. 点击"读取"按钮
2. 显示当前环境光状态
3. 用手遮挡光敏电阻
4. 再次读取，状态应从"亮"变为"暗"

### 4️⃣ 自动刷新测试

1. 勾选"自动刷新"
2. 观察光敏电阻值是否每秒更新
3. 改变环境光（开灯/关灯）
4. 确认显示实时更新

---

## 🔧 故障排查

### 问题 1: 连接失败

**检查**:
```bash
# 在树莓派上检查服务
curl http://localhost:5000/health

# 检查防火墙
sudo ufw status
```

**LabVIEW 测试**:
- 使用简单 HTTP GET VI 测试连接
- 确认 IP 和端口正确

### 问题 2: LED 无响应

**检查**:
```bash
# 手动测试 API
curl -X POST http://192.168.1.13:5000/led/on
curl http://192.168.1.13:5000/led/status
```

### 问题 3: 光敏电阻读数不变

**检查**:
```bash
# 手动读取
curl http://192.168.1.13:5000/sensor/light

# 检查 GPIO 连接
gpioinfo
```

---

## 📚 LabVIEW 关键 VI 参考

### HTTP 相关
- `HTTP Client.vi` - 发送 HTTP 请求
- `HTTP Open Connection.vi` - 打开连接
- `HTTP Close Connection.vi` - 关闭连接

### JSON 相关
- `JSON Parse.vi` - 解析 JSON 字符串
- `Unflatten from JSON.vi` - 转换为 LabVIEW 数据类型

### 字符串相关
- `Format Date/Time String.vi` - 格式化时间
- `Concatenate Strings.vi` - 连接字符串

---

## 🎨 界面美化建议

1. **使用 Tab 控件** 分组功能
2. **添加图标** 使界面更直观
3. **使用颜色** 区分状态 (绿=正常，红=异常)
4. **添加提示** 鼠标悬停显示帮助信息
5. **使用本地变量** 避免数据竞争

---

## 📞 技术支持

有问题随时找绾绾～ 😊

---

*绾绾制作 · 2026-03-21*
