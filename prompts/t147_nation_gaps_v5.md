# t147 — Nation 剩余 26 个缺口深挖收口（Big-3 v5 / Nation 线）

## 背景与目标
`scratch/t136/out/remaining_gaps_v4.json` 中 `entity == "nation"` 仍有 **26 个未闭合缺口**（`gap_off_not_in_read_stream`: 15、`gap_helper_computed`: 9、`gap_other_table_same_tag`: 1、`gap_child_off_not_in_child_stream`: 1），使 nation 净覆盖停在 186/212 = 87.7%。
你的目标是逐条深挖这 26 个 nation occurrence，补齐 `table_9` / `table_10` / `table_extra_9` / `lang_db` / 子表链路，将可证项升至 L3 或确证排除，剩余项写明精确阻断点。

## 必读上下文与只读输入
- `AGENTS.md`、`docs/REPO_STATUS.md`
- `scratch/t136/out/remaining_gaps_v4.json`（只取 `entity == "nation"` 的 26 条）
- `scratch/t136/out/REPORT.md`、`scratch/t136/out/hop_audit_v4.json`
- `scripts/t136_big3_final_closure.py`、`scripts/t143_lang_db.py`
- `scratch/t95/funcs/*.c`、`scratch/t124/out/funcs/*.c`、`scratch/t132/out/funcs/*.c`
- `scratch/t108/out/fourcc_mem_map_v2.json`
- 路径统一通过 `scripts/fm24_config.py` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 方法要求
1. 严格遵守证据分级（L1/L2/L3/L4），特别注意 `table_9`（NTC）与 `table_10`（NATION）及 `table_extra_9` 的 receiver 边界，不得混用偏移空间。
2. 对 `Nnam`/`Nsnm`/`N3ln` 等名称字段核实其在 `table_extra_9` 或 `lang_db` 的精确持久化来源；对 `TCht`、阵型枚举、`NCro` 等历史保留项做诚实复验。
3. 严禁修改 `reports/` 与 `scratch/t01/LEDGER.json`，严禁修改既有脚本。
4. 新脚本必须使用 `import fm24_config`，支持 `--help` 和 `--selftest`（退出码 0/1/2），并通过 `py -V:3.12 -B scripts/check_repo.py`。

## 交付物
1. `scripts/t147_nation_gaps_v5.py`（可执行、`--help`、`--selftest` 全过）
2. `${OUTDIR}/nation_gaps_v5.json`（含 `"status": "complete"` 或 `"partial"`、26 条逐条裁决、守恒统计）
3. `${OUTDIR}/REPORT.md`
4. `${OUTDIR}/DONE.md`（首行含 `DONE type=nation_gaps_v5`）
