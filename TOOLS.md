# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Infrastructure

- **树莓派 5** (惠州): 8GB RAM + 128GB SSD, hosts OpenClaw container
- **AGX Thor** (深圳): 128GB VRAM（目前未使用）
- **Runtime**: Agent runs in Docker container for isolation
- **Model**: Qwen3.5-Plus (云端 API)

### Location

- **定位工具**: `/openclaw_data/.openclaw/workspace/scripts/locate.sh`
- **定位方式**: IP 定位（ip-api.com，免费无需 API key）
- **网络接口**: wlan0 (WiFi), eth0 (有线), tailscale0 (VPN)
- **默认位置**: 惠州（出差）/ 深圳光明区（工作）
