# t58 完成记录

- 公共 schema 已从 v7 增量升至 v8；v7 Markdown 前缀、指定保护节和既有 club 子表计数逐值保持。
- 并入 t57/E97：双档各 84,259 行、34 位置、native identity 12 B、reader 1,412/167、13 L3、11 held、10 skipped、399 unmapped、72 倒置；held/unmapped 原台账嵌入。
- 主行 coverage：433 occurrences / 13 L3 / 11 held / 399 unmapped / L4=0；子表 `club_L3_occurrences=94` 不变。
- provenance 增加 t57/E97，并以条目级 canonical claim SHA 守卫 E87/E89/E90/E91/E92/E93/E94/E95/E96/E97。
- 交付：`consolidate_v8.py`、`verify.py`、v7/v8 快照、报告、完成记录及 `spot_*.log`。
- JSON SHA-256 `76da94d4376613a9e649a32d3bfc415f19596d4c7fb1c7c861d60b5951770cbf`；Markdown SHA-256 `5067502eadd489fac0e9842c6ece45e8402ff656e43d41e721522714308737f6`。
