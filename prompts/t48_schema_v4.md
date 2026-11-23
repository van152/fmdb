# t48 — club/nation 子表 schema v4(并 t44 Cafl/Cvfl 共享 CLUB_LINK 辅助源)

你是受指挥官委派的子代理。t45 已交付 schema v3(8 表 52 L3,E83)。t44 Cafl/Cvfl 静态发现已接受(E84:**共用具名辅助 POD 成员 `club_links.dat`**,Cafl 26/29 L3、Cvfl 16/19 L3)。本任务增量升级 **v4**,并入 Cafl/Cvfl。**只增量,不重写已接受字段**。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;negative 原样保留)
- reports/club_nation_subtable_schema.json + .md(**v3 产物,增量基础**)
- scratch/t45/out/consolidate_v3.py + verify.py + club_nation_subtable_schema.v2.json(v3 builder/verifier/快照,复用扩展)
- scratch/t44/out/fields_cafl_cvfl.json + cursor_club_links.json + discovery_cafl_cvfl.json + REPORT.md(**t44 已接受 E84**)
- scratch/t46/out/REPORT.md + grammar_diff_client_server.json(**t46 nation server table_10 数据侧 L1/L2 已接受 E85**,grammar open)
- scratch/t37/out/nation_subtable_inventory.json(nation 25 unknown partial,0 独占 L3)
- scratch/t01/LEDGER.json(E84 t44 / E85 t46)

## t44 关键事实(并入依据)
- **共享源**:Cafl/Cvfl 两视图读同一 `CLUB_LINK*` 集合,磁盘=`server_db/club_links.dat`(**具名辅助成员,无数字 table_type/entry RTTI/vptr/slot19/factory case**)。client 无成员。
- **POD cursor**:47B 行,`12 + 9261×47 + 0 = 435279`(8B header `03017461642ef10d` + u32 count@8;**无 per-row selector/identity tail/vector footer**;标准 legacy14/wire13 不适用)。payload SHA `8933328064...`,row-block `17a167f0...`。版本 word VA `0x141b60330` 门槛 `0x0dd6`(本档头 0x0df1→现代 47B;旧 43B 反例)。
- **affl**:双 i32 端点 wire+0/+9→对象+0/+8,**L3 派生**(当前 club==A 取 B 否则取 A);各 9261/9261 命中 club/t3 实际 84259 ordinal 域(row0 A=1270→UID1688,B=11272→UID4212156;UID 否证 row misses A5751/B8560)。**ismc**:同两端点,当前 club==A,**L3 派生非 bit**。
- **stdt/endt** wire+13/+17(各4B→+0x20/+0x24)**L3** packed date(day=u16&0x1ff,year=高u16;年1900..2024/1900..2042,默认1900day1 6909/8902)。
- **fri%/pwgp** wire+35/+42(i8→+0x33/+0x36)**L3**(-1 unset 7715/131,live[0,100],pwgp raw0 8776)。
- **20 bool 共 u32@wire+5..8**(CLUB_LINK+0x1c,单 4B transfer,**非各独立 byte**):bit→code `1frly 2golo 3fotb 4plfr 5yutr 6perm 7smbo 9fnhl 10hlwf 13mrrl 14scks 15cpsd 16ualf 17lpfs 18ustf 19yout 20rsrv 21pfpr 23UsSK 28bttr`;flag_counts 32 元;row0 word e2018004 frly真golo假。
- **held**:`type`(i8@+4,CAfT 枚举缺21,609 raw,首 row12@580=21,domain_conflict)、`yfee`(i32@+25,8984 个-1,首 row0@37=ffffffff,domain_conflict)、`msls`(i8@+36,全表-1,首 row0@48=ff,all_missing)。
- **clfr**:Cvfl wrapper+8,**runtime-only 非 wire**(枚举0..6,validator 写1..6,副本生成不按校验成功过滤);不入 wire 字段台账,单列 runtime_only。
- occurrence_grades:Cafl{L3:26,held_all_missing:1,held_domain_conflict:2}(29 occurrence,idx370-398);Cvfl{L3:16,held_domain_conflict:2,runtime_only_no_wire_slot:1}(19 occurrence,idx400-418)。**共享 occurrence 不当作独立 wire 槽**。

## 任务(增量)
1. **新增共享辅助源条目** CLUB_LINK/`club_links.dat`(table_type=null,source_kind=named_auxiliary_pod,rtti=null,无 factory case)。记 47B POD cursor、closure、payload/row-block SHA、版本 word 门槛、client 缺席。Cafl/Cvfl 作为该源上的**两视图**,各列 scoped occurrence(code/schema_idx/grade/encoding/wire 坐标或派生说明)。
2. **坐标政策**:
   - affl/ismc 为**派生字段**(viewer-relative 双端点),coordinate_note 说明派生逻辑(当前 club==A 取 B/取真),不写单一 row_offset 冒充实槽;两端点 wire+0/+9 如实记。
   - 20 bool 共用 u32@wire+5,每 bit 一 occurrence,记 bit_index/bit_mask,coordinate_note 说明共字 bitmask(非独立 byte)。
   - clfr 单列 runtime_only_no_wire_slot,**不计入 wire L3**。
   - held type/yfee/msls 留首反例与原因,不晋级。
3. **coverage 计账(双口径,明确政策)**:保留 v3 `club_L3_fields=52`(8 数字表 scoped 字段)verbatim;新增 Cafl/Cvfl 后同时报:
   - `club_L3_occurrences`(scoped occurrence 计)= 52 + 26 + 16 = **94**;
   - `club_L3_unique_wire_fields`(独立 wire 槽计)= 52 + Cafl/Cvfl 共享源去重后的独立 L3 wire 槽数(从 fields_cafl_cvfl.json 实算,affl 双端点/ismc 派生/20 bool 共字如何计须写明政策,clfr runtime 排除)。
   - held_fields、negative_regressions、L4=0 相应更新并说明。schema_version=4。
4. **保留 v3 全部 8 表 52 L3 + 16 held + 4 negative verbatim**;存 v3 快照 scratch/t48/out/club_nation_subtable_schema.v3.json;独立校验 v3 八表字段未改。
5. **nation 侧**:并 t46 数据侧状态(server table_10 251 行框架/闭合 L1/L2 闭合,row ID 跨配 t25,whole-row grammar different,A/B/C/D 内部 open,**0 新 L3**);t37 25 unknown partial 仍 0 独占 L3(t47 sol 静态发现进行中,不预支)。nation 侧不晋级任何 server-only 字段。
6. 全 provenance 从 t44/t46 产物抽(source_task=t44/t46,reader VA、master SHA 7d57477e、editor SHA b82ebe8e、各 payload SHA)。

## 边界
- 只增量 t44 Cafl/Cvfl + t46 nation 数据侧状态;不新解析、不跑游戏/编辑器/IDA、不联网、不读写 Z:。
- 候选/held/runtime_only 不升级;negative 原样保留;L4=0。
- 只写 scratch/t48/ 与 reports/club_nation_subtable_schema.{json,md}(v4 in-place,自己产物演进)。

## 交付
- reports/club_nation_subtable_schema.json + .md(v4,8 数字表 + CLUB_LINK 共享辅助源两视图)
- scratch/t48/out/consolidate_v4.py(--help/--selftest:双口径计账、v3 八表 verbatim、CLUB_LINK POD closure、affl/ismc 派生注记、clfr runtime 排除、bool bitmask)、verify.py(独立不 import builder)、club_nation_subtable_schema.v3.json、REPORT.md、DONE.md
- Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + t01_anchors.py(7/7)。