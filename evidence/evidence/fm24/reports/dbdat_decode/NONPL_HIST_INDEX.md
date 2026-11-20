# b51 — `non_pl_hist_index/id/dt` 对齐结论

状态：只读分析；Python 3.12.10；数据源 FM24 db 2430（`Z:` 安装副本）。L4 未尝试。脚本 `scripts/b51_nonpl_hist_index.py`，机读结果 `reports/dbdat_decode/nonpl_hist_index.json`。

## 结论

**non-player 的 `index → id range → dt byte offset` 关系可按 player 侧范围模型完整恢复（L1）。** `non_pl_hist_id.dat` 每一对是 inclusive `(start_offset,end_offset)`：两端均为 24 字节对齐，`end` 指向该块的终止记录。历史块行链按 `+24` 递进，末行 `next@+20 = 0xffffffff`。索引第二列是 `id` 范围序号，而不是 DT 行号；有效序号 `0..746542` 全部且仅引用一次。

与 player 模型的区别也已量化：non-player 的排序 key 允许重复，且含 sentinel。不能把 `index` 第一列当唯一人员主键，也不能从 746,543 个范围推导“当前职员数”。

## 全量不变量（L1，db 2430）

| 项 | 实测 | 结果 |
|---|---:|---|
| `non_pl_hist_index.dat` 解压长度 / count | 6,037,508 B / 754,688 对 | 计数与长度相符 |
| index key | 673,317 个唯一值；81,371 条同 key 额外项 | 非严格递增，非唯一 |
| index ordinal `0xffffffff` | 8,145 项 | sentinel；不指向范围 |
| 有效 ordinal | 746,543 项 | `0..746542` 的完整置换，每 ordinal 恰好一次 |
| `non_pl_hist_id.dat` | 746,543 对，header 后无 count | 第 1/2 列均为 24 对齐范围偏移 |
| 相邻范围 | 746,542/746,542 次 `next_start - previous_end = 24` | 连续、无重叠、无间隙 |
| `non_pl_hist_dt.dat` 解压 | 77,098,632 B = 3,212,443 × 24 | 整流完整覆盖，尾余 0 B |
| 范围行数 | 2,465,900 个 covered/non-terminal + 746,543 个 terminal | 合计 3,212,443 |
| 链接检查 | 3,212,443/3,212,443 个 `next` | 中间行指向 `offset+24`，末行均为 `0xffffffff`；0 违例 |

首个 id range 为 `(0,0),(24,24),(48,48)…` 不代表整个文件只有单行块：全量中 265,881 个范围单行，剩余 480,662 个范围包含更多记录。`history_index_summary.json` 原有首尾样例与本轮全量检查一致。

## 布局 / 解释边界

- index: `tad.` v3569 + zstd；payload `<u32 count><count × (u32 history_id, u32 range_ordinal)>`。
- id: `tad.` v1；offset 8 起为无 count 的 `<u32 start,u32 end>` 对数组。
- dt: `tadc` v3 + 串联 Zstd；每行 24B。与既有 `HIST_DT.md` 行结构一致：club u32、join/leave day/year、flag、sentinel year、role u32、next u32。此处核验的是范围/链结构，不重新命名 role 枚举。
- **L1**：字节长度、偏移对齐、引用排列、相邻间距、DT 完整覆盖及所有 next 指针均已全量复核。
- **L2 未声称**：未以独立职员名录证明 746,543 是“工作人员人数”；这是历史范围数，范围内有 2,465,900 个非终止工作记录。
- **L3/L4**：本结论未依赖 exe 反汇编；未启动游戏或编辑器，不存在 L4。

## 重跑

```powershell
py -V:3.12 -I scripts/b51_nonpl_hist_index.py --help
py -V:3.12 -I scripts/b51_nonpl_hist_index.py --selftest --json
py -V:3.12 -I scripts/b51_nonpl_hist_index.py --analyze --json
py -V:3.12 -I scripts/b51_nonpl_hist_index.py --analyze --output reports/dbdat_decode/nonpl_hist_index.json
```

退出码：0 全部不变量通过，1 数据不满足不变量，2 用法/输入/致命错误。脚本只读游戏 DB；`--output` 限于当前 worktree。
