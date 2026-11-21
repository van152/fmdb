# t85 — NATION+0x108 与 COMP 集合对象的数据侧画像(deepseek)

你是受指挥官委派的子代理。t75(E114)把 nation 10 段文法闭合、99 槽裁决,但一批 held 字段的状态是 **getter_proven_but_no_main_row_sink**:它们的 getter 读的是 `[NATION+0x108]` 集合对象(t75 实例:nhrl 的 gate 17048862 "compares bounds at [this+0x108]+0x4a0/0x4a8; not a scalar bit load"),值在 wire 上的家还没找到。本任务数据侧画像这些集合对象,找出它们的 wire 对应物。

## 已冻结地基(直接用,不重做)

- `scratch/t75/out/xref_reverse.json`:顶层 `nation_escalations`(10 段文法)、`slots`(99 槽裁决,注意所有 `getter_proven_but_no_main_row_sink` 条目的 first_counterexample.gate/source)、`negative_evidence`(不翻案)
- `scratch/t72/out/`(E112):三主表未命名槽位清单+值指纹——集合字段很可能落在这里的未命名槽
- `scratch/t78/out/buckets.json`:nation 318 条 no_wire_evidence、comp 38 条 unresolved 的分母明细
- 行框:`scripts/fm24_dump.py` FIELDS(nation client t10 251 行等)+ `scratch/t74/out/frames.json`(9 变长表);E80 成员寻址口径(member start = data_base(34)+entry.offset)
- 静态引用(只读 editor.exe,SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`):可对 [NATION+0x108] 的 vtable/gate 地址(如 17048862=0x1044B1E 一带的 helper)再抽样取证,但**以数据侧为主**,反汇编不是本任务重心

## 任务

1. **集合字段清单**:从 t75 slots 里程序化捞出全部 `getter_proven_but_no_main_row_sink` + source 含 `[this+0x108]` 或同类集合模式的字段( nation 侧;comp 侧从 t78 的 comp unresolved 明细同理捞),产出 `scratch/t85/out/collection_fields.json`
2. **wire 对应物搜索**:在 460 单帧成员 + 编号子表 + extra_* 里找"每 nation 一组"或"251 元素集合"的候选结构:行数/元素数/步长指纹对齐(t72 指纹口径);comp 同法(7,047 行)。wrong-UID 控制同报
3. **画像**:对命中候选给结构 profile(头/计数/步长/子段),并把第 1 步字段逐个对到候选内偏移;命中→L2/candidate,不命中→held 原样+首反例
4. **escalate 纪律**:复杂变长循环、跨对象指针、跳表分发两轮定不出→标 `escalate_to_sol`(即后续 neon 车道),不硬猜
5. `verify.py`(独立重抽)+ `--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7

## 避坑纪律

1. 只写 `scratch/t85/` 和 `scripts/t85_*.py`;不碰 reports/、LEDGER、t75/t72 文件
2. 单次文件写 ≤120 行,先骨架后追加;`0xffffffff` 与合法 0 分列;负结果原样保留
3. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t85/out/

`collection_fields.json`、`wire_candidates.json`(候选成员指纹对齐)、`profile_{nation,comp}.json`、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t85 status=complete`)。
