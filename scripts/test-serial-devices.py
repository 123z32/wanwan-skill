#!/usr/bin/env python3
"""
串口设备测试脚本
验证容器内是否可访问 USB 串口和硬件串口
"""

import os
import glob

def check_device(path):
    """检查设备是否存在"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {path}: {'存在' if exists else '不存在'}")
    
    if exists:
        # 读取设备权限
        stat_info = os.stat(path)
        print(f"   权限：{oct(stat_info.st_mode)[-3:]}")
        print(f"   所有者：UID={stat_info.st_uid}, GID={stat_info.st_gid}")
    
    return exists

def list_serial_devices():
    """列出所有串口设备"""
    print("\n🔍 查找串口设备...\n")
    
    # USB 串口
    print("📌 USB 串口 (/dev/ttyUSB*):")
    usb_devices = glob.glob("/dev/ttyUSB*")
    if usb_devices:
        for dev in usb_devices:
            check_device(dev)
    else:
        print("   未找到 USB 串口设备")
    
    # 硬件串口
    print("\n📌 硬件串口 (/dev/ttyAMA*):")
    ama_devices = glob.glob("/dev/ttyAMA*")
    if ama_devices:
        for dev in ama_devices:
            check_device(dev)
    else:
        print("   未找到硬件串口设备")
    
    # mini UART
    print("\n📌 Mini UART (/dev/ttyS*):")
    s_devices = glob.glob("/dev/ttyS*")
    if s_devices:
        for dev in s_devices:
            check_device(dev)
    else:
        print("   未找到 Mini UART 设备")
    
    # serial0 别名
    print("\n📌 Serial0 别名 (/dev/serial*):")
    serial_devices = glob.glob("/dev/serial*")
    if serial_devices:
        for dev in serial_devices:
            if os.path.islink(dev):
                target = os.readlink(dev)
                print(f"✅ {dev} -> {target}")
            else:
                check_device(dev)
    else:
        print("   未找到 serial 别名设备")

def test_serial_import():
    """测试 pyserial 是否可用"""
    print("\n🔧 测试 pyserial 库...")
    try:
        import serial
        import serial.tools.list_ports
        
        ports = serial.tools.list_ports.comports()
        if ports:
            print(f"✅ 找到 {len(ports)} 个串口：")
            for port in ports:
                print(f"   - {port.device}: {port.description}")
        else:
            print("⚠️  pyserial 已安装，但未找到串口")
            
    except ImportError:
        print("❌ pyserial 未安装")
        print("   安装命令：pip3 install pyserial")

if __name__ == "__main__":
    print("=" * 60)
    print("🔌 串口设备测试工具")
    print("=" * 60)
    
    list_serial_devices()
    test_serial_import()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
