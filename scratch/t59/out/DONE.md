# t59 交接 — 行框/CFG 完成，字段 partial

- `table_25`：client 7,047 / server 7,047 行，`13 + Σrow + 9` 双档封口；原生 identity 12 B，非旧 13 B lookahead 记法。Reader replay 与独立 raw identity census 逐行一致。
- 82 个实档外层位置，另有 2 个未触发的静态可选 payload。255 个 XML occurrence：49 L3（26 个新 4CC）、10 held、196 unmapped；L4=0。t01f 的 26 个槽、46 步旧游标、10 组命名夹具、六洲及 parent 352 全部复洽；negative 原样保留。
- 全档 builder / 独立 verify 通过；两者 `--help`、`--selftest` 通过；`scripts/t01_anchors.py` **7/7**。测试记录在 `scratch/t59/validation.log`。未访问 Z:、未联网、未运行游戏/编辑器/IDA。没有将 Club/Stadium 值域可用误写成 COMP 字段绑定，也未给未命名集合补语义。

## 交付清单

- `scratch/t59/out/REPORT.md`、`scratch/t59/out/DONE.md`
- `scratch/t59/out/field_slots.json`、`scratch/t59/out/field_map.json`
- `scratch/t59/out/instructions.part01.json`–`instructions.part07.json`
- `scratch/t59/out/branches.part01.json`–`branches.part03.json`
- `scratch/t59/out/verify.py`
- `scripts/t59_compmain_fields.py`
