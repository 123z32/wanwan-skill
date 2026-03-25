# Modbus TCP协议（Modbus TCP Protocol）

> 来源: OneNote > 通信 > Modbus协议
> 修改: 2026-03-25T08:10:57Z

Modbus TCP协议（Modbus TCP Protocol）
 
 
 
 
 

 
 
Modbus TCP 是一种基于 TCP/IP 网络的工业通信协议，用于在 PLC、仪表、能源管理设备、IoT 网关等设备之间进行快速、稳定的数据交互。相比传统串口方式的 Modbus RTU，Modbus TCP 具备更高带宽、更强并发能力与更灵活的网络拓扑，是现代工业自动化和物联网平台最常用的协议之一。

 
1. Modbus TCP 是什么？

 
Modbus TCP（也称 Modbus TCP/IP）是将 Modbus 应用层协议封装在 TCP/IP 网络传输层之上的协议版本。

 
主要特点包括：

 
- 使用 TCP 502 端口
 
- 通过 MBAP Header 替代 RTU 帧头与 CRC（Modbus应用协议头）
 
- 速度快、无时序限制，可跨网段传输
 
- 功能码与寄存器模型与 Modbus RTU 完全一致
 
- 可支持多个客户端同时访问同一个从站设备
 
这使得 Modbus TCP 成为智能制造、工业互联、能源监控系统等领域的通用通信方式。

 
2. Modbus TCP 报文结构（MBAP + PDU）

 
Modbus TCP 报文结构 = MBAP Header + PDU，如下所示：

 
+----------------------+---------------------------+￼| MBAP Header (7 字节) | PDU(Function + Data) |￼+----------------------+---------------------------+

 
2.1 MBAP Header（7 字节）

 
 

 | 字段
 | 长度
 | 含义
 
 

 | Transaction ID
 | 2
 | 请求编号，用于客户端匹配响应
 
 

 | Protocol ID
 | 2
 | 固定为 0（表示 Modbus）
 
 

 | Length
 | 2
 | 后续 PDU 数据长度
 
 

 | Unit ID
 | 1
 | 从站地址（用于 TCP → RTU 网关）
 
 

 
2.2 PDU（功能码 + 数据）

 
PDU = Function Code (1 字节) + Data (N 字节)

 

 
PDU 与 Modbus RTU 完全一致，因此 Modbus TCP 在应用层保持良好兼容性。

 
3. Modbus TCP 与 Modbus RTU 的区别

 
 

 | 项目
 | Modbus TCP
 | Modbus RTU
 
 

 | 传输介质
 | TCP/IP 网络
 | RS-485 串口
 
 

 | 校验方式
 | 依赖 TCP（无需 CRC）
 | 带 CRC 校验
 
 

 | 地址规则
 | Unit ID（主要用于网关场景）
 | 1–247
 
 

 | 帧结构
 | MBAP Header + PDU
 | 起始位 + PDU + CRC
 
 

 | 并发性
 | 多客户端并发
 | 单主机
 
 

 | 性能
 | 高速，无时序限制
 | 受串口波特率限制
 
 

 
总结：Modbus TCP 更适用于需要稳定、高速、跨网络访问的场景，是物联网平台和 SCADA 系统的主流协议方案。

 
4. 常用 Modbus TCP 功能码

 
 

 | 功能码
 | 名称
 | 描述
 
 

 | 01
 | Read Coils
 | 读线圈
 
 

 | 02
 | Read Discrete Inputs
 | 读离散输入
 
 

 | 03
 | Read Holding Registers
 | 读保持寄存器
 
 

 | 04
 | Read Input Registers
 | 读输入寄存器
 
 

 | 05
 | Write Single Coil
 | 写单线圈
 
 

 | 06
 | Write Single Register
 | 写单寄存器
 
 

 | 15
 | Write Multiple Coils
 | 批量写线圈
 
 

 | 16
 | Write Multiple Registers
 | 批量写寄存器
 
 

 
5. Modbus TCP 报文示例

 
5.1 请求（读取保持寄存器 40001 开始 2 个寄存器）

 
00 01 00 00 00 06 01 03 00 00 00 02￼↑ MBAP Header ↑ ↑ PDU（功能码+地址+数量） ↑

 
1

 
2

 
5.2 响应

 
00 01 00 00 00 05 01 03 04 00 0A 00 14

 
1

 
解析：

 
- 功能码：03
 
- 返回字节：04
 
- 数据：0x000A、0x0014
 
6. Modbus TCP 通信拓扑结构

 
Modbus TCP 基于以太网进行通信，通常采用星型或树型网络拓扑，典型结构包括：

 
- 一个主站（SCADA / PLC / 工控机 / 网关）
 
- 多个从站（智能仪表、传感器、控制器等）
 
- 通过交换机进行以太网连接
 
相比 RTU，Modbus TCP 支持更高的通信速率，网络扩展更灵活，并可通过 IP 地址方式管理大量设备。

 ![拓补图](https://graph.microsoft.com/v1.0/users('2209338213@qq.com')/onenote/resources/0-97d55bfb06054367bf25609c8d48950d!1-9E53C6D99C1E5AD1!s80f8fee137134466a9ec7945149fc2ff/$value)
 
7. Modbus TCP 常见问题（FAQ）

 
7.1 Modbus TCP 是否需要 Unit ID？

 
需要，但不一定生效。

 
- 真·TCP 设备 → Unit ID 通常固定为 1
 
- 网关（TCP→RTU） → Unit ID = RTU 从站地址
 
7.2 为什么 Modbus TCP 没有 CRC？

 
因为 TCP 传输层已经提供可靠性保证，不需要冗余 CRC。

 
7.3 Modbus TCP 是否支持广播？

 
不支持，广播仅在 Modbus RTU 中有效。

 
7.4 Modbus TCP 地址与 RTU 是否相同？

 
完全一致，Modbus TCP 仅改变了链路层封装。

 
8. 总结

 
Modbus TCP 是最广泛应用的工业网络协议之一，兼具稳定性、可靠性、跨网络访问和高性能优势。通过 MBAP Header 与标准化 PDU 结构，Modbus TCP 在保持与 Modbus RTU 兼容的同时，实现了更快的数据传输、更灵活的部署方式以及更高的并发能力。

 
掌握 Modbus TCP 报文结构、寄存器模型、功能码含义以及与 Modbus RTU 的区别，有助于快速完成设备调试、物联网平台接入以及工业网络的统一管理。