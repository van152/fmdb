# t13 阶段二：空白表锚点结果

## 总结

本次核查了指定 10 张非空表和 2 张空表：**4 张以 A 类静态锚 resolved，6 张 negative，2 张 empty**。没有把仅靠数量接近或链邻近的猜测写成结论。

| table_type | count | 结果 | 实体 | 主要依据/未决点 |
|---:|---:|---|---|---|
| 12 | 28,597 | resolved | `awar` (award) | A：reader object_off 128 ↔ 唯一 award 字段 `AHp1`。行数与已知 award 表不同，尚未解释其行集差异。 |
| 26 | 90,128 | negative | — | reader 只有 12-byte opaque call、无 object_off；club 数量接近但不吻合。 |
| 29 | 13,278 | negative | — | 邻近 player 码簇没有与本 reader 成员相连的证据。 |
| 32 | 315 | negative | — | 与 weather 334 行相差 5.69%；数量接近不是锚点，reader 无唯一字段码。 |
| 33 | 32,409 | resolved | `club` | A：reader object_off 68 ↔ 唯一 club 字段 `CMWE`。 |
| 36 | 6,535 | negative | — | 与 comp 7,047 行相差 7.27%；只有无语义的宽度/偏移信息。 |
| 38 | 5,241 | negative | — | reader 附近字段码跨实体共享；language 126 行明显不吻合。 |
| 39 | 117 | negative | — | 与 injury 115 行相差 1.74%；仅数量接近，无独立字段/值域锚。 |
| 45 | 84,477 | resolved | `pers` (person) | A：reader object_off 86 ↔ schema 唯一 person 字段 `gols`。 |
| 48 | 5,210 | resolved | `pers` (person) | A：逐表 reader object_off 86 ↔ 同一唯一 person 字段 `gols`；不以与 45 共享 reader 作为实体相同的依据。 |
| 52 | 0 | empty | — | boundaries 工件：empty payload，`14 + 0 + 8 == 22`。 |
| 57 | 0 | empty | — | boundaries 工件：empty payload，`14 + 0 + 8 == 22`。 |

## A 类锚复核

- **12 → award**：`reader_widths.json` 的 type 12 含 object_off 128；`chain_0106` 的 `AHp1` 访问指令为 `mov edi, dword ptr [rdi + 0x80]`。`schema_inventory.json` 中 `AHp1` 只属于 award（df=1）。
- **33 → club**：type 33 含 object_off 68；`chain_0145` 的 `CMWE` 指令为 `mov edi, dword ptr [rbx + 0x44]`。schema 中该码只属于 club（df=1），字段名为 Maximum Wage Allowed。
- **45、48 → person**：两个 table_type 各自的 reader 序列均含 object_off 86；`chain_0153` 的 `gols` 指令为 `movsx ebx, word ptr [rdi + 0x56]`。`gols` 在 schema 中只属于 person（df=1），字段语义为 Goals。两个类型复用了 reader/链；这里只分别映射实体类型，不据此宣称两张表相同。

以上 `file_off` 均指实际指令位置，不是 4CC 比较点；`verify.py` 会通过 PE 映射在原始 `editor.exe` 反汇编复核声明指令，并验证 reader、链、object_off、schema df 和 exe SHA-256。

## 数量候选及拒绝理由

百分比以独立已知实体基数为分母。实体计数均取 `scratch/t05/COVERAGE.json` 中已映射的另一张表；这些比较仅用于排除/保留线索，接近本身不当作 B 锚。

- table 26 对 club 84,259：差 5,869（6.97%），且无 reader 字段关联，拒绝。
- table 29 对 comp 7,047：差 6,231（88.42%）；邻近 player 码簇不构成关联，拒绝。
- table 32 对 weather 334：差 19（5.69%），不足以定案，拒绝。
- table 36 对 comp 7,047：差 512（7.27%），不足以定案，拒绝。
- table 38 对 language 126：差 5,115（4,059.52%），不吻合；邻近码均共享，拒绝。
- table 39 对 injury 115：差 2（1.74%），仅为数量接近，拒绝。
- table 45 对 club 84,259：差 218（0.26%），但唯一字段 `gols` 指向 person；不把数量巧合当作 club 锚。
- table 12 与已知 award 表 3,545 行相差 25,052（706.68%）。因此没有 B 类基数支持；当前实体映射仅由 A 锚支撑，仍需解释两行集为何规模不同。

## 负结果原文与尚缺证据

本次开始前没有 t13 负结果文件可继承。以下保留现有工件原始字段，不将 unknown 改写成实体结论：

> `scratch/t05/COVERAGE.json`：相关六张表均为 `"entity": null, "entity_tier": "unknown"`，且 `boundary` 为 `"closed"`。原始行数/mode 为：26=`90128/straight-line`、29=`13278/straight-line`、32=`315/count-loop`、36=`6535/count-loop`、38=`5241/straight-line`、39=`117/mixed`。

- 26、29：缺少从各 table_type reader 到唯一 schema 4CC 的成员级链路；需找到直接 reader/dispatch 证据或独立值域来源。
- 32、36、38、39：缺少能排除竞争实体的唯一字段码、独立吻合基数或带语义来源且 fill/sentinel 同时吻合的 ID 域证据。
- 12：实体类有 A 锚，但 28,597 行与已知 award 表的规模差异待解释，不能宣称两个行集相同。

## 空表证据

`COVERAGE.json` 与 `scratch/t05/server_bounds/boundaries.json` 均记录 table 52、57 的 count=0；后者将其标为 `empty_table_payload`，payload_len=22，闭合式为 `14 + 0 + 8 == 22`。没有可从空表读取的实体锚点。

## 验证与验收状态

- `py -V:3.12 -I scratch/t13/out/verify.py --help`：通过。
- `py -V:3.12 -I scratch/t13/out/verify.py --selftest`：`SELFTEST PASS`。
- `py -V:3.12 -I scratch/t13/out/verify.py`：`VERIFY PASS`；4 个 resolved A 锚均通过 exe 指令反汇编和工件关联复核，12 张表覆盖完整，2 张空表计数/封口通过。
- 验收线 1、2、3、4 达成；“每张均找到 A/B/C 锚”未达成的 6 张已明确保留为 negative，没有硬凑。 
