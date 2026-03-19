#!/usr/bin/env python3
"""
SCADA 下位机 - Modbus TCP 继电器控制服务
运行在树莓派宿主机 (Ubuntu 24.04)

依赖安装:
  sudo pip3 install --break-system-packages pymodbus python-periphery
"""

import asyncio
import logging
from datetime import datetime
from periphery import GPIO

# ================= 配置区 =================
GPIO_CHIP = 4          # GPIO 芯片编号
GPIO_LINE = 17         # GPIO 引脚号 (物理引脚 11)
MODBUS_PORT = 5020     # Modbus TCP 端口
SYNC_INTERVAL = 0.1    # 10Hz 同步频率
# ==========================================

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('Modbus_SCADA')

# 全局变量
relay = None
# Modbus 存储区 (简单 dict，不用 pymodbus 复杂的 API)
store = {
    "co": [False] * 100,  # Coils
    "di": [False] * 100,  # Discrete Inputs
    "hr": [0] * 100,      # Holding Registers
    "ir": [0] * 100,      # Input Registers
}

def init_gpio():
    """初始化 GPIO"""
    global relay
    try:
        relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        relay.write(False)
        logger.info(f"✅ 物理硬件初始化成功：/dev/gpiochip{GPIO_CHIP} Line {GPIO_LINE}")
        return True
    except Exception as e:
        logger.error(f"❌ GPIO 初始化失败：{e}")
        return False

async def sync_hardware():
    """后台任务：同步 Coil 0 或 HR 0 到物理继电器"""
    last_state = -1
    
    while True:
        try:
            # 优先检查线圈，其次检查保持寄存器 (LabVIEW 可能写 HR)
            coil_status = store["co"][0] or (store["hr"][0] > 0)
            relay.write(bool(coil_status))
            actual = relay.read()
            
            if last_state != coil_status:
                timestamp = datetime.now().strftime('%H:%M:%S')
                state_str = "🟢 ON " if coil_status else "🔴 OFF"
                verify = "✓" if actual == coil_status else "⚠️ 不一致"
                logger.info(f"[{timestamp}] Coil 0: {state_str} | GPIO: {verify}")
                last_state = coil_status
        except Exception as e:
            logger.error(f"❌ 同步错误：{e}")
        
        await asyncio.sleep(SYNC_INTERVAL)

async def handle_client(reader, writer):
    """处理 Modbus TCP 客户端"""
    addr = writer.get_extra_info('peername')
    logger.info(f"📡 客户端连接：{addr}")
    
    try:
        while True:
            data = await asyncio.wait_for(reader.read(8), timeout=2.0)
            if not data:
                break
            
            # 解析 Modbus TCP 帧头
            length = int.from_bytes(data[4:6], 'big')
            remaining = length - 2
            if remaining > 0:
                data += await asyncio.wait_for(reader.read(remaining), timeout=2.0)
            
            # 提取字段
            trans_id = int.from_bytes(data[0:2], 'big')
            unit_id = data[6]
            fc = data[7]
            payload = data[8:]
            
            logger.info(f"📥 请求：FC=0x{fc:02X}, 事务 ID={trans_id}, 数据={payload.hex()}")
            
            # 处理功能码
            response = None
            
            # 功能码 01: 读线圈
            if fc == 0x01:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                logger.info(f"   读线圈：地址={addr}, 数量={qty}")
                
                values = store["co"][addr:addr+qty]
                byte_count = (qty + 7) // 8
                byte_data = sum((1 << i) for i, v in enumerate(values) if v)
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))  # 事务 ID
                response.extend(b'\x00\x00')  # 协议 ID
                response.extend(((3 + byte_count)).to_bytes(2, 'big'))  # 长度
                response.append(unit_id)  # 单元 ID
                response.append(0x01)  # 功能码
                response.append(byte_count)  # 字节数
                response.append(byte_data)  # 数据
                
                logger.info(f"   响应：byte_count={byte_count}, data=0x{byte_data:02X}")
            
            # 功能码 02: 读离散输入
            elif fc == 0x02:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                values = store["co"][addr:addr+qty]  # 映射到线圈
                byte_count = (qty + 7) // 8
                byte_data = sum((1 << i) for i, v in enumerate(values) if v)
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(((3 + byte_count)).to_bytes(2, 'big'))
                response.append(unit_id)
                response.append(0x02)
                response.append(byte_count)
                response.append(byte_data)
            
            # 功能码 03: 读保持寄存器
            elif fc == 0x03:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                values = store["hr"][addr:addr+qty]
                byte_count = qty * 2
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(((3 + byte_count)).to_bytes(2, 'big'))
                response.append(unit_id)
                response.append(0x03)
                response.append(byte_count)
                for v in values:
                    response.extend(int(v).to_bytes(2, 'big'))
            
            # 功能码 05: 写单个线圈
            elif fc == 0x05:
                addr = int.from_bytes(payload[0:2], 'big')
                value = int.from_bytes(payload[2:4], 'big')
                store["co"][addr] = (value == 0xFF00)
                logger.info(f"✍️ 写线圈：地址{addr}, 值={'ON' if store['co'][addr] else 'OFF'}")
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x05)
                response.extend(payload)
            
            # 功能码 06: 写单个寄存器
            elif fc == 0x06:
                addr = int.from_bytes(payload[0:2], 'big')
                value = int.from_bytes(payload[2:4], 'big')
                store["hr"][addr] = value
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x06)
                response.extend(payload)
            
            # 功能码 15 (0x0F): 写多个线圈
            elif fc == 0x0F:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                byte_count = payload[4]
                values_data = payload[5:5+byte_count]
                
                for i in range(qty):
                    byte_idx = i // 8
                    bit_idx = i % 8
                    store["co"][addr + i] = bool((values_data[byte_idx] >> bit_idx) & 1)
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x0F)
                response.extend(payload[0:4])
            
            # 功能码 16 (0x10): 写多个寄存器
            elif fc == 0x10:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                byte_count = payload[4]
                values_data = payload[5:5+byte_count]
                
                for i in range(qty):
                    val = int.from_bytes(values_data[i*2:(i+1)*2], 'big')
                    store["hr"][addr + i] = val
                    # 同步到线圈 (如果写的是地址 0)
                    if addr + i == 0:
                        store["co"][0] = (val > 0)
                
                logger.info(f"✍️ 写寄存器：地址{addr}, 值={store['hr'][addr]}")
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x10)
                response.extend(payload[0:4])
            
            else:
                logger.warning(f"⚠️ 不支持的功能码：0x{fc:02X}")
            
            # 发送响应
            if response:
                logger.debug(f"📤 响应：{response.hex()}")
                writer.write(response)
                await writer.drain()
    
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        logger.error(f"❌ 客户端错误：{e}")
    finally:
        writer.close()
        await writer.wait_closed()
        logger.info(f"📡 客户端断开：{addr}")

async def run_server():
    """主服务器"""
    if not init_gpio():
        return
    
    logger.info("\n" + "=" * 60)
    logger.info("    🏭 SCADA 下位机 - Modbus TCP 服务运行中")
    logger.info("=" * 60)
    logger.info(f"    监听端口：{MODBUS_PORT}")
    logger.info(f"    控制地址：Coil 00000 -> GPIO Line {GPIO_LINE}")
    logger.info(f"    同步频率：{int(1/SYNC_INTERVAL)} Hz")
    logger.info("\n    等待上位机 (LabVIEW) 连接...")
    logger.info("=" * 60 + "\n")
    
    # 启动后台同步任务
    asyncio.create_task(sync_hardware())
    
    # 启动 TCP 服务器
    server = await asyncio.start_server(handle_client, '0.0.0.0', MODBUS_PORT)
    
    async with server:
        await server.serve_forever()

def cleanup():
    """清理资源"""
    logger.info("\n👋 安全退出...")
    if relay:
        relay.write(False)
        relay.close()
        logger.info("✅ 继电器已关闭")

async def main():
    try:
        await run_server()
    except KeyboardInterrupt:
        logger.info("\n⚠️  用户中断")
    except Exception as e:
        logger.error(f"❌ 服务器异常：{e}")
    finally:
        cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"启动失败：{e}")
        exit(1)
