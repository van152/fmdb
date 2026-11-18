# t15 任务书:数据侧 FK 交叉 —— 给 RTTI 锚配 C 类佐证 + 658k/792k 悬案

先读 [AGENTS.md](../AGENTS.md)。你是旁路数据组,主线是 luna 的 t14;**你的输出与 t14 独立评分,互相印证**。

## 环境变化(重要)

游戏数据库已本地化:`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`(环境变量已设好,`scripts/fm24_dump.py` 已支持)。**不许再读 Z: 盘。** dump 用法:

```
py -V:3.12 -I -B scripts/fm24_dump.py --archive server --table 26 --csv scratch/t15/out/t26.csv
```

## 一句话目标

对司令官 RTTI 初步命名的表做值域/FK/哨兵/fill 分析,给每张"C 类佐证"或"否证";并攻 658,011 vs 792,149 的 134,138 悬案。

## 背景:司令官 RTTI 中期图(与你的数据侧独立,不要求你采信)

| table | 行数 | RTTI 类名 |
|---|---|---|
| 26 | 90,128 | COMP_HISTORY_RECORD |
| 29 | 13,278 | (未定) |
| 30 | 72,473 | STARTING_INJURY |
| 32 | 315 | STARTING_FUTURE_TRANSFER |
| 36 | 6,535 | (未定) |
| 38 | 5,241 | STARTING_BAN |
| 39 | 117 | STARTING_AVERAGE_POINTS |
| 45 | 84,477 | STARTING_RECORD |
| 48 | 5,210 | STARTING_RECORD |
| 49 | 792,149 | STARTING_PERSON_HISTORY |

已验证实体基数(见 `scratch/t13e/out/baselines.json`,4 路独立计数一致):comp 7,047、club 84,259、city 56,293、nation 251、weather 334、language 126、injury 115、lcrg 2,488、stadium 48,413、person(basic_people_db)658,011、award 3,545、team 84,507。

## 任务

对每张上表 dump 出 CSV(输出到 `scratch/t15/out/`),前 20 列做:distinct / min-max / 0 与 0xFFFFFFFF 比例 / 候选 ID 列(monotonic 或值域密集)。然后:

1. **t26**:是否有列值域 ⊆ [0,7047)(comp ID)?可否解释 90,128 ≈ 7047 × ~12.8?
2. **t30**:是否有 person 引用列(值域接近 [0,658011) 或 [0,792149))?injury 类型码列 ⊆ [0,115)?
3. **t32**(315)/ **t38**(5,241):引用谁?STARTING_BAN 若引用 person,值域应落在 person ID 空间。
4. **t39**(117):117 个对象是什么?列值像联赛/分区引用吗?
5. **t45/t48**(STARTING_RECORD):84,477 vs 5,210,行数差 16 倍但同类名——值域画像能否区分两个行集?与 club 84,259 差 218 是巧合吗(列值比对)?
6. **t49 悬案**:distinct person 引用 ID 数 vs 658,011;多出的 134,138 是否对应 non-player(person 基数 658,011 只是 basic_people_db,`non_pl_hist_dt.dat` 27.6MB 未解析)?给出可检验的数字,不下结论。
7. **t29/t36**:值域画像 + 最接近的基数候选(candidate 级,标"仅 C 类")。

## 规则

- 量级/值域吻合只算 **C 类**;E42 教训(fill 越接近 1 越偏向小表、值域法单独不能定案)写进你的判断。
- 与 RTTI 类名一致时标 `corroborates`,矛盾时标 `contradicts` + 原文——矛盾照报,**不许隐掉**。
- 不许把 C 类写成实体确认。

## 纪律

- 只写 `scratch/t15/out/`;其他目录只读;不联网、不启动游戏/编辑器。
- py -V:3.12 -I;分析脚本放 `scratch/t15/out/`(须 --help/--selftest,退出码 0/1/2)。
- 每张表 dump 限时;卡住就跳过并记录。整体 25 分钟做不完就落盘标 `"status":"partial"`。

## 交付(scratch/t15/out/)

1. `fk.json` —— 逐表:列画像摘要 + FK 判断 + corroborates/contradicts + 顶层 status。
2. `fk.md` —— 人读版。
3. `people_diff.md` —— 134,138 悬案的数字与假设。
4. 各表 CSV 留在 out/ 里作证据。
