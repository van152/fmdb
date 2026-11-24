# t160 — 语言库（`lang_db_2400.dat` + `lang_update_db.dat`）双向修改重打包引擎

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**。
- 直接 `import` 复用 `scripts/t143_lang_db.py` 与 `scripts/fm24_config.py`，不要重写底层 FMF/Zstd 容器解析。

## 背景与目标
目前 `server_db`/`client_db`（`t140`）、`people_db`（`t151`）、6 个历史档案（`t155`）均已完成双向修改与重打包验证。本任务补齐最后一块拼图——**22 语种语言库双向修改回写引擎** `scripts/t160_lang_roundtrip.py`：
1. 验证 `lang_db_2400.dat` 与 `lang_update_db.dat` 核心中文/英文成员的无损解包与重编码（解压字节流 `diff == 0`）；
2. 实现通用译名修补 API：按 `(language_id, entity_table, dbid)` 修改本地化译名（支持**变长 UTF-8 字符串**修改，例如修改简体中文里“英超”与“利物浦”译名），重编码并重打包输出到 `${OUTDIR}` 临时 `.dat`；
3. 用 `t143_lang_db` 解码器回读修改后的 `.dat`，证实目标词条精确生效、同成员其余数万条词条零错位。

## 纪律与边界
- 原始 `.dat` 只读；严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。
- 路径统一使用 `import fm24_config`，通过 `check_repo.py`。

## 交付物
1. `scripts/t160_lang_roundtrip.py`（支持 `--help`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/lang_roundtrip_report.json`（含 `"status": "complete"`、成员无损校验、变长译名修改前后回读对比）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=lang_roundtrip`）
