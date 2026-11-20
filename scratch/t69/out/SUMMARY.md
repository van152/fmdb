# t69｜三表尾账总表（L2）

**18 项：10 个 club 跳过项均有承接，0 悬案；nation 4 项仍 held；COMP 3 项 static-zero、1 项 edge-pending。** t61、t66、t68 均已交付；本轮不新增 L3/L4，不改公共 schema。

| 主表 | 类别 / 数量 | 可折叠结论 | 证据与承接任务 |
|---|---|---|---|
| club `table_3` | `skipped` ×10 | 8 个编号子表 + 1 个具名成员的 2 个视图。跳过指不占 t3 主行槽，不是缺失；`Tchl`、`Csme` 均不计为 club 独占。 | t57 `field_map.json#/grade_counts/skipped_separate_member` → schema v8/v9 `/tables/0..7`、`/club_auxiliary_sources/0/views/0..1`；t27/t30/t31/t32/t34/t36/t39/t41/t44 承接。t68 只复核 t3 行框/执行模板，不承接或验证独立成员。 |
| nation `table_10` | `held` ×4 | `Necf/Nygn/Ngct/Nsod` 沿用 `no_enum_source`，无晋级；不将原值补作哨兵或枚举标签。 | t55 原字段 → t61 `enum_inventory.json#/occurrences/6..9`。t61 复核完成，语义结论仍 held。 |
| comp `table_25` | `static-zero` ×3 | `+0xa8/+0xe0` 每项 server presence `{0:7047}`，`vec30` server u32 count `{0:7047}`；client 7,047 行均走 mode 0，**没有读取这些字节**。双档均 0 次 payload/item 触发。 | t59 `field_slots.json#/slots/{43,44,45,51,52}`、`branches.part01.json#/{30,43,54}` → t66 `collections.json#/collections/{+0xa8,+0xe0,vec30}`。t66 保持 held；非零分支/项无实档见证，待办未指派。 |
| comp `table_25` | `edge-pending` ×1 | `+0x100` server i16 count `{0:6918,1:62,2:56,3:9,5:1,6:1}`，129 行非空、212 项各 5 B。client 跳过。**t66 已定性物理文法，业务名/getter 绑定仍未定。** | t59 `field_slots.json#/slots/65` → t66 `collections.json#/collections/+0x100`。t66 承接物理层；后续语义未指派。 |

`static-zero` 不等于死边；`edge-pending` 在此专指 `+0x100` 未闭合的业务绑定。前三个 COMP 项的开放边随原条目保留，不重复计数。逐项指针、归档摘要和值分布见 [tail_ledger.json](tail_ledger.json)；club 十项及静态谓词见 [REPORT.md](REPORT.md)。
