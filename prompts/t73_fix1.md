# t73-fix1 — 恢复与分块交付(deepseek;接 t73 会话)

上一轮卡点(已诊断):**单次 `write` 工具调用超出输出 token 上限被截断**,turn 结束时 builder 没写成,`scratch/t73/out/` 仍是空的。你之前已收集的四表事实(city 行框列 `["ordinal","body_start","selector","end","N","M","uid"]`、continent/region/currency 探针结果)都在会话上文里,别重探,直接落盘。

## 恢复纪律(必须严格执行)

1. **任何文件写单次 ≤120 行**。大文件拆多次:先写骨架,再用后续 write/append(bash heredoc 追加)补全;禁止一次写几百行的文件。
2. **先落盘,后完善**。顺序:
   a. `scratch/t73/out/frames.json` —— 把已能闭合的 (archive,table) 行框立即写入(闭不了的写 `escalate_to_sol` 条目);
   b. 每表 `slots_{archive}_{table}.json` —— 已算出的槽位值域/字段候选先写,哪怕部分表只有 identity+少量槽;
   c. `verify.py` + `REPORT.md` + `DONE.md`(首行 `DONE type=t73 status=partial` 或 `complete`);
   d. builder `scripts/t73_table_slot_mapper.py` 若一次写不下,拆成 `t73_mapper_core.py` + `t73_table_slot_mapper.py`(CLI 壳)两个文件,都遵守 `scripts/t73_*.py` 防冲突纪律。
3. **交付优先于完美**:宁可交付 partial(4 表里闭出 2–3 张也收),不留空 out。
4. 其余口径(分级/锚点回归/escalate/负结果保留)沿用 `prompts/t73_slot_mapper.md` 原文。
