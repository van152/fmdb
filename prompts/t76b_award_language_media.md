# t76b — 批量扫表:award(0) + language(8) + media(7)(deepseek)

你是受指挥官委派的子代理。公共资产:`scripts/t73_table_slot_mapper.py`(t73 通用扫表工具,**只读复用,不得修改**)、`scratch/t74/out/frames.json`(t74 行框,**以此为准**)。本任务扫三张小表:`award(0)`、`language(8)`、`media(7)`,双档。

## 必读

- AGENTS.md;`prompts/t73_slot_mapper.md`(工具口径)、`prompts/t74_row_frames9.md`(先验表:award 77B×3,545 双档同 payload;language 126 行"ordered name + 30B suffix";media 208 行"ordered-name + u32 trailer",client/server 行宽不同)
- `scratch/t74/out/frames.json` + `REPORT.md`;`scripts/t73_table_slot_mapper.py`
- `evidence/fm24/reports/editor_schema/master.json`:`entities['award.xml']` / `entities['language.xml']` / `entities['media source.xml']`(注意 entity key 是 'media source.xml' 不是 'media.xml')+ `enums` + `field_codes`
- 既有锚点:`scripts/fm24_dump.py` FIELDS(client award `rdui@64/duni@68`;language `rdui_suffix@17`;media `rdui@3/duni@7`);t12 是 award 样 28,597 行的另一张表,**不在范围**,勿混
- 语言表特殊性:language 126 行≈语言清单,行内主体是名字字符串,rdui_suffix@17 说明 identity 是"suffix"形态——以 t74 自证结论为准

## 任务

1. **逐表逐档**(6 个 (archive,table)):frames 跑 mapper → 逐槽值域 → schema 对齐(award.xml 字段多为 enum/text;`AHp1` 等 award 专属码在 t13 静态锚里有 object_off=128 的先例,可引用 t13 锚点但注明其边界)→ 分级交付(数据侧=L2/candidate;有仓内静态锚支持的字段标 L3)。
2. 字符串槽不猜:award/language/media 的 name 类字段给"字符串区起始+编码+长度规则"的数据侧证据(UTF-8/UTF-16、长度前缀),但不强配到具体 4CC,除非 master.json type+长度分布都吻合。
3. media/derby 类的 trailer u32 序列若 t74 已定结构,mapper 直接复用;若 frames 缺 → 记 `dependency_blocked`,不重开行框。
4. 每表交付 `slots_{archive}_{table}.json`;跨对象指针/复杂分发 → `"escalate_to_sol"`。
5. **独立 verify.py**:不 import builder;重抽锚点 + ≥5 槽位对拍。

## 避坑纪律(必须遵守)

1. **防冲突**:只写 `scratch/t76b/` 和 `scripts/t76b_*.py`;**不碰** `reports/`、`scratch/t01/LEDGER.json`、`scratch/t72|t73|t74/`、其他车道目录;不改 `t73_table_slot_mapper.py`。
2. **上交纪律**:两轮内定不出立即 `escalate_to_sol`。
3. 负结果原文保留;候选不写成结论;`0xffffffff` 与合法 0 分列。

## 交付 scratch/t76b/out/

- `slots_client_{0,8,7}.json`、`slots_server_{0,8,7}.json`、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t76b status=complete`);辅助脚本 `scripts/t76b_*.py`。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=<WORKSPACE>/scratch/data`;完成跑 `scripts/t01_anchors.py`(7/7)。
