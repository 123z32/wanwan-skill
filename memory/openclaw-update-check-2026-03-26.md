# OpenClaw 更新检查 — 2026-03-26

## 📊 版本状态

| 项目 | 信息 |
|------|------|
| **当前版本** | 2026.3.13 (61d171a) |
| **最新版本** | 2026.3.24 |
| **发布日期** | 2026-03-25 16:57 UTC |
| **差距** | 落后 11 天版本 |
| **建议** | ✅ 建议升级 |

---

## 🔥 2026.3.24 主要更新

### ✨ 新功能

1. **Gateway/OpenAI 兼容性**
   - 新增 `/v1/models` 和 `/v1/embeddings` 端点
   - 支持转发显式模型覆盖到 `/v1/chat/completions` 和 `/v1/responses`
   - 更广泛的客户端和 RAG 兼容性

2. **Agents/Tools 改进**
   - `/tools` 命令现在显示当前代理实际可用的工具
   - 新增紧凑默认视图 + 可选详细模式
   - Control UI 新增 "Available Right Now" 实时区域

3. **Microsoft Teams 集成**
   - 迁移到官方 Teams SDK
   - 添加 AI-agent UX 最佳实践（流式回复、欢迎卡片、反馈等）
   - 支持消息编辑和删除

4. **Skills 一键安装**
   - 捆绑技能新增一键安装配方（coding-agent, gh-issues, weather 等）
   - Control UI 技能管理增强（状态过滤、点击查看详情、API key 输入）

5. **CLI 容器支持**
   - 新增 `--container` 和 `OPENCLAW_CONTAINER` 环境变量
   - 可在运行中的 Docker/Podman OpenClaw 容器内执行命令

6. **Discord 自动线程命名**
   - 可选 `autoThreadName: "generated"` 使用 LLM 生成简洁线程名

### 🐛 重要修复

1. **安全/沙箱**: 修复 mediaUrl/fileUrl 别名绕过漏洞 (#54034)
2. **Gateway 重启**: 修复重启后会话唤醒问题 (#53940)
3. **Docker 安装**: 修复 fresh Docker 安装的启动失败 (#53385)
4. **Gateway 通道**: 通道启动改为顺序执行，避免单通道失败阻塞其他 (#54215)
5. **WhatsApp**: 修复群聊回复检测和 bot 检测问题
6. **Telegram**: 修复论坛主题路由、照片上传、错误处理

### 📦 技能更新

以下技能新增一键安装支持：
- coding-agent
- gh-issues
- openai-whisper-api
- session-logs
- tmux
- trello
- weather

---

## 🚀 升级命令

```bash
# 方式 1: 使用 OpenClaw CLI（推荐）
openclaw update

# 方式 2: 使用 npm
npm install -g openclaw@latest

# 方式 3: 指定版本
npm install -g openclaw@2026.3.24
```

---

## ⚠️ 升级前检查

- [ ] 备份配置文件：`/openclaw_data/config/config.json`
- [ ] 备份工作区：`/openclaw_data/.openclaw/workspace/`
- [ ] 确认 Node.js 版本 ≥ 22.14（推荐 Node 24）
- [ ] 检查当前是否有运行中的任务

---

## 📝 升级后验证

```bash
# 检查版本
openclaw --version

# 检查 Gateway 状态
openclaw gateway status

# 检查技能状态
openclaw skills info

# 测试 RAG 系统
curl http://localhost:9900/api/stats
```

---

## 💡 值得升级的理由

1. **安全性**: 修复了沙箱媒体访问漏洞
2. **稳定性**: 多个 Gateway 和通道启动修复
3. **兼容性**: 更好的 OpenAI API 兼容，对 RAG 系统有利
4. **用户体验**: Control UI 技能管理大幅改进
5. **容器支持**: 对 Docker 部署更友好

---

*检查时间：2026-03-26 05:22 UTC*
*下次检查：2026-04-02*
