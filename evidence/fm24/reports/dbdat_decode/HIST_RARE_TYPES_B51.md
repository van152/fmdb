# b51 — `pl_hist_dt` 稀见 `row_type` 收尾

只读分析 db 2430；工具 `scripts/b51_rare_hist.py`；全量机读样本 `reports/dbdat_decode/rare_hist_types_b51.json`。L4 未尝试。

## 全量结果（L1）

本库共 17 个不同 row_type 值：主体 0/1/2 + **14 个 ≥3 的稀见码**。`HIST_DT.md` 的计数包含每个人物块的 terminator；本轮同时把 career rows 与 terminator rows 拆开，且全量验证 4,515,803 行、515,581 个终止行、所有 44-byte next 链 0 违例。

| code | 含 terminator 总数 | career rows | terminator rows | 观测边界 |
|---:|---:|---:|---:|---|
| 3 | 15,599 | 14,296 | 1,303 | 4,333 career rows 的 apps/goals=255 |
| 4 | 729 | 698 | 31 | fee=-3 为最常见值（338 career rows） |
| 5 | 3 | 2 | 1 | 仅 2 条 career rows |
| 6 | 20 | 20 | 0 | 极少样本 |
| 8 | 139 | 138 | 1 | 极少样本 |
| 9 | 2 | 2 | 0 | 极少样本 |
| 10 | 1 | 1 | 0 | 单例 |
| 12 | 19 | 19 | 0 | 极少样本 |
| 16 | 27 | 24 | 3 | 极少样本 |
| 20 | 5 | 4 | 1 | 极少样本 |
| 24 | 7 | 6 | 1 | 极少样本 |
| 28 | 3 | 3 | 0 | 极少样本 |
| 32 | 6 | 1 | 5 | 仅 1 条 career row，其余为 terminator |
| 34 | 1 | 1 | 0 | 单例 |

## 样本交叉与负结果

以下名字来自本机 `people_db`/姓名锚与 history ID 的本地 join，**不是独立事实源**；球队名也来自本机数据库。因此它们用于定位样本/核对形状，只记 L1，不升为 L2：

- `row_type=4`：Juan Esnaider（history_id 881）1996–97 Atlético Madrid，35/16，fee=-3；William Gallas（2265）2005–06 Chelsea，34/5，fee=-3。两条都长得像常规俱乐部赛季统计，但同样的赛季统计也见于 `row_type=0`。`-3` 的含义未知；**不能**据此给 code 4 命名为“转会/合同/赛事类别”。
- `row_type=16`：Atiba Harris（7,453,276）2012 Vancouver 记录 7/0；样本自身不说明 code 16 语义。
- `row_type=24`：Jeff Larentowicz（980,777）2012–13 Chicago Fire 32/3、fee=-2；紧邻的 2013 row_type 0 同俱乐部 32/2，赛季字段有重叠。它提示重复/分拆/源数据合并等可能性，无法据此断言 24 的类别。
- `row_type=20`：Gianluca Busio（72,023,345）2017 Sporting Kansas City 行 apps/goals=255/255（未知哨兵），只凭单行无法定级。
- type 32 共 6 条中 5 条是 terminator，仍有 1 条非终止记录；故不能简单把 type 32 当终结标记。

任务书提到的特例路线也做了结构搜索：找到同一 club ID 的两条 type-1 借用记录样例（history_id 149，club 994，1998 与 1999），但没有独立史料确认具体借用关系；fee=0 后出现 type-2 的朴素命中多为职业史起始阶段的青训行，无法证明“自由离队后回归青训”。这些 pattern 不足以给任何 ≥3 code 赋语义。

**结论：0/14 个稀见码获得独立 L2 定级。** 已交付完整计数、terminator 拆分、每个 code 最多 3 个上下文样本与 fee/apps/goals 概况；这是明确负结果，不把 L1 本地关联包装成“外部验证”。下轮如要推进，需要获得独立可引用的球员完整履历或找到 `fm.exe` 中实际消费 row_type 的 enum/switch 证据。

## 重跑

```powershell
py -V:3.12 -I scripts/b51_rare_hist.py --help
py -V:3.12 -I scripts/b51_rare_hist.py --selftest --json
py -V:3.12 -I scripts/b51_rare_hist.py --census --json
py -V:3.12 -I scripts/b51_rare_hist.py --census --output reports/dbdat_decode/rare_hist_types_b51.json
```
