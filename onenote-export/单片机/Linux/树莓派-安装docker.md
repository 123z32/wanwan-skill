# 树莓派-安装docker

> 来源: OneNote > 单片机 > Linux
> 修改: 2026-03-16T01:32:55Z

树莓派-安装docker
 
 
 
 
 

 
更新软件源并安装 Docker 及 Compose 插件：

 
sudo apt update

 
sudo apt install docker.io docker-compose-v2 -y

 

 
将当前用户加入 Docker 用户组： (这一步是为了让你以后运行 docker 命令时，不需要每次都敲 sudo 输密码)

 
sudo usermod -aG docker $USER

 

 
验证版本docker

 
docker --version

 
docker compose version

 

 
创建数据目录并下载官方配置

 
将所有相关的配置、长期记忆和知识库数据都集中放在 ~/openclaw_data 文件夹里

 
mkdir -p ~/openclaw_data

 
cd ~/openclaw_data

 
git clone [https://github.com/openclaw/openclaw.git .

 

 

 
cd ~/openclaw-docker