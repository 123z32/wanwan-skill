#!/bin/bash
# 定位工具 - 用于获取树莓派当前位置

# IP 定位（使用 ip-api.com，免费无需 API key）
ip_location() {
    echo "📍 IP 定位信息:"
    curl -s "ip-api.com/json/?fields=city,region,country,lat,lon,isp,query,timezone" | \
    node -e "
    const d = JSON.parse(require('fs').readFileSync(0, 'utf8'));
    console.log('  城市：' + d.city);
    console.log('  省份：' + d.region);
    console.log('  国家：' + d.country);
    console.log('  坐标：' + d.lat + ', ' + d.lon);
    console.log('  ISP: ' + d.isp);
    console.log('  IP: ' + d.query);
    console.log('  时区：' + d.timezone);
    "
}

# WiFi 定位（需要扫描周围的 WiFi）
wifi_location() {
    echo "📡 WiFi 扫描:"
    if command -v iwlist &> /dev/null; then
        sudo iwlist wlan0 scan 2>/dev/null | grep -E "ESSID|Quality|Address" | head -30
    else
        echo "  iwlist 未安装，尝试 nmcli..."
        nmcli dev wifi list 2>/dev/null | head -10
    fi
}

# 返回 JSON 格式（供程序调用）
ip_location_json() {
    curl -s "ip-api.com/json/?fields=city,region,country,lat,lon,isp,query,timezone,status,message"
}

# 主程序
case "${1:-}" in
    --wifi)
        wifi_location
        ;;
    --json)
        ip_location_json
        ;;
    --help|-h)
        echo "用法：locate.sh [选项]"
        echo "  --wifi    扫描周围 WiFi"
        echo "  --json    返回 JSON 格式"
        echo "  --help    显示帮助"
        echo "  (无参数)  显示定位信息"
        ;;
    *)
        ip_location
        ;;
esac
