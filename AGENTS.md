# AGENTS.md — fm24-db 工作区

## 使命(唯一)

**FM24 数据库(`.dat`)语义解析:把 schema 字段映射到行内偏移。**

容器/解压层已 100% 解完(无加密,`tad.` 外壳 + Zstd);本工作区不做解密、不做格式研究、不做 FMF 生成器、不做存档研究。跨出本使命的任务回到 `<OLD_REPO>` 旧仓库体系。

## 三阶段目标与验收

| 阶段 | 目标 | 验收判据 |
|---|---|---|
| **一** | comp 表 packed 区(table_25 client 行 +0..51 / +68..113) | ≥10 个业务字段获得 L3 槽位定位,且与既有 L2 锚点(六大洲 0..5、England=139/China PR=55、parent row 352)交叉不矛盾 |
| **二** | 50 张 unknown 数值表的表号→实体映射 | 每张表至少 1 个独立锚点;优先复用阶段一发现的通用映射结构 |
| **三** | club/nation 批量字段映射(433+346 字段) | 字段台账逐字段记录证据等级;不设"全解"为验收线,按"能支撑编辑问题"滚动 |

person 属性块(PDxx)不在本工作区范围;如需启动须用户明示。

## 硬约束

1. **只读外部数据**:游戏安装库(`<GAME_DRIVE>\...`)与旧证据库(`<OLD_REPO>`)一律只读;不启动游戏/编辑器,除非用户对具体任务明确授权。
2. **证据分级沿用旧仓口径**:L1 自家解码自检 / L2 独立事实对照 / L3 exe 静态证据(须注明二进制、VA、来源)/ L4 真机加载。候选不写成结论;负结果必须保留原文,不得删除或改写。
3. **引用旧证据必须经 `evidence/fm24/` 快照并对照 `evidence/MANIFEST.json` 的 SHA-256**;快照日期 2026-11-18,之后的旧库变更不在快照内,引用原始路径时须注明。
4. **IDA 库不复制入库**(501MB):`<OLD_REPO>\ida\editor_merge_v2.i64` 与 `input\editor.exe`、`input\fm.exe` 按只读引用;IDA 会话产物只进 `scratch/<任务>/`。
5. **Python 3.12**:`py -V:3.12 -I ...`;新脚本须有 `--help` 与 `--selftest`;退出码 0 成功 / 1 检查未过 / 2 用法或致命错误。
6. **Git**:任务分支 `tNN-短名`;提交信息 `feat/fix/docs/chore(tNN): 摘要`;大数据与二进制不入库(`.gitignore` 已覆盖)。
7. **临时实验写 `scratch/<任务>/`**;结论文档进 `reports/`,机读结果与报告同名成对。

## 任务起点与当前进度

起步任务(2026-11-18 订立;状态更新至 2026-11-20):

- **t01**:editor.exe 字段槽位映射侦察——找 table type → schema 字段 → 行内偏移的映射结构。线索:`PROPERTY_MAP.md` 的 `database_table_type=25`→`cext` 反推先例、`fm.i64` `sub_1449A06C0` 手法复刻、86 份既有伪代码(`<OLD_REPO>\reports\reverse_engineering\`)。**已演化为 t41–t70 主线**:三重闸门法(frozen 唯一 occurrence → getter 4CC 精确分发 → 同位移 sink)+ 目标 ordinal join + 条目级 ledger 守卫,已跨多任务复用。
- **t02**:单变量编辑器对照(需用户授权)——**仍未启动**,保持只读,未经显式授权不做。
- **t03**:把既有 L2 锚点固化为回归项——**已落地** `scripts/t01_anchors.py`(7/7)。

当前:分支 `t70-schemav10`,公共 schema v10、LEDGER 110 条(E110)。完整拓扑、版本演进、仍开事项见 [docs/REPO_STATUS.md](docs/REPO_STATUS.md)。

## 基线与进度

- 覆盖率基线:[docs/BASELINE.md](docs/BASELINE.md)
- 外部只读引用:[docs/refs.md](docs/refs.md)
