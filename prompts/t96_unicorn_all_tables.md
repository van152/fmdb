# t96 — 全表 Unicorn 微执行 Wire 追踪与字节精确闭合

> 交付目录：`OUTDIR`（`scratch/t96/out`）
> 脚本路径：`scripts/t96_unicorn_all_tables.py`（Python 3.12 `-B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 允许使用：已安装的 `unicorn`、`capstone`、`pefile`、只读 `D:\tmp2b\fm24\input\editor.exe`、`scratch/data/*.dat`、`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`。不要启动游戏/编辑器；不要修改 `reports/` 或 `LEDGER.json`。

## 已有基建（直接复用，不要从头造轮子）

1. **`scripts/t95_unicorn_trace.py`**：已验证可跑通 `editor.exe` 真 x86_64 机器码！
   实测已 `ok=True, err=None, un=[]` 跑通 6 张大表：`table_45` (93B/20 reads)、`table_9` (57B/35 reads)、`table_3 CLUB` (79B/10 reads)、`table_25 COMP` (126B/64 reads)、`table_0 AWARD` (40B/28 reads)、`table_21 STADIUM` (37B/9 reads)。
2. **`scratch/t95/vtable_index.json`**：67 张表全量 vtable 索引，已含每张表的 `slot19_read_server`、`slot20_read_client`、`hop1_functions`（283/284 函数已反编译到 `scratch/t95/funcs/<va>.c`）。
3. **`scripts/t38_multiframe.py`**：权威 `.dat` 解压加载器（E80 规则：成员起点 = `data_base + offset`，按 `entry.size` 选帧）。

## 任务目标

### 1. 升级 Unicorn 引擎实现「整表逐行微执行」
基于 `scripts/t95_unicorn_trace.py` 构建 `scripts/t96_unicorn_all_tables.py`，解决：
- **行帧边界自动对齐**：确认 `DATABASE_TABLE` 13B 头（`03 01 tad. <u16 ver> <u32 count>`）后每行的前置 1B 标志位（如 `0x00` 行起始哨兵 vs 无哨兵），并在逐行推进时检查下一行起点与末尾 9B footer（`payload_len - 9`）的精确闭合。
- **修复 `table_10 (NATION)` 等剩余异常**：检查 `table_10` 在 row 0 触发 `_Xlength_error` 的原因（偏移 13 vs 14？或 `a3/a4/a5/a6/a7` 参数 / `std::vector` 初始字段 / `this` 需先调构造函数初始化？注意 `sub_140F49530` 中各表构造器有默认初值！必要时对 `this` 先执行 `sub_140F49530` 或给关键偏移置默认值）。
- **捕获字符串与动态数组读取**：除 `dst_kind == "this"` 外，标注 `stack`/`heap` 读取对应的长度字段与父调用链，尽量给出每条 `stream->read` 写入的稳定 `obj_off`（包括通过子对象指针写入的容器）。

### 2. 全表批量跑通（`server_db.dat` + `client_db.dat`）
对 `server_db.dat` 和 `client_db.dat` 中所有 `table_<N>.dat`（排除 0 行空表或标注 0 行）：
- 至少跑通每张表的前 **5 行**（若总行数 ≤ 500 行，例如 `table_9` 251 行、`table_10` 251 行、`table_0`/`table_5`/`table_6`/`table_7`/`table_8`/`table_19`/`table_27`/`table_41` 等，**跑通全表所有行**并校验是否精确命中 `payload_len - 9` footer！）。
- **重点闭环 `table_9` (`NATIONAL_TEAM_CONTAINER`, `0x14105D510`)**：跑通 `server_db/table_9.dat` 全部 251 行与 `client_db/table_9.dat` 全部 251 行，核对总消费字节 == `307,564` / `31,956`（含 13B header + 9B footer），列出所有出现过的 helper caller VA 与 211 种 body 长度分布的成因（直接解决 `scratch/t92/out/REPORT.md` 未决项 #4）！
- 同时重点检查 `table_3 (CLUB)`、`table_10 (NATION)`、`table_25 (COMP)`、`table_21 (STADIUM)`、`table_24 (TEAM)`、`table_45 (STARTING_RECORD)` 的前 20 行与多行推进是否字节精确对齐！

### 3. 交付物（写入 `OUTDIR`）
1. `wire_traces.json`：含 `"status": "complete"`（或 `"partial"`），按 `(archive, table_id)` 记录：
   - `class`, `func_va`, `version`, `total_rows_header`, `rows_tested`, `rows_ok`, `all_rows_closed_to_footer` (bool), `row_prefix_bytes` (0/1), `row0_consumed_bytes`
   - `canonical_fields`: 聚合后的字段序列 `[{idx, wire_off_example, n, dst_kind, obj_off, caller_va, variable_len, seen_in_rows}]`
   - 若某表失败，如实记录 `error`, `end_rip`, `unhandled_calls`（不隐瞒、不伪造）。
2. `table9_251_closure.json`：`table_9` server + client 251 行全量逐行字节长、helper 触发统计与 footer 闭合验证。
3. `REPORT.md`：总表覆盖统计（成功表数/总表数、闭合到 footer 的表清单、失败表诊断、`table_9` 251 行闭包总结）。
4. `DONE.md`：含 `DONE type=t96` 与核心指标摘要。

## 验收标准
- `py -V:3.12 -B scripts/t96_unicorn_all_tables.py --selftest` 退出 0。
- `wire_traces.json` 至少成功追踪 **35 张以上**表的真实行，且 `table_9` server/client 251 行与 `table_45` / `table_25` / `table_3` / `table_10` 均给出可复现的字节精确追踪结果。
- 完成后打印交付清单与核心统计数字。
