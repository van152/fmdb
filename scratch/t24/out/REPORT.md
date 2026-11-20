# t24 — client table_3：逐 transfer 闭合

**状态：`complete_observed_client_row_cursor_partial_off_path_CFG`。** 当前 client member 的 84,259 行均逐 transfer 消费闭合；class 由流中前缀字节决定，不用 ordinal。标准行 84,256 行走 `CLUB`，三个 55 B 行走 `LEAGUE_BODY_CLUB`。主行新增 **10 个 L3 字段**（433 项中 10 项；另有 239 个嵌套 schema occurrence 单独记账）。本结论不外推到 server、旧版本或带扩展业务块的 reader 模式。

## Class、坐标和封口

- t21 的 `50+N+M` 和三条 compact 的跨度成立。**分隔字节归属修正**：旧坐标从第一个业务字节起算，旧“trailer”其实是下条记录的 selector；第 0 行的 selector 位于 member `0x0d`。旧 footer `0x69c66a` 仍是 t21 坐标对账点，但从实际 reader 对齐看，最后一行结束在 `0x69c669`，随后的 9 B 是 `00 00 00 00 | 01 | e3 c0 3a 77`（空向量 count、1 B、4 B）。旧框架把最后一个 count 的首字节当作最后一行 trailer，因而恰差 1 B。迁移 selector 的归属不改变任何行长，也不改变本报告采用的历史业务坐标；selector 在该坐标的 `row-1`。
- 以下地址为 **PE file offset**，VA 和原始指令字节见 `cursor.json` 及 `instructions.part*.json`。loader `0xf2ba0e` 每行先读 1 B，`0xf2ba1b` 将它置入 EDX，`0xf2ba23` 调 factory，`0xf2ba51` 调返回类的 slot 19。case 3 `0xf48daf` 比较 `BL,0x0c`，相等时构造并换成 derived vptr；其余走 CLUB 构造，当前数据其余值均为 `0x00`。三条 `0x0c` 选择的是 **69706–69708 本行**，不是旧 trailer 所在的 69705–69707。旧 ordinal 分段不成立；旧 `+16` 的 5B/4B 假设不是 class split。
- 两条 reader 轨共享 `5 × u32 + 6 B`，后接两个 `u32 length + UTF-8[length]`。`0xe5a900` 受 member version `0x0df1` 驱动，走现代宽度；`0x35b0847` 在长度为零时跳过 payload transfer。名字后走 base helper：`1 B -> object+0xba`、`2 B -> +0xb8/+0xb9`、`12 B -> +0x08`。这 12 B 中第一项与行号一致、后两项 UID 相等；walker 用它们作后置校验，**不**搜索 identity 或以行号选择语法。
- compact 不是空洞：前缀 `0x0c` 后是 derived 的 `4 B@+0x170`（wire `ff ff ff ff`）和 `1 B@+0x178`（wire `00`）。`0x43bec36` 以 `r8=0` 调 CLUB，避免重复调用 base helper；`0x43bec5b` 再尾跳至 base helper（这不是函数内循环）。共享 20 B 为五个 `0xffffffff`，6 B 块为零；名字的两个零长度分别在历史 `row+31`、`row+35`。随后 `1+2+12` B 完成 body。`1+5+26+4+4+3+12=55`；附三行的完整 hex 和轨迹。

## 分支与证据范围

- t21b 记载的 167 个 CLUB 条件、derived 的 3 个条件逐条入表。选定 client 路径 17 条（2 条数据来源、3 条本地状态计算、12 条运行时前提）；其余 153 条为该分支专化未走的路径：10 条有局部上下文/全局谓词线索、3 条有局部计数/参数线索、140 条谓词未解。**未证明为全局死代码**。字符串 helper、base helper 和表 loader 的关键互过程分支另列。
- `0xe5a9ba` 的扩展模式来自调用者（栈参数），**不是** selector，也未从 client 入口独立静态证明为零。数据侧反推：非零边上仅最先的 `1+2+4+1 B` 就超过全部 84,259 行实际在两段字符串后、identity 前的 3 B；零模式的 base helper 和 identity 转移在所有行闭合。流对象非空、成功返回、引用计数等是成功路径的运行时前提，不伪称可从 `.dat` 判定。字符串上界由 reader 的外部全局值提供；本 walker 以 member 边界和后置条件约束实际数据。
- L1：两个独立的流走查、字段列统计、末端和逐行轨迹复算。L3：只读 `editor.exe` 的 factory、slot、transfer、getter 证据；PE 换算用 `scripts/t05_pe.py`。二进制 SHA-256 与登记一致，登记及 schema 快照与 `evidence/MANIFEST.json` 对照一致。不主张 L4。

## 主行字段晋级

以下均为旧业务坐标；derived 对同一 CLUB 业务槽加 5。`N`/`M` 是全名/短名字节长度。四个 4 B 引用是 **fix-up 前的 wire index**，不是被引用对象的 UID；`Cbni` getter 有空引用时回退到 `Cnti` 的路径。

| 4CC | CLUB `row+` | 宽度 | `object+` | 备注 |
|---|---:|---:|---:|---|
| `Cnti` | 0 | 4 | `0xd8` | Nation |
| `Cbni` | 8 | 4 | `0xe8` | Based Nation |
| `Cccn` | 12 | 4 | `0xf0` | Continental Cup Nation；derived `row+17` |
| `Ccty` | 16 | 4 | `0xf8` | City |
| `Csot` | 20 | 1 | `0x160` | mask `0x02` |
| `CASt` | 21 | 1 | `0x161` | mask `0x01` |
| `CnCV` | 23 | 1 | `0x163` | mask `0x01` |
| `Csnm` | `34+N` | `M` | `0xc8` | 零长无 payload transfer |
| `PLgn` | `36+N+M` | 1 | `0xb9` | Player Gender |
| `duni` | `41+N+M` | 4 | `0x0c` | identity transfer 的第二个 dword |

`Cccn@row+8` 保持 E60 negative（55,868/84,259 行与 `row+0` 相等）；本轮证据是**第四次**而非第三次 u32 transfer：`0xe5a877` 的 RDX 指向 `+0xe8`，`0xe5a8a0` 才把 `rdi=object+0xf0` 显式复制进 RDX。`Cnam` 的写入证据落到 `+0xc0`，getter 经过本地化代理，未将底层字符串等同于该 getter。`Clri` 通过 `+0xf8` City 引用再读 city `+0x38`，不是另一个主行槽。t18/t19 的跨子表/继承位点（包括未建立本类 getter 链的 `NDBC/FDBC`）未计入本轮主行 L3。

## 子对象边界

- `subtables.part*.json` 保留 239 个嵌套字段的 schema index、父 4CC 和可证明的表引用；没有分配主行 offset。`Cstc` 归属 t22 有 E56；其 28 个 occurrence 按 t20 候选槽或仅家族证据记录，重复码仍按 schema index 展开。t22 slot 0 / object+`0x18` 是关联 club 的**候选**引用槽；不把 t20 已发现矛盾的候选行坐标晋级。
- `fields_club.part*.json` 里的 `subtable_references` 分开保留 t12/t18 对债务、战绩等表的旧槽位，并附表身份裁定状态。未有可接续证据的嵌套字段，表号/引用槽仍未知；candidate/negative 的归属不提升。672 是 club schema 的总 occurrence（433 顶层、239 嵌套），不是“672 个已各自定位在子表的字段”。

## 交付与复跑

- `cursor.json` + `cursor.part*.json`：逐行位置、selector、长度、UID；根据同文件的 transfer 模板无损重建轨迹。`branches.part*.json`、`instructions.part*.json` 为分片的分支分类和字节证据。
- `fields_club.json` + `fields_club.part*.json` + `subtables.part*.json`：字段台账、全量统计和样本、子对象边界。
- `scratch/t24/out/verify.py`：不导入 builder 的独立复算、静态字节重读及字段抽样/列统计。
- `scripts/t24_club_cursor.py`：builder。Python 3.12；`--help`、`--selftest` 可用。`FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I scripts/t24_club_cursor.py`。
- builder 和 verifier `--selftest` 通过；独立全量 verifier 通过，重读 532 个指令记录；随后 `py -V:3.12 -I scripts/t01_anchors.py` **7/7** 通过。未覆盖 t19/t21/t21b 产物；未启动应用、未联网、未访问 Z:。
