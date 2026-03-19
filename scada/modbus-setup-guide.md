# Modbus TCP SCADA 系统部署指南

## 📋 概述

使用 **Modbus TCP** 工业标准协议 + **periphery** 底层 GPIO 控制，构建真实 SCADA 架构验证环境。

---

## 🏗️ 架构

```
┌─────────────────┐      Modbus TCP      ┌─────────────────┐
│   上位机        │ ──────────────────→  │   树莓派宿主机   │
│  (LabVIEW/Python)│     端口 5020        │  gpio_modbus_service.py │
│                 │                      │  + periphery GPIO │
└─────────────────┘                      └─────────────────┘
```

---

## 🚀 部署步骤

### 步骤 1：在树莓派宿主机安装依赖

```bash
# SSH 登录树莓派宿主机
ssh pi@192.168.1.13  # 或你的宿主机 IP

# 安装 Python 依赖
sudo pip3 install pymodbus python-periphery
```

### 步骤 2：启动 Modbus 服务

```bash
# 进入工作目录
cd /openclaw_data/.openclaw/workspace/scada

# 启动服务（需要 sudo 访问 GPIO）
sudo python3 gpio_modbus_service.py
```

**预期输出**:
```
2026-03-19 08:00:00 - INFO - ✅ 物理硬件初始化成功：/dev/gpiochip4 Line 17
2026-03-19 08:00:00 - INFO - ✅ Modbus 数据存储区初始化成功
2026-03-19 08:00:00 - INFO - ============================================================
2026-03-19 08:00:00 - INFO -    🏭 SCADA 下位机 - Modbus TCP 服务启动
2026-03-19 08:00:00 - INFO - ============================================================
2026-03-19 08:00:00 - INFO -    监听端口：5020
2026-03-19 08:00:00 - INFO -    控制地址：Coil 00000 -> GPIO Line 17
2026-03-19 08:00:00 - INFO -    同步频率：10 Hz
2026-03-19 08:00:00 - INFO - ============================================================
2026-03-19 08:00:00 - INFO -    等待上位机连接...
```

### 步骤 3：测试连接（Python 上位机）

在**容器或任何能访问树莓派的设备**上：

```bash
cd /openclaw_data/.openclaw/workspace/scada

# 测试连接（使用树莓派 IP）
python3 modbus_client_test.py 100.93.35.112 5020
```

**交互模式命令**:
- `on` - 打开继电器
- `off` - 关闭继电器
- `toggle` - 切换状态
- `status` - 查看状态
- `quit` - 退出

---

## 🎯 LabVIEW 上位机配置

### 1. 建立连接（一次性）

使用 **NI Datalog API** 或 **Modbus Library**:

| 参数 | 值 |
|------|-----|
| IP Address | `100.93.35.112` (Tailscale) 或局域网 IP |
| Port | `5020` |
| Slave ID | `0` (或 `1`, 代码中 `single=True`) |

### 2. 控制继电器（While 循环内）

**写入线圈** (Write Single Coil):
- Starting Address: `0`
- Value: `True/False` (布尔开关)

**读取状态** (Read Coils):
- Starting Address: `0`
- Number of Inputs: `1`
- 输出：布尔数组 → 提取索引 0 → 连接指示灯

### 3. 断开连接

循环结束后调用 **Shutdown** VI 关闭连接。

---

## 📊 CMD 状态反馈示例

服务运行时，终端会实时打印状态变化：

```
[08:15:23] Coil 0: 🟢 ON  GPIO: ✓
[08:15:35] Coil 0: 🔴 OFF  GPIO: ✓
[08:16:02] Coil 0: 🟢 ON  GPIO: ✓
```

- `🟢 ON` / `🔴 OFF` - 线圈状态
- `✓` - GPIO 实际电平与期望一致
- `⚠️ 不一致` - 状态不匹配（可能硬件故障）

---

## 🔧 故障排查

### 问题 1: GPIO 初始化失败

```
❌ GPIO 初始化失败：[Errno 2] No such file or directory: '/dev/gpiochip4'
```

**解决**:
```bash
# 检查 GPIO 设备
ls -la /dev/gpiochip*

# 确认内核模块加载
lsmod | grep gpio

# 树莓派 5 可能需要更新内核
sudo apt update && sudo apt upgrade
```

### 问题 2: 无法连接 Modbus 服务

```
❌ 无法连接到 Modbus 服务器：100.93.35.112:5020
```

**解决**:
```bash
# 在宿主机检查服务是否运行
sudo netstat -tlnp | grep 5020

# 检查防火墙
sudo ufw status
sudo ufw allow 5020/tcp

# 测试本地连接
curl telnet://localhost:5020
```

### 问题 3: pymodbus 版本不兼容

```
ImportError: cannot import name 'StartAsyncTcpServer' from 'pymodbus.server'
```

**解决**:
```bash
# 确认版本（需要 3.x）
pip3 show pymodbus

# 升级
sudo pip3 install --upgrade pymodbus
```

---

## 📁 文件清单

| 文件 | 用途 | 运行位置 |
|------|------|----------|
| `gpio_modbus_service.py` | Modbus TCP 下位机服务 | 树莓派宿主机 |
| `modbus_client_test.py` | Python 上位机测试 | 任意设备 |
| `modbus-setup-guide.md` | 本部署文档 | 工作区 |

---

## 🔐 安全提示

1. **sudo 运行** - GPIO 访问需要 root 权限
2. **防火墙** - 仅开放必要端口（5020）
3. **Tailscale** - 建议使用 VPN 而非公网暴露
4. **看门狗** - 生产环境建议添加硬件看门狗

---

## 🎨 扩展建议

- **多继电器** - 映射 Coil 1-7 到不同 GPIO 引脚
- **传感器输入** - 使用 Discrete Input 读取数字传感器
- **模拟量** - 使用 Holding Register 存储 ADC 值
- **日志记录** - 添加 InfluxDB 记录历史数据
- **Web 界面** - 添加 Flask 网页控制面板
