# t159 — Wave 15 增量回归矩阵与受保护路径守卫（`scripts/t159_wave15_regression.py`）

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**。

## 背景与目标
Wave 15 已陆续交付多个新脚本（`t149_edfx_upstream.py`、`t150_remaining_tables_semantics.py`、`t151_people_roundtrip.py`、`t152_warehouse_v2.py`、`t153_special_members_catalog.py`、`t154_cross_archive_audit.py`、`t155_history_roundtrip.py`、`t157_fm24_sdk.py`、`t158_l4_prep_kit.py`，以及后续将交付的 `t146`/`t147`/`t148`/`t156`/`t160`）。
在不修改既有 `scripts/t145_final_regression.py` 的前提下，编写 `scripts/t159_wave15_regression.py`：
1. 自动发现并运行 `scripts/t146_*.py` .. `scripts/t160_*.py` 中已就绪脚本（存在对应 `scratch/tNN/out/DONE.md` 或 `edfx_verdict.json`）的 `--help` 与 `--selftest`；
2. 联合执行 `scripts/check_repo.py` 与 `scripts/t145_final_regression.py --cached`；
3. 校验 `reports/` 与 `scratch/t01/LEDGER.json` 的 SHA-256 在回归前后保持逐字节不变；
4. 输出机读矩阵 `${OUTDIR}/wave15_regression_matrix.json`、`${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=wave15_regression`）。

## 交付物
1. `scripts/t159_wave15_regression.py`（使用 `import fm24_config`，支持 `--help`、`--selftest`、`--cached`，通过 `check_repo.py`）
2. `${OUTDIR}/wave15_regression_matrix.json`（含 `"status": "complete"`）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`
