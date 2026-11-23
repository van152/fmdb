# t110 — 全库 67 表 Unicorn 动态 Wire × IDA 4CC 区间重叠自动 Join 与统一 L3 总账生成

> 交付目录：`OUTDIR`（`scratch/t110/out`）
> 脚本路径：`scripts/t110_master_l3_schema.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：
> - `scratch/t96c/out/wire_traces_master.json`（Unicorn 真机微执行 79 表对：41 整表 `diff=0` 闭合 + 27 大表 50 行零异常 = **68/79 跑通**）
> - `scratch/t96c/out/table9_251_closure.json`、`table10_251_closure.json`
> - `scratch/t108/out2/fourcc_mem_map_v2.json`（全 67 表 8,046 条 4CC→`mem_off`，18/18 L3 回归 0 mismatch）
> - `scratch/t95/vtable_index.json`、`reports/club_nation_subtable_schema.json`、`reports/other_tables_schema.json`、`reports/xml_denominator_coverage.json`
> - 若 `scratch/t98/out/`, `scratch/t99/out/`..`scratch/t109/out/` 中任何车道已完成（有 `DONE.md`），自动兼容读取作补充标注（缺失不报错）。
> 不要修改 `reports/` 或 `LEDGER.json`。

## 任务目标

### 1. 构建「区间感知（Range-Aware）」双引擎 L3 自动 Join
普通精确匹配（`unicorn.obj_off == ida.mem_off`）单在 server 端 5 秒初测就已自动连出 **53 张表、436 条 L3 映射**！
请把 Join 升级为**完整区间 + 继承链 + 双端（server + client）精确 Join**：
1. **区间重叠匹配**：Unicorn 一次 `stream->read(dst=this+O, len=W)` 写入字节区间 `[O, O+W)`（如 `CLUB` 的 6 字节 coalesced span `0x160..0x165` 或位域槽、4/8 字节结构体、12 字节 identity `0x8..0x13`）。凡 IDA `t108b` 中 `mem_off ∈ [O, O+W)`（或 `subobj_deref` 基指针落在 `[O, O+W)`）的 4CC，均精确计算**槽内字节偏移 `in_slot_off = mem_off - O`** 并完成 Join！
2. **双端对比（server vs client）**：对同时存在于 `server_db.dat` 和 `client_db.dat` 的表，分别给出 `server` 与 `client` 的 wire 序列、并标注哪些字段为 `server_only`（仅 `a7=1` 出现）vs `shared`（双端共享）。
3. **跨类合并**：注意 `tt=3` 合并 `CLUB` + `TEAM_CONTAINER`，`tt=9` 合并 `NATIONAL_TEAM_CONTAINER` + `TEAM_CONTAINER`，`tt=24` 合并 `TEAM` + `NATIONAL_TEAM`，`tt=45/48` 共享 `STARTING_RECORD`。
4. **独立回归防幻觉**：把 Join 结果与 `reports/club_nation_subtable_schema.json` 既有 L3 槽位逐条核对，报告 `exact` / `within_slot` / `mismatch`（目标 `mismatch == 0`，有差异必须逐条解释原因）。

### 2. 产出全库 67 表统一机读 L3 总账 + 覆盖率里程碑
- 按表统计（全部 63 张 dedicated 表 + 11 张 default 空表）：
  - `unicorn_status`: `CLOSED (diff=0)` | `OK_SAMPLE (50 rows)` | `FAIL` | `NOT_IN_SERVER_CLIENT_DB`
  - `server_wire_fields` / `client_wire_fields`
  - `joined_l3_fourccs`（精确命中的 4CC 数量与列表，每条附 `wire_off_row0`, `wire_len`, `obj_off`, `in_slot_off`, `caller_va`, `getter_cite`）
  - `unmatched_wire_fields`（有 wire 读但未命中 4CC 的列，如字符串/动态数组/内部标志）
- 生成全库进度总览：从此前 **6/74 表** 跃升到 **多少张表已获得机器执行级 L3 字段映射**！

## 交付物（写入 `OUTDIR = scratch/t110/out`）
1. `master_67tables_l3.json`：含 `"status": "complete"`，全库统一 L3 schema 总账（紧凑、清晰、可被未来只读库直接消费，体积 < 15 MB）。
2. `coverage_milestone.json`：按表覆盖矩阵、server/client 统计、既有 L3 回归对账结果。
3. `REPORT.md`：全库 67 表全景总表 + 核心大表详细样例 + 剩余 11 张 Unicorn 失败表清单。
4. `verify.py`：独立校验脚本（重跑完整性、回归对账、无越界偏移断言）。
5. `DONE.md`：含 `DONE type=t110` 与核心统计数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t110_master_l3_schema.py --selftest` 退出 0。
- `py -V:3.12 -I -B scratch/t110/out/verify.py` 退出 0。
- 必须真实读取并 Join `scratch/t96c/out/wire_traces_master.json` 与 `scratch/t108/out2/fourcc_mem_map_v2.json`，打印实际 Join 表数、总 L3 映射数、回归结果。
