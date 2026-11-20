# t66 DONE — 物理文法闭合，绑定结论 partial

- `table_25.dat` 双档各 7,047 母行，12 B identity、9 B footer 完整封口；server 7 个非空集合的项文法 L3，client mode 0 跳过，不是写零。
- t59 坐标重验 `+0xc0/+0xc8/+0xd0/+0xd8` 非空分别 **315/366/121/51**，不同于 brief。`vec30` 全零 count，`+0xa8/+0xe0` 全零 presence，三个 item 文法 held。
- 4 条引用 lane L3：`vec18:item+1 → t24`，`+0xd0:item+0`、`+0xd8:item+0/+4 → t23`。另 4 条 lane held（全一或无唯一目标）；未命名业务字段。未发现新的 COMP 独立归档成员绑定，未推定 getter 后备层。L4=0。
- Python 3.12 `-I -B`：builder/verify `--help`、`--selftest`、全档 build 和独立 verify 全通过，`t01_anchors.py` **7/7**。旧 t59 和 club/nation 闭层未改。

交付：`scratch/t66/out/{collections.json,census.json,verify.py,REPORT.md,DONE.md}`、`scripts/t66_comp_subtable_discovery.py`。
