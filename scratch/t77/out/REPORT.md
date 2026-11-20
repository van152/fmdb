# t77 — schema v10 → v11 模块化合并 + 仓库治理

日期 2026-11-21 · 分支 `t70-schemav10`(线性链)· Python `py -V:3.12 -I -B` · **L4 = 0**

## 结论

E111–E120 十个验收包已**纯增量**并入公共 schema v11,仓库治理(体积拆分、`nul` 清理、
三份文档同步、merge-to-main 评估)完成。既有 v10 内容**逐字节保留**:22 个根节在
`--verify` 中逐一 `==` 比对全等,根键新增 10 个、删除 0 个,既有 coverage 数字只改
`club_main_row_L3`(21→43)。

三档自检:`--selftest` 7/7、`--build` 4/4、`--verify` **63/63**,退出码均为 0。
回归:`t01_anchors.py` 7/7、`baseline_coverage.py --check` 冻结数字不变。

## 交付

| 文件 | 体积 | 说明 |
|---|---:|---|
| `reports/club_nation_subtable_schema.json` | 29,884,088 B | v11;36 个根键 |
| `reports/club_nation_subtable_schema.md` | 87,373 B | 77,028 B 的 v10 字节作**严格前缀** + t77 附录 |
| `reports/other_tables_schema.json` | 286,605 B | **新**:13 张非主表槽位裁决 |
| `reports/xml_denominator_coverage.json` | 297,905 B | **新**:1,034 occurrence 分母台账 |
| `README.md` / `docs/REPO_STATUS.md` / `docs/BASELINE.md` | — | v11 增量同步(E 号引用,历史段落未改) |
| `scripts/t77_common.py` `t77_sections_a.py` `t77_sections_b.py` `t77_build.py` `t77_assemble.py` `t77_other_tables.py` `t77_denominator.py` `t77_md.py` `t77_verify.py` `t77_schema_v11.py` | 10 个文件 | 入口 `t77_schema_v11.py`(`--build/--verify/--selftest`) |
| 根目录 `nul` | 0 B | **已删除**(Windows 保留名事故产物;`.gitignore` 早已覆盖) |

JSON 体积从 29,511,808 B → 29,884,088 B,**只增 372,280 B(+1.26%)**:十个新节中
只有 `stadium_team_l3`(57 KB)与 `scan_tables`(84 KB)带实体内容,其余为紧凑摘要或指针;
分母全账本与 13 张非主表结论都拆到独立文件。

## 十一节并入内容(节名 → E/任务 → 验收要点)

| 节 | E / 任务 | 等级 | 内容摘要 |
|---|---|---|---|
| `club_extra_object_row` | E111 / t71 | L3 | `CLUB+0x100` = `table_extra_3.dat` 双档行框(client 12+13,053,896+0 = 13,053,908;server 12+35,009,236+0 = 35,009,248;84,259×2 行);**24 条 held 转正**(22 cnst 投影 + `Cebd` + `Cyfn`);club 主行 L3 21→**43** |
| `slot_fingerprints` | E112 / t72 | L2 | club 34 / comp 84 / nation 40 槽(未命名 20/36/24);10 项 nation 内层文法升级移交 t75;**partial,不言称闭合** |
| `simple_tables` | E113 / t73 | L2 | city(2)/continent(5)/region(19)/currency(41) **8/8 帧闭合**;10 个 distinct L2 三元组;冻结锚点 14/0 冲突;alias group 否定结果原文保留 |
| `nation_segment_grammars` | E114 / t75 | L3 | 10 段内层文法,8 段字节级闭合,`slot_2`/`slot_3` 无真项保持 held |
| `xref_reverse_adjudication` | E114 / t75 | L3 | 99 槽逐条裁决(nation 34 / comp 40 / club 25 held),**新具名 L3 = 0**;t71 的 24 个 4CC 排除不重复计 |
| `row_frames9` | E115 / t74 | L2 | 9 表 × 2 档 = **17 个 (archive,table) 行框闭合,0 escalations**;team(24) client 条目按 t66 **真缺失**(如实记录) |
| `xml_denominator_coverage` | E116 / t78 | L1 | 指针节:1,034 occurrence,物理覆盖 **110/1034 = 10.6%**;全账本在拆分件 |
| `stadium_team_l3` | E117 / t79 | L3 | stadium.xml 41 L3 / team.xml 11 L3 / `table_extra_24` 3 映射字段 / club `+0x18` 转发 6 字段 held→L3 |
| `scan_tables` | E120 / t76a + E118 / t76c | L2 | stadium **12 client / 47 server 槽,0 未覆盖字节**,verify 49/49;derby 10 / weather 25 / local_region 11 / agreement 9 槽,8/8 档闭合 |
| `pointer_artifacts` | — | — | 两个拆分件的 path + SHA-256 + 体积,`--verify` 重算比对 |

`scan_tables` 不含 award / language / media:t76b 三连墙零落盘已弃,这三表在
`other_tables_schema.json` 中标 `slots_status: pending:t76b(由 t83 接收)`,只带 t74 行框。

## 体积治理(为什么拆)

v10 主 JSON 达 29.5 MB,体积来自内嵌批量记录(`nation_t9_wire` 1.27 MB、
`comp_collections` 4.10 MB、r2 的 held/unmapped 清单)。v11 **不碰这些既有节**(逐字节保留),
而是让本轮新增内容指针化:

- `reports/other_tables_schema.json` — 13 张非主表槽位裁决(t73 4 + t76a 1 + t76c 4 + t74 行框 4),286 KB
- `reports/xml_denominator_coverage.json` — 1,034 条 occurrence,逐条含 `evidence_ref`,298 KB

主 schema 的 `pointer_artifacts` 与 `coverage` 双处记 path + SHA-256。

## 守卫与证据等级

- **条目级 ledger 守卫**:E111–E120 十条按 `id + kind + level + canonical claim SHA-256` 钉死
  (`PINNED_LEDGER`),claim 文本被改写即构 `--verify` 失败。
- **E119 是 `probe_negative`,不是验收**:t80 枚举增补前提证伪(快照与 master 枚举 100% 恒等),
  车道裁撤。v11 如实记为负结果探测。
- **E116 是 L1**:只用冻结产物做账,不读 `.dat`、不反汇编。
- **E121 明确不在本版**:t82 的 `table_extra_3` 双对象闭合(35 新 L3 / 39 held /
  `table_45` 117 字段族正名)在本车道离场后入账,归 **t87** 补丁;`incremental_provenance`
  的 `out_of_scope_note` 已写明。
- **L4 = 0**:全程未启动游戏/编辑器/IDA,未解任何 `.dat` payload。

## 诚实负结果清单(原样带进 v11,未润色)

1. E113 alias group:固定步长简单表 `header_origin_data_unique` 全 False → **数据侧无法判定
   header 起源**,结论保持"否定"。
2. E113 计数口径:claim 写 17 个 L2 槽,产物枚举 10 个 distinct (表,字段,offset) 三元组、
   覆盖 14 条 archive 级记录。两个数字都发布,差额作为**开放记账项**记录(见
   `simple_tables.L2_slots.count_note`),不做平滑。
3. E114:99 槽裁决**新具名 L3 = 0**,是负结果,不是"部分成功"。
4. E112:partial 交付,明确不宣称槽位闭合;t72 车道的 verify.py/REPORT/DONE 因墙钟被杀未交付,
   已在节内如实注明。
5. E115:team(24) 的 client 条目是**真缺失**(t66 记录,双档目录 460 条目 client 侧缺该 entry),
   按"absent"记,不按"未映射"记。
6. t76b:三连墙零落盘,award/language/media 三表槽位**无结论**,标 `pending`,不臆测。

## 文件写纪律

单次写入 ≤120 行;`reports/*.json` 全部由 builder 生成(不手写大 JSON);
`reports/*.md` 由 v10 字节 + 追加附录构成,不做整文件重写。

## 命令

```powershell
py -V:3.12 -I -B scripts/t77_schema_v11.py --selftest   # 7/7
py -V:3.12 -I -B scripts/t77_schema_v11.py --build      # 写 4 个报告 + diff summary
py -V:3.12 -I -B scripts/t77_schema_v11.py --verify     # 63/63,只读
py -V:3.12 -I -B scripts/t01_anchors.py                 # 7/7
py -V:3.12 -I scripts/baseline_coverage.py --check      # 冻结数字不变
```
