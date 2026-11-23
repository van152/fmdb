# t109c — 收尾 `scripts/t109_big3_l3_join.py`（解决 33 条对账冲突并落盘 `REPORT.md` + `DONE.md`）

> 交付目录：`OUTDIR`（`scratch/t109/out`）
> 已有脚本：`scripts/t109_big3_l3_join.py`（已过 `--selftest`，退出 0；三大主表 1,034 分母守恒：`L3_static_closed=82`, `L3_subtable_routed=274` → 总覆盖 356/1,034 = **34.4%**，净持久化覆盖 356/653 = **54.5%**）
> 不要修改 `reports/` 或 `LEDGER.json`。

## 待收尾的 3 件小事（基于已有代码直接续作，不要重写）
1. **核对并修/解释 `coverage_summary.json` 里那 33 条与既有 L3 的对账冲突**：
   - 重点修正 `comp` 的 ~21 条 `Pcs*`/`Pcj*`（既有 L3 偏移 393–414）被误分进 `excluded_non_db_l3` 的 bug（检查为何误判，至少标为真实持久化或子对象路由，不得把已验收持久化字段判为 non-db！）。
   - 修复 `club/comp` 的 `duni` 跨表误归属到 `table_1/BASIC_PERSON` 的问题（`duni` 是 `DATABASE_OBJECT` 共享基类 identity 偏移 `0x8..0x13`）。
   - 对剩余无法单靠静态闭合的少数条（如 `comp cbcl@292`/`ctcl@296`、`Cesd/Ceed/Cead/CteA/Chaf/Cmtp`）逐条写入清晰 `reason`。
2. **重跑 `scripts/t109_big3_l3_join.py --selftest`（须退出 0）和主生成命令**，确认 `big3_l3_join.json`、`coverage_summary.json`、`remaining_gaps.json` 均为 `"status": "complete"` 且 1,034 条分母严格守恒（club 433 + nation 346 + comp 255 = 1,034）。
3. **落盘 `scratch/t109/out/REPORT.md` 和 `scratch/t109/out/DONE.md`（含 `DONE type=t109c`）**，打印完整交付清单与核心统计（原 10.6% vs 新总覆盖率与净持久化覆盖率）。
