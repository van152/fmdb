# t47 交接：partial（成果已复验）

- 15 个目标全记录：9 个已证明内嵌 reader 链，6 个保留未解。没有新增独立 list 表；t37 原报告和 inventory 未改。
- `Ntxr` 在 server table 10 mode=1 读出 1,899 个 25 B 税项（合成 tag=1 证实 23 B 路径）。两档各 251 行逐游标闭合，client mode=0 跳过税项。7 L3、2 held、0 L4。
- `Nntp/Nctp/Nrtp` 与 `NTRv/NWGv/NSps` 各有独立的内嵌集合，另有 `Nfmp` / `NCro`；都连到 type 9 owner 和 slot 19，尚未完成主表/sidecar 分档走表与 item 域闸门，不发布字段坐标。
- `Nrvn` 已定位 runtime 筛选（container `+0x48/+0x50`，项 `+0xb=6`），未知填充源；`Nftb/Calt/TCrs/EDfx/EDsc` 保留部分路径或扫描负例。
- Builder、独立 verifier、二者的 `--help` 和 `--selftest` 均通过；`t01_anchors.py` **7/7**。退出码 0/1/2。未启动游戏/编辑器/IDA、未联网、未访问 Z:。

交付：`scripts/t47_nation_unknown.py`；本目录 `discovery_nation_unknown.json`、`cursor_nation_tax.json`、`fields_nation_tax.json`、`instructions.part001–010.json`、`branches.part001–002.json`、`verify.py`、`REPORT.md`、`DONE.md`。
