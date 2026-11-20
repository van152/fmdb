# t56 — 公共 club/nation schema v7 增量

## 变更

- 基线：v6/t54 JSON 与 Markdown 快照 SHA 固定；Markdown 旧内容逐字节保留为新文件前缀。
- 新增 `nation_main_row_fields`：嵌入 t55 全量 field_map、field_slots 与 ABC closure 结构记录，并固定来源 artifact SHA。
- Nation 汇总：L3 occurrences 35、unique wire fields 35、held occurrences 25、negative records 15；L4=0。
- 新增 t55/E94 L3 与 v6 基线 E95/L2 的 entry-level ledger 记录；不比较 live ledger 全文件哈希。
- 保持 `tables`、`negative_regressions`、`v3_baseline`、club 计数、`club_auxiliary_sources`、`nation_data_side_status`、`nation_static_side`、`nation_t9_wire` 原值。

## 验收

- t55：992 CFG instructions；40/15 positions；251+251 rows；15/346 XML alignments；L3=5、L4=0。
- t55 source independent verifier passed before consolidation; t56 builder selftest, independent verify, spot checks, and anchors are recorded in `spot_*.log`.
- v7 JSON SHA-256 `d93a5070489c737e5d70fa2b8ffb135f9d4135d70df7ae4b6e2d27a4379ded10` (5759895 bytes); v7 Markdown SHA-256 `f84d265c2ca067794bd98f8ddb15cda026dc2b63bd185bd3db0eab43bd6b83bc` (59740 bytes).
