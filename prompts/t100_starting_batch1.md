# t100 — `STARTING_*` 子表批次 1（tt 12..46，共 16 张表）Hex-Rays 线协议与 L3 字段定稿

> 交付目录：`OUTDIR`（`scratch/t100/out`）
> 脚本路径：`scripts/t100_starting_batch1.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`、`scratch/data/server_db.dat`、`scripts/t38_multiframe.py`。不要修改 `reports/` 或 `LEDGER.json`。

## 目标表清单（16 张，不含 t98 专攻的 tt=45）
`tt = 12, 26, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 42, 43, 46`（以及 `tt=4` `RGB_COLOUR` 若存在）。
具体每张表的类名、vtable、`slot19_read_server` / `slot02_get_prop` / `slot03_set_prop` 文件路径全部已在 `scratch/t95/vtable_index.json` 中就绪！

## 任务要求
对这 16 张表逐一：
1. 精读 `slot19_read_server`（及其 `hop1` 若为薄封装）的 Hex-Rays C 伪代码，提取精确 wire 字段顺序：`(wire_idx, field_kind: u8/u16/u32/u64/dbid8/date4/string/vec/base12, mem_off, c_line)`。
2. 精读 `slot02_get_prop` / `slot03_set_prop`，把 `4CC → mem_off` 与步骤 1 的 `mem_off → wire_idx` 自动/人工 Join，给出每张表的完整 L3 字段定义（带 C 文件行号）。
3. 在 `scripts/t100_starting_batch1.py` 中为每张表实现真实解码器，对 `server_db/table_<N>.dat` 跑全表（或大表前 2,000 行 + 末行闭合检查）验证，核对总行数与末尾 9B footer 是否字节精确闭合！
4. **分块落盘原则**：每完成 4 张表就把中间结果写入 `OUTDIR/batch1_schemas.json`，避免单次长跑超时丢进度。

## 交付物（写入 `OUTDIR`）
1. `batch1_schemas.json`：含 `"status": "complete"`，16 张表逐表 L3 wire schema、4CC 映射、真数据校验结果（rows_decoded, footer_closed, sample_row0）。
2. `REPORT.md`：汇总表（表号、类名、行数、列数、4CC 命中数、footer 闭合状态）。
3. `DONE.md`：含 `DONE type=t100` 与核心统计数字。
