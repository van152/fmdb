DONE type=t108b

# t108 — 4CC ↔ 内存偏移 v2（helper 内联 + Cnti 修复）

status: complete
outputs: scratch/t108/out

## 核心统计

- tables_covered: 67/67
- unique_fourcc: 2301
- table_fourcc_pairs: 8046
- pairs_with_this_or_subobj_offset: 3720 (t97: 1808)  → +1912
- child_table_resolved (4CC 在子表 handler 内定位): 725
- access_kind: direct_field=1836, bitfield=84, subobj_deref=441, resolved_via_helper=2084, helper_computed=956, confirmed_computed_or_ui=847, delegated_or_empty=1798
- t97 access_kind: direct_field=1255, bitfield=125, subobj_deref=89, helper_computed=2525, delegated_or_empty=2225
- helper_computed: 2525 → 956
- helper_inline_resolutions_in_map: 2084
- attach_v2_extras: 12010/12010 候选（含 alt）已回填（child_table 798，helper_chain 2248）

## 回归（18 条已验收 L3）

- checked=18 exact=15 within_slot=3 no_static_hit=0 mismatch=0
- `Cnti == 216`（0xd8：外层子对象指针，压过内层附属标量 0xb9）

## 1,034 分母

- unresolved_wire_slot (160 条): direct_mem_off=51, resolved_via_helper=18, resolved_via_helper_subobj=0, child_table=1, helper_computed=28, absent_everywhere=8
- held (59 条): direct_mem_off=29, resolved_via_helper=6, resolved_via_helper_subobj=0, child_table=0, helper_computed=4, absent_everywhere=1
- no_wire_evidence (564 条): direct_mem_off=53, resolved_via_helper=1, resolved_via_helper_subobj=0, child_table=147, helper_computed=55, absent_everywhere=260
- denominator_upgrades_with_new_this_offset: 285
- proposed_totals: {"absent_everywhere_in_67_tables": 312, "absent_locally_code_in_other_table": 37, "hit_confirmed_computed_or_ui": 68, "hit_delegated_or_empty": 31, "hit_direct_mem_off": 176, "hit_helper_child_table": 239, "hit_helper_computed": 115, "hit_other_table_same_tag": 9, "hit_resolved_via_helper": 27, "hit_subobj_deref": 20}

## 静态 read 交叉

- fourccs_with_offset: 3720
- hit_read_server: 1285
- hit_read_client: 482
- hit_any_read: 1471 (t97: 802, delta 669)

## 交付物

| 文件 | 字节 | sha256[:16] |
|---|---|---|
| `fourcc_mem_map_v2.json` | 18874021 | `67cc6efa6813da05` |
| `xml_triage_v2.json` | 1245890 | `100a3504cb1d7a03` |
| `static_read_join_v2.json` | 2838357 | `e0d626bb20f44d9c` |
| `REPORT.md` | 24788 | `90753795b9923ae0` |
| `DONE.md` | 2274 | `ac73e23520373afc` |

