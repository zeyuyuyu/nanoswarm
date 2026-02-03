# MEMORY.md - 长期记忆

## 工具偏好

### 🌐 浏览器自动化
**遇到网页点击问题时，首选 agent-browser！**

原因：xdotool 坐标点击在 zeyu 的显示器上经常失败（HiDPI 缩放问题，3024×1964 → 2000×1299）。

解决方案：
1. **首选**: agent-browser（用 @e1 元素引用，不用坐标）
2. **备选**: keyboard-nav skill（Tab + Enter）
3. **最后**: xdotool 坐标（记得 ×1.51 缩放系数）

```bash
export PATH=~/.npm-global/bin:$PATH
agent-browser snapshot -i    # 获取元素引用
agent-browser click @e21     # 点击
```

---

## 关于 Zeyu

- UCLA 学生
- 有 ICML 2026 论文投稿（VSA-LLM, Beyond Scaling, HADR）
- OpenReview 账号: zeyuwang@ucla.edu

---

## 重要事件

### 2026-02-03
- 成功提交 ICML 2026 论文排名（VSA-LLM > Beyond Scaling > HADR）
- 学到了 agent-browser 比 xdotool 坐标点击更可靠
