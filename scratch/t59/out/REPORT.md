# t59 — COMP `table_25` 主行槽位普查

**双档行框与现代外层序列闭合；字段命名 partial。** Client、server 各 7,047 行，独立数据 census 与 reader 游标逐行一致。82 个实档外层位置；另有两个静态存在但全档不进的可选 payload。冻结 `comp.xml#comp` 的 255 个顶层 occurrence 中，54 项连到 wire 槽或投影；49 项过本轮 L3（48 个不同 4CC，`duni` 重复 2 次），其中 **26 个新 4CC**；10 held，196 unmapped。数字包含 5 个无绑定 wire 的 held；不回撤旧 t01f client 静态证据。L4=0。

## 行框双证

| 档 | 原生封口 | 原生行宽 | 解压成员 SHA-256 |
|---|---|---|---|
| client | `13 + 894,969 + 9 = 894,991` | 127 B | `ae14d97c7ef951f197d885cc6f925cf13d13b09f7f2d9d04925fb17dcefb4a4d` |
| server | `13 + 1,533,950 + 9 = 1,533,972` | 198–1,894 B | `98bb59ad08a6de9bc73992d8e7bf400ea6697159bf5911b5e56742a6bdb1d8f5` |

从 FMF 目录 `data_base + entry.offset` 的受限成员区域按声明长度唯一选帧。数据侧不按固定 stride 猜 server 边界：扫描四种字节对齐的 `ordinal|UID|UID` triple，分 ordinal 层计数非重叠全铺法。标准约束下双档各一路；`ordinal=0..7046`；UID `1..2000340046` 非零、严格递增、唯一、双档同值。Reader 从 `@13` 顺走，不使用 triple 搜索来修补游标。

| 敏感性（client / server） | 结果 |
|---|---|
| 12 B identity，footer 7 / 8 / 9 / 10 / 12 | 均 `0 / 0 / 1 / 0 / 0`；错 footer 首个断点 ordinal 7046，候选 `@894970` / `@1533951` |
| 强制 13 B 且第 13 byte=0，footer 7 / 8 / 9 / 10 / 12 | 均 `0 / 1 / 0 / 0 / 0`；只是把下一 selector（末行则取 footer 第一字节）借给前行 |
| 13 B / 8 B 放开 marker、放开 UID 递增、或仅放开 UID 非零 | 单项放宽双档仍各 1 路；供对照的 lookahead 集 `{0,12}` 不等于 COMP 支持 selector 12 |
| 同时放开 UID 非零与递增（保留 lookahead 约束） | client `≥1,000,000`（上限），server 4 路 |
| 数据侧 header 11–15，13 B / 8 B | 每个候选各 1 路；仅靠尾 triple 不能定 header |

**原生 identity 是 12 B，footer 是 9 B。** `0xeb7d84 → 0xfae340 → 0x3c600f0`，`0x3c60106/0d/19` 向 `this+8` 一次读 `0x0c` B；实档尾部 after identity 为 `00000000 | 01 | 4ec43a77`。对应表读循环结束后的 `0xf2ba7f → 0xffa5d0@0xffa602` 读 u32 count（本档 0，无 item transfers），再由 `0xf2baa2` 和 `0xf2bac2` 读 1 和 4 B，合计 9 B；不为尾 dword 自拟语义。表首 count/byte 样本 `0xf2ad00/1f`；`0xf2ba0e` 消费首 selector，COMP writer `0xeb893b/52` 在**当前** body 之前写标记。全游标封口使第一 selector 在 `@13`，client legacy body 在 `@14 + ordinal×127`，`body+126` 非 COMP 字段。b47 `rdui@+114 / duni@+118` 是字节锚标签：原生 `dsha` 为 ordinal，原生 `duni` 为第二 lane，第三 lane 才是 saved `rdui`，本档全与 `duni` 相等。

## 静态链与外层普查

来源：只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。冻结 master SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`；master、`IDA_PROVENANCE.md`、DB_TABLES_BIG 两件与旧 comp 样本对 MANIFEST 核验。本文地址为 **PE file offset**；分片含 VA、原始 bytes 和后继。

- Factory `0xf48b30` rel32 表 `0xf49d38` case 25（格 `0xf49d9c`）→ `0xf49129`，分配 `0x1b0`，`0xf49139 → 0xeb5db0` 构造 `db::COMP`，`0xeb5dd5/0xeb5ddc` 写 vptr `0x14187dcb8`。另一路 `0xf02aa7 → 0xff9910` 传 table 25，`0x3ceb8e2` 存 table type，`0xf02ab4/0xf02abb` 设置 `DATABASE_TABLE<COMP>` vptr `0x14187f6d8`；**两种对象，不合并**。表循环按 `table+0x54` 调工厂，经 `0xf2ba51` 调记录 slot 19；尚不声明已追通 archive opener 实例。
- COMP 真 slot 19 `0x187d350 → 0xed0a40 → 0x3b3f0d0 → 0xeb7000`（主体 VA `0x140eb7a00`）；主 extent `0xeb7000..0xeb7e42` 有 837 条可达指令、114 个条件、0 extent 外边。主函数 54 个直接 `stream+0x28`，51 个对应已观测外层 scalar/标记/count，3 个为另一引用模式 `0xeb7218/0xeb72f8/0xeb7332`；并不等于业务字段数。交付 21 个有界 CFG、3,721 条指令记录（含外置佐证）、376 个条件分支。无法静态定性或未观察的边不写成死边。t01 A3 所称 slot6 含 RTTI 头，等于真实 slot 5 注册器，VA `0x140ebfa40`；A4 保留 67 cases。
- `0xf2ba0e` selector 两档全 0；`0xf2ba38` 的 external mode 经 slot wrapper 转发，由 `0xeb73a0` 控扩展。wrapper 把 arg8 清 0，选择 ordinal 路径。Client 强制 mode 1 首错 row 0 `@129` `vec30` count 16,777,216；server 强制 mode 0 在 row 0 `@128` 误报 identity `(255,4294901760,131071)`。这是档案封口证据，不是实机动态赋值观测。
- Client 51 个外层位置、一个模板；server 25 个条件模板，每行 77–82 个位置，联合 82。`field_slots.json` 的 `execution_index` 是双档模板联合的顺序（不按地址）；各模板的 `sequence` 数组下标是该执行模板内的次序。每槽保留 `(ordinal, absolute, span)` 的全档摘要、首样例、相对 legacy body 的偏移分布；父集合按 count + opaque item 序列计一个逻辑 span。
- Server 独有扩展位于公共 70 B 后、56 B 尾部之前。`vec30` 是 `u32 count + 2N`，本档全 0；`vec18` 不按固定 stride，先读 i32 count，再按每个 item tag 走 8/9 B；本档 32 行非空。`+0xa8/+0xe0` presence 全 0，保留静态分支但无实档 payload 坐标；`+0xe8/+0xc0/+0xc8/+0xd0/+0xd8` 的 payload 分别出现 149/315/366/121/51 行。`+0xe8` 内 item 依 revision 消费 10/11/12 B，`+0xc0` 是外 count 与内 count×12，`+0xc8` 为 25 B，`+0xd0/+0xd8` 现代各 15 B，`+0x100` 为 i16 count×5（另计 count 2 B）。未给这些 opaque 集合、其中的整数、引用或日期强贴 schema 名；不触及独立 subtables 或 t44 `CLUB_LINK`。

## 字段闸门：4CC/成员 → reader sink → 全档域

按 case-sensitive 4CC 与同对象成员对接，**不按 XML 顺序**。54 项有 slot/lane，产生 818 对次序倒置（同一外层槽不强行排序）。例如两个 `duni` XML occurrence 都在前部，但共享最后一个 identity 槽；`ccti` wire 先于 `cnti`，XML 则相反。所有 255 occurrence 各有一条台账。未对齐不等于没有 wire。

**新增 26 项。** `LAUC` (`+0x1a7`, `0xeb7883`) 按 `uoct` 检查，server 7,047/7,047，值 0–5。`cext/cusn/culn` 是同一个 `+0x1a1` byte (`0xeb7610`) 的 bit 2/0/6，由各自 getter 的 `shr/and` 证明；server 真分别 2,327/1,995/0。`culn` 仅观测假，L3 指确定 bit 投影而非已观测真态。

另有 **22 个 `cnst` contract-status 投影**。A block 现代 tag 2，`COMP+0x198..0x19e` 依次 `Pcsp/Pcsk/Pcsf/Pcsr/Pcsb/Pcsh/Pcsy`，legacy `+20..26`。B block 现代 tag 3，`COMP+0x189..0x197` 依次 `Pcjm/Pcja/Pcjc/Pcjy/Pcji/Pcjg/Pcjp/Pcjs/Pcdf/Pcda/Pcdr/Pcss/Pctd/Pchd/Pcsc`，legacy `+28..42`。顶层 local getter 在 `0xec0621` 或 `0xec2c5a` 调相应 helper；分片含精确比较或 bit-test gate、helper rel32 格，以及 `0x433bc2f/32/3b/41` 的逐 byte cursor。两档每字段 7,047 项，均在 scoped `cnst`；观测值为 `{0,1,2,4,6}` 的子集，`Pcsc` 只观测 6（冻结 enum 中是 `-`，不凭空改为自拟哨兵）。结论是该 COMP 本地 getter 的 wire 投影，不覆盖它之前可能处理 4CC 的外部 override。

| 引用字段 | 实际目标 | 每档 live / null / miss |
|---|---|---|
| `ccti` | t5 continent | 6,981 / 66 / 0 |
| `cnti` | t10 nation | 6,769 / 278 / 0 |
| `cpcm` | t25 competition | 3,506 / 3,541 / 0 |
| `cnor`, `csou`, `cwes`, `ceas` | t2 city | 680/6,367/0；671/6,376/0；642/6,405/0；641/6,406/0 |

t2/t3/t5/t10/t21/t25 每档目标分别 56,293 / 84,259 / 7 / 251 / 48,413 / 7,047，按实际逐行 triple 核验。t3 只验 key：client 独立 raw census，server 有序 exact triple 前向最早与后向最迟一致；t10 仅复查 t47 identity 原始坐标。未找到闭合的主行 Club/Stadium 命名引用，不用目标基数或相似值域配槽。`0xffffffff` 与合法 ordinal 0 不混；wrong-UID 控制例：`cpcm` 3,506 live 中仅 29 命中 UID 集，`cnti` 仅 2,687 命中。Continent 目标表有 7 个实际 ordinal，COMP 使用集仍严格为 `{0..5}`，不把使用集当目标全域。

`wbst/wben` 每档均逐日历验证：LE 首 word 低 9 位为 day、高 word 为 year，本档余位均 0；每列有 6,820 个 `(1900,1)`，保持原值，不自拟 null；其余各 227 项。年范围 `1900–2023 / 1900–2024`。`crep` 只在 server，i16 范围 `[0,200]` 无越界；XML 标 `is_client_field` 不推翻具体 reader 的 skip。`levl` 的 getter 明确排除 100、加 1，5,437 live 为 1–12，其余 1,610 是 100；四个 pitch 尺寸按 getter 有符号 `/10` 且非正值不暴露。

**Held 原因与首反例。** `dbty` 的 signed byte 在 `COMP+0xf4`，sentinel `-1` 有 163，`cdbt` 无 30：15 个越界，首 server row 394 `@102218:1e`。`CTty` 首 client row 0 `@32:05`、`PLgn` 首 server `@141:00` 都无 scoped `enum_ref`，保持静态槽不写枚举结论。`CpRp` 首 server `@90:64`，getter 受 context 分支控制。`rdui` 首 client `@136:01000000` 与前一 UID 一致，全部 7,047 条均抑制；byte slot 仍保留。`cnam/csnm/c3ln` 不按邻近值猜字符串槽：row 0 `@28:00` 未进 inline tag 4，且该备选路径只读 `+0x48/+0x40`，不读 `+0x50`。`VARt/HKEt` 的直接分发读规则/context，不能当成 COMP 同对象 wire 绑定；首静态反链见 JSON，未捏造实档坐标。其余 VAR/HKE/集合和未定标量保持 unmapped。原 t01f 的 falsified 记录原样保存在 `field_map.json`，未改旧报告。

## 回归及复跑

- t01f 26 个具名/内部槽与 46 个完整游标步骤（含两段 packed 异常控制与 legacy lookahead）复洽；公共前 70 B 和后 56 B 逐行逐字节跨档一致。冻结 10 组洲/国家夹具、两组 parent 夹具全过：England ordinal 139 → UID 765，China PR 55 → 110；child 707/708 都指 parent ordinal 352 → UID 150990。既有 `crep` 四个样例坐标及各自扩展长复现。
- `verify.py` 独立读取目录、反向数据 DP、重建 PE CFG、重放双档和全域并复核 t01f；不 import builder、ReaderCFG 或 `fm24_dump`。两脚本 `--help` / `--selftest`、全档 build / verify、t01 anchors 7/7。退出码 0 成功、1 核验失败、2 用法或致命错误。未启动游戏/编辑器/IDA，未联网或访问 Z:。

```text
FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t59_compmain_fields.py --build
py -V:3.12 -I -B scratch/t59/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
