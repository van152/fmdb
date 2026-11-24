# t156 — 高频业务非主表 L3 字段语义闭合（8 张核心表）

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**，分步构建并测试。
- **限时收敛**：直接复用 `scratch/t150/out/remaining_tables_semantics.json`、`scratch/t121/out/wire_traces_79of79.json`、`scratch/t108/out/fourcc_mem_map_v2.json` 与 `scripts/t133_fm24_reader_v2.py` 做自动化 join 与 L2 实盘抽样核验，前 10 分钟摸清输入结构后立即编写 `scripts/t156_highfreq_tables_l3.py` 并落盘全部交付物。

## 背景与目标
对以下 **8 张高频核心业务非主表**完成 `slot19 wire offset <-> C++ object mem_off <-> 4CC getter/setter` 联合映射（可证则标 L3/L2，无法闭合的槽位诚实标为 `held`/`unnamed`，绝不编造），并用 `server_db.dat` / `client_db.dat` 真实样本验证：
1. `table_6` (`INJURY`, 115 行)
2. `table_22` (`STADIUM_CHANGE`, 449 行)
3. `table_26` (`COMP_HISTORY_RECORD`, 90,128 行)
4. `table_29` (`STARTING_LOAN`, 13,278 行)
5. `table_32` (`STARTING_FUTURE_TRANSFER`, 315 行)
6. `table_33` (`STARTING_CLUB_DEBT`, 32,409 行)
7. `table_49` (`STARTING_PERSON_HISTORY`, 792,149 行)
8. `table_71` (`STARTING_PAST_TRANSFER`, 616,665 行)

## 纪律与边界
- 路径统一通过 `import fm24_config` 读取（禁止硬编码 `D:\` 或 `Z:\`）。严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。

## 交付物
1. `scripts/t156_highfreq_tables_l3.py`（支持 `--help`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/highfreq_tables_l3.json`（含 `"status": "complete"` 或 `"partial"`、8 张表逐槽 L3/L2/held 映射与覆盖统计）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=highfreq_tables_l3`）
