# t88-fix1 — table_45 扫表续作(全新会话;前作静态台账已在盘,本会话只做行框+join+装配)

你是受指挥官委派的子代理,**全新会话**。t88 前作三连墙零 outbox,但 `scratch/t88/*.json` 已有 **20 个静态资产**(全部直接引用,不得重做):

- `TC_GET2_4cc.json` / `TC_SET2_4cc.json`:记录族 4CC 双链分发台账
- `record_get_handlers.json` / `record_get_tagmap.json` / `record_set_blocks.json`:RECORD_GET/SET handler 与 tag 映射
- `f4_dispatch.json` / `f4_to_rectype.json`:rec_type 分发
- `club.json` / `colstat.json` / `disp4c_sites.json` 等

## 任务(顺序,每步落盘;全部新文件写 `scratch/t88/out2/`)

1. **10 分钟内先落** `scratch/t88/out2/row_frame.json` 骨架:server `table_45.dat`(7,608,748B,84,477 条)行结构判定——先试定长步长(总长/行数整除检验),不行再 t74 三模型;identity 13B 自证(t74 判据 A/B)。client 档有无 table_45 条目一并记录
2. **rec 结构**:行内 `[rec+0x4c]`(应=CLUB+0xc 即 club UID)与 `[rec+0x5e]`(rec_type)的 wire 位点验证;84,477 条 vs 84,259 club 的对应关系(每 club 平均 1.0026 条——多出的 218 条是什么?rec_type 分布?)
3. **117 字段 join**:用前作 `record_get_tagmap.json`/`TC_GET2_4cc.json` 的静态映射,把 master.json club.xml[211..327] 字段对到行内偏移;数据侧= L2/candidate;wrong-UID 控制同报;`0xffffffff` 与合法 0 分列
4. `verify.py`(独立重抽)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t88 status=complete`)
5. 跑 `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t88/out2/` 和 `scripts/t88_*.py`(新文件);**不修改** scratch/t88/ 既有文件;不碰 reports/、LEDGER、t82/t74
2. `>20KB` 文件不进会话;程序化处理,print ≤30 行/次;单次文件写 ≤120 行
3. 负结果原样保留;候选不写成结论;两轮定不出→escalate
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t88/out2/

`row_frame.json`、`rec_structure.json`、`slots.json`、`domain_stats.json`、`verify.py`、`REPORT.md`、`DONE.md`。
