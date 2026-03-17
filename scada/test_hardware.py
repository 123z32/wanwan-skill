#!/usr/bin/env python3
"""
SCADA 系统 - 快速测试脚本
========================
用途：在树莓派上快速测试继电器和传感器，无需 Modbus
"""

import sys
import time

# 尝试导入 GPIO
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("⚠️  RPi.GPIO 未安装")

# 尝试导入 I2C
try:
    import smbus2
    I2C_AVAILABLE = True
except ImportError:
    I2C_AVAILABLE = False
    print("⚠️  smbus2 未安装")

# ==================== 配置 ====================

RELAY_PIN = 2  # GPIO2
AHT20_ADDRESS = 0x38

# ==================== 测试函数 ====================

def test_gpio():
    """测试 GPIO 控制"""
    print("\n🔌 测试 GPIO 控制")
    print("=" * 40)
    
    if not GPIO_AVAILABLE:
        print("❌ GPIO 不可用，跳过测试")
        return
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        
        print(f"✅ GPIO{RELAY_PIN} 初始化成功")
        
        # 测试打开
        print("📍 打开继电器...")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(2)
        print("✅ 继电器已打开（应该听到'吧嗒'声）")
        
        # 测试关闭
        print("📍 关闭继电器...")
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(2)
        print("✅ 继电器已关闭")
        
        # 测试闪烁 3 次
        print("📍 测试闪烁 3 次...")
        for i in range(3):
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(RELAY_PIN, GPIO.LOW)
            time.sleep(0.5)
            print(f"   闪烁 {i+1}/3")
        
        print("✅ GPIO 测试完成")
        
    except Exception as e:
        print(f"❌ GPIO 测试失败：{e}")
    finally:
        GPIO.cleanup()

def test_i2c():
    """测试 I2C 传感器"""
    print("\n🌡️  测试 I2C 传感器")
    print("=" * 40)
    
    if not I2C_AVAILABLE:
        print("❌ I2C 不可用，跳过测试")
        return
    
    try:
        bus = smbus2.SMBus(1)
        print("✅ I2C 总线初始化成功")
        
        # 扫描 I2C 设备
        print("📍 扫描 I2C 设备...")
        devices = bus.scan()
        print(f"   发现设备：{[hex(d) for d in devices]}")
        
        if AHT20_ADDRESS in devices:
            print(f"✅ 发现 AHT20 传感器 (0x{AHT20_ADDRESS:02X})")
            
            # 初始化传感器
            bus.write_i2c_block_data(AHT20_ADDRESS, 0xE1, [0x08, 0x00])
            time.sleep(0.01)
            
            # 读取 5 次
            print("📍 读取温湿度数据...")
            for i in range(5):
                # 触发测量
                bus.write_i2c_block_data(AHT20_ADDRESS, 0xAC, [0x33, 0x00])
                time.sleep(0.08)
                
                # 读取数据
                data = bus.read_i2c_block_data(AHT20_ADDRESS, 0x71, 7)
                
                # 解析
                humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
                humidity = (humidity_raw / (2 ** 20)) * 100.0
                
                temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
                temperature = (temp_raw / (2 ** 20)) * 200.0 - 50.0
                
                print(f"   [{i+1}/5] 温度：{temperature:.2f}°C, 湿度：{humidity:.2f}%")
                time.sleep(1)
            
            print("✅ I2C 传感器测试完成")
        else:
            print(f"⚠️  未在 0x{AHT20_ADDRESS:02X} 找到传感器")
            print("   可能原因：")
            print("   1. 传感器未正确接线")
            print("   2. I2C 未启用 (运行 sudo raspi-config 启用)")
            print("   3. 传感器地址不同")
        
    except Exception as e:
        print(f"❌ I2C 测试失败：{e}")
        print("   提示：运行 'sudo i2cdetect -y 1' 手动检测")

def show_pinout():
    """显示引脚图"""
    print("\n📌 树莓派 GPIO 引脚图 (简化版)")
    print("=" * 40)
    print("""
    物理引脚排列（从上到下，元件面朝上）：
    
       [3.3V] [1] [2] [5V]
       [GPIO2] [3] [4] [5V]     ← 继电器 IN (GPIO2)
       [GPIO3] [5] [6] [GND]    ← 继电器 GND
       [GPIO4] [7] [8] [GPIO14]
       [GND] [9] [10] [GPIO15]
       [GPIO17] [11] [12] [GPIO18]  ← 建议继电器改接 GPIO17
       ...
    
    I2C 引脚:
    - SDA: GPIO2 (物理引脚 3)
    - SCL: GPIO3 (物理引脚 5)
    """)

def main():
    """主函数"""
    print("🏭 SCADA 系统 - 快速测试")
    print("=" * 40)
    print(f"Python 版本：{sys.version}")
    print(f"GPIO 可用：{GPIO_AVAILABLE}")
    print(f"I2C 可用：{I2C_AVAILABLE}")
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "gpio":
            test_gpio()
        elif cmd == "i2c":
            test_i2c()
        elif cmd == "pinout":
            show_pinout()
        else:
            print(f"未知命令：{cmd}")
            print("用法：python3 test.py [gpio|i2c|pinout]")
    else:
        # 运行所有测试
        show_pinout()
        test_gpio()
        test_i2c()
        
        print("\n✅ 所有测试完成！")

if __name__ == "__main__":
    main()
