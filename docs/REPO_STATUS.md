# 仓库现状速览(2026-11-21, schema v11 同步)

本文件是一次只读梳理的快照,面向新接手者/新 session 快速定位。**结论性证据仍以 `BASELINE.md`、`reports/`、`scratch/t01/LEDGER.json` 为准**;本速览不改动任何验收口径。

## 一、身份与拓扑

| 项 | 值 |
|---|---|
| 使命 | FM24 `.dat` 数据库字段 → 行内偏移语义映射(详见 `AGENTS.md`) |
| 当前分支 | `t70-schemav10`(线性链,HEAD 已推进至 t82/E121) |
| 提交数 | 234 |
| 本地分支 | 36(任务分支 `tNN-短名` 线性链,见下) |
| 验收台账 | `scratch/t01/LEDGER.json`,**121 条**,末条 E121 |
| 远端 | `origin` = `github.com/van152/fm24-db.git` |
| 体积 | 2.0 GB(`.git` 190 MB、`scratch` 1.7 GB、`reports` 29 MB、`evidence` 15 MB) |
| 公共 schema | `reports/club_nation_subtable_schema.{json,md}` **v11**(29.9 MB / 87 KB) |

**分支拓扑**:主体是一条任务分支线性链 `t41-csme-cursor → … → t70-schemav10`,每次 pi dispatch 建新分支、指挥官在分支上提交,工作全部保留、尚未 merge-to-main。`main` 停在 `7a8a0bf`(初始化骨架),`github-snapshot` 停在 `c9e7dab`(脱敏快照,也是 `origin/main`)。远端自快照后无更新。

### v11 拆分件(体积治理)

v10 主 JSON 达 29.5 MB(大量内嵌批量记录:nation_t9_wire 1.27 MB、comp_collections 4.10 MB、r2 held/unmapped 清单)。v11 不改这些既有节(逐字节保留),而把本轮新增内容做成指针式:

| 文件 | 内容 | 体积 |
|---|---|---|
| `reports/club_nation_subtable_schema.json` | 三主表 + 8 编号子表 + CLUB_LINK + r2/r3 + v11 指针节 | 29.9 MB |
| `reports/other_tables_schema.json` | 13 张非主表槽位裁决(t73 4 + t76a 1 + t76c 4 + t74 行框 4) | 286 KB |
| `reports/xml_denominator_coverage.json` | 1,034 occurrence 分母台账(逐条含证据引用) | 298 KB |

主 schema 的 `pointer_artifacts` 节与 `coverage` 节都记有上述两文件的 path + SHA-256;`--verify` 会重算比对。

## 二、方法与硬约束(摘自 AGENTS.md)

- **证据分级**:L1 自检 / L2 独立事实对照 / L3 exe 静态证据(注明二进制、VA、来源)/ L4 真机加载(=0)。候选不写成结论,负结果原文保留不删改。
- **只读外部数据**:游戏库 `Z:`、旧证据库 `D:\tmp2b\fm24` 一律只读;不启动游戏/编辑器/IDA,除非显式授权。引用旧证据须经 `evidence/fm24/` 快照 + MANIFEST SHA-256。
- **Python 3.12**:`py -V:3.12 -I`;新脚本须有 `--help` 与 `--selftest`;退出码 0/1/2。
- **Git**:任务分支 `tNN-短名`;提交信息 `feat/fix/docs/chore(tNN): 摘要`;大数据/二进制不入库。
- **落地位置**:临时实验进 `scratch/<任务>/`,结论进 `reports/`,机读结果与报告同名成对。

## 三、进度脉络

### schema 版本演进(v3 → v11)

| 版本 | 任务/E | 并入内容 |
|---|---|---|
| v3 | t45 | 8 numbered 表基线 |
| v4 | t48/E88 | Cafl/Cvfl 并入 CLUB_LINK |
| v5 | t52/E92 | nation 侧(t47 Ntxr + t49 t9 wire),30 L3 |
| v6 | t54/E95 | TCrs 双闭裁决 |
| v7 | t56/E96 | t55 nation 主行 5 L3 |
| v8 | t58/E98 | t57 club 主行 13 L3 |
| v9 | t60/E100 | t59 comp 主行 49 L3 |
| **v10** | t70(E110) | E104–E109 r2 证据:club +8 L3(累计 21)、comp/nation 0 新 L3、7 文法 + 4 lane、EDsc 闭合、尾账 18 项 |
| **v11** | **t77(本轮)** | E111–E120 additive:club 主行 21→**43**(E111 extra_3 对象 22 cnst 投影 + Cebd/Cyfn)、三主表槽位指纹(E112)、city/cont/regi/curr 8 帧闭环(E113)、nation 10 段文法 + 99 槽裁决(E114)、9 表行框(E115)、分母 1,034(E116)、stadium/team L3(E117)、t76c 四表 + t76a stadium 槽位(E118/E120)。**E119=t80 枚举前提证伪(probe_negative,非验收)**;t76b 弃(award/language/media → t83) |

公共 schema 文件 `reports/club_nation_subtable_schema.json` 现为 **v11**(29.9 MB;v8 起体积主要由内嵌批量记录驱动),`.md` 87 KB(v10 字节为严格前缀 + t77 附录)。v10 的 JSON/Markdown SHA-256 记于 `scratch/t70/out/REPORT.md`,v11 的记于 `scratch/t77/out/`。

### 三张主表行框(per-table identity 宽度必须按表自证,不得照抄)

| 表 | 实体 | 行框 | identity | 主行 L3 |
|---|---|---|---|---|
| table_9 / extra_9 / table_10 | nation | client 13+24,710+9=24,732;server 13+422,323+9=422,345,各 251 行 | 13B(旧 13B 假设经敏感性反例修正) | 5 / 346 |
| table_3 | club | client 6,932,082 / server 16,595,312 B,84,259×2 行 | 12B(修正旧 13B) | 43 / 433 |
| table_25 | comp | client 13+894,969+9 / server 13+1,533,950+9,7,047×2 行 | 12B + 9B footer | 49 / 255 |

### 可复用方法资产

- **三重闸门**:frozen 唯一 occurrence → getter 4CC 精确分发 → 同位移 sink;配套目标实表 ordinal join + 条目级 ledger 守卫。已跨 t47/t49/t51/t53/t55/t57/t59 五次复用。
- **E80 修复**:成员绝对起点 = `data_base(34)+entry.offset`,按 `entry.size` 选帧;`entry.sha256` 是压缩区 SHA(非 payload SHA)。
- **wire 顺序 ≠ XML 顺序**(E94);`date_relationship_control` 类负结果原样保留。
- **EDsc 分发闭合**(E105):key `0x45447363` 归一化 `+0xbabb8ccf = 0x32`,表基址 `0x2a7f0` 第 `0x32` 格 → `0x29389`,按对象类型进 COMP/NATION Schedule 生成器并返 UI;是 UI 分发、非持久化字段,held 保持正确。

## 四、工作区未提交状态(本次梳理时)

```
 M  README.md                                    # v11 增量同步
 M  reports/club_nation_subtable_schema.json     # t77 v10 -> v11 additive fold(29.9 MB)
 M  reports/club_nation_subtable_schema.md       # v10 字节 + t77 附录
 M  docs/REPO_STATUS.md                          # 本次同步
 M  docs/BASELINE.md                             # 本次同步(E111-E120 增量节)
??  reports/other_tables_schema.json             # 新:13 张非主表槽位裁决(286 KB)
??  reports/xml_denominator_coverage.json        # 新:1,034 occurrence 分母台账(298 KB)
??  scripts/t77_*.py                             # builder / common / sections / verify
??  scratch/t77/                                 # 构建产物、diff summary、日志
```

`t77` 的 builder 三档全过:`--selftest` 7/7、`--build` 4/4、`--verify` **63/63**;`t01 anchors` 7/7;`baseline_coverage.py --check` 冻结数字不变;L4=0。**v11 纯增量已自证**:22 个 v10 根节 byte 不变(逐节 `==` 比对)、根键 = v10 + 新 10 节、既有 coverage 数字只改 `club_main_row_L3`(21→43)。E121(t82)已入账但不入 v11,归 t87 补丁。根目录 `nul` 0 字节事故产物已删除(`.gitignore` 早已覆盖)。

## 五、仍开事项(接 BASELINE E120)

1. **EDfx 上游持久化来源**:仅 cmp @`0x29c37`,链路至 fles 容器/日历桶/NATION+`0x108` backlink,7 条可重开排除。
2. **未映射主行字段**:club 350 / comp 196 / nation 318;分母口径已量化(E116):总 1,034 occurrence,物理覆盖 110/1,034 = 10.6%。其中 `unresolved_wire_slot` 277(club 20 槽命中率最高、comp 36 槽)、`no_wire_evidence` 564,`held` 59。
3. **award / language / media 三表槽位**:t76b 三连墙零落盘已弃,转 **t83** 接收(v11 中 `reports/other_tables_schema.json` 对应表标 `pending:t76b`)。
4. **comp 集合业务语义**:t66 仅物理层 7 文法 + 4 lane,+`0x100` 业务绑定仍 pending。
5. **held 枚举域批量补**:scoped `enum_ref` 专项。
6. **E121 补丁**:t82 的 table_extra_3 双对象闭合(35 新 L3 / 39 held / table_45 117 字段族正名)需 t87 并入 schema(v12 或 v11.1)。
7. **merge-to-main**:见下节专论。

## 六、merge-to-main 评估(本次只评估,不执行)

| 项 | 事实 |
|---|---|
| 分支形态 | 36 本地分支均为单条线性链上的任务分支;`HEAD` 是 `origin/main` 的**直接超集后继** |
| 领先/落后 | 领先 `origin/main` **234 个提交**,落后 **1**(`c9e7dab` 脱敏快照提交本身) |
| 内容差异 | `origin/main..HEAD` = 1,181 文件、+6,002,470 / −154,102 行 |
| 证据等级 | 全部 L1/L2/L3;**L4 = 0**(未做真机加载) |
| 回归 | `t01 anchors` 7/7;`baseline_coverage.py --check` 冻结数字不变 |
| 远端 | 自 `c9e7dab` 快照后 `origin` 无新提交,无并行漂移需要 rebase |

**结论:建议合并,但应先定口径再动手。** 理由:(a) 拓扑是快进式线性链、无并行分支冲突,合并动作本身风险极低;(b) 234 个提交的成果已在 `main` 之外累积两个月,再不合并会持续加大单次差异的审阅成本;(c) `L4=0` 不是合并阻塞项——仓内所有结论已按 L1/L2/L3 分级写明,合并只是把内部已验证的分级成果回主流,不构成"已验证可上线"的宣称。

**不建议立即执行的两个前提未满足项**:(1) `github-snapshot` 是**脱敏**快照,而工作区 234 个提交里含 `reports/club_nation_subtable_schema.json`(29.9 MB)与 `scratch/` 下大量原始派生数据——需先确认远端仓库的**体积与脱敏策略**是否接受 30 MB 级 JSON(否则应改为"合并但排除大文件"或走 LFS);(2) 合并前应把 `baseline_coverage.py --check`、`t01_anchors.py`、`t77_schema_v11.py --verify` 三道回归在同一 commit 上再跑一次并记入 ledger。

**未执行任何 merge 操作**;本节仅为评估。

## 七、磁盘占用大头(清理候选,本次未执行任何删除)

`scratch/` 独占 1.7 GB。最大的可复算中间产物集中在 `scratch/t26/`(`raw.pkl` 382 MB、`T.pkl` 202 MB、`trailers.pkl` 69 MB、`bp.pkl` 52 MB、`best.pkl` 44 MB,合计 ~750 MB)与 `scratch/t13d/out/t49.csv`(70 MB)。这些 `.pkl/.npy` 已被 `.gitignore` 排除、可由脚本复算。**本次仅梳理未删除**;如需回收空间,请先确认再单独处理。

## 八、参考

- 交接与恢复指令:`scratch/cmd/HANDOFF.md`
- 夜班/日班记录:`scratch/cmd/morning_report_2026-11-20.md`、`docs/BASELINE.md` 各增量节
- 逐条验收台账:`scratch/t01/LEDGER.json`
