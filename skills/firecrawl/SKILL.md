---
name: firecrawl
description: 使用 Firecrawl 爬取网页内容，支持 Markdown、HTML、截图等多种格式。
homepage: https://www.firecrawl.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "🕷️",
        "requires": { "bins": ["curl", "python3"] },
        "install": [],
      },
  }
---

# Firecrawl 网页爬虫技能

通过本地 Firecrawl 容器爬取网页内容，支持单页爬取、全站爬取、站点地图等功能。

## 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "firecrawl": {
      "enabled": true,
      "baseUrl": "http://172.17.0.1:3002",
      "timeout": 60,
      "defaultFormats": ["markdown", "html"]
    }
  }
}
```

## 使用方法

### 1. 爬取单个网页

```bash
# 基础用法
python3 /home/node/.openclaw/workspace/scripts/firecrawl_scrape.py https://example.com

# 指定格式
python3 /home/node/.openclaw/workspace/scripts/firecrawl_scrape.py https://example.com --formats markdown html

# 输出到文件
python3 /home/node/.openclaw/workspace/scripts/firecrawl_scrape.py https://example.com --output result.md
```

### 2. 爬取整个网站

```bash
python3 /home/node/.openclaw/workspace/scripts/firecrawl_crawl.py https://example.com --limit 10 --max-depth 2
```

### 3. 获取站点地图

```bash
python3 /home/node/.openclaw/workspace/scripts/firecrawl_map.py https://example.com
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/scrape` | POST | 爬取单个网页 |
| `/v1/crawl` | POST | 爬取整个网站 |
| `/v1/map` | POST | 获取站点所有链接 |

## 请求格式

### Scrape（单页爬取）

```json
{
  "url": "https://example.com",
  "formats": ["markdown", "html", "screenshot"],
  "onlyMainContent": true,
  "waitFor": 0
}
```

### Crawl（全站爬取）

```json
{
  "url": "https://example.com",
  "limit": 10,
  "maxDepth": 2,
  "formats": ["markdown"]
}
```

### Map（站点地图）

```json
{
  "url": "https://example.com"
}
```

## 响应格式

```json
{
  "success": true,
  "data": {
    "markdown": "# Page Title\n\nPage content...",
    "html": "<html>...</html>",
    "metadata": {
      "title": "Page Title",
      "description": "Page description",
      "url": "https://example.com"
    }
  }
}
```

## 错误处理

| 错误码 | 说明 |
|--------|------|
| 400 | 请求格式错误 |
| 401 | 需要 API key（如果配置了认证） |
| 404 | 网页不存在 |
| 408 | 请求超时 |
| 429 | 请求过于频繁 |
| 500 | 服务器错误 |

## 注意事项

1. **容器连接**：确保 Firecrawl 容器在运行，可通过 `http://172.17.0.1:3002` 访问
2. **超时设置**：复杂网页可能需要更长时间，适当增加 `timeout`
3. **速率限制**：避免短时间内大量请求，防止被目标网站封禁
4. ** robots.txt**：遵守目标网站的 robots.txt 规则

## 示例：在飞书中使用

在飞书发送消息：
- "爬取 https://example.com"
- "抓取这个网页的 Markdown：https://example.com"
- "获取 https://example.com 的所有链接"

绾绾会自动调用 Firecrawl 技能并返回结果。

---

*最后更新：2026-04-07*
