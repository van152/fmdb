# t97 — 全量 67 表 Hex-Rays 4CC ↔ 内存偏移自动抽取与 XML 1,034 分母分诊

> 交付目录：`OUTDIR`（`scratch/t97/out`）
> 脚本路径：`scripts/t97_extract_4cc_mem.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（全部只读）：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（283 份 IDA 9.4 Hex-Rays 反编译 C 文件）、`reports/xml_denominator_coverage.json`（1,034 行分母台账）。不要修改 `reports/` 或 `LEDGER.json`。

## 背景

`scratch/t95/` 已经通过 IDA Pro 9.4 + Hex-Rays x64 在 77 秒内反编译了全部 67 个数据库表类的核心虚函数：
- `slot02_get_prop`（`get_property(this, 4CC, out_val)`）
- `slot03_set_prop`（`set_property(this, 4CC, in_val)`）
- `slot05_reg_prop`（`register_properties`）
- `slot19_read_server` / `slot20_read_client` / `slot21_write`
以及 2-hop 内联/thunk 目标（包括 `NATION` 的 `141045d50.c`、`141063f30.c`、`1410668f0.c` 与 `CLUB` 4,623 行 / `COMP` 4,552 行 / `TEAM_CONTAINER` 1,646 行 / `STADIUM` 877 行等）。初扫已见 **1,897 个唯一 4CC**！

## 任务目标

### 1. 构建稳健的 Hex-Rays 伪代码 4CC 解析器（`scripts/t97_extract_4cc_mem.py`）
遍历 `scratch/t95/vtable_index.json` 中全部 67 张表的 `slot02_get_prop`、`slot03_set_prop` 及其 `hop1_functions`（注意同时追踪 `slot02`/`slot03` 尾调用的基类 `get_prop`/`set_prop`，例如 `CLUB -> TEAM_CONTAINER`、`NATIONAL_TEAM_CONTAINER -> TEAM_CONTAINER`、`NATION -> ...`）：
- 识别所有 4CC 分支：`case <int>:`、`case 0x...:`、`if ( a2 == <int> )` / `a2 == 0x...`（大端 4 字节 ASCII 编码，如 `1869899892 == 0x6F737474 == 'ostt'`）。
- 对每个 4CC 分支体（至下一个 `case`/`break`/`goto`/`return`），自动抽取：
  - `mem_offsets`: 所有 `a1 + <off>` / `*(type *)(a1 + <off>)` / `a1[idx]`（注意根据函数参数 `a1` 的指针类型如 `_DWORD *a1` 乘以 4、`_QWORD *a1` 乘以 8、`__int64 a1` 乘以 1，统一换算成**字节偏移** `0xNN`！）
  - `c_type` 与推断宽度（`1 / 2 / 4 / 8 / string / container / date / subobj`）
  - `bitmask_or_shift`（若存在位域操作如 `& 1`, `>> 2`）
  - `helper_calls`（分支内调用的子函数，排除通用 variant 封装 `sub_14083D4F0`）
  - `access_kind`: `direct_field` | `bitfield` | `subobj_deref` | `helper_computed` | `delegated_or_empty`
  - `source_file`, `func_va`, `line_no`（精确溯源到 C 文件行号，构成严格 L3 证据！）
- **特别核对 `NATION` (`tt=10`)**：检查 `141042940.c`（或 `slot02_get_prop` 解析后的文件）、`141045d50.c`、`141063f30.c`、`1410668f0.c` 是否覆盖了 nation 的全部 getter/setter，若 `slot02`/`slot03` 中还有未在 `scratch/t95/funcs/` 中的直接子调用，单独列出清单 `missing_subcalls`。

### 2. 对 `reports/xml_denominator_coverage.json` 1,034 条分母做全量分诊
把提取出的 `(entity/class, 4CC -> mem_off, access_kind)` 与 `reports/xml_denominator_coverage.json`（club 433 / nation 346 / comp 255）逐条 join：
- 统计此前标为 `unresolved_wire_slot` (160)、`held` (59)、`no_wire_evidence` (564) 的条目中：
  - 有多少在 `CLUB` / `TEAM_CONTAINER` / `NATION` / `NATIONAL_TEAM_CONTAINER` / `COMP` 的 `get_prop`/`set_prop` 中**直接命中了明确 `mem_off`**！
  - 有多少在 `get_prop`/`set_prop` 中命中了 `subobj_deref`（如 extra_3 / extra_9 / subtable）或 `helper_computed`！
  - 有多少在对应类的整套继承链 `get_prop`/`set_prop` 中**完全不存在**（强证据表明是纯 UI / 编辑器派生 / 仅存档字段）！

### 3. 静态 `slot19_read_server` / `slot20_read_client` 内存偏移交叉对照
对每张表的 `slot19_read_server` 和 `slot20_read_client` 伪代码，也抽取其中出现的所有 `a1 + <off>`（按参数指针宽度换算成字节偏移），与 `slot02`/`slot03` 的 `mem_off` 做集合交集，直接生成 **静态初筛 join 表 (`4CC ↔ mem_off ↔ read_server_line`)**！

### 4. 交付物（写入 `OUTDIR`）
1. `fourcc_mem_map.json`：含 `"status": "complete"`，全部 67 张表的 4CC → `mem_off` 映射（带 `func_va` 和 `line_no`）。
2. `xml_triage.json`：1,034 条分母的逐条分诊结果与分桶变化汇总。
3. `static_read_join.json`：全表 `4CC ↔ mem_off ↔ slot19/slot20 行号` 的静态交叉表。
4. `REPORT.md`：核心发现、每张大表命中率、1,034 分母突破统计、`missing_subcalls` 清单。
5. `DONE.md`：含 `DONE type=t97` 与摘要数字。

## 验收标准
- `py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest` 退出 0（须包含对 `STARTING_RECORD` `1415446a0.c` 中 `case 1869899892 ('ostt') -> 0x28`、`case 1918989417 -> 0x5a`、`case 1920099681 -> 0x5c` 的自检断言）。
- 覆盖全部 67 张表，输出 JSON 结构完整且无语法错误。
- 完成后打印交付清单与统计数字。
