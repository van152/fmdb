# t32 — Cmti / table 43 月供子表静态 cursor

**Server 535 行 × 46 B 全闭合；client 无 table 43。6 个 scoped occurrence 中，4 个固定坐标 + 1 个上下文条件坐标晋级 L3，1 个 held，L4=0。** `club` 是按当前俱乐部选取的对手方，不能上报为一个固定偏移；`icom` 也是视角派生值，没有独立存储槽。这不是按行数或数据分布给字段命名。

## 归档和边界

| Archive | 目录条目 | 成员 | Count | Stride | 解压 payload SHA-256 |
|---|---:|---|---:|---:|---|
| client | 31 | 不存在（不是空表） | — | — | — |
| server | 77 | `server_db/table_43.dat` | 535 | 46 B | `7981267028706e701d39a32126b5b2e85f9b4973266cf1545f09869a524a069e` |

Server 目录项 offset `24766564`，Zstd 首帧 offset `24766598`，packed size `8796`，version `0x0df1`。`load_payload` 首帧已解得完整 `24632 B`，首帧不是 E66 式空 stub；帧地址也等于 t29 `packed_offset`。核对两 archive 的 SHA、全目录条目数、成员元数据；直接消费 t29 profile / `.rows.jsonl`，比对全部 535 行旧坐标原字节、row block SHA 与使用槽的 unsigned 统计，不重 dump。t29b `subtable_inventory.json` 已消费：核对其 Cmti 页的 table、archive、RTTI、reader、idx 范围与 profile/rows 哈希；保留原 `link_status=candidate`，不使用候选栏位投票晋级。

- Wire：`13 + 535 × (1 selector + 33 properties + 12 identity) + 9 = 24632`。按 CFG read site 推进后才归纳 stride。第 `i` 行 selector `13+46i`，body `14+46i`，行尾 exclusive `59+46i`。全表 selector 为 0；loader 消费并传入 factory，case 43 不检查它。注入 selector=1 是 replay 观察域拒绝，不是 native factory 拒绝。
- Legacy：`14 + 535 × 46 + 8 = 24632`。业务 wire 坐标 = legacy + 1；legacy `+45` 借用下一行 selector，末行借 footer 首字节。
- Identity bulk 在 legacy `+33` / wire `+34` 落对象 `+0x08..+0x13`。原始 lane0 是 `0..534`，后两 lane 相等非零（数据中 535 个 distinct，1..535）；先以流数据执行本机阈值谓词，再校验原始 lane，不能让 ordinal overwrite 掩盖错误。
- Footer 从 `24623` 开始：`00 00 00 00 | 01 | 17 02 00 00`。`0xffa602` 读 vector count，本档为 0，跳过逐元素三次 4 B 读；外层 1 B 到 `table+0x58`、末 4 B 到 `table+0x50`。末 u32 `535` 同时等于 max UID 和行数，**不足以区分语义**；控制行循环的 count 是头部独立 u32。

## 静态链及分支

只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`，对照 `evidence/fm24/reports/qa/IDA_PROVENANCE.md`。冻结 `evidence/fm24/reports/editor_schema/master.json` SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`；两份快照与 `evidence/MANIFEST.json` 一致。除明确标注外，下面的地址均为 PE **file offset**，对应 VA 与原始 bytes 见 `instructions.part*.json`。

1. Factory `0xf48b30`：rel32 表 `0xf49d38` 第 43 格入 `0xf49675`；`0xf496a2 → 0xf496a9` 写 vptr VA `0x141883a68`。COL `0x18859c0` → TD `.?AVSTARTING_MONTHLY_INSTALLMENT@db@@`。
2. Slot 19 VA `0x14153d0a0` / offset `0x153c6a0` 是 leaf thunk。属性 reader `0x4370860..0x43709c6`（VA `0x1444dbe60..0x1444dbfc6`，末地址 exclusive）：118 条可达指令、26 块，6 次直接 stream `vtable+0x28`，宽度 `8,8,8,4,4,1`。成功处 `0x43709c1 → 0xfae340`（leaf thunk）→ `0x3c600f0..0x3c6016e`（VA `0x143dcb6f0..0x143dcb76e`）：43 指令、11 块，真正 12 B read 在 `0x3c60119`。两个 extent 均由 PE `RUNTIME_FUNCTION` 定界；唯一 extent 外 CFG 边是真 tail-jump，已追完。
3. 属性 reader 和 identity tail 无 caller mode 谓词：loader 写的 stack mode byte 未读取；R9 保存/转发，callback 前写 `r9b=1`，不以其值选读法。属性末尾清 R8D，identity 重新从刚读 lane 0 取 R8D。无需 mode fork；getter 的当前俱乐部上下文与 reader layout 无关。

| 谓词来源 | Reader + tail / 外层切片 | 证据与首个反例 |
|---|---:|---|
| `wire_data` | 4 / 5 | `0x4370896/0x43708df/0x4370928` 检查三组 8 B key 的第二 i32：非零直过；为 0 时复制第一 lane，不多读 1 B。全表非零；首行依次把 lane1 置零（绝对 `18/26/34`）均复验复制且行尾仍 `59`。`0x3c60131` 比较新读 lane0 与 `10000001`，首行注入反例 `row 0: identity @47 raw=(10000001, 1, 1), stored ordinal=0`。外层为 count/循环与 footer vector count。 |
| `runtime-external` | 0 / 1 | `0xf48b3b` 为 directory 传入 table type 的 factory 上界；首行 type=43，不是读入 selector，也不是 body mode。 |
| `IO-result` | 6 / 11 | 前三个属性读先保存 `stream+0x10` 再 release、测 EBP；后三个直接测 status；非零汇合 `0x437099e`，AL=false。首个短读 `row 0: short transfer @14 width 8 site 0x437088f; IO-result -> 0x437099e (AL=false)`。Identity bulk 无即时 status 检查；`row 0: short transfer @47 width 12 site 0x3c60119; no immediate native bulk status test` 仅声称 replay 拒绝。 |
| `context-lifecycle` | 10 / 3 | 属性三组各有 stream-null 和 refcount 边。Null 边跨过 transfer 后仍在 `0x437089e/0x43708e7/0x4370930` 解引用 null（首行反例），不是可选布局。Tail 四条为 stream/null callback/release/refcount；callback 用 caller stack 的 table this。以 live stream/retained owner 为模型前提，callback 与终析构不展开，无真机观测。 |
| `dead` | 0 / 0 | 不因观察域没有走某条边就删 CFG 边。Null/最后引用/非零 vector 等边照列，不当成另一套有效行宽。 |

`branches.part*.json` 逐条记录谓词、来源、前驱证据、两个后继、实测数据上的 replay 次数（仅 reader/tail）及反例或外层约束。`cursor_cmti.json` 存两套坐标、row template、五条样本、逐行 trace 摘要及合成负例。

## 三重闸门与 6 项台账

冻结 `club.xml/Cmti.list_item_fields` 与 t24 的 nested idx **213–218** 一一对应。Club 的 `Cmti` 分发 `0xe842b3 → 0xe831c5 → 0xe57de0`，`0xe58339` 调 `0x1523b10`，以当前 club 的 identity pair 过滤子项 `+0x20` **或** `+0x28`，不是给某个单独槽硬指派 parent。该 arm 的 list helper `0xea12d0` 调到同一类 slot 3 (`0xea14d6` → `0x153ce50` → `0x4371980`)；slot 2 getter VA `0x14153d380` 用从 EDX 复制的 ESI 分发精确 4CC。台账记录每个 getter route、对象 offset 与真实 wire sink。

| 4CC | 对象 | Legacy / wire | Width | 全表画像与等级 |
|---|---:|---:|---:|---|
| `icom` | 依赖 `+0x28` 与当前 club | — | — | **held：无独立 sink**。匹配 `+0x28` 时返回 1，否则 0；setter `0x4371b18..0x4371b24` 可交换两端 key，不写方向字段。不命名 0/1 的 UI 标签。 |
| `play` | `+0x18` | `+0 / +1` | 8 | **L3**。两个 `i32` 串成 person record key；535/535 命中实际 class-2 target identity。没有 `-1/-1` null 或第二 lane 0。 |
| `club` | `+0x20` 或 `+0x28` | `+8,+16 / +9,+17` | 8 each | **L3 条件坐标**。当前 club 与 `+0x20` 相同（原 pair 或解析结果相同）时返回解析后的 `+0x28`，否则返回 `+0x20`。两个槽分别 535/535 命中 club identity；均无 `-1/-1` null 或 lane1=0。未给单一 `row_offset`。 |
| `cash` | `+0x34` | `+28 / +29` | 4 | **L3**，`i32`，1041..3861111，通过 XML `[0,1000000000]`；不推断币种、缩放或显示转换。 |
| `mths` | `+0x30` | `+24 / +25` | 4 | **L3**，`i32`，2..84，通过 XML `[1,100]`。 |
| `pyiv` | `+0x38` | `+32 / +33` | 1 | **L3** 坐标与 signed `i8`（getter `movsx` 与 slot 3 低字节 store），`{1:8, 6:11, 12:516}`，未见 `0` / `-1`，无 getter sentinel 测试。冻结 schema 无 `enum_ref`，画像只证明观测集合，不主张完整枚举域或 UI 标签。 |

### 引用不是 ordinal：先实测并保留负例

本类 slot 20 直接 `AL=true; ret`，没有像 t31 那样的 ordinal→指针 fixup；slot 21 直接发送 `+0x18..+0x2f` 的六个原成员。`play` getter `0x153ca17` 以 `Pers` 标签进入 `0xfe68b0`，取同一成员的两 lane；boxing 对负首 lane 走缺失分支，原始 null 以构造器的 `(-1,-1)` 记账，不把 0 当成 `-1`。`club` 的 setter 从目标 `+0xc/+0x10` 建 key、第二 lane 为 0 时回退首 lane，getter 的 `0x3bf0bc0` resolver 比目标 `+0xc/+0x10`，不是 `+8` ordinal；保留 alias lookup 的静态路径，不声称复刻外部上下文解析器。

从本地镜像重读实际目标 ordinal 集与 identity lanes（仅为 Cmti 引用验真，不解析其他表的字段）：basic_people 658011 条，含 class-2 key 476158；client table3 用 t24 已闭合行尾重取 84259 个 key。**实测 ordinal 假说冲突并保留**：`play +0` 535 个 miss，首个 row0 值 `(29175064,29175064)`，实际 join 到 person ordinal `174166`；`club +8` 19 个 miss，首个 row10 `(3800256,3800256)`；`club +16` 39 个 miss，首个 row69 `(5110769,5110769)`。这不是把真实 ordinal 引用换成 UID 来提高命中：writer/getter 与 resolver 已证实本类实际传的是成对 identity key；它们在相应目标表的实际 identity 集均完整命中，不靠数值落在范围内作证。

**首个 held 反例**：同一 row0 原始字节不变，当前 club key `(671,671)` 则 `icom=0` 且 `club` 取 legacy `+16` 的 `(630,630)`；当前 key `(630,630)` 则 `icom=1` 且 `club` 取 legacy `+8` 的 `(671,671)`。535/535 行的两端均不同，可从两端重放这个视角选择；不能把任意一个 byte/bit 指作 `icom`，也不能把 `club` 固定到任一端。没有 scoped `i16`、独立 wire bool 或日期字段，不做掩码/packed day-year 猜测。

## 复验

`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。`py -V:3.12 -I -B scripts/t32_cmti_cursor.py`、`py -V:3.12 -I -B scratch/t32/out/verify.py` 均 PASS。独立 verifier 不 import builder 或 `ReaderCFG`，从原 PE 重建可达图，从归档复算 cursor/反例坐标/目标域/全表画像，并逐行对比 t29。两脚本 `--help` / `--selftest` 均 PASS，退出码 0 成功 / 1 检查未过 / 2 用法或致命错误。`py -V:3.12 -I -B scripts/t01_anchors.py` **7/7 PASS**。未启动游戏、编辑器、IDA，未联网或访问 Z:。
