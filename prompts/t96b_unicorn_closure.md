# t96b — Unicorn 全表（79 对 server+client）字节精确闭合与 `table_9` / `table_10` 251 行全闭

> 交付目录：`OUTDIR`（`scratch/t96b/out`）
> 脚本路径：`scripts/t96b_unicorn_closure.py`（Python 3.12 `-B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 不要修改 `reports/` 或 `LEDGER.json`。

## 指挥官刚刚已经实证打通的 3 个核心机制（全部已写入 `scripts/t95_unicorn_trace.py`！）

1. **`slot19` 一函双用：`a7=1` 读 `server_db.dat`，`a7=0` 读 `client_db.dat`！**
   - `slot20` 是引用解析器，不是 client 读流器！client 表统一调 `slot19(..., a7=0)`，server 表调 `slot19(..., a7=1)`！
2. **每行前面有 1 字节行前缀标志**（位于 13B 表头之后、每次调用 `slot19` 之前跳过/读取这 1B）。
3. **SI 引擎两个内部池分配器已 hook 到 `EditorEmulator._alloc`**（`0x1407e4490`/`0x143671d70`、`0x1407e58c0`/`0x143676ca0`、`0x141750cc0`）。

**仅凭这 3 处修复，指挥官刚实测已瞬间全表闭合（`diff == 0, closed=True`）：**
- `server/t5` (7/7)、`client/t5` (7/7)
- `server/t6` (115/115)、`client/t6` (115/115)
- `server/t7` (208/208)、`client/t7` (208/208)
- `server/t8` (126/126)、`client/t8` (126/126)
- **`client/t9` (251/251, 31947 == 31947, diff=0!)**
- **`client/t10` (251/251, 24723 == 24723, diff=0!)**
- `server/t46` (7/7, 188 == 188, diff=0!)
- 以及 `server/t25`, `client/t25`, `server/t2`, `client/t2`, `server/t21`, `client/t21`, `client/t3`, `server/t45` 全部 10/10 干净跑通！

## 你需要攻克的最后 3 个小问题（攻克即全库 70+ 表闭合！）

1. **`server/t9` (251 行) & `server/t10` (251 行) 的 `rip=0x140893bef` (`addr=0x0`)**：
   - `0x140893be0` 是 `std::vector<T*>::reserve(rcx=vec_ptr, rdx=count)`，`rcx == 0` 是因为 `THIS_BASE` 是全零缓冲，**没有调用真正的 C++ 构造函数**！
   - 查 `scratch/t94/out/decompiled/tt011_140f49530.c`（工厂 `sub_140F49530`）：
     - `case 9` 调 `sub_14105A430(this)`；`case 10` 调 `sub_14103F5F0(this)`；`case 3` 调 `sub_140E5A440(this)`；`case 25` 调 `sub_140EB67B0(this)`！
   - **解法**：在每次 `trace_read` 之前，直接用 Unicorn 先执行该表的构造函数（或调用 `sub_140F49530(table_type, flag)` 拿到已构造好的 `this` 指针，再作为 `RCX` 传入 `slot19`！注意同时为可能需要的辅助分配器/全局单例打必要 stub）。
   - 验证 **`server/t9` 全部 251 行闭合到 `footer=307555` (`diff=0`)** 且记录全部 251 行长度分布与 24 个 helper 调用统计（彻底解决 v11.3 未决项 #4）！
   - 验证 **`server/t10` 全部 251 行闭合到 `footer=422336` (`diff=0`)**！
2. **`server/t3 (CLUB)` row 3 (`huge_read` at `0x14371be86`) 与 `server/t0 (AWARD)` row 1 (`flag=0xc8`, `0x140f92cc4`)**：
   - 排查 `flag`（每行前缀 1B）的语义：在 `table_3` / `table_24` / `table_0` 等多态表中，`flag` 可能决定子类 vtable（例如 `CLUB` vs `LEAGUE_BODY_CLUB` 当 `flag==12`！看 `sub_140F49530` `case 3: if ((BYTE)a2 == 12) vtable=LEAGUE_BODY_CLUB else CLUB`！以及 `case 24: if ((BYTE)a2 == 11) NATIONAL_TEAM else TEAM`！），或者决定某些可选段！
   - 若直接调 `obj = sub_140F49530(table_type, flag)`，然后取 `*(uint64*)(*(uint64*)obj + 19*8)` 作为 `slot19` 虚函数地址执行，多态表（`t3`/`t24`/`t0`）会自动分发到正确的子类构造函数和 `slot19`！！
3. **全量跑通 `server_db.dat` + `client_db.dat` 全部 79 张有行表**：
   - 小/中表（`nrows <= 2000`）：**全表跑完所有行**并校验 `pos == len(payload) - 9` (`diff == 0`)！
   - 大表（`nrows > 2000`，如 `t3` 84k 行、`t25` 7k 行、`t21` 48k 行、`t45` 84k 行、`t49` 792k 行、`t71` 616k 行）：跑前 **50 行**（若速度很快如 `t25` 7,047 行可在 30s 内跑完也欢迎全跑！），确保零异常推进！
   - **重要体积纪律**：`wire_traces_v2.json` **不要存每行的原始 reads 列表**（避免 800MB），只存每张表聚合后的 `canonical_fields`（字段序、示例 `wire_off`、`n`、`dst_kind`、`obj_off`、`caller_va`、`is_varlen`、出现行频）+ `row0_reads` + 闭合统计，文件体积控制在 **< 15 MB**！

## 交付物（写入 `OUTDIR = scratch/t96b/out`）
1. `wire_traces_v2.json`：含 `"status": "complete"`（或 `"partial"`），全部 79 对 `(archive, table_id)` 的 Unicorn 真机微执行聚合 schema + 闭合结果。
2. `table9_251_closure.json`：`table_9` server 251/251 (`307555`) + client 251/251 (`31947`) 完整逐行长度、211 种长度分布成因、helper 调用频次统计。
3. `table10_251_closure.json`：`table_10` server 251/251 (`422336`) + client 251/251 (`24723`) 完整逐行闭合与字段序。
4. `REPORT.md`：总表闭合率（目标 ≥ 50/79 全表或 50 行干净跑通，所有 ≤2000 行表尽量 100% `diff=0`）、多态 flag 发现、剩余失败表精确诊断。
5. `DONE.md`：含 `DONE type=t96b` 与核心统计数字。

## 验收标准
- `py -V:3.12 -B scripts/t96b_unicorn_closure.py --selftest` 退出 0（须断言 `server/t5`, `client/t5`, `client/t9`, `client/t10` 至少 4 表 `diff == 0`）。
- 优先把 `server/t9` 251/251 和 `server/t10` 251/251 跑通闭合到 `diff == 0`。
- 诚实报告未闭合表，绝不伪造。
