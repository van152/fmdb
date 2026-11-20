# t74 — 九张表数据侧双档行框闭合 + identity 宽度自证(deepseek)

你是受指挥官委派的子代理。第 2 波三条 deepseek(t76a/b/c)要批量扫 9 张表,需要你先把这 9 张表的**行框**钉死:双档 closure、每行 identity 宽度自证、变长文法精确到字节。纯数据侧任务,不做 exe 静态断言。

## 核心纪律:identity 宽度必须按表自证,不得照抄

club/comp 用 12B、nation 用 13B、client extra_3 是另一套——每张表都要走 t57 式敏感性(四对齐 identity triple DP、ordinal 分层非重叠铺法计数、footer 7/8/9/10/12 敏感性)自证;上游普查(header 14/footer 8)只是先验,不是地面真值。

## 九张表与已知先验(到 2026-11-21 为止)

| 表号 | 实体 | 先验(需自证) | 已有锚点(结论不得冲突) |
|---|---|---|---|
| 21 | stadium(stad) | client 38B×48,413 / server 181B×48,413,header14/footer8 | client `Scti@3/Slat@17/Slon@21/rdui@25/duni@29`(fm24_dump FIELDS) |
| 24 | team(team) | **server-only**(client 无 entry,t66 已证);84,507 行;82B 定长已被 E37 否证,均值 104.36B,变长 | t66 用过 t24 ordinal→UID(84,507);`table_extra_24.dat` 只取 ordinal,不在本任务范围 |
| 0 | award(awar) | fixed 77B×3,545(header14);payload 双档同 272,987B | client `rdui@64/duni@68` |
| 8 | language(lang) | "ordered name + 30-byte suffix" ×126;payload 双档同 5,248B | client `rdui_suffix@17` |
| 7 | media(mdso) | "ordered-name + repeated-u32 identity trailer" ×208;client 36,824 / server 38,280(不同!) | client `rdui@3/duni@7` |
| 18 | derby(drbr) | 同上 trailer 文法 ×1,567;client 139,891 / server 149,293 | RTTI `db::DERBY`(t13 的 'city secondary-name' 命名冲突勿混) |
| 27 | weather(weat) | 同上 ×334;payload 双档同 43,345B | 实体基数 334(high) |
| 47 | local_region(lcrg) | **本仓已否证上游 44B 定长**:`lcrg_tail` 变长 41+5k B×2,488(payload 109,505B 双档同;见 fm24_dump OVERRIDE);server 行框同样要钉 | client `rdui@-13/duni@-9` |
| 56 | agreement(agrm) | fixed 13B×6(header14);payload 双档同 100B | client `rdui@0/duni@4`;最小的表,先拿它跑通 |

## 必读

- AGENTS.md;`scratch/t57/out/REPORT.md` 行框方法节与敏感性表(范本);`scratch/t59/out/REPORT.md` 同节
- `evidence/fm24/reports/dbdat_decode/db_tables_small.json` / `db_tables_big.json` / `EXTRA_TABLES.json` / `VARLEN_ROWS.md`(先验与上游口径)
- `scripts/fm24_dump.py`(load_payload 复用模式 + OVERRIDE 里 lcrg_tail 的既有结论,可 runpy 不得修改)
- `evidence/fm24/reports/editor_schema/master.json` 对应 entity(只需 field 类型清单,帮助判断行内是否含字符串)

## 任务

1. **逐表逐档闭合**:每 (archive,table) 输出 `{header, footer, count, model: fixed|variable, 行长规则, identity: {width, 结构(ordinal|UID|UID 还是别的), 在行内位置}, payload_sha256, 敏感性摘要}`;closure `header + Σrow + footer == payload_len` 必须逐字节成立,走不齐就 escalate,不许静默截断。
2. **字符串行文法**:language/media/derby/weather 是"ordered name + trailer"类——长度前缀规则、trailer 的 u32 序列结构要精确到字节(每行行长可复算);server/client 行宽不同的表(media/derby)给出差异来源的**数据侧证据**(如 server 行多一段),不猜语义。
3. **team(24) 变长攻坚**:84,507 行、变长、server-only。方法建议:identity triple 四对齐 DP(t57 式)先试;若行文法复杂(多 count 循环)两轮内定不出 → 该表标 `escalate_to_sol`,但其余 8 表照常交付。
4. **自证基线回归**:fm24_dump FIELDS 锚点(stadium/award/language/media/lcrg/agreement 上面列的)在你的行框下必须逐个复核成立;冲突=文法错,回查。
5. **独立 verify.py**:不 import builder;重抽 ≥3 表重算 closure + identity + 锚点对拍。

## 避坑纪律(必须遵守)

1. **防冲突**:只写 `scratch/t74/` 和 `scripts/t74_*.py`;**不碰** `reports/`、`scratch/t01/LEDGER.json`、其他任务目录。
2. **上交纪律**:同一张表行文法两轮内定不出、或发现需要跨对象/读 exe 才能定——立即 `"escalate_to_sol": {"table": ..., "what_tried": ..., "blocker": ...}`,把算力让给能闭合的表。
3. 负结果原文保留;候选不写成结论;`0xffffffff` 与合法 0 分列;不用值域相似倒推行边界。

## 交付 scratch/t74/out/

- `frames.json`(9 表 × 双档全量行框,含 escalate 项)、`row_widths_{table}.csv`(逐行行长分布,大表可采样摘要+全量直方图)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t74 status=complete`);builder `scripts/t74_row_frames9.py`(`--help`/`--selftest`,退出码 0/1/2)。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。team(24) payload 8.8MB×84k 行,DP 要向量化。
