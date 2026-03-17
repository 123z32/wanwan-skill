#!/usr/bin/env python3
"""
SCADA 系统 - 树莓派从站控制器
===========================
功能：
1. Modbus TCP 从站服务（监听 502 端口）
2. GPIO 继电器控制（GPIO2 高电平触发）
3. AHT20/BHT80 温湿度传感器读取（I2C）

作者：绾绾
日期：2026-03-17
"""

import sys
import time
import logging
from datetime import datetime
from threading import Lock

# GPIO 控制
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("警告：RPi.GPIO 未安装，将使用模拟模式")

# I2C 传感器
try:
    import smbus2
    I2C_AVAILABLE = True
except ImportError:
    I2C_AVAILABLE = False
    print("警告：smbus2 未安装，传感器将返回模拟数据")

# Modbus TCP 从站
try:
    from pymodbus.server import StartTcpServer
    from pymodbus.datastore import ModbusSequentialDataBlock
    from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
    from pymodbus.transaction import ModbusRtuFramer, ModbusTcpFramer
    MODBUS_AVAILABLE = True
except ImportError:
    MODBUS_AVAILABLE = False
    print("错误：pymodbus 未安装，请运行：pip3 install pymodbus")
    sys.exit(1)

# ==================== 配置 ====================

# GPIO 引脚定义
RELAY_PIN = 17  # 继电器控制引脚 (GPIO17, 物理引脚 11)

# I2C 传感器地址
AHT20_ADDRESS = 0x38
BHT80_ADDRESS = 0x38  # BHT80 和 AHT20 地址相同

# Modbus 配置
MODBUS_PORT = 502

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/scada_controller.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SCADA_Controller')

# ==================== 继电器控制类 ====================

class RelayController:
    """继电器控制器 - 高电平触发"""
    
    def __init__(self, pin=RELAY_PIN):
        self.pin = pin
        self.state = False
        self.lock = Lock()
        
        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            logger.info(f"继电器初始化完成，引脚：GPIO{self.pin}")
        else:
            logger.warning("继电器：模拟模式（无 GPIO）")
    
    def turn_on(self):
        """打开继电器"""
        with self.lock:
            if GPIO_AVAILABLE:
                GPIO.output(self.pin, GPIO.HIGH)
            self.state = True
            logger.info("继电器：ON")
            return True
    
    def turn_off(self):
        """关闭继电器"""
        with self.lock:
            if GPIO_AVAILABLE:
                GPIO.output(self.pin, GPIO.LOW)
            self.state = False
            logger.info("继电器：OFF")
            return True
    
    def toggle(self):
        """切换继电器状态"""
        with self.lock:
            if GPIO_AVAILABLE:
                current = GPIO.input(self.pin)
                GPIO.output(self.pin, not current)
                self.state = bool(not current)
            else:
                self.state = not self.state
            logger.info(f"继电器：TOGGLE -> {'ON' if self.state else 'OFF'}")
            return self.state
    
    def get_state(self):
        """获取继电器状态"""
        return self.state
    
    def cleanup(self):
        """清理 GPIO"""
        if GPIO_AVAILABLE:
            GPIO.cleanup(self.pin)
            logger.info("GPIO 已清理")

# ==================== 温湿度传感器类 ====================

class AHT20Sensor:
    """AHT20/BHT80 温湿度传感器 (I2C)"""
    
    def __init__(self, address=AHT20_ADDRESS, bus=1):
        self.address = address
        self.bus = None
        self.last_temperature = 25.0  # 默认值
        self.last_humidity = 50.0     # 默认值
        
        if I2C_AVAILABLE:
            try:
                self.bus = smbus2.SMBus(bus)
                logger.info(f"温湿度传感器初始化完成，I2C 地址：0x{address:02X}")
                self._initialize_sensor()
            except Exception as e:
                logger.warning(f"传感器初始化失败：{e}，将使用模拟数据")
                self.bus = None
        else:
            logger.warning("传感器：模拟模式（无 I2C）")
    
    def _initialize_sensor(self):
        """初始化传感器"""
        if self.bus is None:
            return
        
        try:
            # 发送初始化命令
            self.bus.write_i2c_block_data(self.address, 0xE1, [0x08, 0x00])
            time.sleep(0.01)
            logger.info("传感器初始化命令已发送")
        except Exception as e:
            logger.warning(f"传感器初始化命令失败：{e}")
    
    def read_temperature_humidity(self):
        """读取温度和湿度"""
        if self.bus is None:
            # 模拟数据
            import random
            self.last_temperature = 20.0 + random.uniform(-2, 2)
            self.last_humidity = 50.0 + random.uniform(-5, 5)
            return self.last_temperature, self.last_humidity
        
        try:
            # 触发测量
            self.bus.write_i2c_block_data(self.address, 0xAC, [0x33, 0x00])
            time.sleep(0.08)  # 等待测量完成
            
            # 读取数据 (7 字节)
            data = self.bus.read_i2c_block_data(self.address, 0x71, 7)
            
            # 检查状态
            if data[0] & 0x08:
                logger.warning("传感器忙，重试中...")
                return self.last_temperature, self.last_humidity
            
            # 解析数据
            humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
            humidity = (humidity_raw / (2 ** 20)) * 100.0
            
            temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
            temperature = (temp_raw / (2 ** 20)) * 200.0 - 50.0
            
            self.last_temperature = temperature
            self.last_humidity = humidity
            
            logger.debug(f"传感器读数：T={temperature:.2f}°C, H={humidity:.2f}%")
            return temperature, humidity
            
        except Exception as e:
            logger.error(f"传感器读取失败：{e}")
            return self.last_temperature, self.last_humidity
    
    def get_temperature(self):
        """只读取温度"""
        temp, _ = self.read_temperature_humidity()
        return temp
    
    def get_humidity(self):
        """只读取湿度"""
        _, hum = self.read_temperature_humidity()
        return hum

# ==================== Modbus 从站服务 ====================

class ModbusSlaveServer:
    """Modbus TCP 从站服务器"""
    
    def __init__(self, relay: RelayController, sensor: AHT20Sensor):
        self.relay = relay
        self.sensor = sensor
        self.store = None
        self.context = None
        
        # 初始化 Modbus 数据存储
        # 线圈 (Coils) - 继电器控制
        # 0x0000: 继电器控制 (0=OFF, 1=ON)
        # 0x0001: 继电器切换
        # 离散输入 (Discrete Inputs) - 只读状态
        # 0x0000: 继电器状态
        # 保持寄存器 (Holding Registers) - 传感器数据
        # 0x0000: 温度 (×100, 整数)
        # 0x0001: 湿度 (×100, 整数)
        
        self.store = ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [0] * 10),      # 离散输入
            co=ModbusSequentialDataBlock(0, [0] * 10),      # 线圈
            hr=ModbusSequentialDataBlock(0, [0] * 10),      # 保持寄存器
            ir=ModbusSequentialDataBlock(0, [0] * 10),      # 输入寄存器
        )
        self.context = ModbusServerContext(slaves=self.store, single=True)
        
        logger.info("Modbus 从站初始化完成")
    
    def update_sensor_data(self):
        """更新传感器数据到 Modbus 寄存器"""
        try:
            temp, hum = self.sensor.read_temperature_humidity()
            # 温度 ×100 存储为整数 (如 25.5°C -> 2550)
            self.store.setValues(3, 0, [int(temp * 100)])  # HR 0x0000
            # 湿度 ×100 存储为整数
            self.store.setValues(3, 1, [int(hum * 100)])   # HR 0x0001
            logger.debug(f"Modbus 数据更新：T={temp:.2f}°C, H={hum:.2f}%")
        except Exception as e:
            logger.error(f"更新传感器数据失败：{e}")
    
    def process_request(self):
        """处理 Modbus 请求（在服务器回调中调用）"""
        try:
            # 检查线圈 0x0000 - 继电器控制
            relay_cmd = self.store.getValues(1, 0, 1)[0]
            if relay_cmd == 1:
                self.relay.turn_on()
            elif relay_cmd == 0:
                self.relay.turn_off()
            
            # 检查线圈 0x0001 - 继电器切换（脉冲信号）
            toggle_cmd = self.store.getValues(1, 1, 1)[0]
            if toggle_cmd == 1:
                self.relay.toggle()
                # 重置切换命令
                self.store.setValues(1, 1, [0])
            
            # 更新离散输入 - 继电器状态
            relay_state = 1 if self.relay.get_state() else 0
            self.store.setValues(2, 0, [relay_state])
            
            # 更新传感器数据
            self.update_sensor_data()
            
        except Exception as e:
            logger.error(f"处理 Modbus 请求失败：{e}")
    
    def start(self):
        """启动 Modbus TCP 服务器"""
        logger.info(f"启动 Modbus TCP 服务器，端口：{MODBUS_PORT}")
        
        try:
            StartTcpServer(
                context=self.context,
                address=("0.0.0.0", MODBUS_PORT),
                framer=ModbusTcpFramer,
                # 自定义回调
                # 注意：pymodbus v3.x 的回调方式可能不同
            )
        except Exception as e:
            logger.error(f"Modbus 服务器启动失败：{e}")
            raise

# ==================== 主程序 ====================

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("SCADA 控制器启动")
    logger.info("=" * 50)
    
    # 初始化设备
    relay = RelayController(pin=RELAY_PIN)
    sensor = AHT20Sensor(address=AHT20_ADDRESS)
    
    # 初始化 Modbus 从站
    modbus_server = ModbusSlaveServer(relay, sensor)
    
    # 注册信号处理
    import signal
    
    def signal_handler(sig, frame):
        logger.info("收到退出信号，清理中...")
        relay.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动 Modbus 服务器（阻塞）
    try:
        modbus_server.start()
    except KeyboardInterrupt:
        logger.info("用户中断")
    finally:
        relay.cleanup()
        logger.info("SCADA 控制器已停止")

if __name__ == "__main__":
    main()
