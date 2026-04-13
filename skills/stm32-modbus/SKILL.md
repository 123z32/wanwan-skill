# STM32 Modbus 远程控制 Skill

通过飞书消息控制 STM32 外设。链路：飞书 → OpenClaw → 树莓派 TCP Server (8086) → ESP8266 透传 → STM32 → Modbus 外设。

## 触发条件

用户在飞书消息中提到以下关键词时激活：
- `STM32`
- `Modbus`
- `读取` / `控制` / `外设`
- `GPIO` / `寄存器` / `线圈`

## 可用命令

### 1. 读取线圈（Discrete Input / Coil）
```
读取 GPIO
读取线圈 0-15
读取继电器状态
```

### 2. 写入线圈（控制输出）
```
打开 GPIO 5
关闭 GPIO 3
打开继电器
关闭 LED
```

### 3. 读取寄存器（Holding Register）
```
读取寄存器 0
读取寄存器 0-3
读取 ADC 值
```

### 4. 写入寄存器
```
写入寄存器 0 值 100
设置 PWM 为 50%
```

### 5. 查看连接状态
```
STM32 状态
ESP8266 连接状态
```

## Modbus 协议帧格式

### 读线圈（Function Code 0x01）
```
地址(1) + FC(1) + 起始地址(2) + 数量(2) + CRC(2)
例：01 01 00 00 00 10 [CRC]  → 读取线圈 0-15
```

### 读离散输入（Function Code 0x02）
```
01 02 00 00 00 10 [CRC]  → 读取离散输入 0-15
```

### 读保持寄存器（Function Code 0x03）
```
01 03 00 00 00 01 [CRC]  → 读取寄存器 0
```

### 写单个线圈（Function Code 0x05）
```
01 05 00 00 FF 00 [CRC]  → 写线圈 0 = ON
01 05 00 00 00 00 [CRC]  → 写线圈 0 = OFF
```

### 写单个寄存器（Function Code 0x06）
```
01 06 00 00 00 64 [CRC]  → 写寄存器 0 = 100
```

## 执行流程

1. **解析用户意图** — 识别命令类型、地址、值
2. **构建 Modbus RTU 帧** — 包含 CRC16 校验
3. **通过 TCP 发送到树莓派** — 端口 8086
4. **等待 ESP8266 返回响应**
5. **解析响应并格式化输出**
6. **发送结果给用户**

## 脚本位置

- TCP 服务器：`scripts/modbus_tcp_server.py`（已在后台运行）
- Modbus 工具脚本：`scripts/modbus_client.py`

## CRC16 计算

Modbus RTU 使用 CRC16-Modbus (多项式 0xA001)：

```python
def calc_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc
```

## 注意事项

1. 树莓派和 ESP8266 必须在同一局域网
2. TCP Server 监听 8086 端口
3. 默认 Modbus 从站地址为 0x01
4. 超时时间 5 秒
5. 如果 ESP8266 未连接，提示用户检查 WiFi 连接
