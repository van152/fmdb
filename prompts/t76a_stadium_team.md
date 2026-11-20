# t76a — 批量扫表:stadium(21) + team(24)(deepseek)

你是受指挥官委派的子代理。第 1 波已交付两个公共资产:`scripts/t73_table_slot_mapper.py`(t73 通用扫表工具,**只读复用,不得修改**)和 `scratch/t74/out/frames.json`(t74 九表行框,**行框以此为准**)。本任务扫两张表:`stadium(21)` client+server、`team(24)` server-only(client 无 entry)。

## 必读

- AGENTS.md;`prompts/t73_slot_mapper.md`(工具口径:分级/锚点回归/escalate 规则)、`prompts/t74_row_frames9.md`(行框先验表)
- `scratch/t74/out/frames.json` + `REPORT.md`;`scripts/t73_table_slot_mapper.py`(`--table --archive --json`,可 runpy 调函数,不得改)
- `evidence/fm24/reports/editor_schema/master.json`:`entities['stadium.xml']` / `entities['team.xml']` 字段清单 + `enums` + `field_codes`
- 既有锚点:`scripts/fm24_dump.py` FIELDS(client stadium `Scti@3/Slat@17/Slon@21/rdui@25/duni@29`)——结论不得冲突;`scratch/t66/out/REPORT.md`(t24 ordinal→UID 84,507;`table_extra_24.dat` 只取 ordinal,不入本任务)
- t21 目标基数 48,413(t59 已验)

## 任务

1. **stadium(21) 双档**:frames 跑 mapper → 逐槽值域(u8..f32)→ 按 stadium.xml 字段清单对齐(类型宽度 × 值域 × 外键命中;stadium→city/t2 的引用 lane 重点验证,wrong-UID 控制同报)→ 分级交付(数据侧=L2/candidate;可引用仓内已冻结静态锚的个别字段标 L3 并给证据指针)。
2. **team(24) server**:若 t74 frames 已闭合 → 同流程;若 t74 标了 `escalate_to_sol` 或缺 frame → 记 `dependency_blocked`(one-line reason),不自己重开行框攻坚(那是 sol 的活),把算力给 stadium。
3. team.xml 字段量大(俱乐部运营侧),对齐时优先:identity 三件套之外的稳定标量簇;字符串槽不猜(t59 cnam/csnm 口径);外键 lane 候选对 t2/t3/t5/t10/t21/t23/t25 逐一验。
4. 每表交付 `slots_{archive}_{table}.json`;跨对象指针/复杂分发 → `"escalate_to_sol"`。
5. **独立 verify.py**:不 import builder;重抽锚点 + ≥5 槽位对拍。

## 避坑纪律(必须遵守)

1. **防冲突**:只写 `scratch/t76a/` 和 `scripts/t76a_*.py`;**不碰** `reports/`、`scratch/t01/LEDGER.json`、`scratch/t72|t73|t74/`、其他车道目录;不改 `t73_table_slot_mapper.py`。
2. **上交纪律**:文法/分发两轮内定不出立即 `escalate_to_sol`,不硬猜。
3. 负结果原文保留;候选不写成结论;`0xffffffff` 与合法 0 分列;不用值域相似配槽。

## 交付 scratch/t76a/out/

- `slots_client_21.json`、`slots_server_21.json`、`slots_server_24.json`(或 dependency_blocked)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t76a status=complete`);辅助脚本 `scripts/t76a_*.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=<WORKSPACE>/scratch/data`;完成跑 `scripts/t01_anchors.py`(7/7)。
