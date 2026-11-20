# t61-fix1 — 保护源守卫范围修复(指挥官指派,接续 t61-enumref)

`verify.py --check` 报 "protected source changed: reports/club_nation_subtable_schema.json":你构建时钉了 reports/ 的**整体 SHA**(且采样到 t60 构建中间态 8a3d9595…;最终已提交 v9 为 703df30e…,指挥官已落 E100)。这是守卫**范围**问题,不是内容问题——枚举复核的判定不依赖 schema 全文件。

## 修复指令(只做这些)

1. verify.py 的 schema 守卫改为**条目级**:对 t61 实际引用的台账条目(E94/E97/E98/E99)逐条钉 `id + claim canonical SHA + kind/level`(与 t54-fix1/t58 口径一致);删除或废弃全文件钉;如需记录当时所见 SHA,可留历史快照字段但断言只用条目级。
2. builder 若有同款全文件钉,一并改条目级。
3. 重跑:builder --selftest → PASS(不改写 out/ 交付物内容,只改守卫);verify.py --check → rc0;scripts/t01_anchors.py 7/7。
4. REPORT.md 末尾加 "## fix1" 两三行:根因(t60 v9 构建/落账竞态 + 全文件钉范围)与本修复;其它内容一字不动。DONE.md 同步一行。

Python `py -V:3.12 -I -B`;只写 scratch/t61/ 与 scripts/t61_enum_ref_sweep.py(如需重生成 out/ 内容应与当前一致)。
