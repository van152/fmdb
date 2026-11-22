# t91 §4 — 文法印证:外源 ext/fm-data@d7a7150 主张 vs 我们 FM24 现状

**纪律**:外源一律 `provenance=ext/fm-data@d7a7150`,只作假设源。下表每条给出
「外源主张 / 我们现状(带证据坐标)/ 一致性 / 需补的验证」。一致性只分四档:
**同族(独立印证)** / **部分同族** / **不可比(域不同)** / **冲突(待查)**。
本文件不新增任何 L1/L2/L3 分级,不改 reports/ 与 LEDGER。

我们侧的坐标全部来自本仓既有落盘件(只读引用):
`scratch/t88/out2/row_frame.json`、`scratch/t84/out/joins.json`、
`scratch/t91/out/nulldate_probe.json`、`scratch/t91/out/code_coverage.json`、
`reports/club_nation_subtable_schema.json`(v11.1)、
`evidence/fm24/reports/editor_schema/master.json`。

---

## H1 — 内联字符串文法 `[u32 len][utf8 name]`

- **外源主张**:agentB §2.1 — person 记录的全名字段是 `[u32 len][utf8 name]`,
  len 为 UTF-8 字节数;内联串前另置 sentinel `ff ff ff ff 00`。
- **我们现状**:`server table_45` 行框冻结结论 `header_name_grammar =
  "[u32 len][utf8 name] at row+37; rowlen == 80 + len"`,且 `rowlen_eq_80_plus_namelen
  = true`(84,477 行全过)。即长度字段与行长的算术关系被逐行验证,不只是"看起来像"。
- **一致性**:**同族(独立印证)**。两边在同一容器族(tad.+zstd)上独立得到
  同一 length-prefix 文法,且我们这侧有**行框闭合**这层额外自证(外源没有行长约束)。
- **需补的验证**:外源 `ff ff ff ff 00` 五字节前缀在我们 row+37 的**前 5 字节**是否也出现;
  若出现,则可判定两族共享同一"内联串 sentinel"约定。本任务未做(row+32..36 未逐行统计),
  留作 t92 候选。**不得**据此把 row+37 的字段语义升级。

## H2 — 空日期常量 `01 00 6c 07` = (doy 1, year 1900)

- **外源主张**:agentB §2.2 — `01 00 6c 07` 是 FM 的 null date;日期统一编码为
  `(u16 day_of_year, u16 year)`。
- **我们现状**:`0x076c0001` 早已在我们侧作为 date4 sentinel 使用,分散记于
  t28/t44/t71/t76a/t79/t82/t83(例:`scripts/t71_club100_cnst.py` 的
  `default_1900_day1` 统计、`reports/club_nation_subtable_schema.json`
  的 `packed_date_u32` 槽位)。**但此前没有一次全档逐槽位命中率普查。**
  本轮补上(`nulldate_probe.json`),结果见 H2a–H2c。
- **一致性**:**同族(独立印证)+ 一处口径扩展**。同一常量、同一 `(doy, year)` 解码,
  两边独立成立;我们还额外得到"槽位级命中率"这一维证据。

### H2a — 槽位命中率(我们侧新证据,L1 自检量)

| 表 | 行数 | 命中率 100% 的槽位 | 次高 |
|---|---|---|---|
| `client table_21`(stadium) | 48,413 | row+13 | — |
| `server table_21` | 48,413 | row+156 | +135 (99.62%)、+131 (96.12%)、+45 (94.73%)、+41 (92.70%)、+37 (78.93%) |
| `client/server table_0`(award) | 3,545 | 无 | row+19 (92.86%)、row+60 (89.45%) |

`server table_21` 的六个槽位与既有 L3 记录**逐一对齐**:`Splr`(body 131, held)、
`Sprl`(135, L3)、`Sbld`(37, L3)、`Srbd`(41, L3)、`Doco`(45, L3),以及 body 156
(= `Sbln`/`Sexp` 一带的 held 区)。**这是独立复算,不是新判据。**

### H2b — 随机与"任意常量"对照(证明不是巧合命中)

- 同表**其它槽位的平均命中率**:`client_21` = 0.0286、`server_21` = 0.0316、
  `table_0` = 0.0246。即基线约 2.5–3.2%,而命中槽位 78.9–100%,差 25–35 倍。
- **对照常量**:`0x076c0002` / `0x076c0000` 在同表所有槽位的最高命中率分别是
  0.0 / 0.0006;`0x01000001`(仅换字节序写法)最高 0.0051。→ 命中的是**这个特定值**,
  不是"任何 4 字节常量都会命中"。
- 字节级期望随机出现次数 = `len(payload)/2^32` ≈ 0.0004–0.002,实测命中是它的 10^5 量级。

### H2c — 非 sentinel 行的 `(doy, year)` 文法校验

对命中槽位上**不等于** sentinel 的行,直接按外源的 `(doy, year)` 解码:

| 槽位 | 非 sentinel 行 | 文法通过 | 通过率 | year 范围 | doy 范围 |
|---|---|---|---|---|---|
| `table_0` row+19 | 253 | 253 | **100%** | 2003–2024 | 1–365 |
| `table_0` row+60 | 374 | 374 | **100%** | 2008–2024 | 7–366 |
| `server_21` row+131 | 1,880 | 1,880 | **100%** | 1957–2024 | 1–366 |
| `server_21` row+41 | 3,534 | 3,533 | 99.97% | 1919–2028 | 1–366 |
| `server_21` row+45 | 2,549 | 2,529 | 99.22% | 1859–2028 | 1–366 |
| `server_21` row+37 | 10,202 | 10,094 | 98.94% | 1807–2029 | 1–366 |
| `server_21` row+135 | 182 | 174 | 95.60% | 2009–2031 | 1–365 |

**这是本任务对外源最有价值的一条独立印证**:同一个 4 字节槽位,在等于常量时是
null date,在不等于常量时**几乎全部**解成合理的 (doy∈[1,366], year∈[1807,2031])。
两条互不重叠的证据(常量命中 + 非常量解码)共同支撑 `(u16 doy, u16 year)` 编码。
**但仍不构成 L3**:缺 exe 侧 getter/setter 对该槽位的宽度与解码指令;`row+37` 的
99% 也留 1% 反例(108 行)未解释,负结果原样保留。

### H2d — 与既有 date4 sentinel 分列口径的关系

**只增证据,不推翻**。既有口径按"表/字段"记 sentinel 恒等(`0x076c0001` 全档默认值),
本轮补的是"**槽位级命中率 + 非 sentinel 解码通过率**"这一维;两者互不否证。
差异点如实记录:外源称 1900-01-01 为 *null date*(语义:未设置),我们既有记录多写作
*default/sentinel*(语义:常量)。**语义命名不改判**,待 exe 侧确认 getter 是否抑制该值
(既有 `t83` 已有"getter suppresses 1900-01-01"的先例,可作 t92 的对照起点)。

## H3 — person id 相邻双写 `[uid][uid]`

- **外源主张**:agentB §5 — 每个 player 的 unique id 在记录内以**相邻重复 u32 对**出现;
  agentC §basic_people — 84 字节定长记录里 id 也在 offset 16/20 双写。
- **我们现状**:identity 定义 `[ordinal u32][UID u32][UID u32][marker 1B]`,13 字节,
  `u1 == u2` 且 `u1 > 0` 为判定式(`scripts/t74_frames_part2.py::_ident_at`)。
  `table_45` 84,477 行 `bad_identity = 0`、`ordinal_matches_index = true`。
  `table_21` 48,413 行 ×2 档同样闭合。
- **一致性**:**同族(独立印证),且我们的约束更强**。外源只有"相邻重复"这一条,
  我们额外要求 **ordinal == 行号** 且 **UID 严格递增**,并以此做 DP 唯一铺法计数
  (路径数 == 1 才算行框成立)。外源 agentB §7 自陈"id 对不足以从 raw 单独定位"
  (p−8 ∈ {0,1} 匹配 ~28M 位置)——我们的 ordinal+递增双约束正是他们缺的那一半。
- **需补的验证**:无(此条已是我们的强侧)。**注意**:这不构成对外源等级的背书,
  只是两条独立观察落在同一文法上。

## H4 — 位置掩码 u32 / CA u16 / age u8(外源 FM26 值域)

- **外源主张**:agentC §summary — `pos_flags` u32 位掩码(bit 表见其 §position)、
  `summary_ca` u16 范围 0–195、`summary_age` u8。
- **我们现状**:我们**没有** people/summary 表的字段映射(people 属性块 PDxx 明确
  不在本工作区范围,见 AGENTS.md)。我们的 `Ppsr`(position)在 `play` 域,
  `Ncra`(current ability)在 `nnpl` 域,均为**行内槽位未定**状态。
- **一致性**:**不可比(域不同)**。外源解的是 FM26 的 summary.dat(未压缩、
  独立 TLV 表);我们解的是 FM24 的 client/server/table_* 成员。**表不同、版本不同、
  容器不同**。外源的值域(0–195 / u8)只能作为**未来若触及 people 域时的先验**,
  对现有 78 个 club L3 + 49 个 comp L3 **零影响**。
- **需补的验证**:若将来启动 people 域,须先确认 FM24 的 CA 上界是否同为 195
  (FM24 有 200 制与 195 制之争),不得直接沿用 FM26 的 195。

## H5 — people 表按 nation_ref 分组排序 → 对照我们的 nation 域行序

- **外源主张**:agentB §1/§6 — people 表**按 nation_ref 分组**(Algerians 先,
  2,079 个不同 nation_ref 值)。
- **我们现状**:`table_9`(NATIONAL_TEAM_CONTAINER)251 行 ×2 档,
  `ordering_policy = "wire 顺序 ≠ XML 顺序,后续映射不得按 XML 序号对齐"`
  (`reports/club_nation_subtable_schema.json::nation_main_row_fields`)。
- **一致性**:**部分同族**。两边都观察到"**行序不是 XML 序**"这一现象,但我们这侧
  的结论是**负向的**(禁止按 XML 序号对齐),外源给的是**正向的分组键**(nation_ref)。
  两者不矛盾,但**外源的 nation_ref 是 FM26 people 表的键,不是我们 table_9 的键**——
  table_9 本身就是 nation 容器(251 行 = 国家/地区),不存在"再按 nation 分组"的空间。
- **需补的验证**:若要复用"按外键分组"这一模式,应在 FM24 的 **club 表(table_3,
  ~84k 行)** 上验证是否存在按 nation/division 的分组单调性。本任务未做,
  且这属于新假设,不得写入 schema。

## H6 — 容器头 `03 01 "tad." a0 0f 90 0e 07 00` + zstd@12

- **外源主张**:agentA §1 — 12 字节头,`03 01` = version 0x0103,`tad.` magic,
  6 字节常量后 zstd 帧。
- **我们现状**:我们头部是 `03017461642ef10d`(**8 字节**,`tad.` 后直接 zstd@8),
  见 `nulldate_probe.json::people_family` 的 `header_hex` 与
  `scripts/t71_club100_cnst.py::HEAD = 03017461642ef10d`。
- **一致性**:**部分同族 + 一处确定差异**。version 与 magic 完全一致;
  但**外源的 6 字节 `a0 0f 90 0e 07 00` 在我们档里不存在**,我们这里是 `f1 0d`
  两字节后直接是 zstd magic。→ 这是**版本/产品线差异**(FM24 vs FM26),
  不是任一方解错。我们的 8 字节头在 t71 已按 SHA-256 钉死并逐档验证。
- **需补的验证**:无。**不得**把外源的 12 字节头套到我们档上;已在 REPORT 记为
  确定差异(negative result,原文保留)。

## H7 — `summary.dat` 未压缩

- **外源主张**:agentA §1 / agentC §输入 — `summary.dat` 不是 zstd,是裸结构化表。
- **我们现状**:`scratch/data/summary.dat` 1,648,018 字节,`zstd_at = -1`
  (全档无 zstd magic),头 `03017461642ef10d 07000000 01000000`,
  `0x076c0001` 出现 **0** 次(`nulldate_probe.json::summary_dat`)。
- **一致性**:**同族(独立印证)**。两边独立判定 summary.dat 未压缩。
  **附加负结果**:该档内**没有** null date 常量——与外源 agentC 的
  "summary.dat 里没有 DOB"陈述一致(他们也没找到 DOB)。这条是**双向负结果吻合**。

## H8 — 码表码空间同族(2103 vs 3009)

- **外源主张**:agentA §3 — editor.fmf 提取 2103 条 `db_field` 码,739 条 `pers`,
  表标签含 `pers, club, comp, natc, stad, team, weat, awar, inju, nati, city, agrm`。
- **我们现状**:`master.json` 3009 码 / 395 个表标签 / `pers` 271 码 / 60 个码无 name。
  可恢复的 18 个外源 `pers,*` 样例**全部命中**我们的码表(0 缺失),
  14/18 标签规范化后**完全相同**。
- **一致性**:**同族(码空间)+ 4 条标签漂移 + 3 条表域漂移**。
  - 标签漂移:`PnRV` Full Name↔name、`Pnti` (无 name)↔nation、
    `PCJO` Job↔club primary job、`PSJO` Secondary Job↔club secondary job。
  - 表域漂移:`Ncra`/`Npta` 我们记 `nnpl`、外源记 `pers`;`Ppsr` 我们记 `play`、
    外源记 `pers`。
  - **`natc` 在我们侧完全不存在**(0 码);我们有 `nati`(339 码)+ nation.xml。
- **一致性判读**:**冲突列不改判**。FM26(26.2.0)与 FM24(24.4.2)的 editor schema
  本就分属不同版本;表域漂移最可能是**外源把 `pers,*` 当作"人相关"的宽松归类**,
  而非我们码表错。`natc` 的缺席是**命名域冲突**(他们把 nation 容器写作 `natc`,
  我们写作 `nati`),不是覆盖缺口。
- **需补的验证**:要判定 `natc` 是否等同 `nati`,需要外源 `field_dict.csv` 原件
  (不在克隆内);本任务**无法**完成,如实记为未解项。

---

## 汇总

| # | 主题 | 一致性 | 对外源等级的净效果 |
|---|---|---|---|
| H1 | `[u32 len][utf8]` 内联串 | 同族(独立印证) | 无(我们不升,外源不降) |
| H2 | `01 00 6c 07` null date + (doy, year) | 同族 + 我们新增槽位级证据 | 无;我们侧仍为 L1 自检量 |
| H3 | `[uid][uid]` 双写 | 同族,我们约束更强 | 无 |
| H4 | CA u16 / age u8 / pos u32 掩码 | 不可比(域不同) | 无 |
| H5 | people 按 nation_ref 分组 | 部分同族 | 无 |
| H6 | 12 字节容器头 | 部分同族 + **确定差异** | 无(记为负结果) |
| H7 | summary.dat 未压缩 | 同族(含双向负结果吻合) | 无 |
| H8 | 码表码空间 2103 vs 3009 | 同族 + 7 条漂移 | 无(冲突不改判) |

**净结论(候选,非结论)**:外源与我们在 H1/H2/H3/H7 上**独立收敛**到同一批文法,
这提升了我们对这几条文法**描述**的信心,但**不产生**任何新的 L3 槽位定位,
也**不改变**任何既有分级。H4/H5/H6/H8 是域/版本差异,不构成互相验证。
