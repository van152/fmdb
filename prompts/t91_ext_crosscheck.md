# t91 — 外源仓库对照:nottatdat/fm-data 的码表/哨兵/文法 vs 我们的 FM24 解码(假设源,不升等级)

你是受指挥官委派的子代理,**全新会话**。用户提供外部仓库 `github.com/nottatdat/fm-data`(FM26/27 提取工具+逆向报告),已克隆至 **`scratch/ext/fm-data/`(只读,commit d7a7150,2026-11-11)**。他们逆向了 FM26 同族容器(tad.+zstd)与 people/summary 表。本任务做三件对照:**外部知识只是假设源,一切结论必须过我们自己的闸;外部标签永不升级我们的 L1/L2/L3 分级**。

## 外源关键情报(已由指挥官预读,直接引用)

- 报告:`scratch/ext/fm-data/docs/reports/agentA-native-re.md`(容器+RTTI+字段字典)、`agentB-people-db.md`(people 记录)、`agentC-summary-db.md`(summary/basic 表)
- **字符串文法**(agentB):`[u32 len][utf8 name][u16 doy][u16 year]`,内联串前置 sentinel `ff ff ff ff 00`——与我们 t88 row+37 `[u32 len][utf8]` 同族,可独立印证
- **空日期常量**:`01 00 6c 07` = (u16 doy=1, u16 year=1900);DOB 编码=(u16 day_of_year, u16 year)
- **id 双写**:person id 相邻重复 u32 对(印证我们 identity `[uid][uid]` 双写)
- **值域假设**(agentC,FM26):CA=u16 0..195、age=u8、位置=u32 位掩码(bit 表见 agentC §position)、summary_u32_a≈nation id(216 值)
- **people 表按 nation_ref 分组排序**——对照我们 table_9(251 行 nation 域)的行序假设
- **field_dict.csv**:2103 条 (table, db_field, label),FM26 editor.fmf 提取,码空间与我们 master.json 同族

## 任务(全部写 `scratch/t91/out/`;每节完成立即落盘)

1. **10 分钟内**落 `out/code_coverage.json` 骨架
2. **码表对拍**:`scratch/ext/fm-data/docs/reports/agentA-native-re.md` 引用的 field_dict.csv 实际位于他们 work/(不在克隆内)——**改为从 agentA 报告 §3 的码表样例+`fm26/offline/` 源码内嵌字段清单**提取;与 `evidence/fm24/reports/editor_schema/master.json` 全码表 diff:①我们有没有、他们没有 ②他们有、我们没有 ③双方都有但标签/表域冲突。产出三清单+计数(注意 FM26≠FM24 码表版本漂移,冲突列不改判)
3. **空日期探针**:`01 00 6c 07` 全档扫描(用 `scripts/t71_club100_cnst.py` archives() 或 fm24_dump 载荷,程序化):在我们已解码表的 date4/日期类槽位命中率 vs 随机 4 字节对照;命中槽位列清单;与现有 date4 sentinel 分列口径对照(不推翻,只增证据)
4. **文法印证**:用我们的 t88 行框(row+37 [u32 len][utf8])与 t84 name pools、identity [uid][uid] 双写,逐条对照 agentB/agentC 的同族模式,产出 `out/hypotheses.md`(每条:外源主张/我们现状/一致性/需补的验证)
5. `out/verify.py`(独立复算 ②③ 的计数)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t91 status=complete`)
6. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. **外部代码一律不执行**(fmdb.py/parse_people.py 等只读源码,不运行);我们数据用我们自己的加载器
2. 只写 `scratch/t91/out/` 和 `scripts/t91_*.py`;不碰 scratch/ext/(只读)、reports/、LEDGER、其他 tNN
3. `>20KB` 不进会话(master.json、xref_reverse 程序化);print ≤30 行/次;单次写 ≤120 行;每节完成立即落盘
4. 外源标签一律标 `provenance=ext/fm-data@d7a7150`,不得写入 reports/ 或 LEDGER(指挥官验收时定夺);候选不写成结论
5. 时间不够→已落盘小节保留 + `DONE status=partial` 列剩余,不静默放弃
6. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored `D:/tmp2b/fm24/tools/python`;不联网(克隆已在盘)

## 交付 scratch/t91/out/

`code_coverage.json`、`nulldate_probe.json`、`hypotheses.md`、`verify.py`、`REPORT.md`、`DONE.md`。
