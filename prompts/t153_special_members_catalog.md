# t153 — 13 个特殊成员 + `table_extra_*` + `summary.dat` 统一结构与语义目录

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 控制在 150 行以内**，分步构建脚本与落盘结果。

## 背景与目标
`t150` 已补齐 79 张编号表中剩余非主表的语义目录。除编号表外，`server_db.dat` / `client_db.dat` 中还包含 **13 个特殊字典成员**（如 `club_links`、`table_extra_3`、`table_extra_9`、`table_extra_24`、名称/语言字典等）以及独立的 `summary.dat`。
你的目标是综合 `t119`、`t130`、`t133`、`t136`、`t143` 的已有成果，编写 `scripts/t153_special_members_catalog.py`，产出这 13 个特殊成员 + `summary.dat` 的统一机读目录（成员名、client/server 体积、行数/条目数、物理布局摘要、已知语义与外键关联、证据等级 L1/L2/L3），并用真实 `.dat` 样本完成自检。

## 必读上下文与只读输入
- `AGENTS.md`、`docs/REPO_STATUS.md`、`scripts/fm24_config.py`
- `scripts/t130_archive_inventory.py`、`scripts/t133_fm24_reader_v2.py`
- `scratch/t136/out/archive_audit_v4.json`、`scratch/t136/out/REPORT.md`
- 路径统一通过 `import fm24_config` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 交付物
1. `scripts/t153_special_members_catalog.py`（支持 `--help`、`--selftest`，通过 `check_repo.py`）
2. `${OUTDIR}/special_members_catalog.json`（含 `"status": "complete"`、全部特殊成员与 `summary.dat` 清单、行数、语义与证据等级）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=special_members_catalog`）
