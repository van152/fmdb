# t51 DONE — partial，L3=6 / L4=0

- `Nrvn` 绑定 t9 主表：server 720 项，`nati`/`leve` L3；client mode 0 绕过。
- `Calt` 绑定 t9 主表、确认 owner 是 `NATIONAL_TEAM_CONTAINER`（base `TEAM_CONTAINER`），server 251 个零 count，`cmid`/`stid` held。
- `TCrs` 同一 owner，查到 `[this+0xb0]+0x48` 的 getter、分配池与 `0x11d3200` 填充路径；`table_extra_9.dat` 为候选，未完成成员/mode/EOF 验收。主表 `+0x188` 的同 reader 路径不可代替。
- `Nftb` 绑定 t10 主表，反驳 debug-only 即不持久化；server 7 项，三字符串及 packed date L3，三个引用 held。
- `EDfx` 确认 NATION 输入的 UI 构造路径，未证明 archive backing；`EDsc` 保留 unresolved。t37/t47 原项及负例不改。

交付：`REPORT.md`、`discovery_unknown2.json`、`cursor_table_{9,10}_{client,server}.json`、`fields_{Nrvn,Calt,Nftb}.json`、`instructions.part001–006.json`、`branches.part001.json`、独立 `verify.py`；builder `scripts/t51_nation_unknown2.py`。

复验：Python 3.12 `-I -B`，builder 与独立 verifier 的 `--help`/`--selftest` 通过；builder `--build` 和 verify 通过；`t01_anchors.py` 7/7 PASS。未运行游戏、编辑器或 IDA，未联网或访问 Z:。
