# t35 — Cafl/Cvfl 俱乐部附属关系子表数据侧发现(luna 广度侦察)

先读 D:\tmp2b\fm24-db\AGENTS.md。你是受指挥官委派的子代理。club 子表静态 cursor 由 sol 复制(t27/t30/t31/t32 已闭 Cstc/Clhs/CSrs/Cmti,37 L3);t29b inventory 把 Cafl/Cvfl 标 unknown。本任务做**数据侧发现+画像**,为 sol 后续静态闭合备料。**不做静态 cursor、不晋级 L3**。

## 核心假说(待证据验证,不预设结论)
Cafl(29 字段)与 Cvfl(19 字段)**共享大量 item 字段**:affl/ismc/stdt/type/yfee/fri%/frly/golo/fotb/plfr/smbo/fnhl/perm/yutr/hlwf/mrrl/scks/cpsd。Cvfl 近似 Cafl 子集,但多 `clfr`(Validated? enum)、少 `endt` 及 Cafl 后段字段(msls/yout/rsrv/pfpr/pwgp/bttr/ualf/lpfs/ustf/UsSK)。t27 replication.md 静态线索:Cafl compare `0xe8b4db`→`0xe8f13d`→thunk `0x141532ab0`(R8D=0,取 club +0x118/+0x120);Cvfl compare `0xe8c1e8` 后比较 club 相同偏移,`0xe8c217` 调 `0x141532c60`(R8B=1)。**假说:同一 club-owned affiliation 集合的两个视图(R8 flag 0/1 选视图),而非两个独立表。** 用数据验证或反驳,保留反例。

## 必读
- D:\tmp2b\fm24-db\scratch\t27\out\replication.md(§3 Cafl/Cvfl 优先切口)
- D:\tmp2b\fm24-db\scratch\t29\out\subtable_inventory.json(Cafl/Cvfl unknown 页)+ profiles/ 已有 13 表
- D:\tmp2b\fm24-db\scratch\t14\out\census.json(74 表 table_type/handler_off/vtables.class/primary_class/entity_tag)+ reports/stage2_table_identity.json(54 resolved)
- D:\tmp2b\fm24-db\scratch\t24\out\subtables.part00*.json(Cafl idx370–398 / Cvfl idx400–418 完整 item 字段)
- evidence/fm24/reports/editor_schema/master.json(club.xml,冻结 SHA 7d57477e 对照 MANIFEST)
- scripts/fm24_dump.py(FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data);多帧成员注意 E66 caveat(load_payload 取首帧,空 stub 时取真实第二帧)

## 任务(数据侧)
1. **定候选表**:在 t14 census + stage2 identity 中按 RTTI 语义搜 CLUB_AFFILIATION / AFFILIATE / CLUB_LINK 类名(及近义),列出所有候选 table_type+archive+RTTI+primary_class+entity_tag。匹配不确定标 unknown,**不猜**。
2. **画像候选**:dump 候选表全行(多帧感知),报 count/stride/行封口方程;逐列画像——stdt/endt 落 packed day/year(两 u16=day,year 或 high16 year/low9 day-of-year,year 1850–2100/day 1–366);yfee cash 样金额;affl club ref 落 club ID 域 [0,84259) 或成对 record-key i32(参 t32 E69 模型,第二 lane 零则复制);type/clfr enum 值集;~20 个 bool 是否共享 bitmask 字节(逐 bit 统计)。
3. **视图假说检验**:若找到一个表,检验其行能否同时容纳 Cafl 29 字段与 Cvfl 19 字段(Cvfl 子集兼容?clfr 列存在?endt 列存在?);若找到两个表,比较 stride/字段覆盖/affl 域是否重叠。报告支持"一集合两视图"还是"两独立表"的**数据证据与反例**,不下静态结论。
4. **复制就绪清单**:输出 {parent_4cc, candidate_table_type, archive, rtti_class, count, stride, item_field_candidates(L2 candidate), view_hypothesis_evidence, confidence, blockers}。

## 纪律
- 只读 scratch/data/ + 仓内证据 + 只读 editor.exe(若需 VA 对照用 scripts/t05_pe.py);只写 scratch/t35/out/ 与 scripts/t35_*.py;不覆盖 t24/t27/t29 产物。
- 候选不写结论;无独立证据不赋列名;负结果/反例保留;匹配不到如实 unknown。
- 卡壳写 partial 再做下一个;新脚本 --help/--selftest,退出码 0/1/2;单次打印 ≤400 行;大 JSON 分片;状态词 complete_*/partial_*/negative_*。
- 不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。

## 交付 scratch/t35/out/
- cafl_cvfl_discovery.json(候选表+画像+视图假说证据+confidence+blockers,可分片)
- profiles/(候选表逐列画像机读)
- REPORT.md(候选表数/视图假说结论倾向/unknown 清单/与 sol 静态衔接)
- verify.py(独立复算行封口+候选列统计抽样;ROOT 用 Path(__file__).resolve().parents[2] 指向 fm24-db,**勿犯 t29b parents[3] bug**)
- DONE.md

Python `py -V:3.12 -I -B`;完成跑自己的 verify + t01_anchors.py(7/7)。打印交付清单。