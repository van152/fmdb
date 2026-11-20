# t52-fix1 — builder 守卫自相矛盾修复(指挥官指派,接续 t52)

你的 consolidate_v5.py 现在自相矛盾,`--selftest` 必败:

- build 侧(L535/545/656):`tasks["t50"]["acceptance_ledger_entry"]="E91"` + `ledger_status` 注明 "E91 accepts L2 data-side profile only; no L3 field, reader, mode, or parent mapping"(你在指挥官落 E91 后自适应加入,语义**正确**)。
- validate 侧(L821-822):`require(... is None, "t50 must not be represented as a ledger-accepted schema mapping")`(E91 存在前写的旧守卫)。
- 当前已交付的 reports/ v5 是早前(E91 落账前)构建的产物,t50.acceptance_ledger_entry=None;builder 自测已在 E91 存在下失败。

## 修复指令(只做这些,不要动其它内容)

1. **对齐 validate 与 build**:把 L821-822 的守卫改为——当且仅当 `acceptance_ledger_entry=="E91"` 且 live ledger 中 E91 的 (kind,level)==("acceptance","L2") 且 `ledger_status` 注记在场时放行;同时**保留原意图**的另一半:验证 `nation_static_side`/`nation_t9_wire.table_9`/`tables` 等字段映射结构中**没有任何 grade/field 归因给 t50**(即 t50 只出现在 provenance/t50_L2_cross_validation/L2 章节)。
2. 重跑并全部通过:`consolidate_v5.py --selftest` → PASS;`consolidate_v5.py --build` 重写 reports/ 两文件(t50 节将更新为引用 E91 的版本,markdown addendum 同步);`scratch/t52/out/verify.py --check`;`scripts/t52_spot_v5.py --check`;`scripts/t01_anchors.py` 7/7。全部 log 追加进 spot_*.log(注明 fix1)。
3. REPORT.md 与 DONE.md 末尾追加 "## fix1" 小节:说明守卫矛盾的根因(build 先行引用 E91、validate 滞后)与本修复;不改写其它结论。
4. 不得改动:v4 保护节、club 计数、t47/t49/t51 的 grade 归因、t50 framing conflict "NO WINNER" 记录、t50 的 L3=0 定位。
5. verify.py / spot_v5.py 若同样有 None 断言,一并按同一语义对齐;两者仍须独立于 builder。

完成后打印交付清单。Python `py -V:3.12 -I -B`;只写 scratch/t52/、scripts/t52_*.py、reports/ 两文件。
