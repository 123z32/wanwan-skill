#!/usr/bin/env python3
"""
从容器控制 GPIO - 通过 HTTP API 调用宿主机的 GPIO 服务
"""

import requests
import time
import sys

# 宿主机 IP（树莓派的 Tailscale IP）
HOST_IP = "100.93.35.112"
PORT = 5000
BASE_URL = f"http://{HOST_IP}:{PORT}"

def relay_on():
    """打开继电器"""
    r = requests.post(f"{BASE_URL}/relay/on")
    if r.status_code == 200:
        print("✅ 继电器：ON")
        return True
    else:
        print(f"❌ 失败：{r.text}")
        return False

def relay_off():
    """关闭继电器"""
    r = requests.post(f"{BASE_URL}/relay/off")
    if r.status_code == 200:
        print("✅ 继电器：OFF")
        return True
    else:
        print(f"❌ 失败：{r.text}")
        return False

def relay_toggle():
    """切换继电器状态"""
    r = requests.post(f"{BASE_URL}/relay/toggle")
    if r.status_code == 200:
        data = r.json()
        state = "ON" if data.get('state') else "OFF"
        print(f"✅ 继电器：TOGGLE -> {state}")
        return True
    else:
        print(f"❌ 失败：{r.text}")
        return False

def relay_status():
    """获取继电器状态"""
    r = requests.get(f"{BASE_URL}/relay/status")
    if r.status_code == 200:
        data = r.json()
        state = "ON" if data.get('state') == 'on' else "OFF"
        print(f"📊 继电器状态：{state}")
        return state
    else:
        print(f"❌ 失败：{r.text}")
        return None

def relay_pulse(count=3, interval=0.5):
    """脉冲输出（闪烁）"""
    r = requests.post(f"{BASE_URL}/relay/pulse", json={
        "count": count,
        "interval": interval
    })
    if r.status_code == 200:
        print(f"✅ 脉冲完成：{count} 次")
        return True
    else:
        print(f"❌ 失败：{r.text}")
        return False

def health_check():
    """健康检查"""
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=2)
        if r.status_code == 200:
            print(f"✅ 服务正常：{r.json()}")
            return True
    except:
        pass
    print("❌ 服务不可用")
    return False

def main():
    print("=" * 50)
    print("🔌 继电器控制 (容器 → 宿主机)")
    print("=" * 50)
    print(f"宿主机：{HOST_IP}:{PORT}")
    print("")
    
    # 健康检查
    print("📍 检查服务...")
    if not health_check():
        print("\n错误：GPIO 服务未运行")
        print("请在树莓派宿主机上运行:")
        print("  sudo python3 /mnt/ssd/openclaw_data/.openclaw/workspace/scada/gpio_http_service.py")
        sys.exit(1)
    
    # 获取状态
    print("\n📍 获取当前状态...")
    relay_status()
    
    # 测试打开
    print("\n📍 打开继电器... (3 秒)")
    relay_on()
    time.sleep(3)
    
    # 测试关闭
    print("\n📍 关闭继电器... (3 秒)")
    relay_off()
    time.sleep(3)
    
    # 测试闪烁
    print("\n📍 闪烁测试 (5 次)...")
    relay_pulse(count=5, interval=0.5)
    
    print("\n✅ 测试完成！")
    print("\n💡 提示:")
    print("  在容器里可以随时调用:")
    print("    python3 relay_container_control.py on")
    print("    python3 relay_container_control.py off")
    print("    python3 relay_container_control.py toggle")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='继电器控制')
    parser.add_argument('action', nargs='?', choices=['on', 'off', 'toggle', 'status', 'test'], default='test')
    args = parser.parse_args()
    
    if args.action == 'on':
        relay_on()
    elif args.action == 'off':
        relay_off()
    elif args.action == 'toggle':
        relay_toggle()
    elif args.action == 'status':
        relay_status()
    else:
        main()
