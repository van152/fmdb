# t73 — 通用扫表工具 table_slot_mapper.py + city/continent/region/currency 四表闭环(deepseek)

你是受指挥官委派的子代理。t57(club)/t59(comp)已把"行框闭合 → identity 自证 → 逐槽值域 → 字段对齐"的方法在两张主表上跑通,但方法散在两个一次性脚本里。本任务把它抽成**通用工具**,并用 4 张最简单的表跑通闭环:`city(2)`、`continent(5)`、`region(19)`、`currency(41)`(双档)。第 2 波的 3 条 deepseek 会拿这个工具批量扫 9 张表。

## 必读

- AGENTS.md;`scratch/t57/out/REPORT.md` 行框方法节(四对齐 identity triple DP、footer 敏感性、12B identity 结论的来路)、`scratch/t59/out/REPORT.md` 同节
- `evidence/fm24/reports/editor_schema/master.json`:`entities['city.xml'/'continent.xml'/'region.xml'/'currency.xml']` 字段清单(field/name/type/dependencies)+ `enums`(scoped enum 域)+ `field_codes`
- `evidence/fm24/reports/dbdat_decode/db_tables_small.json` / `db_tables_big.json`(上游行框先验,**只当先验不当地面真值**):city 43B×56,293(header14/footer8)、cont 34B×7(client)/server 不同(payload client 260B/server 358B)、regi 45B×28(client)/server payload 1,310B、curr 173 行变长"four-string + rate/history + 13-byte trailer walk"(payload 双档同 74,352B)
- `scripts/fm24_dump.py` 的 FIELDS 既有锚点(城市 `Clat@1/Clon@5/Cnti@10/rdui@30/duni@34`;cont/curr 的 rdui/duni 尾锚)——你的结论**不得与这些锚冲突**,冲突=你的文法错了,回查
- `scripts/t01_anchors.py`(回归 7/7)

## 任务

1. **通用工具** `scripts/t73_table_slot_mapper.py`:输入表号+档,自动完成:
   - 载荷解码(`fm24_dump.load_payload` 模式,runpy 复用,不得修改它)
   - 行框闭合:identity triple(ordinal|UID|UID 形态,宽度按本表自证 11/12/13B 都试)四对齐 DP + footer 敏感性(7/8/9/10/12)→ 输出唯一铺法或 escalate
   - 逐槽 profiling:每偏移的宽度候选值域(u8..u32/i8..i32/f32)、cardinality、all-zero、全一占比
   - 字段候选对齐:master.json 字段类型宽度 × 值域形态 × 外键命中(t2/t3/t5/t10/t21/t23/t24/t25 live ordinal 集,wrong-UID 控制同报)——**不按 XML 顺序硬排、不用"值长得像"配槽**;结论分级:数据侧闭合=L2/candidate;能引用仓内已冻结静态锚(如 E22/t01c/property_map)的字段标 L3 并给快照证据指针
   - 锚点回归:既有 FIELDS 锚逐个复核
   - CLI:`--table N --archive client|server --json OUT`,支持 `--help`/`--selftest`,退出码 0/1/2
2. **四表闭环**(双档 8 个 (archive,table) 全做):
   - city:56,293 行定长 43B 先验要重新自证(13+43n+9 与 14+43n+8 同分区,报原生口径);双档 payload 逐字节相同,报 SHA 并利用
   - continent:client 7×34B vs server 7×更宽(server 358B=13+7×48+9?自己算),两档行宽不同是**发现**不是错误,解释差异来源(如 server 多字段)要证据,不许硬套同一 stride
   - region:client 28 行 vs server payload 1,310(28×46+? 自证);currency:173 行变长 trailer walk,行宽规则要精确到字节
   - 每表交付 `slots_{archive}_{table}.json`(槽位→字段候选+等级+证据)
3. **独立 verify.py**:不 import 你的 builder;重抽 ≥2 表重算行框与 ≥5 个槽位值域对拍。
4. 四表若有 schema 字段对不上任何槽,列 `unmapped` 清单,不硬凑;跨对象指针/复杂循环 → `"escalate_to_sol"`。

## 避坑纪律(必须遵守)

1. **防冲突**:只写 `scratch/t73/` 和 `scripts/t73_*.py`;**不碰** `reports/`、`scratch/t01/LEDGER.json`、其他任务目录。
2. **上交纪律**:行框闭合失败、变长规则两轮内定不出、需要读 exe 才能定分发的——标 `escalate_to_sol` 跳过,不硬猜。
3. 负结果原文保留;候选不写成结论;`0xffffffff` 与合法 0 分列。

## 交付 scratch/t73/out/

- `frames.json`(4 表 × 双档行框+敏感性)、`slots_client_{2,5,19,41}.json`、`slots_server_{2,5,19,41}.json`、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t73 status=complete`);builder `scripts/t73_table_slot_mapper.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;完成跑 `scripts/t01_anchors.py`(7/7)。
