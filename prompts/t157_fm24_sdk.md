# t157 — FM24 全库统一纯 Python 读写 SDK & CLI（`scripts/t157_fm24_sdk.py`）

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**，分步构建并测试。
- 直接 `import` 复用现有模块（`fm24_config`、`t133_fm24_reader_v2`、`t138_people_pure_py`、`t140_fm24_roundtrip`、`t143_lang_db`、`t155_history_roundtrip`、`t152_warehouse_v2`），不要重写底层二进制解析器。

## 背景与目标
目前 13/13 官方 `.dat` 的纯 Python 读取、双向回写和 SQLite 查询能力分散在十几个 `tNN_*.py` 脚本中，外部用户难以一键调用。
你的目标是封装一个清晰、统一、生产级的顶层入口脚本 `scripts/t157_fm24_sdk.py`，提供：
1. `FM24Database` Python API 类（延迟加载，统一封装世界库 79 表、人物库 65.8 万行、6 个历史库、22 语种语言库、SQLite 数仓查询）；
2. 统一 CLI 子命令：`--help`、`inventory`（全库 13 档案健康体检）、`lookup <uid_or_name>`（跨库聚合查询，返回实体基本信息 + 中文译名 + 能力属性/履历）、`selftest`（全面自检所有子模块集成，退出码 0/1/2）。

## 纪律与边界
- 原始 `.dat` 只读；严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。
- 路径统一使用 `import fm24_config`，通过 `py -V:3.12 -B scripts/check_repo.py`。

## 交付物
1. `scripts/t157_fm24_sdk.py`（`--help`、`--selftest` 全过）
2. `${OUTDIR}/sdk_selftest_report.json`（含 `"status": "complete"`、各子系统连通性与实测样本输出）
3. `${OUTDIR}/REPORT.md`（含简洁的 API 与 CLI 使用示例）与 `${OUTDIR}/DONE.md`（首行含 `DONE type=fm24_sdk`）
