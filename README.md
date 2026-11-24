# fm24-db

FM24 `.dat` 数据库格式逆向与双向读写工程的工作仓库。

## 当前状态（2026-11-24）

| 项 | 值 |
|---|---|
| 分支 | `main`（HEAD `2b11ee9`） |
| 提交数 | 292 |
| 远端 | `origin` = `github.com/van152/fmdb.git`，`origin/main` 与本地 HEAD 一致 |
| 公共 schema | `reports/club_nation_subtable_schema.json` **v11.3**（`generated_by: t92`，21.4 MB） |
| 验收台账 | `scratch/t01/LEDGER.json` 142 条，末条 E142 |
| 回归套件 | `scripts/t145_final_regression.py` |

## 从哪里读

1. `docs/REPO_STATUS.md` — 仓库现状、环境要求、未结项；**新接手先读这份**
2. `docs/BASELINE.md` — 覆盖率冻结基线与增量记录
3. `AGENTS.md` — 目标、边界与脚本约定
4. `WAVE14_MORNING_REPORT.md` — 叙事性总结，**不是验收依据**；结论以台账、脚本输出和机读产物为准

## 目录

- `docs/` — 基线、现状速览、外部引用
- `prompts/` — 各任务（tNN）的原始任务说明（历史归档）
- `scripts/` — 解码/普查/复算/回归脚本（Python 3.12）
- `reports/` — 公共 schema 与正式机读结论
- `evidence/fm24/` — 旧证据库只读快照（带 SHA-256 清单）
- `scratch/` — 实验、会话、中间产物（**不验收；仅 `t01/LEDGER.json` 入库**）
- `scratch/t01/LEDGER.json` — 逐条验收台账

## 运行前准备

见 `docs/REPO_STATUS.md` 的“环境与可复现”节。简言之：Python 3.12、外部游戏库与旧证据库路径、vendor 版 `zstandard`；路径统一由 `scripts/fm24_config.py` 解析，可用环境变量覆盖。
