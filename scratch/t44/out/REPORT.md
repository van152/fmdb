# t44 — Cafl/Cvfl 共用 `club_links.dat`

**发现闭合：两视图读同一个 `CLUB_LINK` 集合，磁盘来源是具名辅助成员 `server_db/club_links.dat`，不是数字 `table_type`，也不是 `table_3.dat` 的内嵌行段。** Server **9,261 × 47 B** 全闭合；client 无该成员。`Cvfl` 会从同一集合制作副本并计算 `clfr` 验证结果；静态路径不只保留通过验证的项。Cafl **26/29 L3**，Cvfl **16/19 L3**（按 scoped occurrence 计；两者共享字段不当作独立 wire 槽），L4=0。

## 静态链：为什么 t35 扫不到

只读 `<OLD_REPO>/input/editor.exe` SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`，由冻结 `IDA_PROVENANCE.md` 对照；master SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`。两者及旧 `DB_SERVER_TABLES.md` 均按 `evidence/MANIFEST.json` 核验。旧报告已经列出该具名成员，但留在 `unresolved_auxiliary`；本次以双向代码链和原始档补齐语义。以下地址为 PE **file offset**；对应 VA 和原始 bytes 在指令分片（CLUB 的 COL、TD、slot2 指针、`.dat` 与 `CLUB_LINK` 池名原字节在 discovery）。

- **Cafl**：`CLUB` vptr VA `0x14187cd08` 的 slot 2 → `0xe89a00`，`0xe8b4db/0xe8b4e1` 精确匹配 `Cafl`；`0xe8f13d → 0x15320b0 → 0x43637a0`，传 `R8D=0`。`0x436385d/0x4363864` 读当前 club `+0x118/+0x120`，每 8 B 一个指针。`0xe95720 → 0xe95a7c → 0xe95aa8 → 0xeaeb80 → 0x3b0e140 → 0x15261e0` 继续到同一项的字段分发。非 `serv` 特殊支路下 helper 会排序，并计入前置的 4..8/20 类型；Cafl 枚举器从该起始索引继续，而非无条件重放磁盘顺序。
- **Cvfl**：`0xe8c1e8` 精确匹配 `Cvfl`，先比较当前 club `+0x118/+0x120`；`0xe8c217 → 0x1532260` 置 `R8B=1`，以 `0x15322f3/0x15322fa` 取同一 vector。`0x153234d/0x1532354` 仅跳过 null，分配 `0x38` B 并复制整项；`0x15323d3/0x15323e4/0x15323ed` 将临时验证结果写到 wrapper `+8`。不测 validator 返回值就追加该 wrapper（`0x15323f1 → 0x1532320` 或扩容路径）；`0xe962a0` 枚举它，经 `0x15328f0 → 0x43656a0` 调共同 getter，并对 `clfr` 单独取 wrapper byte。**反例**：合成一个非空 link 但 endpoint A=null，validator 在 `0x1528484 → 0x152866a` 写 reason=1；wrapper 生成处没有成功门槛。不据此外推最终 UI 行筛选或实机 `clfr` 频次。
- **持久化反链**：具名打开器 `0x434e390` 拼出 `club_links` 和 `.dat`，`0x434e483 → 0x1529210`。另一读取入口 `0xf2a395/0xf2a3af` 传上下文 `+0x680` 的 staging vector 给同一 reader；后续 `0xf3dba1/0xf3dbae → 0x1529850 → 0x434e5e0` 从同一 staging 逐项解析两个端点。`0x434e6ca/0x434e6d5 → 0xe6ca10 → 0x3ad6f50` 把**同一 link 指针**注册到两个 club 对象的 `+0x118/+0x120`，`+0x128` 是容量端。fixup 有有效性、类型和上下文限制；全表 wire 命中不代表每条都被编辑视图展示。构造路径 `0xf7411f → 0xf741c3 → 0xf73e10` 也用同一池并执行双端注册。
- **无 entry vptr/RTTI、无 slot 19、无数字 factory case。** VA `0x141b5ecc8` 是 reader/Cvfl/构造共用的分配池，不是 t39/t41 的 `table+0x80` 全局子表。池诊断名为 `CLUB_LINK`，不是 RTTI。`0x1529383` 分配 56 B，`0x1529393` 把首 qword 清零，`0x15293e7` 直接填端点 A 的 4 B；这里不是 constructor 写 vptr。数字 rel32 分发 `0xf48b30` 属于另一 loader 路径。t35 的 74 RTTI、45 stage2 零命中与本结论一致；原 JSON（含 `view_hypothesis`、`unknown_list`、`near_miss_club_classes`）及原报告未改。

## Archive、读游标及五类分支

| 归档 | 目录项 | 成员 | Count / stride | 解压 SHA-256 |
|---|---:|---|---|---|
| client | 31 | 不存在（不是空表） | — | — |
| server | 77 | `server_db/club_links.dat` | 9,261 / 47 B | `8933328064b13a9d8dc153dd5b455970a7c28ada1e24f4ecc9df35735f42f3d2` |

`entry.offset=38906216`，`data_base=34`，成员区 `[38906250,38970194)`，压缩 63,944 B，刚好止于下一成员。成员内一帧按 `entry.size=435279` 唯一选中。目录底层未提供 SHA 字段，结果中的 `entry.sha256` 为**压缩区**实算 `894f1efb9caf18482402198ed19294d04725a583ca262a6a01b2ed95c2222fe0`，不与 payload SHA 混用。

`0x1529210..0x1529844` 的 PE `RUNTIME_FUNCTION` 内有 **404 条可达指令**，日期 thunk `0xdb7f80 → 0x39dd7b0..0x39dd7f9` 有 **26 条**，两者均无 extent 外 CFG 边。`0x152923a` 读 count；每项 16 次必读、1 次条件读（包括两个经 helper 的实际读；另有不消费字节的 lifecycle 调用）。`0x152960e` 根据全局版本 word `VA 0x141b60330` 决定是否读最后 4 B，门槛 `0x0dd6`。本档头 `0x0df1`，且仅现代 47 B 模式闭合；未声称观察到实机对此全局的赋值。用同一 payload 回放旧分支得 43 B，首行在 `@55` 提前结束，全表走到 `@398235` 留 37,044 B。两种合成正确长度均有 selftest。

| 分类 | 数量 | 判据或首反例 |
|---|---:|---|
| wire_data | 3 | count=0 快捷途径、已读 A=B 时不入 staging（合成首行仍读 47 B）、按 count 回边（实测 9,260 次，末项退出）。 |
| runtime-external | 1 | 版本 word，非 selector 或 link type；旧版本反例见上。 |
| IO-result | 18 | stream `+0x10` 或日期 helper AL；每站都保留首个短读反例，例如 count `@8 w4`、首项端点 A `@12 w4`。 |
| context-lifecycle | 24 | 初始 staging 容量、TLS、pool、stream/refcount；按有效 stream、成功分配建模，不能用未观察的边证明死代码。 |
| dead / 有效输入不可达 | 3 | `0x15297a3/0x1529825` 的 taken 边由 `xor eax,eax; test al,al` 证明不可达；日期 helper null 跳进 `[rsi+0x10]` 解引用，只在有效读语境排除该边。 |

**闭合 `12 + 9261 × 47 + 0 = 435279`**。首 8 B 为档头，`@8` 是 u32 count；第 `i` 项 `@12+47i`。没有 selector、数字表 identity tail 或 vector footer；后置校验依靠精确 EOF、逐行 hash、双端点和独立 club 键域，未拿尾搜索切项。标准 `legacy14`、`wire13` 均**不适用**：首项 `@12 f6040000` 就是 ordinal 1270，`@13/@14` 在该 lane 内。JSON 保存全行 trace 摘要、代表 raw 行、未命名 lane、type/selector 画像（后者为空）。

## 字段三重闸门与负例

冻结 club scoped schema 与 t24 idx **370–398 / 400–418** 分别唯一对应；先验 4CC 命中、再验 getter 成员到 reader sink、后验全表域。偏移均从 47 B 原生行首算。

| 4CC | Wire / 对象 | 判定 |
|---|---|---|
| `affl` | 双 i32 `+0/+9` → 对象 `+0/+8` | **L3 派生**：当前 club 是 A 就取 B，否则取 A（只针对已注册到该 club 的 link）。两 lane 各 9,261/9,261 命中实际 t3 ordinal。首行 A=1270→UID 1688；B=11272→UID 4212156。把 wire 当 UID 分别漏 5,751 / 8,560 行，首反例都在 row 0。 |
| `ismc` | 同两端点；当前 club == A | **L3 派生**，不是 bit。首行以 A 为 viewer 为真，以 B 为 viewer 为假；同一 raw bytes 可以产生两个值。 |
| `stdt` / `endt` | `+13/+17`，各 4 B → `+0x20/+0x24` | **L3**：day=`u16 & 0x1ff`，year=高 u16；逐行按闰年校验 1..365/366。年域 1900..2024 / 1900..2042；构造默认 1900 day 1 各 6,909 / 8,902 条，不擅称空值。 |
| `type` | signed i8 `+4` → `+0x30` | **held**：4CC 与 sink 已锁定；冻结相应 `CAfT` 枚举缺 21，raw 有 609 条；首 row 12 `@580 15`。不补标签、不发布验收坐标。 |
| `yfee` | i32 `+25` → `+0x10` | **held**：域 `[0,10^9]` 下有 8,984 个 −1；首 row 0 `@37 ffffffff`（type=4）。getter 无 −1 特判；不推货币单位。 |
| `fri%` / `pwgp` | signed i8 `+35/+42` → `+0x33/+0x36` | **L3**：显式 `-1` 未设置（7,715 / 131），live 在 XML `[0,100]`。`pwgp` 的 8,776 个 raw 0 不是 −1。 |
| `msls` | signed i8 `+36` → `+0x34` | **held：全表只有 −1**。getter 明确省略该值，但无法实证 live 域 `[1,30]`；首 row 0 `@48 ff`。 |
| `clfr` | Cvfl wrapper `+8`，不是 wire | **runtime-only**。冻结枚举 `0..6`；初始化 0，validator 写 1..6。用合成 null 端点分支否证“必须从磁盘有一列读出”。 |

`affl` 的端点 resolver 从 club family（对象 type 3）修复索引；兼容/重映射路径未简化成无条件索引。实际键域以 client t3 的 84,259 个逐行 identity（含三条 compact）构建；用相同 triple 在 server t3 做前向最早、后向最迟有序对齐，84,259/84,259 一致。这里只核验 t3 target 键边界，不解析其非附属字段。本档无 A=B，自连接合成反例不改 wire 长度。

**位图**：20 个布尔共用 `CLUB_LINK+0x1c` 的 u32，单次 4 B transfer 到行 `+5..+8`，**不是都在一个 byte，也不是 20 个独立 byte**。`ismc` 另行派生。bit→代码：`1 frly, 2 golo, 3 fotb, 4 plfr, 5 yutr, 6 perm, 7 smbo, 9 fnhl, 10 hlwf, 13 mrrl, 14 scks, 15 cpsd, 16 ualf, 17 lpfs, 18 ustf, 19 yout, 20 rsrv, 21 pfpr, 23 UsSK, 28 bttr`。每位以具体 getter load/shift/mask 绑定，验首 set/clear 及 one-hot；所有已命名位都有两种观测值。例：row 0 `@17 e2018004` 中 `frly` 为真而 `golo` 为假，单一 Boolean 解释不成立。其余位和其他未命名 lane 不晋级。

## 复验及剩余

`FM24_DB_DIR=<WORKSPACE>/scratch/data`、`py -V:3.12 -I -B`。Builder、独立 verifier、两者 `--help`/`--selftest`、`scripts/t01_anchors.py`（**7/7**）均通过。Verifier 不 import builder 或 `ReaderCFG`：独立按目录/区界解压，重建可达边，以 `struct` 固定布局复算全行和各字段，对照原 PE 指令及 t35 原证据 SHA。退出码 0/1/2 为成功/检查失败/用法或致命错误。未启动游戏、编辑器或 IDA，未联网，未访问 Z:。剩余为 `type=21` 的枚举解释、`yfee=-1` 的域定义、`msls` 活样本、实机 `clfr` 画像与未命名 lane；均不把静态/回放当实机观测。
