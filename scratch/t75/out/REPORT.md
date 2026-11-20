# t75 — Club / Nation / COMP 主行槽位反查

**结论：处理 t72 的 10 项 Nation 上交，8 段实项逐字节闭合，2 段因没有实项保持 held。复验 A/B/C/D 的 19 个既有具名子槽，补齐 server 全档域；新增具名 L3 = 0，L4 = 0。** 三主行 99 个 t72 `unnamed/held` 外层槽全部入账：Club 25、COMP 40、Nation 34。完成指本轮验收，不表示剩余业务字段全解。未修改公共 schema v10。

## 1. Nation 优先：按 count、helper 与下一槽重放

坐标来自 t55/E94，静态地址是 PE **file offset**；数据 `@` 是解压成员绝对偏移，`body_relative` 以当前 selector 后的 `legacy14` 行体为原点。只读二进制 `<OLD_REPO>/input/editor.exe` SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。交付含 VA/bytes；冻结 master 与 `IDA_PROVENANCE.md` 对 MANIFEST 核验。`0x103fae6` 是外部 mode 门：client 不消费前六项的 count，不记作 251 个空 count。

| t72 上交 | NATION 对象位移 / count site | 已观察的 item 读法（LE） | Server 非空行 / item |
|---|---|---|---:|
| `slot_2` | `+0x128 / 0x103fb37` | i16 count；静态每项 4B，经 `0x103fcbd` 读到临时 qword 再插入。`0x3d603a7` 见同 vector 的 context `+0x28` resolver；不能以零实项闭合引用。首 count `@18:0000` | 0 / 0 |
| `slot_3` | `+0x158 / 0x103fe72` | i32 count；静态每项 4B，由 `0x103ff79` 读取。首 count `@20:00000000` | 0 / 0 |
| `slot_4` `Nftb` | `+0x170 / 0x104011f` | i16 count；`0x10401dd → 0x15cf370 → 0x448f890`：u8 tag、四组 `u32 len + bytes`、4B date、四个 4B lane。首实项 row 162 `@278811`；全 tag 1、46–54B | 1 / 7 |
| `slot_11` `Ntxr` | `+0x60 / 0x1040462` | i32 count；`0x1040494 → 0x144bca0 → 0x420c8f0`；`1+4+4+4+2+1+1+4+1+1`，tag≥2 再读 2B。首 `@54`；实档全 tag 2 / 25B | 221 / 1,899 |
| `slot_12` | `+0xd8 / 0x10404d1` | u32 count；`0x1040529` 读 4B，`0x104053f/554 → 0xdb7f80 → 0x39dd7d4` 各读 4B 日期。首项 `@258` | 164 / 27,178 |
| `slot_13` | `+0x78 / 0x3d74e62` | u32 count；`0x1040592 → 0x104e6b0 → 0x3d74e30`，`0x3d74f9c → 0x1072560 → 0x3daa110` 循环 `1+4+4+1+1+1+1+1`。首项 row 52 `@33627`；首 byte 实档全 1，读到栈上 | 19 / 58 |
| `slot_23` A `Nlns` | `+0x48 / 0x1040717` | i8 count，`0x104075b` 循环 `4+1` | 237 / 492 |
| `slot_24` B `Nefr` | `+0xa8 / 0x10407b0` | i32 count，`0x1040829` 循环 `5×4 + date4 + date4` | 43 / 214 |
| `slot_25` C `Nnfr` | `+0x90 / 0x104086c` | i32 count，`0x10408eb` 共用 B 的 item reader；由 getter selector 区分两 vector | 20 / 63 |
| `slot_26` D `Nagr` | `+0xc0 / 0x1040927` | i32 count，`0x10409a7` 循环 `4 + date4 + date4` | 126 / 162 |

- 全量游标闭合：client `13+24710+9=24732`；server `13+422323+9=422345`。Server 251 条 legacy 行逐条对照 t46 profiles，再核 t55 全槽坐标；没有用 t46 的 identity 找点来修补游标。A/B/C/D 首行 client `@38/54/58/62`、server `@562/578/582/586`；四段双档**各 251/251** count 和 payload 字节一致。t46 强套同偏移的 A 首反例 `row+24:a6 → -90` 原文保留。
- **A/B/C/D (E64)：** 原 A `lang/perc`、B/C 各 `nfrn/nfrc/fren/nfrr/nfra/stdt/endt`、D `NGag/NGsd/NGed`，共 19 个既有位置。每个引用均用目标档实表身份（t5/8/10/19/56）复验 ordinal、UID、错指、`ffffffff` 与合法 0。`lang` 的 492/492 ordinal 命中中，按 UID 查反而有 488 个命中，**488 个全部错指**；首 server `@563=1`，ordinal→UID 2，UID→ordinal 0。`Nnfr/nfrc` 63 项全空，保留既有静态槽，不声明活值；`Nlns/perc` 的 91 个单项行中 17 个 raw 不等于 reader 改写的 100。`stdt/endt` 的索引 locations 未列 Nation，JSON 如实保留；实际 occurrence 与精确 item getter 仍由冻结父列表和 t28 链核验，不补造索引记录。
- **Nftb / Ntxr (E90/E87)：** 四个已命名 Nftb 子项和七个已命名 Ntxr 子项保持原等级；变长串的四个长度前缀、税项修订尾均单独画像。`NbFt` 七个 ordinal 和 UID 都命中但全部错指，`NbPn` 0/7 ordinal（首 `@278852=788`，UID→ordinal 162）；延用 `NbPi` 的 E90 命中/首负例，不重读 person。`ppty/txty` 缺 scoped enum，`ppty` 99 个 raw 0 的读后改写仍适用。`Nftb` 父仅有 setter/item 证据，未补出精确父 getter。
- **两段新细化的未命名物理 lane：** `slot_12:item+0` 经 `0x104056d → 0x1040e00 → 0x3d5df50`，`0x3d745dc/df` 比较 i32 key，`0x3d5dfa7` 写有序节点 `+0x1c`，其后两日期存到节点 `+0x20/+0x24`。全档 27,178 个不同 key，t3/t10/t25 ordinal 均 0 命中；按 UID 只有 t3 碰巧 2 个命中。它是容器 key，**不**声称是业务 ID。两 packed date lane 各 27,178 个、无日历越界。`slot_13` tag 后对象目的位移 `+0,+4,+8,+9,+0xa,+0xb,+0xc`；7 个子 transfer 都有全档域，未见精确父/子 4CC，继续 held 命名。

## 2. Club / COMP 指纹优先，及 held 邻接

`xref_reverse.json` 以 t72 小枚举子集、实表 ordinal 与错 UID 分离度排队，再扫 live held 和零/全一槽。成员位移反查索引保留直接 compare、bit gate、rel32 cell 与数值位移碰撞；匹配到另一 `this` 或虚表偏移不算同成员。CLUB 主 reader `0xe5a7a0..0xe5bfca`（1,412 条）；COMP `0xeb7000..0xeb7e42`（837 条）；NATION `0x103fac0..0x1040be4`（992 条）。COMP 本地 getter `0xec0060` 的有界反查比仅直接边多解 **19 张**精准归一化的 rel32 表（共 5,736 条）；`0xec1298` 间接尾跳和 `0xec604b` 非 4CC 归一化路径不作本文的字段层穷尽。CLUB slot-2 主 extent 沿用 E106 的分发表形状，不展开 t71 `+0x100` helpers。

| 槽 | 反查裁决 |
|---|---|
| Club `ref_e0` | `0xe5a843 → +0xe0 → 0xe5c59e/c5a5/c5b9` 的 Nation resolver 复现 E106。每档 26,587 live 全命中；UID 误查 9,286 个且全指别行，首 miss client `@19270:aa000000`。没有精确 scoped 4CC，仍 held。 |
| Club `raw168`；COMP `m152` | 真 t21 ordinal 分别 84,259/84,259（server）、7,047/7,047（各档），错误 UID 各 10,851 / 1,067 命中但全错指。首 server `@162=2750` / client `@88=6009`；均无所需 resolver + 4CC，不能命名为 Stadium。 |
| COMP `m1a4`；`mf9` | `0xec2c88/8e → 0xec2c94` 精确 `Ccre`，与 `0xeb70ed/0xeb7100` 的 `+0x1a4` 同址；样例 client `@31:01`。虽然六值落入冻结 `cdbt` 子集，**`Ccre` 不在冻结索引**。`cosr` 精确同址但也不在索引，`0xec35e3/e6` 抑制 -1；双档全 -1，首 `@127:ff`。两条不补猜语义。 |
| COMP `m1a8`、`mf4` | `+0x1a8` 的 getter 位移撞到另一个 context 子对象 `RDI`，非 COMP reader 的 `RBX`。`WpBn` 是 `+0xf4` 受 Nation/context 和 bit gate 控制后的计算投影（helper `0xec4341`，`0xec4346` 加 1）；`dbty` 仍有首反例 server row 394 `@102218:1e` 不入 scoped `cdbt`。 |
| COMP `m138/m13c`；Nation `slot_31` | 两日期 lane 双档各 7,047 个，无无效日期，但没有 scoped getter，且不等于 `wbst/wben` 的 `+0x140/+0x144`。Nation `+0x1b8` t25 ordinal 251/251、错 UID 56（全错指），首 `@606=981`，一样缺 resolver 和 getter。 |
| 版本/模式及其它 held | Club tag `{0,2}` 虽落入 `cnst` 子集，实为 `0xe5ada9` 的对象分支；COMP presence、颜色/修订标志不作业务枚举。对 `Necf/Nygn/Ngct/Nsod` 等保留旧首反例及域限制。`EDsc` 复核 E105：归一化后 base `0x2a7f0` 格 `0x32 → 0x29389`，是已追到的 UI 分发，不是新增 wire。 |

**边界**：不重做 t66 已闭 COMP 集合、八个独立 Club 子表、`CLUB_LINK`、t71 的 24 个 `+0x100` 项、person/PDxx。未启动游戏、编辑器或 IDA；未联网或访问 `Z:`。负例以原始 JSON 值复制到台账并带引用 ID（含 E60 的旧 `Cccn@row+8`、t59 falsified、t64 exclusions、t62 exclusions），没有翻案。没有将全一等同于空、或将 absence 等同于零 count，除非静态/既有槽定义确立其解释。

## 3. 复跑

```bash
export FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t75_slot_xref_reverse.py --build
py -V:3.12 -I -B scratch/t75/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py
```

独立 verifier 自解 FMF 目录和 Zstd 成员界，复用 t55/t57/t59 的**独立 verifier**外层游标，不 import builder / `ReaderCFG` / `fm24_dump`。独立复算 item、目标身份、域和静态原字节/VA/关键 rel32。固定宽度坐标、值域、ordinal/UID 和日期扫描向量化；变长串和 tax tag 顺序走界，不抽样代替。两个脚本 `--help`、`--selftest` 与全量 build/verify 均通过；anchors **7/7**；退出码 0/1/2。
