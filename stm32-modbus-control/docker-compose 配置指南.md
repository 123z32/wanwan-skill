# Docker 容器添加 USB 串口设备配置

**目标**：为 OpenClaw 容器添加 USB 转串口设备 `/dev/ttyUSB0`，使其能够访问 STM32

**日期**：2026-04-07  
**作者**：绾绾

---

## 📋 任务清单

- [ ] 检查当前 Docker 容器配置
- [ ] 创建/修改 `docker-compose.yml`
- [ ] 停止并删除现有容器
- [ ] 用 docker-compose 重新启动
- [ ] 验证设备是否可访问

---

## 0️⃣ 启用硬件串口（可选，但推荐）

**如果要用硬件串口（GPIO），先执行这一步**。如果只用 USB 串口，跳过这步。

### 编辑 /boot/config.txt

```bash
sudo nano /boot/config.txt
```

**添加以下内容**：

```ini
# 启用硬件串口
enable_uart=1

# 禁用蓝牙串口（释放 ttyAMA0 给 GPIO 使用）
dtoverlay=disable-bt
```

**保存并重启**：
```bash
sudo reboot
```

### 验证串口设备

重启后检查：

```bash
# 查看硬件串口
ls -la /dev/ttyAMA0
ls -la /dev/serial0

# 查看 USB 串口（插入 USB 转 TTL 模块）
ls -la /dev/ttyUSB0
```

**预期输出**：
```
crw-rw---- 1 root dialout 204, 64 Apr  7 14:00 /dev/ttyAMA0
lrwxrwxrwx 1 root root    7 Apr  7 14:00 /dev/serial0 -> ttyAMA0
crw-rw-rw- 1 root dialout 188,  0 Apr  7 14:00 /dev/ttyUSB0
```

---

## 1️⃣ 检查当前配置

在树莓派宿主机上执行：

```bash
# 查看容器名
docker ps | grep openclaw

# 查看当前容器配置
docker inspect openclaw | grep -A10 "Devices\|Mounts\|Config"

# 查看容器启动命令（可选）
docker inspect openclaw --format='{{.ArgsEscaped}}'

# 查看数据卷位置
docker inspect openclaw --format='{{range .Mounts}}{{.Source}}:{{.Destination}}{{"\n"}}{{end}}'
```

**记录以下信息**：
- 容器名称（通常是 `openclaw`）
- 镜像名（如 `openclaw:latest` 或具体版本号）
- 数据卷路径（通常是 `/openclaw_data/.openclaw`）
- 端口映射（通常是 `18789:18789`）
- 环境变量（如果有）

---

## 2️⃣ 创建 docker-compose.yml

在 `/openclaw_data/` 目录创建 `docker-compose.yml`：

```bash
cd /openclaw_data
nano docker-compose.yml
```

**文件内容**（根据实际情况调整）：

```yaml
version: '3.8'

services:
  openclaw:
    image: openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    
    # 🔌 关键配置：同时支持 USB 串口和硬件串口
    devices:
      # USB 转串口模块（即插即用，推荐调试用）
      - /dev/ttyUSB0:/dev/ttyUSB0
      # 树莓派硬件串口（GPIO 14/15，更稳定）
      - /dev/ttyAMA0:/dev/ttyAMA0
      # 可选：mini UART（蓝牙串口）
      # - /dev/ttyS0:/dev/ttyS0
    
    # 📁 数据卷挂载
    volumes:
      - /openclaw_data/.openclaw:/home/node/.openclaw
      # 可选：挂载工作区
      - /openclaw_data/workspace:/home/node/.openclaw/workspace
    
    # 🌐 端口映射
    ports:
      - "18789:18789"  # OpenClaw 控制 UI
      # 可选：其他端口
      # - "18800:18800"  # CDP 端口
    
    # ⚙️ 环境变量（如果有）
    environment:
      - TZ=Asia/Shanghai
      # 添加其他原有环境变量...
    
    # 🔒 权限配置（可选，如果需要访问 GPIO）
    # privileged: true
    # 或者更细粒度的配置：
    # cap_add:
    #   - SYS_RAWIO
    # devices:
    #   - /dev/mem:/dev/mem
```

**保存并退出**：`Ctrl+O` → `Enter` → `Ctrl+X`

---

## 3️⃣ 停止并删除现有容器

```bash
# 停止容器
docker stop openclaw

# 删除容器（不会删除数据，数据在 volume 里）
docker rm openclaw

# 验证容器已删除
docker ps -a | grep openclaw
```

---

## 4️⃣ 用 docker-compose 启动

```bash
cd /openclaw_data

# 启动容器
docker-compose up -d

# 查看启动日志
docker-compose logs -f

# 按 Ctrl+C 退出日志查看
```

---

## 4.5️⃣ 串口接线参考

**硬件串口（GPIO）接线**：
```
树莓派 5          STM32F407 (SkyStar)
────────          ─────────────────
GPIO 14 (TXD) ←→  PA3 (USART2_RX)
GPIO 15 (RXD) ←→  PA2 (USART2_TX)
GND           ←→  GND
```

**USB 转串口接线**：
```
USB-TTL 模块      STM32F407 (SkyStar)
────────────      ─────────────────
TX (绿)       ←→  PA3 (USART2_RX)
RX (黄)       ←→  PA2 (USART2_TX)
GND (黑)      ←→  GND
5V (红)       ←→  5V (可选供电)
```

---

## 5️⃣ 验证设备是否可访问

```bash
# 方法 1：在容器内查看设备
docker exec openclaw ls -la /dev/ttyUSB*

# 方法 2：进入容器测试
docker exec -it openclaw bash
ls -la /dev/ttyUSB*
exit

# 方法 3：运行测试脚本（推荐）
docker exec openclaw python3 /home/node/.openclaw/workspace/scripts/test-serial-devices.py
```

**预期输出**：
```
crw-rw-rw- 1 root dialout 188, 0 Apr  7 14:00 /dev/ttyUSB0
```

---

## 6️⃣ 测试 OpenClaw 功能

```bash
# 检查容器状态
docker ps | grep openclaw

# 查看 OpenClaw 日志
docker logs openclaw --tail 50

# 访问控制 UI
# 浏览器打开：http://树莓派 IP:18789
```

---

## 🔧 常用命令速查

```bash
# 查看容器状态
docker-compose ps

# 重启容器
docker-compose restart

# 停止容器
docker-compose stop

# 启动容器
docker-compose start

# 查看日志
docker-compose logs -f

# 重新加载配置
docker-compose down
docker-compose up -d

# 更新容器
docker-compose pull
docker-compose up -d
```

---

## ⚠️ 注意事项

1. **设备权限**：如果容器内提示权限不足，可能需要：
   ```bash
   # 在宿主机上添加用户到 dialout 组
   sudo usermod -a -G dialout $USER
   
   # 或者临时设置设备权限
   sudo chmod 666 /dev/ttyUSB0
   ```

2. **设备名称**：
   - USB 转串口通常是 `/dev/ttyUSB0`
   - 如果是 CH340 芯片，可能是 `/dev/ttyUSB0`
   - 如果是 CP2102 芯片，也可能是 `/dev/ttyUSB0`
   - 用 `ls /dev/ttyUSB*` 查看实际设备名

3. **容器名冲突**：如果 `docker rm` 失败，可能需要：
   ```bash
   docker rm -f openclaw
   ```

4. **数据备份**：操作前建议备份配置：
   ```bash
   cp -r /openclaw_data/.openclaw /openclaw_data/.openclaw.backup
   ```

---

## 🐛 故障排查

### 问题 1：容器启动失败

```bash
# 查看详细错误
docker-compose up -d
docker-compose logs

# 检查端口占用
sudo netstat -tlnp | grep 18789
```

### 问题 2：设备不可见

```bash
# 检查宿主机是否有设备
ls -la /dev/ttyUSB*

# 检查设备权限
ls -l /dev/ttyUSB0

# 重新插拔 USB 设备
# 然后重启容器
docker-compose restart
```

### 问题 3：OpenClaw 无法访问

```bash
# 检查容器状态
docker ps

# 检查防火墙
sudo ufw status

# 检查端口监听
docker exec openclaw netstat -tlnp | grep 18789
```

---

## 📚 参考资料

- [Docker Compose 官方文档](https://docs.docker.com/compose/)
- [Docker 设备挂载文档](https://docs.docker.com/compose/compose-file/compose-file-v3/#devices)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

*此文档由绾绾整理，用于指导 Claude Code 配置 Docker 容器*
*最后更新：2026-04-07*
