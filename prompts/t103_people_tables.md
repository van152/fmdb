# t103 — 人物体系表（`BASIC_PERSON` tt=1 / `PLAYING_HISTORY` tt=14 / `NON_PLAYING_HISTORY` tt=44）与 people/hist 归档 L3 解析

> 交付目录：`OUTDIR`（`scratch/t103/out`）
> 脚本路径：`scripts/t103_people_tables.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`、`scratch/data/basic_people_db.dat`、`scratch/data/people_db.dat`、`scratch/data/pl_hist_*.dat`、`scratch/data/non_pl_hist_*.dat`、`scripts/t38_multiframe.py`。不要修改 `reports/` 或 `LEDGER.json`。

## 任务要求
1. 精读 `scratch/t95/funcs/*.c` 中以下 3 个核心人物表类的反编译伪代码：
   - `tt=1 BASIC_PERSON` (`slot19`, `slot20`, `slot02`, `slot03`, `slot05` 及 `hop1` 如 `140e4fd70.c`, `140e50250.c`, `140e50cd0.c`, `140e52de0.c`)
   - `tt=14 PLAYING_HISTORY` (`slot19`, `slot20`, `slot02`, `slot03` 及 `hop1`)
   - `tt=44 NON_PLAYING_HISTORY` (`slot19`, `slot20`, `slot02`, `slot03` 及 `hop1` 如 `14437e8d0.c`, `14437ef40.c`, `14437f2a0.c`)
2. 提取三者的完整 L3 wire 顺序与 `4CC ↔ mem_off ↔ wire_off` 映射（带 `func_va` 与 C 行号）。
3. 检查 `basic_people_db.dat` (12.9 MB)、`people_db.dat` (67.5 MB)、`pl_hist_dt/id/index.dat`、`non_pl_hist_dt/id/index.dat` 的内部结构与头帧格式，用代码在真实 `.dat` 样本（每档至少前 1,000 行 + 索引表校验）上验证解码器字节对齐！
4. 如实标注 `people_db.dat` 中 `PERSON` 子类（如 `PLAYER`/`NON_PLAYER`/`OFFICIAL`）的扩展块边界（若超出现有 3 个 vtable，列出待后续 IDA 反编译的子表 vtable VA）。

## 交付物（写入 `OUTDIR`）
1. `people_tables_schema.json`：含 `"status": "complete"`，3 表完整 L3 schema、4CC 映射、各 `.dat` 归档结构摘要与真数据样本验证。
2. `REPORT.md`：清晰报告与后续扩展子类的 vtable 清单。
3. `DONE.md`：含 `DONE type=t103` 与核心统计数字。
