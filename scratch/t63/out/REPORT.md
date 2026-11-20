# t63 — CLUB `table_3` 主行 unmapped 第二轮普查

E97 的 **399** 个 `unmapped` occurrence 全部复查，增量为 **8 L3 / 41 held / 350 unmapped**；L4=0。八项均是 **server mode、`CLUB+0x150` 的 tag 0 本地 getter 投影**，不是八个新外层位置；client 没有这段载荷。E97 原有 13 L3、11 held、10 个独立成员跳过项和负证据不变；未修改 v9 `club_main_row_fields`。

## 行框和静态扫描边界

只用 `scratch/t57/out/field_slots.json` 的行框：client `13+6,932,060+9 = 6,932,082`，server `13+16,595,290+9 = 16,595,312`，各 84,259 行；12 B `ordinal | UID | UID`、34 个逻辑位置。逐行顺读、两档 identity/selector 配对，所有位置坐标摘要都与 E97 一致。没有从 XML 序号或字节相似性推槽。ID `E97/club.xml#club/NNN` 中 `NNN` 仅是冻结 occurrence 的索引。

静态来源为只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。冻结 master 和旧夹具经 `evidence/MANIFEST.json` 校验。下文地址为 PE file offset；JSON 保留 VA、原始字节及指令。`CLUB` slot 19 `0xe5a7a0`（VA `0x140e5b1a0`），extent `0xe5a7a0..0xe5bfca`：1,412 条可达指令、167 条条件、41 个直接 stream 站点。扫描覆盖 E97 的主 reader 和六个有界 reader helper；台账保留 407 个条件和分支后继，不把未观察路径视为死边。

CLUB slot 2 `0xe89a00` 的本地扫描覆盖 5,894 条可达指令、18 个已解 rel32 表和 708 个条件；另扫描七个相关 getter extent（含继承分派，只做注册/路由普查）。按大小写精确的 4CC 对齐：190/399 在 CLUB 顶层有匹配入口，293/399 在八个有界 getter 中至少有一个入口，106/399 无入口证据。匹配只证明本地分派可达，不证明本类拥有被返回字段。寄存器 tail call/外部 override 未做任意展开，未处理者保留边界；已命名的 virtual 分派交叉核对 vtable 格。`projections.json` 给出每个 occurrence 的比较/bit-test/rel32 格、局部等值路径、直接 helper 边，以及可证的读取路径或首断点。字符串不按相邻值猜槽。

## 通过的八个投影

`0xe5a9ba` 控模式；`0xe5ada9` 读 tag，`0xe5adc8..0xe5add3` 选 tag 0，`0xe5ae12/19` 安装 vptr，`0xe5aea6` 保存 `CLUB+0x150`。同一个 vptr 的 slot 4 经 `0xe5aef1 → 0x1476470 → 0x423fef0` 读载荷，slot 2 经本地 getter `0xe8c605 → 0xe8c615 → 0xe8eb9f → 0x147a290` 返回投影。并非此路上每个调用都用 rel32：两个 virtual 格是已核实的 64-bit vtable pointer；reader thunk 是 next-IP rel32；`Cmtp` 顶层另有基址相对 rel32 格 `0xe91cfc`。`Cpfa` 由相邻的 `0xe8e787` arm 走相同 tag 0 getter。

`obj150` 内 45 B 游标顺序为 `(+0x14,4) (+0x3c,1) (+0x39,3) (+0x2c,13) (+0x10,4) (+0x18,20)`，坐标是 **tag 0 对象内成员**、不是 CLUB 直接位移。每项全扫两档：client 84,259 条绕过；server 84,256 条有载荷、3 条 tag 2 绕过；tag 1 静态存在、零观测。`Chaf` 另有 getter 内部条件抑制。

| 4CC | 顶层 gate → tag 0 helper gate | tag 0 成员 / 载荷 lane | 已验证全档域（server） |
|---|---|---|---|
| `Ccba` | `0xe8b7b3 → 0x147a2e1` | `+0x14` / 0–3 | `0x147a2f5` 用 vtable `+0x190` 调 `0x55fc0`，取 i32 原值；−85,917,952 到 450,000,000，均在 XML ±1,000,000,000 内。 |
| `Cadm` | `0xe8b4cf → 0x147a2c9` | `+0x3b` / 7 的 bit 1 | `0x147a52c` 取 byte，`0x147a539/3b` 做 `shr 1; and 1`。0=84,253，1=3；raw `{0:84246,2:3,16:7}`，不能以 byte 非零代替。 |
| `Cesd` | `0xe8c5f9 → 0x147a402` | `+0x2c` / 8–11 | 23 个不同日期，年 1900–2024；84,215 个 `(1900,1)`。 |
| `Ceed` | `0xe8bb98 → 0x147a3f6` | `+0x30` / 12–15 | 25 个不同日期，年 1900–2025；84,215 个 `(1900,1)`。 |
| `Cead` | `0xe8a391 → 0x147a3ea` | `+0x34` / 16–19 | 4 个不同日期，年 1900–2024；84,252 个 `(1900,1)`。 |
| `CteA` | `0xe8bdcc → 0x147a4c1` | `+0x38` / 20 | `movsx` i8；`{0:84253,15:2,19:1}`。XML 仅定 integer，未声明 min/max，不自拟年龄域。 |
| `Chaf` | `0xe8a6fc → 0x147a364` | `+0x39` / 5 | `0x147a5f2` 要求 `+0x3c != 0`；返回值 0=444、1=22，83,790 条被抑制，不算 false。Raw 0=84,234、1=22；不是 `Cadm` 所在 byte 的位。 |
| `Cmtp` | `0xe8a49f` 格 `0xe91cfc → 0x147a37c` | `+0x18` / 25–28 | f32 有限，0–100，均在 XML 0–300 内；reader `0x423ffa0` 的 >150 清零分支全档未触发。只声明本地 getter 单位，不把 XML `store_pence` 解释成编辑器写回的换算规则。 |

三个日期 getter 皆取低 word 的低 9 位作年内日、高 word 作年；其余 7 位本档全 0。逐条按 Gregorian 年长（含闰年）检查，0 越界；不把 `(1900,1)` 擅改成 null。另测日期关系：41 对非默认 start/end 全部顺序正常；4 对有非默认 appeal/start 的记录全部不满足标题的 “Must Be Before Start”。首例 server row 1410 `@851416:1b01e7071c01e8075801e707`，`(2023,344)` 晚于 `(2023,283)`。这条负证据保留在 `date_relationship_control`；L3 不声称输入表符合 UI 编辑约束。

## Held 与控制

- **22 项 `cnst`**：玩家态通过 `0xe89be8` 的精确格进 `0xe89bea → 0xe89c13 → 0x151d9b0`；职员态有 `0xe89fd3` bit-test、精确比较及 `Ccss` 的 rel32 入口，均汇入 `0xe89fdc → 0xe8a005 → 0x151e500`。两个 helper 以逐个 `movsx` 证明 7+15 个 byte 位置，分别在 **`*(CLUB+0x100)+0xe0..0xe6` 和 `+0xe7..0xf5`**。首断点 `0xe89bef` / `0xe89fe1` 都是加载额外对象指针，不是 CLUB 同址 `+0xe0/+0xe7`。无 t57 主游标相接，故只录本地 getter、冻结 scoped enum 及缺游标的反链；没有主行坐标，也没有把 comp 的观测枚举子集搬过来。
- **`Chsd` / `Cpfa`** 找到精确字节，但没有 scoped `enum_ref`；分别以 row 0 `@107:00` / `@110:00` 记域证据不足的首见证，不伪称 0 越界。`Cpfa` 与 `Cadm` 共用 raw byte，不能按 `Cadm` 单位解整个枚举掩码。**`Casp`** 的同对象 f32 绑定成立，但一条违反 XML 0–10,000：server row 78,210 `@15571299:3b79a747` = 85,746.4609375。**`rdui`** 是 identity 的第三 dword；继承 getter `0xfe389d/0xfe38a2/0xfe38a7` 在其等于 UID 时不暴露它，两档每条均抑制，首例 client row 0 `@104:39000000`。不把 persisted lane 计为可用字段。
- **引用无新命名 L3**：`Clri` 实为从已解析 City 再走 `City+0x38`；`Cldi/Cndi/Codi` 转发第一 Team；`Csmn/Csna` 按上下文列表找匹配 Team，不能错填 `Ctsi` 的 `+0x140`。旁证 `ref_e0` 读 `0xe5a843`，与 Nation 同 resolver/context `+0x28`，但没有精确 4CC。按两档 t10 实际 251 个 ordinal（只复查 t47 的 identity 原字节）验证：每档 live 26,587 全命中，null 57,672；错读 UID 仅命中 9,286，首 miss row 238（client `@19270` / server `@119872:aa000000`），不是完整映射。两档首 live row 5 的 ordinal 126 → UID 752。未命名，不用值域把它强配 schema。
- 其余 static-stop 候选保留阻断指令：`Cebd` 走 `+0x100 → extra+0x78`，`Csjd/Csld` 取上下文记录，`Css*` 走 `+0xb0` 运行时列表调用，`Cmls/Chdb` 未闭合同对象位/游标。其余 350 项保留 unmapped；没有推断它们不存在 wire。

## 回归与复跑

Liverpool 双档 ordinal 460 / UID 676 → city ordinal 1061 / UID 100047，短名与国家列一致；Bernabéu ordinal 430 / UID 1056 容量/座位均 81,044。Old Trafford `74,031 != 74,140` 仍保留。成立年只复验冻结的 14 条 client extra_3 fixture：Liverpool 1892，Manchester City 1894 vs 外部起源 1880 的约定差异原样保留。未普查 sidecar、八个独立子表或 CLUB_LINK，未重解 nation/comp 或 person/PDxx。未启动游戏、编辑器、IDA；未联网或访问 Z:。

独立 `verify.py` 不导入 builder、ReaderCFG、fm24_dump；重建 PE 有界分派、独立读取 FMF 目录、重放 168,518 条行和所有候选值、对照原始锚点。两个脚本 `--help` / `--selftest` 通过，退出码 0/1/2。全档 build / verify 通过，t01 anchors **7/7**。

```bash
export FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data
py -V:3.12 -I -B scripts/t63_club_unmapped_r2.py --build
py -V:3.12 -I -B scratch/t63/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
