#!/usr/bin/env python3
"""
GPIO HTTP 服务 - 让容器可以控制 GPIO
运行在树莓派宿主机上
"""

from flask import Flask, request, jsonify
from periphery import GPIO
import logging

app = Flask(__name__)

# 配置
GPIO_CHIP = 4
GPIO_LINE = 17
relay = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GPIO_Service')

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "gpio-http"})

@app.route('/relay/on', methods=['POST'])
def relay_on():
    """打开继电器"""
    global relay
    try:
        if relay is None:
            relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        relay.write(True)
        logger.info("继电器：ON")
        return jsonify({"success": True, "action": "on"})
    except Exception as e:
        logger.error(f"打开失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/relay/off', methods=['POST'])
def relay_off():
    """关闭继电器"""
    global relay
    try:
        if relay is None:
            relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        relay.write(False)
        logger.info("继电器：OFF")
        return jsonify({"success": True, "action": "off"})
    except Exception as e:
        logger.error(f"关闭失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/relay/toggle', methods=['POST'])
def relay_toggle():
    """切换继电器状态"""
    global relay
    try:
        if relay is None:
            relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        current = relay.read()
        relay.write(not current)
        logger.info(f"继电器：TOGGLE -> {'ON' if not current else 'OFF'}")
        return jsonify({"success": True, "action": "toggle", "state": not current})
    except Exception as e:
        logger.error(f"切换失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/relay/status', methods=['GET'])
def relay_status():
    """获取继电器状态"""
    global relay
    try:
        if relay is None:
            relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        state = relay.read()
        return jsonify({"success": True, "state": "on" if state else "off"})
    except Exception as e:
        logger.error(f"读取状态失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/relay/pulse', methods=['POST'])
def relay_pulse():
    """脉冲输出（闪烁）"""
    global relay
    try:
        if relay is None:
            relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        
        data = request.get_json() or {}
        count = data.get('count', 3)
        interval = data.get('interval', 0.5)
        
        for i in range(count):
            relay.write(True)
            time.sleep(interval)
            relay.write(False)
            time.sleep(interval)
            logger.info(f"脉冲 {i+1}/{count}")
        
        return jsonify({"success": True, "action": "pulse", "count": count})
    except Exception as e:
        logger.error(f"脉冲失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    import time
    
    logger.info("=" * 50)
    logger.info("🔌 GPIO HTTP 服务启动")
    logger.info("=" * 50)
    logger.info(f"GPIO 芯片：gpiochip{GPIO_CHIP}, line {GPIO_LINE}")
    logger.info("监听端口：5000")
    logger.info("")
    logger.info("API 端点:")
    logger.info("  POST /relay/on      - 打开继电器")
    logger.info("  POST /relay/off     - 关闭继电器")
    logger.info("  POST /relay/toggle  - 切换状态")
    logger.info("  GET  /relay/status  - 获取状态")
    logger.info("  POST /relay/pulse   - 脉冲输出")
    logger.info("  GET  /health        - 健康检查")
    logger.info("")
    
    # 初始化 GPIO
    try:
        relay = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        relay.write(False)
        logger.info("✅ GPIO 初始化成功")
    except Exception as e:
        logger.error(f"❌ GPIO 初始化失败：{e}")
        logger.error("请确认使用 sudo 运行")
        exit(1)
    
    # 启动 Flask 服务
    app.run(host='0.0.0.0', port=5000, debug=False)
