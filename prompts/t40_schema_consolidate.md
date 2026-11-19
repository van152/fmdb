# t40 — club/nation 子表已证 L3 字段 consolidated schema(首份可用语义交付)

你是受指挥官委派的子代理。club/nation 子表 cursor 法已 6 次证实,累计 **44 个 L3 字段**分散在 6 个任务台账。本任务把它们 **consolidate 成首份可用语义 schema**(reports/ 结论 + 统一 JSON),全 provenance,不新增解析、不碰未闭表。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;结论入 reports/ + 同名 JSON)
- 6 份已接受台账(只读消费,不重跑 cursor):
  - scratch/t27/out/(Cstc stadium table22,fields_t22.json,14 L3;scripts/t27_stadium_cursor.py)
  - scratch/t30/out/fields_clhs.json(Clhs table_type37,8 L3)
  - scratch/t31/out/fields_csrs.json(CSrs table_type62,10/10 L3;REPORT.md)
  - scratch/t32/out/fields_cmti.json(Cmti table_type43,5 L3 + 1 held)
  - scratch/t34/out/fields_cntp.json(CNtp nati table_type66,2 L3 + 2 held)
  - scratch/t36/out/fields_cdbt.json(Cdbt table_type33,5/5 L3)
  (table_type 与 table_id 可能不同;以各台账实际字段为准,勿臆测)
- scratch/t01/LEDGER.json(E69/E71/E73 等接受记录)
- evidence/fm24/reports/editor_schema/master.json(club.xml/nation.xml 字段 4CC 对照,冻结 SHA 7d57477e)

## 任务
1. 逐台账抽取每个 L3 字段:parent 4CC、table_id、archive、field 4CC、schema 名、row 内 byte offset(双坐标 legacy14/wire13)、type(i8/i16/i32/u32/float32/bool/packed_date/ordinal_ref/pair_key)、signedness、sentinel(-1/0/-99.0/-1.0 区分)、reference target(目标表 + ordinal 域)、grade、证据 VA + source task。
2. held/negative 字段单列(保留首反例,不删不改写),注明 held 原因。
3. 统一 JSON `reports/club_nation_subtable_schema.json`:每 parent 一节,fields[] 全 provenance;附 closure 公式(header+Σrow+footer==payload_len)、count、stride、payload SHA。
4. `reports/club_nation_subtable_schema.md`:人类可读总表 + 每字段一行(offset/type/sentinel/ref/grade/VA/task)+ held/negative 节 + 方法学小结(6 次复制证实)。
5. 交叉一致性检查:同 parent 跨 archive offset 一致?reference target 的 ordinal 域是否真存在(消费 t29b/t37 inventory)?发现矛盾如实记 held,不妄断。

## 边界
- 只 consolidate 已接受 L3;不新解析、不跑游戏/编辑器/IDA、不联网、不读写 Z:。
- 候选/held 不升级为结论;negative 原样保留;L4=0。
- 只写 scratch/t40/ 与 reports/club_nation_subtable_schema.{json,md}(reports 新文件,不覆盖他人)。

## 交付
- reports/club_nation_subtable_schema.json + .md
- scratch/t40/out/consolidate.py(--help/--selftest:校验 JSON 字段数==44 L3 + held 计数、provenance 完整、closure 算术自洽)、verify.py(独立,不 import builder)、REPORT.md、DONE.md
- Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + t01_anchors.py(7/7)。