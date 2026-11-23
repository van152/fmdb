# t46 — nation server table_10 数据侧画像(t25 client grammar 参照,备 sol server 攻坚)

你是受指挥官委派的子代理。t25 已闭 **nation client table_10** 坐标(复杂变长 4 段计数循环),但 **server table_10 grammar 仍开**(t25 明确"no formula extrapolation to server")。本任务做 **server 侧数据画像**,为 sol 静态 server grammar 攻坚备料。**只数据侧 L1/L2,不晋级 L3,不重跑 client。**

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束)
- scratch/t25/out/cursor_nation.json + REPORT.md(**client grammar 真源,参照不外推**:prefix25B,A=signed i8 count@row+24/items5B,B/C=signed i32 count/items28B,D=signed i32 count/items12B,identity ordinal|id|repeated;client 251 行 24732B SHA7e9d740b,collection A492/B214/C63/D162)
- scratch/t25/out/schema_split.json(client_direct/inherited_list_item/server_only_explicit/unknown_unmarked codes)
- scratch/t37/out/nation_subtable_inventory.json(nation 上下文)
- scripts/t38_multiframe.py(load_payload_mf 参考)+ scratch/t38/out/REPORT.md(**E80:成员起点=data_base34+offset,按 entry.size 选帧,entry.sha256=压缩区 SHA**)

## 任务
1. 两 archive 目录+payload:nation table_10 client/server 是否存在/count/payload SHA(多帧感知,按 size 选);server 无成员如实记。
2. **server table_10 独立画像**(不套 client 公式):逐行结构剖析,prefix/各段 count 位置与符号性/item 宽度/identity 尾;与 client A/B/C/D grammar **逐项差分**(相同/不同/未知),每差异附首行反例。
3. 全表列画像:i8/i16/i32 有符号与 sentinel -1/0 区别,bool 掩码,date packed day/year,cash,ordinal 引用候选(走目标表实际 ordinal 集,不妄断)。
4. 闭合尝试:header+Σrow+footer==payload_len(变长则逐行求 row_len);若 server grammar 与 client 同构则验证,若不同则诚实记差异+候选 grammar(L1/L2),**不写 L3 结论**(reader 静态绑定 sol 另案)。
5. 消费 t25 client rows 作对照(不重 dump client);server rows 落 .rows.jsonl + profile.json(同 t29/t33 格式)。

## 边界
- 只 nation table_10 server 画像;不碰已闭 client/club 子表;不晋级 L3(reader 绑定 sol-tier);L4=0。
- 候选不写结论;negative/held 反例保留;不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。
- 只写 scratch/t46/ 与 scripts/t46_*.py;server grammar 若预算内无法确定则诚实 partial+已绑定子集+首反例。

## 交付 scratch/t46/out/
- profiles/table_server_10.profile.json + .rows.jsonl、grammar_diff_client_server.json、REPORT.md、verify.py(独立)、DONE.md
- scripts/t46_nation_server10.py(--help/--selftest)

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + t01_anchors.py(7/7)。