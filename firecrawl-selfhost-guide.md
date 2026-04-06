# 🔥 Firecrawl 自托管部署指南

**文档来源**: https://github.com/firecrawl/firecrawl  
**更新时间**: 2026-04-05  
**适用版本**: Firecrawl 2026 最新版

---

## 📋 自托管优势与限制

### ✅ 优势
- **安全合规**: 数据保留在自己基础设施内
- **可定制**: 可根据需求定制服务
- **学习价值**: 深入了解 Firecrawl 工作原理
- **免费**: 无需支付 API 费用

### ⚠️ 限制
- **无 Fire-engine**: 无法访问高级反反爬功能
- **手动配置**: 需要自己配置代理等
- **维护成本**: 需要自己维护和更新

---

## 🛠️ 部署方式

### 方式 1: Docker Compose（推荐）⭐

#### 1. 环境要求
- Docker 20.10+
- Docker Compose 2.0+
- 至少 4GB RAM
- 20GB 磁盘空间

#### 2. 创建项目目录
```bash
mkdir -p ~/firecrawl-selfhost
cd ~/firecrawl-selfhost
```

#### 3. 创建 .env 配置文件
```bash
cat > .env << 'EOF'
# ===== 必需配置 =====
PORT=3002
HOST=0.0.0.0

# 数据库认证（可选，使用 Supabase）
USE_DB_AUTHENTICATION=false

# ===== AI 功能（可选）=====
# OPENAI_API_KEY=sk-xxx
# OPENAI_BASE_URL=https://api.openai.com/v1

# 使用 Ollama（实验性）
# OLLAMA_BASE_URL=http://localhost:11434/api
# MODEL_NAME=deepseek-r1:7b
# MODEL_EMBEDDING_NAME=nomic-embed-text

# ===== 代理配置（可选）=====
# PROXY_SERVER=http://proxy.example.com:8080
# PROXY_USERNAME=
# PROXY_PASSWORD=

# ===== 搜索 API（可选）=====
# SEARXNG_ENDPOINT=http://your.searxng.server

# ===== Supabase（可选）=====
# SUPABASE_ANON_TOKEN=
# SUPABASE_URL=
# SUPABASE_SERVICE_TOKEN=

# ===== Redis（可选，用于队列）=====
# REDIS_URL=redis://localhost:6379

# ===== 日志 =====
LOG_LEVEL=info
EOF
```

#### 4. 创建 docker-compose.yml
```bash
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
      - USE_DB_AUTHENTICATION=false
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
EOF
```

#### 5. 启动服务
```bash
docker compose up -d
```

#### 6. 验证运行状态
```bash
docker compose ps
curl http://localhost:3002/health
```

#### 7. 查看日志
```bash
docker compose logs -f app
```

---

### 方式 2: 源码部署

#### 1. 克隆仓库
```bash
git clone https://github.com/firecrawl/firecrawl.git
cd firecrawl
```

#### 2. 安装依赖
```bash
# Node.js 18+  required
npm install

# 或者使用 pnpm
pnpm install
```

#### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要参数
```

#### 4. 启动服务
```bash
# 开发模式
npm run dev

# 生产模式
npm run build
npm run start
```

---

## 🔧 配置说明

### 必需配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 3002 | API 服务端口 |
| `HOST` | 0.0.0.0 | 监听地址 |
| `USE_DB_AUTHENTICATION` | false | 是否启用数据库认证 |

### 可选配置

#### AI 功能
```bash
# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1

# Ollama（本地模型）
OLLAMA_BASE_URL=http://localhost:11434/api
MODEL_NAME=deepseek-r1:7b
```

#### 代理配置
```bash
#  authenticated proxy
PROXY_SERVER=http://proxy.example.com:8080
PROXY_USERNAME=user
PROXY_PASSWORD=pass

#  unauthenticated proxy
PROXY_SERVER=192.168.1.100:8080
```

#### 搜索配置
```bash
# 使用 SearXNG 代替 Google
SEARXNG_ENDPOINT=http://your.searxng.server
SEARXNG_ENGINES=google,bing
SEARXNG_CATEGORIES=general
```

---

## 📊 API 使用

### 本地 API 端点

启动后，API 可通过以下地址访问：
- **主 API**: `http://localhost:3002`
- **健康检查**: `http://localhost:3002/health`
- **文档**: `http://localhost:3002/docs`（如启用）

### 示例请求

#### Scrape（抓取网页）
```bash
curl -X POST 'http://localhost:3002/v2/scrape' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://example.com"
  }'
```

#### Search（搜索）
```bash
curl -X POST 'http://localhost:3002/v2/search' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "firecrawl",
    "limit": 5
  }'
```

#### Crawl（爬取网站）
```bash
curl -X POST 'http://localhost:3002/v2/crawl' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://example.com",
    "limit": 100
  }'
```

---

## 🔗 与 OpenClaw 集成

### 配置 OpenClaw 使用本地 Firecrawl

编辑 `/home/node/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "firecrawl": {
        "enabled": true,
        "config": {
          "webFetch": {
            "baseUrl": "http://localhost:3002",
            "apiKey": "local-no-auth"
          }
        }
      }
    }
  }
}
```

### 重启 OpenClaw
```bash
pkill -f openclaw-gateway
openclaw gateway --port 18789 &
```

---

## 🐛 故障排查

### 问题 1: 容器启动失败
```bash
# 检查日志
docker compose logs app

# 常见原因：
# - 端口被占用
# - 环境变量配置错误
# - 内存不足
```

### 问题 2: 抓取失败
```bash
# 检查网络连接
curl -I https://example.com

# 检查代理配置
# 某些网站可能需要代理才能访问
```

### 问题 3: Redis 连接失败
```bash
# 检查 Redis 是否运行
docker compose ps redis

# 测试 Redis 连接
docker compose exec redis redis-cli ping
```

---

## 📈 性能优化

### 1. 增加并发
```bash
# 在 .env 中设置
MAX_CONCURRENT_REQUESTS=10
```

### 2. 配置缓存
```bash
# 启用 Redis 缓存
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600
```

### 3. 调整超时
```bash
# 增加抓取超时
TIMEOUT=30000
```

---

## 🔒 安全建议

### 1. 启用认证
```bash
USE_DB_AUTHENTICATION=true
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_TOKEN=your_token
```

### 2. 配置防火墙
```bash
# 只允许本地访问
ufw allow from 127.0.0.1 to any port 3002

# 或者只允许内网
ufw allow from 192.168.1.0/24 to any port 3002
```

### 3. 使用 HTTPS
```bash
# 使用 Nginx 反向代理
# 配置 Let's Encrypt SSL 证书
```

---

## 📚 参考链接

- **GitHub**: https://github.com/firecrawl/firecrawl
- **文档**: https://docs.firecrawl.dev
- **Discord**: https://discord.gg/firecrawl
- **自托管讨论**: https://github.com/firecrawl/firecrawl/issues

---

*最后更新：2026-04-05*
