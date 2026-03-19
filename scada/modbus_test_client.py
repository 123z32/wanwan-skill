#!/usr/bin/env python3
"""
Modbus TCP 测试客户端 - 验证树莓派服务
"""

import socket
import struct

HOST = "100.93.35.112"
PORT = 5020

def build_modbus_request(trans_id, unit_id, func_code, payload):
    """构建 Modbus TCP 请求"""
    length = len(payload) + 2  # 单元 ID + 功能码 + 数据
    header = struct.pack('>HHHB', trans_id, 0, length, unit_id)
    return header + bytes([func_code]) + payload

def read_coils(trans_id, unit_id, start_addr, quantity):
    """功能码 01: 读线圈"""
    payload = struct.pack('>HH', start_addr, quantity)
    return build_modbus_request(trans_id, unit_id, 0x01, payload)

def write_coil(trans_id, unit_id, addr, value):
    """功能码 05: 写单个线圈"""
    coil_value = 0xFF00 if value else 0x0000
    payload = struct.pack('>HH', addr, coil_value)
    return build_modbus_request(trans_id, unit_id, 0x05, payload)

def parse_response(data):
    """解析响应"""
    if len(data) < 8:
        return None
    
    trans_id = struct.unpack('>H', data[0:2])[0]
    proto_id = struct.unpack('>H', data[2:4])[0]
    length = struct.unpack('>H', data[4:6])[0]
    unit_id = data[6]
    fc = data[7]
    payload = data[8:]
    
    return {
        'trans_id': trans_id,
        'proto_id': proto_id,
        'length': length,
        'unit_id': unit_id,
        'fc': fc,
        'payload': payload
    }

def test_modbus():
    """测试 Modbus 通信"""
    print(f"\n📡 连接 {HOST}:{PORT}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((HOST, PORT))
        print("✅ 连接成功\n")
    except Exception as e:
        print(f"❌ 连接失败：{e}")
        return
    
    # 测试 1: 读线圈 (初始状态)
    print("1️⃣  测试：读线圈 (地址 0, 数量 1)")
    request = read_coils(1, 0, 0, 1)
    print(f"   发送：{request.hex()}")
    sock.sendall(request)
    
    response = sock.recv(1024)
    print(f"   接收：{response.hex()}")
    
    resp = parse_response(response)
    if resp:
        print(f"   ✅ 事务 ID: {resp['trans_id']}, 功能码：0x{resp['fc']:02X}")
        if resp['fc'] == 0x01 and len(resp['payload']) >= 1:
            byte_count = resp['payload'][0]
            value = resp['payload'][1] if byte_count > 0 else 0
            state = "ON" if (value & 0x01) else "OFF"
            print(f"   📊 线圈 0 状态：{state}")
    
    # 测试 2: 写线圈 (打开)
    print("\n2️⃣  测试：写线圈 (地址 0, 值 ON)")
    request = write_coil(2, 0, 0, True)
    print(f"   发送：{request.hex()}")
    sock.sendall(request)
    
    response = sock.recv(1024)
    print(f"   接收：{response.hex()}")
    
    resp = parse_response(response)
    if resp:
        print(f"   ✅ 事务 ID: {resp['trans_id']}, 功能码：0x{resp['fc']:02X}")
        if resp['fc'] == 0x05:
            print(f"   ✅ 写入成功")
    
    # 等待同步
    import time
    time.sleep(0.2)
    
    # 测试 3: 读线圈 (验证状态)
    print("\n3️⃣  测试：读线圈 (验证状态)")
    request = read_coils(3, 0, 0, 1)
    print(f"   发送：{request.hex()}")
    sock.sendall(request)
    
    response = sock.recv(1024)
    print(f"   接收：{response.hex()}")
    
    resp = parse_response(response)
    if resp:
        print(f"   ✅ 事务 ID: {resp['trans_id']}, 功能码：0x{resp['fc']:02X}")
        if resp['fc'] == 0x01 and len(resp['payload']) >= 1:
            value = resp['payload'][1]
            state = "ON" if (value & 0x01) else "OFF"
            print(f"   📊 线圈 0 状态：{state}")
    
    # 测试 4: 写线圈 (关闭)
    print("\n4️⃣  测试：写线圈 (地址 0, 值 OFF)")
    request = write_coil(4, 0, 0, False)
    print(f"   发送：{request.hex()}")
    sock.sendall(request)
    
    response = sock.recv(1024)
    print(f"   接收：{response.hex()}")
    
    resp = parse_response(response)
    if resp:
        print(f"   ✅ 写入成功")
    
    sock.close()
    print("\n✅ 测试完成\n")

if __name__ == "__main__":
    test_modbus()
