# Modbus TCP 协议完整指南

*基于树莓派 SCADA 系统实战经验总结*

---

## 📖 目录

1. [Modbus TCP 协议基础](#1-modbus-tcp-协议基础)
2. [帧结构详解](#2-帧结构详解)
3. [时序要求](#3-时序要求)
4. [常用功能码](#4-常用功能码)
5. [LabVIEW 集成](#5-labview-集成)
6. [常见问题与解决](#6-常见问题与解决)

---

## 1. Modbus TCP 协议基础

### 1.1 什么是 Modbus TCP

Modbus TCP 是 Modbus 协议在 TCP/IP 网络上的实现，用于工业自动化系统中的主从通信。

| 特性 | 说明 |
|------|------|
| **传输层** | TCP/IP (端口 502 标准) |
| **架构** | 主从 (Master/Slave) |
| **连接** | 面向连接 (TCP 三次握手) |
| **应用** | PLC、SCADA、传感器、执行器 |

### 1.2 核心概念

| 术语 | 说明 |
|------|------|
| **Master (主站)** | 发起请求的设备 (如 LabVIEW、上位机) |
| **Slave (从站)** | 响应请求的设备 (如树莓派、PLC) |
| **Transaction ID** | 事务标识符，匹配请求和响应 |
| **Function Code** | 功能码，指定操作类型 |
| **Coil** | 线圈，1 位布尔量 (可读可写) |
| **Discrete Input** | 离散输入，1 位布尔量 (只读) |
| **Holding Register** | 保持寄存器，16 位整数 (可读可写) |
| **Input Register** | 输入寄存器，16 位整数 (只读) |

---

## 2. 帧结构详解

### 2.1 Modbus TCP 帧格式

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Transaction │   Protocol  │   Length    │   Unit ID   │
│    ID       │     ID      │             │  (Slave ID) │
│  (2 bytes)  │  (2 bytes)  │  (2 bytes)  │  (1 byte)   │
├─────────────┴─────────────┴─────────────┴─────────────┤
│                    Function Code                       │
│                      (1 byte)                          │
├───────────────────────────────────────────────────────┤
│                         Data                          │
│                    (N bytes)                          │
└───────────────────────────────────────────────────────┘
```

### 2.2 各字段说明

| 字段 | 长度 | 说明 |
|------|------|------|
| **Transaction ID** | 2 字节 | 事务标识符，请求和响应必须一致 |
| **Protocol ID** | 2 字节 | 固定为 `0x0000` (Modbus) |
| **Length** | 2 字节 | 后续字节数 (Unit ID + FC + Data) |
| **Unit ID** | 1 字节 | 从站地址 (通常 0-247) |
| **Function Code** | 1 字节 | 功能码 (如 01/02/03/05/06/15/16) |
| **Data** | N 字节 | 功能码相关数据 |

### 2.3 示例：读线圈请求

```
请求：00 01 00 00 00 06 00 01 00 00 00 01
      │  │  │  │  │  │  │  │  │  │  │  │
      │  │  │  │  │  │  │  │  │  │  │  └─ 数量 (1 个)
      │  │  │  │  │  │  │  │  │  │  └──── 起始地址 (0)
      │  │  │  │  │  │  │  │  │  └─────── 功能码 (01=读线圈)
      │  │  │  │  │  │  │  │  └────────── 单元 ID (0)
      │  │  │  │  │  │  │  └───────────── 长度 (6 字节)
      │  │  │  │  │  │  └──────────────── 协议 ID (0000)
      │  │  │  │  │  └─────────────────── 事务 ID (1)
      │  │  │  │  └─────────────────────── (高位)

响应：00 01 00 00 00 04 00 01 01 01
      │  │  │  │  │  │  │  │  │  └─ 数据 (00000001 = 线圈 0=ON)
      │  │  │  │  │  │  │  │  └──── 字节数 (1 字节)
      │  │  │  │  │  │  │  └─────── 功能码 (01)
      │  │  │  │  │  │  └────────── 单元 ID (0)
      │  │  │  │  │  └───────────── 长度 (4 字节)
      │  │  │  │  └──────────────── 协议 ID (0000)
      │  │  │  └─────────────────── 事务 ID (1, 必须与请求一致!)
```

---

## 3. 时序要求 ⚠️

### 3.1 Transaction ID 匹配 (最关键!)

**规则**: 响应的 Transaction ID 必须与请求完全一致

```python
# 请求
trans_id = 0x0001
# 响应必须使用相同的 trans_id
response[0:2] = trans_id.to_bytes(2, 'big')  # ✅ 正确

# 错误示例
response[0:2] = 0x0000  # ❌ LabVIEW 报错：Transaction ID mismatch
```

**LabVIEW 错误 538**: `Response Transaction ID doesn't match Request`

### 3.2 响应超时

| 设备 | 典型超时 |
|------|---------|
| LabVIEW | 1000ms - 5000ms |
| Python pymodbus | 3000ms |
| 工业 PLC | 500ms - 2000ms |

**建议**: 从站响应时间 < 100ms

### 3.3 连接管理

```
Master                          Slave
  │                              │
  │──── SYN ────────────────────▶│  TCP 连接建立
  │◀─── SYN/ACK ─────────────────│
  │──── ACK ────────────────────▶│
  │                              │
  │──── Modbus Request ─────────▶│
  │◀─── Modbus Response ─────────│  必须配对
  │                              │
  │──── Modbus Request ─────────▶│
  │◀─── Modbus Response ─────────│
  │                              │
  │──── FIN ────────────────────▶│  连接关闭
```

### 3.4 3.5 字符静默时间 (RTU 特有)

**注意**: Modbus TCP **不需要** 3.5 字符静默时间，这是 RTU 的要求。

---

## 4. 常用功能码

### 4.1 位操作 (Coils/Discrete Inputs)

| 功能码 | 名称 | 用途 | 数据方向 |
|--------|------|------|---------|
| `0x01` | Read Coils | 读线圈状态 | Slave → Master |
| `0x02` | Read Discrete Inputs | 读离散输入 | Slave → Master |
| `0x05` | Write Single Coil | 写单个线圈 | Master → Slave |
| `0x0F` | Write Multiple Coils | 写多个线圈 | Master → Slave |

### 4.2 寄存器操作 (Holding/Input Registers)

| 功能码 | 名称 | 用途 | 数据方向 |
|--------|------|------|---------|
| `0x03` | Read Holding Registers | 读保持寄存器 | Slave → Master |
| `0x04` | Read Input Registers | 读输入寄存器 | Slave → Master |
| `0x06` | Write Single Register | 写单个寄存器 | Master → Slave |
| `0x10` | Write Multiple Registers | 写多个寄存器 | Master → Slave |

### 4.3 功能码 05: 写单个线圈

```
请求：00 01 00 00 00 06 00 05 00 00 FF 00
                              │  │  │  │
                              │  │  │  └─ 值 (0xFF00=ON, 0x0000=OFF)
                              │  │  └──── 线圈地址 (0)
                              │  └─────── 功能码 (05)
                              └────────── 单元 ID (0)

响应：00 01 00 00 00 04 00 05 00 00 FF 00
      (原样返回请求，确认写入)
```

### 4.4 功能码 16: 写多个寄存器

```
请求：00 01 00 00 00 09 00 10 00 00 00 01 02 00 01
                              │  │  │  │  │  │  └─ 值 (0x0001)
                              │  │  │  │  │  └──── 字节数 (2)
                              │  │  │  │  └─────── 数量 (1 个)
                              │  │  │  └─────────── 起始地址 (0)
                              │  │  └────────────── 功能码 (16=0x10)
                              │  └───────────────── 单元 ID (0)

响应：00 01 00 00 00 04 00 10 00 00 00 01
      (确认写入的地址和数量)
```

---

## 5. LabVIEW 集成

### 5.1 Modbus Library 配置

| 参数 | 建议值 | 说明 |
|------|--------|------|
| **IP Address** | 树莓派 IP | 如 `100.93.35.112` |
| **Port** | `5020` | 标准 502 需要 root |
| **Slave ID** | `0` 或 `1` | 必须与从站一致 |
| **Timeout** | `1000ms` | 超时时间 |
| **Function** | `03/06/16` | 根据需求选择 |

### 5.2 典型 LabVIEW 流程

```
1. Create TCP Connection (一次性)
        ↓
2. While Loop (持续运行)
   ├─ Write Register (控制)
   ├─ Read Register (状态反馈)
   └─ Wait (100ms)
        ↓
3. Close Connection (退出时)
```

### 5.3 常见 LabVIEW 错误

| 错误代码 | 原因 | 解决 |
|---------|------|------|
| **538** | Transaction ID 不匹配 | 检查响应构建 |
| **539** | 超时 | 增加超时时间或优化从站响应 |
| **540** | 连接失败 | 检查 IP/端口/防火墙 |

---

## 6. 常见问题与解决

### 6.1 Transaction ID 不匹配

**症状**: LabVIEW 报错 538

**原因**: 响应的事务 ID 与请求不一致

**解决**:
```python
# 从请求中提取
trans_id = int.from_bytes(data[0:2], 'big')

# 原样放入响应
response[0:2] = trans_id.to_bytes(2, 'big')
```

### 6.2 长度字段错误

**症状**: 响应被拒绝或解析失败

**原因**: Length 字段计算错误

**正确计算**:
```python
length = len(payload) + 2  # Unit ID (1) + Function Code (1) + Data
response[4:6] = length.to_bytes(2, 'big')
```

### 6.3 字节序问题

**症状**: 数值读取错误

**原因**: 大小端不匹配

**解决**: Modbus 使用 **大端 (Big-Endian)**
```python
value = int.from_bytes(data, 'big')  # ✅ 正确
value = int.from_bytes(data, 'little')  # ❌ 错误
```

### 6.4 线圈状态不同步

**症状**: 写入了但继电器不动作

**原因**: 存储区和硬件未同步

**解决**:
```python
# 后台任务持续同步
async def sync_hardware():
    while True:
        coil_status = store["co"][0]
        relay.write(bool(coil_status))
        await asyncio.sleep(0.1)  # 10Hz
```

---

## 7. Python 实现要点

### 7.1 服务器框架选择

| 方案 | 优点 | 缺点 |
|------|------|------|
| **pymodbus 3.x** | 标准库 | API 复杂，版本变化大 |
| **手写 asyncio** | 简单直接，完全控制 | 需要自己处理所有细节 |

**推荐**: 简单应用用手写，复杂应用用 pymodbus

### 7.2 关键代码片段

**处理客户端连接**:
```python
async def handle_client(reader, writer):
    while True:
        # 读取帧头 (8 字节)
        data = await asyncio.wait_for(reader.read(8), timeout=2.0)
        
        # 读取剩余数据
        length = int.from_bytes(data[4:6], 'big')
        remaining = length - 2
        if remaining > 0:
            data += await asyncio.wait_for(reader.read(remaining), timeout=2.0)
        
        # 解析并处理
        trans_id = int.from_bytes(data[0:2], 'big')
        fc = data[7]
        response = process_request(trans_id, fc, data[8:])
        
        # 发送响应
        if response:
            writer.write(response)
            await writer.drain()
```

**构建响应**:
```python
def build_response(trans_id, unit_id, fc, payload):
    response = bytearray()
    response.extend(trans_id.to_bytes(2, 'big'))  # 事务 ID (必须一致!)
    response.extend(b'\x00\x00')  # 协议 ID
    response.extend(((2 + len(payload))).to_bytes(2, 'big'))  # 长度
    response.append(unit_id)  # 单元 ID
    response.append(fc)  # 功能码
    response.extend(payload)  # 数据
    return response
```

---

## 8. 调试技巧

### 8.1 启用详细日志

```python
logging.basicConfig(level=logging.INFO)
logger.info(f"📥 请求：FC=0x{fc:02X}, 事务 ID={trans_id}")
logger.info(f"📤 响应：{response.hex()}")
```

### 8.2 使用 Wireshark 抓包

```
过滤器：tcp.port == 5020
查看：Transaction ID、Length、Function Code
```

### 8.3 Python 测试客户端

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.13', 5020))
sock.sendall(request_bytes)
response = sock.recv(1024)
print(response.hex())
```

---

## 9. 参考资料

- **Modbus 规范**: https://modbus.org/specs.php
- **Modbus TCP 指南**: https://modbus.org/docs/Modbus_Messaging_Implementation_Guide_V1_0b2.pdf
- **pymodbus 文档**: https://pymodbus.readthedocs.io/
- **NI ModVIEW 教程**: https://www.ni.com/docs/

---

*文档创建时间：2026-03-19*  
*基于树莓派 SCADA 系统实战经验*
