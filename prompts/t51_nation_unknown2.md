# t51 — Nation 剩余 6 unknown parent 静态 getter 发现(t47 后继:owner 判定 + 反查收尾)

你是受指挥官委派的子代理,负责**最难**的静态发现收尾。t47(sol,E87)对 nation 15 个 item-bearing unknown parent 完成静态发现:9 连到内嵌集合+reader(Ntxr 单独闭合 7 L3;8 落 t9 NATIONAL_TEAM_CONTAINER,由 t49 做双档 wire 验收),**6 个仍 unknown**(unknown_links=6)。本任务只做这 6 个:确认真实 owner 对象(NATION/TEAM/其它)、backing member、reader/集合;可闭合者走 cursor+三重闸门晋级,不可闭合者给出**加固过的诚实 negative**。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;negative 原样保留;候选不写结论;L4=0)
- scratch/t47/out/discovery_nation_unknown.json(**真源**:6 个 parent 条目原样;extents 可复用;factory 表;t9_owner_fixup)
- scratch/t47/out/REPORT.md(**方法范本**:factory→slot→PE extent→ReaderCFG;五类分支;Ntxr 三重闸门表;Ntxr 负例记法)
- scratch/t39/out/REPORT.md(**TEAM 侧 helper 锚点**:`0x15e9830→0x44d7bf0`、全局 VA `0x141b60158` table `+0x80` vector、owner 筛选;NATION slot2 `0x1041f30→0x1041f40`)
- scratch/t37/out/nation_subtable_inventory.json(负例 baseline SHA 8af89c72,**原样保留不删改**)
- scratch/t49/out/REPORT.md(若已交付:member↔mode 绑定与 t9 游标成果可引用;**t51 不重复 t9 的 8 parent**)
- evidence/fm24/reports/editor_schema/master.json(nation.xml#nation,冻结 SHA 7d57477e 对照 MANIFEST)

## 目标 6 parent(t47 保留的首路径,原样不删,本任务推进或加固)
| parent | idx | items | t47 首路径/负例(verbatim) |
|---|---:|---|---|
| Nrvn | 216 | nati,leve | 12 sites(17196454/17196460/17200624/17214736/64577402/64577421/64577429/18778368/65774480/65774484/65774555/65774568);"constructed wrapper: filters 16 B objects in current container +48/+50 on item +b == 6; reader/fill source not yet proven" |
| Nftb | 234 | NbPi,NpFn,NpSn,NbPd,NbPn,NbFt,NbCn | debug_only=true;6 sites;"setter-shaped import route with posl code lookup; no getter/storage proof" |
| Calt | 235 | cmid,stid(nested 另有 year,cate 等 6) | 5 sites;"Team-container candidates; name match alone does not join NATION storage or a member" |
| TCrs | 64 | PUnI,PUnT,PUnP,PUnJ | 6 sites;"Team-container candidates; source vector/reader not proven" |
| EDfx | 342 | date,day_of_week,time,stadium_rules,text,highest_division_level,lowest_division_level | 0 sites;"only reversed raw immediate at file 0x29c39; no reachable exact getter proven" |
| EDsc | 344 | date,day_of_week,time,stadium_rules,competition,text | 0 sites;"neither raw 4CC byte order in editor PE; computed or resource route not excluded" |

**owner 判定优先**:Calt/TCrs 的 t47 sites 指向 Team-container 候选——先判定它们究竟挂在 NATION、TEAM 还是两处各有独立集合,再谈 backing member,不凭名字相似断言。EDfx/EDsc/Nftb 可能是编辑器 UI 专用或 debug-only 不持久化——negative 合法,但须给出"不持久化"的静态证据链(如仅 UI 构造路径、无 archive 打开器、wire 无对应 member),**不是搜不到就算**。

## 任务
1. **owner/table_type 判定(逐 parent)**:从 t47 sites 出发建 xref,追每个调用点的上下文对象(this 来源);NATION slot2 `0x1041f30` 与 TEAM 侧 helper 都试;真源是调用上下文,不是 schema 名。
2. **发现 backing member**:4CC 分发→集合 helper→全局集合 table/分配池→entry vptr 或具名打开器→factory rel32 case **或**具名 `.dat` 成员;每跳 bytes+VA+指令分片。同簇共用或各自独立,如实判定。
3. **可闭合者走全链**:archive 双档 payload(count/stride/SHA,E80:data_base34+entry.offset、entry.size 选帧、entry.sha256=压缩区 SHA)→reader extent→ReaderCFG(t21b_control_flow.ReaderCFG)→cursor(wire13/legacy14 双坐标、selector 前置、identity 后置、footer count0/flag1/maxid 如实)→变长 t41 法/POD t44 法→三重闸门(frozen master 唯一 scoped occurrence→getter 4CC 精确分发→对象 member sink)→**target ordinal join**(nati→nation、cmid→competition、stid→stadium、PUnP→person、NbPi/NbPn/NbFt 走目标实表实际 ordinal 集,非 public UID)。enum 域(day_of_week、nstr、ftjn)冲突 held 留首反例;bool 验 bitmask(t31/t44 法);date packed 如实。
4. **negative 加固**:对判定不持久化/UI-only 的,写明证据链与首反例;t37/t47 负例原文不删不改。
5. 五类分支(wire_data/runtime-external/IO-result/context-lifecycle/dead)逐条证据+首反例;独立 verify.py(**不 import builder/ReaderCFG/fm24_dump**)+ builder scripts/t51_nation_unknown2.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只这 6 parent;**不碰** t47 已闭 9(Ntxr+Nntp/Nctp/Nrtp/NTRv/NWGv/NSps/Nfmp/NCro)、t28 已闭 4(Nagr/Nefr/Nnfr/Nlns)、Tchl(t34)、club 子表、zero-item schema。
- 候选不写结论;t37/t47 negative/held/baseline 原样保留;L4=0;不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。
- 预算内无法全闭则诚实 partial:已判定 owner+已发现链接+已闭合子集+剩余+首反例。**优先级:Nrvn(12 sites 最成熟)→Calt/TCrs(owner 判定)→Nftb→EDfx/EDsc。**

## 交付 scratch/t51/out/
- discovery_unknown2.json(逐 parent:owner 判定+member/reader 静态链或 negative 加固)、cursor_*.json/fields_*.json(闭合者)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t51_nation_unknown2.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t51/ 与 scripts/t51_*.py;完成跑 verify + t01_anchors.py(7/7)。
