# t88-fix3 — table_45 rec 结构+槽位 join(微交付续作;前两棒骨架与静态台账已在盘)

你是受指挥官委派的子代理,**全新会话**。前棒(t88-fix2)三次尝试因 upstream mid-stream 崩溃中断,**盘上进度完好,接着做,不要从头开始**:

- `scratch/t88/out3/rec_structure.json` 骨架已落(status=in_progress,pending 清单在内)——**本棒第一步就是把它做完**,做完一节立即覆写落盘一节
- 行框冻结:`scratch/t88/out2/row_frame.json`(80..122B 变长,rowlen=80+namelen,[u32 len][utf8 name]@row+37,identity 13B@row_end-13 tail=0,84,477 行,server-only)——沿用,不重算
- 静态台账(只读):`scratch/t88/record_get_tagmap.json`、`record_get_handlers.json`、`record_set_blocks.json`、`TC_GET2_4cc.json`、`TC_SET2_4cc.json`、`f4_to_rectype.json`、`rt_tag_fields.json`、`tag_offsets.json`;静态锚点 `TC_RECORD_GET @ 0x3ebad50`/`RECORD_GET @ 0x1543ca0`/`RECORD_SET @ 0x1544c80`,匹配语义 `[rec+0x4c]==[CLUB+0xc]` 且 `[rec+0x5e]==rec_type`
- 载荷:`scratch/t88/out2/_p_server_45.bin`(7.6MB)+ `_starts.bin`(行起点);`evidence/fm24/reports/editor_schema/master.json` 程序化查 club.xml[211..327]

## 任务(微交付:每小节做完立即覆写落盘,进度永不回退)

1. **先做** `out3/rec_structure.json` 里 status=in_progress 的 pending 项,逐项完成逐项覆写:
   a. rec_type 的 wire 偏移 + 全档分布(84,477 行)
   b. `[rec+0x4c]`(club UID)与 `[rec+0x5e]`(rec_type)的 C++ 结构偏移→wire 偏移对照(指令证据或全档统计判据,二者取一并注明)
   c. 84,477 vs 84,259 club:多出 218 条的归属
2. **再做** `out3/slots.json`:117 字段 join(用 tagmap/TC_GET2 静态映射→行内偏移;L2/candidate;wrong-UID 控制;`0xffffffff` 与合法 0 分列;日期槽 sentinel 分列)
3. `out3/domain_stats.json`(全档逐字段域统计,程序化)
4. `out3/verify.py`(独立重抽)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t88 status=complete`)
5. `scripts/t01_anchors.py`(7/7)

## 避坑纪律(与前棒相同,特别防 mid-stream 死亡丢工)

1. 只写 `scratch/t88/out3/` 和 `scripts/t88_*.py`(**新文件**,不修改既有文件);不碰 reports/、LEDGER、t82/t74/t71
2. **每完成一个小节立即覆写目标文件**(哪怕只有一节),不攒大块;单次写 ≤120 行
3. `>20KB` 不进会话(载荷与 tagmap 全部程序化);print ≤30 行/次
4. 负结果原样保留;候选不写成结论;时间不够→把已完成小节落盘后写 `DONE type=t88 status=partial` 说明剩余项,**不静默放弃**
5. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored `D:/tmp2b/fm24/tools/python`

## 交付 scratch/t88/out3/

`rec_structure.json`(补完)、`slots.json`、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`。
