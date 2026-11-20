# t42 — club/nation 子表 schema v2(并 t39 Tchl + 补 master.json 冻结 SHA)

你是受指挥官委派的子代理。t40 已交付首份 consolidated schema(44 L3,6 表), commander 接受(E79)但记两处待补。本任务升级到 **v2**,闭合缺口。**只增量,不重写已接受字段**。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束;negative 原样保留不删改)
- reports/club_nation_subtable_schema.json + .md(**t40 你自己的 v1 产物,在此基础上增量**)
- scratch/t40/out/consolidate.py + verify.py(v1 builder/verifier,复用扩展)
- scratch/t39/out/fields_tchl.json + cursor_tchl.json + REPORT.md(**t39 Tchl 已接受 E78,7 L3+2 held**)
- scratch/t01/LEDGER.json(E78 t39 / E79 t40 接受记录)
- evidence/fm24/reports/editor_schema/master.json(冻结 SHA **7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda**,对照 evidence/MANIFEST.json)

## 任务(增量)
1. **并 t39 Tchl**:新增第 7 表 Tchl/table_type34/RTTI STARTING_TEAM_CUP_HISTORY,7 L3 字段(tchc/mstn/sstn/dbrt 双槽/posi/cquf/tcop)+ 2 held(styr/edyr,u16 年整数零值与 XML[1900,2100]域冲突,首反例 row28@1254/row2695@118604)。全 provenance 从 fields_tchl.json 抽(row_offset/wire_offset/width/interpretation/schema.idx/source_task=t39/reader VA 0x144511e90..0x14451206f)。server payload 313082 SHA a07b2bb7,count7115 stride44,closure 13+7115*44+9=313082;**club/nation 共用,7084 非空 owner 全指 table24 selector11 NATIONAL_TEAM,club 独占 L3=0**(记入 reference_domains/排他注记,不沿 entity_tag 作独占)。
2. **补 master.json 冻结 SHA**:binary_provenance(或新增 schema_provenance 节)显式记 master.json path + SHA 7d57477e... + MANIFEST 对照结果。
3. coverage 升级:club_tables 7、club_L3_fields **51**、held_fields 15(13+2)、negative_regressions 4 不变、L4=0。schema_version=2。
4. **保留 v1 全部 44 字段 + 13 held + 4 negative + 2 Cstc 非业务槽 verbatim**(不删不改写已有坐标/结论);nation 侧仍仅 t37 partial 上下文(0 新 L3)。
5. 交叉一致性:Tchl reference target(table24/25/23)ordinal 域消费 t37/t39 实证;跨表 offset 坐标政策一致。

## 边界
- 只增量 t39 + master.json SHA;不新解析、不跑游戏/编辑器/IDA、不联网、不读写 Z:。
- 候选/held 不升级;negative 原样保留;L4=0。
- 只写 scratch/t42/ 与 reports/club_nation_subtable_schema.{json,md}(v2 in-place,你自己产物演进)。

## 交付
- reports/club_nation_subtable_schema.json + .md(v2,7 表 51 L3)
- scratch/t42/out/consolidate_v2.py(--help/--selftest:7 表/51 L3/15 held/4 neg/L4=0、master.json SHA 在、v1 44 字段 verbatim 保留校验)、verify.py(独立不 import builder)、REPORT.md、DONE.md
- Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + t01_anchors.py(7/7)。