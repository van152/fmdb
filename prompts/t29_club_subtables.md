# t29 任务书:club 子表数据侧发现 + 画像(239 嵌套字段的广度侦察)

先读 `AGENTS.md`。t24 闭合了 club 主行(10 L3),但 433 schema 中 239 个是嵌套 list 字段,下沉在子表(E39/E40"二级派发+子对象下沉")。sol 正在 t27 攻 stadium 子表(Cstc)的**静态 cursor 模板**。本任务做**互补的广度数据侧侦察**:把其余 club 子表找出来、画像、生成候选列映射,为 t27 方法复制备料。**不做静态 cursor、不晋级 L3**(那是 sol 的活)。

## 已确认基线

- **239 嵌套字段清单**(t24):`scratch/t24/out/subtables.part00{1,2,3}.json` 的 `nested_fields`,按父码分组:Cafl 29 / Cstc 28 / Cvfl 19 / Clhs 12 / CSrs 10 / CAmb 10 / CpTI 9(实际 12)/ Tchl 9 / Calt 6 / Cspb 6 / Coin 6 / Camc 6 / Cmti 6 / Cdbt 5 / Cwcl 5 / …。**Cstc 归 sol t27,本任务跳过 Cstc,专注其余父码。**
- **schema item 语义**(冻结 master.json,SHA 7d57477e 对照 MANIFEST):`evidence/fm24/reports/editor_schema/master.json#entities.club.xml[0].fields`,每个 list 父码的 `list_item_fields` 给出 item 字段名+类型。例:Cafl=[affl,ismc,stdt,endt,type,yfee](联盟,含开始/结束日期+年费);Clhs=[year,orde,divi,posi,mxtm,poin](联赛史,年份/名次/积分);CAmb=[type,levl,styr,enyr,mage,mlen](雄心,起始/结束年)。这些日期/cash/integer/ref 语义是画像的强目标。
- **子表身份来源**:`scratch/t14/out/census.json`(74 表,table_type/handler_off/vtables.class/primary_class/entity_tag/adjudication)+ `reports/stage2_table_identity.json`(54 resolved)+ `scratch/t20/out/cursor_t22.json`(stadium 先例:RTTI STADIUM_CHANGE,factory 0xF49092,slot-19 reader 0x1537800,449×79B)。
- **数据导出**:`scripts/fm24_dump.py`,`FM24_DB_DIR=<WORKSPACE>/scratch/data`;子表多在 **server** archive。t13d 画像先例 `scratch/t13d/out/audit.json`(packed day/year 手法)。

## 唯一目标(数据侧,候选不晋级)

对每个非 Cstc 的 club list 父码:

1. **定子表**:用 RTTI 类名语义匹配(如 Cafl→CLUB_AFFILIATION 类、Clhs→联赛史类)+ t14 census 的 primary_class/entity_tag + stage2 身份 + schema item 的 database_table_type(若有),定出 table_type 与 archive(client/server)。匹配不确定的标 `unknown`,**不要猜**。
2. **画像**:dump 该子表全行,报 count/stride/行封口方程;逐列画像(值域、distinct、哨兵 0xFFFFFFFF 率、packed day/year 日期识别、club ID 域 [0,84259) 落界、cash 样数值、enum 值集)。
3. **候选列映射**:把 item schema 字段(按类型语义)对到候选列(date 列必须落 packed day/year 画像、ref 列落 club ID 域、cash 列落合理金额),生成 **L2 候选**(标 `candidate`,绝不写 L3/已确认);每个候选附全量统计证据。
4. **复制就绪清单**:每父码输出 {parent_4cc, table_type, archive, rtti_class, reader_va(若 t14 有), count, stride, item_field_candidates, confidence, blockers}。

## 纪律

- 只读 `scratch/data/` 与仓内证据 + 只读 editor.exe(若需 VA 对照,PE 用 `scripts/t05_pe.py`);只写 `scratch/t29/out/` 与 `scripts/t29_*.py`;不覆盖 t24/t20/t27 产物。
- **候选不写成结论**;无独立证据的列名不赋义;负结果保留;匹配不到的父码如实标 unknown。
- 每父码独立落盘,**卡壳就写 partial 再做下一个**(devseek 式纪律);20+ 父码做不完就交已完成的,顶层 status 汇总。
- 新脚本 `--help`/`--selftest`,退出码 0/1/2;单次打印 ≤400 行;大 JSON 分片;状态词 `complete_*`/`partial_*`/`negative_*`。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:。

## 交付

1. `scratch/t29/out/subtable_inventory.json`:每父码的发现+画像+候选+confidence+blockers(可分片)。
2. `scratch/t29/out/profiles/`:各子表逐列画像机读结果。
3. `scratch/t29/out/REPORT.md`:已定子表数/候选字段数/unknown 清单/与 t27 的衔接说明。
4. `scratch/t29/out/verify.py`:独立复算行封口 + 候选列统计抽样。

完成后跑自己的 verify 与 `py -V:3.12 -I scripts/t01_anchors.py`(7/7)。打印交付清单:每个父码拿到什么、卡在哪。