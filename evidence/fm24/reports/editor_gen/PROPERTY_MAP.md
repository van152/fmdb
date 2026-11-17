# FM24 编辑器 property 码 → schema 字段映射（property_map）

状态：**已完成**。数据源为用户编辑器数据 XML 树、DBC wire 解码与 basic comps 资源，方法为纯静态证据对齐，不猜测。

## 1. 方法

1. `db_changes` 记录的 `property` 是 32-bit unsigned 值。把它按**大端**解释为 4 个 ASCII 字符，得到被改字段的 4 字符代码：`1400071283 = 0x53736473 = "Ssds"`。用户 XML 与 DBC wire（同一条记录：DBC 字段 `ytrp`/`prty` 值一致）交叉验证成立。
2. 解码出的 4cc 在 `reports/editor_schema/master.json`（3009 个 field_codes）中查找；实体归属用所在记录的数值 `database_table_type` 判定：锚点为 schema 枚举 `dbts`（`resources_modding/comp editor/comp editor/format/format.xml` 的 Database Table 列，21=Stadium、25=Competition、9=Nation 等），并用"schema 位置唯一的字段码"对每个表号投票复核。
3. 共现验证：`lsop=1` 的记录其 `new_value/id` 标记必须是该 list 字段 `list_item_fields` 之一（本次数据 137/137 全部吻合，0 违例）；`new_value` 子树中出现的 4 字符码与映射字段的 item 字段集合对齐。
4. 不猜测：解码失败或 schema 中不存在的码如实列入未解清单。

## 2. 覆盖率

- 观察到的不同 property 码：**108**（共 120355 条 db_changes 记录）
- 解析为 schema 字段：**105**
- 编辑器记录级操作码（非字段）：3（`ADDR`=新增记录、`COPY`=复制记录、`DELE`=删除记录；证据见 `property_operations`）
- 未解：**0**
- basic comps 资源（55 个 XML）中的 property 属性：0（basic comps 是 rule-group XML，不含 db_changes 信封，因此不贡献 property 码）

数据源：`reports/editor_data/*.tree.json`（8 文件）、`reports/editor_fmf/dbc_decoded/*.json`（12 个 payload，其中 6 个版本无对应 XML）、`resources_modding/comp editor/comp editor/basic comps/`。

## 3. database_table_type 数值 → 实体

| 表号 | 实体 | 投票（唯一归属字段码） | dbts 枚举名 | 一致 | 备注 |
|---:|---|---|---|---|---|
| 0 | award | 772/772 | Award | 是 |  |
| 1 | person | 89760/89760 | Person | 是 |  |
| 3 | club | 3849/3861 | Club | 是 |  |
| 9 | nation | 146/146 | Nation | 是 |  |
| 10 | nation | 495/495 | — | — |  |
| 21 | stadium | 1164/1164 | Stadium | 是 |  |
| 25 | comp | 1683/1683 | Competition | 是 |  |
| 56 | agreement | 10/10 | Agreement | 是 |  |
| 2 | city | 0/0 | City | 是 | from dbts enum only; not observed in analyzed data |
| 5 | continent | 0/0 | Continent | 是 | from dbts enum only; not observed in analyzed data |
| 6 | injury | 0/0 | Injury | 是 | from dbts enum only; not observed in analyzed data |
| 7 | media source | 0/0 | Media Source | 是 | from dbts enum only; not observed in analyzed data |
| 8 | language | 0/0 | Language | 是 | from dbts enum only; not observed in analyzed data |
| 18 | derby name | 0/0 | Derby Name | 是 | from dbts enum only; not observed in analyzed data |
| 19 | region | 0/0 | Region | 是 | from dbts enum only; not observed in analyzed data |
| 23 | stage name | 0/0 | Stage Name | 是 | from dbts enum only; not observed in analyzed data |
| 24 | team | 0/0 | Team | 是 | from dbts enum only; not observed in analyzed data |
| 27 | weather | 0/0 | Weather | 是 | from dbts enum only; not observed in analyzed data |
| 35 | description | 0/0 | Description | 是 | from dbts enum only; not observed in analyzed data |
| 41 | currency | 0/0 | Currency | 是 | from dbts enum only; not observed in analyzed data |
| 47 | local region | 0/0 | Local Region | 是 | from dbts enum only; not observed in analyzed data |

说明：表号 10 未出现在 dbts 枚举中，但 `Nntp`/`Necf`/`Nrgi`/`Ne*` 等 **nation.xml 独有**字段全部落在表 10（且与表 9 的变更使用相同 `db_unique_id`），故表 10 与表 9 均指向 nation 实体；两者的细分语义（编辑器不同面板/子表）未解，如实记录。表号 55 仅由 `ADDR` 操作使用（`new_value.database_table_type=25` 说明被添加记录本身是 competition），无 schema 锚点。

## 4. 字段映射清单（按实体）

### agreement

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Anti` | 1097757801 | database_record_list | Nations | — | — | — | 10 | 56 |

### award

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `AWci` | 1096246121 | database_record_unique_id | Continent | — | — | — | 380 | 0 |
| `AWmi` | 1096248681 | database_record_unique_id | Competition | — | — | — | 392 | 0 |

### city

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Cnam` | 1131307373 | string | Name | — | — | — | 390 | 3 |
| `Cnti` | 1131312233 | database_record_unique_id | Nation | — | — | — | 384 | 3 |

### club

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `CIns` | 1128885875 | boolean | Is Institute | — | — | — | 12 | 3 |
| `CSrs` | 1129542259 | list | Reserve Teams To Create | — | — | — | 384 | 3 |
| `Cafl` | 1130456684 | list | Current Affiliations | — | — | — | 3 | 3 |
| `Cbni` | 1130524265 | database_record_unique_id | Based Nation | — | — | — | 384 | 3 |
| `Ccty` | 1130591353 | database_record_unique_id,string | City | — | — | — | 3 | 3 |
| `Cdvi` | 1130657385 | database_record_unique_id | Division | — | — | — | 656 | 3 |
| `Cext` | 1130723444 | boolean | Extinct | — | — | — | 384 | 3 |
| `Cl3n` | 1131164526 | string | Three Letter Name | — | — | — | 387 | 3 |
| `Cldi` | 1131177065 | database_record_unique_id | Last Division | — | — | — | 26 | 3 |
| `Clps` | 1131180147 | integer | Last Position | — | — | — | 12 | 3 |
| `Cmag` | 1131241831 | integer | Maximum Age | — | — | — | 12 | 3 |
| `Cnam` | 1131307373 | string | Name | — | — | — | 390 | 3 |
| `Cndi` | 1131308137 | database_record_unique_id | Next Division | — | — | — | 656 | 3 |
| `Cnti` | 1131312233 | database_record_unique_id | Nation | — | — | — | 384 | 3 |
| `Cprs` | 1131442803 | enum | Status | — | — | — | 384 | 3 |
| `Crdl` | 1131570284 | list | Regional Divisions | — | — | — | 3 | 3 |
| `Crep` | 1131570544 | integer | Reputation | — | — | — | 384 | 3 |
| `Csnm` | 1131638381 | string | Short Name | — | — | — | 394 | 3 |
| `Csti` | 1131639913 | database_record_unique_id | Stadium | — | — | — | 33 | 3 |
| `Csxn` | 1131640942 | string | Six Letter Name | — | — | — | 391 | 3 |
| `Tsti` | 1416852585 | database_record_unique_id | Stadium | — | — | — | 256 | 3 |
| `levl` | 1818588780 | integer | Division Level | — | — | — | 168 | 25 |

### club b team

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `C2dv` | 1127375990 | database_record_unique_id | Division | — | — | — | 12 | 3 |

### comp

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `CTty` | 1129608313 | enum | Trophy Type | — | — | — | 1 | 25 |
| `Cdvi` | 1130657385 | database_record_unique_id | Division | — | — | — | 656 | 3 |
| `HKEt` | 1212892532 | boolean | Uses Goal-line Technology | — | — | — | 5 | 25 |
| `Pfq0` | 1348890928 | enum | Frequency | — | — | — | 1 | 25 |
| `Pfq1` | 1348890929 | enum | Frequency | — | — | — | 1 | 25 |
| `Pob0` | 1349476912 | boolean | Obligatory | — | — | — | 1 | 25 |
| `Pob1` | 1349476913 | boolean | Obligatory | — | — | — | 1 | 25 |
| `VARt` | 1447121524 | enum | Video Assistant Referee | — | — | — | 7 | 25 |
| `c3ln` | 1664314478 | string | Three Letter Name | — | — | — | 196 | 25 |
| `cbcl` | 1667392364 | colour | Background Colour | — | — | — | 1 | 25 |
| `ccti` | 1667462249 | database_record_unique_id | Continent | — | — | — | 346 | 25 |
| `cext` | 1667594356 | boolean | Is Extinct | — | — | — | 204 | 25 |
| `cfcl` | 1667654508 | colour | Foreground Colour | — | — | — | 1 | 25 |
| `chst` | 1667789684 | list | History | — | — | — | 4 | 25 |
| `cnam` | 1668178285 | string | Name | — | — | — | 196 | 25 |
| `cnti` | 1668183145 | database_record_unique_id | Nation | — | — | — | 180 | 25 |
| `cpcm` | 1668309869 | database_record_unique_id | Parent Competition | — | — | — | 48 | 25 |
| `crep` | 1668441456 | integer | Reputation | — | — | — | 181 | 25 |
| `crgt` | 1668441972 | list | Registered Teams | — | — | — | 6 | 25 |
| `csnm` | 1668509293 | string | Short Name | — | — | — | 196 | 25 |
| `ctcl` | 1668572012 | colour | Trim Colour | — | — | — | 1 | 25 |
| `ctms` | 1668574579 | database_record_list | Teams | — | — | — | 65 | 25 |
| `cuae` | 1668637029 | boolean | Uses Extra Officials | — | — | — | 4 | 25 |
| `dbty` | 1684173945 | enum | Type | — | — | — | 218 | 25 |
| `levl` | 1818588780 | integer | Division Level | — | — | — | 168 | 25 |

### continent

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Ccty` | 1130591353 | database_record_unique_id,string | City | — | — | — | 3 | 3 |
| `Cnam` | 1131307373 | string | Name | — | — | — | 390 | 3 |

### currency

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Cnam` | 1131307373 | string | Name | — | — | — | 390 | 3 |

### nation

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `NTRv` | 1314148982 | list | Transfer Values | false | false | — | 14 | 9 |
| `NYRt` | 1314476660 | integer | Youth Rating | — | — | — | 4 | 10,9 |
| `Nagr` | 1315006322 | list | Agreements | — | — | — | 6 | 9 |
| `Ncti` | 1315140713 | database_record_unique_id | Continent | — | — | — | 4 | 9 |
| `Ne10` | 1315254576 | real |  | — | — | — | 18 | 10,9 |
| `Ne11` | 1315254577 | real |  | — | — | — | 18 | 10,9 |
| `Necf` | 1315267430 | integer | Economic Factor | — | — | — | 10 | 10 |
| `Nefr` | 1315268210 | list | Nations Treated as EU | — | — | — | 4 | 9 |
| `Neu1` | 1315271985 | real |  | — | — | — | 6 | 10,9 |
| `Neu2` | 1315271986 | real |  | — | — | — | 6 | 10,9 |
| `Neu3` | 1315271987 | real |  | — | — | — | 8 | 10,9 |
| `Neu4` | 1315271988 | real |  | — | — | — | 6 | 10,9 |
| `Neu5` | 1315271989 | real |  | — | — | — | 6 | 10,9 |
| `Neu6` | 1315271990 | real |  | — | — | — | 14 | 10,9 |
| `Neu7` | 1315271991 | real |  | — | — | — | 14 | 10,9 |
| `Neu8` | 1315271992 | real |  | — | — | — | 8 | 10,9 |
| `Neu9` | 1315271993 | real |  | — | — | — | 6 | 10,9 |
| `Nfap` | 1315332464 | integer | FA Financial Power | — | — | — | 12 | 10,9 |
| `Nfpa` | 1315336289 | integer | FA Patience | — | — | — | 2 | 9 |
| `Ngct` | 1315398516 | enum | Gain Nationality Type | — | — | — | 2 | 10 |
| `Nmya` | 1315797345 | integer | Max. Youth Age | — | — | — | 2 | 10 |
| `Nndn` | 1315857518 | boolean | Does Not Allow Dual Nationality | — | — | — | 2 | 10 |
| `Nnfr` | 1315858034 | list | Nations Treated as Non-Foreign | — | — | — | 6 | 9 |
| `Nnsi` | 1315861353 | database_record_unique_id | National Stadium | — | — | — | 1 | 10 |
| `Nntp` | 1315861616 | list | Nation Transfer Preferences | — | — | — | 288 | 10 |
| `Nrgi` | 1316120425 | database_record_unique_id | Region | — | — | — | 10 | 10,9 |
| `Ntxr` | 1316255858 | list | Tax Rules | — | — | — | 158 | 10,9 |
| `Numa` | 1316318561 | boolean | Allow Multiple Assistant Managers | — | — | — | 4 | 9 |
| `Nygn` | 1316579182 | integer | Years To Gain Nationality | — | — | — | 2 | 10 |
| `crep` | 1668441456 | integer | Reputation | — | — | — | 181 | 25 |

### person

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `PCJO` | 1346587215 | enum | Job | — | — | — | 6528 | 1 |
| `PSJO` | 1347635791 | enum | Secondary Job | — | — | — | 6528 | 1 |
| `PcHC` | 1348683843 | boolean | Has Contract | — | — | — | 6528 | 1 |
| `Pces` | 1348691315 | enum | Contract Type | — | — | — | 6528 | 1 |
| `Pcex` | 1348691320 | date | Contract Expires | — | — | — | 4896 | 1 |
| `Pcjd` | 1348692580 | date | Date Joined | — | — | — | 6528 | 1 |
| `Pcna` | 1348693601 | string | Common Name | — | — | — | 6528 | 1 |
| `Pcsd` | 1348694884 | date | Date Last Contract Signed | — | — | — | 6528 | 1 |
| `Pcti` | 1348695145 | database_record_unique_id | Club | — | — | — | 6528 | 1 |
| `Pdob` | 1348759394 | date | Date Of Birth | — | — | — | 6528 | 1 |
| `Pfna` | 1348890209 | string | First Name | — | — | — | 6528 | 1 |
| `Pife` | 1349084773 | boolean,enum | Gender | — | — | — | 6528 | 1 |
| `Pirc` | 1349087843 | boolean | On Rolling Contract | — | — | — | 6528 | 1 |
| `Pnti` | 1349416041 | database_record_unique_id | Nation | — | — | — | 6528 | 1 |
| `Psna` | 1349742177 | string | Second Name | — | — | — | 6528 | 1 |
| `Ptyp` | 1349810544 | enum | Person Type | — | — | — | 6528 | 1 |
| `levl` | 1818588780 | integer | Division Level | — | — | — | 168 | 25 |

### person name

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Pife` | 1349084773 | boolean,enum | Gender | — | — | — | 6528 | 1 |
| `Pnti` | 1349416041 | database_record_unique_id | Nation | — | — | — | 6528 | 1 |

### stadium

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Scpy` | 1399025785 | integer | Capacity | — | — | — | 1 | 21 |
| `Secy` | 1399153529 | integer | Expansion Capacity | — | — | — | 1 | 21 |
| `Snam` | 1399742829 | string | Name | — | — | — | 1 | 21 |
| `Spln` | 1399876718 | short_distance | Pitch Length | — | — | — | 1 | 21 |
| `Spwd` | 1399879524 | short_distance | Pitch Width | — | — | — | 1 | 21 |
| `Ssds` | 1400071283 | list | Stadium Sides | false | false | true | 1154 | 21 |
| `Sste` | 1400075365 | enum | State | — | — | — | 1 | 21 |
| `Su19` | 1400189241 | enum | Used By National U19 Team | — | — | — | 1 | 21 |
| `Su21` | 1400189489 | enum | Used By National U21 Team | — | — | — | 1 | 21 |
| `Sunt` | 1400204916 | enum | Used By National Team | — | — | — | 1 | 21 |
| `Sush` | 1400206184 | boolean | Has Undersoil Heating | — | — | — | 1 | 21 |

### team

| 4cc | property 值 | 类型 | 名称 | allow_add | allow_remove | debug_only | 记录数 | 表号 |
|---|---:|---|---|---|---|---|---:|---|
| `Cnti` | 1131312233 | database_record_unique_id | Nation | — | — | — | 384 | 3 |
| `Tsti` | 1416852585 | database_record_unique_id | Stadium | — | — | — | 256 | 3 |

多实体字段（归属由表号判定）：`Ccty`, `Cdvi`, `Cnam`, `Cnti`, `Pife`, `Pnti`, `Tsti`, `crep`, `levl`。

受限字段（校验器 v3 的 ERROR/WARNING 面）：

- `allow_add=false` 的实体 list 字段：`NTRv`, `Ssds`。
- `debug_only=true` 的实体 list 字段：`Ssds`。

## 5. 编辑器操作码（非字段）

- `ADDR`（add-record）：7069 条记录，外层表号 ['55']。信封形状：`new_value` 携带目标记录的 `database_table_type`/`dcty`/`db_unique_id`，无 `lsop`。
- `COPY`（copy-record）：294 条记录，外层表号 ['0']。信封形状：`new_value` 携带目标记录的 `database_table_type`/`dcty`/`db_unique_id`，无 `lsop`。
- `DELE`（delete-record）：7 条记录，外层表号 ['0']。信封形状：`new_value` 携带目标记录的 `database_table_type`/`dcty`/`db_unique_id`，无 `lsop`。

## 6. 未解清单

无。观察到的全部 property 码均已解析（105 字段 + 3 操作码）。

## 7. lsop 语义（观察结论，供校验器使用）

- `lsop=0`：整条 list item 内容设置。编辑器实际写出两种形状：A) `value` 直接含 item 字段（0.3.2/0.26.1 时代，如 Ssds `value{indx,exis,capc,...}`）；B) `value{new_value{item}, odvl{old_item}}`（球场修复时代）。两者均为**修改既有条目**，在 8 个用户文件共 769 条 lsop=0 记录中无一携带"新条目无旧值"特征。
- `lsop=1`：**list item 单字段更新**。`new_value/id` = 被改的 item 字段 4cc（NTRv→`valu`、crgt→`Ttea`、chst→`pla1`、Nntp→`sckn`/`rati`、Ntxr→`perc`、Nnfr→`endt`），`value` = 新字段值（标量/记录引用/null），`olvl` = 旧 item 快照。137/137 条全部满足 id∈list_item_fields 且 olvl 存在。
- `lsop=3`：无 payload 的 list 级操作（ctms/Cafl/Crdl/Nagr/Nefr），疑为移除/清空类，语义未定，校验器仅弱处理。
- **没有**任何用户记录呈现 `lsop=1 + id=nwvl + value{new_value{整条 item}} + 无 olvl` 的形状（QA fixture `ssds_corner_add.xml` 第二条记录的形状）——该形状在观察数据中不存在，被校验器归类为"插入新条目"，落在 `allow_add=false` 列表（Ssds）上即 ERROR。

证据路径：`reports/editor_gen/property_map.json`（全量机读）、`reports/editor_data/*.tree.json`、`reports/editor_fmf/dbc_decoded/*.json`、`reports/editor_schema/master.json#enums.dbts`、`resources_modding/comp editor/comp editor/format/format.xml`。

## 8. editor.exe 静态证据（只读扫描）

- 信封字段码以**反序 4 字节**存于 .rdata 静态表（与 DBC wire 的反序约定一致）：`dtty (database_table_type)`×173；`duni (db_unique_id)`×141；`prty (property)`×80；`nwvl (new_value)`×72；`lsop (list operation)`×185。
- 108 个 property 值按小端 dword 扫描：**94 个命中**（未命中 14 个：`Pirc`、`Neu6`、`Neu7`、`Neu1`、`Neu2`、`Neu3`、`Neu4`、`Neu5`、`Neu8`、`Neu9`、`Pfq0`、`Pfq1`、`Pob0`、`Pob1`；未命中多为 `ADDR/COPY/DELE` 操作码或低频码，不影响结论）。
- 这证明 property 值 = 字段 4cc 的小端 dword 是编辑器自身的编码约定，不是 XML 解码的巧合。
