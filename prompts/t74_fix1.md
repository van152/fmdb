# t74-fix1 — 恢复与分块交付(deepseek;接 t74 会话)

上一轮卡点(已诊断):反复撞 40 分钟超时墙(rc=124),每次 resume 重读上下文烧掉大半时间窗,`scratch/t74/out/` 仍是空的。你会话里已经积累的行框分析(media server fitcount 全中 208 行、stadium/team/award 等探针结果)都在上文,**别重探,立即落盘**。

## 恢复纪律(必须严格执行)

1. **任何文件写单次 ≤120 行**;大文件拆多次写/bash heredoc 追加;禁止单次写几百行。
2. **第一步就是写盘**:把会话里已闭合的 (archive,table) 行框立即写进 `scratch/t74/out/frames.json`(先骨架后追加;闭不了的表写 `"escalate_to_sol"` 条目)。这一步在本次 turn 的前 5 分钟内完成,不许再做新探针。
3. 然后:`row_widths_{table}.csv`(只写直方图摘要,别逐行 8 万行)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t74 status=partial` 或 `complete`)。builder `scripts/t74_row_frames9.py` 最后写,写不下就拆两个文件。
4. **交付优先于完美**:partial 也收;team(24) 闭不了就 escalate,其余 8 表照常交付。
5. 其余口径(自证 identity 宽度、锚点回归、负结果保留)沿用 `prompts/t74_row_frames9.md` 原文。
