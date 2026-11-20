# `table_extra_N` 布局模型判定（b17 残留项正式结案，b37）

> **b47 后续补充（2026-11-17）：**本文对 `table_extra_3` 的“行边界未恢复”是 b17 时点结论。b47 现用 client ordinal + `Cyfn@+4` 年域恢复了 84,259 条 client 边界；server ordinal 全序列覆盖 84,259 项，53,572/53,592 个非空 client 年值在同 ordinal server 区间出现。server 的低置信残项、三路线证伪和计数差异见 [`DB_TABLES_BIG.md`](DB_TABLES_BIG.md) 的 table_3 / table_extra_3 节；本文其余表结论不变。

> 证据等级口径见 README「证据等级口径」。本文全部结论为 **L1**（本机安装库字节 + 工作区解码器；安装库是游戏自己的数据，但读取工具是本工作区的，没有第二个独立参照，故不升级为 L2）。**L4 = 0**。
>
> 只读边界：`client_db.dat` / `server_db.dat` 从游戏目录只读打开；写入只发生在 `reports/dbdat_decode/extra_tables_verdict.json`（本报告第 1–5 节）与 `reports/save_decode/`（第 6 节，样本副本）。
>
> 机读结论：`reports/dbdat_decode/extra_tables_verdict.json`；复跑：
> ```powershell
> python -I scripts\extra_tables_verdict.py --save-game-db "reports\save_decode\extracted\1 1-大连人\1 1-大连人\game_db.dat"
> ```

## 0. 结案：b17 的问题是什么、答案是什么

b17 / FMRTE 洁室审计的第一优先级问题是：「`table_extra_N` 是否记录**行偏移/长度表**？」

**答案：否，全部证伪。** 五个 extra 表（client `extra_3`/`extra_9`，server `extra_3`/`extra_9`/`extra_24`）没有一个是行偏移表或行长度表；正确的模型是**记录头（record header）**——记录/行自带 rownum（row ordinal）键，而不是由一个中心偏移数组索引。这正是 `reports/qa/FMRTE_CLEANROOM_AUDIT.md` 预判的"证伪后转向记录头"路线。

| 表 | 记录数 | 表体字节 | 模型判定 | 关键证据 | 反例（保留） |
|---|---:|---:|---|---|---|
| client `table_extra_3` | 84,259 | 13,053,908 | **ordinal 标记的变长行**（行边界未恢复） | 全表存在完整的 0..84,258 递增 u32 序列；表头 count == `table_3` count | 贪婪序列位置不可靠：前两行位置仅相距 51 B（server 侧为 9 B，明确为行内杂散值） |
| client `table_extra_9` | 251 | 83,927 | **ordinal 标记的变长行**（行边界未恢复） | 行 0/1/2 的 ordinal 前缀分别在 12/262/705，且 12+4 是 `u32 11 + "Les Fennecs"`；b34 客户端↔服务器 199/199 同 row_index 同文本 | "行 = ordinal + u32 长度 + 文本" 的**连续**模型在 row 1 就被证伪（row 1 @262 之后是二进制载荷，不是字符串） |
| server `table_extra_3` | 84,259 | 35,009,248 | **ordinal 标记的变长行**（行边界未恢复） | 同上；行首模板含重复默认 4 字节 `00 6c 07 01`（0x01076c00）与 `6c 07`(=1900) | 贪婪序列自相矛盾（前两行相距 9 B）→ 位置不可用；每行长度模型未解 |
| server `table_extra_9` | 251 | 105,228 | **ordinal 标记的变长行**（行边界未恢复） | 同 client extra_9，且与 client 的行序号/文本交叉命中 | 同上 |
| server `table_extra_24` | 84,507 | 6,929,586 | **ordinal 键控定长 82 B 行**（已解） | `6,929,586 = 12 + 82 × 84,507` 精确；84,507/84,507 行的前 4 字节 = 0-based 行序号（0..84,506）；自动化 stride 搜索独立命中 stride=82 且覆盖全文件 | 无（该模型通过全部测试）；字段语义仍未解（只有 3 个字节变动） |

**每个 extra 表的 count 都等于对应 `table_N` 的 count**（84,259 / 251 / 84,507），这支持"extra 表是主表的**行键控补充区**"这一读法。

## 1. 模型测试定义（可复跑、可证伪）

`scripts/extra_tables_verdict.py` 对每个 extra 表依次跑以下测试，任何通过的模型都必须同时给出反例：

| 测试 | 判定"通过"的条件 |
|---|---|
| `row_offset_table` (u32/u64 @12) | 表体开头是 `count` 个严格递增的偏移量，首值不在数据区外 |
| `row_offset_at_candidate_offsets` | 在表头偏移 12..64（步长 2）任一位置存在同样的递增偏移数组 |
| `row_length_table` (u16/u32) | `count` 个长度值全部落在 `(0, len(body)]` 且**总和等于表体长度** |
| `ordinal_fixed_stride` | `count × stride == len(body-12)`，且每条记录首 u32 严格等于其 0-based 行序号 |
| `ordinal_slot_stride` | 存在 stride ∈ [8,1024]，使前 min(count,1000) 个槽位首 u32 等于槽位序号（再全量复核） |
| `index_string_rows` | 行是连续的 `(u32 ordinal, u32 byte length, UTF-8)`，ordinal 严格递增且恰好 `count` 行、恰好消费到表尾 |
| `ordinal_sequence_scan`（启发式） | 表体内存在完整的 0..count-1 递增 u32 序列（贪婪匹配，**位置可能落在行内杂散值上**，因此另报最小间距） |
| `periodic_u32_runs` | 存在 ≥8 个连续相同 u32（模板/默认值填充签名） |

## 2. 证伪记录（b17 的直接答案）

- **行偏移表：证伪。** 五个表的表体开头都不是递增偏移数组；额外在 12..64 的 27 个候选表头偏移上重试，**没有任何偏移通过**（`row_offset_at_candidate_offsets.passing_offsets == 0`）。举例（client `table_extra_3` @12 起 4 个 u32）：`0x00000000, 0xFFFF079B, 0x0000FFFF, 0x00000000`——第 2 个值就在文件之外，绝不可能是偏移量。
- **行长度表：证伪。** u16/u32 长度数组的总和与表体长度相差 5–6 个数量级（例：client extra_3 `sum=144,658,115,803,400` vs body `13,053,896`），且存在大量 `0xFFFFFFFF`/超长值。
- **定长 stride（除 extra_24 外）：证伪。** `(len-12) % count != 0`（client extra_3：13,053,896 / 84,259 = 154.90…；server extra_3：35,009,236 / 84,259 = 415.5…），因此不存在整数 stride。
- **"ordinal + 长度 + 文本"连续行：证伪（extra_9）。** row 0 (@12) 之后 row 1 的位置上不是长度前缀而是二进制载荷；b34 记录的"row 1 长度前缀在 266"实际上是**槽位内偏移**（12 + 250 附近），不是连续行的第二个元素。这一条很重要：它把 b34 的 199/199 字符串命中从"行结构已解"收紧为"**行内含 ordinal 键控的字符串记录，行边界未解**"。
- **保留的反例**都在 verdict JSON 的 `models[*].counterexample` 与 `ordinal_scan_counterexample` 字段里，未做任何删除。

## 3. `table_extra_24`（server）：唯一已解的定长模型

- `6,929,586 = 12 + 82 × 84,507`，`stride=82` 精确整除；**全部 84,507 行的首 u32 依序等于 0..84,506**（自动化测试 `ordinal_fixed_stride` + `ordinal_slot_stride(stride=82)` 双路径独立通过）。
- 记录内 `+4..+7 = FF FF FF FF`，`+12..+15` 恒为 `10000`（`0x2710`），另有 `6c 07`(=1900) 反复出现 → 大量默认/模板填充。
- 只有 3 个字节在行间变化：`+10`、`+11`（各取 0..7）与 `+81`（取 {0,2,99}）→ 每行除序号外是"默认模板 + 2 字节小枚举 + 1 字节标志"。
- 与 `table_24` count 相同（84,507）→ 行键控的 Team 补充区。
- **未解**：`+10/+11/+81` 与 Team schema 字段（`Trep`/division/contract 等）的映射无证据，不给命名。

## 4. `table_extra_3`：记录头方向可行，但行边界仍是断点

- 两侧 count 都是 84,259（= `table_3` count）；client 13,053,908 B vs server 35,009,248 B → **server 每行平均多约 260 B**，说明 server 侧行内多一段变长载荷（与 server 表普遍更"富"的观察一致）。
- server 行首可见模板（行 0 @12）：`00 00 00 00 | 03 07 00 00 | 00 01 00 00 | 00 01 00 00 | 00 00 00 01 | 00 6c 07 01 | 00 6c 07 01 | …`——首 u32 = 行序号，其后是反复出现的默认 4 字节 `00 6c 07 01`；这类重复在 `periodic_u32_runs` 中表现为最长 12 个连续相同 u32（值 `0x00000000`）。
- 贪婪 ordinal 扫描在两侧都能找到完整的 0..84,258 序列（这个序列**不可能是巧合**：逐步命中特定值的随机概率约 1/2³² 量级），但**位置不等于行起点**（server 侧前两个位置相距 9 B）。因此结论写成"ordinal 标记的变长行，行边界未恢复"，并把 9 B 间距作为反例保留。
- 下一跳（静态手段，本工作区可复跑）：server extra_3 行内多出的 ~260 B/行需要独立边界证据——建议用 `table_extra_3` 与 `table_3` 的同索引行做**逐字节互信息/公共子串**对照，或找编辑器/游戏侧读该表的 tag→schema 绑定证据，而不是继续猜偏移。

## 5. `table_extra_9`：字符串层结论保留，行结构收紧

- 行 0：@12 `u32 0`，@16 `u32 11`，@20 `"Les Fennecs"`；行 1 的 ordinal 前缀在 @262（不是 31），行 2 在 @705 —— **变长且不均匀**。
- b34 的 client↔server 交叉（199 个 `(row_index, length, text)`，199/199 同长度同文本同 row_index）在字符串层面成立，本报告沿用为 L1；但它**不**证明行是连续的 `(ordinal, length, text)` 记录。
- 内容确认为国家队昵称（`Les Fennecs`、`Palancas Negras`、`Les Écureuils`、`The Zebras`、`The Pharaohs`、`The Black Stars`…），server 侧额外含姓名池字符串。

## 6. save 侧 `game_db.dat`：没有名字目录，但有同款记录签名

对 `reports/save_decode/extracted/1 1-大连人/1 1-大连人/game_db.dat`（83,432,017 B）的结构扫描：

| 检查 | 结果 |
|---|---|
| 嵌套 `fmf.` magic 计数 | **0**（不是档案容器） |
| `tad.` magic 计数 | **1**（整份文件一个 TAD 头，v3569） |
| `table_` / `game_db` 名字字符串 | **0 / 0**（没有名字目录，`extra_N` 是**安装库的 file-level 成员命名**） |
| 181 B stride 上的递增序号段 | **21,064 行**，起始字节 `27,837,953`（= 行区 27,837,785 + 168），序号从 0 起 → **独立复现了 `game_db_alignment.json` 的 table_21 对齐**（本轮用完全不同的方法：算术级数扫描） |
| 82 B stride 上的递增序号段 | **136 段**，最大 8,268 行（起始字节 40,220,864，序号 33,375）；另有多段 5,312 / 4,260 行 → 与安装库 82 B `table_extra_24` 行同构的**逐行记录区**，无名字可绑 |
| 38 B / 127 B stride | 0 段（本轮范围内未定位） |

**结论**：save 侧 `game_db.dat` 是**无目录的对象/记录流**，`table_extra_N` 这种"按名字枚举的成员"在 save 侧不存在；但安装库的**逐行记录布局在 save 侧仍在用**（181 B 与 82 B 两种 stride 都被独立扫到）。要按表枚举 save 侧记录，需要的是运行时注册表（`GAME_DATABASE_RECORD`）或对象类型映射（`memory_pools.dat` 的 pool 类型名），不是文件目录——这与 `reports/save_decode/IDA_LOAD_CHAIN.md` 第 4 节的断点一致。

## 7. 与其它报告的关系

- `reports/dbdat_decode/PEOPLE_DB.md`：本文第 5 节收紧其"`table_extra_9` 行结构"表述（字符串层结论保留，行边界未解）；第 3 节复述并自动化复核其 `table_extra_24` 结论。
- `reports/qa/FMRTE_CLEANROOM_AUDIT.md`：第一优先级（extra 表偏移/长度表）在本报告结案；第 3 节的写回风险另见 `reports/SAVE_WRITE_PROTO.md`。
- `reports/save_decode/game_info_census.json` + `GAME_INFO_FIELDS.md`：`game_info.dat` 25–257 的逐偏移普查（本任务的第 4 项）。

## 8. 独立双实现交叉验证（2026-11-16 第二轮）

本节由第二条并行会话**不看本文与 `extra_tables_verdict.py`**、独立实现 `scripts/analyze_extra_tables.py` 后得出。两套实现的模型命名不同，但**逐表语义判定完全一致**，因此第 0 节的结案结论获得一次方法独立的交叉支持（仍为 L1：两套实现都读同一批安装库字节，且都由本工作区编写，不是外部参照）。

| 表 | 本报告 / `extra_tables_verdict.py` | 独立实现 `analyze_extra_tables.py` | 一致？ |
|---|---|---|---|
| client / server `name_table_extra_0/1/2` | （本文未涉及） | `length_prefixed_string_pool`，confidence high | — |
| client `table_extra_3` | `ordinal_tagged_variable_rows` | `ordinal_keyed_variable_rows`，medium，`supported_with_boundary_ambiguity` | **是** |
| client `table_extra_9` | `ordinal_tagged_variable_rows` | `ordinal_keyed_variable_rows`，medium | **是** |
| server `table_extra_3` | `ordinal_tagged_variable_rows` | `ordinal_keyed_variable_rows`，medium | **是** |
| server `table_extra_9` | `ordinal_tagged_variable_rows` | `ordinal_keyed_variable_rows`，medium | **是** |
| server `table_extra_24` | `ordinal_keyed_fixed_stride_rows` | `fixed_stride_records`，high，stride 82，ordinal 84,507/84,507 | **是** |

两套实现都独立给出"行偏移表被证伪"的反例，且反例形式不同（本报告用"表体开头不递增"，独立实现用"`u32[i]` 超出 body 长度 + 偏移不减性被破坏"），互不依赖。

`name_table_extra_*` 的补充结论（独立实现给出；本轮未在安装库上逐字节复核，**仅作线索，不计入结案**）：三张表分别有 245,981 / 542,060 / 85,668 条 `(u32 id, u32 len, utf8)` 记录，id 从 0 连续递增、全部消费到 EOF；client 与 server 两侧载荷**完全相同**。这与既有 `DBDAT_FORMAT.md` 对 `name_table_extra_i` 的描述（`{u32 id, u32 len, utf8}`）一致，可视为对该描述的独立复核。

机读件：`reports/dbdat_decode/EXTRA_TABLES.json`（独立实现，含每张表的 `refuted_models[].counterexamples`）。两套实现并存，便于日后任一方出错时对照。

**边界**：本节不改变第 0 节任何判定的证据等级——双实现一致性降低的是"实现出错"概率，不是获得外部独立参照（L2）。`table_extra_3/9` 的行边界仍然未解。

## 9. save 侧内联国籍昵称记录的独立复现（2026-11-16 第二轮）

第 6 节提到 save 侧 `game_db.dat` 有"同款记录签名"但无名字目录。第二轮在 `1 1-大连人/game_db.dat`（83,432,017 B）里定位到一条**内联**的 `table_extra_9` 同形记录：

| 偏移 | 字节 | 解释 |
|---|---|---|
| `0x346FFA9` | `fb 00 00 00` | u32 = 251（与安装库 `table_extra_9` 的记录数相同） |
| `0x346FFAD` | `00 00 00 00` | row ordinal = 0 |
| `0x346FFB1` | `0b 00 00 00` | u32 = 11（字符串长度） |
| `0x346FFB5` | `"Les Fennecs"` | 11 字节 UTF-8，与安装库 client/server extra_9 的 row 0 文本相同 |

**关键否定结果**：在其后按 `(ordinal, len, text)` 连续推进时，row 1 立刻失效（读到 `ordinal=45, len=17,301,504`）——与第 5 节安装库的结论**完全同构**。因此 save 侧不是"更规整的一版",而是同样的"槽位内 ordinal 键控字符串记录、行边界未解"。

**证据等级**：L1（save 字节 + 本工作区定位）。**未证**：这条记录属于哪张运行时表（save 侧无表名目录，见第 6 节与 `IDA_LOAD_CHAIN.md` §4 #4）。
