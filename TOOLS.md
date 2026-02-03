# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## 🌐 Browser Automation - 首选 agent-browser

**遇到网页点击/交互问题时，优先使用 agent-browser skill！**

### 为什么？
- xdotool 坐标点击在 HiDPI/缩放显示器上经常失败（3024×1964 屏幕截图缩放到 2000×1299）
- agent-browser 用元素引用（@e1, @e2）而不是坐标，更可靠

### 快速参考
```bash
# 确保 PATH 包含 agent-browser
export PATH=~/.npm-global/bin:$PATH

# 核心工作流
agent-browser open <url>        # 打开页面
agent-browser snapshot -i       # 获取可交互元素列表（返回 @e1, @e2...）
agent-browser click @e21        # 点击指定元素
agent-browser fill @e2 "text"   # 填写输入框
agent-browser screenshot /tmp/x.png  # 截图

# 等待
agent-browser wait @e1          # 等待元素出现
agent-browser wait --text "Success"  # 等待文本出现
```

### 本地配置
- **安装位置**: `~/.npm-global/bin/agent-browser` (v0.8.7)
- **需要设置 PATH**: `export PATH=~/.npm-global/bin:$PATH`

### 什么时候用其他方法？
- 简单的 URL 导航 → 可以用 xdotool key ctrl+l 然后输入 URL
- 纯键盘操作 → keyboard-nav skill（Tab + Enter）
- agent-browser 无法连接时 → 回退到坐标点击（记得乘以 1.51 缩放系数）

---

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
