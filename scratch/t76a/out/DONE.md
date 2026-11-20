DONE type=t76a status=complete

## 交付清单

| 文件 | 内容 |
|---|---|
| `scripts/t76a_stadium_slots.py` | builder(892 行):行框引用 + 逐列 profiling + 字段对齐,`--all/--archive/--json/--check/--selftest` |
| `scratch/t76a/out/slots_client_21.json` | client 38B 槽表:12 槽,38/38 字节有槽,L2/L3 73.7% |
| `scratch/t76a/out/slots_server_21.json` | server 181B 槽表:47 槽,181/181 字节有槽;含 `server_only_segment`(143B)+ `shared_tail`(38B) |
| `scratch/t76a/out/verify.py` | 独立 verifier:numpy 直接重抽,不 import builder;`--selftest/--json` |
| `scratch/t76a/out/verify.json` | 49/49 检查机读结果 |
| `scratch/t76a/out/REPORT.md` | 结论报告 |
| `scratch/t76a/out/DONE.md` | 本文件 |

## 核心结论

- **行框**:client `14+48,413×38+8=1,839,716` / server `14+48,413×181+8=8,762,775`,双档闭合;
  identity `48,413/48,413`。行框取自 `scratch/t74/out/frames.json`,**未重闭**。
- **143B 差额**:`server[143:181] == client[0:38]` 在 48,413/48,413 行逐字节相同
  → 143B 是 server 独有前缀段,已单列 `server_only_segment`,`shared_tail` 单列。
- **锚点 5/5(client)+ 4/4(server)** 全过。
- **锚点冲突回查**:冻结 `rdui@25` 实测**等于行下标**(48,413/48,413),是**行序数**不是 Random ID;
  偏移正确、标签错位,已按数据记为 `row_ordinal@25` / `rdui_raw@33`,原锚点原文保留。
- **数据侧新发现**:四个容量槽满足 `Scas@12 <= Sscy@4 <= Scpy@0 <= Secy@8`,
  在 5,065 行上成立 **98.70%**;新增 `L2_structural` 档承载(66 行反例原样保留,不升 L2)。

## 分档统计

| 档 | client | server |
|---|---:|---:|
| L2 | 5 | 5 |
| L2_structural | — | 4 |
| L3(冻结锚点) | 2 | 2 |
| candidate | 2 | 31 |
| unassigned | 3 | 5 |
| 合计槽 | 12 | 47 |

## 验证

- builder `--selftest`:21/21
- builder `--all --check`:双档 `status=closed`
- `verify.py`:49/49 PASS(含 5 个锚点重抽 + 逐槽对拍 + JSON 产物一致性)
- `scripts/t01_anchors.py`:7/7 PASS(未回归)
- **L4 = 0**:未启动游戏/编辑器,未读 `Z:`,未联网

## 边界

- team(24)/extra_24 未触及(归 t79)。
- 字符串/列表/子表/非 wire 字段进 `held`,不猜。
- 静态 L3 归 t79,本任务只**引用**并标 `t79 cited`,不重导、不改动其产物;
  凡"只有静态能定"的项一律降为 candidate,故 server 侧只有 11 L2/L2_structural + 2 L3,
  而非照抄 t79 的 41 L3。
- Sowi@16 因 club UID 集不可取(t3 frame 未解析),wrong-UID 控制**缺失**,降 candidate。
