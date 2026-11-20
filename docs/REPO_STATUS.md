# 仓库现状速览(2026-11-20)

本文件是一次只读梳理的快照,面向新接手者/新 session 快速定位。**结论性证据仍以 `BASELINE.md`、`reports/`、`scratch/t01/LEDGER.json` 为准**;本速览不改动任何验收口径。

## 一、身份与拓扑

| 项 | 值 |
|---|---|
| 使命 | FM24 `.dat` 数据库字段 → 行内偏移语义映射(详见 `AGENTS.md`) |
| 当前分支 | `t70-schemav10` |
| 提交数 | 216 |
| 本地分支 | 34(任务分支 `tNN-短名` 线性链,见下) |
| 验收台账 | `scratch/t01/LEDGER.json`,**110 条**,末条 E110 |
| 远端 | `origin` = `<REMOTE>` |
| 体积 | 2.0 GB(`.git` 190 MB、`scratch` 1.7 GB、`reports` 29 MB、`evidence` 15 MB) |

**分支拓扑**:主体是一条任务分支线性链 `t41-csme-cursor → … → t70-schemav10`,每次 pi dispatch 建新分支、指挥官在分支上提交,工作全部保留、尚未 merge-to-main。`main` 停在 `7a8a0bf`(初始化骨架),`github-snapshot` 停在 `c9e7dab`(脱敏快照,也是 `origin/main`)。远端自快照后无更新。

## 二、方法与硬约束(摘自 AGENTS.md)

- **证据分级**:L1 自检 / L2 独立事实对照 / L3 exe 静态证据(注明二进制、VA、来源)/ L4 真机加载(=0)。候选不写成结论,负结果原文保留不删改。
- **只读外部数据**:游戏库 `Z:`、旧证据库 `<OLD_REPO>` 一律只读;不启动游戏/编辑器/IDA,除非显式授权。引用旧证据须经 `evidence/fm24/` 快照 + MANIFEST SHA-256。
- **Python 3.12**:`py -V:3.12 -I`;新脚本须有 `--help` 与 `--selftest`;退出码 0/1/2。
- **Git**:任务分支 `tNN-短名`;提交信息 `feat/fix/docs/chore(tNN): 摘要`;大数据/二进制不入库。
- **落地位置**:临时实验进 `scratch/<任务>/`,结论进 `reports/`,机读结果与报告同名成对。

## 三、进度脉络

### schema 版本演进(v3 → v10)

| 版本 | 任务/E | 并入内容 |
|---|---|---|
| v3 | t45 | 8 numbered 表基线 |
| v4 | t48/E88 | Cafl/Cvfl 并入 CLUB_LINK |
| v5 | t52/E92 | nation 侧(t47 Ntxr + t49 t9 wire),30 L3 |
| v6 | t54/E95 | TCrs 双闭裁决 |
| v7 | t56/E96 | t55 nation 主行 5 L3 |
| v8 | t58/E98 | t57 club 主行 13 L3 |
| v9 | t60/E100 | t59 comp 主行 49 L3 |
| **v10** | **t70(本轮,待提交)** | E104–E109 r2 证据:club +8 L3(累计 21)、comp/nation 0 新 L3、7 文法 + 4 lane、EDsc 闭合、尾账 18 项 |

公共 schema 文件 `reports/club_nation_subtable_schema.json` 约 6.4 MB(v8 起),`.md` 约 77 KB。v10 的 JSON/Markdown SHA-256 记于 `scratch/t70/out/REPORT.md`。

### 三张主表行框(per-table identity 宽度必须按表自证,不得照抄)

| 表 | 实体 | 行框 | identity | 主行 L3 |
|---|---|---|---|---|
| table_9 / extra_9 / table_10 | nation | client 13+24,710+9=24,732;server 13+422,323+9=422,345,各 251 行 | 13B(旧 13B 假设经敏感性反例修正) | 5 / 346 |
| table_3 | club | client 6,932,082 / server 16,595,312 B,84,259×2 行 | 12B(修正旧 13B) | 21 / 433 |
| table_25 | comp | client 13+894,969+9 / server 13+1,533,950+9,7,047×2 行 | 12B + 9B footer | 49 / 255 |

### 可复用方法资产

- **三重闸门**:frozen 唯一 occurrence → getter 4CC 精确分发 → 同位移 sink;配套目标实表 ordinal join + 条目级 ledger 守卫。已跨 t47/t49/t51/t53/t55/t57/t59 五次复用。
- **E80 修复**:成员绝对起点 = `data_base(34)+entry.offset`,按 `entry.size` 选帧;`entry.sha256` 是压缩区 SHA(非 payload SHA)。
- **wire 顺序 ≠ XML 顺序**(E94);`date_relationship_control` 类负结果原样保留。
- **EDsc 分发闭合**(E105):key `0x45447363` 归一化 `+0xbabb8ccf = 0x32`,表基址 `0x2a7f0` 第 `0x32` 格 → `0x29389`,按对象类型进 COMP/NATION Schedule 生成器并返 UI;是 UI 分发、非持久化字段,held 保持正确。

## 四、工作区未提交状态(本次梳理时)

```
 M  reports/club_nation_subtable_schema.json       # t70 v10 fold(6.4 MB 级)
 M  reports/club_nation_subtable_schema.md
??  scratch/t70/                                    # v9/v10 快照 + consolidate/verify 脚本 + spot 日志
??  scratch/t02/pi-logs/t70-*.log
??  scratch/t02/pi-sessions/2026-11-20T13-07-42-419Z_t70-*.jsonl
```

`t70` 的 DONE/REPORT 齐备、builder/verifier 的 `--help`/`--selftest`/`--check` 与退出码 1/2 探针全过、t01 anchors 7/7、L4=0。**指挥官已独立 spot 123 项(0 FAIL)并落 E110、提交 schema v10**;README 与本报告随后同步该状态。

## 五、仍开事项(接 BASELINE E109)

1. **EDfx 上游持久化来源**:仅 cmp @`0x29c37`,链路至 fles 容器/日历桶/NATION+`0x108` backlink,7 条可重开排除。
2. **未映射主行字段**:club 350 / comp 196 / nation 318(第二轮复查均为 0 新 L3,收益递减已量化)。
3. **comp 集合业务语义**:t66 仅物理层 7 文法 + 4 lane,+`0x100` 业务绑定仍 pending。
4. **held 枚举域批量补**:scoped `enum_ref` 专项。
5. **merge-to-main**:按 `HANDOFF.md` 搁置;schema v10 已提交,可评估。

## 六、磁盘占用大头(清理候选,本次未执行任何删除)

`scratch/` 独占 1.7 GB。最大的可复算中间产物集中在 `scratch/t26/`(`raw.pkl` 382 MB、`T.pkl` 202 MB、`trailers.pkl` 69 MB、`bp.pkl` 52 MB、`best.pkl` 44 MB,合计 ~750 MB)与 `scratch/t13d/out/t49.csv`(70 MB)。这些 `.pkl/.npy` 已被 `.gitignore` 排除、可由脚本复算。**本次仅梳理未删除**;如需回收空间,请先确认再单独处理。

## 七、参考

- 交接与恢复指令:`scratch/cmd/HANDOFF.md`
- 夜班/日班记录:`scratch/cmd/morning_report_2026-11-20.md`、`docs/BASELINE.md` 各增量节
- 逐条验收台账:`scratch/t01/LEDGER.json`
