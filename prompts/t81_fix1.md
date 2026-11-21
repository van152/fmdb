# t81-fix1 — 续作:三小表扫描 + 收尾(全新会话;前作 fk_index 已交付)

你是受指挥官委派的子代理,**全新会话**。t81 前作已交付 `scratch/t81/out/fk_index.json`(37 目标,变长表 client 闭合)、`rescan_fk_city.json`(Cnti mapped-ordinal:56,293/56,293 全在域,UID 控制被否)、`rescan_fk_t76.json`。 launcher 启发式提前判收,**本会话只补齐剩余交付**,做完即收:

## 剩余任务(按顺序,每步落盘)

1. **三小表双档扫表**( Injury(6)/stage_name(23)/description(35)):
   - 行框自证(t73 方法:identity 自证+alias group 结论适用:数据侧不能定 header 原点,报 footer flag 判据);t6 payload 仅 1,862B/115 行、t23 208 行 ordered-name、t35 13,372B/35 行——小表全量
   - 槽位 profiling + master 字段对齐(entities 键 `injury.xml`/`stage name.xml`/`description.xml`,field_codes+enums 程序化查)+ FK(t6 的 inju 与 t30 关系只引用 stage2 结论,不重裁)
   - 分级:数据侧=L2/candidate;冻结锚点支持的标 L3(t6 `rdui@3/duni@7`、t23 `rdui@1/duni@5`、t35 `rdui@2/duni@6`)
2. `scratch/t81/out2/slots_{client,server}_{6,23,35}.json`(骨架先行,逐个追加,单次写 ≤120 行)
3. `verify.py`(独立重抽 FK 索引与三表行框对拍)+ `REPORT.md` + `DONE.md`(首行 `DONE type=t81 status=complete`)

**输出目录:全部新文件写入 `scratch/t81/out2/`(注意:不是 out/;out/ 是前作 fk_index/rescan 的既有成果,只引用不改动)**
4. 跑 `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 `scratch/t81/` 和 `scripts/t81_*.py`;不碰 t73/t74 文件与 out、reports/、LEDGER;**不重做 fk_index/rescan**(前作成果直接引用)
2. `>20KB` 文件不进会话;程序化处理,print ≤30 行/次
3. 单次文件写 ≤120 行;`0xffffffff` 与合法 0 分列;负结果原样保留
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付(全部在 scratch/t81/out2/)

`slots_client_6.json`、`slots_server_6.json`、`slots_client_23.json`、`slots_server_23.json`、`slots_client_35.json`、`slots_server_35.json`、`verify.py`、`REPORT.md`、`DONE.md`。
