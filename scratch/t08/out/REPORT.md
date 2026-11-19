# t08 分发链分组报告

## 结论

- 状态：`complete_direct_target_reviewed`。
- 命名从 t07 的 **45/240** 增至 **138/240**（新增 93 槽）；达到验收下限 62，但未达到任务标题的 150+ 目标。
- type22 独立链内复现 **14/19**，达到验收线；对照 t05 的 17 个名字，复现 14 个、不同名 0 个、未复现 3 个。t05 仅用于本段事后交叉校验，没有作为生成输入。
- t07 的 45 个命名槽原名全部保留；injury 13/13、city 6/6 校准通过；所有 archive 的 `sum(width)==business_width`。
- 产物仅写入 `scratch/t08/out/`；输入的 t05/t07 文件和脚本未修改。

## 逐实体前后对比

| type_id | entity | t07 | t08 | 新增 |
|---:|---|---:|---:|---:|
| 2 | city | 12 | 16 | 4 |
| 6 | inju | 18 | 18 | 0 |
| 19 | regi | 0 | 12 | 12 |
| 21 | stad | 14 | 17 | 3 |
| 22 | ? | 0 | 14 | 14 |
| 23 | stgn | 0 | 0 | 0 |
| 30 | ? | 0 | 5 | 5 |
| 31 | ? | 0 | 0 | 0 |
| 34 | ? | 0 | 4 | 4 |
| 35 | ? | 0 | 0 | 0 |
| 37 | ? | 0 | 11 | 11 |
| 42 | ? | 0 | 0 | 0 |
| 43 | ? | 0 | 3 | 3 |
| 46 | ? | 0 | 0 | 0 |
| 47 | lcrg | 1 | 8 | 7 |
| 49 | ? | 0 | 6 | 6 |
| 50 | ? | 0 | 0 | 0 |
| 51 | ? | 0 | 0 | 0 |
| 58 | ? | 0 | 5 | 5 |
| 60 | ? | 0 | 0 | 0 |
| 61 | ? | 0 | 0 | 0 |
| 62 | ? | 0 | 7 | 7 |
| 63 | ? | 0 | 0 | 0 |
| 64 | ? | 0 | 0 | 0 |
| 66 | ? | 0 | 3 | 3 |
| 70 | ? | 0 | 9 | 9 |
| **合计** | **26** | **45** | **138** | **93** |

最终 confidence：`chain_unique=81`、`chain_ambiguous=12`、原 `readpair=37`、原 `ref_only=8`、`unresolved=102`。歧义槽保留所有码，没有强行择一。

## 分发链与配对矩阵

- 起点是 t07 的 2,103 条候选记录；读取 1,979 个不同 cmp 文件偏移，按相邻间距 ≤512 字节形成 587 个临时簇。只在这些簇的有限文件范围内局部解码，没有重新扫描全库。
- 保留 **226 条** `n_codes>=5` 的链；361 个不足 5 码的簇记入 `chains.json.discarded_clusters`，未纳入配对。保留链的直接分支目标均落在同一 PE section、目标 VA 范围受限，连通性检查 226/226 通过；共用的默认分支目标也保留在 `targets[]` 中。链内访问同时收窄读和写，以匹配任务要求的指令形态证据。
- 矩阵覆盖 26 个 reader。**15/26** reader 得到主链，均满足 exact `(object_off,width)` score≥3；矩阵中共有 115 个 reader-chain 关系达到该分数。每个 reader 仅裁决一条主链；按 score、宽度一致率排序，落选链保留在 `top3`/`candidates` 中。单条链可配多个 reader（例如 city/inju/lcrg 的共同链）。
- type22 主链为 `chain_0148`，score **14**，width 一致率 1.0；次选 `chain_0147` score 8、`chain_0160` score 7。链内直接窄访问独立得到 `Scap, Styp, Scpm, Sscp, Snxa, Snmn, Snmx, Stks, Slhm, Scam, Scns, ScTL, ScYL, Sceb`。`ScYK` 是前一条 `jle` 边界比较，不把其误关联到后续 `ScYL` 的窄读；这是对 t07 相邻比较分支串码问题的修正。
- type22 的 t05 事后对照：17 个字段中精确复现 14 个；未复现 `Sold/Snew/Salt`，没有链内输出与参照名冲突。未复现原因和 Snew 的错实例修正见下节及 `MISSING_CODES.md`。

## 仍为零命名的实体及原因

| type_id | entity | 最高 exact score | 原因分类 | 证据摘要 |
|---:|---|---:|---|---|
| 23 | stgn | 1 | 配对分数不足 | 有低分链候选，未达 3 命中门槛 |
| 31 | ? | 2 | 配对分数不足 | 最佳链仅 2 个 exact 命中 |
| 35 | ? | 2 | 配对分数不足 | 最佳链仅 2 个 exact 命中 |
| 42 | ? | 2 | 配对分数不足 | 最佳链仅 2 个 exact 命中 |
| 46 | ? | 2 | 码表缺失/宽度不符 | 偏移有重叠，但最多 3 个 offset-only 命中中有宽度不一致，exact score 仍只有 2 |
| 50 | ? | 2 | 配对分数不足 | 最佳链仅 2 个 exact 命中 |
| 51 | ? | 1 | 配对分数不足 | 最高仅 1 个 exact 命中 |
| 60 | ? | 1 | 配对分数不足 | 最高仅 1 个 exact 命中 |
| 61 | ? | 0 | 当前码表无可配对 4CC 链 | 所有保留链均无 reader object_off 命中 |
| 63 | ? | 0 | 当前码表无可配对 4CC 链 | 所有保留链均无 reader object_off 命中 |
| 64 | ? | 2 | 配对分数不足 | 最佳链仅 2 个 exact 命中 |

零命名实体没有可证实的“链太短”归因：361 个被丢弃短簇对这些 reader 的最高 exact overlap 均小于 3。这里的“无可配对链”只表示本候选表/本轮保留链没有偏移交集，不声称实体绝不存在别的 dispatch 机制。

## 回归与复跑

```powershell
py -V:3.12 -I scratch/t08/out/build.py --help
py -V:3.12 -I scratch/t08/out/build.py --selftest
py -V:3.12 -I scratch/t08/out/build.py
py -V:3.12 -I scratch/t08/out/verify.py --help
py -V:3.12 -I scratch/t08/out/verify.py --selftest
py -V:3.12 -I scratch/t08/out/verify.py
```

`verify.py` 强制检查 t07 45 名回归、injury/city 校准、行偏移/宽度与业务宽度闭合、type22/总命名数门槛、26 reader 配对覆盖，以及每个 `chain_unique` 槽的链内 `(off,width)` 唯一性。
