# t16b 任务书:命名桥重校准 + 全实体台账(承接 t16 现场)

先读 [AGENTS.md](../AGENTS.md)。t16 引擎已跑通 walk 但黄金门(强求引擎全新命名)没过——门定义错了,不是引擎错了。你来重校准并把台账真正交出来。

## 现场只读清单

- `scratch/t16/out/`:`entity_trace_{city,club,comp,nati}.json`、`debug_fields_*.json`、`fields_*.json`(5 实体)、`golden_results.json`、`ledger.json`(partial_golden_gate_failed)、`scripts/t16_serializer_walk.py`(你自己的引擎,只许新增 t16b_ 前缀文件,不许改它——要复用就 import)
- 命名桥证据源:
  - `scratch/t12/out/codes_full.json` —— 4,278 条 4CC 实例,**含 object_off**(t13 A 锚就是靠它:CMWE@68↔[rbx+0x44])
  - `scratch/t08/out/chains.json` —— 226 条链
  - `reports/t12_field_names.json` —— 132/240 已命名槽(E55 口径)
  - `scratch/t01/inbox/t01l/output.json` —— E27 weather 89 字段基线(t16 没找到它,路径在这)
  - `scratch/t01/inbox/t01f/output.json` —— E20 comp 18 行偏移基线
  - `scratch/t05/schema_inventory.json` + `scratch/t05/reader_widths.json`
- `scratch/t14/out/stage2_map.json` —— 表→实体全图(54/59 resolved)
- `scratch/t15/out/fk.json` —— t30/t38/t49 的 C 类佐证

## 黄金门(重校准版——门要能过,但不能白给)

**G1 传承一致性**:引擎 walk 出的 (offset,width) 序列,与 E27 weather 基线 89 字段、E20 comp 18 字段、E55 已命名槽**逐一比对**,一致率 ≥95% 即过(冲突列清单,不许静默覆盖)。
**G2 命名桥规则**:walked offset ↔ codes_full.json 的 object_off 实例 ↔ 4CC ↔ schema entity 字段——三段式桥,每接通一个字段记 `grade:"L3_instruction"`;接不通但 E55/E20/E27 有名的记 `grade:"L3_inherited"`;两者皆无记 `unnamed`。**unnamed 是合法台账行,不是失败。**
**G3 数据侧交叉**:t30/t38/t49 的 C 类佐证作为对应字段行的 `grade:"L2_data"` 旁证写入。

## 任务

1. 按新门复跑/扩展现有 walk(未跑的实体:team/stad/inju/regi/stgn/awar/agrm/drbr/curr/mdso/cont/lcrg/nati 家族等,以 stage2_map 的 54 个 resolved 实体 tag 去重为准),优先 tier-1:club → nation → comp → team。
2. 每实体一个 `fields_<tag>.json`:逐字段 `{"field","offset","width","grade","evidence","source"}`;`ledger.json` 汇总覆盖率;`status` 完成时 `complete_ledger_partial_coverage_<限定词>`。
3. `verify.py`:G1 传承比对 + 抽样字段指令复算,--help/--selftest。
4. club 是 mixed 实体,t04 只闭合过 1 字段——若 walk 拿到它的序列化分支结构,如实报分支数;拿不到就写清楚卡在哪。

## 纪律

- 只写 `scratch/t16b/out/` + 新增 `scripts/t16b_*.py`;其他全只读;不联网。
- 输出预算:单次写盘 ≤400 行;fields_<tag> 超 50KB 分片。
- 45 分钟做不完就分批落盘 partial——**宁可 partial 台账,不许硬凑命名**。

## 交付(scratch/t16b/out/)

`fields_<tag>.json` × N、`ledger.json`、`ledger.md`、`verify.py`、`REPORT.md`(方法、G1 结果、冲突清单、未闭合项)
