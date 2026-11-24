# t152 — SQLite 数仓 v2（集成教练 34 属性、中文译名、生涯履历与统一查询 CLI）

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**严禁在单次 `write` 中一次写出超过 150 行代码**。
- 请务必**直接 `import` 复用**现有模块（`t139_fm24_db_cli`、`t137d_manager_cards_full`、`t143_lang_db`、`t127_pl_hist`、`t128_non_pl_hist`、`fm24_config`），先写精简骨架再分步 `edit` 追加子命令与自检，不要重复造解析轮子。

## 背景与目标
`scripts/t139_fm24_db_cli.py` 构建了 SQLite 数仓，覆盖 24 张核心表与球员 54 项属性。
本任务在不改动 `t139_fm24_db_cli.py` 的前提下，编写精简高效的 `scripts/t152_warehouse_v2.py`，基于已有模块或既有 SQLite/产物构建增强版数仓 `${OUTDIR}/fm24_warehouse_v2.sqlite`（增量表：`manager_attributes`、`lang_zh_cn`、`career_history_summary`），并提供毫秒级双语查询 CLI。

## 必读上下文与只读输入
- `AGENTS.md`、`scripts/fm24_config.py`
- `scripts/t139_fm24_db_cli.py`、`scripts/t137d_manager_cards_full.py`
- `scripts/t143_lang_db.py`、`scripts/t127_pl_hist.py`、`scripts/t128_non_pl_hist.py`
- 路径统一通过 `import fm24_config` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 交付物
1. `scripts/t152_warehouse_v2.py`（支持 `--help`、`--build`、`--query`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/warehouse_v2_benchmark.json`（含 `"status": "complete"`、表清单、行数、体积、典型查询耗时与校验样本）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=warehouse_v2`）
