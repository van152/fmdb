DONE type=t92 status=complete

# t92 — schema v11.3 候选装配

**状态:complete**(机械合并;只装配不改判)

## 产物(`scratch/t92/out/`)

| 文件 | 大小 | 说明 |
|---|---|---|
| `schema_v113.json` | 21,369,551 B | **v11.3-candidate**,43 根节(40+3),sha256 `e4175578…944254e` |
| `denominator_note.json` | 65,118 B | 分母 117 条 grade 注记(值不变) |
| `diff_inventory.json` | 92,105 B | verify 产出:423 条叶子 diff 全溯源,8/8 过 |
| `verify.py` | 18,032 B | 独立校验器 V1–V8(不 import 构建器) |
| `REPORT.md` | — | 装配报告 |
| `DONE.md` | — | 本文件 |

构建器:`scripts/t92_schema_v113.py`(`--selftest` / `--build` / `--denominator` / `--all`)

## 校验结果

- `verify.py` → **8/8 PASS**(V1 溯源 / V2 E127 修正 / V3 新节计数 / V4 根不变式 /
  V5 family↔rt vs slots / V6 分母注记 / V7 E132–E138 台账哈希 / V8 t9 双档一致)
- `scripts/t01_anchors.py` → **7/7 PASS**
- `scripts/t92_schema_v113.py --selftest` → PASS

## 关键变更

1. `table9_closure_e127`:**307,555 → 307,564**(两处 t51 游标键,+9B footer),留 `t92_why_before`。
2. 新节 `table45_structure_e132_e138`:行分解(80+namelen 普适,t92 重算 84,477 行零反例)、
   三列、~14 物理列、117 码=访问器视图、family↔rt(7 族 7 rt,无冲突)。
3. 新节 `t9_grammar_e133`:13B 头(count@+8=251)、双档闭包、ordinal/sentinel 双 251/251。
4. 新节 `cbw_route_e135_e137`:4CC 零存在负结果原文保留、tag 位置路由、E121 引用降级为
   unverified、fix8 真 PE 节表(18 节,.reloc 45.6MB)。
5. `schema_version` → `11.3-candidate`,`generated_by` → `t92`,`incremental_provenance`
   追加 E132–E138 快照 + 源文件 SHA-256 + 装配守卫。

## 纪律

- `reports/` 零写入;`LEDGER` 零写入;其他 `scratch/tNN/` 只读。
- 未新增 L3,L4=0;负结果原样保留;冲突未裁决(见 REPORT §6 未决 5 条)。

## 交接

指挥官验收时把 `schema_v113.json` 合入 `reports/club_nation_subtable_schema.json`,
把 `denominator_note.json` 的注记合并进 `reports/xml_denominator_coverage.json`
(仅加 `grade_note`/`grade_unchanged`/`note_ledger`,不动值)。
