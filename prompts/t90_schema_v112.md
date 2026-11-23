# t90 — schema v11.2 候选装配 + 分母重桶(机械合并,纯数据作业)

你是受指挥官委派的子代理,**全新会话**。t87(E124)已立 schema **v11.1**;本轮把 E125/E126/E127 三条已验收增量合入出 **v11.2 候选**,并重发分母分桶。**只装配,不改判**——所有结论以各任务 out 文件为准,冲突处标注不裁决。

## 输入(全部只读)

- 基线:`reports/club_nation_subtable_schema.json`(**v11.1**,37 root keys;只读,**禁止修改 reports/ 任何文件**);构建器范式 `scripts/t87_v11_patch.py`(可读可参考,**不得修改**)
- **E125(t81)**:`scratch/t81/out/fk_index.json`、`rescan_fk_city.json`(变长表 FK 索引;city Cnti 闭环 56,293/56,293;三小表六档)
- **E126(t83)**:`scratch/t83/out/field_map.json`(**214KB,程序化处理,不整读**)、`domain_stats.json`、`REPORT.md`、`xref_{award,language,media,weather,derby}.json`——五表 188 字段全入账 **152 L3**、media 20 步文法闭合、weather 风/降水 **R1/R2 纠偏 E118**
- **E127(t85)**:`scratch/t85/out2/collection_fields.json`、`wire_candidates.json`、`profile_nation.json`(table_9 严格闭包 13+28,922+12×251+9=31,956;条目文法 held)
- 分母基线:`reports/xml_denominator_coverage.json`(1034 occurrences,110/1034 unresolved=10.6%;只读)

## 任务(顺序,每步落盘;全部新文件写 `scratch/t90/out/`)

1. **10 分钟内先落** `out/schema_v112.json` 骨架(meta+status,结构对齐 v11.1 root keys,不发明新根键,增量走新增节)
2. **v11.2 装配**:按 t87 模式合入 t81/t83/t85 三包增量——新增节建议 `fk_index_e125`、`five_tables_l3_e126`、`table9_closure_e127`;weather 纠偏要在 v11.1 相应字段上**改值并留 R1/R2 provenance 注记**(不改结构);每条增量带 grade(L1/L2/L3)+ 源文件指针
3. **分母重桶**:读 coverage 基线,把 110 unresolved 中的 ① 117 项 CBW*/CBD* 记录族 → re-route 到 server table_45(grade=L2 candidate,注记 t88-fix2 车道进行中);② t83 五表已转正字段 → resolved(L3);③ t81 city Cnti → resolved;其余原样保留。产出 `out/denominator_v2.json`:逐字段 grade+pointer+新分母统计(总 unresolved/占比前后对比)
4. `out/verify.py`(独立核对:v11.2 相对 v11.1 的 diff 清单逐条可溯源到源 out 文件;分母重桶前后总数守恒)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t90 status=complete`)
5. 跑 `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t90/out/` 和 `scripts/t90_*.py`(新文件);**禁止写/改 reports/、LEDGER、任何其他 scratch/tNN/**(reports/ 合并在指挥官验收时做)
2. `>20KB` 文件不进会话(field_map.json 214KB、xref_reverse.json 1.3MB 程序化);print ≤30 行/次;单次写 ≤120 行
3. 冲突不裁决:两源数据打架→原样并列+冲突注记,标 escalate;候选不写成结论;负结果原样保留
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t90/out/

`schema_v112.json`、`denominator_v2.json`、`verify.py`、`REPORT.md`、`DONE.md`。
