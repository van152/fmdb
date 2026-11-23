# FM24 数据库 `.dat` 读取格式报告（v4）

状态：只读静态分析。v2 完成固定步长 `table_21`/`table_25`、DBID 搜索、球场 `Ssds` 槽位解码和历史索引边界验证；v3 新增 `name_table_*` 配对结构与 `lang_update_db` 名称索引；v4 解出 `summary.dat` 的文件身份（editor 数据库摘要）、分段布局与记录流结构（详见 `reports/dbdat_decode/summary_dat.json`），并证伪"表行数汇总/schema 罗塞塔/存档 summary 同族"三个假设。未启动游戏/editor，未写安装目录；分析只读，输出留在工作区。

> **证据等级口径（2026-11-15 QA 整改，定义见 README）**：本报告的"全表验证/逐字节相同/完整验证"等表述均为 **L1**（自家解码器 `modding_read_dbdat.py` 对安装文件/存档副本原始字节的复读与算式校验）；`fm.i64`/`input/editor.exe` 静态地址相关结论为 **L3**（来源与重放登记见 `reports/qa/IDA_PROVENANCE.md`）；坐标/城市名比对属 **L2**（外部真实事实）。本报告**无 L4**（未由游戏或编辑器加载验收）。

## 结论摘要

- `.dat` 有多种封装。`client_db.dat`、`server_db.dat`、`lang_update_db.dat` 在 `tad.` v3569 外壳内嵌资源 FMF；人物库/历史库和 `summary.dat` 格式不同。client/server FMF 目录及 Zstd 表项已解压。
- **`summary.dat` 身份已确认（v4）**：它是 FM24 Editor 的 database summary（`database_summary.cpp`），以 `tad.` v3569 外壳写出，文件名由 `"summary"` + `".dat"` 拼接、tag 为 `NULL`。主体是 `ff ff ff ff`(-1) 分隔的记录流（54,086 条）+ 收尾段；与 client_db 表结构无对应关系（证伪行数汇总/schema 假设）。
- `table_21` 是高置信 stadium 表：client 行 38 字节、server 行 181 字节；两边 48,413 行按相同顺序排列，server 每行末 38 字节与 client 对应行逐字节相同。所有行的 `rdui == row_index`，`duni` 的两个 u32 半部相等且唯一。
- `table_25` 是高置信 competition 表：client payload 满足 `14 + 7047×127 + 8`；每行 offset 118 有重复-u32 `duni`。competition 剩余字段仍未逐字段对齐 schema。
- `table_10` 有 251 行，DBID/duni `472446402670` 在原始 payload offset 4166 命中；但它的变长行边界/字段布局仍未解。
- 已从 `server_db/table_21` 解出大庆球场 DBID `23318212` 的 8 个原始 `Ssds` 槽位。原始值均为 `exis=false, capc=0, iuse=false, seat=false`。
- `pl_hist_index` 与 `pl_hist_id` 现可互相对齐到 515,581 个 player-history 范围；全部相邻范围间距均为 44 字节，decompressed `.dt` 尾部也正好剩 44 字节。non-player 历史索引未完全解析；`summary.dat` 的身份与布局已解（v4），字段级语义未解。
- 已定位 FMF/AFE 头 helper、`tadc` 标签 helper 和 `Ssds` 字段访问 helper；仍未得到 `.dat` 主表加载/通用行反序列化调用链。`ida/editor.i64` 仍打不开（IDA rc=4）；editor 侧地址来自对 `input/editor.exe` 的新建临时静态加载，不是损坏的 i64。

## 外层与资源目录

### `client_db.dat`

- 文件头 `03 01 74 61 64 2e f1 0d`：`03 01 "tad."`，`u16 version=3569`；文件偏移 `0x08` 为 `02 01 "fmf." 08 00 00`。
- FMF `data_base=34`，TOC 绝对偏移 `13,113,241`；TOC 后 9 字节处为 Zstd 目录帧，解压目录 1,954 字节。31 项均通过边界校验。
- 表项各自是直接 Zstd 帧；例如 `table_41.dat` 解压为 `03 01 "tad." f1 0d ad 00 00 00 ...`，即 v3569、count=173。
- client 目录/校验信息：`reports/dbdat_decode/client_db_directory.json`；全部外层头：`reports/dbdat_decode/dat_headers.json`。

### 其它文件族

| 文件 | 字节观察 | 状态 |
|---|---|---|
| `server_db.dat` | `tad.` v3569 + embedded FMF；77 项 | 解压 `table_21` 等表 |
| `lang_update_db.dat` | `tad.` v3569 + embedded FMF；352 项 | 目录已解析 |
| `people_db.dat`、`basic_people_db.dat` | `tad.` v3569，offset 8 直接 Zstd | 内容结构未解 |
| `pl_hist_index.dat`、`non_pl_hist_index.dat` | `tad.` v3569，offset 8 Zstd | player index 可解析；non-player 部分结构未解 |
| `pl_hist_dt.dat`、`non_pl_hist_dt.dat` | `tadc` v3，offset 8 多个串联 Zstd 帧 | 全流可解压，通用 record 语义未解 |
| `pl_hist_id.dat`、`non_pl_hist_id.dat` | `tad.` v1，offset 8 后原始 u32 | player offset-pair 已验证；non-player 关系未解 |
| `summary.dat` | `tad.` v3569；无 embedded FMF/Zstd | **v4 已解身份与布局**：editor 数据库摘要，见下文专节与 `reports/dbdat_decode/summary_dat.json` |

`.dat` 与 `.dbc` 外壳不同；不要将 `reports/editor_fmf/DBC_FORMAT.md` 中的 `cbd.` 解密/解压规则套到 `.dat`。

## 固定步长表与 DBID 对齐

### `table_21`：stadium

记录尺寸由 payload 全长与 count 校验：

```text
client: 14 + 48,413 × 38  + 8 = 1,839,716 bytes
server: 14 + 48,413 × 181 + 8 = 8,762,775 bytes
```

- header 14 字节，footer 8 字节。
- client row：`rdui` u32 位于 row+25；`duni` u64 位于 row+29；坐标候选 float32 位于 row+17/+21。
- server row：`rdui` 位于 row+168；`duni` 位于 row+172。每一行的 `server_row[143:181] == client_row[0:38]`，48,413 行全部相等。server 前 143 字节容纳 server-only 字段。
- 全表验证：48,413/48,413 行的 `rdui` 等于 row index；48,413/48,413 个 `duni` 的 high/low u32 相等且全唯一。
- Daqing stadium：DBID `23318212` → 重复-u32 duni `100150957964512964` (`c4 ce 63 01` 重复两次)，row index/rdui=18795。client duni 字节位于 payload offset 714253；server duni 位于 3,402,081。坐标解为 `Slat≈46.4594841`、`Slon≈125.1864014`，与目标球场定位相符。

### `Ssds` 原始 item 布局与大庆样例

`stadium.xml#stad` 的 `Ssds` schema 子字段为 `indx, exis, capc, cond, sage, iuse, tclo, seat, roof, rofs, tunn, reno`。大庆对应的 server `table_21` row 在 row+64..row+127 有 8 个连续 8-byte 槽位；每槽为：

```text
capc: signed i32 @ +0 | sage: signed i16 @ +4 | cond: signed i8 @ +6 | flags: u8 @ +7
```

槽位顺序提供 `indx=0..7`。对应 `reports/dbdat_decode/stadium_sides_sample.json` 的原始 64 字节为 `00 00 00 00 00 00 00 14` 重复 8 次，因此大庆原始 8 槽 `capc=0, sage=0, cond=0, flags=0x14`；`exis=false`（bit0）、`seat=false`（bit1）、`iuse=false`（bit2 反相读取）。其他旗标位：`tunn=3, roof=4, rofs=5, tclo=6, reno=7`。

这组位/偏移来自 `fm.i64` 函数 `sub_1449A06C0` 的指令证据：

- 字节证据：`0x1449A06F2: 81 fa 63 70 61 63`（比较 `capc`），`0x1449A070A: 81 fa 73 69 78 65`（比较 `exis`），`0x1449A080F: 81 fa 78 64 6e 69`（比较 `indx`），`0x1449A081B: 81 fa 65 73 75 69`（比较 `iuse`），`0x1449A0899: 81 fa 74 61 65 73`（比较 `seat`）。这些指令中的 4CC 内存字节反序。
- `capc` 分支在 `0x1449A092A` 的字节 `8b 38` 读取 `[item+0]` dword；`sage` 在 `0x1449A07B0` 的 `0f bf 78 04` 读取 `[item+4]` signed word；`cond` 在 `0x1449A098B` 的 `0f be 78 06` 读取 `[item+6]` signed byte。
- `exis` 分支在 `0x1449A071A` 的 `0f b6 58 07 80 e3 01` 读取 `[item+7]` 并取 bit0。`iuse` 在 `0x1449A0B27` 的 `f6 c3 04 0f 94 45 f8` 对 bit2 执行 test/setz（反相）；`seat` 读取 flags bit1。
- `indx` 由 `0x1449A0ABC` 分支从 item 索引 byte 读取；对固定 8 槽表按槽序给出 0..7。

  > **术语澄清（2026-11-15 QA 整改：运行时 item accessor ≠ 磁盘序列化槽结构）**：上文"item 索引 byte"指 exe 内**运行时 item accessor**（`sub_1449A06C0`）在遍历槽位时持有的**槽位序号**（循环索引/槽序），不是磁盘槽里另存的字段。磁盘上每个 `Ssds` 槽固定 8 字节，只有 `capc(i32@+0) + sage(i16@+4) + cond(i8@+6) + flags(u8@+7)`，**没有**逐槽的 indx byte；磁盘侧 `indx` 只能由 8 个槽的先后顺序推断（即上一节"槽位顺序提供 indx=0..7"）。schema 侧的 `Ssds.indx` 是编辑器/运行时字段名；不要把它误读为每槽还有一个索引字节，也不要把运行时对象布局当磁盘布局。

同 DUNI 的 editor `.tree.json` 修改记录在索引 1/3/5/7 写入 `exis=true, capc=900, seat=true`；这是 editor 的 `new_value`，不是 `.dat` 原始值，样例 JSON 已分开标注。

### `table_25`：competition

- client payload 尺寸严格满足 `14 + 7,047×127 + 8 = 894,991`。
- 每行 row+118 的 u64 是重复-u32 `duni`；全部 7,047 行均满足且唯一。由此 `DBID` 候选取该重复 u32。
- DBID `131126` → duni `563181881786422`、row index 250、payload offset 31,882；DBID `130932` → duni `562348658130804`、row index 245、offset 31,247。`lookup` 同时找到 server table25 原始 byte hit，但 server table25 尚无固定行边界解码。
- `database_table_type=25` 的 `cext` 属性反转映射到 `comp.xml#comp`，支持 table25 的 competition 候选；完整 127 字节中的其余字段尚未逐字段映射到 255 个 schema 字段。样例见 `reports/dbdat_decode/client_table_25_competition_samples.json`。

### `table_10`：nation 候选

- client header count=251；`472446402670` 的 little-endian 字节 `6e 00 00 00 6e 00 00 00` 在 table10 payload offset 4,166 命中。它支持 nation 候选，但表10行变长，offset 4,166 尚不能断言为某一 row 的起始/字段偏移。
- `database_table_type=10` 的 `Nntp` 反转映射到 `nation.xml#nati`，与 table10 结构/计数相符。当前只输出 raw locator，不伪造字段或 row index：`reports/dbdat_decode/client_table_10_nation_locator.json`。

## 查找器与测试

`scripts/modding_read_dbdat.py` 的 `lookup(db_unique_id)` 已落地：

- 64-bit 输入按 little-endian duni 原样搜索；32-bit 输入按 `(dbid << 32) | dbid` 扩成重复-u32 候选。
- 搜索当前目录可用的 client/server `table_N.dat`。只有命中已验证固定行 duni 偏移时才返回 `record_index`；table10 或其它 raw hit 会标为边界未验证。
- IDs 可能是 table-local：例如 `472446402670` 也会出现在 table25 row94 和其它引用处。返回结果包含 archive/table/匹配置信度；不能把不带 table type 的原始 hit 当成全局唯一记录。
- 已测试：131126→table25 row250；130932→table25 row245；23318212→table21 row18795（client+server）；DUNI `100150957964512964` 也命中同两行。明细：`reports/dbdat_decode/dbdat_lookup_tests.json`。

## 名称索引：DBID → 本地化主名称

新增只读工具：`scripts/modding_db_names.py`；样例与交叉验证：`reports/dbdat_decode/name_index_samples.json`。

### `name_table_*` 的格式和用途边界

client 与 server 归档各含同一组 6 个资源：`name_table_{0,1,2}.dat` 与 `name_table_extra_{0,1,2}.dat`。三个主表分别有 245,981、542,060、85,668 个 12-byte metadata rows；对应 extra 表 count 完全相同。

```text
name_table_i:
  tad. v3569 | u32 count | count × 12-byte metadata row
  metadata string ordinal: u32 @ row+2

name_table_extra_i:
  tad. v3569 | u32 count | repeated {u32 string_id, u32 utf8_byte_length, utf8_bytes}
```

对三组完整验证：metadata row 的 `u32@+2` 等于同序 extra `string_id`；extra 各项 UTF-8 合法、string_id 为 `0..count-1`，所有 payload 字节均消费。metadata 剩下的 `u16@0/+6/+8/+10` 语义未定。样例字符串包括 pool0 `Sabri / Oldřich / Miko`、pool1 `Ramadhan / Nejedlý / Mistakesson`、pool2 `DJ Buffonge / Steven Rua / Tre' Ming`。这些是序号索引的 name-pool 数据，不是 `(DBID,string)` 字典；不能用 extra string ordinal 当 entity DBID。完整计数/样例在上述 JSON 的 `name_table_pools`。

### Entity 名字实际来自 language-update 表

本机有 `lang_update_db.dat`，它的 FMF 条目按 `lang_update_db/{language_id}_{table_id}.dat` 组织。已验证的名称资源映射：

| entity | localized-name table suffix | schema 主字段 | identity/data-table 候选 |
|---|---:|---|---:|
| stadium | 21 | `Snam` | 21 |
| club | 3 | `Cnam` | 3 |
| nation | 9 | `Nnam` | 10 |
| comp | 25 | `cnam` | 25 |

Nation 的 name-stream 使用 table9（251 条记录、语言文件可见 `DBID=134 → Singapore/Singapour/新加坡`），而 editor schema 的 nation database type 候选是 table10；这是 name/data 拆分的高置信相关性，不把 table9 与 table10 强行视为同一 row serializer。

语言资源表共同特征：payload 是 `tad.` v3569，offset8 为记录数；行首可识别 `u32 DBID + u32 UTF-8 byte_length + primary string`。后面可继续有 short-name 等字段/标记，当前工具只提取 schema 主名称（`Snam/Cnam/Nnam/cnam`），不声称完整解出每种 entity 的尾随字段。以对应基础表的 DBID 候选集过滤后，按文件位置恢复严格递增 DBID 序列；每种 entity 的 22 个 language-update 文件，其该序列长度都与 header count 完全相等。table21/table25 的 DBID 集来自已经验证的固定行 duni；club/nation 的 DBID 候选来自 base payload 中重复-u32 模式，再由记录数和顺序复核。

这与 `reports/editor_schema/NAMING_MODEL.md` 一致：`Snam/Cnam/Nnam/cnam` 是普通 `string`，但 `is_language_field=true`；同一 DBID 在不同 language-id 文件出现不同名称。它们是实体字段值，不是 `translation_id`。默认选择语言 ID 7（若该 DBID 有英文值），否则返回首个可用 locale；可用 `--language` 指定一个语言 ID/已知语言标签。其它语言前缀仍保留数值 ID，未知标签不按文件名顺序猜。

当前已索引的 localized primary-name 覆盖量（仅计本机 `lang_update_db` 更新记录，不代表基础数据库完整覆盖）：

| entity | language 文件 | 合计记录数 | 不同 DBID |
|---|---:|---:|---:|
| stadium | 22 | 11,840 | 1,466 |
| club | 22 | 72,264 | 6,603 |
| nation | 22 | 519 | 251 |
| comp | 22 | 876 | 318 |

### Stadium improvements 交叉验证与缺名记录

`Stadium improvements.json` 有 **1,227 个全档案唯一 duni**：按 `dtty` 分组后为 1,217 个 type-21 stadium duni，加 10 个 type-3 club duni。因此用户给出的 1,227 与全档案唯一值总数吻合，但严格按 stadium type 统计是 1,217。type-21 目标中，114 个在本机至少一个 language-update stadium 文件中有名称，达到 ≥50 验收。`name_index_samples.json` 包含 114 条 DBID→名称映射，以及 10 条人工地标核验：Villa Park/Birmingham、Parc des Princes/Paris、Roazhon Park/Rennes、Camp Nou 与 Estadi Olímpic/Barcelona、De Kuip/Rotterdam、HBF Park/Perth、Industree Group Stadium/Gosford、Lerkendal/Trondheim、Rajko Mitić/Belgrade；对应 table21 行坐标与这些城市吻合。另列出档案中的 10 个 type-3 duni，避免将 club 记录算成 stadium。

- 大庆球场 DBID 23318212 仍能验证到 `server_db/table_21` row 18795（坐标约 46.4595, 125.1864），但在本机 22 个 `lang_update_db/*_21.dat` 中没有该 DBID 的主名称记录；固定步长 row 本身不含 UTF-8 名字，`name_table_*` 也没有 DBID 键。因此工具返回 `name=null` 并保留 row/坐标，不把猜测名冒充原名。
- DBID 131126/130932 分别仍命中 table25 row250/245，但在本机所有 22 个 `*_25.dat` 名称流中无对应 DBID。table25 的 base 127-byte row 尚未解到 `cnam`/字符串引用，故也如实返回未解析。
- base `client_db/table_3.dat` 有字符串 `Daqing Xinsenweitehengtai`，但它是 club 表文本，未证明与 stadium DBID 23318212 有外键关系，不能作为大庆球场的显示名。

### 重跑名称查询

```powershell
python -I scripts/modding_db_names.py --lookup 603 --entity stadium
python -I scripts/modding_db_names.py --lookup 23318212 --entity stadium
python -I scripts/modding_db_names.py --lookup 131126 --entity comp
python -I scripts/modding_db_names.py --search "Villa Park" --entity stadium
python -I scripts/modding_db_names.py --search "Singapore" --entity nation --language 7
python -I scripts/modding_db_names.py --samples --output reports/dbdat_decode/name_index_samples.json
```

`--search` 默认跨所有可用 language-id 做子串搜索；`--entity` 可限定 stadium/club/nation/comp。工具只读 `client_db.dat` 与 `lang_update_db.dat`，输出文件只允许写入工作区。

## IDA 静态证据与加载器边界

### 已定位的相邻 helper（不是 `.dat` 主表 loader）

- `sub_1407C5A20`（新载入 `input/editor.exe` 的 VA）：字节 `0x1407C5B26: 3d 66 6d 66 2e` 比较 `fmf.`，`0x1407C5B2D: 3d 61 66 65 2e` 比较 `afe.`，并验证后续标志/版本。它是 FMF/AFE 头处理 helper，不是 `.dat` 的 `tad.` parser。
- `sub_144049A20`（同一 editor.exe 静态加载）：`0x144049A84: 81 7c 24 50 74 61 64 63 75 62`，即比较栈上 4CC 与 `tadc`，命中后调用 `sub_141219BF0`。这是 `tadc` 标签对象 helper 候选，尚未追到历史表载入调用链。
- 对 `input/editor.exe` 与 `input/fm.exe` 原始字节搜索均未发现连续 ASCII `tad.` 字符串；不排除该 tag 被拆分/运行时构造。FMF 字符串/比较点则可见。
- `sub_1449A06C0` 是 `Ssds` 子字段访问 helper，提供上节 struct offsets/flag bits；它本身不能证明 `.dat` row loader 的调用链。

### 未完成与 IDA 文件状态

- `ida/fm.i64` 可打开；`ida/editor.i64` 仍以 rc=4 失败，因此未在该 i64 中取得 loader 函数。曾从 `input/editor.exe` 做临时无自动分析静态加载来读取以上地址；没有把它说成原 editor.i64 证据。
- 当前没有证据将上述 helper 连接到 `tad.` v3569 的主数据表加载/通用反序列化函数，也没有定位 Zstd 解压后行流的入口。v3 对目标1仍标为部分完成/阻塞，未伪造调用链。

## 历史索引与 `summary.dat`

详细校验数据见 `reports/dbdat_decode/history_index_summary.json`。

- `pl_hist_index.dat` 全流解压 4,124,652 字节：u32 count=515,581，之后为 515,581 对 `(sorted_id, row_index)`；第一列严格递增，第二列严格等于 `0..515580`。
- `pl_hist_id.dat` offset8 起 1,031,162 个 u32，即 515,581 对 `(start,end)`。从 `(0,748),(792,1496),(1540,2420),...` 可验证每对满足 `start<=end`，所有相邻范围 `next_start - previous_end = 44`。
- `pl_hist_dt.dat` 所有串联 Zstd frame 解压共 198,695,332 字节；最后 indexed end=198,695,288，末尾余 44 字节。player index→id pair→dt byte-range 的关系有强结构支持；range 内 history record 的字段语义仍未解。
- non-player：b51 全量复核 `non_pl_hist_index` 的 754,688 对中有 746,543 个有效 range ordinal 和 8,145 个 `0xffffffff` sentinel；重复 key 保留。`non_pl_hist_id` 746,543 对是 24B 对齐的 inclusive 范围；`non_pl_hist_dt` 3,212,443 条 24B 行由范围/next 链完整覆盖，0 违例（L1）。详见 `reports/dbdat_decode/NONPL_HIST_INDEX.md` + `nonpl_hist_index.json`。
- `summary.dat` 大小 1,648,018；头 `03 01 "tad." f1 0d`。v4 已确认它是 editor 的 database summary，完整布局见下一节；旧的逐 u32 观察（offset8=7、offset12..36=1..7、offset40=251 等）已被吸收进该布局：offset8..36 是第一条 id 向量段 `{count=7, ids=[1..7]}`，offset40 起的 251/3/1280/156928/256 属于未解的 block2。

## `summary.dat`：编辑器数据库摘要（v4 专节）

复跑：`python -I scripts/modding_read_summary.py --output reports/dbdat_decode/summary_dat_read.json`（只读，输出限工作区；字节记账精确覆盖全文件）。结构证据与假设判定：`reports/dbdat_decode/summary_dat.json`。

### 身份（静态证据链，全部来自 `input/editor.exe` 的手工 capstone 反汇编）

- 字符串簇：`ERROR: Could not save database summary`、`ERROR: Could not create database summary`、`Could not remove database summary`、`Creating database summary for ` + ` people kept for `、`ERROR: Cannot create database summary with no dbc files, ...`；源文件路径串 `..\..\code\database_summary.cpp`。
- 文件名不是完整字面量：代码用 `mov dword ['summ'] / mov dword ['mary']` 现场拼出 `"summary"`（长度 7），再与 `".dat"` 字面量一起经 `vtable+0xe0(this, out, "summary", ".dat")` 查找/创建；随后 `0x1407d1280(tag='NULL', out, file, 0xdf1=3569)` 打开 tad 包装对象。这解释了为什么两个 exe 里都搜不到 `"summary.dat"` 连续字符串（fm.exe 也没有任何 `summary` 立即数构造——运行时读取方不在本证据链内）。
- tad 头是逐字段写出的：`write(1B 0x03) + write(1B flag) + write(4B 'tad.') + write(2B version)`（写原语为流对象 `vtbl+0x28(ptr,len)`），与文件头 `03 01 74 61 64 2e f1 0d` 完全吻合。
- 第一段由 id 向量写出器 `0x140ff3840` 生成：`write(count,4)` + 每元素 `write(id,4)` → 文件里的 `{7, [1..7]}`。
- 写出器内含数据质检：对记录 `dword@+4 == 0x303`(771) 且 `dword@+0x90 > 0` 的对象记录告警串 `Germany should not be manageable`（立即数拼接），说明摘要内含数据库质量校验结果。
- 日志串 `Creating database summary for <N> people kept for <M>`：N 来自一个 u32 向量的元素数（`(end-begin)>>2`），与"people"直接相关。

### 文件布局（字节记账精确覆盖 1,648,018 B）

```text
0x000000  8B   tad. 头：03 | flag 01 | 'tad.' | u16 3569
0x000008  36B  id 向量段：{u32 count=7}{u32 ×7 = 1..7}
0x000028  33B  block2（未解）：u32 ×5 = 251, 3, 1280, 156928, 256
               + 13B 碎片 00 5a 92 01 00 ff 7f 8d 1e 97 00 00 00
               （碎片内含 103002 = 记录流第一个 base 序号）
0x000049  …    记录流：54,086 条，分隔符 = ff ff ff ff(-1) + 类型字节 03
0x18FA96  …    收尾段：head(40B) + {2486}{升序 id} + {126}{升序 id}
               + 63 ×(u32 0..64, float32) 对 + u32 -1 终止符
```

记录流两类记录：

- **标准记录**（53,742 条，17B）：`[u32 id][13B payload]`；payload = `[b0][b1][b2][b3][b4][b5][u16@6][u16@8][u16@10][00]`。统计：b0∈{1,2,3}(占 99.96%)、b1∈{4,5,6,7}(b1=4 占 94.1%)、b3/b4 以 0x0b 为主且 b4≈b3 或 b3+1、b5∈{1..6}；u16@6/8/10 共享同一值池（212、1057、346、518、140、144、0x7000、0x7fc0、0x7fff 哨兵…）。id 列全流近似递增（57 → 2,000,339,170）。
- **扩展记录候选**（117 条按现有判据命中）：17B body prefix + 8×00 + `u32 count` + `u32 base`（103,0xx）+ 8B 对数组；count/base/A/B 的业务字段意义未定，344 个非 17B body 也未逐个映射。b51 的 11 个标准 raw 槽均为 L1 定位、0 个 L2 命名；完整字段表、逐值统计、writer L3 路径与负结果见 `reports/dbdat_decode/SUMMARY_SEMANTICS.md` / `summary_field_map.json`。

收尾段：head = `250 | 82,082,540 | 0 | -1 | -1 | (0x00d4,0x7fff) | 0 | 0 | 0 | 0`（字段角色未解）；随后 `{count=2486}{2486 个升序 id}`（156,580 → 2,000,300,412，含 12,040,2xx/12,079,xxx/13,1xx,xxx 等连续 id 块与 2,000,xxx,xxx 段）、`{count=126}{126 个升序 id}`（1..117 缺 34、1,000,000..1,000,004、2,000,005,181..2,000,254,976）、63 对 `(u32 0..64, float32)` + `-1` 终止（u32 列缺 57/61，形似按 age 的直方/均值表）。

### 假设判定（验收项）

1. **表计数/行数汇总说：证伪**。251/3/1280/156928/256 与 client_db 20 个表的行数（48,413/7,047/84,259/56,293/2,488/…）及 31 项目录均对不上；文件里没有任何按表组织的行数数据。251 与 table_9/table_10 的 251 行相同属巧合。
2. **schema 罗塞塔说：证伪**。全文件没有 per-table 步长/偏移/字段布局信息，无法解释 table_21 的 181B 步长、table_25 的 127B 步长或 table_3 的变长行；记录 payload 是按实体的 13 字节结构，不是表 schema。
3. **存档 summary 同族说：证伪**。save 侧 `save_game_summary.dat` 是 `tad.` v22（0x16）、1,678B、文本型（`[len][utf8]` 字段如 `110,MALE,1,0`、`24.4.2`）；`summary.dat` 是 `tad.` v3569 二进制记录流。仅名字相近，序列化器不同族。
4. **新假设（未证实）**："people kept 序号"——base 序号 103,0xx 与 156,928−103,002=53,926 ≈ 记录数 54,086（差 160）吻合"全局 people 列表序号"的解释，但不能证明。
5. **id 空间测试（负结果）**：记录 id/对数组 A/B 与 pl_hist_index id 集、table_3/table_2 的 repeated-u32 duni 候选、club 语言名称文件的 DBID 都只有弱重叠或不重叠；A 列 12,040,2xx 连续块的实体语义未解。



只读脚本：`scripts/modding_read_dbdat.py`，在 `python -I` 下从工作区 `tools/python` 导入 Zstandard。`--output` 限制在工作区内。

```powershell
python -I scripts/modding_read_dbdat.py --help
python -I scripts/modding_read_dbdat.py --list-tables
python -I scripts/modding_read_dbdat.py --list-tables --archive server_db.dat
python -I scripts/modding_read_dbdat.py --scan 21 --archive server_db.dat --limit 3
python -I scripts/modding_read_dbdat.py --scan 25 --limit 3
python -I scripts/modding_read_dbdat.py --scan 10
python -I scripts/modding_read_dbdat.py --lookup 23318212
python -I scripts/modding_read_dbdat.py --lookup 131126
python -I scripts/modding_read_dbdat.py --inspect
```

`scan(21)` 对 client/server 表行结构做校验；server 模式包含 `Ssds` 槽解码。`scan(25)` 解码固定行和 identity，保留其余 raw row；`scan(10)` 明确只报告 header/raw sample。`scan(41/56)` 保留上一版完整解码。

## 尚未完成

1. 从 `tadc`/Zstd helper 追到 `.dat` 主数据库表加载及通用字段流反序列化调用链。
2. 解 `table_10` 变长 row，并将 table10/table25 的所有 row bytes 映射到 schema 字段。
3. 解 `name_table_*` 剩余 metadata 列、`table_extra_*` 及 server-only 其他表的外键/名称引用关系。
4. `summary.dat` 的 payload b0..b5/u16、扩展 count/A/B、收尾 head 与 `(u32,float)` 表语义仍未解；b51 已交付逐槽负结果与 editor.exe writer 的 L3 路径（见 `SUMMARY_SEMANTICS.md`）。历史库剩余语义缺口：non-player role 枚举 176 种仍未与独立 staff/title 表定名；pl_hist 的稀见 row_type ≥3 本轮做了全量拆分但 0/14 获得独立 L2 定级（见 `HIST_RARE_TYPES_B51.md`）。
5. 找到 `summary.dat` 的运行时读取方（fm.exe 无 `summary.dat`/`summary` 文件名字面量；写入方为 editor.exe 已证）。
