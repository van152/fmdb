# 大表字段级调查（b47 检查点）

范围：`client_db.dat` / `server_db.dat` 的 table_2、3、21、25，以及 client/server `table_extra_3`。只读安装库；五个目标均已完成当前阶段的结构、字段与负路线调查。table_3 仍有 9 个辅助序号对应身份未分配，table_25 的 L2 字段少于验收阈值，均如实保留。

证据口径：L1=工作区解码器逐字节/全表结构复核；L2=与独立地名、城市/国家行及语言层名称或成立年锚点对齐；L3=exe 静态证据；本节无 L4，禁止将 L1 复读称为加载验证。

## table_2 — City

### 行模型与身份（L1）

- client 与 server payload 字节完全相同。56,293 行，`2,420,621 = 14 + 56,293×43 + 8`，stride=43。
- 对 header/footer 各 0..256 B 的所有精确算术组合穷举：存在 23 个纯尺寸可整除组合（都是 stride 43、header+footer=22）；再要求 `rdui` 与行序号全等、DUNI 重复-u32 且全唯一后，只有标准 `header=14/footer=8` 的解析成立。
- 56,293/56,293 行：`rdui@+30 == row_index`；`duni@+34` 是 repeated-u32 64-bit，56,293 个全唯一；`Clat/Clon` 候选偏移+1/+5 的 float32 值全部有限且落在合法经纬度范围。
- City 身份高置信，不是按 56,293 这个量级猜表：table_21 的 `Scti` 候选以 row rdui 引用 table_2，48,413/48,413 引用均合法；Liverpool / Manchester / Madrid / München 的 city DUNI、名称和坐标有独立交叉锚点（L2）。

### 槽位表与 schema 对齐

参照 `master.json` 的 `city.xml#city` 与 `LANG_LAYER.md` 的 table_2 英文名流。

| row offset | 字段 / 模型 | 依据与等级 |
|---:|---|---|
| +0 | 未命名 byte | 全量变化统计；不赋义 |
| +1..4 | `Clat` float32 | Liverpool、Madrid、München 等语言名与外部坐标核对；所有行范围有效（L2 锚点，L1 范围） |
| +5..8 | `Clon` float32 | 同上 |
| +9 | 未命名 byte | 不赋义 |
| +10 | `Cnti` Nation reference row ordinal 候选，u8 | Liverpool/Manchester=139、Madrid=170、München=145；分别吻合英文 nation table 的 England/Spain/Germany 记录序号（L2 候选） |
| +11..29 | 未命名原始字段区 | 已逐字节/4-byte lane 统计；未能稳定分配 `Clgi/Clri/Catt/Cinh/Calt/Cwea` 等 schema 字段 |
| +30..33 | `rdui` uint32 | 全行等于 row index（L1） |
| +34..41 | `duni` repeated-u32 uint64 | 全行重复且唯一（L1） |
| +42 | 未命名尾 byte | 已纳入 byte probes |

名称 `Cnam` 不在 row 中内联。基础英文语言表 table_2 有 56,018 条，而数据表有 56,293 行，差 275；不为无名称行猜值，不把语言表数量强行等同基础行数。

### L2 命名锚点

| 城市 | DUNI DBID | row/rdui | `Cnti` 候选 | table_2 坐标（约） |
|---|---:|---:|---:|---|
| Liverpool | 100,047 | 1,061 | 139 / England | 53.408371, -2.991573 |
| Manchester | 100,062 | 1,075 | 139 / England | 53.479324, -2.248485 |
| Madrid | 341 | 316 | 170 / Spain | 40.416775, -3.703790 |
| München | 592 | 540 | 145 / Germany | 48.135124, 11.581981 |

独立交叉：`lang_db_2400` 英文 table_2 对上述 DUNI 分别给出 Liverpool、Manchester、Madrid、München；同一 row index 也被 table_21 的 Anfield、Old Trafford、Bernabéu、Munich Stadium `Scti` 引用。用于命名的语言层本身与 client_db 字节同属安装库，计入 L2 的外部城市名称/地理位置核对，不称 L4。

### 负结果与证伪条件

- **固定步长成立**：精确全长公式 + 56,293/56,293 行序标记 + 全唯一身份共同支持；仅凭总长可除尽不够，故对 23 个 small-framing 算术组合继续用 identity lanes 过滤。
- **仍未解**：row+11..29 与零散 byte 槽位未完成 schema 逐字段对齐；`Cnti` 只以四个知名城市建立 L2 候选，未把 0..249 的每个值硬解为国家。
- 名称表与数据行数的 275 差值是未命名覆盖缺口，不是删掉 275 行或行边界错误的证据。

单表复跑：`py -V:3.12 -I scripts/b47_tables_big.py --table 2 --json`。聚合机读件用 `py -V:3.12 -I scripts/b47_tables_big.py --all --output reports/dbdat_decode/db_tables_big.json`。

## table_21 — Stadium

### 行模型与身份（L1）

- client：48,413 行，`14 + 48,413×38 + 8 = 1,839,716 B`，定长 stride=38。
- server：48,413 行，`14 + 48,413×181 + 8 = 8,762,775 B`，定长 stride=181。
- 48,413/48,413 行：client 与 server 的 `rdui` 均等于 row index；DUNI 均是重复-u32 64-bit 值。server row `[143:181]` 与对应的完整 client 38 B 逐字节相等；坐标字节也逐行相等。
- 名称不在这两种定长 row 内联：`Snam` 由 language table 21 提供（见 `LANG_LAYER.md`）。

### 全槽位表

偏移均相对 row 起点；unknown/opaque 是有意保留的负结论。Schema 对齐参照 `master.json` 的 `stadium.xml#stad`，可视列参照只读 junction `resources_modding/comp editor/comp editor/format/columns/stadium columns.xml`。

| 存储区 | row offset | 字段 / 模型 | 依据与等级 |
|---|---:|---|---|
| client | 0..2 | 未命名原始字节 | 全量 byte probes；未能对齐 schema |
| client | 3..6 | `Scti` 城市引用，uint32；实际值是 table_2 的 `rdui` | 48,413/48,413 引用值均落在 table_2 的 0..56,292；Anfield/Liverpool、Old Trafford/Manchester、Bernabéu/Madrid、慕尼黑体育场/München 四组引用、名称和地理位置吻合（L2） |
| client | 7..16 | 未命名原始字节 | 全量 byte probes；未能对齐 schema |
| client | 17..20 | `Slat` 候选，float32 纬度 | table_21 已有坐标样本与外部位置吻合（L2） |
| client | 21..24 | `Slon` 候选，float32 经度 | 同上（L2） |
| client | 25..28 | `rdui` uint32 | 48,413/48,413 = row index（L1） |
| client | 29..36 | `duni` repeated-u32 uint64 | 48,413/48,413 重复且唯一（L1） |
| client | 37 | 未命名尾字节 | 和 server row+180 相等；byte probe 已纳入 |
| server | 0..3 | `Scpy` 容量候选，uint32 | Santiago Bernabéu=81,044、Allianz/Munich stadium=75,000 精确命中；Old Trafford=74,031 对比任务书给出的 74,140 不符，保留反例（L2，候选） |
| server | 4..7 | `Sscy` seating-capacity 候选，uint32 | Bernabéu=81,044、Allianz=54,511 命中；Old Trafford 同样 74,031≠74,140，保留反例（L2，候选） |
| server | 8..15 | 未命名原始字节 | 有逐字节/按 4-byte lane 统计；无可靠 schema 归属 |
| server | 16..19 | `Sowi` stadium owner club reference，uint32；值匹配 table_3 候选序号 | Liverpool、Arsenal、Bayern、Chelsea、Newcastle、Dortmund 六组独立俱乐部/主场对照全部相等（L2 候选）；table_3 尚差 9 个边界，字段实际表示 row ordinal 的推断保留此限制 |
| server | 20..63 | 未命名原始字节 | 有逐字节/按 4-byte lane 统计；无可靠 schema 归属 |
| server | 64..127 | `Ssds[0..7]`：8 个 8-byte 槽 | `capc:i32@+0, sage:i16@+4, cond:i8@+6, flags:u8@+7`；旗标位由 `sub_1449A06C0` 静态证据定位（L3；详见 `DBDAT_FORMAT.md`），不是每槽另有磁盘 `indx` 字节 |
| server | 128..142 | 未命名 server-only 原始字节 | 全量槽位统计；未能对齐 schema |
| server | 143..145 | 与 client row+0..2 相同 | 未命名原始字节 |
| server | 146..149 | `Scti` 城市引用，uint32 city `rdui` | 与 client row+3..6 相同；见上述 L2 锚点 |
| server | 150..159 | 与 client row+7..16 相同 | 未命名原始字节 |
| server | 160..163 | `Slat` float32 | L2 地理位置交叉核对 |
| server | 164..167 | `Slon` float32 | L2 地理位置交叉核对 |
| server | 168..171 | `rdui` uint32 | 全表等于 row index（L1） |
| server | 172..179 | `duni` repeated-u32 uint64 | 全表重复且唯一（L1） |
| server | 180 | 与 client row+37 相同的未命名尾字节 | byte probe 已纳入 |

额外派生字段：Schema 将 `Snti` 标为只读 Nation 字段；通过 `Scti → table_2 city row → city.Cnti` 可间接确定。辅助 table_2 row+10 的国家行序候选在 Liverpool/Manchester=England、Madrid=Spain、München=Germany 三组独立地名上吻合语言层 nation 行序。它不是 table_21 的独立磁盘槽，不把派生值误报为直接序列化字段（L2 候选）。

### L2 锚点及反例

| 球场 | DBID / table_21 row | `Scpy` row+0 | `Sscy` row+4 | `Scti` → city | 坐标核对 |
|---|---:|---:|---:|---|---|
| Old Trafford | 680 / 71 | 74,031（与 74,140 不同） | 74,031（与 74,140 不同） | rdui 1075 → Manchester | 53.463058, -2.291336 |
| Santiago Bernabéu | 1,056 / 430 | 81,044 | 81,044 | rdui 316 → Madrid | 40.453022, -3.688375 |
| Munich Stadium（坐标对应 Allianz Arena） | 8,700,726 / 12,048 | 75,000 | 54,511 | rdui 540 → München | 48.218803, 11.624716 |
| Anfield | 676 / 67 | 50,109（容量候选） | 50,109（座位候选） | rdui 1061 → Liverpool | 53.430820, -2.960832 |

Bernabéu 与 Allianz 容量锚点 exact-match；Old Trafford 是真实负例而非被丢弃样本。坐标与城市引用四组均吻合独立地理事实。另有六组 owner：Liverpool/Anfield、Arsenal/Emirates、Bayern/Allianz、Chelsea/Stamford Bridge、Newcastle/St James' Park、Dortmund/Signal Iduna Park 的 table_21 row+16 均等于相应 table_3 候选序号。故容量族以外已有 `Scti`、`Snti`（经 City.Cnti 派生）、`Sowi` 三个 L2 字段候选；`Sowi` 仍受 table_3 缺 9 行边界的限制。L2 表示外部事实/语言行参照，不代表 L4 加载。

### 仍未解（明确边界）

- server `+8..15`、`+20..63`、`+128..145` 和 `+150..159`，以及 client `+0..2`、`+7..16`、尾字节 `+37` 仍未能逐字段映射；所有字节均已统计，但统计本身不等于 schema 归属。
- `Sscy` 的容量语义以两个精确座位数锚点支持，Old Trafford 数据不匹配；未将候选提升为无条件结论。
- 没有游戏/editor 加载验证（L4=0）。

复跑：

```powershell
py -V:3.12 -I scripts/b47_tables_big.py --table 21 --json
py -V:3.12 -I scripts/b47_tables_big.py --all --output reports/dbdat_decode/db_tables_big.json
py -V:3.12 -I scripts/b47_tables_big.py --selftest
```

聚合 JSON 由 `--all` 生成，含 table_2/3/21/25/extra_3 的结构、候选字段、负结果与源 payload SHA-256。

## table_25 — Competition

### 行模型与身份（L1）

- client payload：7,047 行，`894,991 = 14 + 7,047×127 + 8`，stride=127。
- `rdui@+114 == row_index`、`duni@+118` 重复-u32 且 7,047 个全唯一，均为 7,047/7,047（L1）。名称不在行内，来自英文 `lang_db_2400` table_25。语言表有 7,035 个名称，和数据表差 12，缺名不猜。
- 按语言名称和行身份交叉核查：UEFA Champions League 的 DBID 是 **1,301,394**（row 639），English Premier Division 是 **11**（row 7）；任务书中的 1,000,028 / 1,000,013 没有照抄。

### 可命名槽位（L2）及字段表

Schema 依据 `reports/editor_schema/master.json` `comp.xml#comp` 与只读 `resources_modding/.../format/columns/comp columns.xml`。偏移相对 127-byte client row。

| offset | 字段 / 候选 | 验证 |
|---:|---|---|
| 0..51 | 未分配 packed/raw 区 | 每 byte、每个起始偏移的 u16/u32 均已统计；数据形状密集、默认值重复，不按可见整数猜 schema |
| +52..55 | `ccti` Continent reference row ordinal | 10 个命名赛事锚点中的 6 个大洲：Africa=0、Asia=1、Europe=2、North America=3、Oceania=4、South America=5；国际 World Cup 为空 `0xffffffff`（L2） |
| +56..59 | `cnti` Nation reference row ordinal | England=139、China PR=55；UEFA/国际赛事用 `0xffffffff`（L2） |
| +60..63 | 未分配原始字节 | 全量统计 |
| +64..67 | `cpcm` Parent Competition reference row ordinal | Vanarama National League North/South（DBID 5,123,054/5,123,055）均指 row 352，即 parent Vanarama National League North/South（DBID 150,990）（L2） |
| +68..113 | 未分配 packed/raw 区 | 每 byte、每个起始偏移的 u16/u32 已探测；尚无独立 schema 锚点 |
| +114..117 | `rdui` uint32 | 全行等于 row index（L1） |
| +118..125 | `duni` repeated-u32 uint64 | 全行重复且唯一（L1） |
| +126 | 未分配尾 byte | 逐字节统计已纳入 |

### L2 命名锚点与负结果

- `ccti` 锚点：English Premier Division / FA Cup / UEFA Champions League→Europe 2；Chinese National First/Second Division→Asia 1；Copa América→South America 5；African/Oceania/N.A. Champions League→0/4/3。值域只有 0..5 与 null，六类均被命名赛事独立锚定。
- `cnti` 锚点：England 139、China PR 55；该行的 nation key 与 base English nation table 顺序一致；没有 nation 的赛事保留 null。
- `cpcm` 两个 sibling-row→同一个 parent-row=352，且 parent 的 DUNI 反查到 150,990；不是仅凭“附近有小整数”命名。
- schema 对齐当前只有 **3 个 L2 业务字段**（`ccti/cnti/cpcm`），低于 10；这是本表明确的负结果，不能写成“127 B 全字段已解”。`dbty` 的 `cdbt` enum（如 Domestic Top Division=0、Domestic Main Cup=2、Club Champions Cup=21）在 schema 中没有 `is_client_field` 标记，未获得唯一 raw slot；`levl` 虽标 client-side 且范围 1..20，但全偏移域扫描没有通过可区分的独立等级锚点。`PLgn`、`crep`、颜色、booleans、日期等也保留未命名。
- 负结果证据：全 row byte、u16、u32 槽位变动扫描；已知赛事 ID/name 锚点；引用域和 parent-child 检查。多个 packed 区存在值域看似像 1-byte enum/boolean 的反例，故只凭“落在 0..20”不升级为字段证据。
- server table_25 不套用 client stride；既有报告中仍只标 raw hit/边界未证，本节不声称解出 server 行。

复跑：

```powershell
py -V:3.12 -I scripts/b47_tables_big.py --table 25 --json
py -V:3.12 -I scripts/b47_tables_big.py --all --output reports/dbdat_decode/db_tables_big.json
```

L1 只说明结构/身份与脚本复读，不是游戏/editor 加载验收；全工作区 L4 仍为 0。

## table_3 — Club

### 候选行链与计数差异（L1，非通用完整解析器）

- client/server header 均声明 84,259；payload 分别 6,932,082 B、16,595,312 B。固定步长不成立（扣除标准 14 B header/8 B footer 后分别余 22,822 B、80,526 B）。
- 既有长度前缀名称 + 重复-u32 DUNI/Team DUNI 单调链，在 client 与 server 各选择 84,250 个候选；进入链前有 95,278 个名称候选。两边候选名完全相同（84,250/84,250），均可在 English club language layer 找到；最后候选为 `Ningxia Pingluo Hengli`，candidate index 84249，client offset 6,931,981 至 data_end。此结果支持稳定的候选顺序，但不是覆盖任意嵌套内容的通用 table_3 行切分器。
- 与 header 数量相差 9。`table_extra_3` 的完整序号流在 candidate index 84249 后还有 ordinal 84250..84258 共 9 个终端辅助记录；client 每条 25 B、server 每条 238 B，两侧均无长度前缀字符串，`Cyfn` 候选值依次为 0、0、0、2021、2021、1992、2014、2016、2018。故差异精确定位在“主表命名候选链结束后仍存在 9 个额外辅助序号”这一层；这些序号的 Club 身份及对应主表字节边界未恢复，不把它们猜成 9 个已切开的主表行。
- 异常反例保留：`NK Željezničar Bosanska Krupa`（NBSP）有 repeated-u32 候选，low-u32=语言层 key−1 且 DUNI 出现在 Team 集合，但该位置落入另一候选段，尚无独立顶层边界证明；不计为已恢复行。`NK Rudar Kamengrad` 的近邻 repeated-u32 候选不在 Team DUNI 集合且不匹配语言层 DBID，证伪为有效锚点。候选筛选不完整/有嵌套命中，报告保持“候选链”措辞。

### 已命名字段与锚点

所有偏移相对候选记录起点；变长 name prefix 会改变部分字段的有效偏移，不能把单一样本偏移套用于全部行。

| 字段 | 候选布局 | 独立核验 / 证据 |
|---|---|---|
| `duni` | repeated-u32 identity 候选，紧邻 primary name 前 | 84,250 条单调链候选；未宣称其覆盖全部 84,259 行（L1 结构候选） |
| `dbnm` | 第一条长度前缀 UTF-8 名称 | 84,250 个候选名称均在英文 club language layer 命中（L2 交叉锚点） |
| `Csnm` | 第二条内联字符串 | Liverpool、Man City、Arsenal、Chelsea、Bayern、Barcelona、Juventus、PSG、Newcastle、Tottenham、Dortmund、Ajax、Inter、AC Milan 共 14/14 匹配语言层 slot 2（L2） |
| `Cnti` | 候选 u32 @+10 | Nation row ordinal；Cardiff、Vaduz、Andorra、Wellington、Derry 等对照其国家记录（5/5，L2） |
| `Cbni` | 候选 u32 @+18 | Based Nation ordinal；上述锚点覆盖 Wales、Liechtenstein、Andorra、New Zealand、Northern Ireland 等（5/5，L2） |
| `Cccn` | 候选 u32 @+22 | Continental Cup Nation ordinal；同一组 5 个独立国家行序核验（5/5，L2） |
| `Ccty` | primary-name payload 前 14 B 处的 u32；常见 row+26，Shanghai Port 样本 row+25 | 值指向 table_2 `rdui`；Liverpool、Manchester、London、Cardiff、Vaduz、Andorra la Vella、Wellington、Londonderry、München、Paris、Shanghai 等 12/12 城市名匹配（L2） |
| `Cyfn` | client `table_extra_3` 同 ordinal 行 u16@+4 | 14 个知名俱乐部成立年锚点 13 个精确；Manchester City 库中为 1894，外部常见起源年 1880，作为约定差异保留（L2） |

新增 L2 命名字段共 6 个（`Csnm/Cnti/Cbni/Cccn/Ccty/Cyfn`），达到本表 ≥5 的字段数量线；但不代表 Club schema 全字段已解。

### 已证伪候选与未定位字段

- `Cext` 的单字节猜测槽观察到 0、2、111；不符合简单 boolean 候选。`PLgn` 的 u16 猜测槽出现 2、4、6、32、26990 等超出 schema enum 0/1 的值。`Cedp` 猜测 byte 为 1 的有 323 行，包含非 MLS 俱乐部；因此撤销这三个具体 raw-slot 假设，不据此否定 schema 字段本身。
- `Clri` 是只读字段，schema 未标 `is_client_field`；旧候选又与已证伪的 PLgn lane 重叠，撤销。
- `ttcl/tbcl`：Liverpool、Man City、Arsenal、Chelsea 的 RGB/BGR 三字节及常见 alpha 前/后缀形式，在对应 client/server table_3 与 table_extra_3 候选片段均无命中；颜色序列化槽仍未定位。
- `Csti`：Dalian Yifang 的 server table_3 候选片段在 row+124 有一个 u32=18,602，恰等于独立 Team.Tsti table_21 `rdui`，再映射到 stadium DBID 23,226,089；这是单个 L2 候选。Dalian Chaoyue 与七个知名俱乐部控制样本均未命中各自 Team.Tsti 的预期 rdui、对应 stadium DBID u32 或重复 DUNI 编码。故有一条正锚点，但尚无通用偏移/空值规则，不把 Team.Tsti 路径推广为全部 Club.Csti。
- `Crep`：对 12 个知名俱乐部做 u16/u32 lane 排序扫描。参照仅是 table_24 DUNI+12 的探索性 Reputation proxy（自身未独立确证）；扫描 Club client/server main 与 client/server extra 的候选行起点/名称尾端，限制 0..10000、至少 8 个非零与 7 个不同值。各源最高 Spearman ρ 分别为 0.034/0.402/0.328/0.593，均未达强一致阈值 0.8。另以 FMPlayer FM24 profile 的 Liverpool=8900、Juventus=8500、Tottenham=7800 作字面值对照；四类候选切片中 u16/u32 little-endian 命中均为 0。网页未标 24.3 等具体 patch，所以这是带版本 caveat 的负探测，不证明该字段缺失或本机版数值不同；`Crep` 保留未定位。
- `CLat/CLon`：22 个由 `Ccty` 可映射到 table_2 的俱乐部样本中，Club main/extra client/server 片段均没有对应城市纬度/经度的精确 float32 命中；直接坐标槽未定位，可经 `Ccty → city` 派生。
- `ttcl/tbcl` 已测试四个知名俱乐部的 RGB/BGR 与常见 alpha 前/后缀形式，样本片段无命中。`Csxn/Cl3n/Ca3n/TCnn/TCht` 等其他语言字符串未完成逐字段映射。未知即保留未知。

外部字段值来源（页面只标 FM24、未标 patch）：[Liverpool](https://fmplayer.net/club/fm-24/liverpool-676)（8900）、[Juventus](https://fmplayer.net/club/fm-24/juventus-1139)（8500）、[Tottenham](https://fmplayer.net/club/fm-24/tottenham-728)（7800）。

复跑：`py -V:3.12 -I scripts/b47_tables_big.py --table 3 --output tmp_b47/table3_probe.json`。

## table_extra_3 — Club auxiliary rows

### 三路线判定与边界

client/server header 均为 84,259；payload 分别 13,053,908 B / 35,009,248 B，首个 ordinal marker 从 offset 12 开始。边界结论限于此 ordinal-tagged variable-record 模型，不把它误称为固定步长表。

| 路线 | 探测 | 结论 |
|---|---|---|
| offset/length index | body 开头 u32/u64 不单调；offset 12..64 的 u32 候选无单调 index；u16/u32 长度数组求和均不等于 body 长度 | 证伪简单 offset/length 数组模型 |
| fixed stride | header/footer 各 0..256 B 穷举，没有任何整数 stride；body/count 为 client 154.9258、server 415.4955 | 证伪固定步长模型 |
| ordinal/template | client 序号 0..84258 全部找到；以 ordinal + `Cyfn` 域（0、65535 或 1800..2100）过滤行内误命中；server 序号扫描覆盖全 84,259 项，并以同 ordinal client 年值交叉 | client 84,259 行边界恢复；server ordinal markers 全量覆盖，53,572/53,592 个非空 client 年值在同 ordinal server 区间再次出现。server 缺少年值的记录与 20 个未命中年份样本保留较低边界置信度，不称每条 server 切片都独立证实（L1/L2 交叉） |

- client 年域校验拒绝 15 个贪婪扫描误命中，实际修正 13 个 ordinal 位置；行长 min/median/max=8/79/1,861 B，最后一行 25 B，未消费尾长 0。server 行长 min/median/max=5/331/5,779 B；5 B 最小值保留，不因大小而删行。
- client `Cyfn@+4` 有 53,592 个非空年份、30,667 个 null；年份值在 53,572 个同序 server 行出现。server 内 `00 6c 07 01` 的 1900 模板重复，不单凭模板命中声称 Cyfn；Bayern/Ajax 等 1900 必须以 client ordinal+4 和俱乐部锚点判定。
- 已知成立年锚点覆盖 Liverpool 1892、Arsenal 1886、Chelsea 1905、Barcelona 1899、Juventus 1897、PSG 1970、Newcastle 1892、Tottenham 1882、Dortmund 1909、Inter 1908、AC Milan 1899 等；Manchester City 库值 1894 的差异见 table_3。
- tail ordinal 84250..84258 共 9 条，client 长度全部 25 B、server 长度全部 238 B；两侧均无长度前缀字符串。这就是主表 named-candidate 链后续的辅助序号差异所在。终端记录身份不明，不从 Cyfn/null 值推测俱乐部名称。

复跑：`py -V:3.12 -I scripts/b47_tables_big.py --table extra_3 --output tmp_b47/extra3_probe.json`。

## b47 当前交付边界

- table_2 城市身份/43 B 布局、table_21 球场全槽位表、table_25 127 B 全槽位表、table_3 六个 L2 字段、table_extra_3 三路线及 ordinal 边界均有可复跑证据。
- table_25 目前只有 `ccti/cnti/cpcm` 三个 L2 业务字段，低于 ≥10 线；按诚实负结果验收，不伪报全 schema 对齐。
- table_3 的 9 个终端辅助序号身份与对应主表边界仍未分配；Club 其他字段与 `table_2` row+11..29 仍有未解区。
- 本报告没有 L4；未启动游戏/编辑器，也未写入安装库或用户数据。
- 本 worktree 已执行全量 regression。按 runner 原有“missing inputs → SKIP”约定补上 census 两项的输入存在性前置检查后，结果为 4 PASS / 0 FAIL / 8 SKIP；8 个 SKIP 均由 ignored decoded/decrypted/save 输入不可用导致。可运行项通过，但不能伪报为 12/12 PASS；详见 `tmp_b47/PROGRESS.md`，应在只读样本可访问时补跑。
