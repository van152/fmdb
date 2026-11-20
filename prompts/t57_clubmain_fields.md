# t57 — Club table_3 主行字段槽位普查(reader CFG 批量法,sol;复刻 t55)

你是受指挥官委派的子代理,负责**最难**的批量字段映射任务。t55(E94)已把 nation table_10 的方法跑通:slot19 reader extent→可达 CFG→**按执行顺序枚举 wire 站点**(40/15 位置)→XML 对齐(15/346,46 倒置如实)→实档域批量检验→5 L3/4 held/327 unmapped。本任务把同一方法应用到 **club table_3**(433 个 club.xml 顶层字段,目前仅 9 命名;84,259 server 行)。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;候选不写结论;negative 原样保留;L4=0)
- scratch/t55/out/field_slots.json + field_map.json + REPORT.md(**方法范本与口径**:execution_index、46 倒置不硬配、域检验+首反例、held 口径、回归要求)
- scratch/t39/out/REPORT.md(**CLUB 锚点**:slot2 `0x1041f30?` 以 t39 实际记载为准;club 集合 helper `0x15e9830→0x44d7bf0`、全局 VA `0x141b60158`)
- scratch/t44/out/REPORT.md + discovery_cafl_cvfl.json(**CLUB slot2 `0xe89a00` 4CC 精确分发**、club `+0x118/+0x120` vector、CLUB_LINK 具名打开器法)
- scratch/t27/out/replication.md(cursor 方法模板)、reports/club_nation_subtable_schema.json(v6:8 个 club 子表已闭,**不要重做**)
- evidence/fm24/reports/editor_schema/master.json(club.xml#club 433 字段,冻结 SHA 7d57477e)
- scratch/t01f(reports/t01f_comp_row_offsets.json)+ t01_anchors.py(L2 回归夹具:Liverpool 坐标、Bernabéu 81,044、成立年等——**必须全部复洽**)

## 任务
1. **定位 club 主 reader**:factory rel32 表 case 3(类比 nation case10 `0xf48f27`)→CLUB 容器构造→slot19 reader extent;PE exception extent→ReaderCFG(t21b_control_flow.ReaderCFG)。club 主表行框:table_3.dat 双档 payload+count(84,259?)+identity tail 结构先由数据侧自证(13B tail 假设须按 t50 敏感性口径检验,不得照抄 nation),闭合判据 `header+Σrow+footer==payload_len` + identity census(ordinal 0..N-1、row_id 非零递增唯一)。
2. **CFG 站点普查**:按实档执行顺序枚举外层 wire 站点(类型/位移/4CC);`field_slots.json` 有序槽位表。已闭子表集合(8 表)与 CLUB_LINK 按已验口径标注跳过。client/server 站点数差异如实(client 行更短)。
3. **XML 对齐**:与 club.xml 433 字段对齐(4CC/同对象成员证据,**不按 XML 序号**);倒置如实记。
4. **实档域批量检验**:84,259 行抽样全档值域 vs XML min/max/enum_ref;引用字段(city/t2、stadium/t21、nation/t10、comp/t25、club 自引用)走目标实表实际 ordinal 集;**t01 夹具回归**(Liverpool/Bernabéu/成立年等必须命中,冲突=映射有错先自查)。过闸门 L3,否则 held 留首反例。
5. 独立 verify.py(不 import builder/ReaderCFG/fm24_dump)+ builder scripts/t57_clubmain_fields.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 club 主行(table_3);**不重做** 8 个已闭子表、CLUB_LINK、nation 侧;不碰 t44/t39 已闭结论;negative/held 原样保留。
- 84,259 行规模:全档统计允许向量化/分块,但**不得抽样代替全档**做 L3 判定(domain 判定须全档);identity census 全量。
- 候选不写结论;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 预算内无法全闭则诚实 partial:槽位普查完成度+已晋级子集+剩余+首反例。**优先级:行框闭合→CFG 普查→对齐→高值字段(坐标/容量/成立年/引用簇)→其余。**

## 交付 scratch/t57/out/
- field_slots.json、field_map.json、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t57_clubmain_fields.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t57/ 与 scripts/t57_*.py;完成跑 verify + t01_anchors.py(7/7)。
