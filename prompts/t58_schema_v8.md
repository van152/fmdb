# t58 — Schema v7→v8 合并:t57 club 主行普查并入(luna)

你是受指挥官委派的子代理,做**谨慎的合并**任务。当前公共 schema 为 **v7**(E96)。t57(E97,**L3 验收**)完成 club table_3 主行槽位普查,并入为 **v8**,保护节 verbatim 只做增量:

1. **club_main_row_fields 节**(t57):双档行框闭合(client 6,932,082/server 16,595,312,84,259×2,identity **12B**、footer e3c03a77);CLUB 主 reader slot19 `0xe5a7a0` extent 1,412 指令/167 分支;34 逻辑位置;433 occurrence→grade_counts {L3:13,held:11,skipped_separate_member:10,unmapped:399};13 L3(新增 Cext/Cedp/Cncl/CIns/Ctsi + duni/Cnti/Cbni/Cccn/Ccty/CASt/Csot/CnCV);**72 对倒置**(首例 Cext pos3/xml13 vs Cnam pos10/xml6);held 首反例(Csnm 537 越界、CLat/CLon、Csti、Cyfn=extra+0xd8 等)逐条保留;E60 Cccn negative 原文保留+真绑定 +0xf0 注记。
2. **行框口径**:identity tail 宽度按表自证(nation 13B/club **12B**)——在 `nation_coverage_policy` 旁新增(或复用)口径注记:任何表不得照抄他表 identity/footer 宽度。
3. coverage:club 侧新增 `club_main_row_L3`(13)等分项,**既有 club_L3_occurrences 94 等子表计数不动**(主行层与子表层分开计);provenance 增 t57(E97,L3,条目级守卫扩至 E87–E97)。
4. `tables` 8 表、`negative_regressions`、`v3_baseline`、`club_auxiliary_sources`、`nation_*` 各节 verbatim 不动。

## 必读
- AGENTS.md;reports/club_nation_subtable_schema.json+.md(**v7 基线**,E96)
- scratch/t57/out/field_slots.json + field_map.json + REPORT.md + DONE.md
- scratch/t56/out/consolidate_v7.py + verify.py(方法复刻;ledger 守卫**条目级**)
- scratch/t01/LEDGER.json(E87–E97)

## 任务
1. `schema_version: 8`;按上述增量;markdown 同步;独立 spot(条目级守卫+v7 快照 SHA+保护节+t57 数字断言:6932082/16595312/84259/13 L3/72 倒置/69705 反例);anchors 7/7;--help/--selftest;退出码 0/1/2。
2. 候选不写结论;t57 held/unmapped 原样;不改 scratch/t47–t57;BASELINE.md 指挥官另行。

## 交付 scratch/t58/out/
- consolidate_v8.py、verify.py、spot_*.log、REPORT.md、DONE.md;reports/ 两文件升 v8

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + t01_anchors.py(7/7)。
