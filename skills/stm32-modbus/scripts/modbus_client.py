#!/usr/bin/env python3
"""
Modbus Client CLI for STM32 via TCP bridge.
Usage:
  python3 modbus_client.py read-coil 0 16
  python3 modbus_client.py write-coil 0 on
  python3 modbus_client.py read-reg 0 1
  python3 modbus_client.py write-reg 0 100
  python3 modbus_client.py send "01 03 00 00 00 01"
  python3 modbus_client.py status
"""

import socket
import sys
import json
import struct
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8086
MODBUS_ADDR = 0x01


def calc_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def build_frame(addr, fc, payload: bytes) -> bytes:
    frame = struct.pack('>BB', addr, fc) + payload
    crc = calc_crc16(frame)
    return frame + struct.pack('<H', crc)


def read_coil(start, quantity):
    payload = struct.pack('>HH', start, quantity)
    return build_frame(MODBUS_ADDR, 0x01, payload)


def read_discrete(start, quantity):
    payload = struct.pack('>HH', start, quantity)
    return build_frame(MODBUS_ADDR, 0x02, payload)


def read_reg(start, quantity):
    payload = struct.pack('>HH', start, quantity)
    return build_frame(MODBUS_ADDR, 0x03, payload)


def write_coil(addr_coil, value):
    val = 0xFF00 if value.lower() in ('on', '1', 'true', '开', '打开') else 0x0000
    payload = struct.pack('>HH', addr_coil, val)
    return build_frame(MODBUS_ADDR, 0x05, payload)


def write_reg(addr_reg, value):
    payload = struct.pack('>HH', addr_reg, int(value))
    return build_frame(MODBUS_ADDR, 0x06, payload)


def parse_response(data: bytes) -> str:
    if len(data) < 3:
        return f"响应太短: {data.hex().upper()}"

    fc = data[1]
    result = []

    if fc == 0x01 or fc == 0x02:
        # 读线圈/离散输入
        byte_count = data[2]
        result.append(f"字节数: {byte_count}")
        coils = []
        for i in range(byte_count):
            byte = data[3 + i]
            for bit in range(8):
                coils.append(1 if (byte >> bit) & 1 else 0)
        result.append(f"线圈状态: {coils}")
        on_count = sum(coils)
        result.append(f"ON: {on_count} / 总计: {len(coils)}")

    elif fc == 0x03 or fc == 0x04:
        # 读寄存器
        byte_count = data[2]
        result.append(f"字节数: {byte_count}")
        for i in range(byte_count // 2):
            val = struct.unpack('>H', data[3 + i*2:5 + i*2])[0]
            result.append(f"寄存器[{i}]: {val} (0x{val:04X})")

    elif fc == 0x05:
        # 写线圈响应
        coil_addr = struct.unpack('>H', data[2:4])[0]
        coil_val = struct.unpack('>H', data[4:6])[0]
        result.append(f"线圈[{coil_addr}] = {'ON' if coil_val == 0xFF00 else 'OFF'}")

    elif fc == 0x06:
        # 写寄存器响应
        reg_addr = struct.unpack('>H', data[2:4])[0]
        reg_val = struct.unpack('>H', data[4:6])[0]
        result.append(f"寄存器[{reg_addr}] = {reg_val}")

    elif fc & 0x80:
        # 错误响应
        error_code = data[2]
        errors = {
            0x01: "非法功能码",
            0x02: "非法数据地址",
            0x03: "非法数据值",
            0x04: "从站设备故障",
            0x05: "确认",
            0x06: "从站忙",
            0x08: "存储奇偶校验错",
        }
        result.append(f"错误码: 0x{error_code:02X} - {errors.get(error_code, '未知错误')}")

    return "\n".join(result)


def send_hex(hex_str):
    raw = bytes.fromhex(hex_str.replace(' ', ''))
    return raw


def send_and_receive(data: bytes, timeout: float = 5.0) -> bytes:
    """直接发送并接收（TCP 同步模式）"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.sendall(data)
        response = sock.recv(256)
        return response
    finally:
        sock.close()


def get_status():
    """尝试连接服务器并检查"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.close()
        return {"server": "online", "host": SERVER_HOST, "port": SERVER_PORT}
    except:
        return {"server": "offline", "host": SERVER_HOST, "port": SERVER_PORT}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == 'status':
        status = get_status()
        print(json.dumps(status, indent=2))
        sys.exit(0)

    if cmd == 'send':
        if len(sys.argv) < 3:
            print("用法: send <hex_data>")
            sys.exit(1)
        data = send_hex(sys.argv[2])
    elif cmd == 'read-coil':
        start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        qty = int(sys.argv[3]) if len(sys.argv) > 3 else 16
        data = read_coil(start, qty)
    elif cmd == 'read-discrete':
        start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        qty = int(sys.argv[3]) if len(sys.argv) > 3 else 16
        data = read_discrete(start, qty)
    elif cmd == 'read-reg' or cmd == 'read-register':
        start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        qty = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        data = read_reg(start, qty)
    elif cmd == 'write-coil':
        if len(sys.argv) < 4:
            print("用法: write-coil <address> <on|off>")
            sys.exit(1)
        data = write_coil(int(sys.argv[2]), sys.argv[3])
    elif cmd == 'write-reg' or cmd == 'write-register':
        if len(sys.argv) < 4:
            print("用法: write-reg <address> <value>")
            sys.exit(1)
        data = write_reg(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)

    print(f"[TX] {data.hex().upper()}")

    try:
        response = send_and_receive(data)
        if response:
            print(f"[RX] {response.hex().upper()}")
            print("---")
            print(parse_response(response))
        else:
            print("无响应（超时）")
    except socket.timeout:
        print("⚠️ 连接超时 - ESP8266 未连接或网络不可达")
    except ConnectionRefusedError:
        print("❌ 连接被拒绝 - TCP 服务器未运行")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    main()
