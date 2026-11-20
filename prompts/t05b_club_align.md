# t05b — schema↔reader 宽度序列对齐器 + club 字段级映射

## 角色与硬约束

你是逆向工程师 + 算法工程师。工作区 `D:\tmp2b\fm24-db`,Python 固定 `py -V:3.12 -I -B`。

**只读边界**:游戏数据 `Z:\...\2430_fm\client_db.dat` 只读;上游 `D:\tmp2b\fm24\` 全目录只读(可读其 reports/scripts);**唯一可写目录 = 本任务 OUTDIR**。不要修改 `scratch/t01`、`scratch/t02` 既有文件。

**纪律**:closure/偏移断言必须可机械复现;允许诚实负结果;第一步先落盘骨架。

## 核心思路(这是本任务与之前失败的 field_mapper 的关键区别)

之前 `scratch/t02/field_mapper/out/field_mapper.py` 试图**追踪游标穿过 CFG**,在分支/循环处断裂,只到 39.7%。**换一个算法**:

> **不要把行内偏移当"运行时游标",把它当"有序序列对齐问题"。**

已知:
- (a) **schema 字段是有序的**,每个字段有类型(integer/enum/boolean/date/colour/database_record_unique_id/cash/real/string/list…),类型给出**候选线宽集合**(见下表);
- (b) **reader 的传输序列也是有序的**:每个字段一次 `mov r8d,N` + `call [rax+0x28]` 配对,N 就是该字段线宽(或项宽);
- (c) 行内偏移 = 前面所有字段线宽的累加;
- (d) 数据侧可以验证:引用型字段的值必须落在目标表行数范围内、enum 值必须小于枚举基数、date 必须落在合理年份、colour 必须是合法 RGB。

于是问题变成:**在类型约束下,把 schema 字段序列与 reader 线宽序列做保序对齐**,使得 (i) 总宽 == 行宽,(ii) 已知锚点吻合,(iii) 数据合法性最大化。这是带约束的 DP / 回溯,不是控制流追踪。

## 输入

| 用途 | 路径 |
|---|---|
| **schema 字段表(权威)** | `D:\tmp2b\fm24\reports\EDITOR_SCHEMA_FIELDS.md` — 用正则取 `### club（记录标识 \`club\`，433 个字段）` 段落;子字段以 `| 　　\`` 缩进标记,`↳` 行是列表项标题 |
| 机器可读 schema(可选) | `D:\tmp2b\fm24\reports\editor_schema\master.json`、`D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json` |
| club 行框架(已全封口) | `D:\tmp2b\fm24-db\scratch\t02\inbox\club_v2\output.json` + `solve.py`(`load_raw()` 解压;84,259 行、footer 精确) |
| club 半自动底稿(74 事件) | `D:\tmp2b\fm24-db\scratch\t02\field_mapper\club_substrate.json` |
| club 已闭合字段 | `D:\tmp2b\fm24-db\scratch\t02\inbox\club_fields\output.json`(Cccn@row+8,字节链 8/8 已验证) + 其 `REPORT.md` |
| 上游 club 结论(6 个 L2 候选) | `D:\tmp2b\fm24\reports\dbdat_decode\DB_TABLES_BIG.md` 的 `table_3` 段 |
| exe | `D:\tmp2b\fm24\input\editor.exe`(club reader entry `0xe5a7a0`,census 在 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01h\output.json`) |
| capstone | 已装(`capstone` 可 import) |

**注意 mixed 模式**:club 有两套 RTTI/reader(`CLUB` 与 `LEAGUE_BODY_CLUB`)。`Cccn@+8` 与 substrate 前几个事件 `[0,4,8,12,16]` 可能来自不同 reader,务必分别建模、不要混用。

## 类型 → 候选线宽(起点,允许你修正并说明依据)

| 类型 | 候选线宽 |
|---|---|
| boolean | 1(常打包成位域,可能多位共享 1 字节 → 视作 0 宽) |
| enum / multiple_enum / day_of_week | 1 或 2 |
| integer | 1 / 2 / 4 |
| date | 2 或 4(常见 2 字节年+日) |
| colour | 3 或 4 |
| database_record_unique_id | 4(常有 0xFFFFFFFF 空值) |
| cash / real / short_distance | 4(real=float32;short_distance 可能 1 或 2) |
| unique_id | 8 或 4+4(重复 u32) |
| string / picture | **行内不内联**:存 u32 引用 → 4;或 0(名称在 lang 表) |
| list / database_record_list | 行内不存元素,存 **计数 + 段偏移**;元素落到段里 |

## 任务分两阶段

### 阶段 A:对齐器 + 夹具自证(必须做,这是本任务的地基)

写 `align.py`,输入 = (实体 schema 字段序列, reader 线宽序列, 行宽, 已知锚点, 数据样本),输出 = 字段→偏移的候选解(可多个,按数据合法性打分)。

**用这些夹具证明对齐器正确**(它们的行宽和部分偏移已知):

| 夹具 | 行宽 | 已知锚点 |
|---|---|---|
| award | 77 B 定长 | `rdui:u32@64`(=row index)、`duni@68`(两半相等)、38 字段(含 1 list) |
| city | 43 B 定长 | `Clat f32@1`、`Clon f32@5`、`Cnti u8@10`、`rdui@30`、`duni@34`、15 字段 |
| stadium | client 38 B 定长 | `Scti u32@3`、`Slat f32@17`、`Slon f32@21`、`rdui@25`、`duni@29`、60 字段(42 顶层) |
| injury | 16 B 定长 | `rdui@3`、`duni@7`、27 字段 |
| language | 变长(名+30B 后缀) | 后缀 `u32@+17` = 0-based 行号、12 字段 |

**验收**:对 award/city/stadium/injury 四个定长夹具,对齐器必须**自动复原全部已知锚点**,且解出的总宽等于行宽。若做不到,如实写负结果并说明约束缺什么。

### 阶段 B:应用到 club(主目标)

用阶段 A 的对齐器 + club 的 reader 线宽序列,求 club 的字段→偏移解。

- 目标:**≥30 个 schema 字段**得到 `confidence: high|medium` 的命名偏移(已有 Cccn@8 算 1 个)。
- 每个命名必须带 **L3 字节证据**:`(reader file offset, 原字节 hex)` 或 `(4CC getter cmp 指令 offset, 原字节 hex)`,形如:
  `{"field":"Cccn","offset":8,"width":4,"evidence":{"reader_file_offset":"0xe5a864","bytes":"49 8d be f0 00 00 00"},"confidence":"high"}`
- 列表字段单独给**段布局**:`{"field":"Crty","kind":"list","count_offset":..,"item_width":..,"item_fields":[...]}`。
- 数据侧必须交叉验证:引用字段的值分布必须落在目标表行数范围内(例如引用 city 的字段,值应 < 56,293);enum 字段值应小于枚举基数。**没通过数据验证的,confidence 降到 low 或不列**。

## 交付

1. `align.py` — 支持 `--selftest`(跑 5 个夹具)、`--entity club`(跑 club)、`--json`。
2. `fixtures_result.json` — 每个夹具:字段数、复原的锚点数/总数、总宽、PASS/FAIL。
3. `club_fields.json` — `{"status":"complete_partial","entity":"club","type_id":3,"total_schema_fields":433,"top_level_scalars":109,"named":[ {field,offset,width,evidence,confidence} ...],"collections":[...],"unresolved":[...]}`
4. `REPORT.md` — 对齐器原理、夹具结果、club 命名清单、未解项与卡点、对 `field_mapper` 旧结论的勘误。

## 验收标准

- `align.py --selftest` 全 PASS(4 个定长夹具全部锚点复原)。
- club 命名字段数 **≥30**,其中 `confidence: high` **≥15**。
- 每个 high 置信项的字节证据我(指挥官)会独立抽查,必须能逐字节对上。
- 诚实标注未解项,不得为了凑数把 low 置信写成 medium。

## 完成后

打印:夹具 PASS 数 / club 命名字段数(high, medium) / 列表段数 / 关键发现一句话。
