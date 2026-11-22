# t89b — table_9 条目文法定型 + held 回填 + 双档对拍(Phase 1 已由指挥官裁决,禁重做)

你是受指挥官委派的子代理,**全新会话**。t89 前棒三次因 upstream 崩溃/墙放弃,但**Phase 1([NATION+0x108] 读链)指挥官已亲自裁决完毕**——本棒禁止重做 Phase 1,直接从其结论出发:

## 指挥官裁决(冻结,勿重证)

读 `scratch/cmd/t89_phase1_verdict.json`(全文):**[NATION+0x108] 容器类型 = NATION_T9 (table_9) 类**;nation getter @0x141043d22 调 `0x1410668f0`(=t9_get_impl 入口),setter @0x14104628a 调 `0x141063f30`(=t9_set_impl 入口),al=false 回落主行;T9 对象内存布局 begin/end 在 +0x4a0/+0x4a8,数据基 +0x18。

## 已冻结地基(直接用,不重做)

- 探针资产(只读,**全部 >20KB 禁止整读,grep/sed 程序化**):
  `scratch/t89/probe_t9_read.txt`(164K,reader 逐指令,VA=0x14105d510..0x14105fa40)——**Phase 2 条目网格的原料**
  `scratch/t89/probe_t9_get_impl.txt`(226K)与 `probe_t9_set_impl.txt`(175K)——**内部按 4CC 分发,每个 case 读/写容器内偏移,这就是 held 回填的 field→offset 映射原料**
  `probe_t9_write.txt`、`probe_t9_ctor.txt`、`probe_helpers.txt` 等
- `scratch/t85/out2/profile_nation.json`:table_9 行 0 body_head_hex 首反例 + 逐偏移 lane 域;framing:13B 头+变长体+12B identity 尾×251+9B 脚,client 31,956B / server 307,555B
- `scratch/t75/out/xref_reverse.json`(1.3MB 程序化):nation slots 里 getter_proven_but_no_main_row_sink 清单(nhrl 等)
- `evidence/fm24/reports/editor_schema/master.json`(程序化查):nation.xml 字段与 4CC
- 行 0 反例:`00 ff ff ff ff 01 01 01 00 00 00 0a 00 00 00 00 00 01 5c 05 00 00 00 00`

## 任务(微交付:每小节完成立即覆写落盘;全部写 `scratch/t89/out/`)

1. **10 分钟内**:把 `out/table9_grammar.json` 的 status 从 skeleton 改 in_progress 并落盘(骨架已在盘)
2. **Phase 2 条目网格**:从 probe_t9_read.txt 逐段还原 reader 的字节网格(fixed_head/变长体/尾部),解释 body 46..449B 与 92 种长度;与行 0 反例逐字节对账(对不上→held+差异字节标注,**不得改反例原文**)
3. **Phase 3 held 回填**:从 probe_t9_get_impl/set_impl 的 4CC 分发 case 提取 field→容器内偏移映射(区分**内存布局偏移**(容器+0x18 基)与 **wire 条目偏移**(载荷内),二者分开记录);nhrl 等逐字段过闸(L2/L3)或 held+首反例
4. **Phase 4 双档对拍**:client 31,956B / server 307,555B(body0 46 vs 1086)的静态解释(reader 里哪段逻辑产生此差)
5. `out/field_map.json`(回填增量)、`out/domain_stats.json`、`out/verify.py`(独立重抽,不 import builder)+ builder `scripts/t89b_*.py`(**新文件名前缀 t89b**);`REPORT.md` + `DONE.md`(首行 `DONE type=t89b status=complete`)
6. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t89/out/` 与 `scripts/t89b_*.py`;**不修改 scratch/t89/ 探针与前棒骨架之外的文件**;不碰 reports/、LEDGER、scratch/cmd/
2. `>20KB` 不进会话;print ≤30 行/次;单次写 ≤120 行;**每小节完成立即落盘**(防 mid-stream 死亡丢工)
3. 时间不够→已落盘小节保留 + `DONE status=partial` 列明剩余,**不静默放弃**
4. 负结果原样保留;候选不写成结论;两轮定不出→escalate 注记
5. 不启动游戏/编辑器/IDA,不联网,Z: 只读(editor.exe 只读,SHA b82ebe8e...)
6. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored `D:/tmp2b/fm24/tools/python`

## 交付 scratch/t89/out/

`table9_grammar.json`(补完)、`field_map.json`、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`。
