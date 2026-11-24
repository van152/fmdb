# t148 — Comp 剩余 20 个缺口 + Comp 集合层业务语义闭合

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**，分步构建并测试。
- **限时收敛**：前 10 分钟快速读完 `remaining_gaps_v4.json`（仅 `entity=="comp"` 20 条）、`scratch/t66/out/collections.json` 与核心反编译文件，之后立即开始写 `scripts/t148_comp_gaps_collections.py` 并落盘全部 JSON / REPORT / DONE。

## 背景与目标
本任务双线收口 `comp`（table_25）：
1. **20 个剩余缺口**：`scratch/t136/out/remaining_gaps_v4.json` 中 `entity == "comp"` 的 20 条记录（`gap_helper_computed`: 12、`gap_delegated_or_empty`: 5、`gap_other_table_same_tag`: 3）。
2. **Comp 集合层业务语义**：`scratch/t66/out/collections.json` 已完成 `table_25` 7 个非空集合（`vec18`, `+0xe8`, `+0xc0`, `+0xc8`, `+0xd0`, `+0xd8`, `+0x100`）的物理文法 L3 闭合，请结合 `140ec0a60.c` / `140ecb5c0.c` 与 `table_25.dat` 样本（英超/欧冠/世界杯）补齐业务语义标注（能证则标 L3/L2，不能证诚实标 `held`）。

## 必读上下文与只读输入
- `AGENTS.md`、`scripts/fm24_config.py`
- `scratch/t136/out/remaining_gaps_v4.json`（`entity == "comp"` 20 条）
- `scratch/t66/out/collections.json`、`scratch/t66/out/REPORT.md`
- `scratch/t95/funcs/140ec0a60.c`、`140ecb5c0.c`、`140ed1440.c`、`140eb9000.c`
- `scratch/t108/out/fourcc_mem_map_v2.json`
- 路径统一通过 `import fm24_config` 读取（禁止硬编码 `D:\` 或 `Z:\`）。严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。

## 交付物
1. `scripts/t148_comp_gaps_collections.py`（`--help`、`--selftest` 全过，通过 `check_repo.py`）
2. `${OUTDIR}/comp_gaps_v5.json`（含 `"status": "complete"` 或 `"partial"`，20 条严格守恒）
3. `${OUTDIR}/comp_collections_semantic.json`（7 个集合语义映射 + L2/L3/held 证据）
4. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=comp_gaps_collections`）
