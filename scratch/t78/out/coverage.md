# t78 — club/nation/comp 1,034 XML occurrence 真实物理覆盖率

分母 = 三主表 XML 顶层 occurrence 共 **1034**(club 433 / nation 346 / comp 255)。
证据全部来自冻结工件(schema v10 + t71 r3 + t72 inventory + t57/t69 尾账),无新解码、无反汇编。

| entity | mapped_l3 | independent_member | string_name_table | ui_or_derived | held | unresolved_wire_slot | no_wire_evidence | Σ |
|---|---|---|---|---|---|---|---|---|
| club | 45 | 10 | 0 | 5 | 28 | 239 | 106 | **433** |
| nation | 5 | 1 | 0 | 1 | 21 | 0 | 318 | **346** |
| comp | 49 | 0 | 0 | 18 | 10 | 38 | 140 | **255** |
| Σ | 99 | 11 | 0 | 24 | 59 | 277 | 564 | **1034** |

**已落到物理承载(mapped_l3 + independent_member + string_name_table)= 110 / 1034 = 10.6%**;
held 59;unresolved_wire_slot 277(有 wire 槽但未命名,t72 已给指纹);no_wire_evidence 564。

## unresolved_wire_slot 明细(给 t02 定向对照与后续波次排序)

- **club**:239 个 occurrence 挂在 20 个未命名物理槽上:`pos0/selector, pos1/derived_170, pos2/derived_178, pos4/ref_e0, pos9/name_len, pos11/short_len, pos14/raw166, pos16/raw16c, pos17/vec110, pos18/obj150_tag, pos20/vec130, pos21/vec138, pos22/raw168, pos24/base_ba, pos26/base18, pos27/base30, pos28/base60, pos29/base78, pos30/base90, pos32/basea8`
- **comp**:38 个 occurrence 挂在 36 个未命名物理槽上:`pos0/selector, pos1/m15c, pos2/m15d, pos3/colour_tag, pos7/m12c, pos8/m130, pos9/m134, pos10/m1a0, pos12/m1a3, pos13/m1a4, pos15/stat_a_tag, pos23/stat_b_tag, pos25/mf6, pos26/m138, pos27/m13c, pos30/m70, pos32/m150, pos34/mb8, pos36/m184, pos37/m186, pos38/m182, pos39/m160, pos40/m168, pos41/m170, pos42/m178, pos43/vec30, pos44/a8_present, pos45/obj_a8, pos46/mf0, pos48/m1a8, pos51/e0_present, pos52/obj_e0, pos66/m148, pos67/m152, pos76/wbcl_present, pos82/mf9`

## 抽样交叉(每桶前 3 条)

- `club` duni(mapped_l3)→ reports/club_nation_subtable_schema.json#/club_main_row_fields/L3_fields/0
- `club` Cext(mapped_l3)→ reports/club_nation_subtable_schema.json#/club_main_row_fields/L3_fields/1
- `club` Cedp(mapped_l3)→ reports/club_nation_subtable_schema.json#/club_main_row_fields/L3_fields/2
- `club` CNtp(independent_member)→ scratch/t69/out/tail_ledger.json#/entries/0
- `club` CSrs(independent_member)→ scratch/t69/out/tail_ledger.json#/entries/1
- `club` Cstc(independent_member)→ scratch/t69/out/tail_ledger.json#/entries/2
- `club` lpRP(ui_or_derived)→ evidence/fm24/reports/editor_schema/master.json#/entities/club.xml/0/fields/35/type
- `club` ipRP(ui_or_derived)→ evidence/fm24/reports/editor_schema/master.json#/entities/club.xml/0/fields/36/type
- `club` hpRP(ui_or_derived)→ evidence/fm24/reports/editor_schema/master.json#/entities/club.xml/0/fields/37/type
- `club` rdui(held)→ reports/club_nation_subtable_schema.json#/club_main_row_fields_r2/held_records/0
- `club` Cnam(held)→ scratch/t57/out/field_map.json#/fields/6/grade
- `club` Csnm(held)→ scratch/t57/out/field_map.json#/fields/7/grade
- `club` dbnm(unresolved_wire_slot)→ scratch/t63/out/projections.json#/occurrences/3/dispatch
- `club` dAPw(unresolved_wire_slot)→ scratch/t63/out/projections.json#/occurrences/4/dispatch
- `club` Csxn(unresolved_wire_slot)→ scratch/t63/out/projections.json#/occurrences/5/dispatch
- `club` NDBC(no_wire_evidence)→ reports/club_nation_subtable_schema.json#/club_main_row_fields_r2/unmapped_records/0
- `club` FDBC(no_wire_evidence)→ reports/club_nation_subtable_schema.json#/club_main_row_fields_r2/unmapped_records/1
- `club` CNse(no_wire_evidence)→ reports/club_nation_subtable_schema.json#/club_main_row_fields_r2/unmapped_records/25
