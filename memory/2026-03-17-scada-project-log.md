# 🏭 SCADA 系统开发日志 - 2026-03-17

**项目**: 树莓派 5 + OpenClaw + AGX Thor SCADA 系统  
**参与者**: 张（用户）、绾绾（AI 助理）  
**日期**: 2026 年 3 月 17 日  
**时间**: 10:42 - 16:22 UTC

---

## 📋 项目目标

构建一个最小可行 SCADA 系统：
- **监控层**: PC (LabVIEW 2022)
- **通信层**: Tailscale 虚拟局域网
- **控制层**: 树莓派 5 (Ubuntu 24.04)
- **执行层**: 继电器 + AHT20/BHT80 温湿度传感器

---

## 🕐 时间线

### 上午 (10:42 - 12:00) - 系统初始化

**10:42** - 新会话启动
- 模型确认：Qwen3.5-Plus (云端)
- 用户身份确认：张

**10:45-11:00** - 测试消息
- 发送测试数字：1, 2, 3, 24

**11:00-11:24** - 飞书聊天记录功能开发
- **需求**: 读取飞书聊天记录
- **实现**:
  - 更新 `chat-schema.ts` 添加 `history` action
  - 更新 `chat.ts` 实现 `getChatHistory()` 函数
  - 使用飞书 SDK `im.message.list` API
- **调试**:
  - 修正 `container_id_type` 为 `"chat"`
  - 找到正确 chat_id: `oc_d77a50191711fcda0c3fab1a2d0e910c`
  - 修正消息内容字段为 `body.content`
- **结果**: ✅ 成功读取 188 条聊天记录

**11:24-11:35** - 日志整理
- 创建 `/memory/2026-03-17.md`
- 更新 `MEMORY.md`

**11:35-11:48** - 天气查询
- 查询惠州天气预报
- 使用 Open-Meteo API

**11:48-12:00** - 定位工具安装
- 创建 `/scripts/locate.sh`
- IP 定位：ip-api.com
- 定位结果：惠州 (23.1115, 114.4152)

---

### 中午 (12:00 - 14:00) - VSCode 安装

**12:07-12:26** - code-server 安装
- **挑战**: GitHub 下载速度慢 (2-4 KB/s)
- **解决**: 张开启 Tailscale 共享代理 (100.82.227.79:7890)
- **结果**: ✅ 4 分半钟下载完成 (89.4MB)
- **安装位置**: `/opt/code-server-4.89.0-linux-arm64`
- **访问地址**: `http://100.93.35.112:8080`

**12:26-12:35** - AGX Thor 连接测试
- **Tailscale IP**: `100.100.145.74`
- **可用模型**: 9 个 (qwen3.5:35b-a3b 为主力)
- **测试结果**: ✅ API 正常，响应时间 ~28 秒

---

### 下午 (14:00 - 16:22) - SCADA 系统开发

**14:10** - 继电器控制需求
- **硬件**: 继电器模块接物理引脚 11 (GPIO17)
- **控制方式**: 高电平触发
- **目标**: 实现 SCADA 四层模型

**14:14-14:30** - SCADA 代码生成
- **生成文件**:
  - `scada_controller.py` - Modbus TCP 从站 + GPIO + I2C
  - `install.sh` - 一键安装脚本
  - `test_hardware.py` - 硬件测试
  - `README.md` - 完整文档
  - `LabVIEW_Example.md` - LabVIEW 连接指南

**14:30-15:40** - GPIO 权限问题排查

**问题 1**: 容器内无法访问 GPIO
```
RuntimeError: Cannot determine SOC peripheral base address
```
**原因**: Docker 容器没有 GPIO 设备权限

**问题 2**: RPi.GPIO 库不兼容
```
RuntimeError: Cannot determine SOC peripheral base address
```
**原因**: Ubuntu 24.04 for Raspberry Pi 5 的 GPIO 访问方式不同

**问题 3**: sysfs 接口失败
```
[Errno 22] Invalid argument
```
**原因**: 树莓派 5 的 GPIO 编号方式改变

**解决方案**: 使用 `periphery` 库 + gpiochip4/line17
```bash
sudo gpioinfo  # 查看 GPIO 映射
# gpiochip4 - line 17: "GPIO17"
```

**15:41-15:53** - HTTP 服务方案设计

**架构**:
```
容器 → HTTP API (端口 5000) → 宿主机 GPIO 服务 → GPIO 硬件
```

**生成文件**:
- `gpio_http_service.py` - 宿主机 HTTP 服务 (Flask)
- `relay_container_control.py` - 容器控制脚本
- `feishu_relay_control.py` - 飞书集成脚本

**API 端点**:
- `POST /relay/on` - 打开继电器
- `POST /relay/off` - 关闭继电器
- `POST /relay/toggle` - 切换状态
- `GET /relay/status` - 获取状态
- `POST /relay/pulse` - 脉冲输出

**15:53-16:17** - 部署与测试

**步骤 1**: 宿主机启动 GPIO 服务 ✅
```bash
sudo nohup python3 gpio_http_service.py > /tmp/gpio_service.log 2>&1 &
curl http://localhost:5000/health
# {"service":"gpio-http","status":"ok"}
```

**步骤 2**: 容器安装 Python 环境 ⏳
```bash
docker exec openclaw_gateway bash -c "apt-get update && apt-get install -y python3 python3-pip python3-requests"
```

**步骤 3**: 飞书集成 ⏳
- 创建技能：`/skills/relay-control/SKILL.md`
- 飞书消息 → OpenClaw → Python 脚本 → GPIO 服务

---

## 📁 生成的文件

### SCADA 系统核心文件
```
/openclaw_data/.openclaw/workspace/scada/
├── scada_controller.py         # Modbus TCP 从站 (11K)
├── install.sh                  # 安装脚本 (2.6K)
├── test_hardware.py           # 硬件测试 (5.3K)
├── relay_quick_test.py        # 快速测试 (1.8K)
├── relay_sysfs_test.py        # sysfs 测试 (2.2K)
├── relay_periphery_test.py    # periphery 测试 (1.6K)
├── relay_container_control.py # 容器控制 (3.3K)
├── gpio_http_service.py       # HTTP 服务 (4.0K)
├── feishu_relay_control.py    # 飞书集成 (2.5K)
├── README.md                  # 完整文档 (5.7K)
└── LabVIEW_Example.md         # LabVIEW 指南 (8.8K)
```

### 技能文件
```
/openclaw_data/.openclaw/workspace/skills/
├── feishu-message-history/SKILL.md  # 飞书聊天记录
└── relay-control/SKILL.md           # 继电器控制
```

### 文档文件
```
/openclaw_data/.openclaw/workspace/memory/
├── 2026-03-17.md                    # 今日日志
├── ai-coding-workflow-test.md       # AI 协作测试
└── MEMORY.md                        # 长期记忆 (已更新)
```

---

## 🎯 技术成果

### 1. 飞书聊天记录功能 ✅
- **工具**: `feishu_chat` (action: `history`)
- **API**: 飞书开放平台 `im.message.list`
- **chat_id**: `oc_d77a50191711fcda0c3fab1a2d0e910c`
- **状态**: 已完成并测试通过

### 2. 定位工具 ✅
- **脚本**: `/scripts/locate.sh`
- **方式**: IP 定位 (ip-api.com)
- **精度**: 城市级别
- **当前位置**: 惠州 (23.1115, 114.4152)

### 3. VSCode (code-server) ✅
- **版本**: 4.89.0
- **位置**: `/opt/code-server-4.89.0-linux-arm64`
- **访问**: `http://100.93.35.112:8080`
- **状态**: 运行中

### 4. SCADA 系统 ⏳
- **GPIO 映射**: gpiochip4, line 17 (GPIO17)
- **HTTP 服务**: ✅ 运行中 (端口 5000)
- **容器 Python**: ⏳ 安装中
- **飞书集成**: ⏳ 待测试

---

## 📊 系统架构

### 网络拓扑
```
┌──────────────────┐
│   用户电脑       │
│ 100.82.227.79   │ ← Clash 代理
└───────┬──────────┘
        │ Tailscale
        │
┌───────┴──────────┐         ┌─────────────────────┐
│   树莓派 5        │◄────────│   AGX Thor          │
│ 100.93.35.112    │ Tailscale│ 100.100.145.74     │
│ code-server:8080 │         │ Ollama:11434        │
│ OpenClaw 容器     │         │ 128GB VRAM          │
│ GPIO 服务:5000    │         │ qwen3.5:35b-a3b     │
└──────────────────┘         └─────────────────────┘
```

### SCADA 控制流
```
飞书消息
   ↓
OpenClaw (容器)
   ↓
feishu_relay_control.py
   ↓
HTTP POST (100.93.35.112:5000)
   ↓
gpio_http_service.py (宿主机)
   ↓
periphery GPIO (gpiochip4, line17)
   ↓
继电器 (物理引脚 11)
```

---

## 🔧 待办事项

### 高优先级
- [ ] 完成容器 Python 环境安装
- [ ] 测试继电器控制 (`python3 feishu_relay_control.py on`)
- [ ] 飞书消息集成测试

### 中优先级
- [ ] 部署 Modbus TCP 从站服务
- [ ] LabVIEW 界面开发
- [ ] AHT20/BHT80 传感器集成

### 低优先级
- [ ] 添加数据记录到数据库
- [ ] 实现报警功能
- [ ] Web 界面开发

---

## 💡 经验教训

### 成功之处
1. **代理加速**: Tailscale 共享代理极大提升了下载速度
2. **HTTP 服务架构**: 解耦容器和硬件，避免权限问题
3. **文档完整**: 每个步骤都有详细记录

### 踩过的坑
1. **GPIO 权限**: 容器无法直接访问 GPIO，需要设备映射或 HTTP 服务
2. **树莓派 5 GPIO**: Ubuntu 24.04 的 GPIO 编号方式不同，需要查 `gpioinfo`
3. **Python 环境**: 容器内没有 Python，需要单独安装

### 改进建议
1. 下次直接在宿主机运行 GPIO 相关服务
2. 容器专注于业务逻辑，不碰硬件
3. 提前确认系统版本和硬件兼容性

---

## 📞 参与者

- **张**: 用户，系统架构师，硬件接线
- **绾绾**: AI 助理，代码开发，系统集成

---

*最后更新：2026-03-17 16:22 UTC*  
*文档生成：OpenClaw Memory System*
