# t92 — schema v11.3 候选装配(机械合并:E132–E138 六条更正/增量 + E127 九字节修正)

你是受指挥官委派的子代理,**全新会话**。t90 已立 v11.2;本轮把 t88 链收束成果合入出 **v11.3 候选**。**只装配,不改判**,全部结论以 LEDGER 各条为准。

## 输入(全部只读)

- 基线:`reports/club_nation_subtable_schema.json`(**v11.2**,40 根节;**禁止修改 reports/**);构建器范式 `scripts/t90_schema_v112.py`(可读,不得修改)
- **E133 修正**:`scratch/t89/out/verify.py` V1 钉死——`table9_closure_e127` 的 server 307,555 → **307,564**(九字节误差;client 31,956 不变)
- **E132/E138 增量**:table_45 结构定论——uniform 行分解(pre37B+name+tail26B+identity13B,rowlen=80+namelen 普适)、三列(u32@0=club-uid、u8@4=rec_type 37 值、u32@5=person-uid)、**117 码=访问器视图(family→rec_type:CFG→24/CHA→13/CHS→25/CLA→26;34 L3 见 `scratch/t88/out3/slots.json`)**
- **E135/E136/E137 更正**:CBW*/CBD* 族 4CC 字节在 editor.exe 与 fm.exe **零存在**(指挥官全量扫描)→ 走 tag 位置路由;**E121 negative_proof 的 cmp 位点引用(CBDa@0x11f0ca7)降级为未验证**;fix8 `scratch/t88/out3/pe_sections.json`(真 PE 节表,45MB .reloc 可执行区)一并引用
- **E133 t9 文法增量**:载荷头 13B 解码(u32 count@+8=251,与 table_45 84,477 同构)、ordinal lane 251/251、sentinel head 251/251、server body 304,530(211 种长度)
- 台账:`scratch/t01/LEDGER.json` E129–E138(程序化查)

## 任务(顺序,每步落盘;全部新文件写 `scratch/t92/out/`)

1. **10 分钟内**:落 `out/schema_v113.json` 骨架(meta+status,结构对齐 v11.2 根键)
2. **修正与增量**:① `table9_closure_e127` server 值改 307,564(留 `why_before` 注记);② 新增节 `table45_structure_e132_e138`(行分解/三列/访问器视图模型/family↔rt 表);③ 新增节 `t9_grammar_e133`(头解码+闭包+ordinal/sentinel lanes);④ 新增节 `cbw_route_e135_e137`(4CC 零存在负结果+tag 路由定性+E121 引用降级注记);⑤ `schema_version` → 11.3-candidate、`generated_by` → t92、`incremental_provenance` 追加 E132–E138 快照
3. **分母联动**:`reports/xml_denominator_coverage.json` v2 的 `re_routed_table_45` 117 条 grade 注记更新为「accessor-view 模型已证,per-suffix 列钉死待下波」(值不变,只加注记字段)——产出 `out/denominator_note.json`
4. `out/verify.py`(独立,≥6 项:v11.2→v11.3 diff 全溯源、E127 修正前后值核对、新增节计数、根节不变式、family↔rt 表与 slots.json 一致性)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t92 status=complete`)
5. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t92/out/` 和 `scripts/t92_*.py`(新文件);**禁止写/改 reports/、LEDGER、其他 scratch/tNN/**(reports/ 合并在指挥官验收时做)
2. `>20KB` 不进会话(master.json 30MB 级、schema 30MB 全程序化);print ≤30 行;单次写 ≤120 行;每节完成立即落盘
3. 冲突不裁决,escalate 注记;负结果原样保留;候选不写成结论
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored

## 交付 scratch/t92/out/

`schema_v113.json`、`denominator_note.json`、`diff_inventory.json`(verify 产出)、`verify.py`、`REPORT.md`、`DONE.md`。
