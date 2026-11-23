# t88-fix2 — table_45 槽位 join 续作(全新会话;行框已闭合冻结,本会话只做 rec 结构+117 字段 join+装配)

你是受指挥官委派的子代理,**全新会话**。t88 链前作已交付并冻结**行框**(`scratch/t88/out2/row_frame.json`,只读引用,不得修改):

- server `table_45.dat`:7,608,748B,84,477 条,**变长行 80..122B(38 种长度)**,`rowlen == 80 + namelen`
- 行头 `row+37` 嵌 `[u32 len][utf8 name]`;identity 13B 在 `row_end-13`:`[ordinal u32][uid u32][uid u32][tail=0]`,判据 A/B 双过,DP unique_paths=1
- client_db 无 table_45 条目(server-only);row 起点 offsets 已在 `out2/_starts.bin`,解压载荷在 `out2/_p_server_45.bin`
- 前作静态资产(只读):`scratch/t88/TC_GET2_4cc.json`、`TC_SET2_4cc.json`、`record_get_handlers.json`、`record_get_tagmap.json`、`record_set_blocks.json`、`f4_dispatch.json`、`f4_to_rectype.json`、`club.json`、`colstat.json`、`disp4c_sites.json`
- 静态锚点(t82,E121):`TC_RECORD_GET @ 0x3ebad50` / `TC_RECORD_SET @ 0x3ebaf50` → `RECORD_GET @ 0x1543ca0` / `RECORD_SET @ 0x1544c80`,匹配语义 `[rec+0x4c]==[CLUB+0xc]` 且 `[rec+0x5e]==rec_type`

## 任务(顺序,每步落盘;全部新文件写 `scratch/t88/out3/`)

1. **10 分钟内先落** `out3/rec_structure.json` 骨架(meta+status)
2. **rec 结构**:把 `[rec+0x4c]`(应=club UID)与 `[rec+0x5e]`(rec_type)对到**行内 wire 偏移**(注意:C++ 结构偏移≠wire 偏移,要给指令证据或全档统计判据);84,477 条 vs 84,259 club——多出的 218 条是什么?给 rec_type 分布
3. **117 字段 join**:用 `record_get_tagmap.json`/`TC_GET2_4cc.json` 的静态映射,把 master.json club.xml[211..327] 字段对到行内偏移;数据侧=L2/candidate;wrong-UID 控制同报;`0xffffffff` 与合法 0 分列;日期槽按 date4 sentinel 分列
4. **全档向量化**:84,477 行逐字段域统计(程序化,print ≤30 行/次)
5. `out3/verify.py`(独立重抽,不 import 前作 builder)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t88 status=complete`)
6. 跑 `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t88/out3/` 和 `scripts/t88_*.py`(**新文件**);不修改 scratch/t88/ 与 out2/ 既有文件;不碰 reports/、LEDGER、t82/t74/t71
2. `>20KB` 文件不进会话上下文(含 `_p_server_45.bin` 7.6MB、tagmap 等一律程序化处理);print ≤30 行/次;单次文件写 ≤120 行
3. 负结果原样保留;候选不写成结论;两轮定不出→`escalate` 并写 `DONE status=partial`,不静默放弃
4. 自检:发现自己在整读大文件→立即停止,换程序化
5. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored 于 `D:/tmp2b/fm24/tools/python`(`-I` 下先 sys.path.insert)

## 交付 scratch/t88/out3/

`rec_structure.json`、`slots.json`(117 字段逐条:offset/width/grade/判据)、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`。
