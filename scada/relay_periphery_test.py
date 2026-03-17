#!/usr/bin/env python3
"""
继电器测试 - periphery 版本 (树莓派 5 推荐)
用法：sudo python3 relay_periphery_test.py
"""

import time
import sys

try:
    from periphery import GPIO
    print("✅ periphery 库已安装")
except ImportError:
    print("❌ periphery 库未安装")
    print("\n安装命令：")
    print("  sudo apt-get update")
    print("  sudo apt-get install -y python3-periphery")
    print("  或：pip3 install python-periphery")
    sys.exit(1)

GPIO_CHIP = 4  # gpiochip4
GPIO_LINE = 17  # line 17 = GPIO17

print("=" * 50)
print("🔌 继电器测试程序 (periphery 版本)")
print("=" * 50)
print(f"使用芯片：gpiochip{GPIO_CHIP}, line {GPIO_LINE}")
print(f"物理引脚：11 (GPIO17)")
print("")

try:
    # 初始化 GPIO
    print(f"📍 初始化 GPIO 芯片 {GPIO_CHIP}, line {GPIO_LINE}...")
    relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
    print("✅ GPIO 初始化成功")
    
    # 测试 1: 打开继电器
    print("\n📍 打开继电器... (3 秒)")
    relay.write(True)
    time.sleep(3)
    print("✅ 继电器已打开！应该听到'吧嗒'声")
    
    # 测试 2: 关闭继电器
    print("\n📍 关闭继电器... (3 秒)")
    relay.write(False)
    time.sleep(3)
    print("✅ 继电器已关闭")
    
    # 测试 3: 闪烁 5 次
    print("\n📍 闪烁测试 (5 次)...")
    for i in range(5):
        relay.write(True)
        time.sleep(0.5)
        relay.write(False)
        time.sleep(0.5)
        print(f"   闪烁 {i+1}/5 ✓")
    
    print("\n✅ 继电器测试完成！")
    
    # 清理
    relay.close()
    print("✅ GPIO 已关闭")
    
except KeyboardInterrupt:
    print("\n⚠️  用户中断")
except Exception as e:
    print(f"\n❌ 错误：{e}")
    print("\n可能的原因:")
    print("  1. GPIO 引脚号不对 (树莓派 5 的 GPIO 编号可能不同)")
    print("  2. 权限不足 (使用 sudo 运行)")
    print("  3. 接线问题")
    print("\n调试建议:")
    print("  运行：gpioinfo | grep -i gpio17")
    print("  查看 GPIO17 对应的实际 line 号")
finally:
    print("\n✅ 程序结束")
