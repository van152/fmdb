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

## 增量(2026-11-20 日班,E100–E109,指挥官记录)

接上节。快照数字不动(`baseline_coverage.py --check` 仍 OK)。E99 之后本轮新增验收:

| 层 | 增量 |
|---|---|
| schema | **v8→v9**(t60/E100,comp 主行并入)、**v9→v10**(t70,本轮 r2 证据并入);条目级 ledger 守卫扩至 E84–E109 |
| club 主行 | t63(E106):399 unmapped 复查 → **+8 L3**(Ccba/Cadm/Cesd/Ceed/Cead/CteA/Chaf/Cmtp,全为 server `CLUB+0x150` tag-0 getter 投影)、41 held、350 unmapped;**club 主行 L3 13→21**;负证据保留(4/4 appeal 早于 start,首 row 1410 @851416;Casp 越界 85,746.46 @15571299) |
| comp 主行 | t64(E107):196 unmapped 复查 → **0 新 L3**(诚实负结果)+ 调用记账修正(55 = 52 外层 + 3 tag-4 备用);+0xa8/+0xe0 静态谓词与 7,047 全零数据反例;8 类排除 196 项 |
| nation 主行 | t65(E108):327 unmapped 复查 → **0 新 L3 / 9 转 held**、318 unmapped;封口 24,732 / 422,345,identity **12B**(修正旧 13B 借用),footer ec7ae404 |
| comp 集合 | t66(E104):**7 个非空集合物理文法 L3**(vec18/+0xe8/+0xc0/+0xc8/+0xd0/+0xd8/+0x100)+ 3 held;**4 条引用 lane L3**:vec18:item+1→t24(team)、+0xd0:item+0 / +0xd8:item+0/+4→t23;未绑定独立 comp 子表成员(诚实负结果) |
| 悬案 | t62(E105):**EDsc 分发闭合**——非字面 4CC,key 0x45447363 归一化 +0xbabb8ccf = 0x32,表基址 0x2a7f0 第 0x32 格 → 0x29389(68 格唯一),按对象类型进 COMP/NATION Schedule 生成器并返回 UI;它不是持久化字段,held 保持正确。**EDfx 上游仍未闭合**(仅 cmp @0x29c37,链路至 fles 容器/日历桶/NATION+0x108 backlink,7 条可重开排除) |
| 数据侧交叉 | t67(E102,comp)、t68(E103,club):DP 单路 + 跨档 UID 同值 + 敏感性全表复现;club selector `{0:84,256, 12:3}` 与 t57 一致;三张主表行框均已有 reader 独立的数据侧证明(与 E91 nation 并列) |
| 尾账 | t69(E109):18 项(club skipped 10 全部承接、nation held 4、comp static-zero 3、edge-pending 1),**零悬案** |
| 仍开 | EDfx 上游持久化来源;club 350 / comp 196 / nation 318 未映射主行字段;comp 集合业务语义(t66 仅物理层);club 22 cnst 投影缺主行游标;merge-to-main(仍按 HANDOFF 搁置) |

更新命令不变:`py -V:3.12 -I scripts/baseline_coverage.py --check`(快照数字仍应 OK)。

## 增量(2026-11-21,E111–E120,schema v10 → v11)

接上节。快照数字不动(`baseline_coverage.py --check` 仍 OK,分母单拆为独立文件不影响冻结聚合)。E109 之后的本轮验收与 `schema v11` 合并:

| 层 | 增量 |
|---|---|
| schema | **v10 → v11**(t77/E111–E120,additive-only):22 个 v10 根节逐字节不变,新增 10 节 + 2 个拆分件指针;`--verify` 63/63。**E121(t82)不入本版**,归 t87 补丁 |
| club 主行 | t71(E111):`CLUB+0x100` 链闭合为 `table_extra_3.dat` 双档行框(client 13+13,053,908+9 / server 13+35,009,248+9,84,259×2 行);**24 条 held 记录转正**(22 cnst 投影在 extra 对象 `+0xe0`/`+0xe7` 双块 + `Cebd` + `Cyfn`);**club 主行 L3 21 → 43** |
| 槽位指纹 | t72(E112):三主表未命名槽位清单 club 34 / comp 84 / nation 40 槽(未命名 20/36/24),10 项 nation 内层文法升级移交给 t75;**partial 交付,不言称闭合** |
| 简单表 | t73(E113):通用映射器 + city(2)/continent(5)/region(19)/currency(41) **8/8 帧闭合**;预警记录 14、flip **1**、未命名 27、candidate 4、unmapped 27;10 个 distinct L2 (表,字段,offset) 三元组;alias group **否定结果原文保留**(header_origin_data_unique 全 False → 数据侧无法定 header 起源);冻结锚点复验 14/0 冲突 |
| nation 文法 | t75(E114):10 段内层文法survey,**8 段字节级闭合**、slot_2/slot_3 无真项保持 held;**99 槽逐条裁决,新具名 L3 = 0**(诚实负结果);club 25 / comp 40 / nation 34 held;t71 的 24 个 4CC 排除不重复计入 |
| 行框 | t74(E115):9 表 × 2 档 = 17 个 (archive,table) 行框闭合、**0 escalations**;team(24) client 条目按 t66 记录**真缺失**(非空目录),已如实记录;identity 宽度逐表自证(敏感性反例已跑) |
| 分母 | t78(E116,L1):**1,034 occurrence** 真实分母(club 433 / nation 346 / comp 255),物理覆盖 **110/1034 = 10.6%**;分桶 held 59 / unresolved_wire_slot 277 / no_wire_evidence 564 / ui_or_derived 24 |
| stadium/team | t79(E117,t71 静态方法收割):stadium.xml 41 L3、team.xml 11 L3、table_extra_24 3 映射字段、club `+0x18` 转发 6 字段 held→L3;L4=0 |
| scan 表 | t76a(E120):stadium **12 client / 47 server 槽,0 未覆盖字节**,verify 49 项 0 failed;t76c(E118):derby 10 / weather 25 / local_region 11 / agreement 9 槽(各档同数),**8/8 档闭合**;derby 6B 差=3 字段、weather 95B=3+4×23 结构发现 |
| 车道裁撤 | t80(E119,**probe_negative**):枚举增补前提证伪——快照与 master 枚举 100% 恒等,无增补空间,车道裁撤。**记为负结果探测,不是验收**。t76b(award/language/media)三连墙零落盘已弃,转 t83 接收 |
| 体积治理 | v11 主 JSON 只留三主表 + 8 编号子表 + CLUB_LINK + r2/r3;13 张非主表槽位裁决 → `reports/other_tables_schema.json`(286 KB);分母全账本 → `reports/xml_denominator_coverage.json`(298 KB)。主 schema 存 path + SHA-256 指针,`--verify` 重算比对 |
| 仍开 | EDfx 上游;club 350 / comp 196 / nation 318 未映射(分母口径已明确:优先级看 E116 的 277 unresolved_wire_slot);award/language/media → t83;comp 集合业务语义;held 枚举域;E121 → t87;merge-to-main(评估见 REPO_STATUS 第六节,未执行) |

更新命令不变:`py -V:3.12 -I scripts/baseline_coverage.py --check`(快照数字仍应 OK)。
