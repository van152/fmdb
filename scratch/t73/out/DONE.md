DONE type=t73 status=complete

# t73 — 通用扫表工具 + city/continent/region/currency 四表双档闭环

## 结果

- **8/8 (archive, table) 行框闭合**:city(2) 双档、continent(5) 双档、region(19) 双档、currency(41) 双档。
- **L2 槽位 17 个**,**L3 冻结锚点 14 个复核全过、零冲突**(`frozen_check` city 9/9)。
- **`verify.py` 44/44**(不 import builder),**`t01_anchors.py` 7/7**。
- 四表均无 `escalate_to_sol`;所有 unmapped 字段均有明确"值域不可判定"理由。

## 关键结论

1. **header 原点数据侧永不唯一**:city/continent/region 各 3 个 alias(`13/9` `14/8` `15/7`)全部逐行 identity 成立。定原点的判据是 **F=8 时 footer 前 4 B 读作 BE `1`**,不是算术。
2. **city 双档 payload 逐字节相同**(`66f8cc27…`),双档槽位共用一套结论。
3. **continent server = client 业务字节 + 14 B 全零槽位**(行 `0:21` 逐字节同,`21:35` 全零),行宽 34→48 是发现不是错误。
4. **region server 每行 +1 B**(45→46),该位点常量 `04`(28/28)。
5. **currency 变长文法逐字节闭合**:`4×(u32 len+utf8) + f32 rate + u32 count + count×7B + 13B trailer`,173/173 行 trailer 自证,footer `00000001d6832f05`。
6. **工具能力缺口如实记账**:FK 判据在 t10/t8/t27/t47(均为变长表)上无能力,`Cnti/Clgi/Clri/Cwea` 未由 FK 命中,其偏移来自 L3 冻结锚点。不把 L3 结果回填成 L2。

## 主动放弃的伪通用规则

- `footer_last_eq_max_uid`:`0x333e4 != 0x7`(continent 7 行不成立)。已从主判据集移除,仅作记录。

## 交付

```
scripts/t73_mapper_core.py            方法层
scripts/t73_table_slot_mapper.py      CLI 壳(--table/--archive/--json/--selftest)
scratch/t73/out/frames.json           8 行框 + alias + footer 敏感性
scratch/t73/out/slots_{client,server}_{2,5,19,41}.json   8 份槽位表
scratch/t73/out/verify.py             独立复核 44/44
scratch/t73/out/REPORT.md             完整报告
```

## 边界

L4=0。未启动游戏/编辑器/IDA;未访问 `Z:`;未写 `reports/`、`scratch/t01/LEDGER.json` 或其他任务目录。
