# 🔧 LabVIEW 子 VI 代码示例

**用于 LED + 光敏电阻控制程序**

---

## 1️⃣ HTTP_Request.vi - HTTP 请求子 VI

### 前面板

**输入控件**:
- `URL` (String): HTTP 地址
- `Method` (Enum): GET, POST, PUT, DELETE
- `Request_Data` (String): JSON 数据 (POST 用)
- `Timeout_ms` (Numeric): 超时时间 (默认 5000)

**输出指示器**:
- `Response` (String): 响应内容
- `Status_Code` (Numeric): HTTP 状态码
- `Success` (Boolean): 是否成功
- `Error_Message` (String): 错误信息

### 程序框图

```
┌─────────────────────────────────────────────┐
│ Case Structure (Method)                     │
│                                             │
│ Case "GET":                                 │
│   HTTP Client.vi                            │
│   ├─ URL: URL                               │
│   ├─ Method: GET                            │
│   └─ Timeout: Timeout_ms                    │
│                                             │
│ Case "POST":                                │
│   HTTP Client.vi                            │
│   ├─ URL: URL                               │
│   ├─ Method: POST                           │
│   ├─ Request Data: Request_Data             │
│   └─ Timeout: Timeout_ms                    │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ 错误处理                                     │
│   ├─ 无错误 → Success = True                │
│   └─ 有错误 → Success = False, 提取错误消息  │
└─────────────────────────────────────────────┘
```

---

## 2️⃣ JSON_Parse_Response.vi - JSON 解析子 VI

### 前面板

**输入**:
- `JSON_String` (String): HTTP 响应

**输出**:
- `Success` (Boolean)
- `State` (String)
- `Value` (U8)
- `Error` (String)
- `Parse_Error` (Boolean)

### 程序框图

```
JSON_String
    ↓
Unflatten from JSON.vi
    ├─ Type: Cluster {success: Bool, state: String, value: U8, error: String}
    └─ Output: Parsed Cluster
    ↓
错误处理 Case Structure
    ├─ 解析成功 → Parse_Error = False
    │   └─ 输出各字段到对应指示器
    │
    └─ 解析失败 → Parse_Error = True
        └─ Error = "JSON 解析失败"
```

### 使用示例

```labview
HTTP_Request.vi (Response)
    ↓
JSON_Parse_Response.vi
    ↓
Case Structure (Success)
    ├─ True → 执行操作
    └─ False → 显示错误
```

---

## 3️⃣ Add_Log.vi - 日志添加子 VI

### 前面板

**输入**:
- `Message` (String): 日志内容
- `Current_Log` (String): 当前日志

**输出**:
- `New_Log` (String): 更新后的日志

### 程序框图

```
Get Date/Time in Seconds
    ↓
Format Date/Time String.vi
    └─ Format: "%H:%M:%S"
    ↓
Concatenate Strings.vi
    ├─ "[" + Time_String + "] "
    ├─ Message
    └─ End of Line
    ↓
Concatenate Strings.vi
    ├─ Current_Log
    ├─ End of Line
    └─ New_Line
    ↓
New_Log (输出)
```

### 使用示例

```labview
Add_Log.vi("LED: ON", Current_Log)
    ↓
New_Log → 绑定到 Log_Display
```

---

## 4️⃣ LED_Control.vi - LED 控制子 VI

### 前面板

**输入**:
- `IP_Address` (String)
- `Port` (Numeric)
- `Action` (Enum): On, Off, Toggle, Pulse
- `Blink_Count` (Numeric): 闪烁次数 (Pulse 用)
- `Blink_Interval` (Numeric): 闪烁间隔 (Pulse 用)

**输出**:
- `Success` (Boolean)
- `Message` (String)
- `LED_State` (Boolean): 当前 LED 状态

### 程序框图

```
┌─────────────────────────────────────────────┐
│ Case Structure (Action)                     │
│                                             │
│ Case "On":                                  │
│   URL = IP + ":" + Port + "/led/on"        │
│   HTTP_Request.vi (POST)                    │
│   ├─ 成功 → Message = "LED 已打开"          │
│   └─ LED_State = True                       │
│                                             │
│ Case "Off":                                 │
│   URL = IP + ":" + Port + "/led/off"       │
│   HTTP_Request.vi (POST)                    │
│   ├─ 成功 → Message = "LED 已关闭"          │
│   └─ LED_State = False                      │
│                                             │
│ Case "Toggle":                              │
│   URL = IP + ":" + Port + "/led/toggle"    │
│   HTTP_Request.vi (POST)                    │
│   ├─ 解析 JSON.state                        │
│   └─ LED_State = (state == "on")            │
│                                             │
│ Case "Pulse":                               │
│   URL = IP + ":" + Port + "/led/pulse"     │
│   构建 JSON: {"count": Blink_Count,         │
│               "interval": Blink_Interval}   │
│   HTTP_Request.vi (POST with JSON)          │
│   └─ Message = "LED 闪烁 {count} 次"         │
└─────────────────────────────────────────────┘
```

---

## 5️⃣ Light_Sensor_Read.vi - 光敏电阻读取子 VI

### 前面板

**输入**:
- `IP_Address` (String)
- `Port` (Numeric)

**输出**:
- `Success` (Boolean)
- `Light_State_Text` (String): "☀️ 亮" 或 "🌙 暗"
- `Light_Level_Text` (String): "HIGH" 或 "LOW"
- `GPIO_Pin` (Numeric): 引脚号
- `Raw_Value` (U8): 原始值 (0 或 1)

### 程序框图

```
构建 URL: IP + ":" + Port + "/sensor/light"
    ↓
HTTP_Request.vi (GET)
    ↓
JSON_Parse_Response.vi
    ├─ success → Success
    ├─ value → Raw_Value
    └─ 其他字段
    ↓
Case Structure (Raw_Value)
    ├─ 1 (HIGH):
    │   ├─ Light_State_Text = "☀️ 亮"
    │   └─ Light_Level_Text = "HIGH"
    │
    └─ 0 (LOW):
        ├─ Light_State_Text = "🌙 暗"
        └─ Light_Level_Text = "LOW"
```

---

## 6️⃣ Connection_Test.vi - 连接测试子 VI

### 前面板

**输入**:
- `IP_Address` (String)
- `Port` (Numeric)

**输出**:
- `Connected` (Boolean)
- `Service_Status` (String): "在线" 或 "离线"
- `Error_Message` (String)

### 程序框图

```
构建 URL: IP + ":" + Port + "/health"
    ↓
HTTP_Request.vi (GET)
    ↓
JSON_Parse_Response.vi
    ├─ 解析 response.status
    └─ 如果 status == "ok" → Connected = True
    ↓
Case Structure (Connected)
    ├─ True → Service_Status = "在线"
    └─ False → Service_Status = "离线" + Error_Message
```

---

## 📋 主 VI 完整代码结构

### LED_Light_Control.vi

```
┌─────────────────────────────────────────────┐
│ 初始化 (Sequence Structure - Frame 0)       │
│  ├─ 初始化日志 = ""                         │
│  ├─ 初始化连接状态 = False                  │
│  └─ 初始化 LED 状态 = False                  │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ While Loop (主循环)                         │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ Event Structure                      │  │
│  │                                      │  │
│  │ Event: Connect_Button                │  │
│  │   └─ Connection_Test.vi              │  │
│  │       ├─ 成功 → Connected = True     │  │
│  │       └─ Add_Log.vi("连接成功")      │  │
│  │                                      │  │
│  │ Event: LED_On                        │  │
│  │   └─ LED_Control.vi(Action=On)       │  │
│  │       └─ Add_Log.vi(Message)         │  │
│  │                                      │  │
│  │ Event: LED_Off                       │  │
│  │   └─ LED_Control.vi(Action=Off)      │  │
│  │       └─ Add_Log.vi(Message)         │  │
│  │                                      │  │
│  │ Event: LED_Toggle                    │  │
│  │   └─ LED_Control.vi(Action=Toggle)   │  │
│  │       └─ 更新 LED_Status             │  │
│  │                                      │  │
│  │ Event: LED_Blink                     │  │
│  │   └─ LED_Control.vi(Action=Pulse)    │  │
│  │       └─ Add_Log.vi(Message)         │  │
│  │                                      │  │
│  │ Event: Read_Button                   │  │
│  │   └─ Light_Sensor_Read.vi            │  │
│  │       └─ 更新光敏电阻显示             │  │
│  │                                      │  │
│  │ Event: Refresh_Button                │  │
│  │   └─ Connection_Test.vi +            │  │
│  │       Light_Sensor_Read.vi +         │  │
│  │       LED_Control.vi(Status)         │  │
│  │                                      │  │
│  │ Event: Auto_Refresh (Value Change)   │  │
│  │   └─ 启动/停止定时循环                │  │
│  │                                      │  │
│  │ Event: Timeout (100ms)               │  │
│  │   └─ 处理定时任务                     │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ 定时循环 (光敏电阻自动刷新)            │  │
│  │  ├─ 检查 Auto_Refresh = True?        │  │
│  │  ├─ 检查上次刷新时间                 │  │
│  │  ├─ 如果 间隔 >= Refresh_Interval    │  │
│  │  │   └─ Light_Sensor_Read.vi        │  │
│  │  │   └─ 更新上次刷新时间             │  │
│  │  └─ 等待 (100ms)                     │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  └─ 停止条件：Stop_Button                  │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ 清理 (Sequence Structure - Frame 1)         │
│  └─ Add_Log.vi("程序已退出")                │
└─────────────────────────────────────────────┘
```

---

## 🎨 类型定义 (.ctl 文件)

### LED_Control_Panel.ctl

```labview
Type Definition Cluster:
├─ IP_Address: String
├─ Port: U16
├─ Connected: Boolean
├─ LED_State: Boolean
├─ Blink_Count: U8
└─ Blink_Interval: DBL
```

### Sensor_Display.ctl

```labview
Type Definition Cluster:
├─ Light_State: String
├─ Light_Level: String
├─ GPIO_Pin: U8
├─ Auto_Refresh: Boolean
└─ Refresh_Interval: DBL
```

---

## 🧪 测试 VI

### Test_HTTP_Connection.vi

```labview
前面板:
├─ IP_Address: "192.168.1.13"
├─ Port: 5000
└─ Test_Button

程序框图:
Test_Button Event
    ↓
Connection_Test.vi
    ↓
显示结果 (Connected, Service_Status)
```

### Test_LED_Control.vi

```labview
前面板:
├─ IP_Address: "192.168.1.13"
├─ Port: 5000
├─ Action: Enum (On, Off, Toggle, Pulse)
├─ Test_Button
└─ Result: String

程序框图:
Test_Button Event
    ↓
LED_Control.vi
    ↓
显示结果 (Message, LED_State)
```

### Test_Light_Sensor.vi

```labview
前面板:
├─ IP_Address: "192.168.1.13"
├─ Port: 5000
├─ Read_Button
└─ Light_State: String

程序框图:
Read_Button Event
    ↓
Light_Sensor_Read.vi
    ↓
显示结果 (Light_State_Text, Light_Level_Text)
```

---

## 📞 技术支持

有问题随时找绾绾～ 😊

---

*绾绾制作 · 2026-03-21*
