# t60 — 公共 club/nation schema v8→v9 增量

- v8 快照：JSON SHA-256 `76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf`；Markdown SHA-256 `5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6`。v9 Markdown 以 v8 原文为逐字节前缀。
- 新增 `comp_main_row_fields`，嵌入 t59 field_slots/field_map 原始对象、全部 L3/held/unmapped occurrence、完整 818 对倒置及源文件哈希。
- Comp 主行：255 occurrences、aligned 54、L3 49、held 10、unmapped 196、818 inversions、L4=0。
- 双档 payload 894,991 / 1,533,972 B，7,047 行各；client 定宽 127 B；identity 12 B、footer 9 B；reader slot19 837 instructions/114 branches；82 个观测位置+2 静态未触发。
- 26 个新 4CC；7 组引用域 join 均 0 miss；factory case25 的 COMP 与 DATABASE_TABLE<COMP> vtable 分别记录，未合并。
- 既有 club 主行、club 子表、nation 节及 tables/negative_regressions/v3_baseline/club_auxiliary_sources 全部逐值保护。ledger entry guard 扩至 E84–E99。
- 验收：builder/verifier 的 --help、--selftest 与独立 verify 均通过；FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data 下 `scripts/t01_anchors.py` 7/7。命令输出在 `spot_*.log`。
- v9 JSON SHA-256 `703df30ea34fbee3b555ccf4233d4fe012bcb614435381efb68a3224e5ae64ee` (7866611 bytes)；v9 Markdown SHA-256 `ded0da91af36098b2648af769ed258fd39d903e86f0494b5b2f8fab3a98c5757` (73801 bytes)。
