# t47 — Nation 未知 item-bearing parent 静态发现(t37 负例攻坚,集合追踪法推广)

你是受指挥官委派的子代理,负责**最难**的发现任务。t37(luna 数据侧)已诚实负例:nation 29 list parent 中 **25 unknown/partial,0 nation 独占 L3**;15 个 item-bearing parent 的 table_type/archive/RTTI/count/stride **全未知**(link_status=partial_parent_to_table_unknown)。t44(sol)刚用**静态集合追踪** crack 了 Cafl/Cvfl 共用的具名辅助 POD 成员 `club_links.dat`(无 factory case/RTTI/slot19)。本任务把同一方法推广到 **NATION** 对象,反查这些未知 parent 的真实 backing member 与 reader,闭合 cursor 并按三重闸门晋级 L3。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- scratch/t37/out/nation_subtable_inventory.json + REPORT.md(**负例真源,原样保留不删改**;parents/link_status/blockers;next_static_handoff 点名 Nntp/Ntxr/Nfmp)
- scratch/t44/out/REPORT.md + discovery_cafl_cvfl.json + cursor_club_links.json(**集合追踪+具名辅助 POD 成员范例**:CLUB slot2 `0xe89a00` 按 4CC 精确分发→club `+0x118/+0x120` vector→分配池 VA `0x141b5ecc8`(CLUB_LINK,非 RTTI)→具名打开器 `0x434e390` 拼 `club_links.dat`→reader `0x1529210`;47B POD,12B header+u32 count@8,无 selector/identity/footer;版本 word VA `0x141b60330` 门槛 `0x0dd6`)
- scratch/t39/out/REPORT.md(**NATION slot2 锚点**:`0x1041f30 → 0x1041f40`,`0x1043322 → 0x1065ef0`,`0x1066981` 同 4CC 汇入 `0x11f41d0`;Team 集合 helper `0x15e9830 → 0x44d7bf0`,全局 VA `0x141b60158` table `+0x80` vector,owner 筛选)
- scratch/t41/out/REPORT.md(变长 cursor 法:wire u32 count 决定 row_len)、scratch/t27/out/replication.md(cursor 模板)
- evidence/fm24/reports/editor_schema/master.json(nation.xml#nation,冻结 SHA 7d57477e 对照 MANIFEST)
- scratch/t24/out/subtables.part*.json(nation nested occurrence idx)

## 目标 parent(15 个 unknown item-bearing,按簇优先)
| 簇 | parent | idx | items | 字段 |
|---|---|---:|---:|---|
| **transfer prefs**(handoff 点名 Nntp) | Nntp | 224 | 6 | nati,rati,sckn,mina,maxa,affl |
| | Nctp | 225 | 5 | cont,rati,mina,maxa,affl |
| | Nrtp | 226 | 5 | regi,rati,mina,maxa,affl |
| **tax/famous**(handoff 点名 Ntxr/Nfmp) | Ntxr | 232 | 9 | lowa,uppa,capa,perc,txty,ppty,year,fram,leve |
| | Nfmp | 233 | 6 | pers,desc,heig,side,perm,rtng |
| | Nftb | 234 | 7 | NbPi,NpFn,NpSn,NbPd,NbPn,NbFt,NbCn |
| **repu values**(同构 repu/valu) | NTRv | 228 | 2 | repu,valu |
| | NWGv | 229 | 2 | repu,valu |
| | NSps | 230 | 2 | repu,valu |
| **dates** | EDfx | 342 | 7 | date,day_of_week,time,stadium_rules,text,highest_division_level,lowest_division_level |
| | EDsc | 344 | 6 | date,day_of_week,time,stadium_rules,competition,text |
| **misc** | Nrvn | 216 | 2 | nati,leve |
| | NCro | 231 | 2 | comp,crep |
| | Calt | 235 | 2 | cmid,stid |
| | TCrs | 64 | 4 | PUnI,PUnT,PUnP,PUnJ |

**强 hypothesis**:同簇可能共用一 backing member(如 Cafl/Cvfl 共用 club_links);transfer prefs 三件、repu values 三件、EDfx/EDsc 尤甚。待静态证实/否证,不预设。

## 任务
1. **静态发现 backing member**:NATION slot2 `0x1041f30`(或实际 nation getter)按 4CC 精确分发→追集合 helper→全局集合 table/分配池→entry vptr 或具名打开器→factory rel32 case **或**具名 `.dat` 成员→确定 table_type/archive/RTTI(或无 RTTI POD)/count/stride。保存每跳 bytes+VA+指令分片。同簇共用或各自独立,如实判定。
2. 对每个 crack 出的 member:两 archive 目录+payload(count/stride/SHA,client 无成员如实记);多帧/data_base 按 E80(绝对起点=data_base34+entry.offset,entry.size 选帧,entry.sha256=压缩区 SHA)。factory→RTTI/vtable→slot19→真 reader(+identity tail)或 POD reader,PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk。
3. 分支五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead)逐条证据+首反例;变长按 t41 法;POD 阵列按 t44 法(版本 word/无 selector)。
4. walk 逐行闭合 header+Σrow+footer==payload_len;双坐标 legacy14/wire13(POD 则如实记不适用);identity 后置校验;selector 全表观察。
5. 三重闸门+全表画像:ordinal 引用(nati→nation/t?、cont→continent、regi→region、comp→competition、pers→person、affl→club、cmid/stid→stadium 等)走**目标实表实际 ordinal 集**(t39/t44 法,非 public UID);date packed;repu/valu/rati/mina/maxa integer 有符号/sentinel;enum 域;bool 验 bitmask(t31/t44 法)。可证实者 L3,域冲突/全空 held 留首反例。
6. 若某 parent **无独立 member**(嵌入 parent 记录/uninformative RTTI/运行时生成):诚实 negative+静态证据指明列表实际所在,保留 t37 负例,不强行晋级。
7. 独立 verify.py(不 import builder/ReaderCFG/fm24_dump)+ builder scripts/t47_nation_unknown.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 nation 未知 item-bearing parent;**不碰** t28 已闭(Nagr/Nefr/Nnfr/Nlns table_10 client-tail)、Tchl(t34 共享,t39 已裂)、club 子表、zero-item schema(Nchi/Nphi/Tko*/Tkg*/AXML)。
- t46(luna)正做 server table_10 **数据侧** profile;若未知 parent back 到 table_10,可引用其 member 但**专注静态 reader/cursor/L3**,不重复 t46 数据侧画像。
- 候选不写结论;t37 negative/held 原样保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 预算内无法全裂则诚实 partial:已发现链接+已闭合子集+剩余+首反例(发现任务允许 negative)。**优先裂 transfer prefs 簇 + repu values 簇 + Ntxr/Nfmp**(handoff 点名),再及其余。

## 交付 scratch/t47/out/
- discovery_nation_unknown.json(parent→member→reader 静态链+table_type 判定,逐 parent)、cursor_*.json/fields_*.json(闭合者)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t47_nation_unknown.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;只写 scratch/t47/ 与 scripts/t47_*.py;完成跑 verify + t01_anchors.py(7/7)。