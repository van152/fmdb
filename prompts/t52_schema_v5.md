# t52 — Schema v4→v5 合并:nation 静态/数据侧成果并入总 schema(luna)

你是受指挥官委派的子代理,做**谨慎的合并**任务(非发现任务)。club_nation_subtable_schema 目前为 **v4**(8 numbered 表 + CLUB_LINK auxiliary;club 94 scoped L3/59 unique wire/21 held/4 negative;`nation_data_side_status` 已并 t46 server table_10 数据侧)。v4 scope 早于 t47,所以 nation_side 静态成果 **new_L3=0 未并**。本任务把以下成果并成 **v5**,全部保留 v4 既有内容 verbatim(不删不改不改写),只做**增量**:

1. **t47(E87)**:nation Ntxr 稳定闭合 —— item 相对偏移 7 L3(lowa/uppa/capa/year/perc/fram/leve)+ 2 held(ppty/txty),1889 item 全档 closure,双档 server mode1/client mode0;以及 nation 15 unknown parent 静态发现总图(9 连/6 unknown,t9_owner_fixup)。
2. **t49(E89,已验收)**:t9 NATIONAL_TEAM_CONTAINER 双档 wire 验收 —— table_9 client mode0/server mode1 各 251 行闭合;逐 parent(Nntp/Nctp/Nrtp/NTRv/NWGv/NSps/Nfmp/NCro)item 字段 grade(以 scratch/t49/out/fields_*.json 为准,17 L3/13 held);sidecar table_extra_9 未绑(6 拒绝记录)如实记 open 负例。
3. **t51(E90,已验收)**:Nrvn→t9(nati/leve L3,720 项)、Nftb→t10 row162(NpFn/NpSn/NbCn/NbPd L3=4,引用 held)、Calt→t9 owner 证实(251 零 count,held)、TCrs 候选 sidecar 未绑(partial)、EDfx UI 路径负例、EDsc unresolved;并记 **cross-walk 交叉验证**:t51/t49/t47 三方 row 边界+逐行 wire SHA 完全一致(独立重walk)。
4. **t50(未交付,dispatch 时仍在跑)**:按 pending 如实记,**不虚构、不占位定稿**;若指挥官附言说明已交付则以其 REPORT.md 为准并入。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;候选不写结论;negative/held 原样保留;L4=0)
- reports/club_nation_subtable_schema.json + .md(**v4 基线**,合并基底)
- scratch/t47/out/discovery_nation_unknown.json + fields_nation_tax.json + cursor_nation_tax.json + REPORT.md
- scratch/t49/out/(REPORT.md + fields_*.json + discovery_t9_wire.json,已提交 77f85b6)
- scratch/t51/out/(REPORT.md + discovery_unknown2.json + fields_*.json + cursor_table_*.json,已提交 c57c046)
- scratch/t50/out/(REPORT.md + profile_t9.json + grammar_diff_t9.json,**交付时存在才并入**)
- scratch/t48/out/consolidate_v4.py + verify.py(v4 合并脚本范例,**方法复刻但内容重写**)
- scratch/t01/LEDGER.json(E84–E89 相关条目,作为 provenance 引用)

## 任务
1. 结构:`schema_version: 5`;新增 `nation_static_side`(t47 Ntxr 7 L3 + 2 held + 静态发现总图,含 item 相对偏移坐标口径说明)与 `nation_t9_wire`(t49 逐 parent 字段 grade + t50 L2 交叉验证;引用 out 文件名+关键 SHA);`coverage` 增量计数如实更新(club 侧计数**不得变动**;新增 nation_L3_occurrences/unique/held/negative 分项);`incremental_provenance` 增加 t47/t49/t50 条目(editor SHA b82ebe8e、各 payload SHA、LEDGER 条目号)。
2. `tables` 8 表与 `negative_regressions` 4 条、`v3_baseline`、`club_auxiliary_sources` **verbatim 不动**;`nation_data_side_status`(t46)verbatim 不动。
3. markdown 同步重生成(v4 md 为底,新增 nation 章节置于 club 章节后);机读 json 与 md 同名成对;数字必须自洽(逐处交叉核对,json 内计数与表格行数一致)。
4. 独立 spot 脚本(**不 import 合并逻辑,不 import builder**):独立读 v4 JSON(SHA 断言基底未变)+ 独立读 t47/t49/t50 out 文件,抽样 ≥20 项核对(含全部 7 个 Ntxr L3、t49 逐 parent 首字段、t50 closure 数字);t01_anchors.py 7/7;verify.py 独立;--help/--selftest;退出码 0/1/2。
5. 候选不写结论:凡 t49/t50 标 held/partial/negative 的,原样进 v5 对应等级,不得改写为 L3。

## 边界
- 只改 reports/club_nation_subtable_schema.json/.md(schema v5)与 scratch/t52/、scripts/t52_*.py;**不改** scratch/t47/t49/t51/t50 任何文件;不改 BASELINE.md(另行)。
- 不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:;L4=0。
- 若 t49/t50 尚未交付对应部分,按指挥官 dispatch 附言的实际清单合并,缺项如实记 pending,不虚构。

## 交付 scratch/t52/out/
- consolidate_v5.py(合并脚本)、verify.py(独立)、spot_*.log、REPORT.md、DONE.md;reports/ 两文件升级为 v5(指挥官验收后由指挥官提交)

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t52/、scripts/t52_*.py 与 reports/ 两文件;完成跑 verify + t01_anchors.py(7/7)。
