# 覆盖率基线(2026-11-18 快照)

来源:对旧库机读证据的聚合分析(`server_tables_census.json` + `db_tables_big.json` + `editor_schema/master.json`;聚合脚本已移植为 `scripts/baseline_coverage.py`)。这是估算不是指标:50 张 unknown 表的分母未知,真实语义覆盖率可能更低。

## 分层现状

| 层 | 进度 | 依据 |
|---|---:|---|
| 容器/目录/解压 | ~95-100% | tad. v3569 + FMF + Zstd 全解;client_db 31 项、server_db 77 项、lang_update_db 352 项边界全过 |
| 表身份 | ~13% | 59 数值表:5 confirmed(2=city, 3=club, 21=stadium, 24=team, 25=comp)、4 candidate(8=lang, 41=currency, 7=media, 10=nation)、**50 unknown**;18 辅助成员 15 个无角色 |
| 行边界 | ~51%(字节)/ ~68%(表数) | 37 定长 stride 候选 + 2 空 + 1 已闭合(table_41);18 变长未解;server_db 242MB payload 中 50.7% 有已解析行模型 |
| 字段语义 | **~1.5%** | 2,144 schema 字段中约 33 个可命名(含身份字段);只算已映射 9 实体(1,175 字段)为 ~2.8% |
| people_db 语义 | ~1.5% | 658,011 行链 100%(L1);身高/体重/DOB/Pcex/Pcti/Pcjd ~6 字段 L2;位置码 4/14;**PDxx 属性 0/40(负结果)**;CA/PA 弱候选 |
| 历史库 | 结构 ~70%,语义 ~5% | pl/non_pl 索引与行链 L1 闭合;履历记录字段语义基本未命名;稀见 row_type 0/14 L2 |
| summary.dat | 身份/布局 100%,字段 0% | b51 为逐槽穷尽负结果 |

## 已映射表明细(命名字段 / schema 字段)

| 表 | 实体 | 命名 | schema | 覆盖 |
|---|---|---:|---:|---:|
| table_2 | city | 6 | 15 | 40% |
| table_21 | stadium | ~10(含 Ssds 结构) | 60 | ~17% |
| table_24 | team | 3 | 25 | 12% |
| table_3 | club | 9 | **433** | 2% |
| table_25 | comp | 5 | **255** | 2% |
| table_10 | nation | **0** | **346** | 0% |
| table_8/41/7 | lang/currency/media | 0 | 12/7/22 | 0% |

## 工作量集中度

club(433)+ nation(346)+ person(271)+ comp(255)+ player(179)五个实体占 2,144 字段的 **69%**;其中 club/comp/nation 语义覆盖 0-2%。剩余工作高度集中 → 攻通用映射结构,不做单字段攻坚。

## 战术结论(承接旧库)

1. 纯字节统计在 packed 区已证伪殆尽(table_25 全偏移 u16/u32 探测、club 颜色四源扫描、summary 逐槽)——边际收益归零。
2. 下一个杠杆 = **editor.exe 内的字段槽位映射结构**(编辑器必须知道每个字段在行内哪里才能显示/编辑)。
3. 既有 L2 锚点是将来验证 L3 映射的测试夹具:六大洲 0..5、England=139、parent=352、Liverpool 坐标、Bernabéu 81,044、俱乐部成立年等。
