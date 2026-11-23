# t88-fix6 — 终装配棒:117 码 (rec_type,offset) 映射 + slots.json + 校验(资产全在盘,只做装配)

你是受指挥官委派的子代理,**全新会话**。前棒 fix5 已把 rec 结构定稿(5 节 done,与指挥官冻结三列自洽),你只做**最后装配**——所有重分析都已完成,禁止重做:

## 冻结资产(只读,直接用)

- `scratch/cmd/t88_rec_probe.json`(E132):u32@0=club-uid、u8@4=类型(37 值)、u32@5=person-uid、identity uid=行自键
- `scratch/t88/out3/rec_structure.json`(E134):5 节 done;prefix 37B=8 列
- `scratch/t88/out3/tcget2_dispatch.json`:80 4CC 一级骨架(entry 有 rec_type/inner_tag 两个 null 字段待填)
- `scratch/t88/out3/{type_layout,byte_profile,slot_domains}.json`、`scratch/t88/out3/recget_tagmap.json`
- `scratch/t88/{TC_GET2_4cc,record_get_tagmap,record_get_handlers,record_set_blocks,f4_to_rectype}.json`(t88 前作静态台账)
- `scratch/t88/out2/{row_frame,_starts,_p_server_45}`(载荷与行起点)
- `evidence/fm24/reports/editor_schema/master.json`:entities['club.xml'][0]['fields'][211:328] = 117 码(纯字符串列表)

## 任务(顺序;每步落盘;全部写 `scratch/t88/out3/`,新文件)

1. **10 分钟内**:写 `out3/slots.json` 骨架(117 码逐条占位,status=骨架)
2. **二级分发解析**:TC_GET2 @0x3ebad50 → RECORD_GET @0x1543ca0 的 case 体里,为每个 4CC 解出 rec_type(u8@4 的值)与 wire 偏移;已知的 80 码补全 rec_type/inner_tag;**CBW*/CBD* 主族(99 个缺失码)逐码定位**——cmp 指令(如 `cmp esi, 0x41576e69`)→ case 体 → [rec+X] 读取 → wire 偏移。产出并入 `out3/slots.json` 逐条:{code, rec_type, wire_off, width, grade, 判据(VA/fo/bytes 或数据侧)}
3. **数据侧验证**(程序化):对每个已映射 (code,rec_type,wire_off):抽该 rec_type 的行,核对值域合理(非全 ffff、宽度一致);wrong-club 控制(@0 不在 club 集的行)同报;`0xffffffff` 与合法 0 分列
4. `out3/domain_stats.json`(117 字段域统计摘要)+ `out3/verify.py`(独立重抽,≥5 项:117 覆盖数、抽样值域、wrong-club、行框不变式、E132 三列不变式)+ `out3/REPORT.md` + `out3/DONE.md`(首行 `DONE type=t88 status=complete`;若部分完成则 `status=partial` 列剩余)
5. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t88/out3/` 新文件与 `scripts/t88_*.py`;不修改既有文件;不碰 reports/、LEDGER、scratch/cmd/
2. **时间预算 40 分钟/attempt:每完成一个码组立即覆写 slots.json**;>20KB 不进会话;print ≤30 行/次;单次写 ≤120 行
3. 两轮定不出某码→标 held+首反例,跳下一个,不恋战;候选不写成结论
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored `D:/tmp2b/fm24/tools/python`
5. 编辑器静态只读:`D:/tmp2b/fm24/input/editor.exe`(SHA b82ebe8e...)

## 交付 scratch/t88/out3/

`slots.json`(117 码)、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`。
