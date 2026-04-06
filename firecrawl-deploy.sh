#!/bin/bash
# 🔥 Firecrawl 自托管部署脚本 - 树莓派版
# 使用方法：bash firecrawl-deploy.sh

set -e

echo "🔥=========================================="
echo "🔥 Firecrawl 自托管部署脚本"
echo "🔥=========================================="
echo ""

# 步骤 1: 检查 Docker
echo "📌 步骤 1/5: 检查 Docker 环境..."
if command -v docker &> /dev/null; then
    echo "✅ Docker 已安装：$(docker --version)"
else
    echo "❌ Docker 未安装！"
    echo "请先安装 Docker:"
    echo "  curl -fsSL https://get.docker.com | sh"
    echo "  sudo usermod -aG docker $USER"
    exit 1
fi

if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
    echo "✅ Docker Compose 已安装"
else
    echo "⚠️ Docker Compose 未安装，尝试安装..."
    sudo apt-get update
    sudo apt-get install -y docker-compose-plugin
fi

echo ""

# 步骤 2: 创建部署目录
echo "📌 步骤 2/5: 创建部署目录..."
DEPLOY_DIR=~/firecrawl-selfhost
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR
echo "✅ 部署目录：$DEPLOY_DIR"
echo ""

# 步骤 3: 创建 .env 配置文件
echo "📌 步骤 3/5: 创建配置文件..."
cat > .env << 'EOF'
# ===== 必需配置 =====
PORT=3002
HOST=0.0.0.0

# 数据库认证（关闭，简化部署）
USE_DB_AUTHENTICATION=false

# ===== Redis（用于队列）=====
REDIS_URL=redis://redis:6379

# ===== 日志 =====
LOG_LEVEL=info

# ===== AI 功能（可选）=====
# OPENAI_API_KEY=sk-xxx
# OLLAMA_BASE_URL=http://localhost:11434/api
# MODEL_NAME=qwen2.5:7b

# ===== 代理配置（可选）=====
# PROXY_SERVER=http://proxy.example.com:8080
# PROXY_USERNAME=
# PROXY_PASSWORD=
EOF
echo "✅ .env 配置文件已创建"
echo ""

# 步骤 4: 创建 docker-compose.yml
echo "📌 步骤 4/5: 创建 Docker Compose 配置..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    image: ghcr.io/firecrawl/firecrawl:latest
    ports:
      - "3002:3002"
    environment:
      - PORT=3002
      - HOST=0.0.0.0
      - REDIS_URL=redis://redis:6379
      - USE_DB_AUTHENTICATION=false
      - LOG_LEVEL=info
    depends_on:
      - redis
    volumes:
      - firecrawl_data:/app/data
    restart: unless-stopped
    networks:
      - firecrawl-network

  redis:
    image: redis:7-alpine
    environment:
      - REDIS_PORT=6379
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - firecrawl-network

volumes:
  firecrawl_data:
  redis_data:

networks:
  firecrawl-network:
    driver: bridge
EOF
echo "✅ docker-compose.yml 已创建"
echo ""

# 步骤 5: 启动服务
echo "📌 步骤 5/5: 启动 Firecrawl 服务..."
if docker compose version &> /dev/null 2>&1; then
    docker compose up -d
else
    docker-compose up -d
fi

echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 验证服务
echo ""
echo "📊 验证服务状态..."
if docker compose version &> /dev/null 2>&1; then
    docker compose ps
else
    docker-compose ps
fi

echo ""
echo "🌐 测试 API 连接..."
sleep 5
HEALTH_RESPONSE=$(curl -s http://localhost:3002/health || echo "failed")
if [ "$HEALTH_RESPONSE" != "failed" ]; then
    echo "✅ API 健康检查成功！"
    echo "响应：$HEALTH_RESPONSE"
else
    echo "⚠️ API 健康检查失败，服务可能还在启动中..."
    echo "请稍后手动测试：curl http://localhost:3002/health"
fi

echo ""
echo "🎉=========================================="
echo "🎉 Firecrawl 部署完成！"
echo "🎉=========================================="
echo ""
echo "📍 服务信息:"
echo "  API 地址：http://localhost:3002"
echo "  健康检查：http://localhost:3002/health"
echo "  部署目录：$DEPLOY_DIR"
echo ""
echo "📚 常用命令:"
echo "  查看状态：cd $DEPLOY_DIR && docker compose ps"
echo "  查看日志：cd $DEPLOY_DIR && docker compose logs -f"
echo "  停止服务：cd $DEPLOY_DIR && docker compose down"
echo "  重启服务：cd $DEPLOY_DIR && docker compose restart"
echo ""
echo "🔗 与 OpenClaw 集成:"
echo "  在 OpenClaw 配置中添加:"
echo '  {'
echo '    "plugins": {'
echo '      "entries": {'
echo '        "firecrawl": {'
echo '          "enabled": true,'
echo '          "config": {'
echo '            "webFetch": {'
echo '              "baseUrl": "http://localhost:3002",'
echo '              "apiKey": "local-no-auth"'
echo '            }'
echo '          }'
echo '        }'
echo '      }'
echo '    }'
echo '  }'
echo ""
echo "✅ 部署脚本执行完成！"
