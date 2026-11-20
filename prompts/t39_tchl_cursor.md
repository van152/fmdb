# t39 — Tchl 杯赛历史子表 cursor 闭合(t27/t30/t31/t32/t34/t36 方法复制)

你是受指挥官委派的子代理。club 子表 branch-aware cursor 方法已六次证实(t27 Cstc14/t30 Clhs8/t31 CSrs10/10/t32 Cmti5+1held/t34 CNtp2+2held/t36 Cdbt5/5,累计 44 L3)。本任务复制到 **Tchl(杯赛历史),table_type=34**。静态攻坚,晋级 L3。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- <WORKSPACE>\scratch\t27\out\replication.md(方法模板;§3 Tchl 行:stride44,club/nation 未排他,见 t13d 伪帧反例)
- <WORKSPACE>\scratch\t36\out\cursor_cdbt.json + fields_cdbt.json + scratch\t32\out\REPORT.md(**最新范例**;record-key i32 pair vs 单 lane identity 逐 read site 判定、packed day/year、float32 real、contextual 坐标、leaf thunk→真 reader+identity tail 双 extent)
- <WORKSPACE>\scratch\t33\out\profiles\table_server_34.profile.json + .rows.jsonl(**数据侧画像,直接消费**)+ scratch\t29\out\profiles\table_server_34.profile.json(t29 先例)
- <WORKSPACE>\scratch\t24\out\subtables.part00*.json(Tchl 9 个 nested occurrence idx562–570)
- evidence/fm24/reports/editor_schema/master.json(club.xml Tchl.list_item_fields,冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点
- Parent `Tchl`,table_id **34**,RTTI `STARTING_TEAM_CUP_HISTORY`,reader VA `0x14156f9d0`(t05_pe.PE.va2f;可能 leaf thunk,追真 reader),schema **9 字段**,stride **44 B**,count **7115**(t29/t33 实测)。
- **多帧成员(E66 关键)**:server table34 含空 stub 首帧(12B,count=0)+ 真实第二帧(**313082B**,SHA a07b2bb7...,相对偏移 +34)。`load_payload` 取首帧会返回 12B 空!**用目录 entry["size"]=313082 选真实帧**(参 scripts/t38_multiframe.py 若已交付,或 scratch/cmd/t29b_spot.py pick_frame;packed_size 界定边界)。client 无 table34 如实记。
- 9 个 item 字段(t24 idx562–570):**tchc**(Competition,ref,optional)、**styr**(Start Year,integer,required)、**edyr**(End Year,integer,required)、**mstn**(Last Stage,ref,optional)、**sstn**(Last Sub-Stage,ref,optional)、**dbrt**(Result,enum,optional)、**posi**(Position Achieved,integer,optional)、**cquf**(Competition Qualified For,ref,optional)、**tcop**(Opposition,ref,optional)。
- **club/nation 排他 blocker(t13d 伪帧反例)**:Tchl 的 table34 配对除 Cstc 外仍为候选,名称相近项可能 club/nation 共享。先验证 table34 是否 club 专属(沿 factory case34 + getter 4CC 分发 + entity_tag),若 nation 也引用同表则如实标 shared/ambiguous,不妄断 parent 独占。
- 5 个 ref 字段(tchc/mstn/sstn/cquf/tcop)目标各异(competition/stage/sub-stage/competition/opposition club?)。逐 read site 判定 u32 ordinal vs i32 pair(t32 E69)vs 单 lane identity(t34 E71);走各目标表实际 ordinal/identity 域,不预设。styr/edyr 是 year integer(非 packed date,注意区别);posi integer 可能 signed i8 sentinel(参 t30)。

## 任务(同 t36)
1. 两 archive 目录+payload(**多帧选 size=313082 真实帧**):table34 client/server count/stride/SHA。
2. factory→RTTI/vtable→slot19→真 reader(+identity tail),PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk,保存 bytes+VA。
3. 分支五分类逐条证据+首行反例;caller mode 条件则 fork 全表跑,无则注明。
4. walk 逐行闭合 `13+7115*44+9==313082`(核实);双坐标(legacy14/wire13);identity 后置校验;selector 全表观察。
5. 三重闸门:唯一 scoped occurrence→getter 4CC 分发+object 成员→实际 wire sink;全表独立画像。ref 走目标表域;year integer 域;enum 值集;posi signed/sentinel。club/nation 排他证据落盘。9 字段可证实者 L3,域冲突/视角派生/shared held 保留首反例。
6. 独立 verify.py(不 import builder,ROOT=parents[2],**多帧选帧**)+ builder scripts/t39_tchl_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 Tchl/table34;不碰已闭 Cstc/Clhs/CSrs/Cmti/CNtp/Cdbt;Cafl/Cvfl 另案。
- 候选不写结论;negative/held 反例保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 消费 t29/t33 画像;预算内无法闭合则诚实 partial+已绑定子集+剩余+首反例。

## 交付 scratch/t39/out/
- cursor_tchl.json、fields_tchl.json(9 字段台账+grade)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t39_tchl_cursor.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;只写 scratch/t39/ 与 scripts/t39_*.py;完成跑 verify + t01_anchors.py(7/7)。