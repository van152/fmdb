# t49 — t9 NATIONAL_TEAM_CONTAINER 双档 wire 验收(t47 静态链→游标闭合)

你是受指挥官委派的子代理,负责**最难**的 wire 验收。t47(sol,E87 已接受)完成 nation 未知 item-bearing parent **静态发现**:15 目标中 9 连到内嵌集合+reader,其中 **8 个落在同一 t9 NATIONAL_TEAM_CONTAINER**(owner_type9),Ntxr 已单独闭合(t10,7 L3)。t47 **只证静态链,未做 t9 按档读游标、未绑 mode、未做 target ordinal join,故未发布任何 t9 item 的 L3 坐标或档内 item count**。本任务把这 8 条静态链推进到**双档 wire 验收**。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;negative 原样保留;候选不写结论;L4=0)
- scratch/t47/out/discovery_nation_unknown.json(**静态链真源**:parents 8 inline 的 reader/sites/collection/schema_index/list_item_fields;factory[9];extents;t9_owner_fixup)
- scratch/t47/out/REPORT.md + cursor_nation_tax.json(**游标方法范例**:Ntxr 双档 server mode1/client mode0、selector 前置、identity 后置、footer count0/flag1/maxid、五类分支+首反例、wrong_mode_first)
- scratch/t46/out/REPORT.md + grammar_diff_client_server.json(t10 数据侧 client/server row grammar 差异范例)
- scratch/t27/out/replication.md(cursor 方法模板)、scratch/t41/out/REPORT.md(变长 cursor)
- evidence/fm24/reports/editor_schema/master.json(nation.xml#nation,冻结 SHA 7d57477e 对照 MANIFEST)
- scratch/t37/out/nation_subtable_inventory.json(baseline SHA 8af89c72,**原样保留不删改**)

## 已知锚点(全来自 t47,PE file offset;editor.exe SHA b82ebe8e)
- t9 owner RTTI `.?AVNATIONAL_TEAM_CONTAINER@db@@`,factory 第 9 格 `0xf48b30`,vptr `VA 0x1418898d8`。slot19 reader **`0x105cb10`(=17156880,8 parent 共用)**按调用上下文版本+mode 分叉;slot2 `0x1065eb0→0x3d95190`(先试 +0x170 Nation,R9D=0,未命中进 `0x1065ef0`);slot20 `0x105fc60→0x3d885f0` 修复 +0x170,成功且非空 `0x3d88644` 写 `NATION[+0x108 + 8*container[+0xb9]]`,Nation 读选第 0 侧(**不声称 251 行 backlink 均选此侧**)。
- 成员(E80:绝对起点=`data_base(34)+entry.offset`,按 `entry.size` 选帧,`entry.sha256`=压缩区 SHA):
  - `table_9.dat`:client 31956 B / server 307564 B;tad shell `03017461642ef10d` + u32 count@8=251。
  - `table_extra_9.dat`:client 83927 B / server 105228 B;同 shell + count@8=251。
  - `table_extra_10.dat`:两档**缺失**。
- **8 parent 静态链**(reader 均 0x105cb10;member 均记 table_9.dat 但 **mode 未绑、sidecar 未分配**;item_count 全 null):
  | parent | idx | item 字段 | 集合/对象 | count | item stride |
  |---|---|---|---|---|---|
  | Nntp | 224 | nati/rati/sckn/mina/maxa/affl | +0xf0/+0xf8,16B 对象 | i8 | 9B(reader 0x41ba910) |
  | Nctp | 225 | cont/rati/mina/maxa/affl | +0x108/+0x110,16B | i8 | 8B(0x41babb0) |
  | Nrtp | 226 | regi/rati/mina/maxa/affl | +0x120/+0x128,16B | i8 | 8B(**与 Nctp 共 item reader,不共 vector/count**) |
  | NTRv | 228 | repu/valu | +0x438 optional i32 array | u8 | 4(getter 合成 20 行,缺 array 置 0) |
  | NWGv | 229 | repu/valu | +0x440 optional i32 array | u8 | 4 |
  | NSps | 230 | repu/valu | +0x448 optional i32 array | u8 | 4 |
  | Nfmp | 233 | pers/desc/heig/side/perm/rtng | +0x6e0/+0x6e8 指针 vector | i16 | 9B(0x3d86430;首 lane 符号扩宽 qword 非零才 append) |
  | NCro | 231 | comp/crep | +0x4f8 nullable 指针 | 存在门槛+1B tag+i32 count | 9B wire(1+4+4) |

## 任务
1. **绑 member↔reader↔mode**:确定 table_9 与 table_extra_9 各自被哪条 reader 路径/mode 消费(主表 vs sidecar)。**不可仅凭 count=251、class、目录名把某子段绑到 sidecar**(t47 明戒)。按 t47 Ntxr 法:factory→slot19→PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 mode 分叉(0x103fae6/0x10409d3 类比),对每档每成员试 mode 0/1,逐行通过者 binds,错 mode 记首反例(invalid count@offset)。保存每跳 bytes+VA+指令分片。
2. **双档变长 row 游标**:对绑定的成员建 selector 前置游标,逐行闭合 `header + Σrow_len + footer == payload_len`(wire13/legacy14 双坐标,legacy 末 byte 借下一 selector/footer 首字节);identity 后置校验(ordinal==row、repeated lanes 相等、唯一性);footer 语义如实记(count/flag/maxid,**不外推**)。变长站点(i16/i32 count、长度前缀字符串、日期对、内嵌项)只用来推进游标,**不命名字段、不重复 t46 全列扫描**。
3. **逐 parent item 闭合 + 三重闸门**:在已框架的行内,按 t47 静态 displacement 定位每 parent 的 count+items,walk 逐 item EOF;三重闸门(frozen master 唯一 scoped occurrence→getter 4CC 精确分发+对象 member→实际 wire sink);**target ordinal join**:affl/nati/regi/cont/pers/comp 等引用走**目标表实际 ordinal 集**(club/t3、nation/t10、region 等真实表,非公开 UID),记 hit/miss+首反例。mina/maxa cash i32、rati/repu/valu/heig/rtng integer 域、sckn/desc/side/perm/crep 如实判;bool 验是否同字节 bitmask(t31/t44 法);enum 域冲突 held 留首反例。**不可由子项内存宽度推 member stride**(t47 明戒);repu wire count 为界**非 20×4 无条件消费**;transfer 三件共 reader 不共集合(Nntp 多一 byte transfer)。
4. 五类分支逐条证据+首反例(wire_data/runtime-external/IO-result/context-lifecycle/dead);全表画像;可证实者 L3,域冲突/无 enum 域 held。
5. 独立 verify.py(**不 import builder**)+ builder scripts/t49_nation_t9.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 t9 这 8 parent;不碰 Ntxr(t47 已闭)、不碰 t28 已闭 4 parent(Nagr/Nefr/Nnfr/Nlns)、不碰 Tchl(t34)。
- 6 unknown(Nftb/EDfx/EDsc/Nrvn/Calt/TCrs)另案,本任务不强行晋级。
- 候选不写结论;t37/t47 negative/held/baseline 原样保留;L4=0;不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。
- 预算内无法全闭则诚实 partial+已闭子集+剩余+首反例。**优先级:transfer 三件(Nntp/Nctp/Nrtp)+repu 三件(NTRv/NWGv/NSps)先闭(固定/i32 array 最简),再 Nfmp/NCro。**

## 交付 scratch/t49/out/
- discovery_t9_wire.json(member↔mode 绑定+静态链复核)、cursor_t9_*.json(双档游标)、fields_*.json(逐 parent 三重闸门+ordinal join+grades)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t49_nation_t9.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t49/ 与 scripts/t49_*.py;完成跑 verify + t01_anchors.py(7/7)。