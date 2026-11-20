# t68 — Club 数据侧交叉验证(t50 范式迁移到 club table_3,sol;L2 目标)

你是受指挥官委派的子代理。本任务把 t50(E91)独立数据侧交叉验证范式迁到 **club table_3**(t57 已给 reader 侧行框:client 6,932,082 / server 16,595,312,84,259×2,identity **12B** ordinal|UID|UID,footer e3c03a77)。

## 必读
- AGENTS.md;scratch/t50/out/REPORT.md + profiles/**.jsonl(**范式与口径唯一来源**)
- scratch/t57/out/REPORT.md + field_slots.json(club 行框与敏感性表;**identity 12B 是 t57 的修正结论**,冲突先自查)
- scratch/t67 brief 若已交付可引用其 comp 侧结论(不依赖,可独立跑)

## 任务
1. **server 变长行平铺唯一性**:84,259 行、club server 行含变长区(t57:公共 70B 前 + 56B 尾;中间 server 扩展)——非重叠全铺 DP + 分 ordinal 层唯一性;与 t57 声明一致;敏感性对照(12B/13B/8B、UID 约束放宽)。
2. **selector 平铺**:双档 selector 直方图与序列;t57 的 34 位置执行顺序的数据侧一致性。
3. **identity 双档同值** + footer 逐字节 + t01 夹具(Liverpool/Bernabéu/成立年)复洽。
4. 84,259 行规模:全量 DP 允许分块/向量化,唯一性判定不得抽样。
5. 独立 verify.py + builder scripts/t68_club_data_crosswalk.py;--help/--selftest;退出码 0/1/2。交付 L2 交叉台账(不改 reports/)。

## 边界
- 只 club table_3;不得修改 scratch/t57;不碰 8 子表/CLUB_LINK;不启动游戏/编辑器/IDA,不联网,不读写 Z:。

## 交付 scratch/t68/out/
- crosswalk.json、sensitivity.json、verify.py、REPORT.md、DONE.md;scripts/t68_club_data_crosswalk.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
