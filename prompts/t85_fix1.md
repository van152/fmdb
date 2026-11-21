# t85-fix1 — 集合画像续作(全新会话;前作 work/ 普查已在盘,本会话只做装配+定向 join)

你是受指挥官委派的子代理,**全新会话**。t85 前作三连墙零 outbox,但 `scratch/t85/work/` 已有 **128 个工作文件**,其中关键资产:

- `ident_census.json`:全部成员双档 (payload, ident_rows) 身份普查——**注意 `client|table_9.dat` ident=251(与 nation 同行数,per-nation 集合候选!)**、`table_10` 251、`table_22` 449、`table_23` 278
- `scan251.json`:同普查紧凑版
- `census.py`/`common.py`:普查代码(可复用逻辑,不得修改 t85 已有文件)

本会话**不做新的全景扫描**,只做装配与定向验证,从第一步就往 outbox 写文件。

## 任务(顺序,每步落盘;全部新文件写 `scratch/t85/out2/`)

1. **10 分钟内先落** `scratch/t85/out2/collection_fields.json` 骨架:程序化读 `scratch/t75/out/xref_reverse.json` 的 slots,捞出全部 `getter_proven_but_no_main_row_sink` + source 含 `[this+0x108]` 或集合模式的字段(nation 侧);t78 `buckets.json` 的 comp unresolved 同理。骨架含 meta+计数,后逐步充实
2. **wire 候选定向验证**(不做全景!):对 census 里 ident=251 的成员(client table_9/table_10/server 同名)逐一抽身份三元组+与 nation 主行的 UID/ordinal 对齐测试;ident=251 之外与 t75 集合字段数吻合的候选(如 comp 侧)同样处理。wrong-UID 控制同报
3. **profile**:命中的候选给结构 profile(头/计数/步长/与 [NATION+0x108] 的 getter 域对照);不命中→held 原样+首反例
4. `verify.py`(独立重抽 census 与 join)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t85 status=complete`)
5. 跑 `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t85/out2/` 和 `scripts/t85_*.py`(新文件);**不修改** scratch/t85/ 既有文件;不碰 reports/、LEDGER、t75/t72
2. `>20KB` 文件不进会话;程序化处理,print ≤30 行/次;单次文件写 ≤120 行
3. 复杂变长循环/跨对象指针/跳表分发两轮定不出→`escalate_to_sol`,不硬猜
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t85/out2/

`collection_fields.json`、`wire_candidates.json`、`profile_{nation,comp}.json`(若 comp 侧有命中)、`verify.py`、`REPORT.md`、`DONE.md`。
