# Club ↔ Stadium 关联：静态对齐结果

## 结论

新增只读脚本 `scripts/modding_club_stadium.py`。安装库路径已打通：`table_3` 的 club DUNI 与 `table_24` 的主 team DUNI 相同；`team.xml` 的 `Tsti` stadium 引用在样本中存成 `table_21` 的 `rdui` 行索引，再经 table_21 身份字段转换成球场 DBID。安装库得到 14 个合理的知名俱乐部映射，另有大连地区样例。

存档 `1 1-大连人.fm` 的已解 `game_db.dat` 中，定位到“**大连人足球俱乐部**”DUNI `0x0207863f0207863f`（候选 DBID 34,047,551）；同 DUNI 的 Team 记录含 save table_21 `rdui=10309`，该行唯一身份映射到球场 DBID **23,226,089**。该存档球场行坐标 `39.020542, 121.561707`，`Scpy` 候选容量 60,000，Ssds 八槽 capc 合计 60,000。

## table_3 / table_24 布局与关联字段

| 资源 | 实测条目/尺寸 | 结构结论 |
|---|---:|---|
| client `table_3.dat` | 84,259 rows / 6,932,082 bytes | 变长记录，名称内联；不满足固定步长尺寸关系 |
| server `table_3.dat` | 84,259 rows / 16,595,312 bytes | 变长记录；DUNI 可在俱乐部名称附近按重复-u32 识别，并与 team 身份交叉核对 |
| server `table_24.dat` | 84,507 rows / 8,819,030 bytes | Team 记录；DUNI 与 table_3 club 记录相同的样例可直接匹配 |
| server `table_extra_3.dat` | 84,259 rows / 35,009,248 bytes | 变长扩展资源，本任务未解其通用字段边界 |
| server `table_extra_24.dat` | 84,507 rows / 6,929,586 bytes | Team 扩展资源，本任务未解其通用字段边界 |

因此 table_3 不能用一个全表 fixed stride 解码。当前可复现的身份锚点是：主名称字符串前有 u32 字节长度，名称附近的重复-u32 DUNI 在 server table_24 中再次出现；主要样例的 DUNI 起点在名称前 40 bytes，少数大连记录是前 39 bytes。该锚点结合 table_24 中的 Tsti 关联解析；不是完整 club row decoder。

`club.xml` 中 `Csti`（Club Stadium）和 `team.xml` 中 `Tsti`（Team Stadium）都定义为 stadium 数据库引用。经交叉验证的通用路径是 **table_24 / Team.Tsti**：Team DUNI 起点后经验位置 `+26` 的 32-bit 值（少数样例 `+25`）作为 table_21 `rdui`；验证 `rdui==row_index` 后，再读取该 row 的 repeated-u32 DUNI 得到 stadium DBID。它不是直接存放的 stadium DBID。下表结果覆盖多个国家/联赛，并以坐标、容量作合理性核对。

### 安装库交叉验证样例

容量列是 server table_21 row+0 的 `Scpy` **候选映射**；它与 schema 字段、多个知名球场容量数据相符，但 server row 前缀尚未整体逐字段解码。坐标来自已验证的 row+160/+164；DBID 来自 row+172 repeated-u32 DUNI。

| Club | club DBID | Team.Tsti rdui | Stadium DBID | 容量候选 | 坐标（lat, lon） | 核对 |
|---|---:|---:|---:|---:|---|---|
| Dalian Yifang（大连一方） | 23,325,084 | 18,602 | 23,226,089 | 60,000 | 39.02054, 121.56171 | 大连体育中心一带 |
| Dalian Chaoyue（大连超越） | 23,245,626 | 2,112 | 131,141 | 30,872 | 39.09536, 121.71915 | 大连城区球场 |
| Liverpool | 172,800 | 67 | 676 | 50,109 | 53.43082, -2.96083 | Anfield 坐标 |
| Manchester City | 173,568 | 7,716 | 5,114,325 | 53,400 | 53.48314, -2.20038 | Etihad 坐标 |
| Arsenal | 153,856 | 7,718 | 5,114,336 | 60,704 | 51.55506, -0.10845 | Emirates 坐标 |
| Chelsea | 161,024 | 27 | 630 | 41,837 | 51.48164, -0.19095 | Stamford Bridge 坐标 |
| FC Bayern München | 233,728 | 12,048 | 8,700,726 | 75,000 | 48.21880, 11.62472 | Allianz Arena 坐标 |
| Barcelona | 436,992 | 423 | 1,049 | 56,000 | 41.36486, 2.15564 | 巴塞罗那奥林匹克体育场一带 |
| Paris Saint-Germain | 221,952 | 351 | 977 | 47,926 | 48.84139, 2.25306 | Parc des Princes 坐标 |
| Juventus | 291,328 | 567 | 1,209 | 41,507 | 45.11000, 7.64110 | 尤文图斯球场坐标 |
| Borussia Dortmund | 231,680 | 642 | 1,293 | 81,365 | 51.49260, 7.45181 | Signal Iduna Park 坐标 |
| AFC Ajax | 253,696 | 754 | 1,417 | 55,500 | 52.31440, 4.94200 | Johan Cruyff Arena 坐标 |
| FC Internazionale Milano | 290,304 | 563 | 1,205 | 75,710 | 45.47806, 9.12400 | San Siro 坐标 |
| Associazione Calcio Milan | 281,088 | 2,474 | 156,312 | 75,710 | 45.47806, 9.12400 | 同坐标的另一条 stadium 记录 |
| Tottenham Hotspur | 186,112 | 19,737 | 28,096,287 | 62,850 | 51.60521, -0.06640 | Tottenham Hotspur Stadium 坐标 |
| Newcastle United | 175,872 | 79 | 688 | 52,404 | 54.97548, -1.62164 | St James' Park 坐标 |

上述 14 个知名俱乐部行均与预期球场坐标/容量相符；Liverpool 指数据库内名称为 Liverpool 的英格兰俱乐部，另有名称为 **Liverpool Fútbol Club** 的乌拉圭俱乐部（其 Tsti 指向 Montevideo 行）。Inter 与 Milan 的两个 DUNI 最终映射到不同 stadium DBID，但坐标和 Scpy 候选完全相同；是重复/别名 stadium 行还是另有语义，未进一步判定。Barcelona 的行落在奥林匹克体育场一带，与数据库版本中临时主场设置相符；未依赖名字猜测。

### 大连人存档侧

| Club（save） | club DBID 候选 | Team.Tsti save rdui | Stadium DBID | 容量候选 | 坐标 | Ssds capc |
|---|---:|---:|---:|---:|---|---|
| 大连人足球俱乐部 | 34,047,551 | 10,309 | **23,226,089** | 60,000 | 39.02054, 121.56171 | 12,474 / 5,100 / 7,326 / 5,100 / 12,474 / 5,100 / 7,326 / 5,100 |

该关联来自 save `game_db.dat`：俱乐部名称前 DUNI 在该文件另有重复出现；另一条同 DUNI 记录的 Tsti 形状字段给出 rdui 10,309。存档的 table_21 对齐区有连续 21,064 行，rdui 连续且 DUNI repeated-u32；rdui 10,309 唯一映射到 DBID 23,226,089。这里的“容量”仍是 `Scpy` 候选；Ssds capc 只是八个边角/看台槽位容量，不等同于已验证的比赛场馆总容量。

## Club.Csti 与 Team.Tsti 的边界

schema 明确存在两个字段，不能把二者合并成一个属性。因此本轮能证实的直接关系挂在 **Team（table_24）的 Tsti** 层；schema 同时存在 Club.Csti，不能据此断言 Club.Csti 不使用或不存在。本工具优先用可交叉验证的 Team.Tsti 路径：同 club DUNI 出现在 table_24，Tsti 指向 table_21 `rdui`；它对上表这些主队给出稳定结果。当前还没有完整解出 table_3 所有变长字段，因此**不声称 Club.Csti 对所有俱乐部都已恢复**。

Dalian Yifang / Dalian Chaoyue 的 table_3 名称附近还各出现一个可映射到大连球场的 rdui 候选；Chaoyue 的该候选与 Team.Tsti 所指 row 不同。它可能对应 Club.Csti，也可能是 table_3 其他字段中的 stadium 引用；在没有通用 Club row parser 前不把它作为已确认值。用户“按俱乐部改球场”脚本当前返回 Team.Tsti 关联，并输出原始 identity/reference 偏移以便审计。

### b47 后续单样本候选（2026-11-17）

b47 按 server table_3 的 DUNI/name candidate slice 复核发现：Dalian Yifang 候选片段 row+124 的 u32=18,602，等于其 Team.Tsti 指向的 table_21 rdui；该 rdui 的 table_21 repeated-u32 DUNI 对应 DBID 23,226,089，坐标也与大连体育中心一带核对一致。这个单样本使 `Club.Csti` 获得一个正候选；Dalian Chaoyue（Team.Tsti rdui=2,112）及 Liverpool、Manchester City、Arsenal、Chelsea、Bayern、Newcastle、Dortmund 控制片段没有同样的直接 rdui 命中。故它仍不是通用 `Club.Csti` offset/serializer 证明；详细偏移探针与保守结论见 `DB_TABLES_BIG.md` table_3。

## 工具用法与验收

```powershell
# 安装库；名称或低 32-bit club DBID 均可
python -I scripts\modding_club_stadium.py --club "Manchester City"
python -I scripts\modding_club_stadium.py --club 173568

# 只读已有的 save 样本副本及其已提取 game_db.dat
python -I scripts\modding_club_stadium.py --source save --club "大连人足球俱乐部"
python -I scripts\modding_club_stadium.py --source save --club 34047551
```

`--source save` 仅接受 `reports/save_decode/samples/` 中的样本副本；读取对应 `reports/save_decode/extracted/<stem>/<stem>/game_db.dat` 与 `game_db_alignment.json`，不写用户 Documents。安装库可用 `--db-path` 覆盖默认 2430 server 数据目录。工具输出 JSON，包含 club DUNI/DBID、Team.Tsti row index、stadium DBID、Scpy 候选容量、坐标和 Ssds 分槽 capc。

已用 `python -I` 实测：Manchester City（名称和 DBID 两种查询）、Liverpool、Dalian Yifang、Dalian Chaoyue、Bayern、Arsenal、Chelsea、Barcelona、PSG、Juventus、Dortmund、Ajax、Inter、Milan、Tottenham、Newcastle，以及 save-side 大连人；全部 Team.Tsti 命中均通过 table_21 rdui/DUNI 身份校验。

## 限制

1. table_3/table_24 是变长数据；本工作没有恢复完整通用行 serializer，也没有逐字段解码所有 Club/Team 属性。Club DUNI 可用重复-u32 身份锚定，但 club row 的通用边界和 rdui 偏移尚未恢复；工具回报的是原始 payload byte offset，不伪造 row index。
2. `Team.Tsti` 的 DUNI 附近 `+26`（大连行 `+25`）是由多 club 同族、schema 和 table_21 身份交叉验证的经验字段定位；不是已恢复的整个 table_24 字段布局。
3. Club.Csti 的通用 raw offset 未解；当前只有 Dalian Yifang row+124 的单样本正候选，工具仍只输出已交叉验证的 Team.Tsti，不把该候选当作通用字段解码。
4. row+0 `Scpy` 仍称容量候选；Scpy 与 known capacity 的交叉样本支持该映射，但尚未从通用 server row loader 静态追到字段反序列化调用链。
5. save game_db 的完整 table directory/table_24 边界尚未恢复；save-side team 记录依据同 DUNI 重现和 table_21 rdui 校验，结论只覆盖这个样本。
6. 所有分析只读游戏目录及工作区 save 副本；没有写安装目录/用户 Documents，没有启动 FM24 或 Pre-Game Editor，也未做实际加载测试。

变长表与 Club 字段后续试解见 [`VARLEN_ROWS.md`](VARLEN_ROWS.md)。
