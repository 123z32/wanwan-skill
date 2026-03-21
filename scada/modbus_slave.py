#!/usr/bin/env python3
"""
Modbus TCP 从站服务 - LED + 光敏电阻控制 (pymodbus 3.x)
========================================
配合宿主机 GPIO HTTP 服务 (端口 5000) 使用
LabVIEW 通过 Modbus TCP 连接本服务控制 LED 和读取光敏电阻

Modbus 寄存器映射 (从站地址=1):
  
  线圈 (Coils) - 功能码 01/05/15:
    0x0000: LED 控制 (写 1=ON, 写 0=OFF)

  离散输入 (Discrete Inputs) - 功能码 02:
    0x0000: LED 当前状态 (1=ON, 0=OFF)
    0x0001: 光敏电阻状态 (1=亮，0=暗)

  保持寄存器 (Holding Registers) - 功能码 03/06/16:
    0x0000: 光敏电阻原始值 (0=LOW, 1=HIGH)
    0x0001: 系统运行时间 (秒) 低 16 位

  输入寄存器 (Input Registers) - 功能码 04:
    0x0000: 光敏电阻原始值 (同保持寄存器)
    0x0001: 系统运行时间 (秒) 低 16 位

LabVIEW 连接配置：
  IP: 树莓派 IP (192.168.1.13 或 100.93.35.112)
  端口：5020 (标准 502 需要 root)
  从站地址：1

硬件配置：
  LED: GPIO 17 (输出)
  光敏电阻：GPIO 27 (输入)

作者：绾绾
日期：2026-03-21
"""

import sys
import time
import logging
import asyncio
import requests
from datetime import datetime

# pymodbus 3.x
try:
    from pymodbus.server import StartAsyncTcpServer
    from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext, ModbusSequentialDataBlock
    from pymodbus.pdu.device import ModbusDeviceIdentification
except ImportError as e:
    print(f"❌ pymodbus 导入失败：{e}")
    print("   请运行：pip3 install --break-system-packages pymodbus")
    sys.exit(1)

# ==================== 配置 ====================

MODBUS_HOST = "0.0.0.0"
MODBUS_PORT = 5020  # 使用 5020 避免权限问题（标准 502 需要 root）
GPIO_SERVICE_URL = "http://100.93.35.112:5000"  # 宿主机 GPIO HTTP 服务
POLL_INTERVAL = 0.2         # 状态轮询间隔 (秒)

# 日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('ModbusSlave')

# ==================== GPIO HTTP 客户端 ====================

class GPIOClient:
    """通过 HTTP API 控制宿主机 GPIO (LED + 光敏电阻)"""

    def __init__(self, base_url=GPIO_SERVICE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 3

    def led_on(self):
        """打开 LED"""
        try:
            r = self.session.post(f"{self.base_url}/led/on")
            return r.json().get("success", False)
        except Exception as e:
            logger.error(f"LED ON 失败：{e}")
            return False

    def led_off(self):
        """关闭 LED"""
        try:
            r = self.session.post(f"{self.base_url}/led/off")
            return r.json().get("success", False)
        except Exception as e:
            logger.error(f"LED OFF 失败：{e}")
            return False

    def led_status(self):
        """读取 LED 状态"""
        try:
            r = self.session.get(f"{self.base_url}/led/status")
            data = r.json()
            return data.get("state") == "on"
        except Exception as e:
            logger.error(f"读取 LED 状态失败：{e}")
            return False

    def read_light_sensor(self):
        """读取光敏电阻"""
        try:
            r = self.session.get(f"{self.base_url}/sensor/light")
            data = r.json()
            if data.get("success"):
                return data.get("value", 0)
            return 0
        except Exception as e:
            logger.error(f"读取光敏电阻失败：{e}")
            return 0

    def health_check(self):
        """健康检查"""
        try:
            r = self.session.get(f"{self.base_url}/health")
            return r.json().get("status") == "ok"
        except Exception:
            return False

# ==================== Modbus 设备上下文 ====================

class LEDLightDeviceContext(ModbusDeviceContext):
    """自定义设备上下文：LED + 光敏电阻"""

    def __init__(self, gpio_client):
        super().__init__()
        self.gpio = gpio_client
        self.start_time = time.time()
        
        # 使用顺序数据块
        self.coils = ModbusSequentialDataBlock(0, [False] * 16)      # 线圈
        self.di = ModbusSequentialDataBlock(0, [False] * 16)         # 离散输入
        self.hr = ModbusSequentialDataBlock(0, [0] * 16)             # 保持寄存器
        self.ir = ModbusSequentialDataBlock(0, [0] * 16)             # 输入寄存器
        
        self._last_coil_state = None

    async def update(self):
        """后台更新数据"""
        while True:
            try:
                # 1. 检查线圈写入 (LabVIEW → LED)
                coil_val = self.coils.getValues(0, 1)[0]
                if self._last_coil_state is not None and coil_val != self._last_coil_state:
                    if coil_val:
                        ok = self.gpio.led_on()
                        logger.info(f"💡 LabVIEW 写入线圈=1 → LED ON {'✅' if ok else '❌'}")
                    else:
                        ok = self.gpio.led_off()
                        logger.info(f"🌑 LabVIEW 写入线圈=0 → LED OFF {'✅' if ok else '❌'}")
                self._last_coil_state = coil_val

                # 2. 读取 LED 状态 → 离散输入 0x0000
                led_state = self.gpio.led_status()
                self.di.setValues(0, [1 if led_state else 0])

                # 3. 读取光敏电阻 → 离散输入 0x0001 + 寄存器
                light_val = self.gpio.read_light_sensor()
                self.di.setValues(1, [1 if light_val else 0])
                self.hr.setValues(0, [light_val])
                self.ir.setValues(0, [light_val])

                # 4. 更新运行时间
                uptime = int(time.time() - self.start_time)
                self.hr.setValues(1, [uptime & 0xFFFF])
                self.ir.setValues(1, [uptime & 0xFFFF])

                state_text = "☀️ 亮" if light_val else "🌙 暗"
                logger.debug(f"📊 光敏电阻：{state_text} (GPIO 27={light_val})")

            except Exception as e:
                logger.error(f"数据更新异常：{e}")

            await asyncio.sleep(POLL_INTERVAL)

# ==================== 主程序 ====================

async def main():
    print("=" * 60)
    print("🏭 SCADA Modbus TCP 从站服务 - LED + 光敏电阻控制")
    print("=" * 60)

    # 初始化 GPIO 客户端
    gpio = GPIOClient(GPIO_SERVICE_URL)
    print(f"\n📡 GPIO 服务地址：{GPIO_SERVICE_URL}")

    # 检查 GPIO 服务
    if gpio.health_check():
        print("✅ GPIO HTTP 服务连接正常")
    else:
        print("⚠️  GPIO HTTP 服务不可用，控制将失败")
        print("   请确保宿主机运行了 gpio_http_service.py")

    # 创建自定义设备上下文
    device_ctx = LEDLightDeviceContext(gpio)

    # 创建服务器上下文
    context = ModbusServerContext(devices={1: device_ctx}, single=False)

    # 设备标识
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'SCADA-Pi5'
    identity.ProductCode = 'RPi5-LED-LIGHT'
    identity.VendorUrl = 'https://github.com/123z32/wanwan-skill'
    identity.ProductName = 'RaspberryPi5 LED & Light Sensor'
    identity.ModelName = 'Modbus-TCP-Slave'
    identity.MajorMinorRevision = '2.0.0'

    # 启动数据更新任务
    asyncio.create_task(device_ctx.update())

    print(f"\n📋 Modbus 寄存器映射:")
    print(f"  ┌─────────────────────────────────────────────────┐")
    print(f"  │ 线圈 (Coils) - 读写                              │")
    print(f"  │   0x0000: LED 控制 (写 1=ON, 写 0=OFF)           │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │ 离散输入 (Discrete Inputs) - 只读                │")
    print(f"  │   0x0000: LED 状态 (1=ON, 0=OFF)                 │")
    print(f"  │   0x0001: 光敏电阻状态 (1=亮，0=暗)              │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │ 保持寄存器 (Holding Registers) - 读写            │")
    print(f"  │   0x0000: 光敏电阻值 (0=LOW, 1=HIGH)             │")
    print(f"  │   0x0001: 运行时间 (秒) 低 16 位                  │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │ 输入寄存器 (Input Registers) - 只读              │")
    print(f"  │   0x0000: 光敏电阻值 (同保持寄存器)              │")
    print(f"  │   0x0001: 运行时间 (秒) 低 16 位                  │")
    print(f"  └─────────────────────────────────────────────────┘")

    print(f"\n🚀 启动 Modbus TCP 服务器：{MODBUS_HOST}:{MODBUS_PORT}")
    print(f"   LabVIEW 连接：IP=192.168.1.13, Port={MODBUS_PORT}, Unit=1")
    print(f"\n按 Ctrl+C 停止服务\n")

    try:
        # 启动 Modbus TCP 服务器
        await StartAsyncTcpServer(
            context=context,
            address=(MODBUS_HOST, MODBUS_PORT),
            identity=identity,
        )
    except KeyboardInterrupt:
        print("\n⏹ 服务停止中...")
    except Exception as e:
        logger.error(f"服务器错误：{e}")
    finally:
        print("👋 Modbus 从站已停止")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 程序已终止")
