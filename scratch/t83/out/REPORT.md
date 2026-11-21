# t83 — award(0) / language(8) / weather(27) / derby(18) / media(7) 五表 L3 升级与 t76b 遗产吸收

## 0. 摘要与证据口径

- **任务范围**:将 `award(0)`、`language(8)`、`weather(27)`、`derby(18)`、`media(7)` 五张表(含已弃 `t76b` 三表遗产)在 `client_db.dat` 与 `server_db.dat` 双档上完成全量向量化数据侧剖析 + `editor.exe` 静态三重闸门 L3 升级。严格不碰 `stadium/team` (`t79`)、`lcrg/agreement` (`t76c`)、三主表及 `reports/`、`LEDGER`。
- **静态二进制(只读)**:`D:/tmp2b/fm24/input/editor.exe` (SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`)。沿用 `t57/t79` 约定:`field_map.json` 记 PE **file offset**(`fo`),`xref_{award,language,weather,derby,media}.json` 逐条同时记 **`fo`、`va`、原始指令字节与 Capstone 反汇编**。
- **冻结快照核验(`evidence/MANIFEST.json`)**:
  - `evidence/fm24/reports/editor_schema/master.json`:`7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda` (PASS)
  - `evidence/fm24/reports/dbdat_decode/db_tables_small.json`:`3d092a521d0683774cc0eaeaf32ac69587d5fec2f66e75cb3a1ce4901f4e63b2` (PASS)
  - `evidence/fm24/reports/dbdat_decode/db_tables_big.json`:`c57b2b6837a3dcca106bf4363da105eca7665df407b738483839d1b7b6de3ddf` (PASS)
- **冻结行框/L2 地基核验**:`scratch/t74/out/frames.json` 全部 10 个 `(archive, table)` 成员的 `payload_len`、`count`、`payload_sha256` 10/10 逐字节吻合;`scratch/t76c/out/slots_{client,server}_{18,27}.json` 4/4 `payload_sha256` 吻合。
- **XML 端分母口径**:`reports/xml_denominator_coverage.json` 仅统计三主表 (`club/comp/nation`, 1,034 occ),不含本任务五张表;故本任务五表 XML 分母直接取自 MANIFEST 校验通过的 `master.json`,共计 **188 字段** (`38 + 12 + 22 + 94 + 22`)。
- **证据等级**:静态链达 **L3**,数据面为全档向量化校验(**零抽样**);**L4 = 0**(未启动游戏/编辑器/IDA,未读写 `Z:`,未联网)。

### 五表总收获一览 (XML 188 字段 100% 入账,全部字节 0 缺口闭合)

| 表 (table_id) | XML 文件 | 行数 | 双档关系 | XML 总数 | **L3** | **held** | editor_meta | computed | lang_layer | subtable | 内部 wire 槽 | 字节覆盖缺口 |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`award`** (`0`) | `award.xml` | 3,545 | `client == server` (77B 定长) | 38 | **24** | **7** | 2 | 2 | 2 | 1 | 10 | **0** (64B body 全覆) |
| **`language`** (`8`) | `language.xml` | 126 | `client == server` (变长) | 12 | **5** | **4** | 2 | 1 | 0 | 0 | 3 | **0** (17B suf 全覆) |
| **`derby`** (`18`) | `derby.xml` | 1,567 | `server = client + 6B/row` | 22 | **18** | **1** | 2 | 1 | 0 | 0 | 3 | **0** (36B/42B 全覆) |
| **`weather`** (`27`) | `weather.xml` | 334 | `client == server` (变长) | 94 | **90** | **1** | 2 | 1 | 0 | 0 | 2 | **0** (95B mid 全覆) |
| **`media`** (`7`) | `media source.xml` | 208 | `server = client + 7B/row` | 22 | **15** | **4** | 2 | 1 | 0 | 0 | 3 | **0** (20 步变长全闭合) |
| **合计** | 5 XML | 5,780 | 10 成员全闭合 | **188** | **152** | **17** | **10** | **6** | **2** | **1** | **21** | **0** |

---

## 1. 工厂、Vtable / RTTI 与全局 `DB_CONTEXT` 静态绑定

工厂函数 `0xf48b30` (`VA 0x140f49730`) 经 rel32 表 `0xf49d38` 精准分发五类(vtable slot 2/3/5/19/20/21 全量在 `xref_*.json` 验证):

| 表号 | 工厂 case (`fo`) | RTTI | Vtable `VA` (`fo`) | slot 2 (`get`) | slot 3 (`set`) | slot 19 (`read`) | slot 20 (`fixup`) | slot 21 (`write`) |
|---:|---|---|---|---|---|---|---|---|
| 0 | `0xf48c54` | `.?AVAWARD@db@@` | `0x14187b828` (`0x187ae28`) | `0xe49a70` | `0xe4c240` | `0xe483b0` | `0x3a96200` | `0xe48940` |
| 8 | `0xf48ebb` | `.?AVLANGUAGE@db@@` | `0x141888db8` (`0x18883b8`) | `0x1038a00` | `0x1039110` | `0x3d546d0` | `0x3d550a0` | `0x3d55740` |
| 18 | `0xf48f77` | `.?AVDERBY@db@@` | `0x141887278` (`0x1886878`) | `0xffd1b0` | `0xffdf50` | `0x3d00950` | `0x3d00fc0` | `0xffea80` |
| 27 | `0xf491dd` | `.?AVWEATHER@db@@` | `0x141882de8` (`0x18823e8`) | `0x158e6b0` | `0x15901a0` | `0x158b970` | `0xbe0` (空) | `0x158be80` |
| 7 | `0xf48ea6` | `.?AVMEDIA_SOURCE@db@@` | `0x1418bdd08` (`0x18bd308`) | `0x1546e60` | `0x154a980` | `0x15457c0` | `0x437a490` | `0x1546220` |

全局 `DATABASE` 构造器 `0xf026c0` 注册的 16 个相关 `db+offset` 表绑定(均由 `mov edx, tid; call 0x140ffa310; mov [r14+off], rdi` 双指令核实):
- `+0x00`:t0 (`AWARD`)、`+0x08`:t2 (`CITY`, 56,293)、`+0x10`:t3 (`CLUB`, 84,259)、`+0x18`:t25 (`COMP`, 7,047)、`+0x20`:t5 (`CONTINENT`, 7)、**`+0x28`:t10 (`NATION`, 251)**、`+0x48`:t7 (`MEDIA_SOURCE`, 208)、`+0x50`:t8 (`LANGUAGE`, 126)、`+0x58`:t47 (`LOCAL_REGION`, 2,488)、`+0x60`:t9 (`NATION_T9`, 251)、`+0x80`:t21 (`STADIUM`, 48,413)、**`+0x98`:t24 (`TEAM`, 84,507)**、`+0xa0`:t27 (`WEATHER`, 334)、`+0xb0`:t18 (`DERBY`, 1,567)。
- 另参考表 UID 索引采用独立后向 DP(与 `t81` `fk_index.json` 在全部 12 张共测表 SHA-256 100% 吻合,且全部 13 张双档共享表 `client == server` 0 差;并在 `t24` row 0 精确检出 `UID=5` + 尾字节 `0x0b`,实现 `84,507/84,507` 唯一 UID)。

---

## 2. `award` (`table_0.dat`, 3,545 行 × 77B, 双档逐字节同构)

### 2.1 先补 L2:77B 逐列向量化 Profiling 与多表 FK 候选矩阵

- **行框闭合**:`client == server` 逐字节相等 (`272,987 B`, SHA-256 `1be793209ed08af033536bb3855dac14bf1d953e7614a5ce246c2bf9c1d041a4`)。原生行框 `13 + 3,545 × 77 + 9 = 272,987` (与 t74 `14 + 3,545 × 77 + 8` 差 1B selector 位移);行首 selector 恒 `0`,后接 **64B body (`@0..63`)** + **12B identity (`ord@64..67, duni@68..71, rdui_raw@72..75`)**。
- **77B 逐字节摘要** 完整记入 `domain_stats.json["award_0"]["l2_column_profile"]["byte_summary_0_76"]`;其中 4 个 4B `i32` FK 形态列(`0xffffffff` null 与合法 `0` 严格分列)在 `t5(7)/t6(INJURY,115)/t10(251)/t47(2,488)/t25(7,047)/t30(STARTING_INJURY,72,473)/t3(84,259)` 上的多表候选与 wrong-UID 对照如下:

| 列 (`body_off`) | live | `0xffffffff` | 合法 `0` | live 值域 | 最紧致 100% ordinal 候选 (`top/N`) | wrong-UID 对照 (目标表) | L3 最终静态裁决 |
|---|---:|---:|---:|---|---|---|---|
| `@23` | 3,452 | 93 | 208 | `[0..5]` | `t5` (0.7143; 大表皆空洞) | 3,244 / 3,452 命中 (小号巧合) | **`AWci`** → `t5` (`0x3bf4a90`) |
| `@27` | 3,232 | 313 | 22 | `[0..248]` | `t10` (0.9880) | 998 / 3,232 命中 (**2,234 miss**) | **`AWni`** → `t10` (`[db+0x28]`) |
| `@31` | 7 | 3,538 | 0 | `[4..4]` | `t5..t3` 皆含 4 (仅 7 行数据不可分) | 0 / 7 命中 `t47` | **内部 `+0x68`** → `t47` (`0x3bf5e90`, 非 XML 字段) |
| `@41` | 3,291 | 254 | 22 | `[0..6971]` | `t25` (0.9892; `t30`/`t3` < 0.10) | 441 / 3,291 命中 (**2,850 miss**) | **`AWmi`** → `t25` (`[db+0x18]`) |

### 2.2 L3 静态升级结果 (`award.xml` 38 字段: 24 L3 / 7 held / 7 non-wire-subtable)

- **24 项 L3**(全部过三重闸门且全档 3,545 行 0 违例):
  - 身份:`duni` (`@68`, `+0x0c`, `0xfe3912`, 3,545 唯一)
  - 外键(3):`AWci` (`@23`, `+0x50`→t5)、`AWni` (`@27`, `+0x60`→t10)、`AWmi` (`@41`, `+0x58`→t25)
  - 整数标量(5):`AWre` (`@15`, i16 `+0x7c`, `[0..20]`)、`AWwh` (`@39`, u8 `+0x91`, getter `0xe4a9e7` 抑制 0, 1,901 live `⊂ [1..200]`)、`AWwr` (`@40`, u8 `+0x92`, getter `0xe49af9` 抑制 0, 1,759 live `⊂ [1..200]`)、`AWma` (`@54`, u8 `+0x90`, getter `0xe49ec1` 抑制 `<=0`, 76 live `[14..70] ⊂ [10..99]`)、`AWmg` (`@53`, u8 `+0x93`, getter `0xe4a9a6` 抑制 `<=0`, 958 live `⊂ [1..100]`)
  - 颜色 RGB555(3,由 `0x4330ce0` 块读):`AWfc` (`@4`, `+0x18`)、`AWbc` (`@6`, `+0x1c`)、`AWtc` (`@8`, `+0x20`),全行 bit 15 = 0
  - 打包日期(2):`AWda` (`@19`, `+0x48`, 0 非法日期, `1900..2024`, 253 非默认)、`AWad` (`@60`, `+0x4c`, 0 非法日期, `1900..2024`, 374 非默认)
  - 布尔位标志(2,共享 `@49`/`+0x8d`):`AWus` (bit 0, 211 true)、`AWop` (bit 1, 73 true)
  - 枚举(8):`AWrb` (`@35`, `+0x85`)、`AWsr` (`@46`, `+0x84`, 跳转表 `0xe4c1f4[15]`)、`AWss` (`@47`, `+0x87`, 跳转表 `0xe4c1f4[16]`)、`AWap` (`@50`, `+0x88`)、`AWrt` (`@51`, `+0x89`)、`AWvf` (`@52`, `+0x8a`)、`AWpo` (`@55`, u32 `+0x78`)、`AWnp` (`@59`, `+0x8b`)。注:`AWARD::fixup (0x3a96273)` 与内联循环 `0xf50de3` 在 `AWmi` 指向 `comp UID 0x5f5e117` 时写 `+0x83=6` 与 `+0x89(8->7)`,wire 层仍按原字节校验。
- **7 项 `held`**(均有精确静态 getter/setter/reader 链,但按三重闸门纪律因数据侧越界或全抑制留 `held` 并附首反例):
  1. `rdui` (`@72`, `+0x10`):`DATABASE_RECORD::get 0xfe38a2` 在 `[+0x0c]==[+0x10]` 时抑制输出,3,545/3,545 全抑制(0 live;首反例 row 0, `duni=102406`)。
  2. `AWsc` (`@2`, `+0x80`, 跳转表 `0xe4c1f4[0]`):raw `movsx`,138 行值为 `0` 越出 `enums['AWsc']={1..8}` (首反例 row 133, `duni=109370`, raw `0`)。
  3. `AWty` (`@17`, `+0x81`, `0xe4aca7`):raw `movsx`,21 行越出 `enums['AWty']` (`{17:4, 20:12, 21:2, 32:3}`;首反例 row 504, `duni=788823`, raw `20`)。
  4. `AWdr` (`@18`, `+0x82`, `0xe4abdd`):raw `movsx`,33 行越出 `enums['AWdr']` (`{7:31, 9:2}`;首反例 row 355, `duni=136504`, raw `7`)。
  5. `AWfo` (`@37`, `+0x8e`, `0xe49b78`):raw `movsx`,3,028 行越出 `enums['foms']` (`{0:3027, 64:1}`;首反例 row 0, `duni=102406`, raw `0`)。
  6. `AWxa` (`@38`, `+0x8f`, `0xe4ad0c`):getter 仅抑制 `<=0`,366 live 行中 2 行越出 `[10..99]` (`val=7` 与 `val=100`;首反例 row 665, `duni=5314319`, raw `7`)。
  7. `AWbr` (`@45`, `+0x83`, `0xe49f99`):raw `movsx`,7 行值为 `9` 越出 `enums['AWbr']={0..8}` (首反例 row 3425, `duni=2000256044`, raw `9`)。
- **7 项非 wire / 子表**:`NDBC`/`FDBC` (editor_metadata)、`dbnm`/`dAPw` (non_wire_computed)、`AWna` (`+0x30`, `0xe4ada2`)/`AWsn` (`+0x38`, `0xe4a3dc`) (non_wire_language_layer,`AWARD::read` 不读入)、`AWsh` (subtable_backed:getter `0xe4a37a` 调 `0x4338030` 扫描 `table_12 AWARD_HISTORY` 28,597 行匹配 `[rec+0x18]==award_ptr`)。
- **10 项内部 wire 槽**(实现 64B body + 12B identity 100% 无缺口闭合):`@0 (+0x7e=0)`、`@1 (+0x7f=0)`、`@3 (colour_ver=1)`、`@10 (+0x24=0)`、`@12 (+0x28=0)`、`@14 (+0x2c=1)`、`@31 (+0x68→t47)`、`@36 (dSAw=0)`、`@48 (+0x8c, 0..50, 613 非零)`、`@64 (ordinal 0..3544, 即 `fm24_dump` 旧标 `rdui@64`)`。

---

## 3. `language` (`table_8.dat`, 126 行, 双档逐字节同构)

### 3.1 先补 L2:17B 后缀 + 13B Identity 逐列剖析与锚点

- **行框闭合**:`client == server` (`5,248 B`, SHA-256 `0c8fbbb7875632f780b12b3e33520abe3cf3ae73fc6830649f51aa5b17b43eb2`),`13 + Σ(1B sel + lstr + 17B suf + 12B id) + 9 = 5,248`,126/126 闭合。
- **L2 多表 FK 候选矩阵**(`domain_stats.json["language_8"]["l2_column_profile"]`):
  - `suf+9..12` (`Lnat`):121 live (`[0..247]`),5 `0xffffffff` null,1 合法 `0`;最紧致拟合 `t10` (`top/N = 0.9841`, wrong-UID 对照仅 49/121 命中,72 miss);跨表具名锚点 **Chinese (row 3) → `55` (China PR)**、**English (row 7) → `139` (England)** 与既有 L2 锚点 100% 交叉相洽!
  - `suf+13..16` (`+0x30`):126 行无 null (`[1..2,000,254,976]`),0 表序数拟合;121/126 行等于 `duni`,仅 5 个后增语言 (`Uyghur/Hakka/Belarusian/Igbo/Hausa`) 为旧版遗留语言 ID (`2000005181..2000254976`),由 `LANGUAGE::read (0x3d547ee)` 传入 `0x1037880`。

### 3.2 L3 静态升级结果 (`language.xml` 12 字段: 5 L3 / 4 held / 3 non-wire)

- **5 项 L3**(0 违例):
  - `duni` (`suf+21..24`, `+0x0c`, `0xfe3912`)
  - `Lnam` (`lstr@0`, `+0x18`, get `0x1038bcb` / set `0x1039188` / read `0x3d546e4`;126/126 非空合法 UTF-8;注:code 在 `language.xml` 与 `local region.xml` 出现 2 次,由 `LANGUAGE` vtable `0x141888db8` 唯一限定)
  - `Linf` (`suf+1`, i8 `+0x3b`, `[0..20]`, get `0x1038da1` / set `0x10392e2` / read `0x3d54721`)
  - `Ldff` (`suf+2`, i8 `+0x3c`, `[0..20]`, get `0x1038b54` / set `0x103914f` / read `0x3d54742`)
  - `Lnat` (`suf+9..12`, i32 `+0x28`→`t10` via `[db+0x28]` in `LANGUAGE::fixup 0x3d550b1`, get `0x1038cc1` / set `0x103930d` / read `0x3d547b6`, 121 live / 5 null / 0 miss)
- **4 项 `held`**(精确静态链 + 首反例):
  1. `rdui` (`suf+25..28`, `+0x10`):126/126 全抑制(首反例 row 0 `Albanian`, `duni=1`)。
  2. `Lfam` (`suf+3..4`, i16 `+0x34`, `0x1038dfd` raw `movsx`):1 行值为 `0` 越出 `enums['Lfam']={1..109}` (首反例 row 120 `Hausa`, `duni=122`, raw `0`)。
  3. `Lgro` (`suf+5..6`, i16 `+0x36`, `0x1038c62` raw `movsx`):11 行越出 `enums['Lgro']={1..22}` (`0` 及 `23..31`;首反例 row 16 `Korean`, `duni=17`, raw `23`)。
  4. `Lsub` (`suf+7..8`, i16 `+0x38`, `0x1038cde` raw `movsx`):17 行越出 `enums['Lsub']={1..24}` (`0` 及 `25..34`;首反例 row 65 `Dzongkha`, `duni=67`, raw `25`)。
- **3 项非 wire**:`NDBC`/`FDBC` (editor_metadata)、`dbnm` (`0x1038a5b` 计算返回 `+0x18`,含 `+0x30 ∈ {0xf4241, 0xf4244}` 特判)。
- **3 项内部 wire 槽**(17B suf 全闭合):`suf+0 (+0x3a=0)`、`suf+13..16 (+0x30 遗留 ID)`、`suf+17..20 (ordinal 0..125, 即 `fm24_dump` 旧标 `rdui_suffix@17`)`。

---

## 4. `derby` (`table_18.dat`, 1,567 行, client 36B / server 42B) — t76c 升 L3

### 4.1 静态文法与关键对账 (`R3`)

`DERBY::read (0x3d00950)` 逐字节闭合 `client (139,891 B)` 与 `server (149,293 B)` 全部 1,567 行,并确立 4 条核心静态裁决:
1. **永远读 4 个 `lstr`**:精确顺序为 **`Dnam` (`+0x18`) → `Dsnm` (`+0x20`) → `Dasn` (`+0x28`, Alternative Short Name) → `Danm` (`+0x30`, Alternative Name)**(注:`Dasn` 在 wire 中位于 `Danm` 之前);`t74` 观察到的 `k ∈ {2, 4}` 实为 `1,446/1,567` 行后两串 `len=0` 所致。
2. **Server-only +6B 精确顺序与门控**:`0x3d00aae` 处 `test bpl, bpl` 门控 3 个 `i16` 成员依次读入——**`D1tw` (`s@28..29`, `+0x70`) → `D1td` (`s@30..31`, `+0x72`) → `D1tl` (`s@32..33`, `+0x74`)**,将 `t76c (E118)` 的无序组 L2 升级为有序精确 L3(全档 903 行同为 `-1` null,664 行 live 且 `0..232 / 0..231 / 0..247 ⊂ [0..10000]`)。双档共有 36B+12B+4 lstr 逐字节 100% 相等。
3. **`Dtm1/Dtm2` 纠偏为 `table_24` (`TEAM`)**:`t76c` 数据侧拟合 `club (84,259)`,而 `DERBY::fixup (0x3d00fc0)` 在 `0x3d00fe4`/`0x3d01007` 读取 **`[db+0x98]` = `table_24` (`TEAM`, 84,507 行)** 调 `0x140f7ee40 (0x3bf3460)` 解析,且 `DERBY::get` 输出 4CC `'Ttea'`,与 `derby.xml` `database_table_type="team"` 完全一致(`Dtm1` 1,567 live / 0 null,`Dtm2` 1,566 live / 1 null,均 0 miss;wrong-UID 对照分别 888 / 977 miss)。
4. **尾部双对精确落位与笔误纠偏**:`Dfg1@c28/s34 (+0x76)`、`Dfg2@c29/s35 (+0x77)`(1,034 同空 `-1`,533 live `0..11/0..10`),`Dwdr@c34/s40 (+0x7c)`、`Dntr@c35/s41 (+0x7d)`(`0..200`,修正 `slots_client_18.json` 中笔误 `36`)。

### 4.2 L3 汇总 (`derby.xml` 22 字段: 18 L3 / 1 held / 3 non-wire)

- **18 项 L3**(0 违例):`duni`、`Dnam/Dsnm/Dasn/Danm`、`Dfmd` (`num@0`, `+0x60`, `1872..2022`, 0 非法日期)、`Dtm1` (`@4`, →t24)、`Dtm2` (`@8`, →t24)、`Dfmc` (`@12`, →t25, 402 live / 1,165 null)、`Dfms` (`@16`, →t21, 137 live / 1,430 null)、`Dfma` (`@20`, i32 `<0` null, 134 live `[15..82100] ⊂ [0..200000]`)、`D1tw/D1td/D1tl` (`s@28/30/32`, server-only)、`Dfg1/Dfg2` (`c@28/29` = `s@34/35`)、`Dwdr/Dntr` (`c@34/35` = `s@40/41`)。具名锚点核对通过:row 0 `Merseyside` (1894, `WDL=67/77/96`)、row 388 `Manchester` (1891)、row 395 `North London` (1909)。
- **1 项 `held`**:`rdui` (`c@44/s@50`, `+0x10`, 1,567/1,567 抑制;首反例 row 0 `Merseyside`, `duni=162233`)。
- **3 项非 wire**:`NDBC`/`FDBC`、`dbnm` (`0xffd478` 返回 `+0x18`)。
- **3 项内部 wire 槽**(36B/42B 全闭合):`num@24..27` (`+0x68`, 内部 4CC `rpdr` → `t25`, 全 `-1`)、`c@30..33/s@36..39` (`+0x78..+0x7b`, 全 `0`)、`c@36..39/s@42..45` (ordinal `0..1566`)。

---

## 5. `weather` (`table_27.dat`, 334 行, 双档逐字节同构) — t76c 升 L3 与两项关键纠偏

### 5.1 四重静态证据纠偏 `R1` (wind/precip 互换) 与 `R2` (`sd` 2B i16 + `dn@blk+22`)

`WEATHER::read (0x158b970)` 精确证实 `t76c` 的 `95B = 3B zero (+0x80..+0x82) + 4 × 23B` 块划分 (`WEATHER+0x20`, 步长 `0x18`, 尾 1B 内存对齐填充),但四重静态链 (`WEATHER::read` + `WEATHER::get 0x158e6b0` + `WEATHER_SEASON::get 0x158f1d0` + `WEATHER::set 0x15901a0`) **明确纠正了两处上游 L2 错配**:

1. **`R1` — 纠正 `t01l(E27)` 与 `t76c(E118)` 的风力/降水互换**:
   - **`blk+2..+6` (`season+0x02..+0x06`, `mid+5..9 + 23b`) 实为 `w{b}w0..w4` (WIND, 内部 4CC `win0..win4`)**:`WEATHER_SEASON::get 0x158f30c` 读 `byte ptr [rcx + 2]` (`win0`),`WEATHER::set 0x15903ef` 写 `[r14 + 0x22]` (`w0w0`)。
   - **`blk+7..+11` (`season+0x07..+0x0b`, `mid+10..14 + 23b`) 实为 `w{b}p0..p4` (PRECIPITATION, 内部 4CC `pre0..pre4`)**:`WEATHER_SEASON::get 0x158f28e` 读 `byte ptr [rcx + 7]` (`pre0`),`WEATHER::set 0x15902f0` 写 `[r14 + 0x27]` (`w0p0`)。
   - **读后归一化器 `0x43e7e10` (thunk `0x158bd70`) 复证**:分别检查 `[+2..+6]` (全档 1,336 季节块中 **76** 块和 `!= 100`,回写 `[+2]`)、`[+7..+11]` (**67** 块和 `!= 100`,回写 `[+7]`)、`[+12..+21]` (**468** 块和 `!= 100`,回写 `[+17]`)。
2. **`R2` — `w{b}sd` 为 2B `i16` 且 `w{b}dn` 落在 `blk+22` (NULL 哨兵 `0x64`)**:
   - `t76c` 将 `blk+0..1` 拆成 `1B w{b}sd + 1B w{b}dn ({0,1})` 并把 `blk+22 ({0,100})` 留空。静态证实 **`blk+0..1` (`season+0x00`) 是 2B `i16` `w{b}sd`** (`0..359 ⊂ [0..365]`, 当 4 季 `sd` 全等时 `0x158bd07` 重置为 `55/145/230/300`, 命中 12 行);**`blk+22` (`season+0x16`) 正是 `w{b}dn` (`tend`)**,`WEATHER_SEASON::get 0x158f3e5` (`cmp edi, 0x64`) 与 `WEATHER::set 0x1590498/a2f/a5b/a87` 明确将 **`0x64 (100)` 作为显式 NULL 哨兵**(20 行干旱/热带区为 100 抑制,其余 314 行 live 值全为 `0 ∈ [0..50]`)。

### 5.2 L3 汇总 (`weather.xml` 94 字段: 90 L3 / 1 held / 3 non-wire)

- **90 项 L3**(0 违例):`duni` (`mid+99..102`)、`wnam` (`lstr@0`, `+0x18`, 334/334 非空 UTF-8)、以及 4 季 × 22 字段 (`w{0..3}{sd, w0..w4, p0..p4, te, tv, t0..t7, dn}`, 共 88 项,全部经 12 张 get 跳转表 + 12 张 set 跳转表 + 标量 cmp 双链闭合)。
- **1 项 `held`**:`rdui` (`mid+103..106`, `+0x10`, 334/334 抑制;首反例 row 0 `English Coastal`, `duni=1`)。
- **3 项非 wire**:`NDBC`/`FDBC`、`dbnm` (`0xfe375d` 虚拟名)。
- **2 项内部 wire 槽**(95B mid 全闭合):`mid+0..2` (`+0x80..+0x82`, 全 `0`)、`mid+95..98` (ordinal `0..333`)。

---

## 6. `media` (`table_7.dat`, 208 行, client 36,824B / server 38,280B) — 中段嵌套文法静态闭合

### 6.1 完整 20 步变长文法 (`MEDIA_SOURCE::read 0x15457c0`) 与双档 +7B 差额证明 (`R4`)

`t74` 记载 `media` 中段嵌套 count/list 未解且 server 每行多 7B。静态反汇编 `MEDIA_SOURCE::read (0x15457c0)` 完整给出全部 20 步顺序文法,数据侧在 `client (36,824 B)` 与 `server (38,280 B)` **208/208 行逐字节闭合至 EOF-9**:

| 步序 | 字段 / 内部槽 | 归档范围 | Wire 文法 | 成员偏移 | Reader `fo` | Fixup / 目标 | 数据侧统计 (208 行) | 评级 |
|---:|---|---|---|---|---|---|---|---|
| 1 | `Mnam` | 双档 | `lstr` | `+0x18` | `0x15457dc` | — | 208/208 非空 UTF-8 | **L3** |
| 2 | *(内部)* | 双档 | `u8` | `+0xd1` | `0x15457f9` | — | 全 `0` | internal |
| 3 | `Mtyp` | 双档 | `u32 cnt + u8[cnt]` | `+0x30..40` | `0x15458b2` | item get `0x4381840` | 235 项 (`{1:181, 2:27}`),全落 `enums['Mtyp']` | **L3** |
| 4 | `Murl` | 双档 | `lstr` | `+0x20` | `0x1545904` | — | 203 非空 / 5 空, 0 UTF-8 错 | **L3** |
| 5 | `Mhtg` | 双档 | `lstr` | `+0x28` | `0x1545921` | — | 208/208 空串 `""` (getter 无抑制) | **L3** |
| 6 | `Misf` | 双档 | `u8` bool | `+0xd2` | `0x154593e` | — | 208/208 `0` (False, getter 无抑制) | **L3** |
| 7 | `Msty` | 双档 | `i8` enum | `+0xd0` | `0x1545962` | — | 全落 `enums['Msty']={0..6}`, 0 违例 | **L3** |
| 8 | `Mcmi` | 双档 | `u32 cnt + i32[cnt]` | `+0x48..58` | `0x15459a4` | `[db+0x18]`→`t25` | 196 项 / 49 行非空, 0 miss (wUID 139 miss) | **L3** |
| 9 | `Mcyi` | 双档 | `i32` | `+0xc0` | `0x1545afd` | `[db+0x08]`→`t2` | 65 live / 143 null, 0 miss (wUID 13 miss) | **L3** |
| 10 | `Mrgi` | 双档 | `u32 cnt + i32[cnt]` | `+0x78..88` | `0x1545b3f` | `0x3bf5e90`→`t47` | 6 项 / 6 行非空, 0 miss (wUID 6 miss) | **L3** |
| 11 | `Mnti` | 双档 | `u32 cnt + i32[cnt]` | `+0x60..70` | `0x1545bbf` | `[db+0x28]`→`t10` | 237 项 / 127 行非空, 0 miss (wUID 110 miss) | **L3** |
| 12 | `Mcti` | 双档 | `i32` | `+0xc8` | `0x1545c1d` | `0x3bf4a90`→`t5` | 95 live / 113 null, 0 miss | **L3** |
| 13 | `Mcli` | 双档 | `u32 cnt + (u32 u1, u32 u2, lstr)[cnt]` | `+0xa8..b8` | `0x1545c6a` | item `0x154dc00` (`club`/`curl`), UID→`t3` | **450 项 / 129 行**:450/450 `u1==u2` 且 **450/450 命中 `t3` CLUB UID 集**(错用序数 132 miss),187 非空 `curl` | **L3** |
| 14 | `Mper` | **server 独有** (`0x1545cfe`) | `i8` enum | `+0xf0` | `0x1545d0b` | — | 2 行 raw `0` 越出 `{1..15}` (首反例 row 116 `Cofina Media S.A`) | **held** |
| 15 | `Mscp` | **server 独有** (`0x1545cfe`) | `i8` enum | `+0xf1` | `0x1545d2f` | — | 6 行 raw `0` 越出 `{1..7}` (首反例 row 137 `Stoke-on-Trent Live`) | **held** |
| 16 | `Mdlp` | **server 独有** (`0x1545cfe`) | `u32` date | `+0xd4` | `0x1545d4f` | — | getter `0x154803d` 抑制 `1900-01-01`,208/208 全抑制 (0 live) | **held** |
| 17 | `Mjor` *(内部)* | **server 独有** (`0x1545cfe`) | `u8 cnt + i32[cnt]` | `+0xd8..e8` | `0x1545d88` | `0x3bf9220` | 208/208 `cnt == 0` → 恰好占 1B | internal |
| 18 | `Mlnm` | 双档 | `u32 cnt + i32[cnt]` | `+0x90..a0` | `0x1545e0d` | `0x3bf5fd0`→`t7` | 22 项 / 16 行非空 (`{0:192, 1:12, 2:3, 4:1}`), 0 miss | **L3** |
| 19 | `Mapc` | 双档 | `u8` bool | `+0xd3` | `0x1545e72` | — | 176 true / 32 false, 0 违例 | **L3** |
| 20 | `ord/duni/rdui` | 双档 | `12B` identity | `+0x08/+0x0c/+0x10` | `0x3c600f0` | — | `duni` **L3** (208 唯一) / `rdui` **held** (208 抑制) | L3/held |

- **Server 每行 +7B 精确闭合**:`0x1545cfe` 门控的 server 块 = `1B Mper + 1B Mscp + 4B Mdlp + 1B u8 cnt_jor (=0 on 208/208)` = **恒为 7B**,`36,824 + 208 × 7 = 38,280 B` 逐行精确相等。
- **Identity 前 5B 的 16 种取值完全解开**:紧接 12B identity 之前是 `Mlnm` (`u32 cnt + i32[cnt]`) + `u8 Mapc`:
  - `cnt_lnm == 0` 的 **192 行**:前 5B 为 `u32(0) + u8(Mapc)`,仅 2 种取值(`0000000001` ×161、`0000000000` ×31)。
  - `cnt_lnm > 0` 的 **16 行**:前 5B 为 `u32(末个 Mlnm 序数) + u8(Mapc)`,共 14 种不同取值(其中 `4000000001` 出现 3 次,其余 13 种各 1 次)。
  - 合计 **`2 + 14 = 16` 种**,与 `t74` 数据侧观测 100% 闭环!

---

## 7. 既定锚点对账与负结果保留

1. **`R1–R5` 全部机器可读入账于 `field_map.json["reconciliations"]`**:涵盖 weather 风/降水互换纠偏 (`R1`)、weather `sd` 2B + `dn@blk+22` (`R2`)、derby `TEAM` FK + server +6B 有序定型 + 4 lstr 序 + `slots_client_18.json` 36 笔误纠偏 (`R3`)、media 20 步文法 + +7B 差额 + 5B 16 取值闭合 (`R4`)、`fm24_dump` `award.rdui@64` / `language.rdui_suffix@17` 实指行序数 (`+0x08`) 而原生 `rdui (+0x10)` 位于 `@72` / `suf+25` 并与 `duni` 相等被抑制 (`R5`,与 E20/E117/E120 完全一致)。
2. **`t57/t63` 既有负结果不翻案**:本任务不触碰三主表主行,保留原条目不动。
3. **17 项 `held` 原样保留并附精确首反例**:候选或带违例项绝不升 L3;业务名全部直接沿用 `master.json`,未发明任何字段名。
4. **L4 = 0**:全程只读外部文件与 `editor.exe`,未启动游戏/编辑器/IDA,未接触 `Z:`。

---

## 8. 独立校验、回归与交付清单

- `scripts/t83_five_tables_l3.py --selftest --build`:5/5 selftest PASS,退出码 0。
- `scratch/t83/out/verify.py --selftest`(严格独立:AST + `sys.modules` 断言 0 禁止 import,不 import builder / `t05_pe` / `fm24_dump` / `t73` / `t81`):
  - **11/11 核心校验全过**(含 5 类 RTTI/vtable/factory + **741** 条 `editor.exe` 指令字节/rel32 逐条复核、17 张参考表独立后向 DP UID 索引且双档一致、10/10 t74 + 4/4 t76c SHA-256、五表双档全行重放与 17 项 `held` 首反例直验)
  - 合成篡改负测试 PASS(拦截非闰年 day 366 与篡改 L4 等级),退出码 0。
- `scripts/t01_anchors.py`:**7/7 PASS**(无回归)。

| 交付文件 | 字节数 | SHA-256 |
|---|---:|---|
| `scripts/t83_five_tables_l3.py` | — | builder (`--help` / `--selftest` / `--build`) |
| `scratch/t83/out/field_map.json` | 214,345 | `3a2db1496cd2c5217a03ec9f4ab5abf805b8ca727080491acc98e0157908969d` |
| `scratch/t83/out/domain_stats.json` | 103,607 | `0591f0d7c6777892e5741b314d091b234bb0f59566b4eb613d60f2c0160c26a9` |
| `scratch/t83/out/xref_award.json` | 43,543 | `8df44b9e1bb3ad6d4ac5e5fbb8d0dfdcda4d27765362222169f060f6d5451134` |
| `scratch/t83/out/xref_language.json` | 13,310 | `8bc82612d9b5592b9b056c42756175f7652af0cb84d3d857dcb48d007b2868a0` |
| `scratch/t83/out/xref_weather.json` | 105,745 | `f278729c0a202ba1193231ba6c116eebae91e518ba4aa2e87cda5b1de88c5209` |
| `scratch/t83/out/xref_derby.json` | 24,518 | `97f2106091dd7d11bc51bb8fb37732ff5195dc58a8e541b2ae92dc482def0a10` |
| `scratch/t83/out/xref_media.json` | 27,091 | `dcc3d4a40ca9588d03f4d1318862748a4cf8269ccfa15222d18475704fbe95f9` |
| `scratch/t83/out/verify.py` | — | 独立校验器 (`--help` / `--selftest`, 11/11 PASS) |
| `scratch/t83/out/REPORT.md` | — | 本文 |
| `scratch/t83/out/DONE.md` | — | 完成标记 (`DONE type=t83 status=complete`) |
