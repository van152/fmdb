# t36 — Cdbt 俱乐部债务子表 cursor 闭合(t27/t30/t31/t32 方法复制)

你是受指挥官委派的子代理。club 子表 branch-aware cursor 方法已四次证实(t27 Cstc 14 / t30 Clhs 8 / t31 CSrs 10/10 / t32 Cmti 5+1held,累计 37 L3)。本任务复制到 **Cdbt(俱乐部债务),table_type=33**。静态攻坚,晋级 L3。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束)
- D:\tmp2b\fm24-db\scratch\t27\out\replication.md(方法模板)
- D:\tmp2b\fm24-db\scratch\t32\out\REPORT.md + scripts\t32_cmti_cursor.py + scratch\t32\out\verify.py(**最新范例**;record-key i32 pair 模型、contextual 坐标、leaf thunk→真 reader+identity tail 双 extent、footer 末 u32 不妄断)
- D:\tmp2b\fm24-db\scratch\t30\out\REPORT.md(**packed day/year 日期手法**;stdt/endt 必用)
- D:\tmp2b\fm24-db\scratch\t29\out\profiles\table_server_33.profile.json + .rows.jsonl(**数据侧画像,直接消费不重 dump**)+ subtable_inventory.json(Cdbt 页)
- D:\tmp2b\fm24-db\scratch\t24\out\subtables.part00*.json(Cdbt 5 个 nested occurrence idx188–192)
- evidence/fm24/reports/editor_schema/master.json(club.xml Cdbt.list_item_fields,冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点
- Parent `Cdbt`,table_id **33**,RTTI `STARTING_CLUB_DEBT`,reader VA `0x141535af0`(t05_pe.PE.va2f;可能 leaf thunk,追真 reader),schema **5 字段**,stride **79 B**,count **32409**(t29 实测;闭合 13+32409×79+9=2560333 已核)。
- 5 个 item 字段(t24 idx188–192):**cash**(Original Debt,cash,required)、**sour**(Source,enum,required)、**stdt**(Start Date,date,required)、**endt**(End Date,date,required)、**inrt**(Interest Rate,real,optional)。
- **stride79 偏大警示**:5 字段 properties 区约 66B(=79-1selector-12identity),远超 cash8+date4+date4+real4/8+enum 的朴素和。可能含成对 record-key i32(参 t32 E69)、contextual 坐标、或额外 identity/对齐。**逐 read site 归纳宽度与 sink,不预设 stride 拆分**;若发现视角派生/无独立 wire sink 字段,held 保留首反例(参 t32 icom)。
- stdt/endt 必须落 packed day/year 画像(两 u16=day,year 或 high16 year/low9 day-of-year/mid7 zero,year 1850–2100/day 1–366),不要只看"值像日期"。inrt real 注意 float32/float64 与定点表示区别。cash 落合理金额域。
- 多 zstd 帧:若 load_payload 空/异常短,查空 stub 首帧(E66),用 profile packed_offset。

## 任务(同 t32)
1. 两 archive 目录+payload:table33 client/server count/stride/SHA;client 无成员如实记。
2. factory→RTTI/vtable→slot19→真 reader(+identity tail),PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk,保存 bytes+VA。
3. 分支五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead)逐条证据+首行反例;caller mode 条件则 fork 全表跑,无则注明。
4. walk 逐行闭合 `header+Σrow+footer==payload_len`;双坐标(legacy 14/wire 13);identity 后置校验(lane0=ordinal,后两 lane 相等非零);selector 全表观察。
5. 三重闸门:唯一 scoped occurrence→getter 4CC 分发+object 成员→实际 wire sink;全表独立画像。date 走 packed day/year;cash 金额域;sour enum 值集;inrt real 表示;引用(若有)走目标表实际 ordinal/identity 域或 t32 pair 模型。5 字段可证实者 L3,域冲突/视角派生 held 保留首反例。
6. 独立 verify.py(不 import builder,ROOT=parents[2] 指向 fm24-db)+ builder scripts/t36_cdbt_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 Cdbt/table33;不碰已闭 Cstc/Clhs/CSrs/Cmti;Cafl/Cvfl 另案(luna t35)。
- 候选不写结论;negative/held 反例保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 消费 t29 画像;预算内无法闭合则诚实 partial+已绑定子集+剩余+首反例。

## 交付 scratch/t36/out/
- cursor_cdbt.json、fields_cdbt.json(5 字段台账+grade)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t36_cdbt_cursor.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t36/ 与 scripts/t36_*.py;完成跑 verify + t01_anchors.py(7/7)。