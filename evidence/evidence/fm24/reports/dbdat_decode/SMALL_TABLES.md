# b46 — client_db 小表与辅助条目业务字段普查

状态：完成本任务范围内 16 张小表与指定辅助条目的只读清点。工具：`scripts/b46_tables_small.py`；机读全量：`reports/dbdat_decode/db_tables_small.json`。数据只由 scoped FMF 读取器按目录随机读取显式目标成员；**未解压/分析** `table_2/3/21/25` 或 `table_extra_3`。未启动游戏/editor，未写安装目录或用户 Documents。

## 1. 结论摘要与证据口径

- 16/16 行边界模型均达到本工具的整表闭合条件：定长表精确满足 header + count × stride + footer；变长表由长度前缀名字/重复-u32 身份尾锚、单调身份序列及总行数共同走到 footer。以下结构结论均为 **L1**（自家工具对安装文件字节的结构记账），不称为 L2“验证通过”。
- 16 张表的实测 count 与任务书清单全部相符。11 张得到可重复-u32 身份字段；另有 table_41 的尾 trailer 身份、table_8 的 0-based 语言序号；table_47 未找到稳定 identity 槽。
- 身份映射档位：确认 9 / 候选 2 / 未知 5。仅把经 Schema、内容及独立公开事实支持的字段记作 **L2**；所有未达 L2 的表都明确给出负结论，不以行数巧合命名。
- L2 业务锚点：Award（公开奖项类别）、Injury（Plantar Fasciitis）、Media source（公开媒体/URL）、Language（语言名）、Nation（Singapore 等国家事实）、table_18 place-name（Oulu/Melbourne）、table_27 climate-name 候选、Currency（公开货币名/符号）。L3 本任务无；L4 仍为 **0**。

## 2. 每表边界、字段槽位与身份映射

偏移均相对行首；`rdui` 和重复-u32 `duni` 是结构命名（L1），不代表其余字段已映射 Schema。全量 byte/u16/u32 变动率、样例、原始 hash 与机器统计见 JSON 的 `tables[N].slots` / `identity_slots` / `field_slots`。

| 表 | 行数 | 行边界模型（L1） | 槽位/身份 | 表号→Schema entity | L2 或明确负结论 |
|---:|---:|---|---|---|---|
| 0 | 3,545 | 77 B 定长；`14 + 3545×77 + 8 = 272,987` | `rdui:u32@+64` = 0..3544；`duni:u64@+68` 两个 u32 相等且 3,545/3,545 唯一。其余 64 B 仅有变动率/对齐数值候选。 | **确认：award**；award.xml；38 个英文 name-update key 全部命中表内 duni。 | **L2**：`MLS Referee of the Year` 公开奖项类别与相应 identity key 关联。其它业务列未命名。 |
| 5 | 7 | 34 B 定长；`14 + 7×34 + 8 = 260` | `rdui:u32@+21` = 0..6；`duni:u64@+25` 重复 halves，ID=1..7。 | **候选：continent**；数量/ID 序列与 7 大洲兼容，但没有名称/外键闭环。 | **无 L2 命名字段**；7 行本身只是候选线索。 |
| 6 | 115 | 16 B 定长；`14 + 115×16 + 8 = 1,862` | `rdui:u32@+3` = 0..114；`duni:u64@+7` 重复 halves，115/115 唯一；余下前缀码与末 byte 不命名。 | **确认：injury**；`injury.xml`。 | **L2**：DBID 133 = `Plantar Fasciitis` / 足底筋膜炎，表内 identity 与英/简中名称层相连。其它业务列未命名。 |
| 7 | 208 | 变长；名字起始 + 单调 repeated-u32 identity 尾锚，208 行精确闭合；80–715 B，均值 176.933 B。 | 首槽为 length-prefixed UTF-8 source name；一组 6-byte 前缀后有 177/208 条可解析 URL 字符串候选；尾部为 `duni×2 + 00`。3/3 英文更新 key 与 slot0 文本逐值相同。 | **确认：media source**；`media source.xml`。 | **L2**：Daily Mirror 与 `mirror.co.uk` 公共名称/URL。URL 偏移角色仍标候选；hashtag/list/scalar 尾部未逐字段命名。 |
| 8 | 126 | 126 个有序语言名行；每行 `[u32 byte_len][UTF-8 name][30 B suffix]`，恰好消费到 footer。 | 后缀 30 B；后缀 `u32@+17` = 0..125，126/126 等于 0-based row ordinal。其余 suffix 字节逐 offset 统计，语义未知。 | **确认：language**；language.xml，名称槽候选 `Lnam`。 | **L2**：126 个语言名与公开语言名相符。suffix 的其它槽未命名。 |
| 9 | 251 | 变长；每行以 `FFFFFFFF` 开始，行尾 `duni×2 + 00` 后接下一 sentinel；251 行全闭合；58–461 B。 | 251/251 identity 唯一、严格递增；其 ID 顺序与 table_10 为 251/251 相同。 | **确认：nation 的 name/key companion**；不是 full Nation 行 serializer。 | **L2**：ID 134 对应 Singapore；简中名称键覆盖 250/251，唯一未覆盖 ID=217945。名称层到原始 key 的关联本身单列为 L1。 |
| 10 | 251 | 变长；按 table_9 的 251 个 identity key 有序寻址，重复-u32 尾锚 + marker 走到 footer；50–1,199 B。 | `duni×2` 尾锚；table_9/table_10 identity sequence 251/251 相等、唯一递增。行内其它标量保持 opaque。 | **确认：nation**；既有 type-10 `Nntp` 反向映射至 `nation.xml#nati`。 | **L2**：Singapore 等公开国家名与 identity key 对照；其余字段偏移未逐项命名。 |
| 18 | 1,567 | 变长；两个连续 length-prefixed UTF-8 名槽 + 单调 identity 尾锚，整表闭合；69–195 B。 | slot0/slot1 都是字符串。两字符串之后的二进制/列表区为 48–134 B（30 种长度）；尾部 `duni×2 + 00`。English 更新表 18 的 25/25 key 与 slot0 名相同。 | **确认：city-associated secondary-name data**（不等同于 table_2 主 City serializer）；依据 LANG_LAYER 第二城市名集合。 | **L2**：Oulu、Melbourne 等公开地名；25/25 英文 key/slot0 相符。中间变长区未映射到 city/local-region XML 槽位。 |
| 19 | 28 | 45 B 定长；`14 + 28×45 + 8 = 1,282` | `rdui:u32@+32` = 0..27；`duni:u64@+36` 重复 halves，28/28 唯一。前 32 B opaque。 | **未知**。 | **无 L2 命名字段**；边界/身份已解，业务含义未定。 |
| 22 | 449 | 13 B 定长；`14 + 449×13 + 8 = 5,859` | `rdui:u32@+0` = 0..448；`duni:u64@+4` = 1..449 重复 halves；末 byte 恒 0。 | **未知 / 序号映射样结构**。 | **无 L2 命名字段**；仅交付序号与身份三元组结构。 |
| 23 | 278 | 14 B 定长；`14 + 278×14 + 8 = 3,914` | `rdui:u32@+1` = 0..277；`duni:u64@+5` 重复 halves，末 byte 0；首 byte 为 0。 | **未知 / 序号映射样结构**。 | **无 L2 命名字段**。`table_for_old_save_23` 与该 payload 逐字节相同（L1）。 |
| 27 | 334 | 变长；名字 + 固定 99 B numeric middle + `duni×2 + 00`，334 行全闭合；117–156 B。 | 字符串槽为 profile name；99 B 中间区未逐字段命名；身份严格递增唯一。 | **候选：weather profile**；内容与 `weather.xml` 多项数字槽相容，未找 numeric table-type 绑定。 | **L2 候选名**：`Daw - Beijing`、`BWh - Aswan` 等气候分类/地点名。状态仍为候选；数字槽语义未定。 |
| 35 | 890 | 15 B 定长；`14 + 890×15 + 8 = 13,372` | `rdui:u32@+2` = 0..889；`duni:u64@+6` 重复 halves、890/890 唯一；末 byte 0。 | **未知 / 序号映射样结构**。 | **无 L2 命名字段**。 |
| 41 | 173 | 变长精确语法：4 个 length-prefixed UTF-8、f32、u32 history count、count×7B history、13B trailer；整表 74,352 B 全消费。行长 118–871 B，mean 429.653。 | 4 个字符串；current-rate f32；history item=`u8 kind + u16 year + f32`。trailer=`rdui:u32 + duni:u32×2 + marker:u8`，rdui=0..172，173/173 repeated identity 唯一。历史项共 9,156（每行 8–116）。 | **确认：currency**；`currency.xml`，`Cexr` 是 exchange-rate 候选。 | **L2**：Euro/€、US Dollar/$、Japanese Yen/￥、UK Pound/£。四个字符串的精确角色与 history kind 未完全命名；不据 rates 推断日期。 |
| 47 | 2,488 | 44 B 定长候选；11 B table prefix 后：`25 + 2488×44 + 8 = 109,505`。 | 全行变动率很高；在每行任意偏移搜索重复-u32：403 行 0 hit、1,350 行 1 hit、729 行 2 hit、6 行 3 hit；无稳定重复身份槽，不能命名 DUNI。 | **未知**。 | **无 L2 命名字段**；11 B 前缀与 44 B 行内槽只做字节/数值统计。 |
| 56 | 6 | 13 B 定长；`14 + 6×13 + 8 = 100` | `rdui:u32@+0` = 0..5；`duni:u64@+4` = 1..6 重复 halves；末 byte 0。 | **未知 / 序号映射样结构**。 | **无 L2 命名字段**。 |

### 2.1 变长 walk 的限制

- table_7/18/27 的记录身份锚位于尾部，名字在行首；walk 约束为 identity 严格递增、下一行首字符串锚、count 精确及到 footer 闭合。table_7 还将 URL（含 `://`）排除为下一行首名字。table_18/27 的中间数值/列表没有根据猜测命名。
- table_9 的行首 sentinel 与 table_9/table_10 的重复 identity 顺序提供互证；table_10 的一个重复键 hit（table key 768 的第二个 hit）没有被用作第二条 row，因为有序 key walk 已闭合 251 行。
- 固定步长与重复-u32 模型只说明本任务观察到的字节布局；不代表得到通用加载器 serializer，也不代表 L4。

## 3. 小表与 Schema 关系的确定度

`master.json` 实体映射不会因 count 相同自动升级。当前分档：

- **确认**：table_0 award、6 injury、7 media source、8 language、9 nation-name/key companion、10 nation、18 city-associated secondary-name data、41 currency。
- **候选**：table_5 continent、27 weather profile。
- **未知**：19、22、23、35、47、56。22/23/35/56 行内的连续 rdui 与重复 duni 有结构事实，但没有字段语义参照。

L2 仅用于与公开实体事实/名称/货币符号的对照；localized update key 与基础表 identity 的字节级关联仍是 L1。任务范围无 exe 静态证据（L3），未做游戏/editor 实际加载（L4=0）。

## 4. 辅助条目

### 4.1 `simple_vars.dat`

解压 payload **34 B**，全部按偏移切片，字段语义不推断：

```text
03017461642ef10d 0000 0800 0000 f10d 04000000 323433304b32 e807 97940400 e707
```

可读片段为 `2430K2`；其余槽位为 u16/u32 原值（见机读 JSON 的 `opaque_slots`）。**只解字节/长度，不命名数据库变量**（L1）。

### 4.2 `name_table_{0,1,2}` 与 `name_table_extra_{0,1,2}`

主表每行 12 B：`u16@0 | u32 string ordinal@2 | u16@6 | u16@8 | u16@10`。`extra_i` 是 `(u32 string_id, u32 UTF-8 byte_length, UTF-8)` 连续流。

| pool | rows / strings | unique text values | 样例（只作内容描述） |
|---:|---:|---:|---|
| 0 | 245,981 | 143,282 | Sabri / Oldřich / Miko |
| 1 | 542,060 | 395,739 | Ramadhan / Nejedlý / Mistakesson |
| 2 | 85,668 | 81,873 | DJ Buffonge / Steven Rua / Tre' Ming |

结构闭环：3/3 pool 的 metadata `u32@+2` 与同序 extra `string_id` 完全相同；extra id 精确为 `0..count-1`，UTF-8 合法且全体 payload 消费至 EOF。client/server 两边主表与 extra 表的三组字节均完全相同（L1）。因此本次可命名的“引用关系”是 **metadata row ordinal → 对应 extra string row 的 local string id**。

边界：ordinal 是 pool-local string index，不是 entity DBID。3 个 pool 的人名文本/计数不同，但“given/family/full-name”角色未独立证明；本任务未证明 16 张小表的任何业务字段引用这三组 pool，也不把相同数值猜成外键。metadata 其余四个 u16 槽的语义仍未知。

### 4.3 旧存档表条目

- `table_for_old_save_23.dat`：278 行、14 B stride；与 client `table_23` payload 逐字节相同（L1）。
- `table_for_old_save_25.dat`：7,047 行，`14 + 7047×123 + 8 = 866,803`，stride=123 B；只做结构清点，没有打开/比较主 `table_25` payload，也不命名字段。

## 5. 复跑与审计边界

```powershell
py -V:3.12 -I scripts/b46_tables_small.py --help
py -V:3.12 -I scripts/b46_tables_small.py --selftest
py -V:3.12 -I scripts/b46_tables_small.py --table 56
py -V:3.12 -I scripts/b46_tables_small.py --json reports/dbdat_decode/db_tables_small.json
```

`--json PATH` 会拒绝 worktree 以外路径。ScopedArchive 只读 FMF 目录以及显式目标压缩成员；全量 JSON `meta.decompressed_entry_paths_by_archive` 记录本次实际解压的成员路径，`prohibited_table_payloads_decompressed` 为空。所有输出都在本 worktree。