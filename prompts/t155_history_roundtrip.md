# t155 — 6 个生涯历史档案（`pl_hist_*` + `non_pl_hist_*`）位级双向无损回写引擎

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**严禁在单次 `write`/`edit` 中一次写出超过 150 行代码**。
- 请直接 `import` 复用现有模块（`t127_pl_hist`、`t128_non_pl_hist`、`fm24_config`），先写精简骨架再分步 `edit` 追加编码器与自检。

## 背景与目标
目前 `server_db` / `client_db` 79 张编号表（`t140`）和 `lang_db`（`t143`）均已完成双向无损回写验证，`people_db` 正在由 `t151` 补齐；而 6 个生涯历史档案（`pl_hist_{index,id,dt}.dat`、`non_pl_hist_{index,id,dt}.dat`，共 772.8 万条履历、67,333 个 4KB 块）目前仅有只读解码器（`t127`/`t128`）。
你的目标是编写 `scripts/t155_history_roundtrip.py`：
1. **信息守恒（Bit-exact 重编码）**：纯 Python 解析全部 6 个历史档案的索引、ID 表与分块数据区，再重新编码打包，验证重编码后的 `index`/`id` 与解压块流与原盘逐字节一致（`SHA-256 == orig` 或 100% 块级无损）。
2. **定向外科手术修改与回读**：支持修改指定球星（如梅西/凯恩）的某条赛季出场/进球记录，以及指定名帅（如瓜迪奥拉）的某条执教记录，重编码写入 `${OUTDIR}` 临时 `.dat` 文件，并用纯 Python 解码器回读验证修改精确生效、其余 772 万+ 条记录零错位。

## 必读上下文与只读输入
- `AGENTS.md`、`scripts/fm24_config.py`
- `scripts/t127_pl_hist.py`、`scripts/t128_non_pl_hist.py`
- 原始 `.dat` 一律只读，输出全部落盘到 `${OUTDIR}`。严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。

## 交付物
1. `scripts/t155_history_roundtrip.py`（使用 `import fm24_config`，支持 `--help`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/history_roundtrip_report.json`（含 `"status": "complete"`、6 档案无损核验结果、球星/名帅修改前后回读对比与耗时）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=history_roundtrip`）
