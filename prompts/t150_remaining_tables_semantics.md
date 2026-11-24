# t150 — 其余非主表语义目录普查（补齐 79 编号表的语义覆盖）

## 背景与目标
`t133` 已实现全部 79 张编号表的纯 Python 零误差解码，`reports/other_tables_schema.json` 覆盖了其中 13 张非主表（2, 5, 19, 41, 21, 18, 27, 47, 56, 0, 7, 8, 24），大三主表（3, 9/10, 25）已由 `t136` 覆盖 85.7%。
但其余几十张编号表（如 1, 4, 6, 11..17, 20, 22, 23, 26, 28..40, 42..46, 48..78 中的非空表）目前只有物理行解码，缺少系统化的**表身份 + 核心列语义 + 外键映射目录**。
你的目标是为这些其余编号表建立机读语义目录（L2+L3 联合标注），填补全库语义拼图。

## 必读上下文与只读输入
- `AGENTS.md`、`docs/REPO_STATUS.md`
- `scripts/t133_fm24_reader_v2.py`（79 张表的物理结构）
- `reports/other_tables_schema.json`（已覆盖的 13 张非主表）
- `scratch/t142/out/`（84 表外键图谱）
- `scratch/t95/vtable_index.json`、`scratch/t108/out/fourcc_mem_map_v2.json`
- 路径统一通过 `scripts/fm24_config.py` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 方法要求
1. 枚举 79 张编号表中不在 `{3, 9, 10, 25}` 且不在 `other_tables_schema.json` 13 表中的全部剩余表，记录每张表的 client/server 行数、RTTI 类名（来自 `vtable_index.json`）、物理列结构（来自 `t133`）、外键关系（来自 `t142`）以及可匹配到的 4CC 语义字段（来自 `fourcc_mem_map_v2.json`）。
2. 抽取典型真实样本行验证语义（L2 锚点，例如语言、颜色、伤病、阵型、转会偏好、规则、历史记录等），未确认列明确标为 `unnamed` 或 `candidate`，严禁编造。
3. 严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有脚本。
4. 新脚本必须使用 `import fm24_config`，支持 `--help` 和 `--selftest`，通过 `check_repo.py`。

## 交付物
1. `scripts/t150_remaining_tables_semantics.py`（`--help`、`--selftest` 全过）
2. `${OUTDIR}/remaining_tables_semantics.json`（含 `"status": "complete"` 或 `"partial"`、逐表身份/行数/列语义/证据等级汇总）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=remaining_tables_semantics`）
