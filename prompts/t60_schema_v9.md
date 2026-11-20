# t60 — Schema v8→v9 合并:t59 comp 主行普查并入(luna)

你是受指挥官委派的子代理,做**谨慎的合并**任务。当前公共 schema 为 **v8**(E98)。t59(E99,**L3 验收**)完成 comp table_25 主行槽位普查,本任务并入为 **v9**,保护节 verbatim 只做增量:

1. **comp_main_row_fields 节**(t59):双档封口(client 13+894,969+9=894,991 / server 13+1,533,950+9=1,533,972,7,047×2 行);identity **12B**(dsha ordinal|duni uid|saved rdui==duni)+ footer 9B `00000000|01|4ec43a77`;client 定宽 127B 行(server 条件模板 77–82 站点,联合 **82 观测**+2 静态未触发,field_slots 84 记录);COMP 真 slot19 `0xeb7000`(extent 837 指令/114 分支)与工厂 case25 双对象形态(db::COMP `0x14187dcb8` / DATABASE_TABLE<COMP> `0x14187f6d8`,**不合并**);255 occurrence→grade_counts {L3:49,held:10,unmapped:196},**26 个新 4CC**(LAUC、cext/cusn/culn bit 投影、22 个 cnst 投影 Pcsp..Pcsy/Pcjm..Pcsc);**818 对倒置**(首例 duni/cfcl xml[1,12] exec[81,4]);引用域 ccti→t5(6,981/66/0)、cnti→t10(6,769/278/0)、cpcm→t25 自引(3,506/3,541/0)、cnor/csou/cwes/ceas→t2,全零违例;held 首反例(dbty/Ctty/PLgn/CpRp/rdui/cnam/csnm/c3ln/VARt/HKEt)与 unmapped 逐条原样;status=partial_schema_join;L4=0。
2. **行框口径**:在既有口径旁注记第三例——comp identity 12B+footer 9B,与 nation 13B/club 12B 并列,**按表自证不得照抄**(既有文字不动)。
3. coverage 新增 `comp_main_row_*` 分项(occurrences 433→同口径 255、L3 49、held 10、unmapped 196、inversions 818、aligned 54);**既有 club/nation 全部计数不动**;provenance `tasks` 增 t59(E99,L3),条目级守卫**扩至 E84–E99**(逐条 id+claim canonical SHA+kind/level,不钉全文件;E100 及以后不守卫)。
4. `tables` 8 表、`negative_regressions`、`v3_baseline`、`club_auxiliary_sources`、`club_main_row_fields`、`nation_*` 各节 verbatim 不动;`generated_by` t58→t60。

## 必读
- AGENTS.md;reports/club_nation_subtable_schema.json+.md(**v8 基线**,E98)
- scratch/t59/out/field_slots.json + field_map.json + REPORT.md + DONE.md
- scratch/t58/out/consolidate_v8.py + verify.py(方法复刻;条目级守卫口径)
- scratch/t01/LEDGER.json(E84–E99)

## 任务
1. `schema_version: 9`;按上述增量;markdown 同步(v8 md 为前缀);独立 spot(条目级守卫+v8 快照 SHA+保护节+t59 数字断言:894991/1533972/7047/12B/9B footer/49 L3/26 新 4CC/818 倒置/82 站点);anchors 7/7;--help/--selftest;退出码 0/1/2。
2. 候选不写结论;t59 held/unmapped 原样;不改 scratch/t47–t59;BASELINE.md 指挥官另行。

## 交付 scratch/t60/out/
- consolidate_v9.py、verify.py、spot_*.log、club_nation_subtable_schema.v8.json/.v8.md 快照、REPORT.md、DONE.md;reports/ 两文件升 v9

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
