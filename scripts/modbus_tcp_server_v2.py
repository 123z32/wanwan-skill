#!/usr/bin/env python3
"""
Modbus TCP Bridge Server v2.1 - ESP8266 透传

修复：按 IP 自动识别 ESP vs 客户端
- 10.74.24.x / 192.168.1.x → ESP（持久连接）
- 172.18.0.x / 其他 → 客户端（请求-响应）
"""

import socket
import threading
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 8086

# ESP 连接池
esp_connections = []   # [{'conn': ..., 'addr': ..., 'busy': False}, ...]
esp_lock = threading.Lock()

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_esp_ip(addr):
    """判断是否是 ESP8266 的 IP"""
    return addr.startswith('10.74.24') or addr.startswith('192.168.1')

def handle_esp(conn, addr):
    """ESP8266 持久连接"""
    with esp_lock:
        esp_connections.append({'conn': conn, 'addr': addr, 'busy': False})
    print(f"[{ts()}] ✅ ESP 已连接: {addr[0]}:{addr[1]} (在线: {len(esp_connections)})")
    
    conn.settimeout(120)
    try:
        while True:
            try:
                data = conn.recv(512)
                if not data:
                    break
                print(f"[{ts()}] 📥 ESP→: {data.hex().upper()} ({len(data)}B)")
            except socket.timeout:
                continue
            except ConnectionResetError:
                break
    except Exception as e:
        print(f"[{ts()}] ❌ ESP 异常: {e}")
    finally:
        with esp_lock:
            esp_connections[:] = [e for e in esp_connections if e['conn'] != conn]
        conn.close()
        print(f"[{ts()}] ❌ ESP 断开: {addr[0]}:{addr[1]} (在线: {len(esp_connections)})")

def handle_client(conn, addr):
    """客户端连接：发命令 → 等响应 → 断开"""
    print(f"[{ts()}] 🔗 客户端: {addr[0]}:{addr[1]}")
    conn.settimeout(10)
    
    try:
        # 接收 Modbus 帧
        cmd_data = conn.recv(512)
        if not cmd_data:
            return
        print(f"[{ts()}] 📤 Client→: {cmd_data.hex().upper()} ({len(cmd_data)}B)")
        
        # 找空闲 ESP
        esp = None
        for _ in range(30):
            with esp_lock:
                for e in esp_connections:
                    if not e['busy']:
                        e['busy'] = True
                        esp = e
                        break
            if esp:
                break
            time.sleep(0.1)
        
        if not esp:
            msg = f"ERROR: No ESP connected (在线: {len(esp_connections)})"
            print(f"[{ts()}] ⚠️ {msg}")
            conn.sendall(msg.encode())
            return
        
        try:
            # 发送给 ESP
            esp['conn'].sendall(cmd_data)
            print(f"[{ts()}] 📡 →ESP({esp['addr'][0]}): {cmd_data.hex().upper()}")
            
            # 等待响应
            response = b''
            start = time.time()
            while time.time() - start < 8:
                try:
                    esp['conn'].settimeout(1)
                    chunk = esp['conn'].recv(512)
                    if chunk:
                        response += chunk
                        print(f"[{ts()}] 📥 ESP→: {chunk.hex().upper()} ({len(chunk)}B)")
                        
                        # 检查 Modbus 响应完整性
                        if len(response) >= 5:
                            fc = response[1]
                            if fc & 0x80:  # 错误
                                break
                            elif fc in (0x01, 0x02):
                                if len(response) >= 4:
                                    bc = response[2]
                                    if len(response) >= 5 + bc:
                                        break
                            elif fc in (0x03, 0x04):
                                if len(response) >= 4:
                                    bc = response[2]
                                    if len(response) >= 5 + bc:
                                        break
                            elif fc in (0x05, 0x06):
                                if len(response) >= 8:
                                    break
                except socket.timeout:
                    continue
            
            if response:
                print(f"[{ts()}] 📤 →Client: {response.hex().upper()} ({len(response)}B)")
                conn.sendall(response)
            else:
                print(f"[{ts()}] ⏰ 超时")
                conn.sendall(b"ERROR: Timeout")
        finally:
            with esp_lock:
                esp['busy'] = False
        
    except socket.timeout:
        print(f"[{ts()}] ⏰ 客户端超时")
    except Exception as e:
        print(f"[{ts()}] ❌ 客户端异常: {e}")
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(20)
    
    import subprocess
    try:
        ip = subprocess.getoutput("hostname -I | awk '{print $1}'").strip()
    except:
        ip = "unknown"
    
    print(f"{'='*50}")
    print(f"  Modbus TCP Bridge Server v2.1")
    print(f"  监听: {HOST}:{PORT}")
    print(f"  本机IP: {ip}")
    print(f"  ESP 识别: 10.74.24.x 或 192.168.1.x")
    print(f"  等待连接...")
    print(f"{'='*50}")
    
    while True:
        try:
            conn, addr = server.accept()
            
            if is_esp_ip(addr[0]):
                t = threading.Thread(target=handle_esp, args=(conn, addr), daemon=True)
                print(f"[{ts()}] 📡 识别为 ESP: {addr[0]}")
            else:
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                print(f"[{ts()}] 📡 识别为客户端: {addr[0]}")
            t.start()
        except Exception as e:
            print(f"[{ts()}] ❌ 服务器异常: {e}")

if __name__ == '__main__':
    main()
