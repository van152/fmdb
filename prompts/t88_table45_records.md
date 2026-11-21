# t88 — server table_45 (STARTING_RECORD) 117 字段族 wire 槽位扫描(deepseek)

你是受指挥官委派的子代理。E121(t82)已把 `club.xml[211..327]` 的 **117 项记录族字段**(含 `CBWa/CBWc/CBWd/CBWf/CBWo`、`CBDa/CBDc/CBDd/CBDf/CBDo` 等 CB*/CBD*)正名到 **`server_db/table_45.dat`**(`DATABASE_TABLE<STARTING_RECORD>`,type 45,84,477 条记录):静态链 `TC_RECORD_GET @ 0x3ebad50` / `TC_RECORD_SET @ 0x3ebaf50` → `RECORD_GET @ 0x1543ca0` / `RECORD_SET @ 0x1544c80`,按 `[rec+0x4c]==[CLUB+0xc]` 且 `[rec+0x5e]==rec_type` 匹配。本任务把这 117 个字段的 wire 槽位扫出来。

## 已冻结地基(直接用,不重做)

- `scratch/t82/out/xref_extra3.json` + `REPORT.md`:静态链地址、`mov edx,0x2d @ 0xf06c70..84`、RTTI `.?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@`、`[rec+0x4c]/[rec+0x5e]` 匹配语义
- `evidence/fm24/reports/editor_schema/master.json`:`entities['club.xml']` 的 211..327 字段清单(type/dependencies)+ `enums` + `field_codes`(程序化查,不整读)
- `scratch/t74/out/frames.json`:行框方法论(定长/顺序语法/identity DP 三模型)
- 成员寻址:E80 口径(member start = data_base(34)+entry.offset,`len==size` 选帧);`scripts/t71_club100_cnst.py` 的 archives() 目录遍历可 runpy 复用(不得修改)
- 分母:`reports/xml_denominator_coverage.json`(club unresolved_wire_slot 明细,t88 的字段集=其中被 re-route 的 117 项)

## 任务

1. **行框自证**:table_45 server 载荷(7,608,748B,84,477 条)定行结构——定长 or 变长,identity 三元组位置(t74 判据 A/B 同法自证);client 档是否有 table_45 条目(有则双档对拍,无则如实记 server-only)
2. **rec 结构**:按静态匹配语义找 `[rec+0x4c]`(=club UID/ordinal?)与 `[rec+0x5e]`(rec_type)的 wire 位置;84,477 条对 84,259 club 的关系(1:1?多条 per club?rec_type 枚举?)要给出数据判据
3. **117 字段槽位对齐**:master 字段按 type 宽度 × 值域 × 4CC gate(t82 的 TC_RECORD_GET 内部 switch 分发)给候选;数据侧判据=L2;冻结锚点冲突=回查;wrong-UID 控制同报
4. **分域验证**:全档向量化(84,477 行);`0xffffffff` 与合法 0 分列;日期槽按 date4 sentinel 分列
5. 过闸=L2/candidate(数据侧);t82 已定的 4CC 身份可直接引用(标注 provenance);**不发明业务名**;两轮定不出标 escalate(下一轮 neon 静态收)
6. `verify.py`(独立重抽)+ builder `scripts/t88_*.py`;`--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7

## 避坑纪律

1. 只写 `scratch/t88/` 和 `scripts/t88_*.py`;不碰 reports/、LEDGER、t82/t74/t71 文件
2. `>20KB` 文件不进会话上下文;程序化处理,print ≤30 行/次;单次文件写 ≤120 行
3. 负结果原样保留;候选不写成结论
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t88/out/

`row_frame.json`(行框+identity 自证)、`rec_structure.json`(+0x4c/+0x5e 位点与 club 对应关系)、`slots.json`(117 字段逐条:offset/width/grade/判据)、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t88 status=complete`)。
