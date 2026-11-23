# t90 — schema v11.2 候选装配 + 分母重桶

**性质:机械装配,不改判。** 本轮只把 E125(t81)/E126(t83)/E127(t85) 三条已验收增量
合入 v11.1,并重发 E116 分母分桶。所有结论以各任务 `out` 文件为准;两源打架处原样并列
并标 `escalate`,不裁决。`L4 = 0`。

产物全部落在 `scratch/t90/out/`;**`reports/` 与 `scratch/t01/LEDGER.json` 零写入**
(校验见 §5 D1)。

---

## 1. 交付物

| 文件 | 字节 | 说明 |
|---|---:|---|
| `schema_v112.json` | 30,291,049 | v11.2 候选;37 → 40 root keys |
| `denominator_v2.json` | 349,292 | E116 分母重桶候选,1,034 行逐条 |
| `verify.py` | 9,372 | 独立校验器(不 import 两个构建器) |
| `diff_inventory.json` | — | `verify.py` 产出的机读 diff 清单 |
| `REPORT.md` / `DONE.md` | — | 本文件与状态行 |

构建器(仓库内新文件,非交付物):
`scripts/t90_schema_v112.py`、`scripts/t90_denominator.py`。两者均带
`--selftest / --build / --verify`(8/8 与 5/5)。

---

## 2. schema v11.2 装配

### 2.1 diff 清单(v11.1 → v11.2-candidate)

新增 3 节,删 0 节,改 5 节 —— **与简报要求的"增量走新增节"完全对齐**:

| 变更 | 节 | 溯源 |
|---|---|---|
| 新增 | `fk_index_e125` | `scratch/t81/out/fk_index.json`、`rescan_fk_city.json`、`rescan_fk_t76.json` |
| 新增 | `five_tables_l3_e126` | `scratch/t83/out/field_map.json`、`domain_stats.json`、`REPORT.md`、5×`xref_*.json` |
| 新增 | `table9_closure_e127` | `scratch/t85/out2/collection_fields.json`、`wire_candidates.json`、`profile_nation.json` |
| 改值 | `schema_version` | `11.1` → `11.2-candidate` |
| 改值 | `generated_by` | `t87` → `t90` |
| 改值 | `coverage` | 追加 `fk_index_E125` / `five_tables_E126` / `table9_closure_E127` / `xml_denominator_pointer_v112` 四个计数器 |
| 改值 | `incremental_provenance` | 追加 E125/E126/E127 ledger 快照 + `t90_volume_policy` + `t90_additive_rule` + `t90_assembly_guard` |
| 改值 | `scan_tables` | **仅** `t76c/27/archives/{client,server}/slots` 的值(weather R1/R2);25 slot 进 / 25 slot 出,offset 集合不变 |

其余 **32 个根节逐字节不变**(`t90_assembly_guard.untouched_root_digests` 逐节 SHA-256,
`verify.py` A8/A9 复算)。

### 2.2 三节内容要点

- **`fk_index_e125`** — 37 targets 全 `closed`(逐 target 只留 archive/table/payload_len/
  row_count/identity_width/status/ordinal_set,窗口与 tie_break 细节留在 t81 原件);
  city 4 条 lane 全 `mapped-ordinal`(Cnti@10→t10 56,293/56,293 in-domain,UID 对照 0.338
  否证);t76 重裁 4 条(Dtm1/Dtm2 对 t24 **refuted** 保留,Lnat?/Lwea? mapped-ordinal)。
  **grade = L2(E125 验收级别)**,每条 lane 保留自己的 `grade_after` 原文。
- **`five_tables_l3_e126`** — 5 表 188 XML 字段逐字段入账(grade/scope/wire_loc/width/
  wire_type/member_off/getter-setter-reader-fixup fo/domain 指针),`L3 = 152`、held 17、
  byte gap 0;R1–R5 五条 reconciliation 原样收入;`preserved_negatives` 与 `integrity`
  (editor.exe + master.json + db_tables_*.json 三个 SHA)逐字搬入。**grade = L3**。
- **`table9_closure_e127`** — table_9 client 31,956 B(`13 + 28,922 + 12×251 + 9`)
  与 server 307,564 B 双档严格唯一 tiling(solutions=1),table_10 两档同法闭合;
  UID 阶梯头/尾 + 长度保留(全 251 项留在原件);`item_grammar = held_no_item_grammar`
  与 `[NATION+0x108]` 未证问题**原样保留为 held**。**grade = L2**。

### 2.3 weather R1/R2:改值 + provenance,不改结构

E126 用四重静态链(read/get/season-get/set + normalizer `0x43e7e10`)纠正 E118 两处:

| 纠偏 | 内容 | 落法 |
|---|---|---|
| **R1** | `blk+2..6` = WIND `w{b}w0..w4`,`blk+7..11` = PRECIP `w{b}p0..p4`(E118 两者互换) | offset 5/10 两个 slot 的 `field`/`why`/`grade` 改值,加 `provenance=R1` |
| **R2** | `blk+0..1` 是 **2B i16** `w{b}sd`(0..359);`blk+22` 是 `w{b}dn`,**`0x64`=100 显式 NULL 哨兵** | `@3` 宽 1→2,`@4` 降为 `merged_into_prev`,`@25` 由 unassigned → `w0dn` |

- 每块四组 × 4 块 = 16 处改值,client/server 各一套。
- **E118 原文不删**:每个被改 slot 的旧 `why` 移入 `why_before_E118`,负结果与旧理由原样保留。
- slot 数(25)、offset 集合、`slot_count`/`unresolved` 字段全部不变 —— 结构零改动。
- `scan_tables.t90_weather_value_edit` 记录规则、R1/R2 全文、被取代对象与保留策略。

---

## 3. 分母重桶(E116 → v2 候选)

### 3.1 三条规则的实际效果

| 规则 | 简报预期 | 实际移动 | 说明 |
|---|---|---:|---|
| ① `CBW*`/`CBD*` 记录族 → `server table_45` | 117 项 | **117** | club.xml[211..327] 整族,E121/E124 已判为 `server_db/table_45.dat` STARTING_RECORD 载荷 |
| ② t83 五表已转正字段 → resolved(L3) | 有 | **0** | 五表不在 1,034 分母内(见 §4 冲突 C2) |
| ③ t81 city `Cnti` → resolved | 有 | **0** | city(2) 同样不在 1,034 分母内(见 §4 冲突 C3) |

**守恒:1,034 → 1,034**,逐条 before/after 都在 `denominator_v2.json["rows"]`。

### 3.2 前后对比

| 分桶 | before | after | Δ |
|---|---:|---:|---:|
| `mapped_l3` | 99 | 99 | 0 |
| `independent_member` | 11 | 11 | 0 |
| `ui_or_derived` | 24 | 24 | 0 |
| `held` | 59 | 59 | 0 |
| `no_wire_evidence` | 564 | 564 | 0 |
| `unresolved_wire_slot` | **277** | **160** | **−117** |
| `re_routed_table_45`(新桶) | — | **117** | +117 |
| 合计 | 1,034 | 1,034 | 0 |

- unresolved 占比:277/1034 = **26.8%** → 160/1034 = **15.5%**。
- 物理覆盖率 **不变**:110/1034 = 10.6%(carried = mapped_l3 + independent_member +
  string_name_table,本轮无一条进入 carried —— table_45 族只是**换桶**,不是转正)。
- 若按 E121 建议把 table_45 族**移出** club extra_3 分母:110/917 = **12.0%**。两种口径
  并列给出,不择一裁决。
- `re_routed_table_45` 的 grade 是 **L2_candidate**,注记 t88-fix2 槽位 join 车道进行中。

---

## 4. 冲突与 escalate(不裁决)

- **C1 —— "117 项 = CBW*/CBD* 族" 的说法过窄。** 简报与 E121 文字都用 `CBW*`/`CBD*`
  指代该族,但 117 项实际含 10 个 `CB*` 码 + 107 个其它码(`CAAa`/`CFGd`/`CGLn`/`CHRn`/
  `CLAc`/`CMAp`/`COPc`/`CWCg`/`CYPd`…)。本轮按 E121 的**区间 [211..327] + 117 条**执行,
  `CB*` 标签按简报原文保留。→ **escalate**(措辞,不影响数据)。
- **C2 —— 规则 ② 结构性为空。** t83 五表(award/language/derby/weather/media)不是
  club/comp/nation 的成员,E116 分母里没有它们的 occurrence。唯一代码名相交的是 `duni`,
  但 nation 的 `duni` 是 table_10 的身份列、held 于 E94/E108,**不是** t83 的 table_0/8/18/27/7
  身份列。按"身份 = 归档成员 + 父 + 码"的三元组口径,**不移桶**。
  → **escalate**:若指挥官认为应把五表并入 1,034 分母,那是分母**扩容**,不是重桶。
- **C3 —— 规则 ③ 同样为空。** city(2) 无 occurrence。分母内确实存在的 `Cnti`
  (club/016、comp/015)在 E116 里**已经是** `mapped_l3`。t81 的 Cnti 结果是真结论,但属
  city(2) 侧,记录在 `denominator_v2.json["e125_city_lane"]` 备查。→ **escalate**。

三条冲突都在 `denominator_v2.json["conflicts"]` 里带 `escalate: true`。

---

## 5. 校验

| 校验器 | 结果 |
|---|---|
| `scripts/t90_schema_v112.py --selftest` | **8/8** |
| `scripts/t90_schema_v112.py --verify` | **36/36**,0 failure |
| `scripts/t90_denominator.py --selftest` | **5/5** |
| `scripts/t90_denominator.py --verify` | **18/18**,0 failure |
| `scratch/t90/out/verify.py --selftest` | **5/5** |
| `scratch/t90/out/verify.py --verify` | **35/35**,0 failure |
| `scripts/t01_anchors.py` | **7/7** |

`verify.py` 独立于两个构建器,只看产物:diff 清单逐条可溯源(A6/A7)、
32 个未触碰根节逐字节复算(A8/A9)、分母前后总数守恒(B3–B5)、
held/no_wire/ui 零移动(B11)、weather 改值不改结构(C1–C5)、`reports/` 零写入(D1)。

只读基线复核(本轮前后一致):
`reports/club_nation_subtable_schema.json` `f811a216…` / 29,893,769 B;
`reports/xml_denominator_coverage.json` `e3a6d56e…` / 297,905 B;
`scratch/t01/LEDGER.json` `794bad55…` / 282,003 B;`scripts/t87_v11_patch.py` `c303310e…`。

---

## 6. 留给指挥官验收时做

1. `reports/` 的合并(本轮**刻意不写**)。
2. `denominator_v2.json` → `reports/xml_denominator_coverage.json` 的替换,
   以及是否采纳"移出 table_45 族"的净分母口径(110/917 = 12.0%)。
3. C1/C2/C3 三条 escalate 的裁决。
4. 是否把 `schema_version` 从 `11.2-candidate` 定为 `11.2`(本轮按"候选"落盘,
   `generated_by = t90` 未伪装成正式版本)。
