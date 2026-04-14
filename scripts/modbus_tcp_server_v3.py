#!/usr/bin/env python3
"""
Modbus TCP Bridge Server v3 - 请求-响应模式

每个客户端连接发送一条 Modbus 命令后，服务器转发给 ESP，
等待 ESP 返回响应，然后返回给客户端，最后关闭连接。

每条命令一个独立的 TCP 请求-响应周期。
"""

import socket
import threading
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 8086

# ESP 持久连接
esp_socket = None
esp_lock = threading.Lock()
esp_connected = threading.Event()

# 客户端响应传递
response_buffer = {'data': None}
response_lock = threading.Lock()
response_ready = threading.Event()


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def handle_esp(conn, addr):
    """ESP8266 持久连接：接收 STM32 响应并传递给等待的客户端"""
    global esp_socket
    
    with esp_lock:
        esp_socket = conn
    esp_connected.set()
    print(f"[{ts()}] ✅ ESP 已连接: {addr[0]}:{addr[1]}")
    
    try:
        while True:
            data = conn.recv(512)
            if not data:
                break
            print(f"[{ts()}] 📥 ESP→: {data.hex().upper()} ({len(data)}B)")
            
            # 如果有客户端在等待响应，传递给它
            with response_lock:
                response_buffer['data'] = data
            response_ready.set()
    except Exception as e:
        print(f"[{ts()}] ❌ ESP 异常: {e}")
    finally:
        with esp_lock:
            esp_socket = None
        esp_connected.clear()
        print(f"[{ts()}] ❌ ESP 断开")


def handle_client(conn, addr):
    """客户端：接收命令 → 转发给 ESP → 等待响应 → 返回 → 关闭"""
    print(f"[{ts()}] 🔗 客户端: {addr[0]}:{addr[1]}")
    
    try:
        # 1. 接收客户端命令
        cmd = conn.recv(512)
        if not cmd:
            return
        print(f"[{ts()}] 📤 Client→ESP: {cmd.hex().upper()} ({len(cmd)}B)")
        
        # 2. 检查 ESP 连接
        if not esp_connected.is_set():
            print(f"[{ts()}] ⚠️ ESP 未连接")
            conn.sendall(b"ERROR: ESP not connected")
            return
        
        # 3. 清空响应缓冲区
        with response_lock:
            response_buffer['data'] = None
        response_ready.clear()
        
        # 4. 发送给 ESP
        with esp_lock:
            if esp_socket:
                esp_socket.sendall(cmd)
            else:
                conn.sendall(b"ERROR: ESP disconnected")
                return
        
        # 5. 等待响应（最多 5 秒）
        if response_ready.wait(timeout=5):
            with response_lock:
                resp = response_buffer['data']
            if resp:
                print(f"[{ts()}] 📤 ESP→Client: {resp.hex().upper()} ({len(resp)}B)")
                conn.sendall(resp)
            else:
                conn.sendall(b"ERROR: Empty response")
        else:
            print(f"[{ts()}] ⏰ 超时 - ESP 未响应")
            conn.sendall(b"ERROR: Timeout")
        
    except Exception as e:
        print(f"[{ts()}] ❌ 客户端异常: {e}")
    finally:
        conn.close()


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
    print(f"  Modbus TCP Bridge Server v3")
    print(f"  监听: {HOST}:{PORT}")
    print(f"  本机IP: {ip}")
    print(f"  ESP 识别: 10.74.24.x 或 192.168.1.x")
    print(f"  等待连接...")
    print(f"{'='*50}")
    
    while True:
        try:
            conn, addr = server.accept()
            ip_str = addr[0]
            
            if ip_str.startswith('10.74.24') or ip_str.startswith('192.168.1'):
                t = threading.Thread(target=handle_esp, args=(conn, addr), daemon=True)
                print(f"[{ts()}] 📡 识别为 ESP: {ip_str}")
            else:
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                print(f"[{ts()}] 📡 识别为客户端: {ip_str}")
            t.start()
        except Exception as e:
            print(f"[{ts()}] ❌ 服务器异常: {e}")


if __name__ == '__main__':
    main()
