#!/usr/bin/env python3
"""
飞书继电器控制 - 通过飞书消息控制 GPIO
部署在容器里
"""

import requests
import json
import sys

# 配置
HOST_IP = "100.93.35.112"  # 树莓派宿主机 IP
PORT = 5000
BASE_URL = f"http://{HOST_IP}:{PORT}"

def control_relay(action):
    """控制继电器"""
    try:
        if action == "on":
            r = requests.post(f"{BASE_URL}/relay/on", timeout=5)
        elif action == "off":
            r = requests.post(f"{BASE_URL}/relay/off", timeout=5)
        elif action == "toggle":
            r = requests.post(f"{BASE_URL}/relay/toggle", timeout=5)
        elif action == "status":
            r = requests.get(f"{BASE_URL}/relay/status", timeout=5)
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

def format_response(result, action):
    """格式化飞书回复"""
    if result.get("success"):
        if action == "on":
            return "✅ 继电器已打开"
        elif action == "off":
            return "✅ 继电器已关闭"
        elif action == "toggle":
            state = "打开" if result.get("state") else "关闭"
            return f"✅ 继电器已切换到：{state}"
        elif action == "status":
            state = "🟢 打开" if result.get("state") == "on" else "🔴 关闭"
            return f"📊 继电器状态：{state}"
    else:
        return f"❌ 失败：{result.get('error', '未知错误')}"

def main():
    """主函数 - 从命令行参数读取动作"""
    if len(sys.argv) < 2:
        print("用法：python3 feishu_relay_control.py [on|off|toggle|status]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action not in ["on", "off", "toggle", "status"]:
        print(f"❌ 未知命令：{action}")
        print("可用命令：on, off, toggle, status")
        sys.exit(1)
    
    print(f"📍 执行：{action}")
    result = control_relay(action)
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

if __name__ == "__main__":
    main()
