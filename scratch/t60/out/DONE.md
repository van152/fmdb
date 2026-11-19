# t60 完成记录

- 公共 schema 已从 v8 增量升至 v9；v8 JSON/Markdown 快照 SHA 固定，Markdown 前缀逐字节不变。
- 并入 t59/E99 L3：client/server 7,047×2；payload 894,991 / 1,533,972 B；client 定宽 127 B；identity 12 B、footer 9 B；49 L3、10 held、196 unmapped、818 倒置、54 aligned、L4=0。
- 保存 82 个观测外层位置和 2 个静态未触发位置；COMP slot19 与 factory 双对象形态分开记录。
- t59 held/unmapped 原始 occurrence 对象逐条保留；26 新 4CC 与引用域零违例检查通过。
- coverage comp_main_row：255 / L3 49 / held 10 / unmapped 196 / aligned 54。
- provenance 添加 t59/E99，并以 id+kind/level+canonical claim SHA-256 守卫 E84–E99，不固定 ledger 全文件哈希。
- builder/verifier --help、--selftest 与独立 verify 通过；指定 FM24_DB_DIR 的 `scripts/t01_anchors.py` 7/7。
- 交付：`consolidate_v9.py`、`verify.py`、v8/v9 JSON/Markdown 快照、报告、完成记录与 `spot_*.log`。
- v9 JSON SHA-256 `703df30ea34fbee3b555ccf4233d4fe012bcb614435381efb68a3224e5ae64ee`；v9 Markdown SHA-256 `ded0da91af36098b2648af769ed258fd39d903e86f0494b5b2f8fab3a98c5757`。
