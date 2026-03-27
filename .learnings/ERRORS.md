# Errors - 错误日志

记录命令失败、异常和意外行为。

## 条目格式

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
失败的简要描述

### Error
```
实际错误消息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 相关的环境详情

### Suggested Fix
如果可以识别，什么可能解决这个问题

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (如果重复出现)

---
```

## 状态

- `pending` - 待处理
- `in_progress` - 正在进行中
- `resolved` - 已解决
- `wont_fix` - 决定不解决

## 解决条目

当问题修复后，更新条目：

1. 更改 `**Status**: pending` → `**Status**: resolved`
2. 添加 Resolution 块：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: 简要描述做了什么
```

---

<!-- 在此追加新的错误条目 -->



