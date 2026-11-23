# Wave 13 — 工具化突破总波次战报

> **结论**：核心资产已汇总并附 SHA-256；但不将不同产物口径混为“全通过”。t96c 的落盘 DONE 标为 `partial`（closed=41），与任务简报的 42 张存在冲突，待审阅原始统计。

## Before / After

| 指标 | Before（v11.3 / E140） | After（Wave 13） | 说明 |
|---|---:|---:|---|
| 已透表数 | 6/74 | 55/67 joined（跨任务材料另称 55+/74） | 分母不同，不能直接视为同一统计；t110 实际产物给 55/67。 |
| 三大主表总分母覆盖 | 110/1,034 = 10.6% | 379/1,034 = 36.7% | t109 coverage_summary。 |
| 三大主表净覆盖 | 未设此口径 | 379/673 = 56.3% | 排除 361 项非 DB 相关字段后的口径。 |
| Unicorn 字节闭合表 | 0 | t96c DONE: 41 closed；任务简报称 42 整表 + 32 大表 / 74/79 | 任务简报与实际 DONE 不一致；按需复核 trace JSON。 |
| table_9 变长行 | 未闭合 | 声称 211 种长度闭合 | 附 `table9_251_closure.json`，以实测数据及回归为准。 |
| basic_people | 已有行链/弱语义 | 658,011 行 framing diff=0；3 anchors | framing 闭合不等于全字段语义闭合；PDxx 不在范围。 |

## 突破与限制

- IDA/Hex-Rays 函数索引、4CC→内存偏移分析、序列化器控制流与 Unicorn×IDA 表映射形成可追溯工具链。
- t109 汇总 379 个 L3 occurrence（毛覆盖 36.7%、净覆盖 56.3%）；t110 报告 55 张表、1,056 条 L3 映射，但回归摘要有 mismatch 项。
- t96c 数据 DONE 仍为 partial（41 closed / 27 sample_ok / 11 failed），不应将任务 brief 的更高数字当作已复核结论。
- t113/t115 people 车道完成基础行框与访问器盘点；PDxx 属性块未纳入本任务。

## v11.3 未决项 #1–#5

| # | 状态 | Wave 13 后续 |
|---|---|---|
| 1 EDfx 上游持久化来源 | 未解决 | 仍需闭合持久化源链。 |
| 2 三主表未映射主行字段 | 部分推进 | gross 379/1,034；剩余项继续按分母分类推进。 |
| 3 award/language/media 槽位 | 未解决 / in-flight | 对应兄弟车道无 DONE 时不报完成。 |
| 4 comp 集合业务语义 | 未解决 | 物理文法与引用 lane 不等于业务语义绑定。 |
| 5 held 枚举域批量补 | 未解决 | 需 scoped enum_ref 专项。 |

## 回归体检

本机运行 7 项，退出码 0：7 项。详见机读文件 `wave13_consolidated.json` 的 `regression_matrix`（完整输出保留）。

## 审阅候选与下一步

`ledger_candidates.json` 含 E142–E150 **草稿**，均需指挥官审阅后再决定是否入账；t116 未写入 `scratch/t01/LEDGER.json`。优先行动：核对 t96c 统计口径；审查 t110 mismatches；之后推进 EDfx、剩余字段/枚举、t83 槽位与 comp 集合语义。

## 产物入口

- [汇总 JSON](wave13_consolidated.json)
- [E142–E150 候选台账](ledger_candidates.json)
- [独立校验器](verify_wave13.py)
- [DONE](DONE.md)
