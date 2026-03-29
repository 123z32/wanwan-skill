# 🔄 系统恢复流程

*创建日期：2026-03-29*
*最后更新：2026-03-29*

---

## 📋 恢复场景

### 场景 1: 树莓派完全故障（需要重新部署）

**前提条件**：
- 新的树莓派 5（8GB RAM + 128GB SSD）
- 已安装 Raspberry Pi OS（64 位）
- 网络连接正常
- GitHub 仓库访问权限

**恢复步骤**：

```bash
# 1. 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. 安装 OpenClaw
npm install -g openclaw

# 3. 克隆工作区仓库
cd /opt
git clone https://github.com/123z32/wanwan-skill.git .openclaw/workspace

# 4. 配置 OpenClaw
mkdir -p /openclaw_data/.openclaw
ln -s /opt/.openclaw/workspace /openclaw_data/.openclaw/workspace

# 5. 恢复配置文件
# 从 GitHub 仓库复制 config.json 到 /openclaw_data/config/

# 6. 启动 OpenClaw Gateway
openclaw gateway start

# 7. 验证状态
openclaw gateway status
```

---

### 场景 2: OpenClaw 配置丢失

**恢复步骤**：

```bash
# 1. 停止 Gateway
openclaw gateway stop

# 2. 从 Git 恢复配置
cd /openclaw_data/.openclaw/workspace
git pull origin master

# 3. 恢复配置文件到正确位置
cp /openclaw_data/.openclaw/workspace/config/config.json /openclaw_data/config/

# 4. 重启 Gateway
openclaw gateway start
```

---

### 场景 3: 工作区文件损坏

**恢复步骤**：

```bash
# 1. 备份当前状态（如果需要）
cd /openclaw_data/.openclaw/workspace
git status
git stash

# 2. 强制重置到最新提交
git fetch origin
git reset --hard origin/master

# 3. 清理未跟踪的文件
git clean -fd

# 4. 重启 Gateway
openclaw gateway restart
```

---

### 场景 4: 从特定备份标签恢复

**可用标签**：
```bash
git tag -l | sort
```

**恢复步骤**：

```bash
# 1. 查看标签列表
git tag -l | sort

# 2. 切换到指定标签
git checkout backup-YYYY-MM-DD

# 3. 或者创建新分支从标签恢复
git checkout -b restore-YYYY-MM-DD backup-YYYY-MM-DD

# 4. 重启 Gateway
openclaw gateway restart
```

---

## 🔧 关键配置项

### OpenClaw 配置位置
- **主配置**: `/openclaw_data/config/config.json`
- **工作区**: `/openclaw_data/.openclaw/workspace/`
- **日志**: `/openclaw_data/.openclaw/logs/`

### 必须恢复的文件
1. `config/config.json` - OpenClaw 主配置
2. `MEMORY.md` - 长期记忆
3. `memory/` - 日常日志
4. `skills/` - 自定义技能
5. `.learnings/` - 学习日志

---

## 📞 紧急联系

**GitHub 仓库**: https://github.com/123z32/wanwan-skill

**备份状态检查**：
```bash
cd /openclaw_data/.openclaw/workspace
git log --oneline -5
git tag -l | tail -3
```

---

## ✅ 恢复验证清单

恢复完成后执行：

- [ ] `openclaw gateway status` - Gateway 运行正常
- [ ] `git status` - 工作区干净
- [ ] 飞书连接测试 - 发送测试消息
- [ ] 技能加载检查 - `openclaw skills list`
- [ ] 内存文件检查 - `ls memory/`
- [ ] 配置文件检查 - `cat /openclaw_data/config/config.json`

---

## 📚 相关文档

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Docker 安装指南](https://docs.docker.com/get-docker/)
- [树莓派 OS 安装](https://www.raspberrypi.com/software/)

---

*此文档应打印或保存在独立位置，以便系统完全故障时参考*
