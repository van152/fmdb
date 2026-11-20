# t62 DONE — partial

- **EDsc：静态调用链闭合到 UI 消费者。** `0x45447363` 经 `0x282b9` 归一为 `0x32`，cell `0x2a8b8:99ebffff` → `0x29389`。按 selected type 进入 COMP `0x6c120` 或 NATION `0x6bb00`，生成结果返回 UI。仍无现代 `table_10` 主行 wire 新槽；旧 `EDsc=held, slot=null` 及原 negative 保留。
- **EDfx：上游持久化未闭合。** 已定位 `fles`/`comp` 输入、日历内存桶与 Nation backlink；原字面命中仅是 compare，所追结果只返回 UI。未验到具体 reader、writer 或 `.dat` 区段，七条有界排除及重开条件已交付。未将对照表或输入候选写为 backing。L4=0。
- **验收：** builder 和独立 verifier 均通过（277 个指令见证、4 个精确 key 回放、双 FMF 目录与 t10/t25 头部对照），两者 `--help` / `--selftest` 通过，`scripts/t01_anchors.py` **7/7**。未启动游戏/编辑器/IDA，未联网、未访问 Z:；未改旧报告或已闭 L3 映射。

## 交付

- `scratch/t62/out/xref.json`
- `scratch/t62/out/chain.json`
- `scratch/t62/out/exclusions.json`
- `scratch/t62/out/verify.py`
- `scratch/t62/out/REPORT.md`
- `scratch/t62/out/DONE.md`
- `scripts/t62_edfx_edsc.py`
