# t88-fix5 — table_45 槽位 join(指挥官已定位三列,本棒只做 per-4CC 映射)

你是受指挥官委派的子代理,**全新会话**。rec 结构三列已由指挥官数据侧探针定位并冻结(`scratch/cmd/t88_rec_probe.json`,先读它,**禁重做**):

- **u32@0 = club-uid**(96.7% 对 club 主表 84,259 uid 集;8,368 club 实际出现)
- **u8@4 = 类型字节**(37 值,255=null×38,968)
- **u32@5 = person-uid**(外源锚定:C罗 735216×18)
- 行=(club,person) 记录;identity uid 为行自键(致密 0..89,974)
- 前提修正:「84,477=84,259+218」已否证,勿再沿此叙事

## 任务(全部写 `scratch/t88/out3/`;每小节完成立即覆写落盘)

1. **10 分钟内**:覆写 `out3/rec_structure.json`(把指挥官五列结论+你的静态验证并入,status=in_progress→各节 done)
2. **静态补强 rec 列**(轻量):在 `scratch/t88/record_get_tagmap.json`/`TC_GET2_4cc.json`/`record_set_blocks.json` 中找 [rec+0x4c]/[rec+0x5e]/person 链的 4CC 分发与 wire 位点对应关系(只 grep 定点,不整读)——给指令三件套 VA/fo/bytes
3. **117 字段 join**:club.xml[211..327] 逐 4CC → (u8@4 的哪个 type 值, 行内 wire 偏移)。方法:t82 的 TC_RECORD_GET 分发按 4CC 选 rec_type;对每个 4CC 找其 case 里的 [rec+X] 读取偏移,再对到 wire(前缀固定区 0..36 或 name 后/尾部锚定);数据侧验证=对该 (club,type) 行抽样核对值域;`0xffffffff` 与合法 0 分列;wrong-club 控制(用 @0 不在 club 集的 399 值行)同报
4. `out3/slots.json`(117 字段:offset/type/grade/判据/provenance)、`out3/domain_stats.json`
5. `out3/verify.py`(独立重抽)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t88 status=complete`)
6. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t88/out3/` 和 `scripts/t88_*.py`(新文件);不修改既有文件;不碰 reports/、LEDGER、scratch/cmd/
2. `>20KB` 不进会话(tagmap/载荷全程序化);print ≤30 行/次;单次写 ≤120 行;**每小节完成立即落盘**
3. 时间不够→已落盘小节保留 + `DONE status=partial` 列剩余项,不静默放弃;两轮定不出→escalate 注记
4. 负结果原样保留;候选不写成结论
5. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored `D:/tmp2b/fm24/tools/python`

## 交付 scratch/t88/out3/

`rec_structure.json`(补完)、`slots.json`、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`。
