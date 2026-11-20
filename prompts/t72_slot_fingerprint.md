# t72 — club/nation/comp 未命名物理槽位清单 + 值域指纹(数据侧,deepseek)

你是受指挥官委派的子代理。第 2 波的 sol 任务(t75)要做"槽位 → 成员偏移 → xref 反查",需要你先铺路:**把三张主表所有还没被 L3 字段认领的物理槽位列出来,并给每个槽位做数据侧值域指纹**。纯数据侧任务,不做任何 exe 静态断言。

## 必读

- AGENTS.md;`scratch/t57/out/field_slots.json`(club 34 槽,含 envelopes/execution_templates/domain_profiles)、`scratch/t59/out/field_slots.json`(comp 82 槽)、`scratch/t55/out/field_slots.json`(nation 40 槽,已带 domain_profiles)
- `reports/club_nation_subtable_schema.json` v10:`club_main_row_fields` / `comp_main_row_fields` / `nation_main_row_fields`(L3 认领清单)+ `club_main_row_fields_r2` / `comp_main_row_fields_r2` / `nation_main_row_fields_r2`(held/unmapped 归因)
- `scratch/t63/out/field_map_r2.json`、`scratch/t64/out/field_map_r2.json`、`scratch/t65/out/field_map_r2.json`(每 occurrence 的 grade)
- `scratch/t66/out/collections.json` + `collections` 文法(comp 集合层已 L3 的 7 文法/4 lane——**这些槽位跳过**,标 `already_closed_by=t66`)
- 证据分级口径(AGENTS.md 硬约束 2)

## 任务

1. **槽位清单**:三表 × 双档,枚举 field_slots 全部物理槽位,按 schema v10 + r2 field_map 归类:
   - `kind=l3_claimed`(被 L3 字段认领,只列不下场)
   - `kind=held`(named 但 grade=held)
   - `kind=unnamed`(无 schema 认领)——本任务主角
   - `kind=collection_closed`(t66 已闭集合,跳过)
2. **逐槽指纹**(unnamed + held 两类都要,双档各自算):
   - 原始字节与宽度候选(u8/i8/u16/i16/u32/i32/f32 各自的 min/max,存在多种解释时全列,不裁决符号性)
   - cardinality(不同值个数)、all_zero 标记、全一(`0xffffffff`)占比(与合法 0 分列)、首/末行样例
   - **外键命中**:非哨兵值落入目标表 live ordinal 集的占比,目标集:t2 city 56,293 / t3 club 84,259 / t5 continent 7 / t10 nation 251 / t21 stadium 48,413 / t23 stgn 278 / t24 team 84,507(仅 server)/ t25 comp 7,047;**同时给 wrong-UID 控制例**(把值当 UID 查的命中率,t66 纪律——ordinal 命中≠UID 命中,两者都报,不下结论)
3. **行重放**:用 field_slots 的 envelopes/execution_templates 重放冻结轨迹(不许从 raw 字节盲扫);每档先核 identity triple(逐行 ordinal/UID)与 t57/t59/t55 冻结值一致才继续;重放失败 ≥2 种办法仍不通 → 该表标 `escalate_to_sol` 保留已完成的另一档。
4. 每槽给 `xref_hint`(可选):把"该槽位值域形态"(小枚举子集/宽值域/全零/疑似指针)写一句话,**只描述数据形态,不做语义命名**。

## 避坑纪律(必须遵守)

1. **防冲突**:只写 `scratch/t72/` 和 `scripts/t72_*.py`;**不碰** `reports/`、`scratch/t01/LEDGER.json`、其他任务目录;不修改任何既有脚本(只读引用)。
2. **上交纪律**:碰到复杂变长循环(尤其 nation A_B_C_D 段内文法)、跨对象指针链、跳表分发——立即在输出 JSON 里标 `"escalate_to_sol": {"item": ..., "what_tried": ..., "blocker": ...}` 跳过,同一问题不硬猜超过 2 轮。
3. 负结果原文保留,不得删除或改写;候选不写成结论;数据侧证据最高只到 L2/candidate。

## 交付 scratch/t72/out/

- `inventory.json`(三表全部槽位分类清单)、`fingerprints.json`(unnamed+held 逐槽指纹,双档)、`verify.py`(独立复算抽样槽 + 重放一致性)、`REPORT.md`、`DONE.md`(首行 `DONE type=t72 status=complete`);builder `scripts/t72_slot_fingerprint.py`(支持 `--help`/`--selftest`,退出码 0/1/2)。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=<WORKSPACE>/scratch/data`。归档成员用 `scripts/fm24_dump.py` 的 `load_payload` 模式(可 runpy 复用,不得修改);大表向量化,别逐行 python 循环 84k×34 慢扫。
