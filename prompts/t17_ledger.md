# t17 任务书:tier-1 字段台账 + 全量回归

先读 [AGENTS.md](../AGENTS.md)。

## 前置条件

`scratch/t14/out/stage2_map.json` 与 `scratch/t16/out/ledger.json` 必须已存在且 status 是 complete_。任一缺失 → 落盘 `"status":"blocked_waiting_<NN>"` 收工。

## 一句话目标

把 t14(表→实体)与 t16(类→字段)产物合流成**阶段三 tier-1 台账**(club/nation/comp),并把全部历史锚点跑成回归,输出"编辑问题可支撑度"评估。

## 任务

1. **合流台账**:对 club(433 字段)/ nation(346)/ comp(7,047 行)三实体,逐字段输出:
   `{"field":"CMWE","entity":"club","row_offset":68,"width":4,"grade":"L3","evidence":{"inst_off":"0x...","source":"t16 fields_club.json"},"named_by":"t12|t16|both","caveats":[]}`
   - 只收 L1-L3;候选证据标 `grade:"cand"` 单列一节,**不许混进正式台账**。
2. **全量回归**(一项都别漏,失败必须原文保留):
   - 六大洲 0..5(L2)、England=139 / China PR=55(comp 锚)、parent row 352;
   - city 56,293 / nation 251 / weather 334 / language 126 / lcrg 2,488 / injury 115 / club 84,259 / comp 7,047 / award 3,545 / stgn 278 / team 84,507 / derby 1,567 基数回归(数据源 `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`,已设);
   - E51 city 坐标 100% 复现;E27 weather 334 行封口(payload 43,345B,行跨度=112+name_len);
   - t13 的 4 个 A 锚(12→award AHp1、33→club CMWE、45/48→person gols)指令复算;
   - t14 的 8 个 RTTI 交叉实体(0/2/8/18/19/23/27/56)。
3. **可支撑度评估**:按"能支撑什么编辑问题"给 tier-1 打分,例如 `club: 名称✓(L3) 工资上限✓(L3) 转移预算✗(未命名)`;诚实标注,不吹覆盖率。

## 纪律

- 只写 `scratch/t17/out/`;其他全只读;py -V:3.12 -I;脚本须 --help/--selftest,退出码 0/1/2。
- 回归任何一项失败:**保留原文 + 标出**,不许为了绿灯改数字。台账进 reports/ 由司令官晨裁,你不写 reports/。

## 交付(scratch/t17/out/)

1. `ledger_club.json` / `ledger_nation.json` / `ledger_comp.json`
2. `regression.json` —— 每项 pass/fail + 实测值;顶层 status。
3. `REPORT.md` —— 可支撑度评估 + 失败项原文。

## 验收线

1. 回归全过(有 fail 就如实写,不许藏)。
2. club/nation 台账覆盖 t16 已命名的全部字段 + 未命名清单。
3. 三个台账逐字段可追溯到证据文件。
