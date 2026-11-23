# t82 — `table_extra_3.dat` 剩余载荷命名：双对象闭合、35 项新 L3 与 `CBW*/CBD*` 负证

## 0. 摘要与证据口径

- **静态二进制(只读)**:`D:/tmp2b/fm24/input/editor.exe`,SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。下文全部地址为 **PE file offset**,对应 VA 与原指令字节全量载入 `xref_extra3.json` 与 `field_map.json`。
- **冻结输入校核(`evidence/MANIFEST.json`)**:
  - `evidence/fm24/reports/editor_schema/master.json`:`7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`
  - `evidence/fm24/reports/dbdat_decode/db_tables_big.json`:`c57b2b6837a3dcca106bf4363da105eca7665df407b738483839d1b7b6de3ddf`
  - `scratch/t57/out/field_map.json`:`0b04de7b15c455ccb85212d43221d5cbecb8fd5ccbf830ba71d5f4f3011f3664`
  - `scratch/t63/out/field_map_r2.json`:`5bdf1fc6e35c6c0cabe666a0e173228f6127a770392b73ca8d23b0a35c24dd46`
  - `scratch/t71/out/chain.json` / `field_map_r3.json` / `rows_extra3.json`:SHA-256 全验通过。
- **数据面范围(全档向量化,无抽样)**:
  - `client_db/table_extra_3.dat`:`84,259` 行,`13,053,908 B`(12B header + rows + 0B footer),逐字节闭合至 EOF。
  - `server_db/table_extra_3.dat`:`84,259` 行,`35,009,248 B`(12B header + rows + 0B footer),逐字节闭合至 EOF。
  - 外键对照表:`table_3.dat` (`84,259` clubs)、`table_25.dat` (`7,047` comps)、`table_23.dat` (`278` stage_names)、`table_45.dat` (`84,477` `STARTING_RECORD`)。
- **边界与纪律**:排除 t71 已转正的 **24 项** (`Cyfn[26]`, `Cebd[48]`, 22 `cnst[155..176]`);不翻案 t57/t63 任何负结果 (`superseded_prior_negatives = []`);不发明业务名(仅记静态 4CC、冻结 schema 名与物理槽);**L4 = 0**(未启动游戏/编辑器/IDA,未访问 `Z:`,未联网)。

### 总收获一览

| 分类 | 计数 | 明细 |
|---|---:|---|
| **新转正 `L3`** | **35** | **31 标量/实数/串**(`Ctlv, Cmle, Cyim, Cyfb, Cytv, Crcb`, `Cetl, Cmtm, Cect, Cemn, Cemx`, `Csly, Csps, Cspt, Csaf, Cste, Cspe`, `Cuf1..Cuf9, Cf10`, `Catd, Cmna, Cmxa`, `TCht`) + **4 列表/多态**(`Cbbl, Csoc, pcpt, CPsL`) |
| **`held`(均附首反例)** | **39** | 1 越界标量(`Csth`) + 4 无作用域枚举(`CScP, Cown, Chti, Cepr`) + 4 越界阵型(`Cpfr, C2pf, Cdfo, Cafo`) + 1 全零条件串(`TCnn`) + 4 重复 XML 颜色(`ttcl×2, tbcl×2`) + 10 只读派生色(`1scl..3tbc`) + 5 列表越界/缺子枚举(`Cscm, Cspb, Cren, Camc, TCrs`) + 6 球衣容器无 `list_item_fields`(`Tko1..3, Tkg1..3`) + 4 保留 t63 `held`(`CssT..E`) |
| **t71 已转正(本轮排除)** | **24** | `Cyfn[26]`, `Cebd[48]`, 22 `cnst[155..176]`(重叠 = 0) |
| **负证：非 `table_extra_3`** | **131** | **117** `club.xml[211..327]` 记录族(含 **`CBW*/CBD*`**) → **`server_db/table_45.dat` (`STARTING_RECORD`)**;**14** 其它非 extra_3 字段(`Csxn/Cl3n/Ca3n`, `Crkt`, `C1sq`, 保留 t63 `held` `Cmls`, `Cdbt/Cffp/Clhs/CAmb/Cmti/Cwcl/Coin/Calt`) |

---

## 1. 关键负证：`CBW*/CBD*` 与全部 117 个俱乐部记录 4CC 不在 `table_extra_3.dat`

- **静态链(`editor.exe`)**:
  - `TC_GET2` (`0x11f0690`) 通过 `0x11f0ca7` (`lea eax, [rsi - 'CBDa']`) / `0x11f0cb6` (`lea eax, [rsi - 'CBWa']`) 等记录族开关汇聚至 `0x11f2a76 → 0x11e8af0`,与 `CLUB_GET` (`0xe89a00`) 汇聚点 `0xe8f1d9 → 0x11e8af0` 共同调用 **`TC_RECORD_GET @ 0x3ebad50`**;对应写路径 `TC_SET2` (`0x11f495b` `CBDa` / `0x11f496b` `CBWa` → `0x11f5473 → 0x11e8b40`) 落入 **`TC_RECORD_SET @ 0x3ebaf50`**。
  - `TC_RECORD_GET @ 0x3ebad50` **完全不访问 `CLUB+0x100` 或 `CLUB+0xb0`**;其首条指令加载全局指针 `VA 0x141b60190` (`fo 0x1b5f190`),遍历 `[table+0x80]` 向量,按 `[rec+0x4c] == [CLUB+0xc]` 且 `[rec+0x5e] == rec_type` 匹配后转发至 `RECORD_GET @ 0x1543ca0` (`RECORD_SET @ 0x1544c80`)。
  - **表号自证**:`0xf06c70..0xf06c84` 以 `mov edx, 0x2d` (**table type `45`**) 调用 `DATABASE_TABLE` 构造函数并安装 vtable `VA 0x141881d08` (`fo 0x1881308`),其 COL/RTTI (`fo 0x1aadf50`) 为 **`.?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@@db@@`**。
  - **数据核验**:`server_db/table_45.dat` 实际存在 (`7,608,748 B`, **`84,477`** 条记录)。因此 `CBWa/CBWc/CBWd/CBWf/CBWo`、`CBDa/CBDc/CBDd/CBDf/CBDo` 以及 `club.xml[211..327]` 全部 **117** 项记录字段在 `table_extra_3.dat` 中占 **0 字节**。
- **其它非 `extra_3` 负证(14 项)**:
  - `Csxn[8] / Cl3n[9] / Ca3n[10]`:虽驻留 `CLUB+0x100 -> +0x00/+0x08/+0x10`(ctor `0x3aaba20` 置空),但 `CLUB_EXTRA_READER 0xe5d210` **从不从 wire 读取这三个偏移**。
  - `Crkt[177]`:无 getter;`CLUB_EXTRA_SET 0xe5820f → 0xe586a0` / `TC_EXTRA_SET 0x11cfa99` 为随机化球衣命令动作,非持久化布尔槽。
  - `C1sq[129]` (`CLUB_GET 0xe8d9f0 → 0x11f41d0` 转发首队 `Tsqi`)、`Cmls[432]` (`0x3ebf730` 读 `COMP+0xb0`,保留 t63 `held`)、`Cdbt/Cffp/Clhs/CAmb/Cmti/Cwcl` (独立全局表)、`Coin` (`CLUB+0x130`)、`Calt` (`CLUB+0xa8`) 均不在 `table_extra_3.dat`。

---

## 2. 双对象架构与 100% 字节闭合台账

`table_extra_3.dat` 单行流经 `0xe5d210` (`CLUB_EXTRA_READER`) 依次填充两个对象:
1. **`CLUB+0x100` (`CLUB_IN_GAME_DATA`, `0x130 B`, ctor `0x3aaba20`, fixup `0x3aae490`, writer `0xe5f3d0`)**:mode 1 (server) 读 23 段 server-only 前缀后汇入公共 `+0xd8(u16 Cyfn)` / `+0xcc(u32 TCoi)`;mode 0 (client) 跳过前缀直落 `+0xd8/+0xcc`。
2. **`CLUB+0xb0` (`TEAM_CONTAINER_IN_GAME_DATA`, `0xb0 B`, reader `0x11d3200`, fixup `0x3ea1030`, writer `0x11d53f0`)**:先读 6 段双档公共尾(`+0x90` 跳过/`+0xac`/`+0x98`/`+0x78`/`+0xa0`/`+0xa8`),server 再读 6 段 server-only 尾(`+0x18`/`+0x30`/`+0x74..77`/`+0x68..70`/`+0x00` 虚分派/`+0x48`)。

### 档位、Sentinel 与构造默认严格分列

- **双档公共尾 100% 逐字节相等**:`client_db` 与 `server_db` 全部 84,259 行的公共尾流(`+0xd8/+0xcc/+0xac/+0x98/+0x78/+0xa0/+0xa8`) SHA-256 完全一致 (`b95acf0b89ccbff5...`)。**不存在 client-only 字段**。
- **`0xffffffff` (`-1`) 与合法 `0` 分列**:
  - `+0xcc` (`TCoi` 内部槽):双档各 **84,259 / 84,259 个 `0xffffffff`**,**0 个 `0`**。
  - `Csth` (`+0xc0`):构造默认 `-1`;全档 **80,279 个合法 `0`**,**3 个 `-1` (`0xffffffff`)**(首反例 row `69,706`,违背 `min_value=0`,故 `held`)。
  - `Cspb.matc`:`44` 个 `-1` 由 `0x11f8a49` 抑制,`2` 个有效值 `1`。`Cren.rsnp`:`857` 个 `-1` (无关联球员),`345` 个有效 person ordinal (`0..631,731`)。
- **构造默认与持久化 wire 分列**:
  - `Cmle/Cytv/Crcb` 构造默认 `10`(server wire 中分别有 `2,414 / 934 / 1,458` 行等于 `10`,其余为不同持久化值)。
  - `Catd/Cmna/Cmxa` 构造默认 `10000`(server wire 中仅 `58 / 47 / 549` 行等于 `10000`,`56,183 / 60,544 / 55,567` 行为 `0`)。
  - `+0x10c` 第二套 supporter profile 全档 **84,259 / 84,259 行恒等于构造默认** (`-1,-1,-1, 10×6, 0×6`),无 4CC。
  - `+0x80/+0x84/+0x88[0..5]/+0xa0[0..5]/+0xb8/+0xbc` 及 election `+0x0c` 全部恒为 date4 sentinel `0x076c0001` (`1900-01-01`)。

---

## 3. 新转正 `L3` 字段汇总(35 项)

### 3.1 `CLUB+0x100` 直接标量(6 项,server-only)

| 4CC | XML idx | 对象偏移 | wire 类型 | getter fo | setter fo | ctor 默认 | 全档观测域 (84,259 行) | 违例 |
|---|---:|---|---|---|---|---:|---|---:|
| `Ctlv` | 64 | `+0x120` | `i8` | `0xe8a998` | `0xe581d1` | 0 | `[0..20]`, `0`=36,560 | 0 |
| `Cmle` | 30 | `+0x121` | `i8` | `0xe8c525` | `0xe5830f` | 10 | `[0..20]`, `0`=71,648, `def(10)`=2,414 | 0 |
| `Cyim` | 68 | `+0x126` | `i8` | `0xe8b983` | `0xe58023` | 0 | `[0..20] ⊂ [-1..20]`, `0`=45,839 | 0 |
| `Cyfb` | 66 | `+0x12b` | `i8` | `0xe8b10c` | `0xe58244` | 0 | `[-1..20]`, `-1`=5,628, `0`=37,880 | 0 |
| `Cytv` | 65 | `+0x12c` | `i8` | `0xe8c3f9` | `0xe58030` | 10 | `[-1..20]`, `-1`=3,405, `0`=37,068 | 0 |
| `Crcb` | 67 | `+0x12d` | `i8` | `0xe8bd74` | `0xe58202` | 10 | `[0..20] ⊂ [-1..20]`, `0`=41,511 | 0 |

### 3.2 `CLUB+0x100 -> +0x78` 选举子对象(5 项,server-only 条件段,11,963 行存在)

不变量验证:`elec_club == row_ordinal` **11,963 / 11,963 (100%)**;`elec_flag == 1` 当且仅当 `Cown ∈ {3, 7}` **84,259 / 84,259 (100%)** (`3`:11,597, `7`:366)。`Cebd[48]` 已由 t71 转正,本轮排除。

| 4CC | XML idx | 子对象偏移 | wire 类型 | getter (`ELECTION_GET`) | setter (`ELECTION_SET`) | 存在行观测域 (`11,963` 行) | 违例 |
|---|---:|---|---|---|---|---|---:|
| `Cetl` | 50 | `+0x12` | `i8` | `0xe970a6` | `0x3aeb82f` | `[1..10] ⊂ [0..100]` | 0 |
| `Cmtm` | 51 | `+0x13` | `i8` | `0xe970b2` | `0x3aeb83b` | `[1..100] ⊂ [0..100]` | 0 |
| `Cect` | 52 | `+0x14` | `i8` | `0xe9702f` | `0x3aeb7f8` | `[1..15] ⊂ [0..100]` | 0 |
| `Cemn` | 53 | `+0x15` | `i8` | `0xe9703b` | `0x3aeb804` | `[0..100]` | 0 |
| `Cemx` | 54 | `+0x16` | `i8` | `0xe96fa5` | `0x3aeb7ad` | `[5..100] ⊂ [0..100]` | 0 |

### 3.3 `CLUB+0x100 -> +0xf8` 球迷画像(6 项,server-only,84,259 行)

reader `0x4340450` (ver=`3` 全行一致);`SUPPORTER_GET 0x1520050` 对 `+0x08..+0x0d` 直接无钳位输出,`SUPPORTER_SET 0x43419b0` 写回。内部字段 `CsSF/CsSS/CsST` 全 `-1`,`Cfph..Cfpc` 全 `0`。

| 4CC | XML idx | 子对象偏移 | getter fo | setter fo | 观测域 (84,259 行) | 违例 |
|---|---:|---|---|---|---|---:|
| `Csly` | 149 | `+0x08` | `0x15202a6` | `0x43419ca` | `[1..20] ⊂ [0..20]` | 0 |
| `Csps` | 150 | `+0x09` | `0x15201a2` | `0x43419eb` | `[1..20] ⊂ [0..20]` | 0 |
| `Cspt` | 151 | `+0x0a` | `0x1520311` | `0x43419f3` | `[1..20] ⊂ [0..20]` | 0 |
| `Csaf` | 152 | `+0x0b` | `0x152029a` | `0x43419c2` | `[1..20] ⊂ [0..20]` | 0 |
| `Cste` | 153 | `+0x0c` | `0x152031d` | `0x43419fb` | `[1..20] ⊂ [0..20]` | 0 |
| `Cspe` | 154 | `+0x0d` | `0x15201ae` | `0x43419d2` | `[1..20] ⊂ [0..20]` | 0 |

### 3.4 `CLUB+0x100 -> +0x48` 欧足联系数环形缓冲(10 项,server-only,569 行存在)

`0x39aa1f0` 读入容量 10 环(全 569 存在行均 `tag=1, cnt=10, head=0`),`CLUB_GET` 跳转表 `0xe91db0[0..8]` + `Cf10 @ 0xe8c8fb` 按 `ring[(head+k)%10] / 1000.0` (双精度 `1000.0 @ 0x179f810` 转 `f32`,缺失行返回 `0.0`),`CLUB_SET` 跳转表 `0xe86b54[0..8]` + `0xe842d0` 写回。

- **`Cuf1..Cuf9, Cf10`** (`club.xml[133..142]`, `real [0..50]`):全档 84,259 × 10 = 842,590 格全部有限且落 `[0.0, 36.0] ⊂ [0, 50]`,**0 违例**。

### 3.5 `CLUB+0xb0` 公共尾 + server 尾标量(4 项)

| 4CC | XML idx | 档位 | 对象偏移 | wire 类型 | getter fo | setter fo | 全档域 | 违例 |
|---|---:|---|---|---|---|---|---|---:|
| `TCht` | 12 | **client+server** | `base+0x98` | `u32 len + UTF-8` | `0x11f0831` | `0x11cfa3e` | 799 非空,0 坏 UTF-8,100% 双档一致 | 0 |
| `Catd` | 61 | server-only | `base+0x68` | `i32` (ctor `10000`) | `0x11f13a6` | `0x11cfa06` | `[0..100000] ⊂ [0..1000000]` | 0 |
| `Cmna` | 62 | server-only | `base+0x6c` | `i32` (ctor `10000`) | `0x11f0e42` | `0x11cfa1e` | `[0..75000] ⊂ [0..1000000]` | 0 |
| `Cmxa` | 63 | server-only | `base+0x70` | `i32` (ctor `10000`) | `0x11f0e4e` | `0x11cf976` | `[0..120000] ⊂ [0..1000000]` | 0 |

### 3.6 列表与多态 `base+0x00` 虚分派 `L3`(4 项,server-only)

| 4CC | XML idx | 容器 / 多态 tag / RTTI | 行数 / 条数 | 子字段验证摘要 | 违例 |
|---|---:|---|---|---|---|---:|
| `Cbbl` | 119 | `base+0x00` tag `7` (`PLAYER_BUY_BACK_INFO`, vt `0x18b8608`, rdr `0x42c66f0`) | 57 / 75 | `play` 75/75 正 UID 对;`club` 75/75 合法 `table_3` ordinal (错配 UID 对照 23 miss);`cash` `[0..68,597,168]`;内部日期 `bbsd/bbed` 0 错 | 0 |
| `Csoc` | 120 | `base+0x00` tag `5` (`NEXT_SALE_PERCENTAGE_INFO`, vt `0x18b8768`, rdr `0x42d2710`) | 801 / 2,616 | `play` 2,616/2,616 正 UID 对;`club` 2,616/2,616 合法 `table_3` ordinal (错配 UID 对照 1,068 miss);`perc` `[3..100]` | 0 |
| `pcpt` | 196 | `base+0x00` tag `38` (`TESTIMONIAL_INFO`, vt `0x18b9428`, rdr `0x14da470`) | 26 / 29 | `PtPl` 29/29 正 person UID;`PtLy` 29/29 合法日期 (`2011..2024`,0 sentinel) | 0 |
| `CPsL` | 197 | `extra+0x68` (`tag=2 + 10B`, get `0x1524af0`, set `0xeac360`) | 249 / 694 | `tag=2` & `+8=900` 全 694 一致;`per1/per2` 全部正 person UID (`132,219..2,000,258,263`) | 0 |

*(注:依 `AGENTS.md` 边界,person/PDxx 表不在本任务解码范围,故 `play/PtPl/per1/per2` 完成正 UID 与成对一致检验并明注边界。)*

---

## 4. `held` 项(39 项)与首反例

| 组别 | 4CC [XML idx] | 数量 | `held` 根因与首反例 |
|---|---|---:|---|
| 标量越界 | `Csth[115]` | 1 | `CLUB_GET 0xe8cef0` 无钳位;3 行等于 `-1` (`0xffffffff`) < `min=0`。首反例:row `69,706` (UID `84027591`), raw=`-1` |
| 无作用域枚举 | `CScP[34], Cown[47], Chti[55], Cepr[49]` | 4 | 冻结 `master.json` 中 `enum_ref=None`(沿用 t63 `Cpfa/Chsd` 与 t79 `PLgn` 纪律)。观测域:`CScP` `0..13`, `Cown` `0..8`, `Chti` `0..3`, `Cepr` `0..62` |
| 阵型越界 | `Cpfr[145], C2pf[146], Cdfo[147], Cafo[148]` | 4 | 非零行越出冻结 `pfms/sfms/dfms/afms`:分别 `78 / 90 / 1,441 / 99` 违例;首反例:row `117(64)` / `220(64)` / `20(29)` / `21(64)` |
| 全零条件串 | `TCnn[11]` | 1 | 受 `CLUB+0xba != 0` 门控,双档 84,259 行全 0 跳过(0 样本) |
| 重复 XML 颜色 | `ttcl[24,76], tbcl[25,77]` | 4 | 冻结 `club.xml` 重复出现(不通过 Gate 1)且 `6,586` 行为 `0x00000000` 回退至 `base+0x78` |
| 只读派生颜色 | `1scl..3sbc, 2tcl..3tbc [70..75,78..81]` | 10 | 无 setter;经 `0x3ae7420/0x11dc460/0x150d300` 从父俱乐部与 `base+0x78` 球衣派生 |
| 列表子项违例 / 缺枚举 | `Cscm[104]` | 1 | `stco` 15,360/15,360 命中 `table_25`、`stnm` `[1..38]`,但 **118 / 15,360** 项 `slsn=(0,0)` (`0xfe68ca` 仅将 `<0` 置空),不在 `table_23` (`min UID=1`);首反例:row `51` (`stco=136544, stnm=30, slsn=0`) |
| 列表子项缺枚举 | `Cspb[86], Cren[199]` | 2 | `Cspb`:46 项 `cmid/matc/stdt/endt` 0 违例,子字段 `type/venu` 缺 `enum_ref`;`Cren`:1,202 项 `rsnn[1..99]` & `rsnp` 0 违例,子字段 `rsnr` 缺 `enum_ref` |
| 列表子项违例 + 缺枚举 | `Camc[121], TCrs[201]` | 2 | `Camc`(tag 6):`973/1,601` 项 `apfr=0 < min=1`(首反例 row `35`) 且 `type` 缺 `enum_ref`;`TCrs`(`base+0x48`):`2,709/23,027` 项 `PUnJ` 越出 `ftjn`(首反例 row `21, PUnJ=247`) 且 `PUnI/PUnT` 缺 `enum_ref` |
| 球衣容器缺子 schema | `Tko1..3, Tkg1..3 [178..183]` | 6 | 双档 100% 一致,`405,204` 项被 `(b22∈{0,1,2}, b25∈{0,1})` 无遗漏划分为 6 桶且双链闭合,但冻结 `club.xml` 无 `list_item_fields` 定义 27B 内部字段 |
| 保留 t63 `held` | `CssT..CssE [109..112]` | 4 | 对应 `base+0x00` 多态 tag `35 (0x23)`,全档确认 **0 / 84,259** 行出现,原样保留 t63 `held` |

### `base+0x00` 其余非 `club.xml` 虚分派项与未暴露内部槽

- **非 `club.xml` 多态 tag**:tag `4` (`COMPETITION_BONUS_INFO`, 697 项/179 行,`CCBc` 不在 `club.xml`);tag `9` (`STARTING_PLAYER_RECORD_INFO`, **55,967** 项/55,967 行,`vt[+28]=0xbb0`,仅供 nation `NA*/NG*` `0x3ebcf40`);tag `16` (`CLUB_CUP_POINTS`, 112 项/112 行,`vt[+28]=0xbb0`);tag `37` (`EPPP_APPEARANCE_MONEY_INFO`, 6 项/4 行,`vt[+38]=0x25≠6` 不被 `Camc` 捕获)。
- **非常量未暴露内部槽**:`extra+0x123` (`i8`, `0..20`, 1,970 行非零)、`extra+0xda` (`5B` 位域解码 `0x4348ef0`)、`base+0xac` (`u16` 公共尾,`0..127`, 2,819 行非零,双档一致) 经全扫 `CLUB_GET/CLUB_SET/CLUB_EXTRA_SET/TC_GET2/TC_SET2/TC_EXTRA_SET` 均为 **0 命中**。`+0x18/+0x20/+0x30/+0x38/+0x70/+0x50/+0x40` 全档全零。

---

## 5. L2 锚点交叉验证与复跑命令

| 俱乐部 | ordinal / UID | `Cyfn` | `Ctlv/Cyfb/Cytv` | `Cown` | `Catd / Cmxa` | `TCht` | `Cuf1..Cf10` (2013/14–2022/23) |
|---|---|---:|---|---:|---|---|---|
| Liverpool | `460` / `676` | 1892 | `20 / 20 / 17` | 1 | `52,998 / 85,000` | `Liverpool` | `[0, 10, 22, 0, 30, 29, 18, 24, 33, 19]` |
| Manchester City | `463` / `679` | 1894 | `20 / 20 / 19` | 1 | `53,249 / 85,000` | `mcfc` | `[19, 15, 26, 18, 22, 25, 25, 35, 27, 33]` |
| Manchester United | `464` / `680` | 1878 | `17 / 17 / 17` | 2 | `73,150 / 120,000` | `MUFTC` | `[23, 0, 13, 26, 20, 19, 22, 26, 18, 19]` |
| Chelsea | `415` / `630` | 1905 | `20 / 20 / 19` | 5 | `37,812 / 60,000` | `Chelsea` | `[25, 21, 18, 0, 18, 30, 17, 33, 25, 21]` |
| Real Madrid | `1297` / `1736` | 1902 | `18 / 18 / 18` | **3** | `68,000 / 76,000` | `""` | `[35, 29, 33, 33, 32, 19, 17, 26, 30, 29]` |
| Bayern Munich | `623` / `915` | 1900 | `19 / 19 / 16` | 1 | `75,024 / 88,000` | `""` | `[27, 28, 29, 22, 29, 20, 36, 27, 26, 27]` |
| Barcelona | `1282` / `1708` | 1899 | `19 / 19 / 20` | **3** | `55,000 / 79,000` | `""` | `[24, 34, 26, 23, 25, 30, 24, 20, 15, 9]` |
| Paris Saint-Germain | `586` / `868` | 1970 | `20 / 20 / 17` | 1 | `47,418 / 47,926` | `""` | `[25, 21, 24, 20, 19, 19, 31, 24, 19, 19]` |

```powershell
$env:FM24_DB_DIR = "D:/tmp2b/fm24-db/scratch/data"
py -V:3.12 -I -B scripts/t82_extra3_remaining.py --selftest --build
py -V:3.12 -I -B scratch/t82/out/verify.py --selftest
py -V:3.12 -I -B scratch/t82/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
