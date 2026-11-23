# t33 — club/team 子表数据侧画像 batch II(扩充 parent↔table 连接池)

你是受指挥官委派的子代理(devseek,数据侧批量)。t29 已画像 13 个 server 子表,t29b inventory 显示 38 个 club nested 父码中 28 个仍 unknown(无表连接)。本任务**画像一批未覆盖的 STARTING_* server 子表**,产出 complete_data_profile,为 parent↔table 连接与 sol 静态复制备料。**不做静态 cursor、不晋级 L3**。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;只读 scratch/data + 仓内证据)
- D:\tmp2b\fm24-db\scratch\t29\out\profiles\table_server_43.profile.json(**画像格式模板**:status/table_type/archive/rtti_class/entity_tag/payload{sha256,packed_offset}/row_closure{count,stride,equation,rows_sha256}/columns[逐字节列 unsigned 统计])
- D:\tmp2b\fm24-db\scratch\t29\out\subtable_inventory.json(38 父码现状:high/candidate/unknown;unjoined_tables;next_scout)
- D:\tmp2b\fm24-db\scratch\t14\out\census.json(74 表 RTTI/primary_class/entity_tag/adjudication)
- D:\tmp2b\fm24-db\scripts\fm24_dump.py(load_payload;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data)

## 目标表(本批 7 个,均 server archive)
| table | RTTI | entity | 可能父码 |
|---|---|---|---|
| 58 | STARTING_WEEKLY_WAGE_CONTRIBUTION | club | **Cwcl**(强候选)|
| 39 | STARTING_AVERAGE_POINTS | team | CPsL/其他? |
| 12 | STARTING_AWARD_HISTORY | awar | Cafl/Calt? |
| 45 | STARTING_RECORD | candidate | 待定 |
| 48 | STARTING_RECORD | candidate | 待定 |
| 59 | STARTING_MEDIA_EXPECTATIONS | play | Csme(inventory candidate)|
| 73 | STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT | play | 待定 |

## 任务(每表独立,数据侧)
1. dump 全行:报 count/stride/行封口方程(`header+Σrow+footer==payload_len`,双约定 13+n*s+9 与 14+n*s+8 都试);payload SHA + packed_offset。
   - **多 zstd 帧 caveat**(E66):若 load_payload 返回空/异常短,查成员是否含空 stub 首帧,用真帧 offset(参 table34 +9 空/+34 真)。
2. 逐字节列画像(同 t29 格式):offset/width/interpretation(u8/i8/u16/i16/u32)/count/distinct/min/max/zero_count/sentinel(0xFF/0xFFFFFFFF)率/top_values。
3. 语义候选(L2,标 candidate 绝不 L3):packed day/year 日期列(高16年/低9日或双 u16)、club ID 域[0,84259)、competition ordinal[0,7046]、stadium ordinal[0,48412]、cash 样数值、enum 值集。把列对到 schema item 字段类型语义(读 master.json 对应父码 list_item_fields)。
4. parent↔table 连接判断:用 RTTI 语义+entity_tag+schema item 语义给 confidence(high/candidate/unknown)+blockers。**不确定标 unknown,不猜**。
5. 每表落 `scratch/t33/out/profiles/table_server_<tid>.profile.json` + `.rows.jsonl`(全行原字节)。

## 纪律(防超时)
- **每完成一表立即落盘 + 追加进度到 scratch/t33/out/PROGRESS.md**;卡壳就标 partial 跳过做下一表。
- 7 表做不完就交已完成的,**全部完成或窗口将尽时写 DONE.md**(一句话:完成 N/7 表 + 各 count/stride + 新连接候选)。即使 partial 也写 DONE.md(让 launcher 正确识别交付,避免 t26 式 gave up 误判)。
- 只写 scratch/t33/out/ 与 scripts/t33_*.py;不覆盖 t29/t29b 产物;候选不写结论;negative 保留;L4=0;不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。
- 新脚本 --help/--selftest,退出码 0/1/2;大 JSON 分片;单次打印 ≤400 行。
- 派生大缓存(pkl/npy)勿放 out/(已 .gitignore 排除 scratch/**/*.pkl|npy)。

## 交付
- scratch/t33/out/profiles/(每表 profile.json + rows.jsonl)
- scratch/t33/out/subtable_candidates.json(本批 parent↔table 连接候选 + confidence + blockers)
- scratch/t33/out/REPORT.md + DONE.md + verify.py(独立复算封口+抽样列统计)
- scripts/t33_profile_batch.py

Python `py -V:3.12 -I -B`;完成跑 verify + t01_anchors.py(7/7)。