#!/usr/bin/env python3
"""
GPIO HTTP 服务 - 让容器可以控制 GPIO
运行在树莓派宿主机上
支持：LED 控制 + 光敏电阻读取
"""

from flask import Flask, request, jsonify
from periphery import GPIO
import logging

app = Flask(__name__)

# 配置
GPIO_CHIP = 4
LED_PIN = 17        # LED 控制引脚（原继电器引脚）
LIGHT_SENSOR_PIN = 27  # 光敏电阻输入引脚

led = None
light_sensor = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GPIO_Service')

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "gpio-http"})

@app.route('/led/on', methods=['POST'])
def led_on():
    """打开 LED"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        led.write(True)
        logger.info("💡 LED: ON")
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
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        led.write(False)
        logger.info("🌑 LED: OFF")
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
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        current = led.read()
        led.write(not current)
        logger.info(f"💡 LED: TOGGLE -> {'ON' if not current else 'OFF'}")
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
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        state = led.read()
        return jsonify({"success": True, "state": "on" if state else "off"})
    except Exception as e:
        logger.error(f"读取状态失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/led/pulse', methods=['POST'])
def led_pulse():
    """脉冲输出（闪烁）"""
    global led
    try:
        if led is None:
            led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        
        data = request.get_json() or {}
        count = data.get('count', 3)
        interval = data.get('interval', 0.5)
        
        for i in range(count):
            led.write(True)
            time.sleep(interval)
            led.write(False)
            time.sleep(interval)
            logger.info(f"脉冲 {i+1}/{count}")
        
        return jsonify({"success": True, "action": "pulse", "count": count})
    except Exception as e:
        logger.error(f"脉冲失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/sensor/light', methods=['GET'])
def read_light_sensor():
    """读取光敏电阻"""
    global light_sensor
    try:
        if light_sensor is None:
            light_sensor = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LIGHT_SENSOR_PIN, "in")
        value = light_sensor.read()
        logger.info(f"📊 光敏电阻：{'HIGH (亮)' if value else 'LOW (暗)'}")
        return jsonify({
            "success": True,
            "value": value,
            "state": "bright" if value else "dark",
            "pin": LIGHT_SENSOR_PIN
        })
    except Exception as e:
        logger.error(f"读取光敏电阻失败：{e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    import time
    
    logger.info("=" * 50)
    logger.info("🔌 GPIO HTTP 服务启动")
    logger.info("=" * 50)
    logger.info(f"GPIO 芯片：gpiochip{GPIO_CHIP}")
    logger.info(f"LED 引脚：GPIO {LED_PIN} (输出)")
    logger.info(f"光敏电阻引脚：GPIO {LIGHT_SENSOR_PIN} (输入)")
    logger.info("监听端口：5000")
    logger.info("")
    logger.info("API 端点:")
    logger.info("  POST /led/on        - 打开 LED")
    logger.info("  POST /led/off       - 关闭 LED")
    logger.info("  POST /led/toggle    - 切换状态")
    logger.info("  GET  /led/status    - 获取状态")
    logger.info("  POST /led/pulse     - 脉冲输出")
    logger.info("  GET  /sensor/light  - 读取光敏电阻")
    logger.info("  GET  /health        - 健康检查")
    logger.info("")
    
    # 初始化 GPIO
    try:
        led = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LED_PIN, "out")
        led.write(False)
        logger.info("✅ LED GPIO 初始化成功")
    except Exception as e:
        logger.error(f"❌ LED GPIO 初始化失败：{e}")
    
    try:
        light_sensor = GPIO(f"/dev/gpiochip{GPIO_CHIP}", LIGHT_SENSOR_PIN, "in")
        logger.info("✅ 光敏电阻 GPIO 初始化成功")
    except Exception as e:
        logger.error(f"❌ 光敏电阻 GPIO 初始化失败：{e}")
    
    # 启动 Flask 服务
    app.run(host='0.0.0.0', port=5000, debug=False)
