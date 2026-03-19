#!/usr/bin/env python3
"""
Modbus TCP 从站服务
==================
配合宿主机 GPIO HTTP 服务 (端口 5000) 使用
LabVIEW 通过 Modbus TCP 连接本服务控制继电器和读取数据

Modbus 寄存器映射：
  线圈 (Coils) - 功能码 01/05/15:
    0x0000: 继电器控制 (写1=ON, 写0=OFF)

  离散输入 (Discrete Inputs) - 功能码 02:
    0x0000: 继电器当前状态 (1=ON, 0=OFF)

  保持寄存器 (Holding Registers) - 功能码 03/06/16:
    0x0000: 温度值 (×100, 如 2550 = 25.50°C)
    0x0001: 湿度值 (×100, 如 5000 = 50.00%)

  输入寄存器 (Input Registers) - 功能码 04:
    0x0000: 温度值 (同保持寄存器)
    0x0001: 湿度值 (同保持寄存器)
    0x0002: 系统运行时间 (秒)

LabVIEW 连接配置：
  IP: 树莓派 Tailscale IP (100.93.35.112)
  端口: 502
  从站地址: 1

作者：绾绾
日期：2026-03-19
"""

import sys
import time
import logging
import threading
import requests
from datetime import datetime

# Modbus
try:
    from pymodbus.server import StartTcpServer
    from pymodbus.datastore import (
        ModbusSequentialDataBlock,
        ModbusSlaveContext,
        ModbusServerContext
    )
    from pymodbus.device import ModbusDeviceIdentification
except ImportError:
    print("❌ pymodbus 未安装，请运行：pip3 install pymodbus[serial]")
    sys.exit(1)

# ==================== 配置 ====================

MODBUS_HOST = "0.0.0.0"
MODBUS_PORT = 502
GPIO_SERVICE_URL = "http://100.93.35.112:5000"  # 宿主机 GPIO HTTP 服务
SENSOR_UPDATE_INTERVAL = 2  # 传感器数据刷新间隔(秒)
RELAY_POLL_INTERVAL = 0.5   # 继电器状态轮询间隔(秒)

# 日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('ModbusSlave')

# ==================== GPIO HTTP 客户端 ====================

class GPIOClient:
    """通过 HTTP API 控制宿主机 GPIO"""

    def __init__(self, base_url=GPIO_SERVICE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 3

    def relay_on(self):
        try:
            r = self.session.post(f"{self.base_url}/relay/on")
            return r.json().get("state") == "on"
        except Exception as e:
            logger.error(f"继电器ON失败: {e}")
            return False

    def relay_off(self):
        try:
            r = self.session.post(f"{self.base_url}/relay/off")
            return r.json().get("state") == "off"
        except Exception as e:
            logger.error(f"继电器OFF失败: {e}")
            return False

    def relay_status(self):
        try:
            r = self.session.get(f"{self.base_url}/relay/status")
            data = r.json()
            return data.get("state") == "on"
        except Exception as e:
            logger.error(f"读取继电器状态失败: {e}")
            return False

    def health_check(self):
        try:
            r = self.session.get(f"{self.base_url}/health")
            return r.json().get("status") == "ok"
        except Exception:
            return False

# ==================== 数据更新线程 ====================

class DataUpdater(threading.Thread):
    """后台线程：同步继电器状态 + 更新传感器数据"""

    def __init__(self, context, gpio_client):
        super().__init__(daemon=True)
        self.context = context
        self.gpio = gpio_client
        self.start_time = time.time()
        self.running = True
        self._last_coil_state = None  # 跟踪上次线圈值

    def run(self):
        logger.info("数据更新线程启动")
        tick = 0
        while self.running:
            try:
                store = self.context[0x00]  # slave context

                # === 1. 处理线圈写入（LabVIEW → 继电器）===
                coil_val = store.getValues(1, 0, 1)[0]  # 读线圈 0x0000
                if self._last_coil_state is not None and coil_val != self._last_coil_state:
                    # 线圈值变化了，说明 LabVIEW 写了新值
                    if coil_val:
                        ok = self.gpio.relay_on()
                        logger.info(f"LabVIEW 写入线圈=1 → 继电器ON {'✅' if ok else '❌'}")
                    else:
                        ok = self.gpio.relay_off()
                        logger.info(f"LabVIEW 写入���圈=0 → 继电器OFF {'✅' if ok else '❌'}")
                self._last_coil_state = coil_val

                # === 2. 读取继电器实际状态 → 离散输入 ===
                relay_state = self.gpio.relay_status()
                store.setValues(2, 0, [1 if relay_state else 0])  # DI 0x0000

                # === 3. 更新传感器数据（每隔几秒）===
                if tick % int(SENSOR_UPDATE_INTERVAL / RELAY_POLL_INTERVAL) == 0:
                    self._update_sensor_data(store)

                # === 4. 更��运行时间 ===
                uptime = int(time.time() - self.start_time)
                store.setValues(4, 2, [uptime & 0xFFFF])  # IR 0x0002

            except Exception as e:
                logger.error(f"数据更新异常: {e}")

            tick += 1
            time.sleep(RELAY_POLL_INTERVAL)

    def _update_sensor_data(self, store):
        """更新温湿度数据（目前使用模拟数据，接传感器后替换）"""
        import random
        # TODO: 接入 AHT20/BHT80 传感器后替换
        temp = 25.0 + random.uniform(-2, 2)
        hum = 50.0 + random.uniform(-5, 5)

        temp_int = int(temp * 100)  # 25.50°C → 2550
        hum_int = int(hum * 100)    # 50.00% → 5000

        # 写入保持寄存器和输入寄存器
        store.setValues(3, 0, [temp_int, hum_int])   # HR 0x0000-0x0001
        store.setValues(4, 0, [temp_int, hum_int])    # IR 0x0000-0x0001

        logger.debug(f"传感器数据: T={temp:.2f}°C H={hum:.2f}%")

    def stop(self):
        self.running = False

# ==================== 主程序 ====================

def main():
    print("=" * 50)
    print("🏭 SCADA Modbus TCP 从站服务")
    print("=" * 50)

    # 初始化 GPIO 客户端
    gpio = GPIOClient(GPIO_SERVICE_URL)
    print(f"\n📡 GPIO 服务地址: {GPIO_SERVICE_URL}")

    # 检查 GPIO 服务
    if gpio.health_check():
        print("✅ GPIO HTTP 服务连接正常")
    else:
        print("⚠️  GPIO HTTP 服务不可用，继电器控制将失败")
        print("   请确保宿主机运行了 gpio_http_service.py")

    # 初始化 Modbus 数据存储
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 16),   # 离散输入
        co=ModbusSequentialDataBlock(0, [0] * 16),   # 线圈
        hr=ModbusSequentialDataBlock(0, [0] * 16),   # 保持寄存器
        ir=ModbusSequentialDataBlock(0, [0] * 16),   # 输入寄存器
    )
    context = ModbusServerContext(slaves=store, single=True)

    # 设备标识
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'SCADA-Pi5'
    identity.ProductCode = 'RPi5-SCADA'
    identity.VendorUrl = 'https://github.com/123z32/wanwan-skill'
    identity.ProductName = 'RaspberryPi5 SCADA Slave'
    identity.ModelName = 'Modbus-TCP-Slave'
    identity.MajorMinorRevision = '1.0.0'

    # 启动数据更新线程
    updater = DataUpdater(context, gpio)
    updater.start()

    print(f"\n📋 Modbus 寄存器映射:")
    print(f"  线圈 0x0000      → ��电器控制 (写1=ON, 写0=OFF)")
    print(f"  离散输入 0x0000   → 继电器状态 (只读)")
    print(f"  保持寄存器 0x0000 → 温度 (×100)")
    print(f"  保持寄存器 0x0001 → 湿度 (×100)")
    print(f"  输入寄存器 0x0002 → 运行时间 (秒)")

    print(f"\n🚀 启动 Modbus TCP 服务器: {MODBUS_HOST}:{MODBUS_PORT}")
    print(f"   LabVIEW 连接: IP=100.93.35.112, Port={MODBUS_PORT}, Unit=1")
    print(f"\n按 Ctrl+C 停止服务\n")

    try:
        StartTcpServer(
            context=context,
            identity=identity,
            address=(MODBUS_HOST, MODBUS_PORT),
        )
    except KeyboardInterrupt:
        print("\n⏹ 服务停止中...")
    except Exception as e:
        logger.error(f"服务器错误: {e}")
    finally:
        updater.stop()
        print("👋 Modbus 从站已停止")

if __name__ == "__main__":
    main()
