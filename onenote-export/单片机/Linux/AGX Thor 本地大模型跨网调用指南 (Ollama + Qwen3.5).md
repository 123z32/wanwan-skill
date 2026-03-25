# AGX Thor 本地大模型跨网调用指南 (Ollama + Qwen3.5)

> 来源: OneNote > 单片机 > Linux
> 修改: 2026-03-15T08:38:03Z

AGX Thor 本地大模型跨网调用指南 (Ollama + Qwen3.5)
 
 
 
 
 

 

 

 

 
核心网络架构

 
 
- 服务端（Edge AI Node）：NVIDIA Jetson AGX Thor，运行 Ollama 底座和 Qwen3.5 模型。
 
- 客户端（Client）：Windows 开发机，运行 Python 脚本。
 
- 网络连接：通过 Tailscale 组建虚拟局域网（服务端分配 IP 为 100.100.145.74）。
 

 

 
第一阶段：服务端配置 (AGX Thor)

 
目标：解决 Ollama 默认仅监听 127.0.0.1 导致的客户端 [WinError 10061] 积极拒绝 报错。

 
1. 安装文本编辑器（如未预装）

 
Bash

 

 
sudo apt update￼sudo apt install nano -y￼

 
2. 修改 Ollama 系统服务配置 打开服务配置文件：

 
Bash

 

 
sudo nano /etc/systemd/system/ollama.service￼

 
在 [Service] 模块下，添加环境变量，强制监听所有网卡：

 
Ini, TOML

 

 
[Service]￼Environment="OLLAMA_HOST=0.0.0.0"￼# ...其他原有配置保持不变...￼

 
(保存退出快捷键：Ctrl+O -> Enter -> Ctrl+X)

 
3. 重载配置并重启服务

 
Bash

 

 
sudo systemctl daemon-reload￼sudo systemctl restart ollama￼

 

 
第二阶段：客户端代码 (Windows Python)

 
目标：

 
 
- 解决 MissingSchema 报错：URL 必须包含完整的 http:// 和端口号 11434。
 
- 解决 502 Bad Gateway (JSON 解析错误)：在代码中屏蔽 Windows 系统代理，防止请求被代理软件错误拦截。
 

 
完整的正确代码 (main.py)：

 
Python

 

 
import requests￼

 
# 1. 完整的接口地址 (协议 + Tailscale IP + 端口 + 路径)￼url = "[http://100.100.145.74:11434/api/chat"￼

 
# 2. 请求载荷 (模型名称需与服务端 ollama list 保持绝对一致)￼payload = {￼ "model": "qwen3.5", ￼ "messages": [￼ {"role": "user", "content": "你好，请介绍一下你自己。"}￼ ],￼ "stream": False # False表示等待模型全部生成完毕后一次性返回￼}￼

 
# 3. 屏蔽系统代理，防止局域网请求被拦截 (解决 502 报错)￼proxies = {￼ "http": None,￼ "https": None￼}￼

 
try:￼ print("正在连接 AGX Thor 发送请求...")￼ # 发送 POST 请求￼ response = requests.post(url, json=payload, proxies=proxies)￼ ￼ # 判断 HTTP 状态码￼ if response.status_code == 200:￼ result = response.json()￼ print("\n🤖 模型回复:\n")￼ print(result['message']['content'])￼ else:￼ print(f"请求失败！HTTP 状态码: {response.status_code}")￼ print(f"服务器端返回: {response.text}")￼

 
except requests.exceptions.RequestException as e:￼ print(f"\n❌ 网络连接发生错误:\n{e}")