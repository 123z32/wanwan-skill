#!/usr/bin/env python3
"""
继电器测试 - sysfs 版本 (树莓派 5 Ubuntu 24.04)
用法：sudo python3 relay_sysfs_test.py
"""

import os
import time

GPIO_PIN = 17
GPIO_PATH = f"/sys/class/gpio/gpio{GPIO_PIN}"

def gpio_export():
    """导出 GPIO 引脚"""
    if not os.path.exists(GPIO_PATH):
        with open("/sys/class/gpio/export", "w") as f:
            f.write(str(GPIO_PIN))
        time.sleep(0.1)
        print(f"✅ 导出 GPIO{GPIO_PIN}")
    else:
        print(f"✅ GPIO{GPIO_PIN} 已导出")

def gpio_unexport():
    """取消导出 GPIO 引脚"""
    if os.path.exists(GPIO_PATH):
        with open("/sys/class/gpio/unexport", "w") as f:
            f.write(str(GPIO_PIN))
        print(f"✅ 取消导出 GPIO{GPIO_PIN}")

def gpio_set_direction(direction="out"):
    """设置方向"""
    with open(f"{GPIO_PATH}/direction", "w") as f:
        f.write(direction)
    print(f"✅ 设置为 {direction} 模式")

def gpio_write(value):
    """写入值 (0 或 1)"""
    with open(f"{GPIO_PATH}/value", "w") as f:
        f.write(str(value))
    status = "HIGH" if value else "LOW"
    print(f"✅ 输出 {status}")

def main():
    print("=" * 50)
    print("🔌 继电器测试程序 (sysfs 版本)")
    print("=" * 50)
    print(f"使用引脚：GPIO{GPIO_PIN} (物理引脚 11)")
    print("")
    
    try:
        # 导出 GPIO
        gpio_export()
        
        # 设置方向
        gpio_set_direction("out")
        
        # 测试 1: 打开继电器
        print("\n📍 打开继电器... (3 秒)")
        gpio_write(1)
        time.sleep(3)
        print("✅ 继电器已打开！应该听到'吧嗒'声")
        
        # 测试 2: 关闭继电器
        print("\n📍 关闭继电器... (3 秒)")
        gpio_write(0)
        time.sleep(3)
        print("✅ 继电器已关闭")
        
        # 测试 3: 闪烁 5 次
        print("\n📍 闪烁测试 (5 次)...")
        for i in range(5):
            gpio_write(1)
            time.sleep(0.5)
            gpio_write(0)
            time.sleep(0.5)
            print(f"   闪烁 {i+1}/5 ✓")
        
        print("\n✅ 继电器测试完成！")
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n提示:")
        print("  1. 确认使用 sudo 运行")
        print("  2. 检查接线是否正确")
        print("  3. 确认继电器模块供电 (5V)")
    finally:
        # 清理
        gpio_unexport()
        print("\n✅ GPIO 已清理")

if __name__ == "__main__":
    main()
