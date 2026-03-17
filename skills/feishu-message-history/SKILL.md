---
name: feishu-message-history
description: |
  Read Feishu chat message history. Activate when user asks to read chat history, 
  view past messages, or search conversation history in Feishu.
---

# Feishu Message History Tool

This skill provides tools to read Feishu chat message history using the `feishu_chat` tool.

## Prerequisites

1. **Feishu Open Platform Permissions**: The app must have the following permissions:
   - `im:message` - Read message content
   - `im:chat` - Access chat information

2. **Configuration**: Feishu channel must be enabled in OpenClaw config.

## Tools

### `feishu_chat` (history action)

Read messages from a Feishu chat.

#### Parameters

```json
{
  "action": "history",
  "chat_id": "oc_xxx or chat_id",
  "page_size": 50,
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-02T00:00:00Z",
  "sort_type": "ByCreateTimeDesc"
}
```

- `action`: `"history"` - List messages in a chat
- `chat_id`: Chat ID (from inbound metadata or chat info)
- `page_size`: Number of messages to retrieve (1-100, default 50)
- `start_time`: Optional ISO 8601 timestamp - only return messages after this time
- `end_time`: Optional ISO 8601 timestamp - only return messages before this time
- `sort_type`: Optional - `"ByCreateTimeAsc"` or `"ByCreateTimeDesc"` (default)

#### Response

```json
{
  "chat_id": "oc_xxx",
  "has_more": true,
  "page_token": "xxx",
  "messages": [
    {
      "message_id": "om_xxx",
      "root_id": "om_xxx",
      "parent_id": "om_xxx",
      "thread_id": "om_xxx",
      "chat_type": "p2p",
      "msg_type": "text",
      "content": "{\"text\":\"Message text\"}",
      "sender_id": "ou_xxx",
      "sender_type": "user",
      "create_time": "2024-01-01T12:00:00Z",
      "update_time": "2024-01-01T12:00:00Z",
      "deleted": false
    }
  ]
}
```

## Usage Example

Get last 20 messages from current chat:

```json
{
  "action": "history",
  "chat_id": "oc_d77a50191711fcda0c3fab1a2d0e910c",
  "page_size": 20
}
```

Get messages from a specific time range:

```json
{
  "action": "history",
  "chat_id": "oc_d77a50191711fcda0c3fab1a2d0e910c",
  "page_size": 50,
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-02T00:00:00Z",
  "sort_type": "ByCreateTimeAsc"
}
```

**Note:** For direct chats, the `chat_id` format is `oc_xxx` (not `user:ou_xxx`). You can get the chat_id from:
- Inbound message metadata (`chat_id` field)
- Using `feishu_chat` with action `info` 
- From a known message using `im.message.get` API

## Notes

- For direct chats, use the `chat_id` from inbound metadata (format: `user:ou_xxx`)
- For group chats, you may need to get the chat_id first using `feishu_chat` tool with action `info`
- Message content is returned as JSON string - parse it to get the actual text
- Use `page_token` from response to fetch more messages when `has_more` is true
- Content format depends on `msg_type`:
  - `text`: `{"text": "message content"}`
  - `post`: Rich text content
  - `image`, `file`, etc.: Media metadata
