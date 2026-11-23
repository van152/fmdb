# t108b — 补齐 `t108_extract_4cc_v2.py` 的 `attach_v2_extras` 落盘与 `--selftest` 23/23 全绿

> 脚本：`scripts/t108_extract_4cc_v2.py`
> 输出：`OUTDIR`（`scratch/t108/out2`）
> 不要修改 `reports/`、`LEDGER.json` 或 `scripts/t97_extract_4cc_mem.py`。

## 背景（已有 95% 完成）
`scripts/t108_extract_4cc_v2.py` 已经完成核心逻辑（`member_resolved=1517`, `dispatch_resolved=805`, 18/18 回归 `exact=15, within_slot=3, mismatch=0`, 静态 read 交叉 `802 -> 1471`），只差最后 3 处收尾：
1. 在 `build_v2` 调用 `T97.build(...)` 之后，补上 `attach_v2_extras(fmap)`：把 `_INFO_BY_BRANCH[(int(cand["func_va"], 16), cand["line_no"])]["_extra"]` 里的 `offset_space`, `helper_chain`, `child`, `subobj_path`, `inner_off`, `primary_role`, `roles`, `helper_member_offsets`, `computed_reasons`, `helper_resolutions`, `primary_line` 回填到每个候选（含 `alt`）上，使 `fourcc_mem_map_v2.json` 和 `xml_triage_v2.json` 里真实呈现出 `child_table_resolved > 0`（~805）与 `helper_inline_resolutions_in_map > 0`（~1517）。
2. 修复 `--selftest` 中两处笔误：
   - `totals.get("mismatch", 0) == 0`（当前因 `mismatch` 键缺省为 `None` 导致断言失败，实际已是 0 mismatch！）
   - `triage row Cnti -> 0xd8`（当前写成了大小写错误的 `CNti`）。
3. 重跑 `py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --selftest`（须全绿退出 0）和 `--run --out scratch/t108/out2`（同时更新 `scratch/t108/out`），删除任何临时脚本（如 `scratch/t108/_wr_tmp.py`），并把最终 `REPORT.md` 和 `DONE.md`（含 `DONE type=t108b`）落盘到 `scratch/t108/out2`。
