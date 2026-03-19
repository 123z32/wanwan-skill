#!/usr/bin/env python3
"""
Modbus TCP 上位机测试脚本 - 模拟 LabVIEW 控制
用于测试树莓派 Modbus 服务

用法:
  python3 modbus_client_test.py [树莓派 IP] [端口]
  例如：python3 modbus_client_test.py 100.93.35.112 5020
"""

import sys
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# 默认配置
DEFAULT_HOST = "100.93.35.112"
DEFAULT_PORT = 5020
COIL_ADDRESS = 0

def print_status(host, port, connected):
    """打印连接状态"""
    print("\n" + "=" * 50)
    if connected:
        print(f"✅ 已连接到 Modbus 服务器：{host}:{port}")
    else:
        print(f"❌ 无法连接到 Modbus 服务器：{host}:{port}")
    print("=" * 50)

def read_coil(client, address):
    """读取单个线圈状态"""
    try:
        result = client.read_coils(address, 1)
        if result.isError():
            print(f"⚠️  读取错误：{result}")
            return None
        return result.bits[0]
    except ModbusException as e:
        print(f"❌ Modbus 异常：{e}")
        return None

def write_coil(client, address, value):
    """写入单个线圈"""
    try:
        result = client.write_coil(address, value)
        if result.isError():
            print(f"⚠️  写入错误：{result}")
            return False
        return True
    except ModbusException as e:
        print(f"❌ Modbus 异常：{e}")
        return False

def interactive_mode(client):
    """交互式控制模式"""
    print("\n📖 交互模式 - 输入命令控制继电器")
    print("   命令：on / off / toggle / status / quit")
    print("")
    
    while True:
        try:
            cmd = input(">>> ").strip().lower()
            
            if cmd == "quit" or cmd == "exit":
                print("👋 退出控制")
                break
            
            elif cmd == "on":
                print("📤 发送：打开继电器")
                if write_coil(client, COIL_ADDRESS, True):
                    print("✅ 指令发送成功")
            
            elif cmd == "off":
                print("📤 发送：关闭继电器")
                if write_coil(client, COIL_ADDRESS, False):
                    print("✅ 指令发送成功")
            
            elif cmd == "toggle":
                current = read_coil(client, COIL_ADDRESS)
                if current is not None:
                    new_state = not current
                    print(f"📤 发送：切换继电器 ({'OFF->ON' if new_state else 'ON->OFF'})")
                    if write_coil(client, COIL_ADDRESS, new_state):
                        print("✅ 指令发送成功")
            
            elif cmd == "status":
                state = read_coil(client, COIL_ADDRESS)
                if state is not None:
                    state_str = "🟢 ON" if state else "🔴 OFF"
                    print(f"📊 当前状态：{state_str}")
            
            else:
                print("⚠️  未知命令，输入 on/off/toggle/status/quit")
        
        except KeyboardInterrupt:
            print("\n⚠️  中断")
            break
        except EOFError:
            break

def auto_test_mode(client):
    """自动测试模式"""
    print("\n🧪 自动测试模式")
    print("")
    
    # 测试 1: 读取初始状态
    print("1️⃣  读取初始状态...")
    state = read_coil(client, COIL_ADDRESS)
    if state is not None:
        print(f"   初始状态：{'ON' if state else 'OFF'}")
    else:
        print("   读取失败，跳过后续测试")
        return
    
    # 测试 2: 打开继电器
    print("\n2️⃣  打开继电器...")
    if write_coil(client, COIL_ADDRESS, True):
        time.sleep(0.5)
        state = read_coil(client, COIL_ADDRESS)
        print(f"   写入：ON, 读取验证：{'✅ ON' if state else '❌ OFF'}")
    
    # 测试 3: 关闭继电器
    print("\n3️⃣  关闭继电器...")
    if write_coil(client, COIL_ADDRESS, False):
        time.sleep(0.5)
        state = read_coil(client, COIL_ADDRESS)
        print(f"   写入：OFF, 读取验证：{'✅ OFF' if not state else '❌ ON'}")
    
    # 测试 4: 快速切换
    print("\n4️⃣  快速切换测试 (3 次)...")
    for i in range(3):
        write_coil(client, COIL_ADDRESS, True)
        time.sleep(0.3)
        write_coil(client, COIL_ADDRESS, False)
        time.sleep(0.3)
        print(f"   脉冲 {i+1}/3 ✓")
    
    print("\n✅ 测试完成")

def main():
    """主函数"""
    # 解析命令行参数
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    
    print("\n" + "=" * 50)
    print("   🖥️  Modbus TCP 上位机测试工具")
    print("=" * 50)
    print(f"   目标服务器：{host}:{port}")
    print(f"   控制地址：Coil {COIL_ADDRESS}")
    print("=" * 50)
    
    # 连接服务器
    client = ModbusTcpClient(host, port=port)
    
    try:
        print(f"\n📡 正在连接 {host}:{port}...")
        client.connect()
        
        if client.connected:
            print_status(host, port, True)
            
            # 选择模式
            print("\n选择测试模式:")
            print("   1 - 自动测试 (快速验证)")
            print("   2 - 交互控制 (手动测试)")
            
            choice = input("\n输入选项 [1/2]: ").strip()
            
            if choice == "2":
                interactive_mode(client)
            else:
                auto_test_mode(client)
                # 询问是否进入交互模式
                again = input("\n是否进入交互模式？[y/N]: ").strip().lower()
                if again == "y":
                    interactive_mode(client)
        else:
            print_status(host, port, False)
            print("\n⚠️  请确认:")
            print("   1. 树莓派 Modbus 服务已启动")
            print("   2. IP 地址和端口正确")
            print("   3. 防火墙允许连接")
    
    except Exception as e:
        print(f"\n❌ 错误：{e}")
    
    finally:
        # 关闭连接
        client.close()
        print("\n👋 连接已关闭\n")

if __name__ == "__main__":
    main()
