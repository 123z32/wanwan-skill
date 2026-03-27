# 📚 本周学习总结 — 2026 年第 13 周 (3/23-3/29)

*创建时间：2026-03-27 13:31 UTC+8*

---

## 📰 AI 前沿动态

### 1. 🔥 黄仁勋宣称"已实现 AGI" + 提到 OpenClaw (3/24-25)
- Lex Fridman 播客中，Nvidia CEO 黄仁勋直言："I think we've achieved AGI"
- 黄仁勋提到 OpenClaw 是开源 AI Agent 平台的"病毒式成功"
- 但也指出"很多人用了几个月就放弃了"，"10 万个 Agent 能创建 Nvidia 的概率是零"
- **意义**: OpenClaw 被行业顶级人物公开认可，但也提醒我们 Agent 平台的长期留存是挑战

### 2. 🇨🇳 中国日均 Token 调用量突破 140 万亿 (3/24)
- 两年增长千倍，Token 成为"智能时代的价值锚点"
- 黄仁勋：Token 正成为硅谷第四种薪酬
- **意义**: AI 使用量爆炸式增长，Token 经济正在形成

### 3. 💻 Arm 发布 AGI CPU：最高 136 核心，性能功耗比 x86 翻倍 (3/25)
- Arm 推出专为 AGI 工作负载设计的新 CPU
- 单 CPU 最高 136 核心，每瓦性能是 x86 芯片的两倍
- **意义**: 硬件厂商集体押注 AI 推理市场，芯片架构从通用计算向 AI 专用转型

### 4. 🍎 Apple 获 Gemini 完整访问权：训练小型设备端 AI 模型 (3/25)
- Apple 与 Google 1 月达成协议，可"完全访问"Google Gemini 模型
- 使用**蒸馏技术**训练专用于 Apple 设备的"学生"AI 模型
- **意义**: 端侧 AI 与大模型云服务的融合趋势，隐私保护 + 强大 AI 能力的平衡

### 5. ⚖️ Anthropic vs 五角大楼：法庭交锋 (3/24-25)
- Anthropic 寻求初步禁令，阻止被列为"军事供应链风险"
- 与特朗普政府在法官 Rita Lin 面前对峙
- **意义**: AI 公司与政府之间的关系复杂化，AI 治理从学术讨论进入法律博弈阶段

### 6. 📧 Beehiiv 通过 MCP 协议接入 AI 机器人 (3/24-25)
- 邮件通讯平台 Beehiiv 将其管理功能通过 MCP 协议接入 ChatGPT/Claude
- **意义**: MCP 正在成为 AI 生态的"USB 接口"，对 OpenClaw 这类 Agent 平台非常有利

---

## 🔧 技术学习

### 1. 股票/基金数据源开发
- **问题**: Yahoo Finance 在中国大陆被墙
- **解决**: 改用东方财富 API（股票）+ 天天基金 API（基金）
- **成果**: `stock-market-pro` skill 支持 A 股/港股/美股/基金实时查询
- **关键点**: A 股涨红跌绿（与美股相反），天天基金估值接口 `fundgz.1234567.com.cn`

### 2. OneNote 全量导出到 RAG 知识库
- **工具**: Microsoft Graph API via Maton 网关
- **成果**: 214 条笔记（587,309 字）成功导入个人知识库
- **技术**: HTML → Markdown 转换 + 标签分类 + 速率控制 (0.3s/请求)
- **RAG 系统**: 从 33 条 → 247 条知识块

### 3. OpenClaw 多智能体路由配置
- **配置**: 按渠道/联系人路由到不同智能体（绾绾/婳婳）
- **应用**: 技术问题→婳婳，生活/事务→绾绾
- **飞书绑定**: 婳婳绑定飞书渠道，实现自动路由

### 4. 本地 Embedding 配置
- **方案**: Ollama + nomic-embed-text
- **依赖**: AGX Thor 运行 Ollama，Tailscale VPN 透传
- **状态**: 等待 AGX Thor 连接稳定

### 5. OCR 工具安装
- **成功**: `tesseract-ocr` 中英文
- **应用**: 发票/行程单图片识别
- **限制**: `easyocr` 因网络超时未安装

---

## 💡 启发与思考

### 1. Agent 平台的长期挑战
黄仁勋的评论提醒我们：创建 Agent 容易，但让用户持续使用很难。绾绾需要：
- 提供持续价值（每日 AI 学习、基金播报、记忆管理）
- 建立使用习惯（心跳机制、每日总结）
- 避免成为"新鲜感玩具"

### 2. MCP 协议的战略价值
Beehiiv 的案例显示，MCP 正在成为 AI 生态的标准接口。对 OpenClaw 的启示：
- 未来可能只需实现 MCP 协议就能接入数百种服务
- 比逐个开发 API 集成更高效
- 建议纳入学习计划（见 `memory/mcp-learning-plan.md`）

### 3. 硬件 AI 化的趋势
从 Nvidia 的 AGI 宣言，到 Arm 的 AGI CPU，到 Intel 的 AI 专用 GPU——2026 年硬件厂商集体押注 AI 推理市场。这意味着：
- 端侧 AI 能力将大幅提升
- 树莓派 + AGX Thor 的架构符合趋势
- 本地 Embedding/推理的成本会持续下降

### 4. 数据隐私与 AI 的张力
Apple 的设备端 AI、Anthropic 的军事用途争议、WebinarTV 的 Zoom 抓取事件——都反映了 AI 时代的隐私和伦理挑战。绾绾作为私人助理：
- 必须坚持隐私优先原则
- 敏感数据本地处理
- 外部 API 调用需用户授权

---

## 📖 参考资料

- [OpenClaw 被黄仁勋提及](https://github.com/openclaw/openclaw)
- [Arm AGI CPU 发布](https://www.arm.com/)
- [MCP 协议](https://modelcontextprotocol.io/)
- [天天基金估值 API](http://fundgz.1234567.com.cn/)
- [东方财富 API](https://quote.eastmoney.com/)

---

## 📊 本周工作统计

| 项目 | 进展 |
|------|------|
| OpenClaw 版本 | 2026.3.24 ✅ |
| 股票/基金 skill | ✅ 完成并上线 |
| OneNote 导出 | ✅ 214 条/587K 字 |
| RAG 知识库 | ✅ 247 条知识块 |
| 多智能体路由 | ✅ 已配置 |
| 每日基金播报 | ✅ 交易日自动播报 |
| AI 前沿学习 | ✅ 每日更新 |
| Git 备份 | ✅ 每日自动 |

---

*最后更新：2026-03-27 13:31 UTC+8*
