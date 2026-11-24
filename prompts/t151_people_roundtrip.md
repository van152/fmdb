# t151 — `people_db.dat` 通用双向无损回写引擎 + `editor.exe` 仿真验收

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**严禁在单次 `write`/`edit` 中一次写出超过 150 行代码**。
- 请务必**直接 `import` 复用**现有模块（`t138_people_pure_py`、`t140_fm24_roundtrip`、`t126_player_attributes_l3`、`t137d_manager_cards_full`、`fm24_config`），先写精简骨架再分步 `edit` 追加编码器、修改 API 与 Unicorn 回读验收。

## 背景与目标
`scripts/t140_fm24_roundtrip.py` 已实现 `server_db` / `client_db` 79/79 编号表的全量 bit-exact 重编码与定向修改，但对 `people_db.dat` 仅实现了哈里·凯恩单人的定点修补。
你的目标是编写 `scripts/t151_people_roundtrip.py`：
1. **全量无损重编码（信息守恒）**：纯 Python 解析 `people_db.dat` 全部 658,011 行后，逐行无损重新拼装/编码，重编码 payload 的 SHA-256 与官方原盘 100.0% 一致（`diff == 0`）。
2. **通用字段修改 API**：支持按 UID 修改任意球员的 54 项属性与 CA/PA、任意教练/非球员的 34 项执教属性与 CA/PA、以及至少 1 项变长字段，并重打包为合法 `.dat`。
3. **双路回读验收**：用纯 Python 解码器 + Unicorn 仿真官方 `editor.exe` 机器码双路回读修改后的记录（至少覆盖 1 名球星 + 1 名名帅），证实修改值在官方 C++ 对象内存中准确落盘。

## 必读上下文与只读输入
- `AGENTS.md`、`scripts/fm24_config.py`
- `scripts/t138_people_pure_py.py`、`scripts/t140_fm24_roundtrip.py`
- `scripts/t126_player_attributes_l3.py`、`scripts/t137d_manager_cards_full.py`
- 路径统一通过 `import fm24_config` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 交付物
1. `scripts/t151_people_roundtrip.py`（支持 `--help`、`--selftest`、`--full`，通过 `check_repo.py`）
2. `${OUTDIR}/people_roundtrip_report.json`（含 `"status": "complete"`、全量 SHA-256 比对、修改前后双路回读结果、耗时）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=people_roundtrip`）
