# 树莓派-SSH流程

> 来源: OneNote > 单片机 > Linux
> 修改: 2026-03-15T08:44:55Z

树莓派-SSH流程
 
 
 
 
 

 
ssh-keygen -R wanwanhua#清除本地保存的旧密钥记录

 
sudo reboot#重启服务器

 
sudo systemctl status ssh#检查并启动 SSH 服务

 

 
Ssh wanwanhua@wanwanhhua#局域网ssh连接

 
安装 Tailscale

 
打开终端（Terminal），运行以下官方安装命令。该命令会下载并执行安装脚本，自动处理依赖和软件源配置：

 
curl -fsSL [https://tailscale.com/install.sh | sh

 
注意：如果提示 curl 未找到，请先运行 

 
sudo apt update && sudo apt install curl -y 进行安装

 

 
ssh wanwanhua@100.93.35.112#Tailscale虚拟局域网ssh连接

 
启用 Tailscale SSH ：

 
sudo tailscale set --ssh=true

 
Tailscale SSH连接（不需要密码）

 
tailscale ssh wanwanhua@100.93.35.112