# 📚 本周学习总结 — 2026 年第 14 周

## 📅 时间范围
2026-03-31 至 2026-04-03

---

## 📰 AI 前沿动态

### 黄仁勋宣称"已实现 AGI" + 提到 OpenClaw
- **来源**: Lex Fridman 播客
- **内容**: Nvidia CEO 黄仁勋直言 "I think we've achieved AGI"
- **OpenClaw 提及**: 被称作开源 AI Agent 平台的"病毒式成功"
- **警示**: "很多人用了几个月就放弃了"，"10 万个 Agent 能创建 Nvidia 的概率是零"
- **意义**: OpenClaw 被行业顶级人物公开认可，但也提醒可持续性很重要

### Arm 发布 AGI CPU
- **规格**: 最高 136 核心，专为 AGI 工作负载设计
- **优势**: 每瓦性能是 x86 芯片的两倍
- **意义**: 硬件厂商开始围绕"AGI"概念设计专用处理器

### Beehiiv 通过 MCP 协议接入 AI
- **内容**: 邮件通讯平台通过 MCP 协议接入 ChatGPT/Claude 等 AI
- **意义**: MCP 正在成为 AI 生态的"USB 接口"，对 OpenClaw 这类 Agent 平台有利

---

## 🔧 技术学习

### 1. Gateway 容器故障排查 (2026-04-03)
**问题**: openclaw-gateway 容器不断重启

**原因**: 配置文件中包含无效参数 `cdpPortRangeEnd`（browser 部分）

**解决**:
- 备份原配置文件
- 移除废弃参数
- 重启容器

**教训**: 配置文件升级时要注意版本兼容性，修改前务必备份

### 2. claude-code CLI 安装与限制 (2026-04-03)
**安装**: 成功安装 claude-code CLI (v2.1.91)

**限制发现**:
- 只支持 Anthropic API (`ANTHROPIC_API_KEY`)
- 不支持 OpenAI 兼容 API（硅基流动/Qwen）
- 只认官方合作云服务（Bedrock/Vertex/Foundry）

**结论**: 继续使用 OpenClaw + Qwen 模型，不需要 claude-code

### 3. Chromium 浏览器安装 (2026-04-03)
**安装**: 容器内安装 Chromium 146.0.7680.177

**问题**: browser 工具仍超时（容器内启动需要额外配置）

**待办**: 可能需要调整容器配置或重启 Gateway

### 4. 发票整理工作流优化 (2026-04-02)
**工具**: pdftotext (poppler-utils 22.12.0) + image OCR

**流程**:
1. 用户发送 PDF 发票/行程单
2. 自动解析关键字段（时间、起点、终点、金额）
3. 整理到飞书表格

**成果**: 整理 60 个行程，总金额 ¥682.01

### 5. 每日备份机制完善 (2026-04-02)
**问题**: 忘记主动执行每日备份

**改进**:
- 建立检查清单习惯
- 每天工作完成后对照 HEARTBEAT.md 逐项检查
- 主动执行 > 被动提醒

---

## 💡 启发与思考

### 1. 系统稳定性的重要性
- Gateway 容器重启问题影响用户体验
- 需要更完善的监控和自动恢复机制
- 心跳检查是很好的实践

### 2. 工具选型要匹配需求
- claude-code 虽好，但不支持 Qwen API
- OpenClaw + 硅基流动 + Qwen 是更合适的组合
- 不要盲目追求"名牌"工具，适合的才是最好的

### 3. 主动服务 > 被动响应
- 用户提醒才备份 = 体验不好
- 建立例行任务检查清单
- 每日总结、备份、晚安要主动完成



---

## 📖 参考资料

- OpenClaw 文档：https://docs.openclaw.ai
- 硅基流动 API：https://api.siliconflow.cn
- Qwen 模型：https://qwenlm.github.io
- MCP 协议：https://modelcontextprotocol.io

---

## 📊 本周统计数据

| 指标 | 数值 |
|------|------|
| Git 提交 | 10+ |
| 创建文件 | 15+ |
| 修复问题 | 3 (Gateway 重启、API 密钥、browser 超时) |
| 整理发票 | 60 个行程 |
| 系统运行时间 | 稳定 |

---

*最后更新：2026-04-03 23:11 UTC*
*第 14 周完成 ✅*
