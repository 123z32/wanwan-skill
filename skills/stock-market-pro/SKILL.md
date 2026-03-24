---
name: stock-market-pro
description: "实时股票行情查询、历史走势、公司信息。支持美股、A股、港股、加密货币。使用 Yahoo Finance 数据，无需 API key。"
version: "1.0.0-local"
author: 绾绾 (基于 sundial-org/awesome-openclaw-skills)
license: MIT
category: finance
tags:
  - stock
  - realtime
  - chart
  - yahoo-finance
languages:
  - en
  - zh
---

# Stock Market Pro - 实时股票行情

基于 Yahoo Finance 的专业股票查询工具，无需 API key。

## 功能

### 1. 实时行情 (`price`)
```bash
bash scripts/stock.sh AAPL price
bash scripts/stock.sh 600519.SS 行情    # 茅台
bash scripts/stock.sh 0700.HK price     # 腾讯
bash scripts/stock.sh BTC-USD price     # 比特币
```

### 2. 公司信息 (`info`)
```bash
bash scripts/stock.sh NVDA info
```

### 3. 历史走势 (`history`)
```bash
bash scripts/stock.sh TSLA history      # 近30天走势
bash scripts/stock.sh 000001.SS 历史    # 上证指数
```

## 代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 美股 | TICKER | AAPL, NVDA, TSLA, MSFT |
| A股(上海) | 代码.SS | 600519.SS(茅台), 601318.SS(平安) |
| A股(深圳) | 代码.SZ | 000858.SZ(五粮液), 000001.SZ(平安银行) |
| 港股 | 代码.HK | 0700.HK(腾讯), 9988.HK(阿里) |
| 加密货币 | COIN-USD | BTC-USD, ETH-USD |
| 指数 | ^代码 | ^GSPC(标普500), ^DJI(道指), 000001.SS(上证) |

## 脚本位置

`/openclaw_data/.openclaw/workspace/skills/stock-market-pro/scripts/stock.sh`

## 依赖

- curl (已安装)
- python3 (已安装)
- 网络访问 Yahoo Finance API

## 注意

- 数据来自 Yahoo Finance，可能有 15 分钟延迟
- A股实时数据在交易时间内可用
- 非投资建议，仅供参考
