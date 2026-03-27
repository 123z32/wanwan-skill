# Feature Requests - 功能请求日志

记录用户请求的缺失功能和新能力。

## 条目格式

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要做什么

### User Context
为什么需要，解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何构建，可能扩展什么

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## 状态

- `pending` - 待处理
- `in_progress` - 正在进行中
- `implemented` - 已实现
- `wont_implement` - 决定不实现

## 实现条目

当功能实现后，更新条目：

1. 更改 `**Status**: pending` → `**Status**: implemented`
2. 添加 Implementation 块：

```markdown
### Implementation
- **Implemented**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: 简要描述实现方式
```

---

<!-- 在此追加新的功能请求条目 -->



