# t58 — 公共 club/nation schema v7→v8 增量

## 变更

- 基线：v7 JSON SHA-256 `d93a5070489c737e5d70fa2b8ffb135f9d4135d70df7ae4b6e2d27a4379ded10`；v7 Markdown SHA-256 `f84d265c2ca067794bd98f8ddb15cda026dc2b63bd185bd3db0eab43bd6b83bc`；Markdown 旧内容逐字节保留为新文件前缀。
- 新增 `club_main_row_fields`：嵌入 t57 双档 34 槽、field_map 全量 occurrence、field_slots、静态 reader extent 与 framing sensitivity。
- Club 主行汇总：433 occurrences、aligned 18、L3 13、held 11、skipped 10、unmapped 399、72 inversions、L4=0。
- 既有 club 子表口径保持：`club_L3_occurrences=94`、`club_L3_unique_wire_fields=59`、`held_fields=21`；8 张表和所有 nation 节逐值保护。
- 条目级 ledger 守卫：E87/E89/E90/E91/E92/E93/E94/E95/E96/E97；E97 为 L3，canonical claim SHA `ba5a1079403dd970b30c9304a90c37d5a66f3d28163ee2cf2588fd355129ff32`。

## 验收

- t57 数字断言：client/server 6,932,082 / 16,595,312 B；84,259 + 84,259 rows；identity 12 B；reader 1,412 instructions / 167 branches；13 L3；72 inversions；69705 13-byte negative 保留。
- held/unmapped 原样保留：`Csnm` 537 越界、`CLat/CLon` 非 Club 坐标、`Csti` 证据不足、`Cyfn` 为 extra+0xd8 非主行；E60 `Cccn` negative 与真绑定 `+0xf0` 注记保留。
- builder selftest、independent verify、`--help` / `--selftest` 与 t01 anchors 结果写入 `spot_*.log`。
- v8 JSON SHA-256 `76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf` (6477903 bytes)；v8 Markdown SHA-256 `5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6` (68129 bytes)。
