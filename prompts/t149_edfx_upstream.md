# t149 — EDfx 上游持久化来源终极追查

## 背景与目标
`docs/REPO_STATUS.md` 第六节第 1 条指出：`EDfx` 上游持久化来源仍未闭合。
此前 `t62`（`scratch/t62/out/REPORT.md`、`chain.json`、`exclusions.json`）仅追到 `0x29c37` 比较以及 `fles`/`comp`/日历内存桶/`NATION+0x108` backlink，未验到具体 `.dat` reader/writer。
现在我们已拥有 `editor.exe` 全库 79/79 编号表 + 13 特殊成员解析器（`t133`）与 Unicorn/Capstone 工具链，需要给出 `EDfx` 的终局裁决：**要么证明它绑定到具体的 `.dat` 表/成员/偏移（L3），要么以机器码级证据确证它属于纯运行时/编辑器规则层字段而非 `.dat` 持久化字段（诚实负结果闭合）**。

## 必读上下文与只读输入
- `AGENTS.md`、`docs/REPO_STATUS.md`
- `scratch/t62/out/REPORT.md`、`scratch/t62/out/DONE.md`、`scratch/t62/out/chain.json`、`scratch/t62/out/exclusions.json`
- `scripts/t62_edfx_edsc.py`
- `scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`、`scratch/t108/out/fourcc_mem_map_v2.json`
- `scripts/t133_fm24_reader_v2.py`
- 路径统一通过 `scripts/fm24_config.py` 读取（禁止硬编码 `D:\` 或 `Z:\`）。

## 方法要求
1. 从 `t62` 的 7 条可重开条件切入，在 `editor.exe`（`fm24_config.EDITOR_EXE`）中反汇编并追踪 `EDfx`（`0x45446678`）及 `fles` 容器、`NATION+0x108` backlink 的写回路径（谁往这些容器里写数据、是否来自任何 `table_*.dat` 或特殊成员或 XML 规则文件）。
2. 严守证据分级，不得臆测；若为非 `.dat` 持久化字段，须给出完整的写者调用链与排除见证。
3. 严禁修改 `reports/`、`scratch/t01/LEDGER.json` 及既有 `t62` 文件。
4. 新脚本必须使用 `import fm24_config`，支持 `--help` 和 `--selftest`，通过 `check_repo.py`。

## 交付物
1. `scripts/t149_edfx_upstream.py`（`--help`、`--selftest` 全过）
2. `${OUTDIR}/edfx_verdict.json`（含 `"status": "complete"` 或 `"negative"`、结论、VA/指令见证链）
3. `${OUTDIR}/REPORT.md` 与 `${OUTDIR}/DONE.md`（首行含 `DONE type=edfx_upstream`）
