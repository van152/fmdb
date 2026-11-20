# t63 — Club 主行 unmapped 第二轮深度普查(sol;t57 方法加深:t59 cnst 投影范式迁移)

你是受指挥官委派的子代理。t57(E97)club table_3 主行 433 occurrence 中 **399 unmapped**。t59(E99)在 comp 侧开创了两个新范式并验证:①**本地 getter 投影**(22 个 cnst 契约状态投影:顶层 getter 调 helper,精确比较/bit-test gate + helper rel32 + 逐 byte cursor,值域=scoped 枚举子集);②**byte 位投影**(cext/cusn/culn 同一 +0x1a1 byte 的 bit 2/0/6,由 getter 的 shr/and 证明)。本任务把两个范式迁移到 club 主行,对 399 unmapped 做第二轮普查。

## 必读
- AGENTS.md;scratch/t57/out/field_slots.json + field_map.json + REPORT.md(**club 行框唯一来源**:client 6,932,082/server 16,595,312,84,259×2,identity 12B,34 位置,slot19 0xe5a7a0 1,412 指令/167 分支)
- scratch/t59/out/REPORT.md(**范式范本**:cnst 投影的 gate/helper/cursor 证据结构、bit 投影的 shr/and 证明、wrong-UID 控制例、LAUC uoct 检查)
- scratch/t59/out/field_map.json(comp 侧 L3 记录形态对照)
- reports/club_nation_subtable_schema.json(v8/v9 以实际为准;club_main_row_fields 原样,不重做已闭)
- evidence/fm24/reports/editor_schema/master.json(club.xml 433 字段冻结)

## 任务
1. **投影扫描**:club 主 reader extent 内(+相关 helper 区)枚举"比较器/位测试 gate → helper rel32 → cursor 逐 byte"三元组,对齐 unmapped XML occurrence(case-sensitive 4CC/同对象成员,不按 XML 序号);每个候选给:gate 指令、helper 格、cursor 路径、对象位移。
2. **全档域检验**:84,259 行双档全量(可向量化),值域 vs XML min/max/enum_ref;bit 投影给 0/1 直方图;引用字段走目标实表 ordinal 集;wrong-UID 控制例;t01 夹具回归(Liverpool/Bernabéu/成立年)必须复洽。
3. **过闸 L3;不过留 held+首反例**;已知 held(11)不重判,但其证据若被新发现推翻需引用旧条目说明(negative 不删)。
4. 优先级:状态/日期簇(类比 cnst)→ 引用簇 → 数值域宽的字段 → 字符串槽不猜(照 t59 cnam/csnm 口径)。
5. 独立 verify.py(不 import builder/ReaderCFG/fm24_dump)+ builder scripts/t63_club_unmapped_r2.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 club 主行 unmapped/剩余层;不重做 8 子表/CLUB_LINK/t57 已闭 L3/nation/comp;不碰 person/PDxx;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 84,259 行:全档统计可向量化,L3 判定不得抽样代替全档。

## 交付 scratch/t63/out/
- projections.json(三元组台账)、field_map_r2.json(增量 grades,引用 r1 id)、verify.py、REPORT.md、DONE.md;scripts/t63_club_unmapped_r2.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
