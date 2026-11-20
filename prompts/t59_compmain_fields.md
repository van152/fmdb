# t59 — Comp table_25 主行字段槽位普查(reader CFG 批量法,sol;复刻 t55/t57)

你是受指挥官委派的子代理,负责**最难**的批量字段映射任务。t55(nation,346 字段,E94)与 t57(club,433 字段,E97)已跑通全链:factory case→slot19 extent→ReaderCFG→按执行顺序枚举 wire 站点→XML 对齐(倒置如实)→实档域批量检验→L3/held。本任务应用到 **comp table_25**(comp.xml 255 个顶层字段;server 行数按 t13e 基数 7,047)。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;候选不写结论;negative 原样保留;L4=0)
- scratch/t55/out/REPORT.md + scratch/t57/out/REPORT.md(**方法范本**:execution_index、倒置不硬配、域检验+首反例、held 口径、t01 夹具回归)
- scratch/t57/out/REPORT.md 行框节(**identity/footer 宽度按表自证**:nation 13B、club 12B——comp 不得照抄,须数据+reader 双证)
- evidence/fm24/reports/editor_schema/master.json(comp.xml 255 字段,冻结 SHA 7d57477e)
- reports/t01f_comp_row_offsets.json(**comp packed 区既有锚点**:table_25 client 行 +0..51/+68..113 槽位、六大洲 0..5、parent row 352 等 L2 夹具——**必须全部复洽**)
- scratch/t01_anchors.py(A3/A4 comp 锚:slot6=0x140ebfa40、switch 67 cases)、t01f 报告
- scratch/t44/out/REPORT.md(CAFl/Cvfl=CLUB_LINK 共享 auxiliary,与 comp 无关但别混淆 4CC)

## 任务
1. **定位 comp 主 reader**:factory rel32 case 25(表身份 tier:comp=table_25 已 confirmed)→COMP 容器构造→slot19 reader extent→ReaderCFG;行框双档闭合(header+Σrow+footer==payload_len;identity census ordinal 0..N-1 非零递增唯一;identity/footer 宽度数据+reader 双证,敏感性表照 t57 口径)。
2. **CFG 站点普查**:按实档执行顺序枚举外层站点;`field_slots.json` 有序槽位表;已闭集合(packed 区 t01f 已验槽位、既有锚)标注;client/server 站点差异如实。
3. **XML 对齐**:与 comp.xml 255 字段对齐(4CC/同对象成员,**不按 XML 序号**);倒置如实记。
4. **实档域批量检验**:全档值域 vs XML min/max/enum_ref;引用字段(nation/t10、club/t3、stadium/t21、city/t2、comp 自引用)走目标实表实际 ordinal 集;t01f 槽位与六大洲/parent352 夹具必须复洽,冲突先自查。过闸 L3,否则 held 留首反例。
5. 独立 verify.py(不 import builder/ReaderCFG/fm24_dump)+ builder scripts/t59_compmain_fields.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 comp 主行(table_25);不碰 club/nation 已闭层、CLUB_LINK、subtables;negative/held 原样保留。
- 候选不写结论;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 预算内无法全闭则诚实 partial。**优先级:行框闭合→CFG 普查→对齐→高值字段(引用/日期/状态簇)→其余。** 7,047 行规模:全档统计允许向量化,L3 判定不得抽样代替全档。

## 交付 scratch/t59/out/
- field_slots.json、field_map.json、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t59_compmain_fields.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t59/ 与 scripts/t59_*.py;完成跑 verify + t01_anchors.py(7/7)。
