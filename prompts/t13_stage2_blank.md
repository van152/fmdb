# t13 任务书：阶段二主攻 —— 10 张空白表的表号→实体锚点

## 一句话目标

给 10 张至今 `entity=None / tier=unknown` 的 archive 表，每张找到**至少 1 个独立锚点**，把 `table_type → entity` 定下来。找不到就交负结果并写清为什么，不许硬凑。

## 背景与精确缺口

阶段二验收线（AGENTS.md）：**50 张 unknown 数值表的表号→实体映射，每张至少 1 个独立锚点**。

已有工件 `scratch/t01/stage2_three_way.json`（E22）定了 21 个表型，把 unknown 从 50 降到 38。这 38 个里：

| 分类 | 数量 | 表号 | 本次是否要管 |
|---|---:|---|---|
| 不在 archive（工厂专属/null-return，E24 已解释）| 14 | 4,11,13,14,15,16,17,20,28,40,44,53,54,55 | **不管**，保留原文 |
| 在 archive、已由 t05–t12 给出布局与命名候选 | 12 | 22,30,31,34,37,42,43,46,49,50,51,58 | **不管**，指挥官自己裁决 |
| **在 archive、完全空白** | **12** | **12,26,29,32,33,36,38,39,45,48,52,57** | **本次任务** |

其中 **t52 与 t57 的 `count=0` 是空表**（`scratch/t05/COVERAGE.json` 已确认），直接按"空表、无锚点可找"结案即可，写进报告不算失败。

**真正要攻的是这 10 张：**

| table_type | archive | count | mode | boundary |
|---:|---|---:|---|---|
| 12 | server | 28,597 | straight-line | closed |
| 26 | server | 90,128 | straight-line | closed |
| 29 | server | 13,278 | straight-line | closed |
| 32 | server | 315 | count-loop | closed |
| 33 | server | 32,409 | straight-line | closed |
| 36 | server | 6,535 | count-loop | closed |
| 38 | server | 5,241 | straight-line | closed |
| 39 | server | 117 | mixed | closed |
| 45 | server | 84,477 | straight-line | closed |
| 48 | server | 5,210 | straight-line | closed |

行数和封口等式都已闭合（`scratch/t05/COVERAGE.json`），**不要重做行边界**，直接拿列数据找语义。

## 什么算"独立锚点"（关键，别自欺）

锚点必须是**能单独把表号指向某个实体**的事实，而且要说明它为什么不依赖其他推理链。三类可用：

**A. exe 静态锚（L3）**：该表的 reader/dispatch 链里出现一个 4CC 码，该码在 `schema_inventory.json` 里**只属于一个实体**（跨实体出现次数 `df=1`），且该实体的名字与码语义自洽。
- 工具：`scripts/t05_reader_widths.py`（reader→槽）、`scratch/t12/out/codes_full.json`（4,278 条码实例，含 shape/object_off/instruction）、`scratch/t08/out/chains.json`（226 条链）。
- 反例（不算锚点）：`levl/venu/perc` 这类跨表同名码；`duni/rdui/NDBC/FDBC/dbnm` 五个通用码。

**B. 独立事实锚（L2）**：行数与已知实体基数吻合，且该基数来自**与本表无关的来源**。已知基数示例（来自 E22/E30/E42 等）：nation 251、weather 334、language 126、city 56,293、stadium 48,413、injury 115、lcrg 2,488、comp 7,047。
- 用法：比如 count=5,241 接近 language? 不吻合；要找真正吻合的，并且给出基数来源文件。
- **注意**：单纯"行数差不多"不算锚点，必须同时给出该实体基数的独立出处与差值百分比。

**C. 值域锚（L2）**：某一列的取值集合落在一个已知实体的 ID 空间内，且哨兵比例、fill 率同时吻合。
- 工具：`scripts/fm24_dump.py --archive server --table N --csv ...`、`scripts/t05_ref_match.py`（值域→表候选）。
- 反例（E42 已证）：fill 越接近 1 越偏向小表，值域法单独不能定案；必须有语义来源配合。

**硬要求**：每张表至少给出 1 个 A/B/C 类锚点；如果只有 C 类，必须写明"仅 C 类，不足以定案"，标 `candidate` 而不是 `resolved`。

## 已知陷阱（都会让你白干）

1. **归属投票会被污染**：t11 算 t47 的原始票数是 `injury 6 : local region 1`，因为被污染的链里塞了 6 个 injury 专有码。最后是靠 `Lpop` 这个独立锚点翻案的。**投票只能排序，不能裁决。**
2. **共享类不是同一张表**：t19 与 t22 共享 `Scap/Sscp/Sceb` 且偏移相同，因为它们序列化同一个类；不能据此说两表是同一实体。
3. **空列不代表字段不存在**：t23 的 row+0 在 278 行里全 0，曾被误命名为 `SNsn`，已撤回。
4. **不要重做行边界**、不要改 `scripts/`、`scratch/t05`~`t12`、`reports/`；只读调用。

## 交付（写到 `scratch/t13/out/`）

1. `anchors.json` —— 10 张表 + 2 张空表，每表一条：
```json
{"table_type":12, "archive":"server", "count":28597,
 "status":"resolved|candidate|negative|empty",
 "entity":"<schema entity tag or null>",
 "anchors":[{"kind":"A|B|C", "claim":"一句话", "evidence":{"file_off":"0x...","instruction":"...","value_range":"...","source_file":"..."}, "independence":"为什么它不依赖别的推理链"}],
 "rejected":[{"entity":"...", "why":"..."}],
 "why_unresolved":"仅 negative/candidate 时必填"}
```
顶层带 `"status"`。
2. `verify.py` —— 可复跑，检查：
   - 12 张表全覆盖（含 2 张空表）；
   - 每个 `resolved` 至少有 1 个 A 或 B 类锚点（只有 C 不算）；
   - 每个锚点的 `evidence` 非空且能被独立复核（给出 file_off 的必须能在 exe 该地址反汇编出声明指令）；
   - 不出现通用码 `duni/rdui/NDBC/FDBC/dbnm` 作为 A 类锚点。
3. `REPORT.md` —— 逐表结论表 + 负结果原文 + 哪些表还缺什么。

## 验收线

1. 10 张非空表逐张给出 `resolved / candidate / negative`，**不许留空**。
2. 至少 **4 张**拿到 A 或 B 类锚点（`resolved`）。
3. 每个 `resolved` 的锚点能被 `verify.py` 从原始工件复算。
4. 2 张空表明确标 `empty` 并附 `count=0` 出处。
5. 负结果保留原文，不许删改。

## 纪律

- `py -V:3.12 -I`；脚本须有 `--help` 与 `--selftest`；退出码 0/1/2。
- **只读**：`scripts/`、`scratch/t05`~`t12`、`reports/`、`docs/`、`evidence/` 一律不许改；只写 `scratch/t13/out/`。
- 不许联网、不许启动游戏/编辑器/IDA。
- **先落盘骨架**（`"status":"in_progress"`），完成时 `"status":"complete_<限定词>"`。
- 拿不到就报负结果，**禁止把候选硬写成结论**。
