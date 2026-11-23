# t47 — Nation 未知 item-bearing parent：静态发现（partial）

**15 个目标中，9 个已连到内嵌集合及其 reader，1 个完成双档游标验证，6 个未连到 reader。没有发现新的独立子表。`Ntxr` 7/9 字段 L3，2 项 held，L4=0。** 其余 8 个已连 reader 的 parent 都落在同一 `NATIONAL_TEAM_CONTAINER`（owner table type 9）；这些链是静态发现，不是 `table_9` / `table_extra_9` 的分档 wire 验收。

## 静态证据与逐 parent 判定

下文地址为 PE **file offset**。只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。`IDA_PROVENANCE.md` 和 `master.json` 按冻结 `evidence/MANIFEST.json` 核验，master SHA-256 为 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`。指令分片含原 bytes、VA、直接跳转目标；发现 JSON 含 factory rel32 格、COL、TD、vptr 槽和 schema。t37 原报告及 inventory 字节未改。t24 分片未收录本次 `Ntxr` 等 Nation scoped item；仅 `Calt`、`TCrs` 命中未分 Nation scope 的同名 occurrence，不能代替 frozen master 所列 Nation item。

**为什么只查 `NATION` 的 slot 19 会漏。** `NATION` slot 2 `0x1041f30 → 0x1041f40`，无本类匹配时 `0x104330f` 取 NATION `+0x108`，非空才在 `0x1043322` 直调 `0x1065ef0`。独立反向见证：factory `0xf48b30` 的第 9 格跳 `0xf48f12`，构造在 `0x1059a4f/56` 写入 `NATIONAL_TEAM_CONTAINER` vptr `VA 0x1418898d8`。其 slot 2 `0x1065eb0 → 0x3d95190` 先试其 `+0x170` 的 Nation（`R9D=0`），未命中才进同一个 `0x1065ef0`。slot 20 `0x105fc60 → 0x3d885f0` 修复 `+0x170`，成功且目标非空时 `0x3d88644` 将容器写入 Nation `[+0x108 + 8*container[+0xb9]]`；Nation 的上述读取选第 0 侧。未声称 251 条 archive 行的 backlink 均选这一侧。旧版 `≤0x0dc3` 的 slot 19 有额外手工构造 Nation 的写点 `0x105cb99/0x105cba0`；不是现代档运行观测。t9 slot 19 为 `0x105cb10`，按调用上下文的版本及 mode 分叉；下表只证明某个 reader 路径，不将 archive 头等同于进程状态。

| Parent | 精确分发及集合 | backing 判定 / reader 证据 |
|---|---|---|
| `Nntp` | `0x10662de → 0x1078df0 → 0x3db28a0`，容器 `+0xf0/+0xf8`，16 B 内存项 | t9 内嵌，`0x105e264` 读 i8 count，`0x105e2b2 → 0x141caa0 → 0x41ba910` 读 **9 B** 再 append。 |
| `Nctp` | `0x1066276 → 0x10790e0 → 0x3db2b40`，`+0x108/+0x110` | t9 内嵌，`0x105e2e9` 读 i8 count，`0x105e332 → 0x141cb70 → 0x41babb0` 读 **8 B**。 |
| `Nrtp` | `0x1066371 → 0x10793d0 → 0x3db3000`，`+0x120/+0x128` | t9 内嵌，`0x105e369` 读 i8 count，`0x105e3b2` 同一 **8 B** item reader。与 `Nctp` 共 reader，不共 vector 或 count。 |
| `NTRv` | `0x106734f`，helper `0x15d1300 → 0x4496e00`，参数 1 取 `+0x438` | t9 内嵌，`0x105e9ec/0x105ea36`，u8 count 加 i32 array。 |
| `NWGv` | `0x106735b`，同 helper 参数 0 取 `+0x440` | t9 内嵌，`0x105ea6b/0x105eab5`，独立 count 及 array。 |
| `NSps` | `0x106686b`，同 helper 参数 2 取 `+0x448` | t9 内嵌，`0x105eaea/0x105eb34`，独立 count 及 array。 |
| `Ntxr` | `0x1042274`，NATION `+0x60/+0x68`；`0x1043546/0x104355e → 0x104ed80 → 0x3d759d0 → 0x144c160` | t10 内嵌，`0x1040462` 读 i32 count、`0x1040494 → 0x144bca0 → 0x420c8f0` 读 **23/25 B**，全档闭合见下。 |
| `Nfmp` | `0x106748b → 0x10799c0 → 0x3db5170`，`+0x6e0/+0x6e8` 的指针数组 | t9 内嵌，`0x105d99c` 读 i16 count，`0x105d9e2` 分配，`0x105da1b → 0x105f730 → 0x3d86430` 读 **9 B**；第一 lane 符号扩宽成 qword，非零才 append。不是“wire count 等于 UI 行数”。 |
| `NCro` | `0x10660c1 → 0x1078b00 → 0x3db25d0`，`+0x4f8` 可空容器指针 | t9 内嵌，`0x105d8c6` 先读存在门槛，`0x105d97a → 0x105f2b0` 读 1 B tag + i32 count，再每项 **1+4+4 B**。 |
| `Nrvn` | `0x10665a6 → 0x106ad10 → 0x3d95f10 → 0x11e8900 → 0x3eba380` | 过滤容器 `+0x48/+0x50` 中的 16 B 内存项，条件为项 `+0xb == 6`。这不是独立名单或一整条 wire 布局；填充源待追。 |
| `Nftb` | `0x1045b34 → 0x1050d40` | setter 形状的输入分发，`0x1050d90` 扫 `posl`；未证明对称 getter、磁盘 reader 或运行时重建。 |
| `Calt` / `TCrs` | `0x11cf7a1` / `0x11cfa56` 在 Team-container 路径有精确命中 | 只保留候选路径，未证明 Nation getter 转发及存储。不能借 `Tchl` 路径或把 t10 某个未命名数组按词义归给 `Calt`。 |
| `EDfx` / `EDsc` | 未证明精确 getter | `EDfx` 倒序原字节只在 `0x29c39` 命中；`EDsc` 两字节序均未命中。字节扫描不排除计算式分发或资源路径，不能据此宣判两者共用/无存储。 |

Repu 三件共享的是 **owner、外层 reader 和 UI 投影 helper**，不是 backing array。`0x4496fd5` 固定循环 20 次，索引写入临时项；数组指针为空则 helper 置值 0。Reader 的循环上界来自 wire count，并非按 20×4 无条件消费。该反例也否证“repu 必占一个持久化 enum 槽”。Transfer 三件也共享 owner/member reader 但对象集合不同，`Nntp` 比另外两件多一个 byte transfer。`affl` 的冻结类型为 enum，不先验按 club ordinal 扫表。对 t9 的上述路径没有发现独立 item vptr 或 item slot 19；**不能**由子项内存宽度推成员 stride。未完成 t9 按档读游标和实际 target ordinal join，因此不发布 t9 item 的 L3 坐标或档内 item count。

## 双归档（E80）和游标

| 成员 | Client（31 个目录项） | Server（77 个目录项） |
|---|---|---|
| `table_10.dat` | 251 行，24,732 B，变长；`7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34` | 251 行，422,345 B，变长；`19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f` |
| `table_9.dat` | u32 header 251，31,956 B | u32 header 251，307,564 B |
| `table_extra_9.dat` | u32 header 251，83,927 B | u32 header 251，105,228 B |
| `table_extra_10.dat` | 缺失 | 缺失 |

表 9 的 header count 不是 cursor 结果；两种成员都在目录中，**不能仅凭 count=251、class 或目录名称把某个 t9 子段绑定到 sidecar**。两档各成员绝对起点 = `34+entry.offset`，在目录规定的 `packed_size` 和下一成员界内枚举帧，按 `entry.size` 唯一选中，所列成员实际均为一帧。`entry.sha256` 是压缩区实算 SHA（目录解析未供应 SHA），另存 payload SHA。t10 client/server 规范起点分别 `5128013 / 8529015`，压缩长度 `5570 / 197744`。没有把邻成员 frame 当作本成员的 stub。

**t10 完整读法。** factory 第 10 格 `0xf48f27 → 0x103ebf0`，`0x103ec17/1e` 写 `NATION` vptr `VA 0x1418893b8`。loader 在 `0xf2ba0e` 读 selector，`0xf2ba38` 从外部参数转发 mode，`0xf2ba51` 调 slot 19 `0x103fac0`。该 reader 的 `0x103fae6/0x10409d3` 按 mode 跳过或进入扩展段。对这个档对，**server mode 1**、**client mode 0** 都逐行通过；不宣称捕获了实机 mode。server 强制 0 首行 `@38` 得 `-90` count；client 强制 1 首行误走读长，最后在 `@7188` 得不合法的 1,507,845。Client member 存在，只是此读法不执行 `Ntxr` count，不将其写成专表缺失或 251 个持久化零 count。

- PE runtime-function extent：NATION reader `0x103fac0..0x1040be4`，992 条可达指令；tax helper `0x420c8f0..0x420ca6e`，111 条；两个范围均无 extent 外边。字段顺序由 stream vcall `+0x28` 与目的寄存器确认，不用 identity 搜索断行。扩展块其它变长站点仅用来推进游标（i16/i32 count、长度前缀字符串、日期对、14 B 内嵌项），不命名字段，不重复 t46 的全列扫描，也不对 t28 已闭 4 parent 重新晋级。
- Server `13 + 422323 + 9 = 422345`，行长 141–30,993 B；client `13 + 24710 + 9 = 24732`，行长 50–1,199 B。双档各 251 个 selector=0；`legacy14` 对齐改为 `14 + Σrow_len + 8`，legacy 最后一个 byte 借下一 selector 或 footer 首字节。12 B identity 由 `0x1040bcf → 0xfae340 → 0x3c60119` 消费，再验证 ordinal、非零重复 UID lanes 和唯一性，双档 251 组三 lane 一致。Footer `00000000 | 01 | ec7ae404`，最后一 lane 此处等于最大 identity，未外推。
- Server 首行 selector `@13`、税 count `8 @50`，items `[54,254)`，identity `(0,5,5) @633`，下一 selector `@645`。251 行中 221 行含税项、30 行税 count=0；首个零为 row 31 `@17819`。**1,899 个 item tag 全是 `2`，均 25 B**。这不是 selector 或全局版本 gate：`0x420ca3f` 比较每个 item 自己刚读的 byte 与 2。合成首个 tag=1 并删去该项尾随 2 B，得到 1×23 + 1898×25，所有 identity/EOF 仍闭合；只改 tag 不删时，首行随后在 `@252` 读到错误 count。未赋予 tag/尾字节业务名称。

### 五类分支与反例

指令及分支分片对 t10 reader、已跟进的消费 helper 给出可达 census、谓词、taken/fallthrough，另列 t9 目标切片；t9 全 CFG 已取，但**没有**把局部谓词分类当作 t9 全路径模型。没有执行真实 allocator/refcount 或模拟编辑器状态。

| 类 | 证据 / 首反例 |
|---|---|
| `wire_data` | `0x1040485/0x10404b2`：税 count 0 跳过，首行 8 次 item；`0x420ca3f`：item tag 1 缩短 2 B；`0x420ca66`：ppty=0 写成 1，不消费额外 byte。 |
| `runtime-external` | `0x103fae6/0x10409d3` mode，不是 selector，错 mode 见上。字符串/数组长度 guard 比较 runtime 限制与 wire 长度，不拿限制当数据。 |
| `IO-result` | 各 stream 状态、helper AL 或 out-status；`0x420c93a` 的短读控制将首税 count 改为 1 并截断到 `@58`，`@55 w4` 不足，不能解释为另一布局。 |
| `context-lifecycle` | reserve/append、TLS、refcount、callback。`0x3c60100` 的假想 null stream 跳过 identity transfer，不能视为成功的有效档行；正常已读取 `@633 w12`。 |
| `dead` | 如 `0x104094a` taken 需要紧邻 `xor eax,eax; test al,al` 的 AL 非零；date thunk null 边落入 null 解引用，只在有效读取语境排除。未观察不等于死。 |

## Ntxr 字段三重闸门

每项在 frozen `nation.xml#nation` parent idx 232 内恰有一个 occurrence；同一 24 B 对象经 `0x144c160` 按精确 4CC 读取，并在 `0x420c8f0` 找到同一 displacement 的 per-item sink，再验全部 1,899 个 wire items。下表是 **item 相对偏移**，父行坐标要经 count/当前 cursor 求得；没有 t10 全表固定行偏移。

| 字段 | item / 对象 offset | 全表判定 |
|---|---|---|
| `lowa` | `+1 / +0x04` i32 | **L3**，0..11,037,528，符合 XML cash 范围。不推币种或倍数。 |
| `uppa` | `+5 / +0x08` i32 | **L3**，0..11,037,527。 |
| `capa` | `+9 / +0x0c` i32 | **L3**，0..132,334；getter 负值缺失，实档没有，0 不删。 |
| `year` | `+13 / +0x10` u16 | **L3**，1900..2028；`movzx` 整数年，不是 packed date。 |
| `ppty` | `+15 / +0x12` i8 | **held**，XML 无可指认 `enum_ref`。raw 0..5，99 个 0 在读后改 1，首 row 48 `@29265:00`；getter 不能直接显示 raw 0。 |
| `txty` | `+16 / +0x13` i8 | **held**，也无独立 enum 域；首 row 0 `@70:04`，全档 raw 1..11 内若干值，不猜标签。 |
| `perc` | `+17 / +0x00` f32 | **L3**，0..60；`movss` 装箱，符合 XML [0,100]。 |
| `fram` | `+21 / +0x14` i8 | **L3**，57 个 live 1..5；getter 测有符号 byte `≤0` 缺失，首 row 0 `@75:00`，共 1,842 次。 |
| `leve` | `+22 / +0x15` i8 | **L3**，19 个 live 0..5；getter 负值缺失，首 row 0 `@76:ff`，实际 −1 计 1,880 次。0 在此域是 live，不与 `fram` 共享哨兵。 |

闭合的 tax 子项不含 ordinal 引用、布尔字段或 packed date 字段；未对仍未闭合的 Nation parent 以值域相似代替真实目标表 join、bitmask 或 enum 域核验。下一步优先绑定 t9 主表/sidecar 各自的 reader 路径与 mode，再对 transfer/repu 和 `Nfmp`/`NCro` 做逐行 EOF、target ordinal 等闸门；6 个未连项的首条路径或字节负例保留在 discovery。

## 复验

`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`，`py -V:3.12 -I -B`。`scripts/t47_nation_unknown.py --build` / `--selftest`，`scratch/t47/out/verify.py` / `--selftest` 和两者 `--help`，`scripts/t01_anchors.py` **7/7**。独立 verifier 不导入 builder、`ReaderCFG` 或 `fm24_dump`；独立 frame 边界、PE 工作队列和 struct 解码检查原字节、坐标、域和 held。退出码 0/1/2。未启动游戏、编辑器、IDA，未联网，未访问 Z:。
