# t78 — club/nation/comp 1,034 个 XML 字段的有效分母分桶 + 真实物理覆盖率(deepseek 轻任务)

你是受指挥官委派的子代理。这是一次 **15 分钟级轻任务,只做数据组装,不做任何新解码/新反汇编**。目标:把 club(433)+ nation(346)+ comp(255)= **1,034 个顶层 XML occurrence** 按 schema v10 + t71 + t72 的既有结论自动分桶,产出一份"真实物理覆盖率"报告,给 t77(schema v11)当分母台账。

## 必读(全部只读)

- `reports/club_nation_subtable_schema.json`(v10):`club_main_row_fields`(L3 21/41 held/350 unmapped)、`comp_main_row_fields`(49/10/196)、`nation_main_row_fields`(5/…)+ 三个 `_r2` 节(held/unmapped 归因)+ `tables`(8 编号子表)与 `club_auxiliary_sources`(CLUB_LINK)
- `scratch/t71/out/field_map_r3.json`(t71 新转正 24 项:22 cnst + Cebd + Cyfn,均 club)
- `scratch/t72/out/inventory.json`(槽位分类:kind=l3_claimed/held/unnamed/collection_closed)+ `fingerprints.json`
- `scratch/t57/out/field_map.json`(club r1:10 skipped_separate_member 的承接表)、`scratch/t69/out/tail_ledger.json`(18 项尾账)
- `evidence/fm24/reports/editor_schema/master.json`:`field_codes`(4CC→locations)+ 三个 entity 的字段清单(type/dependencies——判断 UI/派生口径)

## 分桶定义(每字段唯一归属,优先级从高到低)

1. `mapped_l3` —— schema v10 或 t71 r3 里 grade=L3 的(注意 t71 的 24 项要并入,别漏)
2. `independent_member` —— skipped_separate_member/tail_ledger 已指明承接表(8 编号子表 / CLUB_LINK / table_extra_3 现已 t71 闭合的按 mapped_l3 算)
3. `string_name_table` —— 由 name_table_*/语言层承接的字段(t69 已闭的)
4. `ui_or_derived` —— master.json type/依赖显示 runtime-only 或 client-field/UI 派生(如 clfr;Cprs 之类无 scoped enum 的不算,除非既有台账已如此归档)
5. `held` —— 有精确字节但证据不足(各 held 台账)
6. `unresolved_wire_slot` —— 剩余:t72 指纹显示有 wire 槽位但未命名(附槽位 key 引用)
7. `no_wire_evidence` —— 既无槽位也无静态证据的(t72 unnamed 里全零/全一无 xref 的)

## 任务

1. 写 `scripts/t78_xml_denominator.py`(可 `--help`/`--selftest`,退出码 0/1/2):输入上述 JSON,输出:
   - `scratch/t78/out/buckets.json`:每 occurrence 一条 `{id, code, entity, bucket, evidence_ref}`(evidence_ref 指到 schema/t71/t72/t69 的具体 JSON pointer)
   - `scratch/t78/out/coverage.md`:按表 × 桶的计数矩阵 + 一段"真实物理覆盖率"结论(mapped+independent+string 合计占分母多少;unresolved_wire_slot 有多少个、对应多少个物理槽)
   - `scratch/t78/out/DONE.md`(首行 `DONE type=t78 status=complete`)
2. **数字必须能对上既有台账**:1,034 总数、club 433 / nation 346 / comp 255;t71 24 项、t69 18 项尾账;对不上的差值要解释,不许硬平。
3. 交叉自检:每桶抽 3 条手动对拍证据链,写进 coverage.md。

## 避坑纪律

1. 只写 `scratch/t78/` 和 `scripts/t78_*.py`;不碰 reports/、LEDGER、其他任务目录。
2. 不做新解码/新反汇编;引用一律给 JSON pointer 或报告锚点。
3. **文件写单次 ≤120 行**,大 JSON 分段写(t73/t74 的教训)。

Python `py -V:3.12 -I -B`;不需要 FM24_DB_DIR(不读 .dat)。
