# 🔌 MCP 协议学习计划

*创建：2026-03-26 | 优先级：🔴 高*

---

## 📚 什么是 MCP？

**Model Context Protocol (MCP)** 是一个开放协议，让 AI 模型能够安全地与外部工具和服务交互。

**类比**: MCP 是 AI 生态的"USB 接口"——各类 SaaS 工具通过 MCP 接入 AI，实现操作自动化。

---

## 🎯 学习目标

1. 理解 MCP 协议规范
2. 实现 MCP Client（让绾绾能通过 MCP 调用工具）
3. 集成至少 3 个 MCP Server（文件系统、GitHub、Notion 等）
4. 支持自然语言触发 MCP 操作

---

## 📖 学习资源

### 官方文档
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Anthropic MCP 介绍](https://www.anthropic.com/news/model-context-protocol)

### 现有实现
- **Beehiiv MCP**: 邮件通讯管理（语法检查、数据分析、文章起草）
- **Claude Code auto-mode**: 使用 MCP 进行权限决策
- **datasette-enrichments-llm**: Datasette 插件系统

### 参考项目
```bash
# 官方示例
git clone https://github.com/modelcontextprotocol/servers

# 常见 MCP Servers:
- filesystem (文件操作)
- github (GitHub API)
- notion (Notion API)
- slack (Slack API)
- postgres (数据库查询)
- puppeteer (浏览器自动化)
```

---

## 🗓️ 学习路径

### 第 1 周：理解协议（2026-03-26 ~ 04-01）

**目标**: 读懂 MCP 规范，理解核心概念

**任务**:
- [ ] 阅读 MCP specification
- [ ] 理解 Transport 层（stdio vs HTTP）
- [ ] 理解 Protocol 层（Initialize、ListTools、CallTool）
- [ ] 理解 Security 模型（权限、沙箱）

**产出**: `memory/mcp-protocol-notes.md` 学习笔记

### 第 2 周：实现 Client（2026-04-02 ~ 04-08）

**目标**: 在 OpenClaw 中实现 MCP Client

**任务**:
- [ ] 创建 `mcp-client.js` 或 `mcp-client.py`
- [ ] 实现 stdio transport（本地进程通信）
- [ ] 实现 HTTP transport（远程服务）
- [ ] 实现工具发现（list_tools）
- [ ] 实现工具调用（call_tool）
- [ ] 实现错误处理和超时

**产出**: `/openclaw_data/.openclaw/workspace/mcp/client.js`

### 第 3 周：集成 Servers（2026-04-09 ~ 04-15）

**目标**: 集成至少 3 个 MCP Server

**优先级**:
1. **filesystem** - 文件操作（高优先级）
2. **github** - GitHub API（高优先级）
3. **notion** - Notion API（中优先级）
4. **slack** - Slack API（中优先级）
5. **postgres** - 数据库查询（低优先级）

**任务**:
- [ ] 安装并测试 filesystem server
- [ ] 安装并测试 github server
- [ ] 创建 OpenClaw 技能包装器（让绾绾能自然语言调用）
- [ ] 编写使用文档

**产出**: 
- `/openclaw_data/.openclaw/workspace/mcp/servers/` 配置目录
- `skills/mcp-wrapper/SKILL.md` 技能文档

### 第 4 周：自然语言集成（2026-04-16 ~ 04-22）

**目标**: 让绾绾能用自然语言触发 MCP 操作

**任务**:
- [ ] 实现意图识别（用户说"上传文件" → 调用 filesystem.upload）
- [ ] 实现参数提取（"上传到 /tmp" → path="/tmp"）
- [ ] 实现结果格式化（MCP 响应 → 飞书消息）
- [ ] 添加安全确认（危险操作需用户确认）

**产出**: 完整的 MCP 集成技能

---

## 🔒 安全考虑

### 权限控制
- MCP Server 默认无权限访问敏感文件
- 需要显式配置允许的路径/操作
- 危险操作（删除、执行）需二次确认

### 沙箱隔离
- MCP Server 运行在独立进程
- 限制文件系统访问范围
- 网络访问白名单

### 审计日志
- 记录所有 MCP 调用
- 记录到 `memory/mcp-audit-log.md`
- 定期审查异常调用

---

## 📊 成功标准

| 阶段 | 完成标准 |
|------|----------|
| 第 1 周 | 能清晰解释 MCP 协议的核心概念 |
| 第 2 周 | MCP Client 能成功调用官方示例 server |
| 第 3 周 | 能用自然语言操作文件系统（上传/下载/列表） |
| 第 4 周 | 完整集成，支持至少 3 个服务 |

---

## 💡 应用场景

### 场景 1: 文件管理
```
用户："帮我把昨天的日志打包上传到 GitHub"
→ MCP filesystem: 读取 memory/2026-03-25.md
→ MCP filesystem: 创建 archive.zip
→ MCP github: 上传到 releases
```

### 场景 2: 代码审查
```
用户："检查一下今天的代码变更"
→ MCP github: 获取今日 commits
→ MCP github: 获取 diff
→ 绾绾分析并生成审查报告
```

### 场景 3: 知识库同步
```
用户："把这篇文档同步到 Notion"
→ MCP filesystem: 读取文档
→ MCP notion: 创建/更新页面
```

---

## 📝 进度追踪

| 日期 | 进展 | 备注 |
|------|------|------|
| 2026-03-26 | 创建学习计划 | 开始第 1 周 |
| - | - | - |

---

*下次更新：2026-04-01（第 1 周总结）*
