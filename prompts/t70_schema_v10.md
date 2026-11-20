# t70 — Schema v9→v10 合并:第二轮增量并入(luna)

你是受指挥官委派的子代理,做**谨慎的合并**任务。当前公共 schema 为 **v9**(E100)。本轮已验收六份新证据,并入为 **v10**,保护节 verbatim 只做增量:

1. **club_main_row_fields_r2 节**(t63,E106):399 个 E97 unmapped 复查后的 8 个新 L3(`Ccba`/`Cadm`/`Cesd`/`Ceed`/`Cead`/`CteA`/`Chaf`/`Cmtp`——全部 **server mode 的 `CLUB+0x150` tag-0 本地 getter 投影**,45B obj150 游标 `(+0x14,4)(+0x3c,1)(+0x39,3)(+0x2c,13)(+0x10,4)(+0x18,20)`,client 无此载荷)、41 held(含 22 cnst 定位到 `*(CLUB+0x100)+0xe0..0xf5` 但无主行游标、Casp 越界反例 85,746.46 @15571299、rdui identity 抑制)、350 unmapped。**grade 计数:club 主行 L3 13→21**。保留 `date_relationship_control` 负证据(4/4 appeal 早于 start 违反 UI 约束,首 row 1410 @851416)。
2. **comp_main_row_fields_r2 节**(t64,E107):196 unmapped 复查 = **0 新 L3**(诚实负结果);调用记账修正(55 个 stream+0x28 = 52 外层 + 3 tag-4 备用;t59 报 54/51,多出的是 `wbcl_present` @0xeb7c8f);+0xa8/+0xe0 静态入口谓词(0xeb7532/0xeb76c0 presence → je 跳过)与数据反例(server 各 7,047 全零);8 类排除计数(141/38/5/4/4/2/1/1)。**不改变 t59 的 49 L3/10 held/818 倒置**。
3. **nation_main_row_fields_r2 节**(t65,E108):327 unmapped 复查 = **0 新 L3 / 9 转 held**(rdui identity 末 lane 全抑制 + Nnam/Nsnm/N3ln/Nnty/nhrl/dbnm/ttcl/tbcl 无主行 sink)、318 unmapped;双档封口 24,732/422,345、identity **12B**、footer ec7ae404。
4. **comp_collections 节**(t66,E104):7 个非空集合物理文法 L3(vec18/+0xe8/+0xc0/+0xc8/+0xd0/+0xd8/+0x100,逐条文法与你 brief 的 315/366/121/51 次序修正)+ 3 个 held(vec30/+0xa8/+0xe0);**4 条引用 lane L3**:`vec18:item+1→t24`、`+0xd0:item+0→t23`、`+0xd8:item+0/+4→t23`;item+2/+0xc0 inner 全 ffffffff/多域歧义 → held。
5. **EDfx/EDsc 节**(t62,E105):EDsc **分发闭合**——非字面 4CC,key `0x45447363` 归一化 +0xbabb8ccf=0x32,rel32 表基址 0x2a7f0 第 0x32 格 → `0x29389`(68 格中唯一),按对象类型分叉 COMP(25)/NATION(10) 进 Schedule 生成器,结果返回 UI;**它不是持久化字段,原 held 保持正确**。EDfx 上游**未闭合**:仅 `cmp esi,0x45446678` @0x29c37,链路到 fles 容器/日历桶/NATION+0x108 backlink,无 reader/writer/member;7 条可重开排除条件。**同步更正** t55 记录口径:`grade=held, slot=null` 是原 grade,`no_main_wire_slot` 只是任务简称(旧 negative 原文保留)。
6. **tail_ledger 节**(t69,E109):18 项尾账(club skipped 10 全部承接、nation held 4、comp static-zero 3、edge-pending 1),`unresolved=[]`。
7. coverage:`club_main_row_L3 13→21`、新增 r2 计数;provenance `tasks` 增 t62/t63/t64/t65/t66/t69(E105–E109),条目级守卫**扩至 E84–E109**;`generated_by` t60→t70。**既有 v9 各节 verbatim 不动**(含 club 94/59/21、nation 35、comp 49/818)。

## 必读
- AGENTS.md;reports/club_nation_subtable_schema.json+.md(**v9 基线**,E100)
- scratch/t62/out、t63/out、t64/out、t65/out、t66/out、t69/out 的 REPORT.md + 主 JSON
- scratch/t60/out/consolidate_v9.py + verify.py(**方法复刻**;条目级守卫)
- scratch/t01/LEDGER.json(E84–E109)

## 任务
1. `schema_version: 10`;按上述增量;markdown 同步(v9 md 为逐字节前缀);独立 spot(条目级守卫+v9 快照 SHA+保护节+断言:8 新 L3 名/Casp 85746.46/club 21/comp 49 不变/nation 0 新/EDsc 0x32→0x29389/vec18→t24/tail 18);anchors 7/7;--help/--selftest;退出码 0/1/2。
2. 候选不写结论;held/unmapped 原样;不改 scratch/t47–t69;BASELINE.md 指挥官另行。**只写 reports/ 两文件与 scratch/t70/**。

## 交付 scratch/t70/out/
- consolidate_v10.py、verify.py、spot_*.log、v9 快照、REPORT.md、DONE.md;reports/ 两文件升 v10

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
