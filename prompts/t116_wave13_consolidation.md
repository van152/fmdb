# t116 — Wave 13（工具化突破总波次）全量产物汇总校验、v12 候选增量账与总报告

> 交付目录：`OUTDIR`（`scratch/t116/out`）
> 脚本路径：`scripts/t116_wave13_consolidation.py`（Python 3.12 `-I -B`，须含 `--help`、`--selftest`，退出码 0/1/2）
> **严格只读约束**：不得修改 `reports/`、`scratch/t01/LEDGER.json` 或任何其他 `scratch/tNN/` 目录；所有输出只写 `scratch/t116/out/` 与 `scripts/t116_wave13_consolidation.py`。

## 背景（Wave 13 已完结核心产物清单）
本波次首次打通 IDA Pro 9.4 `idalib` + Hex-Rays x64 与 Unicorn x86_64 真机微执行，已落地大量机读产物：
- `t95` (`scratch/t95/vtable_index.json` + `funcs/*.c` 共 1,173 份 C 文件)
- `t96c` (`scratch/t96c/out/wire_traces_master.json`, `table9_251_closure.json`, `table10_251_closure.json`, `REPORT.md`) — **74/79 (93.7%) 表对跑通，42 张整表 `diff=0` 闭合（含 `server/client t9` 251/251 全部 211 种行长、`server/client t10` 251/251 195 种行长）**
- `t97` (`scratch/t97/out/*`) & `t107` (`scratch/t107/out/helpers_index.json`) & `t108b` (`scratch/t108/out2/*`) — 全 67 表 8,046 对 4CC→`mem_off`，3,720 偏移，725 `child_table`，18/18 已验收 L3 回归 0 mismatch
- `t105` (`scratch/t105/out/big3_serializers.json`) — 三大主表 8 序列化器 274 步骤 + 版本门控
- `t109c` (`scratch/t109/out/*`) — 三大主表 1,034 分母覆盖率从 **10.6% → 36.7%（379/1,034）**，净持久化覆盖率 **56.3%（379/673）**
- `t110` (`scratch/t110/out/master_67tables_l3.json`, `coverage_milestone.json`, `verify.py`) — **55 张表、1,056 条 Unicorn×IDA 执行级 L3 映射**
- `t113b` (`scratch/t113/out/people_vtables_full.json`) & `t115` (`scratch/t115/out/basic_people_l3_schema.json`) — `basic_people_db.dat` **658,011 行 `diff=0` 闭合** + Kane/Ronaldo/Messi 实测命中 + 428 个人物 4CC
- **动态检测仍在收尾的兄弟车道**：运行时自动扫描 `scratch/t98/out`、`scratch/t99/out`..`scratch/t104/out`、`scratch/t106/out`、`scratch/t112/out` 中已落盘的 `DONE.md` / JSON，有则纳入统计、无则标 `in_flight`（不报错）。

## 任务目标
1. **统一溯源与回归体检（`scripts/t116_wave13_consolidation.py`）**：
   - 计算并记录全部已完结 Wave 13 核心机读产物的路径、字节数、SHA-256、`"status"` 与核心指标。
   - 以只读子进程跑一遍基线锚点与各新脚本自检（`scripts/t01_anchors.py`、`t97_extract_4cc_mem.py --selftest`、`t108_extract_4cc_v2.py --selftest`、`t109_big3_l3_join.py --selftest`、`t110_master_l3_schema.py --selftest`、`scratch/t110/out/verify.py`、`t115_basic_people_full.py --selftest`），把每一项退出码与关键输出写入校验表。
2. **生成 `Before (v11.3 / E140) vs After (Wave 13)` 精确突破对照表**：
   - 对比：已透表数（6/74 → 55+/74）、三大主表 1,034 总/净覆盖率（10.6% → 36.7% / 56.3%）、Unicorn 字节闭合表数（0 → 42 整表 + 32 大表 = 74/79）、`table_9` 211 种变长行闭合、`basic_people` 658,011 行闭合、v11.3 未决项 #1–#5 逐条状态。
3. **起草 `ledger_candidates.json`（E142–E150 候选台账草稿）**：
   - 按 `scratch/t01/LEDGER.json` 现有条目结构格式，在 `scratch/t116/out/ledger_candidates.json` 里起草本波次待入账候选条目（带 SHA-256、证据等级 L1/L2/L3、诚实标注 `partial` 项），供指挥官审阅后决定是否入账（**绝不直接修改 `LEDGER.json`**）。

## 交付物（写入 `OUTDIR = scratch/t116/out`）
1. `wave13_consolidated.json`：含 `"status": "complete"`，全产物 SHA-256 清单、回归体检矩阵、Before/After 指标对比、in-flight 车道状态。
2. `ledger_candidates.json`：E142+ 候选台账草稿。
3. `WAVE13_EXECUTIVE_REPORT.md`：给用户看的高管级中文战报（一目了然的数据对比表、核心技术突破、可点击路径、剩余工作与下一步建议）。
4. `verify_wave13.py`：独立校验脚本。
5. `DONE.md`：含 `DONE type=t116` 与核心统计数字。
