# 🚀 Ubuntu Desktop → Server 迁移指南

**目标**: 从 Ubuntu Desktop 24.04 迁移到 Ubuntu Server 24.04，释放 ~1GB 内存

---

## 📋 迁移清单

### 阶段 1：备份（当前系统）⏱️ 15 分钟

- [ ] 运行备份脚本 `./backup-all.sh`
- [ ] 验证备份文件完整性
- [ ] 记录网络配置
- [ ] 记录 OpenClaw 配置
- [ ] 备份到外部存储（可选）

### 阶段 2：准备安装介质 ⏱️ 20 分钟

- [ ] 下载 Ubuntu Server 24.04 LTS for Raspberry Pi
- [ ] 准备 SD 卡（建议 32GB+）
- [ ] 使用 Raspberry Pi Imager 刷写
- [ ] 配置首次启动参数（SSH、WiFi）

### 阶段 3：安装系统 ⏱️ 30 分钟

- [ ] 启动树莓派（自动安装）
- [ ] 等待安装完成
- [ ] 首次登录（SSH）
- [ ] 更新系统 `sudo apt update && sudo apt upgrade -y`

### 阶段 4：恢复数据 ⏱️ 30 分钟

- [ ] 安装必要的工具（git, nodejs, docker 等）
- [ ] 恢复备份文件
- [ ] 恢复 OpenClaw 配置
- [ ] 恢复 RAG 知识库

### 阶段 5：配置服务 ⏱️ 30 分钟

- [ ] 配置 OpenClaw Gateway
- [ ] 配置 RAG 服务
- [ ] 配置心跳监控
- [ ] 配置 crontab

### 阶段 6：测试验证 ⏱️ 15 分钟

- [ ] 测试 OpenClaw 基础功能
- [ ] 测试飞书消息收发
- [ ] 测试 RAG 系统
- [ ] 测试心跳监控
- [ ] 验证内存使用

---

## 📁 文件清单

```
migrate-to-server/
├── README.md                  # 本文件
├── backup-all.sh              # 备份脚本
├── restore-all.sh             # 恢复脚本
├── pre-migration-check.sh     # 迁移前检查
├── post-migration-check.sh    # 迁移后检查
├── install-dependencies.sh    # 依赖安装脚本
└── config-templates/          # 配置模板
    ├── config.json.example
    └── crontab.example
```

---

## ⚠️ 注意事项

### 数据风险
- ⚠️ **务必备份到外部存储**（SD 卡可能损坏）
- ⚠️ 记录所有自定义配置
- ⚠️ 保留原 SD 卡至少 1 周（以防万一）

### 网络配置
- 记录当前 IP 地址、网关、DNS
- 如果是静态 IP，准备新配置
- 确保知道路由器管理员密码

### 服务配置
- OpenClaw Gateway 端口：18789
- RAG 服务端口：9900
- SSH 端口：22

---

## 🆘 紧急联系

如果迁移过程中遇到问题：
1. 保留原 SD 卡（可随时回退）
2. 检查日志文件
3. 重启服务或系统
4. 必要时回退到原系统

---

## 📊 预期结果

### 迁移前（Desktop）
```
总内存：7.7GB
已使用：4.1GB (53%)
可用：3.7GB
```

### 迁移后（Server）
```
总内存：7.7GB
已使用：2.8GB (36%)
可用：5.0GB
节省：~1.3GB ✅
```

---

## ✅ 完成标准

- [ ] 系统正常启动
- [ ] SSH 可连接
- [ ] OpenClaw 正常运行
- [ ] 飞书消息正常收发
- [ ] RAG 系统正常响应
- [ ] 内存使用 < 3GB
- [ ] 心跳监控正常运行

---

*最后更新：2026-03-25*
