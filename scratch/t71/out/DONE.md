DONE type=t71 status=complete

- `CLUB+0x100` 静态绑定 `table_extra_3.dat`；client/server 各 84,259 行，从 12 B 头完整顺读到 EOF，无 footer；按主表 ordinal→UID 双档全量配对。
- 24 项 L3：22 个 `cnst` 与 `Cebd`（server wire），`Cyfn`（双档 wire，84,259 对相等）。0 held，0 L4。旧负证据不改。
- builder/verifier 的 `--help` 和 `--selftest`、全量 build/verify、14 条年份夹具、`scripts/t01_anchors.py` 7/7 均通过。

| 路径 | SHA-256 |
|---|---|
| `scripts/t71_club100_cnst.py` | `d683f6cffbfc77acd49c8d4078732cfa2b4bb41986677865f19c39a20e650c59` |
| `scratch/t71/out/chain.json` | `c001f0d22db79b144760d614c69f21c3812a66de714e3ebeee0f3e35acd09534` |
| `scratch/t71/out/field_map_r3.json` | `5e5a869acbb4a545ff1f27ef346952547b3d92ce052db6a51ce7390b552dfe75` |
| `scratch/t71/out/rows_extra3.json` | `df809f45cdd7329f005144d3a90ec316c4ee1ebd7f16e751f9d082d68914ca38` |
| `scratch/t71/out/verify.py` | `65295f3305716f46687059be3aa815490750eb12d98b491fa6c833642ca26ff5` |
| `scratch/t71/out/REPORT.md` | `950cb77cca017b591ae823b35a5398aeab8cfd44f290844b9c9b2219df683375` |
