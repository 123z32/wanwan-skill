#!/usr/bin/env python3
"""
飞书 LED 控制 - 通过飞书消息控制 LED + 光敏电阻
部署在容器里
"""

import requests
import json
import sys

# 配置
HOST_IP = "100.93.35.112"  # 树莓派宿主机 IP
PORT = 5000
BASE_URL = f"http://{HOST_IP}:{PORT}"

def control_led(action):
    """控制 LED"""
    try:
        if action == "on":
            r = requests.post(f"{BASE_URL}/led/on", timeout=5)
        elif action == "off":
            r = requests.post(f"{BASE_URL}/led/off", timeout=5)
        elif action == "toggle":
            r = requests.post(f"{BASE_URL}/led/toggle", timeout=5)
        elif action == "status":
            r = requests.get(f"{BASE_URL}/led/status", timeout=5)
        elif action == "pulse":
            r = requests.post(f"{BASE_URL}/led/pulse", json={"count": 3, "interval": 0.5}, timeout=10)
        else:
            return {"success": False, "error": f"未知命令：{action}"}
        
        if r.status_code == 200:
            return r.json()
        else:
            return {"success": False, "error": f"HTTP {r.status_code}: {r.text}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "无法连接到 GPIO 服务"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "请求超时"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def read_light_sensor():
    """读取光敏电阻"""
    try:
        r = requests.get(f"{BASE_URL}/sensor/light", timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            return {"success": False, "error": f"HTTP {r.status_code}: {r.text}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "无法连接到 GPIO 服务"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "请求超时"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_response(result, action):
    """格式化飞书回复"""
    if result.get("success"):
        if action == "on":
            return "💡 LED 已打开"
        elif action == "off":
            return "🌑 LED 已关闭"
        elif action == "toggle":
            state = "打开" if result.get("state") else "关闭"
            return f"💡 LED 已切换到：{state}"
        elif action == "status":
            state = "🟢 打开" if result.get("state") == "on" else "🔴 关闭"
            return f"📊 LED 状态：{state}"
        elif action == "pulse":
            return f"✨ LED 闪烁 {result.get('count', 3)} 次完成"
    else:
        return f"❌ 失败：{result.get('error', '未知错误')}"

def format_sensor_response(result):
    """格式化光敏电阻回复"""
    if result.get("success"):
        state = "☀️ 亮" if result.get("state") == "bright" else "🌙 暗"
        value = "HIGH" if result.get("value") else "LOW"
        pin = result.get("pin", 27)
        return f"📊 光敏电阻 (GPIO {pin}): {state} ({value})"
    else:
        return f"❌ 失败：{result.get('error', '未知错误')}"

def main():
    """主函数 - 从命令行参数读取动作"""
    if len(sys.argv) < 2:
        print("用法：python3 feishu_relay_control.py [on|off|toggle|status|pulse|light]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == "light":
        # 读取光敏电阻
        print(f"📍 读取光敏电阻...")
        result = read_light_sensor()
        response = format_sensor_response(result)
        print(response)
        
        # 返回 JSON 给 OpenClaw
        print("\n--- JSON Output ---")
        print(json.dumps({
            "action": "light_sensor",
            "success": result.get("success", False),
            "message": response,
            "data": result
        }, ensure_ascii=False))
    elif action in ["on", "off", "toggle", "status", "pulse"]:
        # 控制 LED
        print(f"📍 执行：{action}")
        result = control_led(action)
        response = format_response(result, action)
        print(response)
        
        # 返回 JSON 给 OpenClaw
        print("\n--- JSON Output ---")
        print(json.dumps({
            "action": action,
            "success": result.get("success", False),
            "message": response,
            "data": result
        }, ensure_ascii=False))
    else:
        print(f"❌ 未知命令：{action}")
        print("可用命令：on, off, toggle, status, pulse, light")
        sys.exit(1)

if __name__ == "__main__":
    main()
