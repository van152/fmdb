# t67 — Comp 数据侧交叉验证(t50 范式迁移到 comp table_25,sol;L2 目标)

你是受指挥官委派的子代理。t50(E91)对 nation t9/t10 做了**独立数据侧交叉验证**(reader 之外的纯数据法),确立"identity-tail 平铺唯一性"与 extra_9 形态。本任务把同一范式迁到 **comp table_25**(t59 已给 reader 侧行框:client 13+7047×127+9 / server 13+1,533,950+9;identity 12B+footer 9B)。

## 必读
- AGENTS.md;scratch/t50/out/REPORT.md + profiles/**.jsonl(**范式与口径唯一来源**:敏感性检验、平铺唯一、selector 逐行)
- scratch/t59/out/REPORT.md + field_slots.json(comp 行框与敏感性表;不得与之矛盾,冲突先自查)
- scratch/t59/out/verify.py 的**独立重放思路可参考但不 import**

## 任务
1. **平铺唯一性**:server 变长行的四种字节对齐 triple 扫描 + 分 ordinal 层非重叠全铺 DP——在标准约束(ordinal 0..7046、UID 非零递增唯一)下验证**仅一路**,与 t59 声明一致;放宽单项的对照集(照 t59 敏感性表口径)复算并扩展 client 侧(127B 定宽下的 12B/13B/8B 假设)。
2. **selector 平铺**:client 7047 个 selector 字节直方图;server selector 序列与模板执行顺序(t59 的 25 模板)的数据侧一致口径(不重做 CFG,只做字节层验证)。
3. **identity 双档同值**:client UID 集与 server UID 集逐一对齐(数据侧,独立于 reader 游标);footer 双档逐字节。
4. **t01f 夹具**:六洲/parent 352/England/China 锚复洽。
5. 独立 verify.py + builder scripts/t67_comp_data_crosswalk.py;--help/--selftest;退出码 0/1/2。交付为 L2 交叉台账(不改 reports/)。

## 边界
- 只 comp table_25;不得修改 scratch/t59;negative/反例如实;不启动游戏/编辑器/IDA,不联网,不读写 Z:。

## 交付 scratch/t67/out/
- crosswalk.json(逐断言:claim/method/evidence/grade)、sensitivity.json、verify.py、REPORT.md、DONE.md;scripts/t67_comp_data_crosswalk.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
