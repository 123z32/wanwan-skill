#!/usr/bin/env python3
"""
SCADA 下位机 - Modbus TCP LED + 光敏电阻控制服务
运行在树莓派宿主机 (Ubuntu 24.04)

硬件配置:
  LED: GPIO 17 (输出)
  光敏电阻：GPIO 27 (输入)

依赖安装:
  sudo pip3 install --break-system-packages pymodbus python-periphery

Modbus 寄存器映射:
  线圈 (Coils) - 功能码 01/05/15:
    0x0000: LED 控制 (写 1=ON, 写 0=OFF)
  
  离散输入 (Discrete Inputs) - 功能码 02:
    0x0000: LED 状态反馈 (1=ON, 0=OFF)
    0x0001: 光敏电阻状态 (1=亮，0=暗)
  
  保持寄存器 (Holding Registers) - 功能码 03/06/16:
    0x0000: 光敏电阻原始值 (0=LOW, 1=HIGH)
    0x0001: 系统运行时间 (秒) 低 16 位
  
  输入寄存器 (Input Registers) - 功能码 04:
    0x0000: 光敏电阻原始值 (同保持寄存器)
    0x0001: 系统运行时间 (秒) 低 16 位

LabVIEW 连接配置:
  IP: 树莓派 IP (192.168.1.13)
  端口：5020
  从站地址：1

作者：绾绾
日期：2026-03-21
"""

import asyncio
import logging
from datetime import datetime
from periphery import GPIO

# ================= 配置区 =================
GPIO_CHIP = 4           # GPIO 芯片编号
LED_PIN = 17            # LED 引脚 (输出)
LIGHT_SENSOR_PIN = 27   # 光敏电阻引脚 (输入)
MODBUS_PORT = 5021      # Modbus TCP 端口 (5020 可能被占用)
# ==========================================

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('Modbus_SCADA')

# 全局变量
led = None
light_sensor = None
start_time = None
last_uptime = 0

# Modbus 存储区 (初始值，不主动刷新)
store = {
    "co": [False] * 100,  # Coils (线圈)
    "di": [False] * 100,  # Discrete Inputs (离散输入) - 仅在读取时更新
    "hr": [0] * 100,      # Holding Registers (保持寄存器)
    "ir": [0] * 100,      # Input Registers (输入寄存器) - 仅在读取时更新
}

def init_gpio():
    """初始化 GPIO"""
    global led, light_sensor, start_time
    
    try:
        # 初始化 LED (输出)
        led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        led.write(False)
        logger.info(f"✅ LED 初始化成功：/dev/gpiochip{GPIO_CHIP} Line {LED_PIN}")
        
        # 初始化光敏电阻 (输入)
        light_sensor = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LIGHT_SENSOR_PIN, "in")
        logger.info(f"✅ 光敏电阻初始化成功：/dev/gpiochip{GPIO_CHIP} Line {LIGHT_SENSOR_PIN}")
        
        # 记录启动时间
        start_time = datetime.now()
        
        return True
    except Exception as e:
        logger.warning(f"⚠️  GPIO 初始化失败：{e}")
        logger.warning("   使用模拟模式 (无硬件)")
        
        # 模拟模式
        led = None
        light_sensor = None
        start_time = datetime.now()
        return True

def read_light_sensor():
    """读取光敏电阻"""
    global light_sensor
    try:
        if light_sensor:
            return light_sensor.read()
        else:
            # 模拟模式：随机生成
            import random
            return random.choice([0, 1])
    except Exception as e:
        logger.error(f"读取光敏电阻失败：{e}")
        return 0

def update_sensor_data():
    """按需更新传感器数据（仅在 Modbus 读取时调用）"""
    global last_uptime
    
    try:
        # 1. 读取 LED 状态
        led_status = store["co"][0]
        if led:
            actual = led.read()
            store["di"][0] = actual
        else:
            store["di"][0] = led_status
        
        # 2. 读取光敏电阻
        light_val = read_light_sensor()
        store["di"][1] = bool(light_val)
        store["hr"][0] = light_val
        store["ir"][0] = light_val
        
        # 3. 更新运行时间
        if start_time:
            last_uptime = int((datetime.now() - start_time).total_seconds())
            store["hr"][1] = last_uptime & 0xFFFF
            store["ir"][1] = last_uptime & 0xFFFF
        
        logger.debug(f"📊 传感器数据已更新：LED={store['di'][0]}, 光敏={light_val}, 时间={last_uptime}s")
        
    except Exception as e:
        logger.error(f"❌ 传感器数据更新失败：{e}")

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
            
            # ========== 功能码 01: 读线圈 ==========
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
            
            # ========== 功能码 02: 读离散输入 ==========
            elif fc == 0x02:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                logger.info(f"   读离散输入：地址={addr}, 数量={qty}")
                
                # 按需更新传感器数据
                update_sensor_data()
                
                values = store["di"][addr:addr+qty]
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
                
                logger.info(f"   响应：byte_count={byte_count}, data=0x{byte_data:02X}")
            
            # ========== 功能码 03: 读保持寄存器 ==========
            elif fc == 0x03:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                logger.info(f"   读保持寄存器：地址={addr}, 数量={qty}")
                
                # 按需更新传感器数据
                update_sensor_data()
                
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
                
                logger.info(f"   响应：寄存器值={values}")
            
            # ========== 功能码 04: 读输入寄存器 ==========
            elif fc == 0x04:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                logger.info(f"   读输入寄存器：地址={addr}, 数量={qty}")
                
                # 按需更新传感器数据
                update_sensor_data()
                
                values = store["ir"][addr:addr+qty]
                byte_count = qty * 2
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(((3 + byte_count)).to_bytes(2, 'big'))
                response.append(unit_id)
                response.append(0x04)
                response.append(byte_count)
                for v in values:
                    response.extend(int(v).to_bytes(2, 'big'))
                
                logger.info(f"   响应：寄存器值={values}")
            
            # ========== 功能码 05: 写单个线圈 ==========
            elif fc == 0x05:
                addr = int.from_bytes(payload[0:2], 'big')
                value = int.from_bytes(payload[2:4], 'big')
                store["co"][addr] = (value == 0xFF00)
                
                # 立即控制 LED
                if addr == 0 and led:
                    led.write(store["co"][0])
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    state_str = "🟢 ON" if store["co"][0] else "🔴 OFF"
                    logger.info(f"[{timestamp}] LED: {state_str} | GPIO: ✓")
                
                logger.info(f"✍️ 写线圈：地址{addr}, 值={'ON (0xFF00)' if store['co'][addr] else 'OFF (0x0000)'}")
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x05)
                response.extend(payload)
            
            # ========== 功能码 06: 写单个寄存器 ==========
            elif fc == 0x06:
                addr = int.from_bytes(payload[0:2], 'big')
                value = int.from_bytes(payload[2:4], 'big')
                store["hr"][addr] = value
                # 如果写的是地址 0，同步到线圈并控制 LED
                if addr == 0:
                    store["co"][0] = (value > 0)
                    if led:
                        led.write(store["co"][0])
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        state_str = "🟢 ON" if store["co"][0] else "🔴 OFF"
                        logger.info(f"[{timestamp}] LED: {state_str} | GPIO: ✓")
                
                logger.info(f"✍️ 写寄存器：地址{addr}, 值={value}")
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x06)
                response.extend(payload)
            
            # ========== 功能码 15 (0x0F): 写多个线圈 ==========
            elif fc == 0x0F:
                addr = int.from_bytes(payload[0:2], 'big')
                qty = int.from_bytes(payload[2:4], 'big')
                byte_count = payload[4]
                values_data = payload[5:5+byte_count]
                
                for i in range(qty):
                    byte_idx = i // 8
                    bit_idx = i % 8
                    store["co"][addr + i] = bool((values_data[byte_idx] >> bit_idx) & 1)
                
                logger.info(f"✍️ 写多个线圈：地址{addr}, 数量={qty}")
                
                response = bytearray()
                response.extend(trans_id.to_bytes(2, 'big'))
                response.extend(b'\x00\x00')
                response.extend(b'\x00\x04')
                response.append(unit_id)
                response.append(0x0F)
                response.extend(payload[0:4])
            
            # ========== 功能码 16 (0x10): 写多个寄存器 ==========
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
                
                logger.info(f"✍️ 写多个寄存器：地址{addr}, 值={store['hr'][addr]}")
                
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
    logger.info("    🏭 SCADA 下位机 - LED + 光敏电阻控制")
    logger.info("=" * 60)
    logger.info(f"    监听端口：{MODBUS_PORT}")
    logger.info(f"    LED 引脚：GPIO {LED_PIN} (输出)")
    logger.info(f"    光敏电阻：GPIO {LIGHT_SENSOR_PIN} (输入)")
    logger.info(f"    工作模式：按需读取 (上位机请求时才刷新)")
    logger.info("\n    等待上位机 (LabVIEW) 连接...")
    logger.info("=" * 60 + "\n")
    
    # 不需要后台同步任务，按需读取
    
    # 启动 TCP 服务器
    server = await asyncio.start_server(handle_client, '0.0.0.0', MODBUS_PORT)
    
    async with server:
        await server.serve_forever()

def cleanup():
    """清理资源"""
    logger.info("\n👋 安全退出...")
    if led:
        try:
            led.write(False)
            led.close()
            logger.info("✅ LED 已关闭")
        except:
            pass
    if light_sensor:
        try:
            light_sensor.close()
            logger.info("✅ 光敏电阻已释放")
        except:
            pass

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
        logger.error(f"❌ 启动失败：{e}")
        exit(1)
