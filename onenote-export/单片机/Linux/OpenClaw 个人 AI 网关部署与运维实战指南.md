# OpenClaw 个人 AI 网关部署与运维实战指南

> 来源: OneNote > 单片机 > Linux
> 修改: 2026-03-21T09:42:23Z

OpenClaw 个人 AI 网关部署与运维实战指南
 
 
 
 
 

 
OpenClaw 个人 AI 网关部署与运维实战指南

 
架构说明：本地 ARM64 主机 (树莓派 5) + Docker 容器化部署 + 远程 Ollama 算力 (Qwen 3.5 35B) + 飞书终端接入

 
一、 准备 Docker 部署文件 (解决网络与环境冲突)

 
在部署过程中，我们通过定制 Dockerfile 避开了官方脚本在精简版容器中的三个大坑：镜像源 403 报错、Npm 下载卡死、缺少交互终端导致闪退。

 
1. 创建工作目录并写入 Dockerfile

 
Bash

 

 
mkdir -p ~/openclaw-docker￼cd ~/openclaw-docker

 
Dockerfile

 

 
# Dockerfile￼FROM node:22-bookworm-slim

 
# 安装基础依赖 (必须带上 git，否则后续脚本会卡死)￼RUN apt-get update && apt-get install -y curl bash git && rm -rf /var/lib/apt/lists/*

 
# 替换 npm 源为淘宝镜像，解决国内网络下载源码包极慢的问题￼RUN npm config set registry https://registry.npmmirror.com

 
# 执行官方安装脚本 (末尾加上 || true 忽略无交互终端导致的静默报错)￼RUN curl -fsSL https://openclaw.ai/install.sh | bash || true

 
# 集中化数据路径，方便外挂 SSD 存储￼ENV OPENCLAW_HOME=/openclaw_data￼ENV OPENCLAW_STATE_DIR=/openclaw_data/state￼ENV OPENCLAW_CONFIG_PATH=/openclaw_data/config/config.json

 
WORKDIR /app￼EXPOSE 18789

 
2. 写入 docker-compose.yml (初始化过渡版) 注：为了能顺利完成初始化向导，这里先使用 tail -f /dev/null 让容器

 
保持“假死待机”状态，防止程序因找不到系统 systemd 导致无限崩溃重启。

 
YAML

 

 
# docker-compose.yml￼services:￼ openclaw:￼ build: .￼ container_name: openclaw_gateway￼ network_mode: "host"￼ volumes:￼ # 建议挂载到固态硬盘以提升知识库读写性能，请根据实际情况修改左侧路径￼ - /mnt/ssd/openclaw_data:/openclaw_data￼ command: tail -f /dev/null ￼ restart: unless-stopped

 
二、 容器构建与初始化向导

 
1. 构建并启动容器 在上述文件所在目录执行：

 
Bash

 

 
docker compose up -d --build

 
2. 运行配置向导 容器稳定运行后，进入容器内部执行初始化：

 
Bash

 

 
docker exec -it openclaw_gateway bash￼# 在容器内部执行：￼openclaw onboard

 
向导关键配置说明：

 
 
- 安全警告 (Security)：务必使用方向键选择 Yes 确认单用户安全协议，否则向导会退出。
 
- 模型提供商 (Model Provider)：选择 Ollama。
 
- Ollama Base URL：填写远程算力节点的 IP 与端口（例如通过 Tailscale 组网的 http://100.100.145.74:11434）。
 
- 模型名称：精确填写远程节点已下载的模型（例如 qwen3.5:35b-a3b）。
 
- 运行模式：强烈建议选择 Local，防止网关擅自从云端拉取数十 GB 的新模型打满带宽和硬盘。
 
- 飞书插件 (Feishu Plugin)：选择 Use local plugin path，直接使用本地已内置的插件。
 

 
三、 控制台透传与最终定型 (解除假死)

 
向导完成后，我们需要让网关真正跑起来，并能随树莓派开机自启。

 
1. 修改配置文件为“生产模式” 打开 docker-compose.yml，将 command: tail -f /dev/null 替换为官方的前台运行指令：

 
YAML

 

 
 # 替换后的 command：￼ command: openclaw gateway --port 18789

 
2. 重启容器应用新配置

 
Bash

 

 
docker compose down￼docker compose up -d

 
3. 访问 Web 控制台 如果你的电脑无法直接通过局域网 IP 访问控制台，可以在个人电脑终端使用 SSH 本地端口转发：

 
Bash

 

 
ssh -N -L 18789:127.0.0.1:18789 wanwanhua@100.93.35.112

 
保持窗口不关，在本地浏览器输入向导最后生成的免密 Token 链接即可登入 Dashboard： http://localhost:18789/#token=你的专属Token字符串

 
四、 飞书频道接入与鉴权排错

 
1. 批准飞书配对 通过控制台或飞书发送消息触发配对后，飞书会返回一串 8 位验证码。在树莓派终端执行以下命令完成绑定：

 
Bash

 

 
docker exec -it openclaw_gateway openclaw pairing approve feishu <你的8位配对码>

 
2. 修复飞书权限报错 (Access denied) 若后台日志提示 ignoring stale permission scope error，需要前往飞书开放平台：

 
 
- 进入对应的应用 -> 权限管理。
 
- 搜索并开通 获取通讯录基本信息 (或 contact:contact.base:readonly) 等日志中提示的权限。
 
- 务必前往 版本管理与发布，创建一个新版本并提交发布，权限才会真正生效。
 

 

 
五、 日常运维与常用控制命令

 
既然使用 Docker 部署，日常的维护和排错都变得非常标准化。以下命令均在树莓派宿主机终端（包含 docker-compose.yml 的目录）执行：

 
1. 容器启停与状态管理

 
 
- 查看运行状态：docker ps （查看 OpenClaw 容器是否在运行及运行时间）
 
- 停止服务：docker compose down （安全停止容器并移除网络）
 
- 启动服务：docker compose up -d （在后台启动容器）
 
- 重启服务：docker compose restart （修改了宿主机配置后快速重启）
 

 
2. 日志查看 (排错神器)

 
当飞书不回消息、控制台打不开，或者模型请求报错时，查看日志是第一选择：

 
 
- 实时滚动查看最新日志：docker logs -f openclaw_gateway
 
- 查看最后 100 行日志：docker logs --tail 100 openclaw_gateway
 
- (提示：按 Ctrl+C 退出日志实时查看)
 

 
3. 进入容器执行 OpenClaw 内部命令

 
如果需要修改 OpenClaw 的内部设置、更新 Token、或手动安装其他插件，需要“钻”进容器：

 
 
- 进入容器内部终端：docker exec -it openclaw_gateway bash
 
- (进入后，你的命令行会变成 root@<主机名>:/app#，在这里可以执行所有的 openclaw 原生命令，例如 openclaw security audit 或 openclaw gateway status。输入 exit 可退出容器回到树莓派终端。)
 
- 重启网关并且转日志到PC： openclaw gateway --port 18789
 
- docker restart ced56fd15ec0
 

 

 
cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada 

 
sudo python3 gpio_modbus_service.py￼￼

 
sudo pkill -f gpio_*; sleep 2 

 
cd /mnt/ssd/openclaw_data/.openclaw/workspace/scada 

 
sudo python3 gpio_led_light_modbus_service.py