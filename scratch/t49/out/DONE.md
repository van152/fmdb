# t49 交接：主表双档闭合，sidecar 待验

- `table_9.dat`：client / mode 0 与 server / mode 1 各 251 行通过；502 组身份尾与两个 footer 均闭合。六条拒绝记录在 `discovery_t9_wire.json`。
- 8 个 parent 均覆盖到其已证明的分档路径：7 个在至少一档有真实 item；`NCro` 仅见 gate=0。17 L3、13 held、L4=0。
- **未闭合：**`table_extra_9.dat` 的正向 reader/mode 和变长行界；`NCro` live item；held 枚举/派生项；剩余未分类 CFG 边。未用 sidecar 表头或候选前缀给任何 parent 分配数据。
- 交付：`discovery_t9_wire.json`、`cursor_t9_client.json`、`cursor_t9_server.json`、`fields_*.json`（8 个）、`instructions.part*.json`、`branches.part*.json`、`verify.py`、`REPORT.md`、`DONE.md`；builder `scripts/t49_nation_t9.py`。
- 复验：builder / 独立 verifier / 两者 `--help`、`--selftest` 通过；`t01_anchors.py` 7/7。t37/t47 基线与负结果原样保留。
