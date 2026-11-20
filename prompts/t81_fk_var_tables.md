# t81 — 变长表 FK 索引补全 + injury(6)/stage_name(23)/description(35) 扫表(deepseek)

你是受指挥官委派的子代理。t73 通用映射器的 FK 判据对变长目标表无能力(t73 REPORT §3.4 如实记账:Cnti/Clgi/Clri/Cwea 全部落 unmapped 是工具缺口,不是字段没有槽)。t74 已把变长表行框闭合并给出 ordinal/UID 位置。本任务:①把变长表身份索引接入(不改 t73 文件);②顺手扫掉阶段二剩余 3 张干净表。

## 必读

- AGENTS.md;`prompts/t73_slot_mapper.md`(方法口径)
- `scripts/t73_mapper_core.py`(**只读复用**,runpy 载函数;不得修改)
- `scratch/t74/out/frames.json`(t10/t8/t27/t47/t24 变长行框+identity 位点)+ `row_widths_*.csv`
- `scratch/t73/out/slots_client_2.json`(city 4 条 FK lane 的现状)
- `scratch/t76a/t76b/t76c/out/`(若已落盘:跨表 FK 复核清单)
- 既有锚点:`scripts/fm24_dump.py` FIELDS(client t6 `rdui@3/duni@7`、t23 `rdui@1/duni@5`、t35 `rdui@2/duni@6`);上游 census(t6 115 行变长 injury、t23 208 行 stgn ordered-name、t35 35 行?——payload client 13,372B,自证)
- `evidence/fm24/reports/editor_schema/master.json`:`entities['injury.xml'/'stage name.xml'/'description.xml']` + `field_codes` + `enums`

## 任务

1. **FK 索引模块** `scripts/t81_fk_index.py`:`build_fk_index()` 读 t74 frames.json + 载荷,产出 `{table_id: {ordinal_set, uid_set(可选), row_count}}`(变长表按 t74 identity 位点抽 ordinal/UID;修复 t10/t8/t27/t47/t24 四张变长目标的"不可判"状态);`--help`/`--selftest`,退出码 0/1/2。**不改 t73/t74 文件**。
2. **补全 t73 遗留 FK**:city 的 `Cnti/Clgi/Clri/Cwea` 四条用新索引重判(t10/t8/t27/t47 的 ordinal 域),给命中/错指/哨兵分列的裁决;升级建议只到 L2(数据侧),不与 t73 冻结锚点冲突。
3. **t76 跨表 FK 复核**:三车道 slots 里的 FK 未判/误判项(若已落盘)用索引重判一遍,输出增量清单。
4. **扫三张表**:injury(6)/stage_name(23)/description(35) 双档:
   - 行框自证(t73 方法:identity 自证+alias group 结论原样适用:数据侧不能定 header 原点,报 footer flag 判据)
   - 槽位 profiling + master 字段对齐 + FK(t6 的 inju 与 t30 伤病实例表的关系只引用 stage2 结论,不重裁)
   - 分级:数据侧=L2/candidate;冻结锚点支持的标 L3
5. **独立 verify.py**:重抽 FK 索引与三表行框对拍。
6. escalate 纪律:两轮内定不出立即 `escalate_to_sol`;负结果原样保留。

## 避坑纪律

1. 只写 `scratch/t81/` 和 `scripts/t81_*.py`;不碰 t73/t74 文件与 out、reports/、LEDGER。
2. t6 payload 只有 1,862B/115 行、t35 13,372B——小表全量;变长索引注意 t24 8.8MB 向量化。
3. 文件写单次 ≤120 行。

## 交付 scratch/t81/out/

`fk_index.json`、`rescan_fk_city.json`、`rescan_fk_t76.json`、`slots_{client,server}_{6,23,35}.json`、`REPORT.md`、`DONE.md`(首行 `DONE type=t81 status=complete`)、`verify.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;完成跑 `scripts/t01_anchors.py`(7/7)。
