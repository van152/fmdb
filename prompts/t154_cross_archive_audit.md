# t154 — 22 语种语言库 × 772.8 万条生涯履历 × 主库跨库一致性质检

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 控制在 150 行以内**，分步构建脚本与落盘结果。
- 复用已有脚本（`t133_fm24_reader_v2`、`t138_people_pure_py`、`t143_lang_db`、`t127_pl_hist`、`t128_non_pl_hist`、`fm24_config`），避免重写解析器。
- **报告体积控制**：`REPORT.md` 与 JSON 只保存统计摘要、异常明细与代表性样本（严禁把几百万行全量 dump 进 Markdown）。

## 背景与目标
目前 13 个 `.dat` 档案均已单独闭合，`t142` 已完成 84 表内部外键图谱（检出 764 处官方悬空引用），但**跨档案联表一致性**尚未系统审计：
1. `lang_db_2400.dat` + `lang_update_db.dat`（704 成员、22 语种）与主库核心实体（Club / Nation / Comp / Stadium / City / People）的 UID 覆盖率与悬空译名统计（重点核查简中 `chinese_simplified`、繁中、英文）。
2. `pl_hist` / `non_pl_hist`（772.8 万条履历）中的 `person_uid`、`club_uid`、`comp_uid` 在 `people_db`、`table_3`、`table_25` 中的命中率与官方悬空引用清单。

## 交付物
1. `scripts/t154_cross_archive_audit.py`（使用 `import fm24_config`，支持 `--help`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/cross_archive_audit.json`（含 `"status": "complete"`、跨库覆盖率矩阵、悬空引用计数与 Top 样本）
3. `${OUTDIR}/REPORT.md`（精简可读，< 50 KB）与 `${OUTDIR}/DONE.md`（首行含 `DONE type=cross_archive_audit`）
