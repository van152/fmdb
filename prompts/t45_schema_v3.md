# t45 — club/nation 子表 schema v3(并 t41 Csme 变长 Melf)

你是受指挥官委派的子代理。t42 已交付 schema v2(7 表 51 L3,E81)。t41 Csme 变长 cursor 已接受(E82,Melf 条件 L3 + Msid held)。本任务增量升级 **v3**,并入 Csme。**只增量,不重写已接受字段**。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束;negative 原样保留)
- reports/club_nation_subtable_schema.json + .md(**v2 产物,增量基础**)
- scratch/t42/out/consolidate_v2.py + verify.py + club_nation_subtable_schema.v1.json(v2 builder/verifier/快照,复用扩展)
- scratch/t41/out/fields_csme.json + cursor_csme.json + REPORT.md(**t41 Csme 已接受 E82**)
- scratch/t01/LEDGER.json(E82 t41 接受)

## 任务(增量)
1. **并 t41 Csme**:新增第 8 表 Csme/table_type59/RTTI STARTING_MEDIA_EXPECTATIONS。**Melf 条件 L3**(wire+19+10j,1B,仅 0≤j<n,2512 值 1..33,XML max127,无 0/ff 哨兵;row_offset 按 t41 台账)。**Msid held**(双 lane sink wire+11+10j 静态绑定,6567 行无 entry+2512 entry 全(-1,-1)无 live 引用,首反例 row2@68;held 原因 no_live_media_reference)。全 provenance 从 fields_csme.json 抽(source_task=t41,reader VA 0x141583ba0..0x141583f80)。
2. server payload 224880 SHA 7eee0ecc,count9079,**变长 closure 13+6567×22+2512×32+9=224880**(row_len=22+10n,n=wire+6 u32 count);client 无 table59。**club 独占 L3=0**(9079 owner 全 Team:8941 sel10/138 sel11),记排他注记。
3. coverage 升级:club_tables 8、club_L3_fields **52**、held_fields 16(15+1)、negative_regressions 4 不变、L4=0。schema_version=3。
4. **保留 v2 全部 51 L3 + 15 held + 4 negative + 2 Cstc 非业务槽 verbatim**;存 v2 快照 scratch/t45/out/club_nation_subtable_schema.v2.json;独立校验 v2 七表字段未改。nation 侧仍 0 新 L3。
5. 变长表坐标政策:Csme 字段坐标含 item 下标 j 与 count n 依赖,coordinate_note 须说明条件性(仅 count=1 行有 Melf),不妄断 count=0 行默认值。

## 边界
- 只增量 t41 Csme;不新解析、不跑游戏/编辑器/IDA、不联网、不读写 Z:。
- 候选/held 不升级;negative 原样保留;L4=0。
- 只写 scratch/t45/ 与 reports/club_nation_subtable_schema.{json,md}(v3 in-place,自己产物演进)。

## 交付
- reports/club_nation_subtable_schema.json + .md(v3,8 表 52 L3)
- scratch/t45/out/consolidate_v3.py(--help/--selftest:8 表/52 L3/16 held/4 neg/L4=0、v2 七表 verbatim、Csme 变长 closure)、verify.py(独立不 import builder)、club_nation_subtable_schema.v2.json、REPORT.md、DONE.md
- Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + t01_anchors.py(7/7)。