# t102 — 16 张核心实体表（AWARD / CITY / STADIUM / WEATHER 等）双端（server+client）L3 定稿

> 交付目录：`OUTDIR`（`scratch/t102/out`）
> 脚本路径：`scripts/t102_core_entities.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`、`scratch/data/server_db.dat`、`scratch/data/client_db.dat`、`scripts/t38_multiframe.py`。不要修改 `reports/` 或 `LEDGER.json`。

## 目标表清单（16 张核心独立实体表）
`tt = 0 (AWARD), 2 (CITY), 5 (CONTINENT), 6 (INJURY), 7 (MEDIA_SOURCE), 8 (LANGUAGE), 18 (DERBY), 19 (REGION), 21 (STADIUM), 22 (STADIUM_CHANGE), 23 (STAGE_NAME), 27 (WEATHER), 35 (PLAYER_TYPE), 41 (CURRENCY_RECORD), 47 (LOCAL_REGION), 56 (AGREEMENT)`。

## 任务要求
1. 利用 `scratch/t95/vtable_index.json` 与 `scratch/t95/funcs/*.c`，为每张表提取：
   - `server` 端 wire 顺序（来自 `slot19_read_server` + `hop1`）
   - `client` 端 wire 顺序（来自 `slot20_read_client` + `hop1`，若在 `client_db.dat` 中存在）
   - `4CC ↔ mem_off`（来自 `slot02_get_prop` / `slot03_set_prop`，例如 `WEATHER` 有 331 个 4CC、`STADIUM` 55 个、`AWARD` 48 个、`DERBY` 34 个）
   - Join 出每张表的 L3 完整字段表（带 `func_va` 和 C 行号）。
2. 在 `scripts/t102_core_entities.py` 中实现每张表的 server + client 解码器，对真实 `server_db.dat` 与 `client_db.dat` 逐行解码校验，检验能否精确闭合到末尾 9B footer！
3. **分块落盘原则**：每完成 4 张表覆写更新 `OUTDIR/core_entities_schemas.json`。

## 交付物（写入 `OUTDIR`）
1. `core_entities_schemas.json`：含 `"status": "complete"`，16 张表双端 L3 schema + 4CC 映射 + 真数据闭合校验。
2. `REPORT.md`：16 张表覆盖矩阵（server/client 行数、闭合率、4CC 映射率、与既有 `other_tables_schema.json` 对比）。
3. `DONE.md`：含 `DONE type=t102` 与核心统计数字。
