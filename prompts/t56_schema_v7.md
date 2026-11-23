# t56 — Schema v6→v7 合并:t55 nation 主行字段普查并入(luna)

你是受指挥官委派的子代理,做**谨慎的合并**任务。当前公共 schema 为 **v6**(E95)。t55(E94,**L3 验收**)完成 nation table_10 主行槽位普查,本任务并入为 **v7**,保护节 verbatim 只做增量:

1. **nation 主行字段层**(t55):新增 `nation_main_row_fields` 节——外层序列闭合(server 40/client 15 位置,992 指令 CFG);346 顶层字段中 15 对齐(4.34%),**5 L3**(Nnsi→t21 Stadium 208/0/43、Ncti→t5 Continent 228/0/23、Nrgi→t19 Region 234/0/17、Ncur→t41 Currency 229/0/22、Nndn u16 0x0200 掩码 239/12);held:Necf/Nygn(域冲突+首反例)、Ngct/Nsod(无 scoped enum_ref)、Npop(不在活动 schema)、EDsc(no_main_wire_slot)、Nftb(linked_parent_held)、prior_collection 5、prior_identity 1、unmapped 327。
2. **顺序口径**:46 对 wire↔XML 顺序倒置(首例 wire pos1 Nnsi 先于 pos15 Ncti,XML 21>16)→ 在 `nation_coverage_policy` 追加"wire 顺序≠XML 顺序,后续映射不得按 XML 序号对齐"。
3. **t46 A/B/C/D 收口**:A=Nlns(1+5a)/B=Nefr(4+28b)/C=Nnfr(4+28c)/D=Nagr(4+12d),双档 count/消费逐行一致;原 t46 文字与负例不动,新增 abc 解释引用。
4. coverage nation 计数:L3 occurrences 30→**35**(t55 的 5 个 main-row id 与既有 30 无重叠;unique ids 列表追加);held/均按 grade_counts 如实;`incremental_provenance.tasks` 增 t55(E94,**level L3**——条目级守卫引用)。

## 必读
- AGENTS.md;reports/club_nation_subtable_schema.json+.md(**v6 基线**,E95)
- scratch/t55/out/field_slots.json + field_map.json + abc_closure.json + REPORT.md + DONE.md
- scratch/t54/out/consolidate_v6.py + verify.py(**方法复刻**;**ledger 守卫必须用 t54-fix1 的条目级口径**:逐条 id+claim SHA+kind/level,不钉全文件)
- scratch/t01/LEDGER.json(E87–E94)

## 任务
1. `schema_version: 7`;按上述增量;`tables` 8 表、`negative_regressions`、`v3_baseline`、`club_auxiliary_sources`、club 计数、`nation_static_side`、`nation_t9_wire`(含 t53 节)**verbatim 不动**。
2. markdown 同步;json/md 数字自洽;独立 spot 脚本(条目级守卫+v5/v6 快照 SHA+保护节+t55 数字断言);anchors 7/7;--help/--selftest;退出码 0/1/2。
3. 候选不写结论;t55 held/unmapped 原样;不改 scratch/t47–t55 任何文件;BASELINE.md 指挥官另行。

## 交付 scratch/t56/out/
- consolidate_v7.py、verify.py、spot_*.log、REPORT.md、DONE.md;reports/ 两文件升 v7

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + t01_anchors.py(7/7)。
