# lang_update_db.dat 语言更新层深度解码（LANG_LAYER）

任务范围：`db/2430/lang_update_db.dat`（语言更新层）的容器结构、语言模型、行语法、中文内容、名称覆盖评估，以及与 `lang_db_2400.dat`（基础层）的双层机制。全部结论只读游戏目录得出，可重跑脚本见文末。

## 0. 结论摘要

1. **容器**：352 项 = 22 种语言 × 16（15 张表 + person_names 占位）。与 b12 解过的 client_db 同为 `tad.` v3569 外壳 + 内嵌 FMF 资源（Zstd）。
2. **语言模型**：文件名中的语言 id 就是 `client_db.dat` table_8（语言实体表，126 行）的**行序号**；1000000–1000004 是扩展变体（序号 122–126）。b12 报告里 "7=English、8=Finnish" 的标注是错的：**7=Dutch、8=English**（本报告已用内容证据修正）。
3. **行语法**：15 张表中 14 张精确解码（22 语言 × 14 表 = **308/308 文件整文件精确游走**）；table 18 用 LIS 回退。基础层 `lang_db_2400.dat` 同一语法，中文俱乐部表 83,837 行全部走通。
4. **中文**：本机就带中文。基础层（2400）有**全量**简体/繁体翻译（简体：俱乐部 77,390/83,837 行、球场 45,866/48,158、国家 251/251、城市 54,850/56,018、比赛 6,981/7,035）；更新层（2430）携带简体增量（914 个 CJK 俱乐部名、313 球场、250 国家、143 城市、50 奖项、42 媒体名）。字符串全部 UTF-8，无 GBK/遗留编码。
5. **覆盖评估**：官方 Stadium improvements 的 1,217 座球场（本地从 1,227 个 duni 解出）中 **1,215 座在全部主要语言（含简繁中文、日韩）有名**，对比 b12 只用更新层时的 114 → **×10.7**；b14 的 16 家俱乐部全部获得中文名；两支中国球队比赛（131126 中甲、130932 中乙）经基础层命名。
6. **关键发现（键空间）**：语言层的行键 = **俱乐部 duni**（与 client table_3 行内重复 u32 对一致）；b14 CLUB_STADIUM.md 报告的 club DBID 值系统性错位（见 §7），但其 club→stadium 结果仍正确。
7. **双层机制**：`lang_db_2400.dat`（db2400，全量表）+ `lang_update_db.dat`（db2430，只含新增/变更行，逐语言行数不同）。游戏按 base∪update（update 优先）合并读取；工具 `modding_db_names.py` 已实现同一合并。

## 1. 容器结构

| 文件 | 大小 | sha256（前 8） | 本地副本 |
|---|---:|---|---|
| `db/2430/lang_update_db.dat` | 2,317,274 B | `fa2608e8…` | `extracted/db2430/lang_update_db.dat` |
| `db/2430/client_db.dat` | 13,113,803 B | `5ce7cd91…` | `extracted/db2430/client_db.dat` |
| `db/2400/2400_fm/lang_db.dat` | 71,427,348 B | 与 `input/lang_db_2400.dat` 一致 | 同左 |

- 外壳：`tad.` 魔数 + 版本 3569，目录/条目为内嵌 FMF（Zstd 压缩），解析基座沿用 b12 的 `scripts/modding_read_dbdat.py`（`_read_archive` / `_decompress_entry`）。
- 条目命名：`lang_update_db/{lang_id}_{table_id}.dat` 与 `lang_update_db/{lang_id}_person_names.dat`。
- **352 = 22 × 16**：22 种语言 ×（15 张表 `{0,2,3,5,6,7,9,18,19,21,23,25,35,47,56}` + 1 个 person_names）。person_names 在更新层全部是 12 字节空载荷（count=0），真实人名翻译不在本文件。

## 2. 语言模型

### 2.1 id 体系

`client_db.dat` 的 table_8 是语言实体表，126 行。**行序号（1-based）即语言 id**：

| id | 语言 | id | 语言 |
|---:|---|---:|---|
| 1–5 | Albanian, Arabic, Bulgarian, Croatian, Czech 区间… | 21 | Russian |
| 6 | Czech | 22 | Norwegian |
| 7 | **Dutch** | 24 | Spanish |
| 8 | **English** | 25 | Turkish |
| 9 | Finnish | 30 | Swedish |
| 10 | French | 32 | Danish |
| 11 | German | 122 | Latin American（文件 id 1000000） |
| 12 | Greek | 123 | Brazilian（1000001） |
| 15 | Italian | 124 | **Chinese Simplified**（1000002） |
| 16 | Japanese | 125 | **Chinese Traditional**（1000003） |
| 17 | Korean | 126 | Usa（1000004） |
| 18 | Polish | 19 | Portuguese |

序号 122–126 在语言文件里改用 `1000000 + (序号 − 122)` 表示（VARIANT_BASE=1000000）。完整 126 名单见 `scripts/lang_update_layer.py` 的 `LANGUAGE_ORDINALS`。

### 2.2 交叉证据（≥2 条）

1. **table_8 顺序**：126 个语言英文名按序号顺序逐个出现在 table_8 载荷中（125/126 精确；唯一例外 `Guaraní` 的 í 字节非 UTF-8 编码，属该表自身的编码瑕疵，见 §9）。
2. **每语言内容**（同一实体在不同语言文件里的名字）：
   - 7=Dutch：'Talent van het Jaar'；10=French；12=Greek；16=Japanese（假名）；17=Korean（谚文）；21=Russian（西里尔）；25=Turkish；30=Swedish；32=Danish。
   - 19=Portuguese 'Singapura' vs 1000001=Brazilian 'Cingapura'。
   - 1000002=Simplified（简体）、1000003=Traditional（繁体）——两文件同实体的中文用字不同。
3. **基础层同构**：`lang_db_2400.dat` 也是 352 项、同样的 22 语言 id 与命名规则，且中文内容集中于 1000002/1000003 两个文件。

### 2.3 本机安装的语言

更新层的 22 种语言即游戏本机带的语言包：
Czech(6) Dutch(7) English(8) French(10) German(11) Greek(12) Italian(15) Japanese(16) Korean(17) Polish(18) Portuguese(19) Russian(21) Norwegian(22) Spanish(24) Turkish(25) Swedish(30) Danish(32) Latin American(1000000) Brazilian(1000001) **Chinese Simplified(1000002)** **Chinese Traditional(1000003)** Usa(1000004)。

### 2.4 对 b12 报告的修正

b12 `DBDAT_FORMAT.md` 将 7 标为 English、8 标为 Finnish——按上述证据 **7=Dutch、8=English**（8 的内容是英文；Finnish 是 9）。b12 的解析机制不受影响，仅语言标签错。

## 3. 行语法

行语法家族（`scripts/lang_update_layer.py::TABLE_GRAMMARS`）：

- 字符串 = `[u32 len][utf-8]`；`0xFFFFFFFF` = NULL（4 字节）。
- 行 = `[u32 dbid][槽位序列]`；变长尾部 = `[u8 n][n × ([u32 len][utf-8][3 flag bytes])]`（变体/别名串）。
- table 3 额外有行尾 `[s][s]` 两个字符串槽。

各表槽位（s=字符串槽，CNT@k=变体计数在槽 k 后）：

| table | 槽位 | CN 内容证据 → 语义 |
|---:|---|---|
| 0 | s,s,str,s,CNT@4 | 50 行 CJK：'意大利足球乙级联赛月度最佳球员' → **奖项名** |
| 2 | str,s,CNT@2 | 143 行 CJK：城市名 → **城市** |
| 3 | str,s,str,s,str,str,str,s,str,CNT@9 + 尾[s,s] | 914 行 CJK：俱乐部名（字段 Cnam）→ **俱乐部** |
| 5 | str,s,str,str,str,s,str,s,CNT@8 | 无 CJK（语法级） |
| 6 | str,s,str,s,CNT@4 | 1 行 CJK：'足底筋膜炎' → **伤病/医疗名** |
| 7 | str,s（无 count） | 42 行 CJK：'梦幻足球'、'90分钟' → **足球媒体** |
| 9 | str,s,str,s,str,str,CNT@6 | 250 行 CJK：国家名 → **国家** |
| 18 | （无语法，LIS 回退） | 72 行 CJK：城镇名（'奥卢'=Oulu）→ 第二城市名集合 |
| 19 | str,CNT@1 | 无 CJK |
| 21 | str,str,s,s,CNT@4 | 球场名（Snam）→ **球场** |
| 23 | str,s,str,s,str,s,CNT@6 | 无 CJK |
| 25 | str,s,str,s,str,CNT@5 | 比赛名（cnam）→ **比赛** |
| 35 | s,s,CNT@2 | 无 CJK |
| 47 | str,s,str,s,CNT@4 | 无 CJK |
| 56 | （空） | 0 行 |

验证：`grammar_walk` 对更新层 **308/308 文件**整文件精确走通（每个文件行数 = 声明 count、字节边界严丝合缝）；基础层 1000002 的 t3/t21/t9/t25/t2 同样精确（83,837 / 48,158 / 251 / 7,035 / 56,018 行）。

## 4. 双层机制（base + update）

- **基础层** `db/2400/2400_fm/lang_db.dat`：同为 352 项容器，每语言**全量**表。
- **更新层** `db/2430/lang_update_db.dat`：每语言**只带新增/变更行**，行数逐语言不同。例如 table_3：English 3,462 行、简中 1,530 行（914 行含 CJK）；table_9：English 1 行、简中 250 行（全 CJK）；table_0：简中 50 行（全 CJK 奖项名）。
- 游戏读取时按 **base ∪ update（update 覆盖 base）** 合并。`modding_db_names.py` 的 `entity_name_map()` 实现了同一合并（update 命中优先，否则回退 base），这是覆盖评估的基础。
- 22 语言更新层各行表**声明 count 之和**（样本 JSON 的 `entity_record_totals_update_layer`）：t3=72,264、t21=11,840、t25=876 等——注意它是 22 语言合计，不是单语言行数。

### 4.1 中文（简体 1000002）双层内容

| 表 | 基础层（2400） | 更新层（2430） |
|---|---|---|
| 俱乐部 t3 | 83,837 行（77,390 行 CJK 名） | 1,530 行（914 CJK） |
| 球场 t21 | 48,158 行（45,866 CJK） | 592 行（313 CJK） |
| 国家 t9 | 251 行（251 CJK） | 250 行（250 CJK） |
| 城市 t2 | 56,018 行（54,850 CJK） | 419 行（143 CJK） |
| 比赛 t25 | 7,035 行（6,981 CJK） | 18 行 |
| 奖项 t0 | — | 50 行（50 CJK） |
| 媒体 t7 | — | 42 行（42 CJK） |

繁体（1000003）同样存在：更新层变更集更小，但经基础层合并后覆盖与简体相当（见 §5）。所有字符串均为 UTF-8；**未发现 GBK/遗留编码**（GBK 扫描无命中，中文名全部来自 UTF-8 CJK）。

### 4.2 缺语言包的影响边界

即便某语言包不存在，`lang_db_2400.dat` 基础层仍随库提供全量翻译；真正缺的是对应语言的"更新层增量"（该语言看不到 2430 的新增/改名，如简中 914 个俱乐部新名）。官方库的中文 club 名主要来自基础层 + 更新层合并，而非 client_db 本体。

## 5. 覆盖评估（如实数字）

对象：官方 Stadium improvements（editor fmf 解码 `dbc_decoded/Stadium improvements.json`，16,024 条记录，任务书口径 1,227 个唯一 duni；本地解析出 1,217 个唯一 table_21 球场 dbid + 10 个唯一 table_3 俱乐部 duni）。

| 指标 | b12（仅更新层） | 本轮（base∪update） |
|---|---:|---:|
| improvement 球场任一语言有名 | 114 | **1,215 / 1,217** |
| improvement 球场简中有名 | 0 | **1,215 / 1,217** |

- 逐语言命中：22 种语言中 21 种 = 1,215；**Brazilian(1000001) 仅 2**（该语言包自身稀疏，如实报告，不硬凑）。
- 繁体(1000003) 同样 1,215。
- 未命中的 2 座：更新层+基础层都无该 duni 的名称行（维持 1,215 不虚报）。
- 比赛：131126 → **中国足球甲级联赛**、130932 → **中国足球乙级联赛**（基础层，22 语言全有译名；client table_25 行 250/245）。
- b14 的 16 家俱乐部：全部经合并层拿到中文名（利物浦、曼彻斯特城足球俱乐部、阿森纳、切尔西、拜仁慕尼黑足球俱乐部、巴塞罗那、巴黎圣日耳曼足球俱乐部、尤文图斯足球俱乐部、多特蒙德普足球俱乐部、阿贾克斯足球俱乐部、国际米兰足球俱乐部、AC米兰足球俱乐部、托特纳姆热刺、纽卡斯尔联，以及两家大连俱乐部的正确归属，见 §7）。
- 球场地标 10 例（坐标+名称双验证）：维拉公园、王子公园、罗连安特路、诺坎普、莫祖锡、凯普、珀斯矩形、中央海岸、莱肯达尔、拉伊科·米蒂奇（详见样本 JSON `manual_landmark_checks`）。

## 6. 球场键空间

- 语言层球场表（t21）的行键 == 球场 dbid == client table_21 的 duni。10 处地标（含新 ID 28,096,287 托特纳姆热刺体育场、1,300,450 莱肯达尔等）逐一验证。
- 同一数值在球场/俱乐部两个实体空间各自独立（676 既是利物浦也是安菲尔德），`--lookup` 会并列返回两个实体。

## 7. 俱乐部键空间与 b14 DBID 勘误（重要发现）

**语言层俱乐部表（t3）的行键 = 俱乐部 duni。** 证据链：

1. **编辑器档案独立佐证**：Stadium improvements 档案里的 10 个 type-3 俱乐部 duni，经语言层键直查全部命中语义合理的"球场改建"俱乐部：

   | duni | 俱乐部（语言层中文名） |
   |---:|---|
   | 600 | 伯恩茅斯 |
   | 677 | 卢顿镇足球俱乐部 |
   | 846 | 南特足球俱乐部 |
   | 1536 | 阿伯丁足球俱乐部 |
   | 1685 | 潘普洛纳竞技 |
   | 106749 | 斯拉文贝鲁波 |
   | 109206 | 格林森林流浪者足球俱乐部（Eco Park 新球场案例） |
   | 138156 | 彻诺摩尔 |
   | 7840141 | 尼亚尔兹维古青年 |
   | 39048732 | 维斯特里体育俱乐部 |

2. **client table_3 字节级验证**：club 行内把自身 duni 存为**名称附近相邻重复 u32 对**。逐字节验证：'Dalian Yifang'→23,325,085、'Dalian Chaoyue'→23,245,672、'Tianjin Quanjian'→23,325,084、'Dalian Professional'→34,053,971，全部与语言层键一致。
3. **地标/成员验证**：dense 前缀行（`[langid][NULL][langid][langid]`，约 55,711 行）行尾重复对 == 语言层键；`client_table3_names` 的 10 处地标全中。

### 7.1 b14 CLUB_STADIUM.md 的 DBID 勘误

b14 报告的 club DBID 值系统性错位（锚点扫描踩线/跨行），但**其 club→stadium 结果本身仍正确**（链路最终仍走到正确 team 行）：

| b14 值 | 实际指向（语言层） | 正确归属 |
|---:|---|---|
| 172,800（Liverpool） | 675<<8 跨界误读形态 | Liverpool 真键 **676**（shift 回退可解：172800→利物浦） |
| 23,325,084（Dalian Yifang） | **天津权健**（相邻 id 的记录） | 大连一方真键 **23,325,085** |
| 23,245,626（Dalian Chaoyue） | **伟利体育会**（澳门 club） | 大连超越真键 **23,245,672** |
| 173,568 / 153,856 / … | 同类 (duni)<<8 跨界形态 | 曼城 679、阿森纳 602、切尔西 630、拜仁 915、巴塞罗那 1708、巴黎 868、尤文 1139、多特 907、阿贾克斯 992、国米 1135、AC米兰 1099、热刺 728、纽卡 688 |

注：语言层同时存在 'Dalian Yifang'(23,325,085) 与 'Dalian Professional'(34,053,971) 两个俱乐部实体（db 库保留历史实体），不是同一键的改名。存档侧（`1 1-大连人.fm`）的大连人 34,047,551 与 2430 客户端键 34,053,971 不等，差值 6,420，属存档工件侧未解边界（b14 的存档侧锚点法已被证明有踩线问题；本任务不追存档）。

## 8. 工具与可重跑

```powershell
# 结构/语言模型/语法/基础层验证（只读）
python -I scripts\lang_layer_probe.py --db-dir extracted\db2430 --base-lang-db input\lang_db_2400.dat

# 语言清单
python -I scripts\modding_db_names.py --languages --db-dir extracted\db2430 --base-lang-db input\lang_db_2400.dat

# 单键查询（自动并列 club/stadium 两实体；--lang 指定语言，默认中文优先）
python -I scripts\modding_db_names.py --lookup 676 --db-dir extracted\db2430 --base-lang-db input\lang_db_2400.dat
python -I scripts\modding_db_names.py --lookup 28096287 --lang 1000002 --db-dir extracted\db2430 --base-lang-db input\lang_db_2400.dat

# 关键词搜索（多语言）
python -I scripts\modding_db_names.py --search 利物浦 --db-dir extracted\db2430 --base-lang-db input\lang_db_2400.dat

# 重新生成样本（name_samples 1,215 条 + multi_language 128 条，≥300 达标）
python -I scripts\modding_db_names.py --samples --db-dir extracted\db2430 --base-lang-db input\lang_db_2400.dat --output reports\dbdat_decode\name_index_samples.json
```

实测输出（本任务内）：probe 容器 352 项、308/308、table_8 序号检查、基础层 5 表走通；`--lookup 676`→安菲尔德球场+利物浦；`--lookup 28096287 --lang 1000002`→托特纳姆热刺体育场；`--search 利物浦`→26 命中（首条 club 676）；`--lookup 172800`→利物浦（shift 回退）；`--samples` 已重生成 `reports/dbdat_decode/name_index_samples.json`（name_sample_count=1215、multi_language_sample_count=128、b14 16 对、type-3 俱乐部 10 对、地标 10、语言清单 22）。

## 9. 已知边界

1. table_18 无行语法（LIS 回退），行内 NULL 字符串与可变尾部只解出部分结构。
2. table_8 的 'Guaraní'（序号 81）的 í 字节非 UTF-8（该表自身编码瑕疵）；语言序号模型其余 125/126 全对。
3. client table_3 的稀疏区（~28.5k 俱乐部共享一个语言前缀）未被 `client_table3_names` 消歧，映射为部分结果（55,711/84,259）；已验证样本内 100% 正确，不再扩大声明。
4. 存档侧大连人 id 差值（§7.1 注）未解，留待存档解码任务。
5. Brazilian(1000001) 语言包稀疏，coverage 仅 2——如实报告。
6. 未动他人交付物：`fmedit.py`、`modding_varlen_rows.py`、`merge_state.py`、`modding_read_summary.py`、`editor_preset_to_spec.py`；本轮只改/新增 `lang_update_layer.py`、`lang_layer_probe.py`、`modding_db_names.py`。
