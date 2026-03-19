#!/usr/bin/env python3
"""
LED GPIO HTTP 服务 - 让容器可以控制 LED
运行在树莓派宿主机上
"""

from flask import Flask, request, jsonify
from periphery import GPIO
import logging
import time

app = Flask(__name__)

# 配置 - LED 使用 GPIO 27 (可根据实际接线修改)
GPIO_CHIP = 4
GPIO_LINE = 27
led = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LED_Service')

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "led-http"})

@app.route('/led/on', methods=['POST'])
def led_on():
    """打开 LED"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        led.write(True)
        logger.info("LED: ON")
        return jsonify({"success": True, "action": "on"})
    except Exception as e:
        logger.error(f"打开失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/led/off', methods=['POST'])
def led_off():
    """关闭 LED"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        led.write(False)
        logger.info("LED: OFF")
        return jsonify({"success": True, "action": "off"})
    except Exception as e:
        logger.error(f"关闭失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/led/toggle', methods=['POST'])
def led_toggle():
    """切换 LED 状态"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        current = led.read()
        led.write(not current)
        logger.info(f"LED: TOGGLE -> {'ON' if not current else 'OFF'}")
        return jsonify({"success": True, "action": "toggle", "state": not current})
    except Exception as e:
        logger.error(f"切换失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/led/status', methods=['GET'])
def led_status():
    """获取 LED 状态"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        state = led.read()
        return jsonify({"success": True, "state": "on" if state else "off"})
    except Exception as e:
        logger.error(f"读取状态失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/led/blink', methods=['POST'])
def led_blink():
    """LED 闪烁"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        
        data = request.get_json() or {}
        count = data.get('count', 3)
        interval = data.get('interval', 0.5)
        
        for i in range(count):
            led.write(True)
            time.sleep(interval)
            led.write(False)
            time.sleep(interval)
            logger.info(f"闪烁 {i+1}/{count}")
        
        return jsonify({"success": True, "action": "blink", "count": count})
    except Exception as e:
        logger.error(f"闪烁失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("💡 LED HTTP 服务启动")
    logger.info("=" * 50)
    logger.info(f"GPIO 芯片：gpiochip{GPIO_CHIP}, line {GPIO_LINE}")
    logger.info("监听端口：5001")
    logger.info("")
    logger.info("API 端点:")
    logger.info("  POST /led/on      - 打开 LED")
    logger.info("  POST /led/off     - 关闭 LED")
    logger.info("  POST /led/toggle  - 切换状态")
    logger.info("  GET  /led/status  - 获取状态")
    logger.info("  POST /led/blink   - 闪烁")
    logger.info("  GET  /health      - 健康检查")
    logger.info("")
    
    # 初始化 GPIO
    try:
        led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", GPIO_LINE, "out")
        led.write(False)
        logger.info("✅ GPIO 初始化成功")
    except Exception as e:
        logger.error(f"❌ GPIO 初始化失败：{e}")
        logger.error("请确认使用 sudo 运行")
        exit(1)
    
    # 启动 Flask 服务 (使用 5001 端口，避免和继电器服务冲突)
    app.run(host='0.0.0.0', port=5001, debug=False)
