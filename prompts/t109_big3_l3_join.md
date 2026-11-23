# t109 — 三大主表（CLUB / NATION / COMP）1,034 分母全自动 L3 Join 与覆盖率跃升审计

> 交付目录：`OUTDIR`（`scratch/t109/out`）
> 脚本路径：`scripts/t109_big3_l3_join.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：
> - `scratch/t108/out2/fourcc_mem_map_v2.json`、`xml_triage_v2.json`、`static_read_join_v2.json`
> - `scratch/t105/out/big3_serializers.json`
> - `scratch/t95/funcs/*.c`（全部 1,173 份 Hex-Rays C 文件，含 t107 补反编译的 524 个 helper）
> - `reports/xml_denominator_coverage.json`、`reports/club_nation_subtable_schema.json`
> - 若 `scratch/t96b/out/wire_traces_v2.json` 或 `scratch/t98/out/table45_full_schema.json` 已存在也可只读融合；若尚未落盘则纯静态完成并预留 `--with-unicorn` 接口。
> 不要修改 `reports/` 或 `LEDGER.json`。

## 背景
经过 `t95` + `t107` + `t108b` + `t105`，我们现在手握三大主表完整的 Hex-Rays 源码（1,173 份 C 文件）：
- `t108b` 已将 1,034 分母的 4CC → `mem_off`（含 2-hop helper 与 725 个 `child_table` 子表落位）做到 **18/18 回归 0 mismatch**！
- `t105` 已拆出 `CLUB`/`COMP`/`NATION`/`NATIONAL_TEAM_CONTAINER` 全部 8 个序列化器的 **274 个有序读取步骤**（及基类 `TEAM_CONTAINER::slot19` `1411d1730.c`）！
- 但 `reports/xml_denominator_coverage.json` 原口径物理 L3 覆盖率还停留在 `110 / 1,034 (10.6%)`！

## 任务目标

### 1. 构建「4CC ↔ mem_off ↔ 序列化器读流步骤」严格 L3 Join 引擎
对 `club (433)`、`nation (346)`、`comp (255)` 合计 1,034 条分母，逐条执行**三重静态 L3 闭合检查**：
1. **路径 A（本对象主行持久化）**：
   - `t108b` 给出 `4CC → mem_off`（带 `get_prop`/`set_prop` VA 与精确 C 行号）
   - 在本类或其基类（如 `CLUB → TEAM_CONTAINER`、`NATIONAL_TEAM_CONTAINER → TEAM_CONTAINER`、`NATION ↔ NATIONAL_TEAM_CONTAINER`）的 `slot19` (`read_server` / `read_client`) 或其调用的 serializer helper 中，找到**精确写入同一 `mem_off`（或覆盖该字节的 coalesced span / bitfield 槽）** 的读流调用（带 VA 与精确 C 行号、`wire_width`、`a7` server/client 门控、`dbver` 版本门控）！
   - 满足双侧精确闭合 → 授予候选级别 **`L3_static_closed`**！
2. **路径 B（子表 / 关联对象持久化）**：
   - `t108b` 已证明 `4CC` 经由 `0x1411e9540` / `0x143ca2e60` / 子对象指针（`subobj_deref` / `child_table`）路由到 `STARTING_RECORD` (`table_45`)、`TEAM` (`table_24`)、`STADIUM` (`table_21`) 或 `table_extra_3/9` 等明确持久化表，并定位到目标表内的 `mem_off` 与其 `slot19` 读流步骤 → 授予 **`L3_subtable_routed`**！
3. **路径 C（纯 UI / 编辑器派生 / 引擎计算 / 仅存档排除）**：
   - `t108b` 证明全 67 表 `get_prop/set_prop` 皆无该 4CC（`absent_everywhere`，312 条），或仅命中 `confirmed_computed_or_ui`（68 条）→ 授予 **`excluded_non_db_l3`**，正式给出**净持久化分母**（扣除明确非 DB 字段后的真实覆盖率）！
4. **剩余缺口精准定位**：
   - 对仍未闭合的条目（例如 `4CC` 有 `mem_off` 但 `slot19` 中尚未见该偏移，或 `helper_computed` 仍缺少数未反编译 helper），按成因分类并输出精准的待查清单（如位于 `table_extra_3`、`table_extra_9` 或仍需反编译的 Top 30 helper VA）。

### 2. 独立交叉校验（防幻觉）
- 拿 `reports/club_nation_subtable_schema.json` 里既有全部已验收 L3 字段（club 43/78、comp 49、nation 5+30）做全量交叉核对：我们的自动 Join 引擎不得与已验收 L3 产生偏移冲突（任何差异必须逐条列明原因）。

## 交付物（写入 `OUTDIR = scratch/t109/out`）
1. `big3_l3_join.json`：含 `"status": "complete"`，1,034 条分母逐条 L3 闭合记录（每条含 `code`, `entity`, `old_bucket`, `new_class`, `mem_off`, `getter_cite`, `serializer_cite`, `wire_width`, `server_only`, `child_table`）。
2. `coverage_summary.json`：原口径（110/1,034 = 10.6%）vs 新口径（总分母 1,034 与扣除非 DB 字段后的净持久化分母覆盖率！）分实体精确统计 + 已验收 L3 对账结果。
3. `remaining_gaps.json`：未闭合条目的精准归因与 Top 30 待补反编译 helper VA。
4. `REPORT.md`：人类可读的突破报告（清晰对比表格 + 典型新解锁字段样例）。
5. `DONE.md`：含 `DONE type=t109` 与核心统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t109_big3_l3_join.py --selftest` 退出 0。
- 1,034 条分母严格守恒（`club 433 + nation 346 + comp 255 = 1034`，零丢行、零重复）。
- 每一条 `L3_static_closed` 必须同时给出 `getter/setter` 的 `file:line` 与 `serializer` 的 `file:line`。
