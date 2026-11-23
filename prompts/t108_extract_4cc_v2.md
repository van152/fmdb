# t108 — 4CC ↔ 内存偏移 v2（内联追踪 t107 新反编译的 500+ helper）+ 1,034 分母深度闭环

> 交付目录：`OUTDIR`（`scratch/t108/out`）
> 脚本路径：`scripts/t108_extract_4cc_v2.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：
> - `scripts/t97_extract_4cc_mem.py`（基线解析器，不要覆盖，新建 `scripts/t108_extract_4cc_v2.py` 扩展）
> - `scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（现已增补至 ~800+ 份 Hex-Rays C 文件！）
> - `scratch/t107/out/helpers_index.json`（t107 补反编译的 500+ helper 索引）
> - `scratch/t97/out/xml_triage.json`、`reports/xml_denominator_coverage.json`、`reports/club_nation_subtable_schema.json`
> 不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标

### 1. 解决 t97 的两个核心遗留
1. **1-hop / 2-hop helper 内联解析**：
   - t97 中有 **2,525 个 `helper_computed` 分支**（含 `club` 205、`comp` 134、`nation` 122），因为像 `0x1411e9540` (400次)、`0x1411f4bd0` (88次)、`0x143ca2e60` (73次)、`0x140fead00` (63次)、`0x140e75ff0` (36次) 等高频 helper 此前尚未反编译。
   - 现在这些 helper 已全部通过 IDA 9.4 反编译落盘到 `scratch/t95/funcs/<va>.c`（带 thunk 别名文件）！
   - 当某 4CC 分支调用 `helper(this, ...)` 或 `helper(*(this + off), ...)` 或 `helper(this + off, ...)` 时，追踪进入 `scratch/t95/funcs/<helper>.c`（最多 2 跳）：
     - 若 helper 是简单的 getter/setter（直接读/写 `arg0 + K`），把最终对象偏移（或二级偏移 `0xOFF->0xK`）提升为 `resolved_via_helper`！
     - 若 helper 是次级 4CC 分派器（例如 `0x1411e9540` / `0x143ca2e60` 接收 `code` 参数再 `switch(code)`），把该 4CC 在次级分派器内的精确 `mem_off` 抽取出来！
     - 若 helper 明确是从全局变量 / 运行时状态 / 字符串拼接 / 纯计算返回且不触碰对象持久化字段，标为 `confirmed_computed_or_ui`！
2. **修复 `Cnti` 回归（`mismatch == 0`）**：
   - t97 回归检查 18 条已验收 L3 中，17 条正确，仅 `Cnti` 选到了 `185 (0xb9)` 而非 `216 (0xd8)`（`v86 = *(_QWORD *)(a1 + 216)`）。
   - 修复候选排序逻辑（外层分支/子对象指针优先于内层附属标量），确保对 18 条已验收 L3 的验证 **`mismatch: 0`**，并把 `Cnti == 216` 写进 `--selftest`！

### 2. 重跑全 67 表与 1,034 分母分诊，对比 t97 → t108 跃升
- 对比 `t97` 与 `t108` 的变化：
  - `direct_field` + `bitfield` + `subobj_deref` + `resolved_via_helper` 合计新增多少条？
  - `club (433)` / `nation (346)` / `comp (255)` 的 `unresolved_wire_slot` (160)、`held` (59)、`no_wire_evidence` (564) 各有多少条从 `helper_computed` 升级为精确 `mem_off` / `subobj_off`？
  - 静态 `slot19/slot20` 交叉命中数从 t97 的 802 提升到了多少？

## 交付物（写入 `OUTDIR`）
1. `fourcc_mem_map_v2.json`：含 `"status": "complete"`，全 67 表 v2 映射（带 `helper_chain` 溯源与精确 C 行号）。
2. `xml_triage_v2.json`：1,034 条分母 v2 分诊与 `t97 -> t108` 提升对比矩阵。
3. `static_read_join_v2.json`：全表 `4CC ↔ mem_off ↔ slot19/slot20` 交叉表。
4. `REPORT.md`：清晰对比表（`t97` vs `t108`）、18/18 回归 0 mismatch 证明、新解锁的核心 `CLUB`/`COMP`/`NATION` 字段清单。
5. `DONE.md`：含 `DONE type=t108` 与核心统计数字。
