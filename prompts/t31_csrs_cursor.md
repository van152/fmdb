# t31 — CSrs 预备队子表 cursor 闭合(t27/t30 方法复制)

你是受指挥官委派的子代理。t27(stadium)、t30(Clhs 联赛史 46 万行)已证实 club 子表 branch-aware cursor 方法可复制。本任务复制到 **CSrs(预备队),table_type=62**。静态攻坚,晋级 L3。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- <WORKSPACE>\scratch\t27\out\replication.md(方法模板:§1 分支五分类、§2 walk 模板、§3 scout)
- <WORKSPACE>\scratch\t30\out\REPORT.md + scripts\t30_clhs_cursor.py + scratch\t30\out\verify.py(**最新复制范例**,定长子表全表 walk+独立 verify;注意有符号 i8 sentinel、footer 末 u32 可能是 max UID 非行数、slot19 跳板→真 reader)
- <WORKSPACE>\scratch\t29\out\profiles\table_server_62.profile.json + .rows.jsonl(**数据侧画像,直接消费不重 dump**;若 inventory 已交付一并读)
- <WORKSPACE>\scratch\t24\out\subtables.part00*.json(CSrs 的 10 个 nested schema occurrence,idx)
- evidence/fm24/reports/editor_schema/master.json(club.xml CSrs.list_item_fields,冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点(t27 scout)
- Parent `CSrs`,table_id **62**,RTTI `STARTING_RESERVE_TEAM`,reader VA `0x14119c960`(t05_pe.PE.va2f 换 file offset;可能是跳板,追到真 reader),schema 10 字段,stride **~42 B**(t13d 算术候选,需自证封口)。

## 任务(同 t30)
1. 两 archive 目录+payload:table62 client/server 各自 count/stride/SHA;client 若无成员如实记(不搬偏移)。
2. factory→RTTI/vtable→slot19→真 reader,PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk,保存原 bytes+VA。
3. 分支按谓词来源五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead),逐条证据+首行反例;未知外部值 fork 全表跑。
4. walk 逐行闭合 `header+Σrow+footer==payload_len`;双坐标(legacy 14/wire 13);identity 后置校验(lane0=ordinal,后两 lane 相等);selector 全表观察。
5. 三重闸门晋级:唯一 scoped occurrence→getter 4CC 分发+object 成员→实际 wire sink;全表独立画像(注意有符号 i8/i16 与 sentinel -1/0 的区别,引用走目标表 ordinal 域,date 才用 packed day/year)。10 字段可证实者 L3,域冲突 held 保留首个反例,不硬凑。
6. 独立 verify.py(不 import builder,重读归档+静态字节/VA+全表画像+抽样)+ builder scripts/t31_csrs_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 CSrs/table62;不碰已闭 Cstc/Clhs;Cafl/Cvfl 双视图另案。
- 候选不写结论;negative/held 反例原样保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 消费 t29 画像;若未交付自行 dump(fm24_dump.py,FM24_DB_DIR=<WORKSPACE>/scratch/data)。
- 预算内无法闭合则诚实 partial+已绑定子集+剩余清单+首个反例。

## 交付 scratch/t31/out/
- cursor_csrs.json、fields_csrs.json(10 字段台账+grade)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md(一句话状态+晋级数)
- scripts/t31_csrs_cursor.py

Python `py -V:3.12 -I -B`;只写 scratch/t31/ 与 scripts/t31_*.py;完成后跑 verify + t01_anchors.py(7/7)。