# t146 — Club 剩余 49 个缺口深挖收口（Big-3 v5 / Club 线）

## 背景与目标
`scratch/t136/out/remaining_gaps_v4.json` 中 `entity == "club"` 仍有 **49 个未闭合缺口**（`gap_off_not_in_read_stream`: 24、`gap_delegated_or_empty`: 13、`gap_helper_computed`: 9、`gap_other_table_same_tag`: 3），使 club 净覆盖停在 222/271 = 81.9%。
你的目标是逐条深挖这 49 个 club occurrence，力争将可证字段升级到 L3，或以机器码级证据确证其为非持久化/派生字段，无法闭合者保留并给出精确阻断点。

## 必读上下文与只读输入
- `AGENTS.md`、`docs/REPO_STATUS.md`
- `scratch/t136/out/remaining_gaps_v4.json`（只取 `entity == "club"` 的 49 条）
- `scratch/t136/out/hop_audit_v4.json`、`scratch/t136/out/big3_l3_v4.json`
- `scripts/t125_big3_gap_closure.py`、`scripts/t136_big3_final_closure.py`
- `scratch/t95/funcs/*.c`、`scratch/t124/out/funcs/*.c`、`scratch/t132/out/funcs/*.c`
- `scratch/t108/out/fourcc_mem_map_v2.json`
- 二进制与 `.dat` 路径统一通过 `scripts/fm24_config.py` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 方法要求
1. 严格遵守证据分级（L1/L2/L3/L4）：候选不写成结论，负结果原文保留。
2. 对每一条 club 缺口，结合现有反编译 `.c` 文件、`editor.exe` 机器码静态反汇编（可用 capstone）或 Unicorn 仿真，追踪完整的 `4CC getter/setter -> receiver 对象 -> 内存偏移 -> slot19 reader / 子表 / table_extra_3 / table_24 / club_links / table_45 / table_48 / lang_db`。
3. 严禁修改 `reports/` 与 `scratch/t01/LEDGER.json`，严禁修改既有 `t136` 或更早脚本。
4. 新脚本必须使用 `import fm24_config`，支持 `--help` 和 `--selftest`（退出码 0/1/2），且通过 `py -V:3.12 -B scripts/check_repo.py` 检查。

## 交付物
1. `scripts/t146_club_gaps_v5.py`（可执行、`--help`、`--selftest` 全过）
2. `${OUTDIR}/club_gaps_v5.json`（包含 `"status": "complete"` 或 `"partial"`、49 条逐条裁决、守恒统计、前后对比）
3. `${OUTDIR}/REPORT.md`（清晰列出新闭合 L3、新确证排除、仍保留缺口与精确阻断点）
4. `${OUTDIR}/DONE.md`（首行含 `DONE type=club_gaps_v5` 及验收摘要）
