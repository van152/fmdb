# t101 — `STARTING_*` 子表批次 2（tt 49..73，共 20 张表）Hex-Rays 线协议与 L3 字段定稿

> 交付目录：`OUTDIR`（`scratch/t101/out`）
> 脚本路径：`scripts/t101_starting_batch2.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`、`scratch/data/server_db.dat`、`scripts/t38_multiframe.py`。不要修改 `reports/` 或 `LEDGER.json`。

## 目标表清单（20 张，不含 t98 的 tt=48 和 t102 的 tt=56）
`tt = 49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73`（注：52 和 57 在 server_db 中为 0 行，仍须从 Hex-Rays 给出 L3 schema；65/67/68/69 共享 `0x141884ca8` vtable，一并核实！）。

## 任务要求
对这 21 张表逐一：
1. 精读 `scratch/t95/funcs/*.c` 中对应的 `slot19_read_server`（含 `hop1`）C 伪代码，提取精确 wire 顺序与 `this+0xNN` 偏移（带 C 文件行号）。
2. 精读 `slot02_get_prop` / `slot03_set_prop`，将 `4CC ↔ mem_off ↔ wire_idx` 串联成严格 L3 schema。
3. 在 `scripts/t101_starting_batch2.py` 中实现每张表的二进制解码器，跑 `server_db/table_<N>.dat` 验证（≤50,000 行全量校验到 9B footer；>50,000 行如 `table_49` 792,149 行 / `table_71` 616,665 行须跑全表或明确记录行长统计与闭合状态，确保高性能）。
4. **分块落盘原则**：每完成 5 张表更新 `OUTDIR/batch2_schemas.json`。

## 交付物（写入 `OUTDIR`）
1. `batch2_schemas.json`：含 `"status": "complete"`，全部目标表 L3 wire schema、4CC 映射与实数校验结果。
2. `REPORT.md`：汇总表与关键发现（如 `65/67/68/69` 共享结构、`table_71` 57MB / `table_49` 28MB 解码验证）。
3. `DONE.md`：含 `DONE type=t101` 与核心统计数字。
