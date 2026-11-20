# t65 — Nation 主行 unmapped 第二轮深度普查(sol;t55 方法加深 + t59 范式迁移)

你是受指挥官委派的子代理。t55(E94)nation table_10 主行 346 occurrence 中 **327 unmapped**(5 L3/held 4:Necf/Nygn/Ngct/Nsod)。本任务做第二轮:把 t59 验证的两个范式(本地 getter 投影、byte 位投影)与 t55 已建 CFG 资产结合,深挖 327 unmapped。

## 必读
- AGENTS.md;scratch/t55/out/field_slots.json + field_map.json + REPORT.md(**行框/CFG 唯一来源**:server 40/client 15 位置,992 指令 CFG;identity 13B)
- scratch/t59/out/REPORT.md(**范式范本**:cnst 投影 gate/helper/cursor、bit 投影 shr/and、wrong-UID 控制例)
- reports/club_nation_subtable_schema.json(v8/v9 以实际为准;nation_main_row_fields 原样;Ntxr 7/t9 parent 17/Nrvn/Nftb 已闭不重做)
- evidence/fm24/reports/editor_schema/master.json(nation.xml 346 字段冻结)
- scratch/t53/out/REPORT.md(TCrs getter 后缀先例:extra_9 内的类型化后缀口径——nation 侧若有同类,引用其裁决格式)

## 任务
1. **投影扫描**:nation 主 reader extent 与相关 helper 区,枚举"gate→helper→cursor"三元组与位投影(shr/and),对齐 unmapped occurrence(4CC/成员证据,不按 XML 序号)。
2. **全档域检验**:251 行双档全量;引用字段走目标实表 ordinal 集;wrong-UID 控制例;值域 vs XML min/max/enum_ref;过闸 L3,否则 held+首反例。既有 held 4 不重判(Ngct/Nsod 无 scoped enum_ref 属 t61 管辖,若 t61 已交付可引用)。
3. **client 15 位置 vs server 40 位置**:未在 client 模板出现的 server-only 站点逐个定性(静态/数据双证);client 未触发的给出条件。
4. 独立 verify.py + builder scripts/t65_nation_unmapped_r2.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 nation 主行;不碰 t9/extra_9/subtables/t55 已闭 L3;不碰 person/PDxx;不启动游戏/编辑器/IDA,不联网,不读写 Z:。

## 交付 scratch/t65/out/
- projections.json、field_map_r2.json、verify.py、REPORT.md、DONE.md;scripts/t65_nation_unmapped_r2.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
