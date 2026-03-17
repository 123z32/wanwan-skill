# MEMORY.md - 长期记忆

*最后更新：2026-03-17*

---

## 👤 用户信息
- **称呼**: 张
- **工作地点**: 深圳光明区中山大学深圳校区
- **临时居住**: 惠州（出差项目）
- **时区**: 中国标准时间 (UTC+8)

---

## 🏗️ 系统架构
- **AGX Thor** (深圳): 128GB VRAM, 运行 Ollama
- **树莓派 5**: 8GB RAM + 128GB SSD, 托管 OpenClaw 容器
- **连接**: Tailscale VPN, 远程 Ollama 模型透传（无需 API key）
- **运行时**: Docker 容器隔离

---

## 🤖 助手身份
- **名字**: 绾绾
- **角色**: 助理
- **模型**: Qwen3.5-Plus (云端)
- **默认模型**: ollama/qwen3.5:35b-a3b

---

## 📋 交流规则
1. **语言**: 全程使用中文
2. **文件操作**: 删除文件前必须征得同意
3. **回复风格**: 不需要"敲键盘"表情包，直接回复
4. **隐私**: 保存对话记录到 memory/ 目录

---

## 🛠️ 已实现功能

### 飞书聊天记录读取 (2026-03-17)
- **工具**: `feishu_chat` (action: `history`)
- **API**: 飞书开放平台 `im.message.list`
- **chat_id**: `oc_d77a50191711fcda0c3fab1a2d0e910c`
- **状态**: ✅ 完成

---

## 📅 重要日期
- **2026-03-11**: 初次通过飞书联系
- **2026-03-16**: 正式确立助理关系，制定交流规则
- **2026-03-17**: 开发飞书聊天记录功能

---

## 📂 文件位置
- **日志**: `/openclaw_data/.openclaw/workspace/memory/YYYY-MM-DD.md`
- **配置**: `/openclaw_data/config/config.json`
- **工作区**: `/openclaw_data/.openclaw/workspace/`

---

*此文件会定期更新，记录重要信息和决策*
