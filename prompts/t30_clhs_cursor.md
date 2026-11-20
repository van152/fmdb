# t30 — Clhs 联赛史子表 cursor 闭合(t27 方法首次复制)

你是受指挥官委派的子代理。t27 已证明 club 子表 branch-aware cursor 方法可复制(验收 33/33 绿,Cstc 0→14 L3)。本任务把该方法**首次复制到 Clhs(联赛史)**,目标 table_type=37。这是静态攻坚,晋级 L3。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- <WORKSPACE>\scratch\t27\out\replication.md(**方法模板**,尤其 §1 分支五分类、§2 walk 模板、§3 scout 表)
- <WORKSPACE>\scripts\t27_stadium_cursor.py + scratch\t27\out\verify.py(builder/独立 verify 范例)
- <WORKSPACE>\scratch\t29\out\subtable_inventory.json + profiles/(**若已交付**:Clhs 的数据侧画像/候选列/stride 封口,直接消费,不重做)
- <WORKSPACE>\scratch\t24\out\subtables.part00*.json(Clhs 的 12 个 nested schema occurrence)
- evidence/fm24/reports/editor_schema/master.json(club.xml Clhs.list_item_fields=[year,orde,divi,posi,mxtm,poin,…],冻结 SHA 7d57477e 对照 MANIFEST)

## 已知锚点(t27 scout)
- Parent `Clhs`,table_id **37**,RTTI `STARTING_TEAM_LEAGUE_HISTORY`,reader VA `0x14119e7f0`(用 t05_pe.PE.va2f 换 file offset),schema 12 字段,stride **40 B**(t13d 来源,需自证封口)。
- item 语义:year/ordre/divi/posi/mxtm/poin = 年份/名次/级别/位置/最大积分/积分 → 强 integer/enum 画像目标;若有 date 列必须落 packed day/year。

## 任务(同 t27)
1. 两 archive 目录 + payload:table37 在 client/server 各自 count/stride/SHA;绝不因表号搬偏移。
2. factory→RTTI/vtable→slot19 reader,PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk 到真 consumer,保存原指令 bytes+VA。
3. 分支按谓词来源五分类(wire_data/runtime-external/IO-result/context-lifecycle/dead),逐条给证据;未知外部值 fork 后全表跑,失败路径要反例。
4. walk 模板逐行闭合:selector→transfer(宽+sink)→condition→identity 后置校验→footer;`header+Σrow+footer==payload_len`。双坐标(legacy 14 / wire 13)同记。
5. 三重闸门晋级:唯一 scoped schema occurrence → getter 4CC 分发+object 成员 → 实际路径 wire sink;全表独立画像验证。12 字段中可证实者 L3,其余 candidate/held,不硬凑。
6. 独立 verify.py(不 import builder,重读归档+静态字节/VA+全表画像+抽样)+ builder scripts/t30_clhs_cursor.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 Clhs/table37;不碰 Cstc(t27 已闭)、不碰 Cafl/Cvfl(双视图歧义,另案)。
- 候选不写结论;negative 原样保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 若 t29 画像未交付,自行 dump 画像(fm24_dump.py,FM24_DB_DIR=<WORKSPACE>/scratch/data),但优先消费 t29 成果避免重复。
- 预算内无法闭合则诚实 partial + 已绑定子集 + 剩余清单 + 首个反例。

## 交付 scratch/t30/out/
- cursor_clhs.json(CFG+分支分类+transfer 坐标+行封口)、fields_clhs.json(12 字段台账+grade)
- instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md(一句话状态+晋级数)
- scripts/t30_clhs_cursor.py

Python `py -V:3.12 -I -B`;只写 scratch/t30/ 与 scripts/t30_*.py;完成后跑 verify + t01_anchors.py(7/7)。