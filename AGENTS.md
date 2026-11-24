# AGENTS.md — fm24-db

## 项目地图

| 路径 | 作用 |
|---|---|
| `AGENTS.md` | 本文件，工作约定 |
| `README.md` | 导航与当前状态速查 |
| `docs/REPO_STATUS.md` | 仓库现状、环境与验证命令（新接手先读） |
| `docs/BASELINE.md` | 覆盖率冻结基线 + 增量记录 |
| `docs/refs.md` | 外部只读引用与路径 |
| `prompts/` | 各任务（tNN）的原始任务说明，历史归档 |
| `scripts/fm24_config.py` | 统一路径/依赖配置（新脚本必须使用） |
| `scripts/` | 解码/普查/复算/回归脚本（Python 3.12） |
| `reports/` | 公共 schema 与正式机读结论 |
| `reports/club_nation_subtable_schema.json/.md` | 公共 schema（当前 v11.3） |
| `evidence/fm24/` + `evidence/MANIFEST.json` | 旧证据库只读快照（带 SHA-256） |
| `scratch/<任务>/` | 临时实验、会话与 IDA 产物（不入验收，大部分不入版本库） |
| `scratch/t01/LEDGER.json` | 逐条验收台账 |
| `WAVE14_MORNING_REPORT.md` | 叙事性总结，不是验收依据 |

## 目标与当前状态

| 阶段 | 目标 | 状态 |
|---|---|---|
| 一 | 编号表零误差解码 | 已达成：79/79 编号表 + 13 特殊成员 + summary.dat，13/13 `.dat` 档案纯 Python diff=0 |
| 二 | 表身份与行边界映射 | 已达成：三主表行框自证闭合；剩余少量非主表语义未命名 |
| 三 | 字段语义映射 | 进行中：大三主表净覆盖 568/663 = 85.7%（毛覆盖 568/1034 = 54.9%） |
| 四 | 双向读写与验证 | 已达成：79/79 位级回写 + editor.exe 机器码回读；完整游戏内加载（L4）仍未做 |
| 五 | 人物属性 | 已纳入范围：球员 54/54 PDxx，非球员 34 项属性；见 t126 / t137d |

## 边界与硬约束

- **证据分级**：L1 自检 / L2 独立事实对照 / L3 exe 静态或机器码仿真证据（注明二进制、VA、来源）/ L4 完整真机加载。候选不写成结论，负结果原文保留不删改。
- **外部数据只读**：游戏库、旧证据库、`scratch/data` 中的原始 `.dat` 一律只读；引用旧证据须经 `evidence/fm24/` 快照 + MANIFEST SHA-256。
- **工具链**：Python 3.12；核心脚本提供 `--help` 与 `--selftest`，退出码 0/1/2。
- **路径**：新脚本不得硬编码 `D:\`、`Z:\` 等绝对路径，统一用 `scripts/fm24_config.py` 提供的变量（可用环境变量覆盖）。
- **Git**：提交信息 `feat/fix/docs/chore(tNN): 摘要`；大数据/二进制不入库；`reports/` 与 `scratch/t01/LEDGER.json` 受回归套件保护，测试不得写入。
- **落地位置**：临时实验进 `scratch/<任务>/`，结论进 `reports/`，机读结果与报告同名成对。
