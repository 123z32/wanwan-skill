#!/usr/bin/env python3
"""
Modbus TCP Bridge Server for ESP8266 transparent bridge.
Listens on port 8086, relays Modbus RTU frames between ESP8266 clients and requesters.
Supports multiple concurrent ESP8266 connections.
"""

import socket
import threading
import json
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 8086

# 存储已连接的 ESP8266 客户端
esp_clients = []  # [(conn, addr, last_active), ...]
clients_lock = threading.Lock()

# 命令响应队列（用于 Python 主动发送 Modbus 命令到 ESP8266）
command_queue = []
command_results = {}
cmd_counter = 0
cmd_lock = threading.Lock()


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def handle_esp(conn, addr):
    """处理 ESP8266 连接 - 双向通信"""
    global cmd_counter
    with clients_lock:
        esp_clients.append((conn, addr, time.time()))
    print(f"[{get_timestamp()}] [+] ESP8266 Connected from {addr}")
    conn.settimeout(60)  # 60 秒超时

    try:
        while True:
            try:
                # 检查是否有待发送的命令
                with cmd_lock:
                    if command_queue:
                        cmd = command_queue.pop(0)
                        conn.sendall(cmd['data'])
                        print(f"[{get_timestamp()}] [TX->ESP] {cmd['data'].hex().upper()} (cmd_id={cmd['id']})")
                        # 暂存命令 ID 用于匹配响应
                        cmd['sent_time'] = time.time()

                # 接收 ESP8266 返回的数据
                data = conn.recv(256)
                if not data:
                    break
                print(f"[{get_timestamp()}] [RX<-ESP] {data.hex().upper()}")

                # 尝试匹配命令响应
                with cmd_lock:
                    # 查找最近发送的命令，假设返回的数据是对应的响应
                    for c in list(command_results.values()):
                        if not c.get('response') and time.time() - c.get('sent_time', 0) < 5:
                            c['response'] = data.hex().upper()
                            c['complete'] = True
                            break

                with clients_lock:
                    for i, (c, a, _) in enumerate(esp_clients):
                        if c == conn:
                            esp_clients[i] = (conn, addr, time.time())
                            break

            except socket.timeout:
                continue

    except Exception as e:
        print(f"[{get_timestamp()}] [!] ESP8266 Error: {e}")
    finally:
        with clients_lock:
            esp_clients[:] = [(c, a, t) for c, a, t in esp_clients if c != conn]
        conn.close()
        print(f"[{get_timestamp()}] [-] ESP8266 Disconnected from {addr}")


def send_modbus_command(hex_data: str, timeout: float = 5.0) -> dict:
    """发送 Modbus 命令到 ESP8266，等待响应"""
    global cmd_counter

    try:
        raw = bytes.fromhex(hex_data.replace(' ', ''))
    except ValueError:
        return {'error': '无效的 HEX 格式', 'hex_sent': hex_data}

    with cmd_lock:
        cmd_counter += 1
        cmd_id = cmd_counter
        cmd = {
            'id': cmd_id,
            'data': raw,
            'sent_time': None
        }
        command_results[cmd_id] = {
            'id': cmd_id,
            'hex_sent': hex_data,
            'response': None,
            'complete': False,
            'sent_time': time.time()
        }
        command_queue.append(cmd)

    print(f"[{get_timestamp()}] [CMD] 命令已入队: {hex_data} (cmd_id={cmd_id})")

    # 等待响应
    start = time.time()
    while time.time() - start < timeout:
        with cmd_lock:
            result = command_results.get(cmd_id)
            if result and result.get('complete'):
                # 清理
                del command_results[cmd_id]
                return {
                    'cmd_id': cmd_id,
                    'hex_sent': hex_data,
                    'response': result['response'],
                    'elapsed': round(time.time() - start, 2)
                }
        time.sleep(0.1)

    # 超时，清理
    with cmd_lock:
        if cmd_id in command_results:
            result = command_results.pop(cmd_id)
            return {
                'cmd_id': cmd_id,
                'hex_sent': hex_data,
                'response': None,
                'error': '超时（ESP8266 未响应）',
                'elapsed': round(time.time() - start, 2)
            }

    return {'error': '未知错误'}


def get_status() -> dict:
    """获取服务器状态"""
    with clients_lock:
        active = [(f"{a[0]}:{a[1]}", round(time.time() - t, 1)) for _, a, t in esp_clients]
    with cmd_lock:
        pending = len(command_queue)
    return {
        'port': PORT,
        'esp_connected': len(esp_clients),
        'esp_clients': active,
        'pending_commands': pending
    }


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    import subprocess
    try:
        ip = subprocess.getoutput("hostname -I | awk '{print $1}'").strip()
    except:
        ip = "unknown"

    print(f"{'='*50}")
    print(f"  Modbus TCP Bridge Server")
    print(f"  监听: {HOST}:{PORT}")
    print(f"  本机IP: {ip}")
    print(f"  等待 ESP8266 连接...")
    print(f"{'='*50}")

    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_esp, args=(conn, addr), daemon=True)
            t.start()
        except Exception as e:
            print(f"[{get_timestamp()}] [!] Server Error: {e}")


if __name__ == '__main__':
    main()
