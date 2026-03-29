# Learnings - 学习日志

记录纠正、知识缺口和最佳实践。

## 条目格式

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一行描述学到了什么

### Details
完整上下文：发生了什么，什么是错的，什么是正确的

### Suggested Action
具体的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (如果与已有条目相关)
- Pattern-Key: simplify.dead_code | harden.input_validation (可选)
- Recurrence-Count: 1 (可选)
- First-Seen: 2025-01-15 (可选)
- Last-Seen: 2025-01-15 (可选)

---
```

## 类别

- `correction` - 用户纠正或自我纠正
- `knowledge_gap` - 发现知识过时或缺失
- `best_practice` - 发现更好的方法
- `workflow` - 工作流改进
- `tool_gotcha` - 工具使用陷阱

## 优先级

- `critical` - 阻塞核心功能、数据丢失风险、安全问题
- `high` - 重大影响、影响常见工作流、重复问题
- `medium` - 中等影响、存在变通方法
- `low` - 小不便、边缘情况、锦上添花

---

## [LRN-20260328-001] openclaw-timeout-config

**Logged**: 2026-03-28T15:26:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
OpenClaw 超时配置的正确位置和字段名

### Details
- ❌ 错误：`gateway.timeouts.request/connect/idle` (不存在)
- ❌ 错误：`providers.<name>.timeout` (不存在)
- ✅ 正确：`agents.defaults.timeoutSeconds` (Agent 执行超时)
- ✅ 正确：`tools.exec.timeoutSec` (exec 命令超时)
- ✅ 正确：`env.shellEnv.timeoutMs` (Shell 环境超时)

### Suggested Action
修改超时配置时只使用文档中确认的字段

### Metadata
- Source: error
- Related Files: /openclaw_data/config/config.json
- Tags: timeout, config, openclaw
- Pattern-Key: config.from.docs

---

## [LRN-20260328-002] heartbeat-setup

**Logged**: 2026-03-28T15:43:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: config

### Summary
OpenClaw 心跳机制配置方法

### Details
- 心跳配置在 `agents.defaults.heartbeat`
- 关键配置项：
  - `every`: 间隔 (如 "1h", "30m")
  - `target`: 发送渠道 (如 "feishu")
  - `to`: 接收人 ID
  - `activeHours`: 活跃时间段
  - `prompt`: 心跳提示词
- 正常回复 `HEARTBEAT_OK` 不发送消息
- 有异常时才发送警报

### Suggested Action
心跳机制已配置完成，运行正常

### Metadata
- Source: conversation
- Related Files: /openclaw_data/config/config.json, HEARTBEAT.md
- Tags: heartbeat, automation, monitoring
- Pattern-Key: heartbeat.monitoring

---

<!-- 在此追加新的学习条目 -->



