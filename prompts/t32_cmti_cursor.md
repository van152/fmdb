# t32 — Cmti 月供子表 cursor 闭合(t27/t30/t31 方法复制)

你是受指挥官委派的子代理。club 子表 branch-aware cursor 方法已四次证实(t27 stadium 14 L3 / t30 Clhs 8 / t31 CSrs 10/10 全晋级)。本任务复制到 **Cmti(月供/分期),table_type=43**。静态攻坚,晋级 L3。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- <WORKSPACE>\scratch\t27\out\replication.md(方法模板)
- <WORKSPACE>\scratch\t31\out\REPORT.md + scripts\t31_csrs_cursor.py + scratch\t31\out\verify.py(**最新范例,10/10 全晋级**;leaf thunk→真 reader+identity tail 双 extent、有符号 i8 sentinel、bool 同字节双掩码、ordinal 引用走目标表 ordinal 域、footer 末 u32 含义不妄断)
- <WORKSPACE>\scratch\t29\out\profiles\table_server_43.profile.json + .rows.jsonl(**数据侧画像,直接消费不重 dump**;若 subtable_inventory.json 已交付一并读)
- <WORKSPACE>\scratch\t24\out\subtables.part00*.json(Cmti 的 6 个 nested schema occurrence idx)
- evidence/fm24/reports/editor_schema/master.json(club.xml Cmti.list_item_fields,冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点
- Parent `Cmti`,table_id **43**,RTTI `STARTING_MONTHLY_INSTALLMENT`,reader VA `0x14153d0a0`(t05_pe.PE.va2f;可能 leaf thunk,追真 reader),schema 6 字段,stride **46 B**,count **535**(t29 实测)。
- 注意多 zstd 帧:若 load_payload 返回空/异常短 payload,查成员是否含空 stub 首帧(参 E66 table34 caveat),用 profile 的 packed_offset。

## 任务(同 t31)
1. 两 archive 目录+payload:table43 client/server count/stride/SHA;client 无成员如实记。
2. factory→RTTI/vtable→slot19→真 reader(+identity tail),PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk,保存 bytes+VA。
3. 分支五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead)逐条证据+首行反例;有 caller mode 条件则 fork 全表跑,无则注明(如 t31)。
4. walk 逐行闭合 `header+Σrow+footer==payload_len`;双坐标(legacy 14/wire 13);identity 后置校验(lane0=ordinal,后两 lane 相等非零);selector 全表观察。
5. 三重闸门:唯一 scoped occurrence→getter 4CC 分发+object 成员→实际 wire sink;全表独立画像(i8/i16/i32 有符号与 sentinel -1/0 区别,bool 掩码,ordinal 引用走目标表实际 ordinal 集,date 才 packed day/year)。6 字段可证实者 L3,域冲突 held 保留首个反例。
6. 独立 verify.py(不 import builder)+ builder scripts/t32_cmti_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 Cmti/table43;不碰已闭 Cstc/Clhs/CSrs;Cafl/Cvfl 另案。
- 候选不写结论;negative/held 反例保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 消费 t29 画像;预算内无法闭合则诚实 partial+已绑定子集+剩余+首反例。

## 交付 scratch/t32/out/
- cursor_cmti.json、fields_cmti.json(6 字段台账+grade)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t32_cmti_cursor.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;只写 scratch/t32/ 与 scripts/t32_*.py;完成跑 verify + t01_anchors.py(7/7)。