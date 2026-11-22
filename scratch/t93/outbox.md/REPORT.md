# t93 REPORT — 外部语料挖矿结果

只读外源,零执行。所有条目 `provenance=ext/<repo>@<hash>`;本任务**未产生任何新证据等级**。

## 0. 交付与规模

| 文件 | 规模 | 内容 |
|---|---|---|
| `save_grammar.json` | 30 条文法 (G01–G30), 65 条 file:line 锚点, 9 个源文件 | 容器/分节/表/记录/zstd/门控 |
| `field_dictionary.json` | 58 实体 / 720 字段 / 34 readers | fmsave 字段名+类型+语义 |
| `fm24_memory_layout.json` | 270 字段 (233 已定位) + 15 子记录 + 30 条 curated fact, 5 个源文件 | FM24 **内存**布局 |
| `fm24_fields.json` | 270 字段(同上,无 curated fact) | `t93_fm24.py` 中间产物,非交付物 |
| `fm27_recon_digest.json` | 22 篇 recon / 102 条行锚要点 | FM27 recon 摘要 |
| `crosswalk.json` | 20 条对照,**全 held**,0 次分级变动 | 我方 vs 外部 |
| `verify.py` | 9 项独立校验 | 全绿(见 §5) |

## 1. save_grammar.json(G01–G30)

按层组织,每条带 `file:line` 与原文片段:

- **容器层** G01–G06:6 字节魔数 `02 01 66 6d 66 2e`、26 字节头、header+9 的 trailer 指针、
  trailer frame + 9 字节头、frame base 26、分节种类(`.dat`/`.cmt`;`.apm`/`.scm` 为 match 文件)。
- **目录层** G07–G10:目录头 = u32 名长 + u32 skip;条目 = u32 名长(1–256)+ ASCII 名 +
  u32 ext 长(==4)+ `.xxx` + `<5Q`(相对偏移/压缩长/解压长/两个尾部 u64)+ 40 字节尾;
  条目表结束标记;region 与空洞。
- **zstd 层** G11–G13:frame 魔数 `0xFD2FB528`、skippable `0x184D2A50..5F`、3 字节 block 头
  (bit0 last / bit1-2 type / size>>3)、block ≤128 KiB;解压契约(cap+1、eof、无 unused_data、
  长度必须相等);膨胀上限 64× 单节 / 32× 整档 / 64 MiB 地板。
- **分节层** G14–G17:`03 01` + **反转扩展名**(`dat`→`tad`)+ 偏移 6 的 u16 schema;
  FM26 schema 映射(game_db 4000, save_game_summary 29, game_info 46, humans 21, feeder_man 5,
  injury_manager 8, job_centre 1, tactics_man 26, training_man 31, match_stats_cfg 6);
  布局门控阶梯(own build+schema → schema-on-fit-build → own build → FALLBACK_BUILD
  `26.3.2+2329565`);FM27 只借 FM27 的档位 + `UnsupportedGameError`。
- **表层** G18–G22:计数表用 `RecordStep` 走(nation 表 row_count=251、14 步);表头 `<IB`;
  记录尾 `<III`;club 表 frame 与字段。
- **记录层** G23–G30:player 记录(marker `01 00 6c 07` @+102、CA+0 PA+2 team+16 ratings+24
  attributes+39);contract 链(tag `01 00 6c 07`、selector u32 @+5 == pindex+1、wage +17、
  team +9、尾走 `E = M - 66 - 29*count`);tagged stream(4 字节 tag 字节反转、分隔 0x01、
  u8 0x11 / u16 0x12 / u32 {01,02,03,0B,0F} / string 0x1A / list 0x0A / nil 0x00);
  字符串 = u32 长 + UTF-8;日期 = u16 (doy & 0x1FF | slot<<9) + u16 年 1901–2200;
  person block;staff 记录(含 26 个 preference 槽、14 个有名);reader 门控。

## 2. field_dictionary.json

58 实体 720 字段,状态分布 **verified 373 / unconfirmed 303 / unstated 44**。

优先实体(字段数 / verified / unconfirmed):

| 实体 | 字段 | verified | unconfirmed |
|---|---|---|---|
| PlayerSeasonStats | 69 | 50 | 17 |
| Player | 53 | 19 | 27 |
| Attributes | 52 | 52 | 0 |
| TeamMatchStats | 35 | 33 | 2 |
| Staff | 31 | 5 | 21 |
| Fixture | 28 | 22 | 5 |
| Contract | 25 | 8 | 16 |
| Club | 13 | 2 | 11 |
| Stadium | 20 | 10 | 9 |
| Nation | 2 | 0 | 2 |
| Competition | 4 | 2 | 2 |
| Team | 4 | 0 | 4 |

要点:**fmsave 的 `verified` 是它自己的登记表,不是我方 L1–L4**。它的 `verified` 只覆盖
`register_field_statuses()` 里点名的字段;`PlayerSeasonStats` 的登记表点了 83 个名字而 dataclass
只有 69 个字段,差值(计算列/派生列,如 `save_percent`、`goals_per_90`)单列在
`status_names_not_a_field`,不参与计数。

`readers` 段把 34 个 reader 模块映射到所在 region(`game_db` 等),说明"哪张表由哪个 reader 读",
不含任何解析行为。

## 3. fm24_memory_layout.json

**这是运行中进程的内存布局,不是存档 wire 格式** —— 文件内 `domain_note` 与
`memory_layout_is_not_wire: true` 明写,`verify.py` 第 5 项会核对这句话存在。

- 实体数组(RVA 相对 fm.exe,image base 0x140000000):
  players 83,426 @`0x642EDD0/0x642EDD8` stride `0x3E8` vtable `fm.exe+0x5A4E958`;
  staff 33,835 @`0x642EDE8/0x642EDF0` stride `0x268`;
  clubs 36,725 @`0x642EF58/0x642EF60` stride `0x170`。
- 定位方法:扫 fm.exe 可写段找 `(data, end)` 指针对,再用见证记录(Guardiola 的 personality
  字节、Kane 的 UID)在堆里反查数组。stadium 数组**根未定位**(`rva_stadium_base=0`),
  只能从 club 经 `home_stadium` 链按 stride `0xB0` 取。
- 字段:Club 51(41 定位)/ Player 130(113)/ Staff 75(68)/ Stadium 14(11);未定位的保留
  `located:false` 与 `offset_expr: null`(`c_reputation`、`p_sharpness`、`st_standing` 等)。
- 30 条 curated fact(M01–M30)把散落在文档里的结论(当前日期 `fm.exe+0x631D5BC`、
  contract 链 wage +0x18 / expiry +0x40 / squad status +0x4C / number +0x55、
  未挂牌哨兵 `0x076C0001`、Epic 独立指纹 `0x8FA113DB9DCD8883`)连到具体行。

## 4. fm27_recon_digest.json

22 篇 `docs/recon/*.md`,每篇 3–8 条要点(共 102 条),每点带行号。标题按**逐字**匹配文件首个
非空行,`line_count` 与文件实际行数核对。覆盖面:bans、club-debts、contracts、gamepass ×3、
loans、names、national-teams、nationality、object-pools、prize-money、sponsorships、staff、
steam ×5(含 macOS)、tactics-and-value、transfer-offers、transfers、youth-intake。

## 5. crosswalk.json —— 20 条,全 held

关系分布:structural_match 8、code_agreement 4、naming_match 3、
external_agreement_only / id_namespace_only / range_only / coverage_gap / no_relation 各 1。

三类最值得记的对照:

1. **X06 日期编码**:`pack('<HH',1,1900)` == `0x076C0001`(fmsave wire)与 fm-editor 文档里的
   未挂牌哨兵字节完全相同 —— 两个外部仓互相印证,但对我方 2 字节 `stdt` 槽毫无分量。
2. **X10 squad status**:两个外部仓 17 个码逐一对上(fmsave IntEnum vs FMLibre 表格),
   是本次最强的一致;同时暴露一处外部冲突:**fmsave 命名 18 = Continental Cup Goalkeeper,
   FMLibre 把 18 列为 169,023 名球员中从未出现**。冲突照记,不裁。
3. **X13 clause kind**:重叠段数字完全一致(0/1/2/15/16/17/18/22/32/37/38/41),但
   `0x22` 在 fmsave 是 SHUTOUT_BONUS、在 FMLibre 是 34 = Clean Sheet Bonus —— 同一概念不同码,
   两张外部表**不可互换**。

反面样本同样保留:X15(zstd 容器 vs 我方平铺表,no_relation)、X19(内存偏移 vs wire 偏移,
命名相同坐标系不同 —— 混用就会把 wire 列摆到堆偏移上)。

## 6. 明确的"没有发生"

- 没有任何一条外部标签进入我方分级:`crosswalk.json` 20/20 `held`,`grade_moves: 0`;
  `our_side.grade` 只允许 `L1|L2|L3|held|n/a` 前缀,`verify.py` 第 8 项逐条检查。
- 没有执行外源代码:`scripts/t93_*.py` 4 个 + `verify.py` 全部通过禁用模式扫描
  (`import fmsave` / `from fmsave` / `pip install` / `subprocess` / `os.system` / `cargo build|run`);
  对 `scratch/ext` 只做 `read_text`。
- 没有触碰基线:`schema_v113.json`、`slots.json`、`stage2_table_identity.json` 三份 sha256
  在 `verify.py` 第 3 项逐字节核对(只读侧证)。

## 7. 剩余(未做,不影响交付)

- fmsave 的 `_save.py`(3090 行)只摘了容器/分节/表/记录文法,`cli.py`/`export.py` 未摘
  (与格式知识无关)。
- fm-editor 的 FM26/27 字段表(`src/fields/fm26*`、`fm27*`)未摘,只取 FM24。
- FMLibre 的 `docs/` 非 recon 部分(如 build profile 说明)未摘。
