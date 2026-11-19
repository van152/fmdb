# t30 — Clhs / table 37 静态 cursor

**验收：server 465,712 行全部闭合；client 目录无该成员；Clhs 0 → 8 L3，4 held，L4=0。** 结论限当前 `0x0df1` 归档和已走通的运行时路径，不是任意输入规格。

## 归档与坐标

| archive | 目录条目数 | table 37 | count | stride | 解压 payload SHA-256 |
|---|---:|---|---:|---:|---|
| client | 31 | 不存在（不是空表） | — | — | — |
| server | 77 | `server_db/table_37.dat` | 465,712 | 40 B | `46d9c5a7750a1d0fd2279b5f92b88936e98c143bfa4a0bd5faded5d710ef4f30` |

分别查两个目录，不从 server 搬 client 偏移。server 目录 offset `39061351`，t29 记录 Zstd frame `39061385`；目录成员 SHA 不是解压 payload SHA。全 archive SHA 和原目录项见 `cursor_clhs.json`。消费 t29 已交付的 `profiles/table_server_37.profile.json`：核对同一 payload SHA、legacy row block SHA、count/stride，并逐列对照全表 unsigned 画像；不重 dump。构建时 `subtable_inventory.json` 尚未交付，未将任何数据侧猜测用作命名闸门。

- **物理** `13 + 465712 × (1 selector + 27 members + 12 identity) + 9 = 18628502`。每行的 selector `13+40i`、body `14+40i`、end exclusive `53+40i`，是逐次 transfer 推进后的结果，不是按 stride 裁切后让 reader 匹配。全表 trace 逐行取 identity 和 body SHA 后汇成 digest；JSON 保存可重建的行模板及七条抽样，不铺开 46 万条重复坐标。
- **Legacy** `14 + 465712 × 40 + 8 = 18628502`。物理行内坐标比 legacy body 坐标大 1；legacy `+39` 借下行 selector，末行借 footer 第一字节。物理 footer 从 `18628493` 开始：`00 00 00 00 | 01 | 88 81 da 05`。`0xf2ba7f` 的真 helper 消费 vector count，零时跳过每条 `4+4+4` 的向量数据；外层随后读 1 B 和 4 B 到表对象 `+0x58`、`+0x50`。末 u32 是 `98206088`，此次等于 UID 最大值，**不是**记录数，也不外推为未来文件的不变量。
- 全部 selector 为 0。factory 将其作为参数传入，但 table 37 case 不分派该参数；非零只由本归档 replay 的观察域拒绝。identity 从 body `+27`/物理 `+28` 读到对象 `+8..+19`；raw lane 0 逐行等于 ordinal，后两条 u32 lane 相等、非零，465,712 个 UID 各不相同。后置校验不允许 ordinal overwrite 掩盖 raw 首 lane 失配。

## 静态路线与分支

L3 二进制：只读 `D:\tmp2b\fm24\input\editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`；与快照 `evidence/fm24/reports/qa/IDA_PROVENANCE.md` 核对。`master.json` 冻结 SHA `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`；二者均通过 `evidence/MANIFEST.json`。下表和说明用 PE file offset，VA 和原指令 bytes 见 `instructions.part*.json`。

- factory `0xf48b30` 的表基址 `0xf49d38`，第 37 个 rel32 cell 解到 `0xf49558`；`0xf49574→0xf4957b` 取并写入 vptr `0x14188e118`，slot −1/COL `0x188d870` 回溯 TD `STARTING_TEAM_LEAGUE_HISTORY`。
- slot 19 `0x14119e7f0` / file `0x119ddf0` 是无 runtime-function extent 的直接跳板。真 reader `0x143fce190` / file `0x3e62b90`；PE runtime-function exclusive end `0x143fce3e7` / `0x3e62de7`。`ReaderCFG` 走出 164 条指令、27 基本块、20 条条件、无外部 CFG 边。15 个实际传输都是 stream vtable `+0x28`（14 个成员 transfer 和 `0x3e62d8f` identity bulk），没有要当作 0 B 的属性 helper。另有 2 个间接调用：callback、最终释放。外层 footer helper 也跟到真 transfer `0xffa602`；外层只记录 header、行分派及 footer 的相关片段，并非整个通用 loader CFG。

| 谓词类别 | reader / 外层切片数 | 来源、边与反例 |
|---|---:|---|
| `wire_data` | 1 / 5 | reader `0x3e62da7` 无符号比较刚读的 identity lane 0 与 `10000001`，所有实测行均跳过 overwrite。外层检查行数和 footer vector count。|
| `runtime-external` | 1 / 0 | `0x3e62ba2` 读 caller 栈参；`0xf2b670` 的 R9D → R12B → caller `rsp+0x30` → reader `rsp+0x70`；不是 selector、也不是 header flag。两个入口值均尝试同一完整成员：非零走完；零只读 12 B，首行即反例：`row 0: identity at 14 raw=(6330, 51, 4294967295), stored ordinal=6330`。R9 本身不被此 reader 使用。|
| `IO-result` | 14 / 11 | 每个成员读后测 stream `+0x10`，错误收敛于 `0x3e62d6c`，AL=false；最后一条 `je` 的成功边是 taken。保留每个 transfer 的首行短读反例；例如 `row 0: short transfer @14 width 4 site 0x3e62bd3; IO-result -> 0x3e62d6c (AL=false)`。**bulk 后无即时状态测试**，短读是 replay 拒绝，不能说原生 reader 立即 AL=false。|
| `context-lifecycle` | 4 / 3 | tail 的 stream null、callback null、release stream null、原子减引用计数；caller 给同一 live stream、callback = table this，retained owner 下 release 不进析构。属性路径在 tail guard 之前已解引用 stream；null + 全量模式不是有效输入，null + 跳过属性模式则缺 identity transfer。callback 不直接接收 stream，其体和最终析构未展开，保持运行时限制。|
| `dead` | 0 / 0 | 没拿数据缺席当死边。footer 非零 vector 分支留在切片证据里；不是此档的有效行路径。|

逐条件的 predicate、源、原生目标、fallthrough、reader 实测访问次数在 `branches.part*.json`。

## 12 项台账及晋级

闸门：(1) 冻结 `club.xml/Clhs` 只有一份该 item occurrence，逐项对接 t24 idx 538–549；(2) `Clhs` 父分发 `0xe8c334→0xe8d3b2` 的 collection arm，经 `0x1521d30` 跳到 `0x4344a40`，按对象 `+0x20` 的修复后引用挑选条目；同一 class 的 slot 2 (`0x14119f210`) 从 EDX 的精确 4CC 到下面成员；(3) 成员必须对上实际走到的 wire sink，再以全表通过冻结 XML 域及 getter 哨兵为准。`mxtm` 是 **Max Teams**，非最大积分；`orde` 的 getter 检查 **0** 为缺值，非通用 `-1`。

| 4CC | 对象偏移 | legacy / 物理行内 | 宽 | 等级 / 保留的首个反例（ordinal 0-based） |
|---|---:|---:|---:|---|
| `year` | `+0x36` | 候选 +12 / +13 | 2 | **held**：87 个 0；首行 114717，`0000`，XML 1800–2100，无 getter 缺值分支 |
| `orde` | `+0x38` | +25 / +26 | 1 | **L3**，0 sentinel，443,713 行 |
| `divi` | `+0x18` | +0 / +1 | 4 | **L3**，competition ordinal；观测 0..7044，465,712/465,712 在域内 |
| `posi` | `+0x39` | 候选 +14 / +15 | 1 | **held**：691 处越界；首行 6472，53 (`35`)，XML 0–50 |
| `mxtm` | `+0x3e` | 候选 +26 / +27 | 1 | **held**：2,626 处越界；首行 6269，54 (`36`)，XML 0–50 |
| `poin` | `+0x34` | 候选 +23 / +24 | 2 | **held**：187 处越界；首行 216，−3 (`fdff`)，XML 0–1000；只承认 getter `-1` sentinel |
| `play` | `+0x3a` | +15 / +16 | 1 | **L3** |
| `wins` | `+0x3b` | +16 / +17 | 1 | **L3** |
| `draw` | `+0x3c` | +17 / +18 | 1 | **L3** |
| `lost` | `+0x3d` | +18 / +19 | 1 | **L3** |
| `gfor` | `+0x30` | +19 / +20 | 2 | **L3** |
| `gaga` | `+0x32` | +21 / +22 | 2 | **L3** |

`divi` 是 schema reference，不当作级别 enum：slot 21 writer 从 `obj+0x18` 引用取目标 `+8` 的 ordinal（null 写 `FFFFFFFF`）；slot 20 fixup 取此 u32，经目标表映射后写 qword；getter 收回该指针并以 `comp` 标记装箱。辅助只读对照 client comp/table 25 的 7,047 个连续真实 ordinal，未使用 public UID，也未重判 table 25 字段。其他整数由 `movsx` 或（仅 `year`）`movzx` 锁定，有冲突不做裁剪或 unsigned 重解释。没有 date 字段或日期晋级；`year` 是单独读入的 u16 年份，不是 packed day/year。body +4 和 +8 是未命名的引用槽，identity 不是 nested field；不计 L3。余下工作是解释四个域冲突（包括历史原始值与 UI 限值的差异），并按需验证尚未展开的运行时边，不改写反例。

## 复验

- `py -V:3.12 -I -B scripts/t30_clhs_cursor.py` — PASS，8 L3 / 4 held。
- `py -V:3.12 -I -B scratch/t30/out/verify.py` — PASS；不 import builder，重读两归档目录及 payload、重新反汇编原始 bytes/VA 和重建 CFG、复算 465,712 行与独立列向量画像、抽查样本及 counterexample。
- 两脚本 `--help` / `--selftest` 均通过；退出码 0/1/2 分别为成功 / 检查失败 / 用法或致命错误。
- `py -V:3.12 -I -B scripts/t01_anchors.py` — 7/7 PASS。
