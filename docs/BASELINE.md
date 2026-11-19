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

## 增量(2026-11-20 夜班,E89–E95,指挥官夜班记录)

上表为 2026-11-18 冻结快照(`baseline_coverage.py --check` 所钉数字不变)。以下为快照之后已验收的增量,口径见 `scratch/t01/LEDGER.json` E89–E95 与 `reports/club_nation_subtable_schema.json`(现 v6,v7 fold E94 进行中):

| 层 | 增量 |
|---|---|
| 行边界 | t9/table_extra_9/t10 双档(client/server)全闭合:wire13 变长游标 + 13B identity tail + footer,DP 唯一铺法(E89/E91/E93);t46 A/B/C_D 未解段收口为 Nlns/Nefr/Nnfr/Nagr(E94);extra_9 形态=名称块(ordinal\|name_len\|name)+TCrs getter 类型化后缀(E91/E93) |
| 字段语义 | club 子表层:schema v6 = 8 numbered 表 + CLUB_LINK,94 L3 occurrences/59 unique wire/21 held/4 negative(v4–v6);nation 层:Ntxr 7 + t9 parent 17 + Nrvn/Nftb 6 + 主行 5 = **30+5 L3**(t55 的 5 个待 v7 并),held 20+5 类,negative 15;**nation 表身份下 named 0→5/346** |
| 方法 | 三重闸门(frozen 唯一 occurrence→getter 4CC 精确分发→同位移 sink)+目标实表 ordinal join+条目级 ledger 守卫,已跨 t47/t49/t51/t53/t55 五次复用;wire 顺序≠XML 顺序(46 倒置,E94) |
| 表身份 | t9=NATIONAL_TEAM_CONTAINER(owner)、t41=currency(L3 join 229/22 复核)、t19=region、t5=continent 经引用闭合;extra_9=nation 名称表(L1) |
| 仍开 | EDfx 上游持久化来源、EDsc 调用链、held 枚举域(scoped enum_ref)、327 个 nation 主行未映射字段、club/comp 主行批量字段 |

更新命令不变:`py -V:3.12 -I scripts/baseline_coverage.py --check`(快照数字仍应 OK)。

## 增量(2026-11-20 夜班二段,E96–E99,指挥官夜班记录)

接上节。快照数字不动(`baseline_coverage.py --check` 仍 OK);以下为 E95 之后已验收增量,口径见 `scratch/t01/LEDGER.json` E96–E99 与 `reports/club_nation_subtable_schema.json`(**现 v8**,E98):

| 层 | 增量 |
|---|---|
| club 主行 | t57(E97):table_3 双档封口 client 6,932,082 / server 16,595,312 B,84,259×2 行;**identity 12B**(ordinal\|UID\|UID,修正旧 13B 假设,69705 敏感性反例保留);主 reader slot19 0xe5a7a0 extent 1,412 指令/167 分支,34 逻辑位置;433 occurrence → **13 L3**(Cext/Cedp/Cncl/CIns/Ctsi 新增 + duni/Cnti/Cbni/Cccn/Ccty/CASt/Csot/CnCV)/11 held/10 skipped/399 unmapped;**72 对倒置**;E60 Cccn negative 原文保留+真绑定 +0xf0 注记 |
| comp 主行 | t59(E99):table_25 双档封口 client 13+894,969+9 / server 13+1,533,950+9,7,047×2 行;identity **12B**(dsha\|duni\|saved rdui==duni)+ footer 9B 00000000\|01\|4ec43a77;client 定宽 127B/server 条件模板 77–82 站点,联合 82 观测+2 静态未触发;COMP 真 slot19 0xeb7000 extent 837 指令/114 分支;255 occurrence → **49 L3(48 个 4CC,26 个新 4CC**:LAUC、cext/cusn/culn bit 投影、22 个 cnst 契约状态投影 Pcsp..Pcsy/Pcjm..Pcsc)**/10 held/196 unmapped;818 对倒置;引用域 ccti→t5、cnti→t10、cpcm→t25 自引、cnor/csou/cwes/ceas→t2 全零违例;wbst/wben 历法校验、levl getter 排 100、crep server-only |
| 表身份 | **三张主表行框全部自证闭合**(nation 13B / club 12B / comp 12B+9B footer——per-table identity 宽度必须按表自证,不得照抄,已写入 schema 口径);COMP 工厂 case25 双对象形态(db::COMP 与 DATABASE_TABLE<COMP>)不合并 |
| 语义覆盖 | nation 主行 5/346、club 主行 13/433、comp 主行 49/255 全部过三重闸门+全档域检验;schema v8 为合并基线(comp v9 fold 待下一班) |
| 仍开 | held 枚举域(scoped enum_ref)批量补、EDfx 上游/EDsc 调用链、club 399+comp 196+nation 327 未映射主行字段、comp 82 站点中未对齐的投影、merge-to-main(仍按 HANDOFF 搁置) |

更新命令不变:`py -V:3.12 -I scripts/baseline_coverage.py --check`(快照数字仍应 OK)。
