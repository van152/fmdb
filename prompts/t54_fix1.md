# t54-fix1 — ledger 守卫范围修复(指挥官指派,接续 t54)

`verify.py --check` 现报 "t54 ledger snapshot hash/size mismatch":你在构建时钉扎了**整个 LEDGER 文件**的 SHA/尺寸(snapshot=93 条),指挥官随后(03:52)落了 E94(t55 验收)→ 现文件 94 条,整体哈希必然失配。这是守卫**范围**问题,不是内容问题(builder --selftest 全过)。

## 修复指令(只做这些)

1. verify.py 的 ledger 守卫改为**按引用条目**钉扎:对 v6 实际引用的条目(E87/E89/E90/E91/E92/E93)逐条钉 `id + claim 的 canonical SHA + kind/level`,不再钉全文件 hash/size;删除或废弃全文件钉(ledger_snapshot.json 可保留为历史快照但断言只用条目级)。
2. 若 consolidate_v6.py 也有同款全文件钉,一并改条目级。
3. 重跑:consolidate_v6.py --selftest → PASS(不改写 reports/,内容未变);verify.py --check → rc0;scripts/t01_anchors.py 7/7。spot 日志追加 fix1 记录。
4. REPORT.md/DONE.md 末尾加 "## fix1" 两行说明根因(指挥官落 E94 与构建竞态)与本修复;其它内容一字不动。

Python `py -V:3.12 -I -B`;只写 scratch/t54/ 与 reports/ 两文件(如需重生成,内容应与当前 v6 完全一致)。
