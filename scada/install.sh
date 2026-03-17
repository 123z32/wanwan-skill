#!/bin/bash
# SCADA 系统 - 树莓派安装脚本
# ==========================
# 用途：在树莓派 5 (Ubuntu 24.04) 上安装 SCADA 从站服务

set -e

echo "🏭 SCADA 系统安装脚本"
echo "===================="
echo ""

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    echo "   sudo ./install.sh"
    exit 1
fi

# 更新系统
echo "📦 更新系统..."
apt-get update
apt-get upgrade -y

# 安装 Python 和依赖
echo "🐍 安装 Python 依赖..."
apt-get install -y python3 python3-pip python3-venv i2c-tools

# 启用 I2C
echo "🔌 启用 I2C..."
if ! grep -q "dtparam=i2c_arm=on" /boot/firmware/config.txt 2>/dev/null; then
    echo "dtparam=i2c_arm=on" >> /boot/firmware/config.txt
    echo "✅ I2C 已启用（需要重启）"
else
    echo "✅ I2C 已启用"
fi

# 创建虚拟环境
echo "📦 创建 Python 虚拟环境..."
cd /opt/scada
python3 -m venv venv
source venv/bin/activate

# 安装 Python 包
echo "📚 安装 Python 包..."
pip3 install --upgrade pip
pip3 install pymodbus smbus2 RPi.GPIO

# 创建系统服务
echo "🔧 创建系统服务..."
cat > /etc/systemd/system/scada-controller.service << EOF
[Unit]
Description=SCADA Controller Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/scada
Environment="PATH=/opt/scada/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/opt/scada/venv/bin/python3 /opt/scada/scada_controller.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=scada-controller

[Install]
WantedBy=multi-user.target
EOF

# 创建日志目录
echo "📝 创建日志目录..."
mkdir -p /var/log
touch /var/log/scada_controller.log
chmod 644 /var/log/scada_controller.log

# 重载 systemd
echo "🔄 重载 systemd..."
systemctl daemon-reload

# 启用服务
echo "🚀 启用 SCADA 服务..."
systemctl enable scada-controller.service

echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 下一步操作："
echo "   1. 重启树莓派以启用 I2C: sudo reboot"
echo "   2. 重启后启动服务：sudo systemctl start scada-controller"
echo "   3. 查看状态：sudo systemctl status scada-controller"
echo "   4. 查看日志：sudo journalctl -u scada-controller -f"
echo ""
echo "🔧 常用命令："
echo "   启动：sudo systemctl start scada-controller"
echo "   停止：sudo systemctl stop scada-controller"
echo "   重启：sudo systemctl restart scada-controller"
echo "   日志：sudo journalctl -u scada-controller -f"
echo ""
