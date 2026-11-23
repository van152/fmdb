# t27 — table_22 球场／迁建子表

**逐行 cursor 已闭合，字段台账仍为 partial。** E56 的归属不变：这是 `club.Cstc`，`STADIUM_CHANGE` 是运行时类名，不是 stadium 主表。server 449 行每行消费 79 B（1 B selector + 78 B 行体）；client **也有** table_22，其 449 行只有 selector + 12 B identity，不能用来读业务字段。Cstc 命名从 **0 → 14/28 occurrence（+14 L3、无 L4）**。

## Cursor 与分支

- 静态输入为只读 `D:/tmp2b/fm24/input/editor.exe`；SHA-256 与 IDA_PROVENANCE 一致，provenance 与 schema 快照均经 `evidence/MANIFEST.json` 校验。factory case 22 file offset `0xf49092`，vtable VA `0x1418bd5a8`，slot 19 VA `0x141538200` / file offset `0x1537800`。
- PE runtime extent 至 file offset `0x1537b04`（exclusive），可达 **210 指令、35 基本块、28 条条件分支、2 条无条件跳转**。t20 的 23 条仅数至第一个 `ret`：2 条外部入口条件（context／业务模式）+ 18 条 stream status + 3 条 helper AL。另 5 条在后置路径，其中只有 `0x1537acc` 用 t22 行体读入值决定分支。`branches.part001.json` 逐条记录谓词、双边、证据及两份 archive 的计数。
- 三个漏算的 4B 消费点是 caller `0x1537888` / `0x153789c` / `0x15379d0` → thunk `0xdb7f80` → helper `0x39dd7b0` → stream call `0x39dd7d4`。对象目标分别为 `+0x30/+0x34/+0x38`。它们把 t20 的 18 次直读（54 B）补足为 **66 B 属性块**。t20 的 `66` 刚好也是 `54 B 直读 + 12 B bulk`；两者不能互换。
- 12 B bulk：`0x1537aa1` 取 `this+8`，`0x1537aa8` 设宽度 12，`0x1537ab1` 把 sink 放入 RDX，`0x1537ab4` 执行转移。server `+66/+70/+74`（client `+0/+4/+8`）是三条 little-endian u32，全部为 `(i,i+1,i+1)`，449 行在两个 archive 逐字节相同。首 lane 是 record ordinal，另两 lane 是重复的 UID 形态；均不计 Cstc 业务字段。首 lane 喂无符号阈值 `0x989681` 的 `jb`，449/449 取边、不重写 ordinal；并非用行号决定分支。
- loader `0xf2ba0e` 在每行 **前面**读 selector（两边 449 个均为 `00`）。server payload 35,493 B，client 5,859 B；两边交换模式都在第 0 行 identity 后置校验失败。真实 footer 为 `00000000 01 c1010000`，从 server `35484` / client `5850` 开始。`13 + 449*(1+66+12) + 9 = 35493` 与 t20 的 `14 + 449*79 + 8 = 35493` 都成立：旧坐标的 `+78` 是下一行 selector，最后一行则借 footer 的首零字节。业务偏移仍相对行体首字节（旧起点 14），无需迁移坐标原点。
- **运行时边仍有限制。** 成功 I/O、非空 context／stream、callback 与引用计数不是行字节。`0x153781b` 的值为 caller 参数，由两份 payload 差分反推；不从 `Styp` 或 selector 猜。callback 分派本体及终结析构分支未展开；前者按已定位 loader 的非空参数建模，后者按存活的 stream 持有者建模。这不是全运行时状态的证明，也不外推到其他版本、坏流或其他 caller。

## 晋级与保留

| 已晋级 code | row+ | object+ | 宽度 B |
|---|---:|---:|---:|
| Slea | 12 | `0x30` | 4 |
| Scap | 20 | `0x3c` | 4 |
| Salt | 25 | `0x48` | 4 |
| Scpm | 29 | `0x65` | 1（bit 2） |
| Sscp | 30 | `0x40` | 4 |
| Snxa / Snmn / Snmx / Stks | 34 / 38 / 42 / 46 | `0x50` / `0x54` / `0x58` / `0x5c` | 各 4 |
| Slmd | 50 | `0x38` | 4 |
| Slhm | 54 | `0x66` | 1 |
| ScTL / ScYL | 60 / 61 | `0x67` / `0x68` | 各 1 |
| Sceb | 62 | `0x44` | 4 |

- 三个日期槽 449/449 均满足 t13d 的 packed day/year：`+12` 2000–2030（Slea）、`+16` 2017–2030（Ssta，重复 occurrence，不计命名）、`+50` 1900–2030（Slmd）。每个 getter 均读同一对象槽的两个 u16，非单看数值猜名。
- `Salt` 有 208 个 live ordinal，全部同时落在 club ordinal 区间和 schema 声明的 stadium 目标 ordinal 集；club 数值范围重叠不证明指向 club。`+0` 另有 361 live / 310 distinct / 88 个 `FFFFFFFF`，live `[86,82403]`，全部是 t24 club ordinal 域中的值。对称 writer 取所引用记录的 `+8` 或空引用 `FFFFFFFF`；slot 20 的修复路径也把 `this+0x18` 送进与其后三个 stadium 槽不同的 resolver。slot 0 只记「引用形态、club 域吻合」，没有 scoped Cstc 4CC，不命名。
- `Scpm` 不是整字节布尔：getter 明确取 bit 2，原始分布 `0/2/4 = 390/36/23`，解码 false/true `426/23`。bit 1 不命名。
- `Sold@+4`、`Snew@+8`、`Ssta@+16` 的 wire sink 与 code 已对账，**不把同一 getter 分摊成多个独立命名**。`Styp@+24` 的 88 个 raw `2` 不在冻结 UI enum；`Scns@+59` 的 23 个 raw `0` 不在该 enum（不是 getter 的 `-1` 空值）；`Scam@+55` 有 3 个超出冻结 schema 原始界值的样本。三者保留坐标候选，未擅自重编码或按 `store_pence` 换算后晋级。`Scap/Sscp` 的原始整数范围通过，但只在 raw type `2` 有非空值，冻结 UI 可见性条件为 `6`；晋级仅指 getter 的存储坐标，不声称解决 type 的 UI 对应关系。E56 的 `Scam` 身份不因未晋级而撤回。
- t20 原负例保留：
  > `scratch/t13d/out/audit.json` 对 +12、+16、+50 给出稳定的 packed day/year 画像（年份范围分别为 2000–2030、2017–2030、1900–2030）。候选线性配对却会把 +12 叫作 `Scap`（New Capacity）、把 +16 起始字节叫作 `Styp`（Type）、把 +50 叫作 `Sceb`（Future Stadium Development Fund）；这些不是可接受的独立互验。候选 `Salt@+17` 还落在 +16 日期内部。

## 验证与交付

- `py -V:3.12 -I scripts/t27_stadium_cursor.py` — 生成路径、台账和侦察表；`--help` / `--selftest` 通过。
- `py -V:3.12 -I scratch/t27/out/verify.py` — 独立拆行、验证 449+449 行及 9 B footer，与 t13d CSV 逐字节互验；重解 PE 分支/transfer/getter 证据，复算 449 行字段规则与三行字节抽样，命名增量 +14。`--help` / `--selftest` 通过。
- `py -V:3.12 -I scratch/t20/out/verify.py` — PASS (partial)，原证据未改。
- `py -V:3.12 -I scripts/t01_anchors.py` — **7/7 PASS**。
- 交付索引：`cursor_t22.json`（引用 `branches`、`transfers`、`instructions`、`rows_server` 分片）；`fields_t22.json`（引用三份分片）；`replication.md` 与 `scout.json`（Cafl/Cvfl 共享 club-object 区间线索，独立表号仍 unknown）；`verify.py`；本报告；构建脚本 `scripts/t27_stadium_cursor.py`。
