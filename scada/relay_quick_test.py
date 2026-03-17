#!/usr/bin/env python3
"""
继电器快速测试 - 让继电器动起来！
用法：sudo python3 relay_test.py
"""

import time

try:
    import RPi.GPIO as GPIO
    print("✅ RPi.GPIO 已安装")
except ImportError:
    print("❌ RPi.GPIO 未安装，正在安装...")
    import subprocess
    subprocess.run(["apt-get", "update"])
    subprocess.run(["apt-get", "install", "-y", "python3-rpi.gpio"])
    import RPi.GPIO as GPIO

# 配置
RELAY_PIN = 17  # 物理引脚 11

print("=" * 50)
print("🔌 继电器测试程序")
print("=" * 50)
print(f"使用引脚：GPIO{RELAY_PIN} (物理引脚 11)")
print("")

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)
print("✅ GPIO 初始化完成")
print("")

try:
    # 测试 1: 打开继电器
    print("📍 打开继电器... (3 秒后关闭)")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(3)
    print("✅ 继电器已打开！应该听到'吧嗒'声")
    
    # 测试 2: 关闭继电器
    print("\n📍 关闭继电器... (3 秒后再次打开)")
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(3)
    print("✅ 继电器已关闭")
    
    # 测试 3: 闪烁 5 次
    print("\n📍 闪烁测试 (5 次)...")
    for i in range(5):
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(0.5)
        print(f"   闪烁 {i+1}/5 ✓")
    
    print("\n✅ 继电器测试完成！")
    print("\n💡 提示:")
    print("   - 如果没听到'吧嗒'声，检查接线")
    print("   - 确认继电器模块供电正常 (5V)")
    print("   - 检查 GND 是否接好")
    
except KeyboardInterrupt:
    print("\n⚠️  用户中断")
finally:
    GPIO.cleanup()
    print("\n✅ GPIO 已清理")
