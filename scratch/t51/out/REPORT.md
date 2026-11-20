# t51 — Nation 六个 unknown parent：静态反查（partial）

**3 个 parent 绑定归档成员：`Nrvn`、`Calt` → `table_9.dat`，`Nftb` → `table_10.dat`。`Nrvn` 2 项、`Nftb` 4 项通过 L3；`Calt` 2 项无实档 item、`Nftb` 3 个引用未通过 ordinal 闸门，均 held。`TCrs` 已追到 getter 所用集合和填充 reader，但尚未绑定具体成员；`EDfx` 找到精确 UI 分发，`EDsc` 仍未找到代码路径。L4=0。**

## Owner 从 `this` 判定

所有地址默认是 `editor.exe` PE **file offset**，VA、原 bytes、指令与直接目标均在 JSON。只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。冻结 `master.json`（`7d57477e…`）与 `IDA_PROVENANCE.md` 对照 MANIFEST；t37 inventory `8af89c72…`、t37/t47 的原文与六条原 JSON 项逐条保留。这里的 `TEAM_CONTAINER` 是基类，不是 table type 24 的 `TEAM` 对象，也不是说所有实体只存在一份集合。

- **NATION 入口**：slot 2 `0x1041f30 → 0x1041f40` 保存 `this=R12`，`0x104330f` 取 NATION `+0x108`，`0x1043322` 将它传给 `0x1065ef0`。t9 slot 2 `0x1065eb0 → 0x3d95190` 先试 `+0x170` 指向的 Nation（禁止递归转发），失败时以原 t9 `this` 进同一 `0x1065ef0`。原 `0x3d88644` 有条件地将 t9 写回 `Nation+0x108+8*[t9+0xb9]`；未主张所有档行取 index 0。`0x10685d9–e1` 用同一 `RDI` 转入 `0x11f0690` 基类 getter，`Calt`、`TCrs` 的精确 4CC 都命中。setter 路径独立互证：NATION slot 3 `0x1045300 → 0x3d61fc0` 的 `0x3d61fd8/0x3d61fe9` 将 `+0x108` 送入 `0x1063530`，再 `0x10647d7 → 0x11f4570 → 0x11cf6e0`。t47 两组候选 sites 中这两段是**输入分发**，不是 getter。
- **TEAM 对照**：试过 t39 锚点 `0x11b0f6c → 0x15e9830 → 0x44d7bf0`，其 `0x44d7c6a/71` 取全局 `VA 0x141b60158` 所指表的 `+0x80`，后续按 Team owner 筛选；它不是这里两条 4CC 所达的对象局部 vector。当前证明的是 Nation 请求下的 owner 和基类共享机制，不从同名 schema 推导独立 TEAM/t24 集合，也不把 club 路径纳入验收。
- **工厂**：`0xf48b30` rel32 表 `0xf49d38` 第 9 格 `0xf49d5c → 0xf48f12`，经 `0x1059a4a` 调基类构造 `0x11d01c0 → 0x3ea1420`，`0x1059a4f/56` 覆写 `NATIONAL_TEAM_CONTAINER` vptr `VA 0x1418898d8`。第 10 格 `0xf49d60 → 0xf48f27`，`0x103ec17/1e` 写 `NATION` vptr `VA 0x1418893b8`。独立验证 rel32、COL/TD、slot 2/3/19 原字节。闭合路径的子项是内嵌值或池分配的非多态对象，未找到独立 item vptr/factory case；只有外层成员绑定。

| Parent | 正向证据及边界 |
|---|---|
| **Nrvn** | `0x10665a6/0x10675f0 → 0x106ad10 → 0x3d95f10 → 0x11e8900 → 0x3eba380`。输入是 t9/base `this`，不是 NATION；`[+0x48,+0x50)` 每项 16 B，`item+0xb == 6` 选入输出 view。独立反向：t9 slot 19 `0x105cb10` 的 `0x105ef06/12` 把同一 `this` 传给 `0x11d0d30`，`0x11d1b03` 刷新 u8 count 后以 `this+0x48` resize，`0x11d1b98/9c` 将真正的 16 B item 作为 pending transfer，后续通过 `+0x28` vcall 刷出。`0x11d1b91` 是 coalesced flush 站点，不能把它当成每项一次实机调用。 |
| **Calt** | `0x11f139a → 0x11f21b5 → 0x11ff710 → 0x3ecc060` 读取 t9/base `+0xa8` 可空指针数组，`0x3ecc286` 逐非空指针交给 `0x11fd060`。`0x11cf7a1 → 0x11fc730` 的 setter 查同一 `+0xa8`。reader `0x11d1bf2` 读 i16 count；`0x11d1ca7` 写 `this+0xa8`，每项传输 `4+4+8+2+4+4+1+1=28 B`，`0x11d1fbb` append。并非某个 NATION 未命名数组。Server 251 个 count 都为 0，首行 `@1097:0000`；client 直接绕过 count，未发布验收字段坐标。 |
| **TCrs** | `0x11f15ab → 0x15634b0 → 0x4391e40` 保存 t9/base `this` 到 wrapper `+0x18`；`0x11f3e37/44/54` 从 `[this+0xb0]+0x48` 取 vector。`0x11f40d8` 投影，`0x4387250` 生成四个 PUn* key，`0x155a320` 走减法/rel32 dispatch。setter `0x11cfa56 → 0x11fbb40 → 0x11e9970 → 0x3ebb830` 对同一 vector 分配 12 B 项（池 VA `0x141b5e150`）。反向 `0x11d3200` 分配/取 `+0xb0`、`0x11d4bad` 写扩展对象 `+0x48`，再 `0x11d4bfe → 0x155b450 → 0x4387ab0 → 0x155c120`（同一池）。外层 `0x3b94c5d` 或 `0x3bb97ec` 从对象表取 ordinal 的 `this`；`0xf51665/71` 取 context `+0x60` table，`0x3bb9698 → 0xffa3b0 → 0x3cefbe0` 以 R8B=1/R9B=0 拼 `table_extra_` + `[table+0x54]` 的数字，`0x3bb96d6` 按 `.dat` 打开。主档路径 `0xf4e131 → 0xf2d810` 对同一 context slot 选主名称，`0xf2dbd0/d3` 以该 table ID 走 factory。**`table_extra_9.dat` 是目前有命名链支持的候选**，没有将 ID/mode/双档 EOF 判成正向绑定。**反例**：已绑定的 t9 主 reader 在 `0x105dd63` 也调此 item reader，**但 `0x105dd56` 写 `this+0x188`**。Server presence 为 0/1 共 166/85 行；row 0 `@673:00`，row 1 `@1726:01` 后确实消费 308 B。即使 wire 结构一致，也不能把 `+0x188` 直接认作 `[+0xb0]+0x48`。不主张两者绝无迁移/别名，不发 `PUnP`、`ftjn` 或 bool 的实档结论。 |
| **Nftb** | `0x104536b` 保存 NATION `this`，`0x1045b34 → 0x1050d40` 是 typed-property import，受 global `VA 0x141b60320` gate。`posl` arm `0x1050e7d → 0x15d07b0 → 0x44929b0` 从 `VA 0x141b5f1b8` 分配 56 B，再 `0x104b6f0 → 0x3d6beb0` append 到 **NATION `+0x170` 所指 vector**。同源 item 投影 `0x10512c0 → 0x3d78450` 取该 vector，`0x3d78561 → 0x1051580 → 0x3d78720 → 0x10728c0` 逐子项按精确 4CC 装箱；未证实 NATION slot 2 有精确的 `Nftb` 父显示分发。t10 reader `0x104011f` 读 i16 count、`0x104012c` reserve 同 vector、`0x1040199` pool/宽度一致、`0x10401dd → 0x15cf370 → 0x448f890` 填项再 append。**`debug_only` ≠ 不持久化**：server row 162 `@278809:0700`，真实 7 项。旧 t9 `≤0x0dc3` 另有 `0x105d80c/13` 经 t9 `+0x170` 解到 **Nation** 的 `+0x170` 并复用 item reader；不是第二个现代持久化集合。 |
| **EDfx** | 原 raw 命中 `0x29c39` 实为 **可达** `0x29c37 cmp esi,0x45446678` 的立即数。`0x28166/6b` 分开保存选中的对象和 UI 上下文；`0x29c66/69` 要求 selected record table type **10**，`0x29c80 → 0x907f0` 以 UI context 和 NATION 为不同入参构造结果。`0x9082e` 用 UI context `+0x1c0`；`0x909d9 → 0x103f9f0 → 0x3d5c091` 取 Nation backlink，`0x90a24` 以 runtime 日期/上下文生成结果。`type=24` 走拒绝边。**已证此视图生成路径，不是证明所有输入或派生数据都不持久化**：没有正向 archive opener/record sink，不赋厂表或字段坐标。 |
| **EDsc** | 两字节序零命中；冻结 schema `allow_add=false, allow_remove=false`，同一 code 另见 `advanced/database test/comp test.xml#cpts`。这是“不凭 Nation 层名声称有 Nation backing”的首反例，不是 UI-only 的静态定论。无已验 `this`、opener 或 cursor。`day_of_week`、`nstr` 与 date 均未映射。 |

## 双档归档与目标游标

E80：目录项数 client/server **31/77**，从 `34+entry.offset` 开始，在当前 `packed_size` 和下一成员起点内枚举真实 Zstd 帧，按 `entry.size` 唯一选择。`entry.sha256` 是压缩区 SHA；另存 payload SHA。下表括号内为绝对起点和压缩 B。`table_extra_9.dat` 双档存在但**未分配给 TCrs**；t49 两种 slot 19 模式的原拒绝逐条引用（首行 `@1189` i8 -1 或 `@28` 762536805），它们不能反驳尚未闭合的扩展 reader。双档无 `table_extra_10.dat`。

| Member | Client | Server |
|---|---|---|
| `table_9.dat` | (5133583,10752)，251 行变长，31,956 B，`784810f0…` | (8726759,82354)，251 行变长，307,564 B，`6c2d8a06…` |
| `table_10.dat` | (5128013,5570)，251 行变长，24,732 B，`7e9d740b…` | (8529015,197744)，251 行变长，422,345 B，`19337841…` |
| `table_extra_9.dat` | (5144335,17352)，83,927 B，`2717052d…` | (8809113,28845)，105,228 B，`a5671537…` |

`0xf2ba0e` selector 前置，`0xf2ba38/51` 转发外部 mode 再调用 slot 19。沿用 t47/t49 已验的 **client 0 / server 1**，不把 mode 当档内 selector。PE exception extents + `ReaderCFG`：t9 `0x105cb10..0x105f040` / `0x11d0d30..0x11d24ce` 为 2,141/1,508 条可达指令；t10 `0x103fac0..0x1040be4` / item `0x448f890..0x448f9b5` 为 992/83 条。`TCrs` 扩展 reader `0x11d3200..0x11d4dd3` 为 1,466 条，子 reader `0x155c120..0x155c661` 为 334 条，发布的是目标分片及直接 CFG，不宣称全间接分派已解。

非目标段复用 t47/t49 冻结边界、逐行 hashes；不解码此前的 8 个 t9 parent。Nrvn/Calt 从目标 count 站点向前消费到 identity，Nftb 从行首推进两段 opaque vectors，再走变长 item，结束与下一已验站点前的 24 B 固定转移一致。后置校验 identity 的 raw `(ordinal,uid,uid)`、非零重复 lane、unique UID，251 行双档逐条一致。绝对坐标同时可减 `wire13`（selector 起点）或 `legacy14`（body 起点）；legacy 最后 byte 借下一 selector/首个 footer byte。Footer 四份均 `00000000 | 01 | ec7ae404`（count=0、flag=1、末 u32=82,082,540，恰等于实档 max identity）。Client mode 0 不执行本次三个 target counts，不能说写了 251 个零。Server Nrvn 194 个非空 row，720/720 项均为 `(kind,tag)=(2,6)`；Nftb 仅一个非空 row，7 项 tag 1、长 46–54 B。

## 三重闸门、首反例和边界

- `Nrvn.nati`：冻结 parent 216 内唯一，item getter `0x1106bfd`、源对象 `+0` 的 `0x11071ce`；`0x110586b` 的 kind 2 rel32 cell 与 fixup `0x11d2aa9`、`0x1105906/0x11059cf` 连到对象解析（旧版转换有附加 category 判定）。实档 i32 在 16 B 项 `+0`，位于 8 B 传输低半部，实读高半部为 0；720/720 命中真实 t10 ordinal。首 row 0 `@1017=29` → UID 34；当 UID 查则给 ordinal 24（错指对象）。强行 UID join 另有 **446 miss**，首 row 7 `@8234=162`。
- `Nrvn.leve`：`0x1106de9/df5` 精确分发并 `movsx` 读取同一对象 `+0xc`，16 B 直接 item sink 对应 wire item `+12` i8。720 项 5–100，XML 0–100。首 `@1029=90`；变更 tag 6→5 只影响 view，不改变显式 16 B 消费。
- `Calt.cmid/stid`：冻结 Nation parent 235 仅这两项；不把同名 nested 额外字段合并进 scope。`0x11fd28a → 0x11fd44e`、`0x11fd34d → 0x11fd503` 与 `0x11d1e86/e65` 给静态候选。client 的真实 t25 7,047 个 competition、t21 48,413 个 stadium ordinals 只作目标基线；server Calt **0 live，不执行目标 join**。合成 count=1 并插 28 B 只证明采样路径跨度，不用于晋级。
- `Nftb`：变长 item `tag u8 + 4×(u32 byte length + bytes) + packed date 4 + 4×i32`。唯一 XML occurrence、精确 `0x10728c0` item 分发、同 displacement reader sink 逐项对上。`NpFn`（字符串 0）、`NpSn`（1）、`NbCn`（3）及 `NbPd`（四串后 date）L3；字符串 2、另一个 i32 不命名。`NbCn` 实档均 0 长（首 `@278840`），L3 指静态长度站点，而非已观察非空公司名。出生日期是两 LE u16，按 `0x107298c` 装箱 `(year<<17)|((word0&511)<<8)|(word0>>9)`；首 `@278844 2700b607`，不是 u32 年或 Unix 时间。
- **Nftb 引用 held**：`NbPi` live 6/6 命中 person 身份值、实际 ordinal 只 2/6；首 `@278906=83212659` 非序号，UID 对应 person ordinal 360386。`NbPn` live 7/7 命中 Nation 身份值、ordinal 0/7；首 `@278852=788` 指 UID 788 / ordinal 162。`NbFt` 七值落入真实 **client Club** ordinal 域，但首 `@278848=1489` 按 ordinal→UID 1967，按 UID→ordinal 1106；`0x3daad0d/10` 取目标 `+0xc` 写入，`0x1072b34/4c` 用标识查找，**数值域重叠不通过 ordinal 闸门**。三者均不以 UID 反查代替晋级；person 只读基础 identity，不读 PDxx；club 只用已有 t24 行尾身份。

## 五类分支与复验

`branches.part001.json` 逐条存 predicate、taken/fallthrough 和首反例/静态对照；这不是全 CFG 分支归因。

| 类 | 首例 |
|---|---|
| `wire_data` | `0x11d1b0f`：首 rival 空行 row 1 `@2269:00`；`0x1040144`：首 takeover count `@24:0000`；`0x155c378/3f3` 的 TCrs tag 闸门变宽，未当作 archive 绑定。 |
| `runtime-external` | `0x11d0fa4` 的 mode 0 绕过 t9 两 count，双档 selector 都是 0；`0x1045b14` 的 property gate 不控制 t10 reader。 |
| `IO-result` | Nftb 首实项在 `@278816` 缺 5 B 字节内容时拒绝；`0x448f8d3` 是 out-status，非第二种有效布局。合成的 Calt/TCrs 短读对照与真实观测分开记。 |
| `context-lifecycle` | `0x11d1b88` null stream 跳过 pending transfer，后续 identity 同样不可读；`0x29c5a` null selected object 不会进入 UI 类型检查。 |
| `dead` | `0x3eba542` 的 taken 要求紧邻 `xor eax,eax; test al,al` 的 AL 非零，矛盾；不是仅因实际未命中。 |

`FM24_DB_DIR=<WORKSPACE>/scratch/data`，`py -V:3.12 -I -B`：builder、独立 verifier、两者 `--help`/`--selftest` 均通过；`t01_anchors.py` **7/7**。独立 verifier 不导入 builder、ReaderCFG 或 `fm24_dump`；独立工作队列复核 PE extent/边、按大小选帧、目标跨度、实表身份与首个错误 join。只在 t51 写入；未启动游戏、编辑器、IDA，未联网或访问 Z:。

**剩余**：绑定 TCrs getter 所用扩展读路径的具体 member/mode 并区别主档 `+0x188`；Calt 等实档出现非零 count 后再试 join；Nftb 父精确显示分发与引用编码不升级；EDfx 的上游持久化来源、EDsc 的实际 UI/资源调用链仍未封闭。
