# t109c 收尾报告

## 验收结论

- `scripts/t109_big3_l3_join.py --selftest`：通过，退出码 0。
- 主生成命令已重跑：`python -I -B scripts/t109_big3_l3_join.py --out scratch/t109/out`。
- `big3_l3_join.json`、`coverage_summary.json`、`remaining_gaps.json` 均为 `status: complete`。
- 分母守恒：club 433 + nation 346 + comp 255 = **1,034**。

## 覆盖率

- 旧口径：110/1,034 = **10.6%**。
- 新总覆盖：379/1,034 = **36.7%**（L3 静态闭合 105，子表路由 274）。
- 净持久化覆盖：379/673 = **56.3%**；non-DB 排除 361，剩余 gap 294。
- L3 对账 crosscheck：75 项，其中 exact 61、no-offset 2、within-slot 2、仍未静态闭合 10。

## 冲突修正与边界

- 将 17 个 comp `Pcs*`/`Pcj*` packed L3（offset 393–414 对应的已验收字段）保留为持久化 L3；不会再因 67 表 dispatch scan 未找到而错误标为 `excluded_non_db_l3`。对这类缺少重新闭合 serializer 的字段，`resolution` 明确说明证据来源是既有 accepted schema，未伪称新发现 serializer closure。
- `duni` 对 club/comp 的共享 identity 归属不再误判为 table_1/BASIC_PERSON 的 non-DB 字段：accepted persistent schema 优先，offset 按已验收 identity 保留（0x8 起始；共享基类 identity 范围 0x8–0x13）。
- `comp cbcl@0x124`、`ctcl@0x128`：getter offset 已知，但 own-object serializer 无对应 read step，保留 unresolved，并注明待 serializer/helper closure。
- `Cesd`、`Ceed`、`Cead`、`CteA`、`Chaf`、`Cmtp`：静态分析只确认 delegation，未提取最终对象相对 load/store；保留持久化判断但 offset/serializer route unresolved，未作为 non-DB 排除。
- 其他仍未闭合的 accepted 项及跨实体 tag collision 均保留在 crosscheck/gaps 中；10 项冲突详情和逐条 `reason` 写在 `big3_l3_join.json` 的 `accepted_l3_crosscheck`，具体 gap 解释写入 `remaining_gaps.json`。不以猜测补齐静态闭合证据。

## 输出清单

- `scratch/t109/out/big3_l3_join.json` — 主结果、输入哈希、逐行分类与 accepted-L3 crosscheck。
- `scratch/t109/out/coverage_summary.json` — 总覆盖率、分实体汇总与对账详情。
- `scratch/t109/out/remaining_gaps.json` — unresolved gaps、原因与 helper 汇总。
- `scratch/t109/out/REPORT.md` — 本报告。
- `scratch/t109/out/DONE.md` — 完成标记与交付统计。

未修改 `reports/` 或 `LEDGER.json`。
