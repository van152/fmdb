# t34 — CNtp 转会偏好子表 cursor 闭合(t27/t30/t31/t32 方法复制)

你是受指挥官委派的子代理。club 子表 branch-aware cursor 方法已四次证实(t27 stadium 14 L3 / t30 Clhs 8 / t31 CSrs 10/10 / t32 Cmti 5+1held)。本任务复制到 **CNtp(转会偏好),table_type=66**。静态攻坚,晋级 L3。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束)
- D:\tmp2b\fm24-db\scratch\t27\out\replication.md(方法模板)
- D:\tmp2b\fm24-db\scratch\t32\out\REPORT.md + scripts\t32_cmti_cursor.py + scratch\t32\out\verify.py(**最新范例**;record-key i32 pair 模型、contextual 坐标、leaf thunk→真 reader+identity tail 双 extent、footer 末 u32 含义不妄断)
- D:\tmp2b\fm24-db\scratch\t31\out\REPORT.md(有符号 i8 sentinel、bool 同字节双掩码、ordinal 引用走目标表 ordinal 域)
- D:\tmp2b\fm24-db\scratch\t29\out\profiles\table_server_66.profile.json + .rows.jsonl(**数据侧画像,直接消费不重 dump**)+ scratch\t29\out\subtable_inventory.json(CNtp 页)
- D:\tmp2b\fm24-db\scratch\t24\out\subtables.part001.json(CNtp 的 4 个 nested schema occurrence idx 46–49)
- evidence/fm24/reports/editor_schema/master.json(club.xml CNtp.list_item_fields,冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点
- Parent `CNtp`,table_id **66**,RTTI `STARTING_CLUB_TRANSFER_PREFERENCE`,reader VA `0x141530120`(t05_pe.PE.va2f;可能 leaf thunk,追真 reader),schema **4 字段**,stride **24 B**,count **753**(t29 实测)。
- 4 个 item 字段(t24 idx46–49):**nati**(Nation,database_record_unique_id,optional,ref→nation)、**rati**(Rating,enum,optional)、**mina**(Minimum Age,integer,required)、**maxa**(Maximum Age,integer,required)。
- **t32 新模型警示**:Cmti 的引用不是简单 ordinal,而是**成对 record identity key(双 i32 lane,第二 lane 零则复制第一,key_basis=目标记录 identity +0xc/+0x10)**。nati 是 nation 引用,先验证它是 u32 ordinal 还是 i32 pair;沿 reader read site 宽度与 getter 对象成员判定,不预设。stride24 较小,properties 区可能仅 11B(=24-1selector-12identity),逐 read site 归纳。
- 多 zstd 帧:若 load_payload 返回空/异常短,查空 stub 首帧(E66 table34 caveat),用 profile packed_offset。

## 任务(同 t32)
1. 两 archive 目录+payload:table66 client/server count/stride/SHA;client 无成员如实记。
2. factory→RTTI/vtable→slot19→真 reader(+identity tail),PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk,保存 bytes+VA。
3. 分支五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead)逐条证据+首行反例;有 caller mode 条件则 fork 全表跑,无则注明。
4. walk 逐行闭合 `header+Σrow+footer==payload_len`;双坐标(legacy 14/wire 13);identity 后置校验(lane0=ordinal,后两 lane 相等非零);selector 全表观察。
5. 三重闸门:唯一 scoped occurrence→getter 4CC 分发+object 成员→实际 wire sink;全表独立画像。nati 引用走 nation 表实际 ordinal/identity 域(参 t32 pair 模型);rati enum 列值集;mina/maxa integer 域与 min≤max 关系(若反例保留不妄断);有符号 i8/i16 与 sentinel -1/0 区别,bool 掩码。4 字段可证实者 L3,域冲突/视角派生 held 保留首反例。
6. 独立 verify.py(不 import builder)+ builder scripts/t34_cntp_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 CNtp/table66;不碰已闭 Cstc/Clhs/CSrs/Cmti;Cafl/Cvfl 另案。
- 候选不写结论;negative/held 反例保留;L4=0;不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。
- 消费 t29 画像;预算内无法闭合则诚实 partial+已绑定子集+剩余+首反例。

## 交付 scratch/t34/out/
- cursor_cntp.json、fields_cntp.json(4 字段台账+grade)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t34_cntp_cursor.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t34/ 与 scripts/t34_*.py;完成跑 verify + t01_anchors.py(7/7)。