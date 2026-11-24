# t161 — Wave 15 总成果汇总与台账候选生成器（`scripts/t161_wave15_summary.py`）

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**。

## 背景与目标
Wave 15（`t146`–`t160`）已经陆续产出一批重要成果（`t149` EDfx 终局闭合、`t150` 其余 62 张非主表目录、`t151` `people_db` 全量无损双向回写、`t152` SQLite 数仓 v2、`t153` 16 个特殊成员目录、`t154` 跨档案一致性质检、`t155` 6 个历史档案位级双向回写、`t157` 统一纯 Python SDK、`t158` L4 真机验证预备包，以及进行中的 `t146`/`t147`/`t148`/`t156`/`t159`/`t160`）。
编写 `scripts/t161_wave15_summary.py`：
1. 自动扫描 `scripts/t146_*.py` .. `scripts/t160_*.py` 与 `scratch/t146/out` .. `scratch/t160/out`，汇总每项任务的状态（complete/negative/partial/in_progress）、关键量化指标、产物路径与 SHA-256；
2. 生成供指挥官审阅的台账候选条目（格式兼容 `scratch/t01/LEDGER.json`，但**绝不写入** `scratch/t01/LEDGER.json`，仅输出到 `${OUTDIR}/ledger_candidates_wave15.json`）；
3. 生成简洁清晰的中文总览报告 `${OUTDIR}/WAVE15_SUMMARY.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=wave15_summary`）。

## 交付物
1. `scripts/t161_wave15_summary.py`（使用 `import fm24_config`，支持 `--help`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/wave15_summary.json`、`ledger_candidates_wave15.json`、`WAVE15_SUMMARY.md`、`DONE.md`
