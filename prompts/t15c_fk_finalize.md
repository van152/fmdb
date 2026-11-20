# t15c 任务书:FK 交叉收尾 —— 把已有扫描件汇总成交付物(不重跑)

先读 [AGENTS.md](../AGENTS.md)。你是 t15 的收尾接力:前一轮 devseek 三次尝试都倒在最后汇总一步(超时/上游断流),但**数据工作基本做完了**。你的活是把现场收拢成正式交付。

## 现场清单(全部已存在,只读)

`scratch/t15/out/` 里有:
- 列画像:`scan_t26.json` `scan_t29.json` `scan_t30.json` `scan_t38.json` `scan_t39.json` `scan_t49.json` `prof_t32.json` `prof_t36.json` `prof_t45.json` `prof_t48.json`
- 深挖:`walk_t45.json` `walk_t48.json` `people_probe.json` `more.json` `t45_cols.csv` `t48_cols.csv`
- 以及若干 .npy(person_id/person_uid 等,二进制中间产物,不用管)

对照任务书原文在 `prompts/t15_fk_cross.md`(判断标准在那里:corroborates/contradicts、C 类边界、E42 值域法限制)。

## 任务

1. 逐个读入上述 json,合并成 `fk.json`:
   - 顶层 `{"status":"...","tables":[{"table_type":N,"rtti_class":"...","fk_verdict":"corroborates|contradicts|inconclusive","key_evidence":"一句话+数字","sentinel":"...","id_space":"..."}],"people_diff":{...}}`
   - **判断只用已有数字**,缺数字的表标 `inconclusive` 并写缺什么——不许为了好看编造或重跑 dump。
2. `fk.md`:人读版,逐表 3-5 行。
3. `people_diff.md`:658,011 vs 792,149 悬案,把 people_probe.json / person_ids 相关数字组织成"可检验结论 + 假设"两节。注意 E59 教训:**basic_people_db 的 658,011 是独立档案的行数,不是从 t49 数出来的,所以这个对照不循环**;但若你的推理需要 t49 自己的行数当基数,明确标注。
4. 若某个 scan json 明显残缺(比如只有 2 列),如实降级为 inconclusive。

## 纪律

- 只写 `scratch/t15/out/` 下的 `fk.json` `fk.md` `people_diff.md` 三个文件(不覆盖已有 scan/prof/walk 文件)。
- 不重跑任何 dump;不碰 scripts/;不联网。
- 输出预算:单次工具写盘 ≤300 行;fk.json 预计 <40KB,超了就分片。
- 12 分钟内完不成就把已合成的部分落盘标 `"status":"partial"`。

## 交付

只那三个文件。顶层 status 用 `complete_finalized` 或 `partial`。
