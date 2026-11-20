# t32 完成

- Cmti/table 43：server `535 × 46 B` 全表闭合，client 目录无成员。
- **L3=5**：`play/cash/mths/pyiv` 四个固定坐标；`club` 一个条件坐标（按当前俱乐部选取另一端）。**held=1**：`icom` 无独立 wire sink，保留首行同字节、双视角反例。**L4=0**。
- 保留三个引用槽的 ordinal 假说反例；静态指令和目标表实测支持的是成对 record identity key。两套 reader extent、20 个条件、外层 20 条分支证据已落盘。
- Builder、独立 verify、两脚本的 `--help` / `--selftest`：PASS。`scripts/t01_anchors.py`：**7/7 PASS**。

交付：`scratch/t32/out/{cursor_cmti.json,fields_cmti.json,instructions.part001–008.json,branches.part001–002.json,verify.py,REPORT.md,DONE.md}`、`scripts/t32_cmti_cursor.py`。
