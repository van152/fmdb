# `people_db.dat` 人物主表深度解码（b22 重启）

状态：**只读静态分析**。没有启动 FM24/编辑器；没有写游戏目录或用户 Documents；没有读取/处理 `tadc` / `pl_hist_dt`。本次唯一代码修改为 `scripts/modding_varlen_rows.py`，临时解压和索引都在工作区 `tmp_people/`。

> 路径迁移（2026-11-15 仓库整理）：`tmp_people/` 已拆分——大文件（解压缓存与行索引 jsonl）移至 `archive/people_bins/`，小型机读证据移至 `reports/dbdat_decode/people_evidence/`；下文所有 `tmp_people/...` 路径按上述新位置读。脚本解压缓存路径已同步改到 `archive/people_bins/people_db_streamed_b22.bin`。

## 结论与边界

- 已从安装库直接 Zstd 流式解压 `people_db.dat`：压缩 **67,502,767 B**，解压后 **400,443,970 B**。输出 SHA-256 `21686a985e32ebaf8ced73478058e69720be061d08be499be89e4d441f0f2fbd`，无 content size 的 frame 以 1 MiB 块流式读取。
- 主体中可稳定提取 **186,084 个「姓名长度前缀 + 合法打包出生日期」候选片段**，185,575 个不同姓名；连续候选片段覆盖解压 payload offset `74,870..400,443,970`，候选切片总长 400,369,100 B。**这是候选记录切分，不是已证明的全库 person row serializer**：有嵌套姓名/非人物名字段，长度最大 1,405,886 B，且不能把候选数当作唯一人物数。
- 文件开头另有 **1,193 条**较短的名字/身份候选记录（`offset 6..55,750`）；此格式与后续 DOB 锚点流不同。两段之间有 **19,120 B** 未解字节。开头段的 1,193 个尾部 repeated-u32 候选互异，值域 2,002,040,996–2,002,042,188，但其 DUNI 语义仍未由加载器/跨表闭环证明。
- DOB 的原始 4B 直接证据支持 `packed = (year << 16) | day_of_year`（低 16 位为 1-based day-of-year；按闰年还原日历日期）。例：Messi `0x07c300af` → 1987 / 175 → 1987-06-24。此字节证据不支持旧任务书中另一种 `2*year`/time-code 表述；本报告按实际安装字节正式化 b22 已核实的日期。
- 目前可高置信确认姓名、姓名长度和出生日期；一个国家引用字节为中置信候选。**身高、体重、CA/PA、精确位置槽位、现效力俱乐部、合同均未恢复为可靠字段**；不把邻接整数冒充这些属性。报告最后列出明确未解项。
- `table_extra_9` 已定位到长度前缀 UTF-8 字符串与 u32 行序号；`table_extra_24` 精确为 82 B/行，且每行首 u32 等于 0-based ordinal。两者语义范围见下文。
- `basic_people_db.dat` 解压后为 54,060,043 B，前缀 `5b 0a 0a 00`，结构与本报告的 `people_db.dat` 不同；未将其混入以上切分/行数，仍待单独解码。

## 1. 解压与清点

| 项 | 结果 |
|---|---|
| 安装输入 | `Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm/people_db.dat` |
| 外层 | `03 01 'tad.' f1 0d`，offset 8 直接 Zstandard frame |
| 压缩大小 | 67,502,767 B |
| 工作区解压 | `tmp_people/people_db_streamed_b22.bin`，400,443,970 B |
| SHA-256 | `21686a985e32ebaf8ced73478058e69720be061d08be499be89e4d441f0f2fbd` |
| 行索引 | `tmp_people/people_candidate_rows.jsonl`，186,084 行，90,761,528 B；含候选 start/end、姓名、DOB、首尾原始字节，不含整行 hex |

### 两种连续边界候选

**开头紧凑名字/身份段（1,193 条）**：从 `offset 6` 开始，按以下可复读结构连续切分，直到 `offset 55,750`：

```text
u32 identity-key candidate
u32 type candidate (=5 in all 1,193 rows)
u8 unknown
u32 UTF-8 name byte length
name bytes
8 bytes
u32 repeated identity-key
u64 repeated-u32 candidate (hi32 == lo32)
```

前 20 条即 b22 样本（`Zarko Serafimovski`、`Ronny Pattinasarani` 等）。1,193/1,193 尾部重复-u32 唯一，范围 2,002,040,996–2,002,042,188。其 key/type/DUNI 的业务语义保留为候选。

**主姓名/DOB 候选段（186,084 条）**：每个候选起点满足：

```text
FF FF FF FF 00 | u32 byte_length | UTF-8 full name | u32 packed DOB
```

第一条姓名长度前缀在 `offset 74,875`，姓名起点 `74,879`；每个切片 end 取下一条通过姓名 UTF-8、年份范围、day-of-year（含闰年）检查的同形锚点。最后一条延伸到 payload EOF。该方法完全复现 b22 的三个姓名/DOB 锚点及 Messi `start=38,607,338`。此数值在字节证据中是 **文件 offset**（该处以 `FFFFFFFF 00 [len=31]` 开始），未发现其作为 u32 身份值出现在解压 payload 中，因此不把 38,607,338 记为已验证的 DUNI。

边界质量限定：候选切片内可能含嵌套姓名/子结构。例：`Cristiano Ronaldo dos Santos Aveiro` 的 `[u32 len=35][name][DOB]` 位于 offset `131,427,482..131,427,525`，其 DOB 正确；但它落在 `Silvino de Almeida Louro` 的候选切片内，没有自己的同形顶层 marker。故 186,084 是**可复现的 anchor/slice 清点**，不是 186,084 个去重 person 的证明。

### 与 b27 person ID 模型交叉

`ID_ALLOCATION_V2.md` 的 544 个 type-1 person ADDR DUNI（2,002,250,001–2,002,250,544）是用户 DBC 新分配段，不是安装库人物行数。开头紧凑段的 1,193 个重复-u32 候选区间与该段不重叠；主 DOB 候选流尚未定位完整 DUNI 字段/高水位，无法用行数或尾部普通 u32 替代 person 的完整 `seen_duni`。b27 的 person provider 继续 fail-closed 是正确结论。`summary.dat` 的 54,086 条摘要记录也不是 `people_db.dat` 行数，不能直接等同。

## 2. 字段槽位与置信度

下表区分**已识别字节字段**与**业务语义候选**；“字段数”不等于 10 个业务属性已解。

| 锚点/相对位置 | 观察/解释 | 置信度 |
|---|---|---|
| row `+0..+3` | `FF FF FF FF`，紧邻姓名字符串的 sentinel | 高：结构 |
| row `+4` | `00`，姓名长度前的固定字节 | 高：结构，语义未知 |
| row `+5..+8` | u32 UTF-8 byte length；如 Messi=31 | 高 |
| row `+9..+9+len-1` | UTF-8 full name，含重音字符；如 `Lionel Andrés Messi Cuccittini` | 高 |
| name end `+0..+3` | DOB u32；高 16 位 year、低 16 位 1-based doy | 高；22 位真实球员生日逐字节吻合 |
| DOB `+4..+5` | u16 候选；Messi/Busquets/De Gea 均为 279，Mbappé=777 | 低：未映射 schema |
| DOB `+6..+7` | u16 候选；Messi=1547、Busquets=1551、De Gea=1545 | 低 |
| DOB `+8` | nation byte 前的 u8 子槽；Messi=3、Busquets=6、De Gea=0 | 低 |
| DOB `+9` | **Nation/primary nationality ID 候选**；Messi=187、Busquets/De Gea=170、Mbappé=143、Bellingham=139 | 中：与 Club `Cnti` 候选 England=139、Argentina=187、Spain=170、France=143 交叉相符；尚非 loader 级证明 |
| DOB `+10..+11` | u16 槽候选；样例多为 0 | 低 |
| DOB `+12..+15` | u32 引用/标量候选；Messi=1649、Busquets/De Gea=796 | 低；尚不能标为出生城市、俱乐部或其它外键 |
| DOB `+16..+23` | 在上表 22 个事实样本中各见 8 个 0–20 范围 u8；例如 Messi `11 12 11 13 11 0f 0e 05`，Busquets `0c 0e 12 0f 0f 07 0c 06` | 低：rating/position-like vector 候选；只核对了样本范围，字段顺序/全表范围/语义未解，不能命名为特定位置或 CA/PA |
| candidate row end | 下一个姓名+DOB 锚点；切片大小可变 | 中：边界候选；不是通用 serializer 证明 |

schema 对照来源为 `resources_modding/comp editor/comp editor/format/database/person.xml`：其中 `Pdob`=Date Of Birth、`Phes`=Height（int，max 210）、`Pwes`=Weight（int，max 120）、`Pcbi`=City Of Birth、`Pnbi`=Nation Of Birth、`Pnti`=Nation、`Pcti`/`Ptaj`=Club/team ref、`Pcsd`=Date Last Contract Signed、`Pcex`=Contract Expires、`PFTa`=First Full-Time Contract Age、`PcHC`=Has Contract、`Pces`=Contract Type、`Pirc`=On Rolling Contract。该 schema 是字段目录，不证明这些 ID 在候选字节中的具体偏移。

这已给出 ≥10 个**可观察槽位/派生字段**及证据，但不满足“≥10 个已命名业务属性”。目前没有可靠的 `Phes` 身高、`Pwes` 体重、CA、PA、独立位置、`Pcti` 俱乐部 DBID、`Pcex` 合同到期字段映射。对 21 名有身高/体重公开事实的样本，在 DOB 后前 512 B 搜索 u8/u16/u32 精确值，没有跨样本稳定相对偏移；这是未定位的阴性证据，不证明属性不存在于后续子结构。

## 3. ≥20 名事实球员核对

下表 `DOB` 由原始 DOB u32 还原；全名来自同一 UTF-8 长度前缀。每行列出完整候选切片边界和 DOB 后 `+9` nation-byte 候选。预期生日按常见公开球员资料核对，raw 日期均匹配。切片长度只描述候选边界，不表示完整语义已解。

| 人物全名（DB 原文） | 候选 offset start..end（B） | 解出的生日 / doy | nation-byte 候选 | DOB u32 |
|---|---:|---|---:|---:|
| Lionel Andrés Messi Cuccittini | 38,607,338..38,608,725（1,387） | 1987-06-24 / 175 | 187 | `0x07c300af` |
| Kylian Mbappé Lottin | 236,690,727..236,693,402（2,675） | 1998-12-20 / 354 | 143 | `0x07ce0162` |
| Sergio Busquets Burgos | 96,247,666..96,248,770（1,104） | 1988-07-16 / 198 | 170 | `0x07c400c6` |
| David de Gea Quintana | 96,346,814..96,351,939（5,125） | 1990-11-07 / 311 | 170 | `0x07c60137` |
| Erling Braut Haaland | 154,019,007..154,025,703（6,696） | 2000-07-21 / 203 | 160 | `0x07d000cb` |
| Jude Victor William Bellingham | 252,737,389..252,739,450（2,061） | 2003-06-29 / 180 | 139 | `0x07d300b4` |
| Thibaut Nicolas Marc Courtois | 289,860,904..289,862,625（1,721） | 1992-05-11 / 132 | 131 | `0x07c80084` |
| Manuel Peter Neuer | 226,043,378..226,049,432（6,054） | 1986-03-27 / 86 | 145 | `0x07c20056` |
| Joshua Walter Kimmich | 226,035,017..226,036,819（1,802） | 1995-02-08 / 39 | 145 | `0x07cb0027` |
| Mohamed Salah Ghaly | 393,629,474..393,630,611（1,137） | 1992-06-15 / 167 | 11 | `0x07c800a7` |
| Andrés Iniesta Luján | 96,724,850..96,725,736（886） | 1984-05-11 / 132 | 170 | `0x07c00084` |
| Gerard Piqué Bernabéu | 96,416,950..96,417,850（900） | 1987-02-02 / 33 | 170 | `0x07c30021` |
| Sergio Ramos García | 96,254,918..96,255,682（764） | 1986-03-30 / 89 | 170 | `0x07c20059` |
| Zinedine Yazid Zidane | 236,703,648..236,706,099（2,451） | 1972-06-23 / 175 | 143 | `0x07b400af` |
| David Robert Joseph Beckham | 254,347,507..254,348,259（752） | 1975-05-02 / 122 | 139 | `0x07b7007a` |
| Paolo Cesare Maldini | 177,136,911..177,151,751（14,840） | 1968-06-26 / 178 | 150 | `0x07b000b2` |
| Wayne Mark Rooney | 253,648,684..253,650,493（1,809） | 1985-10-24 / 297 | 139 | `0x07c10129` |
| Frank James Lampard Jr. | 253,104,396..253,107,969（3,573） | 1978-06-20 / 171 | 139 | `0x07ba00ab` |
| Steven George Gerrard | 252,911,688..252,914,047（2,359） | 1980-05-30 / 151 | 139 | `0x07bc0097` |
| Carles Puyol Saforcada | 107,954,458..107,955,026（568） | 1978-04-13 / 103 | 170 | `0x07ba0067` |
| Sir Alexander Chapman Ferguson | 111,675,260..111,676,234（974） | 1941-12-31 / 365 | 167 | `0x0795016d` |
| Didier Yves Drogba Tébily | 389,256,655..389,260,881（4,226） | 1978-03-11 / 70 | 19 | `0x07ba0046` |

额外核对：`Cristiano Ronaldo dos Santos Aveiro` 的直接长度前缀在 `131,427,482`（len=35），姓名起点 `131,427,486`，紧随 DOB `0x07c10024` → 1985-02-05 / 36，符合事实；但它位于另一候选切片内部，不列入上表 22 个顶层 DOB 锚点，正是“candidate slice ≠ 完整 person row”的例证。

## 4. `table_extra_9`：长度前缀、序号与归属

client/server `table_9` 和 `table_extra_9` 头部 count 均为 251。client extra 中扫描到 199 条互异的候选序号字符串；序号范围 0–248，另 52 个行序号没有本次识别到的昵称字符串。每个样本的字节形状为：

```text
u32 row_index | u32 UTF-8 byte_length | UTF-8 nickname
```

例：payload offset 12=`00 00 00 00`（index 0），offset 16=`0b 00 00 00`（len 11），offset 20=`Les Fennecs`；index 1 的长度前缀位于 offset 266，值 15，字符串 `Palancas Negras`。另有 `Les Écureuils`、`The Zebras`、`The Pharaohs`、`The Black Stars` 等国家队昵称。server extra 的嵌套姓名池会造成额外的 heuristic string hits；以 client 找到的 199 个 `(row_index,length,text)` 对照 server 后，**199/199 同长度、同文本、同 row_index 命中**。

归属判断：高置信为与 nation/table_9 行序号相关的变长附加记录；字符串内容表明至少包含国家队昵称，server 侧还扫描到候选姓名池字符串（如 `Akwá`、`Babanco`、`Foxi`、`Nando Có`；具体行归属仍未证实）。但除已验证的字符串头部外，完整的每行长度/count/姓名池 serializer 未恢复；不把扫描到的所有可打印串都等同于第一层 nickname 字段。

## 5. `table_extra_24`：82 B/行与内容观察

server `table_extra_24` 解压 6,929,586 B，count 84,507，与 server `table_24` count 相同，且：

```text
6,929,586 = 12 + 82 × 84,507
```

所有记录的 `record+0:u32` 依序严格等于 `0..84,506`，因此可确定这是按 `table_24` row ordinal 排列的 **82 B/行 Team 扩展区**，不是简单偏移表。

逐行比较得到 61 种“剔除前 4B serial 后”的 body variant。仅 body byte offset `+10`、`+11`、`+81` 变化：`+10/+11` 各取 0..7，`+81` 取 `{0,2,99}`；`+4..+7` 是 `FFFFFFFF`，`+12..+15` 恒为 `10000`。除 4B serial 和这 3 个变动 byte 外，其余 75B 为共同模板。由此可以把内容归为 **Team row-keyed、以默认模板为主的补充状态/枚举数据**；没有足够证据将这两个小枚举或末尾 byte 命名为 `Trep`、division、contract 等 schema 属性。字段语义仍标低置信/未解。

## 6. `table_extra_3` 与 Club 残余字段

`table_extra_3` 的 count 与 `table_3` 同为 84,259；client 13,053,908 B，server 35,009,248 B。去掉 12B 头后都不整除 count，不满足简单固定 stride。开头字节也不构成通用 offset/length 索引；其 per-row serializer 和 Club 字段映射未解。

针对 `Liverpool`、`Manchester City`、`Arsenal` 的 b17 候选 main-table slices（分别 payload offset `278,532..281,035`、`282,309..283,805`、`210,032..211,427`）：在各自 slice 内分别未找到 1892、1880、1886 的 little-endian u16/u32 成立年常量；也未找到与 Anfield/Etihad/Emirates 已知坐标相符的 float32 `(lat,lon)` 对。因此 `Cyfn` 成立年、`CLat/CLon` 坐标**不升级**；`ttcl/tbcl` 球衣颜色、`Crep` 声誉、Club.Csti 球场引用同样没有可验证槽位，继续 unresolved。阴性检索仅针对 b17 候选 main-row slices，不证明这些字段在 `table_extra_3` 或其他子结构中不存在。

**Club ID 勘误沿用 `LANG_LAYER.md`**：本脚本现有 `decode_club_fields()` 对 Liverpool/Man City/Arsenal 会输出 172,800 / 173,568 / 153,856 一类偏移候选；这些不是正确 Club DUNI。交叉验证键应使用 Liverpool=676、Manchester City=679、Arsenal=602。上一份已验证的 `Team.Tsti → table_21 rdui → stadium DUNI` 关系不能反推 Club.Csti，也不能把 stadium 坐标当作 Club.CLat/CLon。

## 7. 重跑与交付

```powershell
# 从安装 people_db.dat 重新流式解压、全量索引所有候选 DOB/name slices
python -I scripts/modding_varlen_rows.py --people `
  --decompressed-path tmp_people/people_db_streamed_b22.bin `
  --output tmp_people/people_candidate_rows.jsonl

# 每行增加 raw_row_hex（大文件；payload 原始完整字节已在 .bin 中保存）
python -I scripts/modding_varlen_rows.py --people `
  --people-path tmp_people/people_db_streamed_b22.bin `
  --output tmp_people/people_candidate_rows_raw.jsonl --raw-row-hex

# Extra 和 Club 候选
python -I scripts/modding_varlen_rows.py --extra
python -I scripts/modding_varlen_rows.py --club Liverpool
```

实现新增 `--people`（分块解压、candidate row 全量索引/JSONL dump，可选 raw hex）和 `--extra`（`extra_3/9/24` 结构摘要）。旧 `--people-sample`、`--inspect-extras` 接口仍保留。全量 raw 解压文件、90,761,528 B 的 candidate row index 和 extra 机读结果均只写在 `tmp_people/`。

**未达成/明确留项**：没有恢复身高/体重、CA/PA、准确 position 槽位、现效力球队 `Pcti`、合同 `Pcsd/Pcex`，也未恢复 Club 成立年/颜色/声誉/直接坐标。后续若要写字段级 decoder，应先找 loader/tag-to-schema 静态证据或独立的已知序列化样本；本轮不依据邻接整数猜写。
