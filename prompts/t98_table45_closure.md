# t98 — table_45 (`STARTING_RECORD`) 全列 L3 定稿与 117 访问器视图闭合

> 交付目录：`OUTDIR`（`scratch/t98/out`）
> 脚本路径：`scripts/t98_table45_closure.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（只读）：
> - `scratch/t95/funcs/141544130.c` (`STARTING_RECORD::slot19_read_server`)
> - `scratch/t95/funcs/1415446a0.c` (`STARTING_RECORD::slot02_get_prop`)
> - `scratch/t95/funcs/141545680.c` (`STARTING_RECORD::slot03_set_prop`)
> - `scratch/t95/funcs/1444e4b00.c` (`STARTING_RECORD::slot21_write`)
> - `scratch/t95/funcs/140e8a400.c` (`CLUB::slot02_get_prop`) 和 `140e834a0.c` (`CLUB::slot03_set_prop`)
> - `scratch/t95/funcs/1411f1090.c` (`TEAM_CONTAINER::slot02_get_prop`)
> - `scratch/data/server_db.dat` 中的 `table_45.dat`（84,477 行）和 `table_48.dat`（5,210 行，共享同一 `STARTING_RECORD` vtable `0x14187df38`！）
> - `reports/xml_denominator_coverage.json` 中 `re_routed_table_45` 的 117 条码，以及 `scratch/t88/` 相关参考。
> 不要修改 `reports/` 或 `LEDGER.json`。

## 已有突破（已由 IDA 9.4 + Unicorn 实证！）

`141544130.c` 与 Unicorn 实测已经把 `table_45`（`80 + namelen` 字节）的 **18 个物理列** 全部对应到 `STARTING_RECORD` 的精确内存偏移：
- `wire+0` (4B) → `this+0x4c` (`a1+19`, u32)
- `wire+4` (1B) → `this+0x5e` (`rec_type`, u8)
- `wire+5` (8B) → `this+0x18` (`a1+6`, 8B DBID/UID)
- `wire+13` (8B) → `this+0x20` (`a1+8`, 8B DBID/UID)
- `wire+21` (8B) → `this+0x28` (`a1+10`, 8B DBID/UID)
- `wire+29` (8B) → `this+0x30` (`a1+12`, 8B DBID/UID via `sub_140FEA0C0`)
- `wire+37` (4+N B) → `this+0x38` (`a1+14`, `[u32 len][utf8]` string via `sub_140814B10`)
- `tail+0` (4B) → `this+0x40` (`a1+16`, 4B date via `sub_140DB8980`)
- `tail+4` (4B) → `this+0x44` (`a1+17`, 4B date)
- `tail+8` (4B) → `this+0x48` (`a1+18`, 4B date)
- `tail+12` (4B) → `this+0x50` (`a1+20`, u32)
- `tail+16` (2B) → `this+0x54` (`a1+21`, u16)
- `tail+18` (2B) → `this+0x56` (u16)
- `tail+20` (2B) → `this+0x58` (`a1+22`, u16)
- `tail+22` (1B) → `this+0x5a` (u8)
- `tail+23` (1B) → `this+0x5b` (u8)
- `tail+24` (1B) → `this+0x5c` (`a1+23`, u8)
- `tail+25` (1B) → `this+0x5d` (u8)
- `tail+26` (12B + 1B next-row prefix) → `this+0x08` (`sub_140FAED40` base identity)

## 任务目标（一次性解决 `scratch/t92/out/REPORT.md` 未决项 #1、#2、#3！）

1. **完整解码 `STARTING_RECORD` 18 物理列的 4CC 语义（L3）**：
   - 精读 `1415446a0.c` (`get_prop`)、`141545680.c` (`set_prop`)、`1444e4b00.c` (`write`)，列出 `STARTING_RECORD` 自身的全部 4CC → `this+0xNN` → `wire_off` 精确三元映射（包括类型、语义、读写行为）。
   - 同时核对 `table_45.dat`（84,477 行）与 `table_48.dat`（5,210 行，共享同一 vtable）各列的值域分布、非空率（按 37 种 `rec_type` 分组统计！）。
2. **钉死 117 个访问器视图码（`club.xml[211..327]`）→ `(rec_type, physical_col, mem_off, wire_off)`**：
   - 精读 `140e8a400.c` (`CLUB::get_prop`) 与 `140e834a0.c` (`CLUB::set_prop`) 中对 34 个 L3 码（`CFG*`/`CHA*`/`CHS*`/`CLA*`/`CYP*`/`CYS*`/`COS*`）以及其余 80 个 held 码（`CBW*`/`CBD*` 等）的处理逻辑：
     - 查清所有 suffix（如 `*n`/`*p`/`*t`/`*d`/`*v`/`*c`/`*y` 等）在 `CLUB::get_prop`/`set_prop` 里访问的是 `STARTING_RECORD` 的哪一个 `this+0xNN` 偏移，直接翻译为精确 `wire_off`！
     - 对 80 个 held 码，按 `rec_type`（共 37 种）结合真实 `table_45.dat` 84,477 行数据中各 `rec_type` 哪些物理列非默认/非空（如 `0xFFFFFFFF` / `0x076C0001` / 空串 / `0`）+ `table_48.dat` 对照，给出每个 `rec_type` 的实际活跃物理列画像，并对照 `club.xml` 的分组顺序给出严格分级（L3 已证 vs L2 数据侧候选 vs 仍 held）。
3. **验证全部 84,477 行 `table_45.dat` 与全部 5,210 行 `table_48.dat` 100% 字节精确解包**（含末尾 9B footer 闭合验证！）。

## 交付物（写入 `OUTDIR`）
1. `table45_full_schema.json`：含 `"status": "complete"`，18 物理列完整三元映射、37 种 `rec_type` 活跃列画像、117 码逐条映射（带证据级别与 C 代码行号）。
2. `table48_comparison.json`：`table_48.dat` 5,210 行的相同解码验证与 `rec_type` 分布对照。
3. `REPORT.md`：清晰汇总（可直接作为后续 schema v12 并入依据）。
4. `verify.py`：独立校验脚本（重跑 `table_45` 84,477 行 + `table_48` 5,210 行解包与 footer 闭合 + 18 列偏移一致性断言）。
5. `DONE.md`：含 `DONE type=t98` 与核心统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t98_table45_closure.py --selftest` 退出 0。
- `py -V:3.12 -I -B scratch/t98/out/verify.py` 全绿退出 0。
- 严格区分 L3（C 代码直接证明）与 L2/held（数据侧推断），不越级定论。
