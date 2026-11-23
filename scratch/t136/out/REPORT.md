# t136 — Big-3 持久化字段复核

| 阶段 | 毛覆盖 | 净覆盖 | 未闭合 |
|---|---:|---:|---:|
| Baseline | 110/1,034 (10.6%) | — | — |
| t109 | 379/1,034 (36.7%) | 379/673 (56.3%) | 294 |
| t125 | 512/1,034 (49.5%) | 512/672 (76.2%) | 160 |
| t136 | 568/1,034 (54.9%) | 568/663 (85.7%) | 95 |

守恒：**1,034 = 568 L3 + 371 排除 + 95 缺口**。达到 85% 净覆盖目标。

| 实体 | L3 | 排除 | 缺口 | 净覆盖 |
|---|---:|---:|---:|---:|
| club | 222 | 162 | 49 | 81.9% |
| nation | 186 | 134 | 26 | 87.7% |
| comp | 160 | 75 | 20 | 88.9% |

## 证据与口径

- `hop_audit_v4.json` 核对 11/11 个 t132 函数及 38/38 个装箱点的上游切片。装箱、析构、分配及修改回调不能单独证明持久化。
- `archive_audit_v4.json` 复跑 19 个 numeric 成员；`table_extra_3` 双档各 84,259 行，`table_extra_24` 84,507×82 B，`club_links` server 9,261×47 B。未将特殊成员的同类数据当成字段绑定。
- `table_extra_9` 双档各 251 行，从 12 B 头连续解到 EOF；client 83,927 B，server 105,228 B，无 footer。共同段为 ordinal、UTF-8 名、u16、UTF-8 hashtag、定长 kit 列表、两组 RGBA；server 再读两向量、4 阵型字节、3 个 attendance、tag-9 记录及独立 TCrs。保留每行跨度和 SHA-256；未套用 table_9 的数值成员 slot19。
- 修正的 v3 排除均逐项列在 coverage JSON。父集合封闭不让其子项自动升格；重复 4CC 仍以 occurrence ID 计，不以代码名字串合并。

## 新裁决

- `10`：2 项。
- `24`：4 项。
- `25`：9 项。
- `3`：7 项。
- `45`：12 项。
- `9`：3 项。
- `club_links`：2 项。
- `table_extra_3`：5 项。
- `table_extra_9`：12 项。

## 剩余缺口

逐 occurrence 阻断点见 `remaining_gaps_v4.json`（club 49、nation 26、comp 20）。未证明的 getter/reader 同对象链、读到默认值的门控、未命中型别和域冲突均不视为排除。
- 特别保留：Nation `TCht` 为全空串；阵型值未通过作用域枚举验证；`NCro` 无实档 item。CLUB 重复 `ttcl`/`tbcl` 不强配；COMP `sySx` 无对应档内子型，`HCA*`/`LCA*` 无匹配的 table_48 记录型。

运行：`py -V:3.12 -B scripts/t136_big3_final_closure.py`，再加 `--selftest`。不启动游戏、Editor 或 IDA。
