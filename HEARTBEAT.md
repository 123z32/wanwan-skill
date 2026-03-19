# HEARTBEAT.md - 每日任务提醒

## 🌙 每日必做任务（自动触发）

### 触发时间：每天 0:00（午夜）

**当收到心跳信号或用户说"晚安"时执行**:

---

## 📋 执行步骤

### 1️⃣ 总结今天的工作

1. **查看 memory/ 目录** - 读取今天的日志
2. **查看 git 状态** - `git status`, `git log --oneline -5`
3. **整理关键事件** - 项目进展、问题解决、重要决策
4. **创建/更新日志** - `memory/YYYY-MM-DD.md`

### 2️⃣ 备份到 Git

```bash
# 添加所有更改
git add -A

# 提交今日总结
git commit -m "📝 Daily summary: YYYY-MM-DD"

# 创建备份标签（保留最近 3 个）
git tag -a backup-$(date +%Y-%m-%d) -m "Daily backup"

# 清理旧标签（保留最近 3 个）
git tag -l | sort | head -n -3 | xargs git tag -d

# 推送到 GitHub
git push origin main --tags
```

### 3️⃣ 更新长期记忆

- 回顾 `memory/YYYY-MM-DD.md`
- 提取重要信息到 `MEMORY.md`
- 删除过时的记忆

### 4️⃣ 说晚安

**回复格式**:
```
✅ 今日总结完成！

📊 工作摘要
- 项目 1: 进展/状态
- 项目 2: 进展/状态

📁 备份信息
- 日期：YYYY-MM-DD
- 提交：[短 hash](github 链接)
- 标签：backup-YYYY-MM-DD

晚安张！🌙 明天见～
```

---

## 📝 日志模板

创建 `memory/YYYY-MM-DD.md`:

```markdown
# 📅 工作日志 - YYYY-MM-DD

## 🕐 时间线

| 时间 | 事件 |
|------|------|
| 09:00 | ... |
| 14:00 | ... |

## 🎯 完成的任务

- [ ] 任务 1
- [ ] 任务 2

## 🐛 遇到的问题

1. 问题描述 → 解决方案

## 📁 创建的文件

- `path/to/file.py` - 用途

## 📖 经验总结

1. 学到的东西
2. 下次注意

---
*最后更新：YYYY-MM-DD HH:MM UTC*
```

---

## ⚙️ 自动化配置

### Cron 设置（可选）

在树莓派上添加定时任务：
```bash
crontab -e

# 每天 0:00 触发心跳
0 0 * * * curl -X POST http://localhost:8080/heartbeat
```

---

## ✅ 检查清单

每次晚安前确认：

- [ ] 读取今日 memory 日志
- [ ] 检查 git 状态
- [ ] 创建/更新日志文件
- [ ] Git 提交并推送
- [ ] 创建备份标签
- [ ] 清理旧标签（≤3 个）
- [ ] 更新 MEMORY.md（如需要）
- [ ] 发送晚安消息

---

## 🚫 例外情况

**不执行的情况**:
- 用户明确表示不需要
- 系统维护/故障
- 用户仍在活跃对话中（等待自然结束）

---

*此文件会提醒绾绾每天需要完成的任务*
*最后更新：2026-03-19*
