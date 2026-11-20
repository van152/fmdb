# t76c — 批量扫表:derby(18) + weather(27) + local_region(47) + agreement(56)(deepseek)

你是受指挥官委派的子代理。公共资产:`scripts/t73_table_slot_mapper.py`(t73 通用扫表工具,**只读复用,不得修改**)、`scratch/t74/out/frames.json`(t74 行框,**以此为准**)。本任务扫四张表:`derby(18)`、`weather(27)`、`local_region(47)`、`agreement(56)`,双档(agreement 仅 6 行,先拿它冒烟)。

## 必读

- AGENTS.md;`prompts/t73_slot_mapper.md`(工具口径)、`prompts/t74_row_frames9.md`(先验:derby "ordered-name + u32 trailer"×1,567 双档行宽不同;weather ×334 双档同;lcrg **本仓 lcrg_tail 变长文法 41+5k B×2,488,上游 44B 定长已被否证**;agrm 13B×6)
- `scratch/t74/out/frames.json` + `REPORT.md`;`scripts/t73_table_slot_mapper.py`
- `evidence/fm24/reports/editor_schema/master.json`:`entities['derby.xml']` / `entities['weather.xml']` / `entities['local region.xml']`(key 带空格)/ `entities['agreement.xml']` + `enums` + `field_codes`
- 既有锚点:`scripts/fm24_dump.py` FIELDS(client lcrg `rdui@-13/duni@-9`;agrm `rdui@0/duni@4`);derby 实体 = `db::DERBY`(RTTI,t13 的 'city secondary-name' 命名冲突勿混)
- lcrg 的 OVERRIDE 文法(`fm24_dump.walk_lcrg`)可直接 runpy 复用作对照

## 任务

1. **逐表逐档**(8 个 (archive,table),agreement 先冒烟):frames 跑 mapper → 逐槽值域 → schema 对齐 → 分级交付(数据侧=L2/candidate;有仓内静态锚支持的标 L3 并给证据指针)。
2. 重点验证的外键 lane:derby→club/t3 两队对抗(值域应双落 club ordinal 集,wrong-UID 控制同报);weather 数值域(温度/概率类,f32/u8 簇);lcrg→city/t2 或 nation/t10(t01 时代就知道 lcrg 与城市次级名有关,只验引用不命名);agreement→club/nation/comp 稳定标量。
3. 字符串槽不猜:给"字符串区+长度规则"数据侧证据即可,不强配 4CC。
4. frames 缺某表 → 记 `dependency_blocked`,不重开行框;跨对象指针/复杂分发 → `"escalate_to_sol"`。
5. **独立 verify.py**:不 import builder;重抽锚点 + ≥5 槽位对拍(小表全量)。

## 避坑纪律(必须遵守)

1. **防冲突**:只写 `scratch/t76c/` 和 `scripts/t76c_*.py`;**不碰** `reports/`、`scratch/t01/LEDGER.json`、`scratch/t72|t73|t74/`、其他车道目录;不改 `t73_table_slot_mapper.py`。
2. **上交纪律**:两轮内定不出立即 `escalate_to_sol`。
3. 负结果原文保留;候选不写成结论;`0xffffffff` 与合法 0 分列。

## 交付 scratch/t76c/out/

- `slots_client_{18,27,47,56}.json`、`slots_server_{18,27,47,56}.json`、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t76c status=complete`);辅助脚本 `scripts/t76c_*.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=<WORKSPACE>/scratch/data`;完成跑 `scripts/t01_anchors.py`(7/7)。
