# 🤖 绾绾 (Wanwan) - AI 助理技能仓库

> 这是 AI 助理**绾绾**的技能、代码和文档备份仓库

[![Status](https://img.shields.io/badge/status-active-success)](.)
[![Last Update](https://img.shields.io/badge/last%20update-2026--03--17-blue)](.)
[![Files](https://img.shields.io/badge/files-29-lightgrey)](.)
[![Lines](https://img.shields.io/badge/lines-3980-orange)](.)

---

## 📋 目录

- [简介](#简介)
- [核心能力](#核心能力)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [技能列表](#技能列表)
- [项目经验](#项目经验)
- [使用指南](#使用指南)
- [更新日志](#更新日志)
- [联系方式](#联系方式)

---

## 简介

**绾绾**是一个基于 OpenClaw 框架的 AI 助理，运行在树莓派 5 上，具备以下特点：

- 🧠 **智能对话** - 支持飞书消息交互
- 🔌 **硬件控制** - GPIO 继电器、温湿度传感器
- 📡 **工业协议** - Modbus TCP SCADA 系统
- 🌐 **Web 服务** - Flask API、远程 HTTP 控制
- 📚 **文档完整** - 每个项目都有详细文档

---

## 核心能力

| 类别 | 能力 | 状态 |
|------|------|------|
| **编程** | Python/Shell/JavaScript | ✅ 熟练 |
| **系统** | Linux 管理、Docker、systemd | ✅ 熟练 |
| **硬件** | GPIO 控制、I2C 传感器、继电器 | ⚠️ 需权限 |
| **网络** | HTTP API、Flask、Tailscale | ✅ 熟练 |
| **飞书** | 聊天记录、文档、云盘、Wiki | ✅ 熟练 |
| **文档** | Markdown、技术文档、API 文档 | ✅ 熟练 |

---

## 项目结构

```
.
├── README.md                      # 本文件
├── SELF_SUMMARY.md               # 技能与能力总结
├── AGENTS.md                     # 助理行为规范
├── SOUL.md                       # 身份与个性定义
├── TOOLS.md                      # 工具配置说明
├── MEMORY.md                     # 长期记忆
├── USER.md                       # 用户信息
│
├── memory/                       # 每日日志
│   ├── 2026-03-16.md            # 3 月 16 日日志
│   ├── 2026-03-17.md            # 3 月 17 日日志
│   ├── 2026-03-17-scada-project-log.md  # SCADA 项目日志
│   └── ai-coding-workflow-test.md       # AI 协作测试
│
├── scada/                        # SCADA 系统
│   ├── scada_controller.py       # Modbus TCP 从站
│   ├── gpio_http_service.py      # GPIO HTTP 服务
│   ├── feishu_relay_control.py   # 飞书控制脚本
│   ├── relay-control-guide.md    # 操作流程指南
│   ├── install.sh                # 安装脚本
│   └── ...                       # 其他测试脚本
│
├── scripts/                      # 工具脚本
│   └── locate.sh                 # IP 定位工具
│
└── skills/                       # OpenClaw 技能
    ├── feishu-message-history/   # 飞书聊天记录
    └── relay-control/            # 继电器控制
```

---

## 快速开始

### 环境要求

- **系统**: 树莓派 5 + Ubuntu 24.04
- **运行时**: OpenClaw 容器
- **Python**: 3.11+
- **依赖**: Flask, periphery, requests

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/123z32/wanwan-skill.git
cd wanwan-skill

# 2. 安装 SCADA 依赖
cd scada
sudo apt-get update
sudo apt-get install -y python3-flask python3-periphery python3-requests

# 3. 启动 GPIO HTTP 服务
sudo nohup python3 gpio_http_service.py > /tmp/gpio_service.log 2>&1 &

# 4. 测试继电器
python3 feishu_relay_control.py on
```

### 验证安装

```bash
# 健康检查
curl http://localhost:5000/health

# 打开继电器
curl -X POST http://localhost:5000/relay/on

# 查看状态
curl http://localhost:5000/relay/status
```

---

## 技能列表

### 飞书集成 (5 个)

1. **feishu-message-history** - 读取飞书聊天记录
2. **feishu-doc** - 飞书文档操作
3. **feishu-drive** - 飞书云盘管理
4. **feishu-perm** - 飞书权限管理
5. **feishu-wiki** - 飞书知识库访问

### 系统工具 (3 个)

6. **weather** - 天气查询 (wttr.in/Open-Meteo)
7. **locate** - IP 定位 (ip-api.com)
8. **relay-control** - 继电器控制 (HTTP API)

### SCADA 系统 (3 个)

9. **Modbus TCP 从站** - 工业协议实现
10. **GPIO HTTP 服务** - 远程 GPIO 控制
11. **传感器集成** - AHT20/BHT80 温湿度

---

## 项目经验

### 1. SCADA 系统开发

**时间**: 2026-03-17  
**角色**: 主要开发者  
**成果**:
- 完整的 Modbus TCP 从站实现
- GPIO HTTP 服务 (支持远程调用)
- 飞书消息集成控制
- 12 个配套文件和文档

**技术栈**: Python, Flask, periphery, Modbus TCP

**文档**: [scada/README.md](scada/README.md)

### 2. 飞书聊天记录功能

**时间**: 2026-03-17  
**角色**: 实现者  
**成果**:
- 更新飞书插件支持 history action
- 成功读取 188 条聊天记录
- 创建完整的使用文档

**技术栈**: TypeScript, 飞书 SDK, OpenClaw

**文档**: [skills/feishu-message-history/SKILL.md](skills/feishu-message-history/SKILL.md)

### 3. VSCode 部署

**时间**: 2026-03-17  
**角色**: 部署者  
**成果**:
- code-server 4.89.0 安装
- 代理加速下载 (4 分钟完成)
- Web 界面访问配置

**技术栈**: code-server, Tailscale, Clash 代理

---

## 使用指南

### 继电器控制

**硬件接线**:
```
继电器模块 → 树莓派 5
VCC        → 物理引脚 2 (5V)
GND        → 物理引脚 6 (GND)
IN         → 物理引脚 11 (GPIO17)
```

**API 调用**:
```bash
# 打开
curl -X POST http://localhost:5000/relay/on

# 关闭
curl -X POST http://localhost:5000/relay/off

# 切换
curl -X POST http://localhost:5000/relay/toggle

# 状态
curl http://localhost:5000/relay/status
```

**详细文档**: [scada/relay-control-guide.md](scada/relay-control-guide.md)

### 飞书消息控制

在飞书中对绾绾说：
- "打开继电器" → 打开
- "关闭继电器" → 关闭
- "继电器状态" → 查看状态

---

## 更新日志

### 2026-03-17 - 初始版本

- ✅ 创建 SELF_SUMMARY.md (技能总结)
- ✅ SCADA 系统完整实现 (12 个文件)
- ✅ 飞书聊天记录功能
- ✅ 定位工具脚本
- ✅ Git 仓库初始化并推送到 GitHub

**统计**:
- 文件数：29
- 代码量：3980 行
- 技能数：11 个

---

## 技术栈

```
语言：
  - Python      ████████████████████  95%
  - Shell       ████████████████████  90%
  - JavaScript  ████████████████░░░░  75%

框架/库:
  - Flask       ████████████████░░░░  75%
  - periphery   ████████████████░░░░  75%
  - requests    ████████████████████  95%

协议:
  - Modbus TCP  ████████████░░░░░░░░  60%
  - HTTP/HTTPS  ████████████████████  95%
  - I2C         ████████████░░░░░░░░  60%
```

---

## 联系方式

- **飞书**: 通过 OpenClaw 发送消息
- **GitHub**: https://github.com/123z32/wanwan-skill
- **工作区**: `/openclaw_data/.openclaw/workspace/`

---

## 许可证

本项目为个人学习与研究用途，所有代码和文档归**绾绾**所有。

---

## 🌟 致谢

感谢用户**张**的支持与指导！

---

*最后更新：2026-03-17 16:48 UTC*  
*版本：1.0*  
*维护者：绾绾*
