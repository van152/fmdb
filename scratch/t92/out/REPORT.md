# t92 — schema v11.3 候选装配(E132–E138 机械合并)

日期 2026-11-22 | 分支 `t75-wirexref` | 车道 t92(全新会话子代理)
产物:`scratch/t92/out/schema_v113.json`、`denominator_note.json`、`diff_inventory.json`、`verify.py`

## 1 结论(一句话)

v11.2 → **v11.3-candidate** 完成机械装配:3 个新根节入册(`table45_structure_e132_e138` /
`t9_grammar_e133` / `cbw_route_e135_e137`),E133 的九字节更正在 `table9_closure_e127`
的 t51 冻结游标上落值,分母 117 条只加注记不动值。**未改判、未新增 L3、L4=0**。

## 2 交付与校验

| 项 | 值 |
|---|---|
| 根节 | 40 → **43**(+3,无删除、无静默改写) |
| 产品 sha256 | `e4175578d587e201b7d0b14bd15c69c967679049d4a0d236cd4f9e861944254e` |
| 产品字节 | 21,369,551 B(indent=1 + CRLF,与 reports/ 同序列化) |
| v11.2→v11.3 叶子 diff | **423 条,全部可溯源**(V1) |
| verify 项 | **8/8 过**(V1–V8,独立重抽,不 import 构建器) |
| `scripts/t01_anchors.py` | **7/7** |

diff 分布:incremental_provenance 174 / table45 108 / t9 73 / cbw 34 / coverage 21 /
table9_closure_e127 11 / 版本 2。

## 3 各节要点(全部以 LEDGER 为准)

### 3.1 `table9_closure_e127` — E133 九字节修正

- `cross_check_t51_frozen_cursor/server|table_9.dat` 的 `t51_footer_at` 与 `t51_last_end`:
  **307,555 → 307,564**(client 31,947/31,956 不变)。
- 保留 `t92_why_before`:307,555 是**末行 body 结束 == footer 起点**,t51 冻结游标停在
  9B footer 之前;那 9 字节就是 footer `00 00 00 00 01 ec 7a e4 04`。
- t92 独立复核:`load_payload(server, table 9)[307555:307564]` 恰为该 footer。
- **同节其余键一字未动**:`closure_claims.table_9_server.payload` 与 `chains` 本来已是
  307,564(v11.2 内部不一致只存在于 t51 交叉校验这一处),此处如实记入 `t92_e127_note`。

### 3.2 `table45_structure_e132_e138` — 行分解 / 三列 / 访问器视图

- **行分解(E138,L2)**:`pre[0..36] 37B | [u32 namelen][utf8 name]@37 | tail 26B | identity 13B`,
  `rowlen == 80 + namelen` 普适。
- **t92 独立重算**(7.6MB payload + 337KB 起始表,84,477 行):
  bad_rowlen=0 / bad_identity=0 / rowlen 80..122(38 种)/ rec_type 37 种 /
  255=null 38,968 / **rt=8 共 3,391 行且 namelen 全 0**——与 E138 逐条吻合。
- **物理列 ~14 条**(8 前缀 u32 槽 + rt u8 + name + ~5 尾列),**装不下 117 字段**
  → 117 码是访问器视图。
- **三列(E132)**:u32@0=club-uid(96.7% 成员率)、u8@4=rec_type、u32@5=person-uid
  (外源锚 735216);未定列(@21/25 双写对等)原样搬运。
- **family↔rec_type(34 L3)**:CFG→24 / CHA→13 / CHS→25 / CLA→26 / CYP→10 / CYS→27 /
  COS→28;7 族 7 rt,**无族内冲突**(V5 与 `slots.json` 逐条比对通过)。
- `reader_off` 语义注明为**内存偏移**([rdi+0xNN]),wire_off 派生仍开放。

### 3.3 `t9_grammar_e133` — 头解码 + 闭包 + 双 lane

- 13B 头:magic `03` + `tad.` + `f1 0d` + **u32 count@+8 = 251**(两档),
  与 table_45 的 84,477 同构 → 共享 DATABASE_TABLE 约定。
- 闭包:client `13+28,922+12×251+9=31,956`;server `13+304,530+12×251+9=307,564`;
  body 长度 92 / 211 种(**server 211 种未解释,原样留 open**)。
- lane:ordinal 251/251、sentinel head `00 ff ff ff ff` 251/251。

### 3.4 `cbw_route_e135_e137` — 4CC 零存在 + tag 路由 + E121 降级

- **负结果原文保留**:CBDa/CBWa/CBWo/CHSo 四码字节串在 editor.exe(74.8MB)与
  fm.exe(491MB)**零出现**(cmp 立即数与原始引用皆无)→ E135 的 80 held 实质正确。
- 路由定性:**(rec_type, tag 序号) 位置路由**,4CC 只存在于 editor schema。
- **E121 降级注记**:`CBDa@0x11f0ca7 / CBWa@0x11f0cb6` 的 cmp 位点引用**无法按字节复现**
  → 记为 *unverified reference*,不再是证据;E121 的 table 定位判据本身不动。
- fix8 真 PE 节表入册:18 节,`.reloc` 45,639,506B 可执行大区,t89_disasm.py 的硬编码
  5 节表不再适用。

## 4 分母联动(`denominator_note.json`)

`reports/xml_denominator_coverage.json` v2 的 `re_routed_table_45` **117 条**逐条加注记:
`grade` 仍为 `L2_candidate`(**值不变**),新增 `grade_note`(accessor-view 模型已证,
per-suffix 列钉死待下波)、`grade_unchanged: true`、`note_ledger: [E132, E138]`。
`totals_after` 与 `unresolved_wire_slot` 原样复制供对账。**reports/ 未被写入**。

## 5 溯源与纪律

- 7 个输入源全部 SHA-256 钉死(`t92_source_snapshot`),E132–E138 逐条 claim SHA-256
  与 LEDGER 一致(V7)。
- 构建器 `scripts/t92_schema_v113.py`(新文件,`--selftest/--build/--denominator/--all`)。
- `reports/` 零写入;`LEDGER` 零写入;其他 `scratch/tNN/` 零写入(仅读)。
- 序列化对齐 reports/ 口径:indent=1 + CRLF、无尾换行;摘要仍用 t90 的 indent=2 口径
  (32 条既有 digest 只在 indent=2 下复现)——两种口径已在代码中分开注释。

## 6 未决(不裁决,交下波)

1. suffix → 物理列钉死(per-family reader_off 或值域匹配)。
2. reader_off(内存)→ wire_off 派生。
3. 80 held 码的 per-rec_type tag 序列 → 字段序 → wire 偏移(纯数据侧)。
4. t9 server 211 种 body 长度、24 个 helper 路由、row0 逐字节对账。
5. `.reloc` 大区的 fo↔VA 换算(PE 基建已有,扫描未做)。

## 7 复现

```
py -V:3.12 -I -B scripts/t92_schema_v113.py --selftest
py -V:3.12 -I -B scripts/t92_schema_v113.py --all
py -V:3.12 -I -B scratch/t92/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
