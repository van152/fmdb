# t29b — club 子表 inventory 综合(t29 画像已交付,只补综合层)

你是受指挥官委派的子代理。t29 已产出 **13 个子表 complete_data_profile**(指挥官独立核验 13/13 封口+count+列统计通过),但超时前未写综合 inventory。本任务**只补综合层,不重 dump、不重画像**——短任务,务必在窗口内完成。

## 已交付(直接读,勿重做)
- D:\tmp2b\fm24-db\scratch\t29\out\profiles\table_server_{33,34,37,43,50,51,60,61,62,63,64,66,70}.profile.json + .rows.jsonl
  - 33 Cdbt STARTING_CLUB_DEBT 32409×79 / 34 Tchl STARTING_TEAM_CUP_HISTORY 7115×44 / 37 Clhs 465712×40(t30 已 8 L3) / 43 Cmti STARTING_MONTHLY_INSTALLMENT 535×46 / 50 MLS_TRADED_SLOT 45×26 / 51 MLS_GENERAL_ALLOCATION_MONEY 59×23 / 60 MLS_TARGETED_ALLOCATION_MONEY 59×23 / 61 ITALIAN_SERIE_A_FREED_NON_EU_SLOT 16×20 / 62 CSrs STARTING_RESERVE_TEAM 37214×42(t31 进行中) / 63 ITALIAN_NON_EU_SLOTS_NUMBER 2×20 / 64 CLUB_STAFF_JOB_STATUS 6946×21 / 66 CNtp CLUB_TRANSFER_PREFERENCE 753×24 / 70 VISION_OBJECTIVE 10075×40

## 必读
- D:\tmp2b\fm24-db\AGENTS.md
- D:\tmp2b\fm24-db\scratch\t27\out\replication.md §3 scout 表(parent↔table 候选配对 + Cafl/Cvfl 双视图歧义说明)
- D:\tmp2b\fm24-db\scratch\t24\out\subtables.part00*.json(club 全部 nested parent_4cc 清单 + 各 list_item_fields idx)
- D:\tmp2b\fm24-db\scratch\t14\out\census.json(74 表 RTTI/handler/vtables/primary_class/entity_tag/adjudication)
- D:\tmp2b\fm24-db\reports\stage2_table_identity.json(54 resolved 实体归属)
- evidence/fm24/reports/editor_schema/master.json(club.xml list 父码 + list_item_fields;冻结 SHA 7d57477e 对照 MANIFEST)

## 任务(纯综合)
1. 写 `scratch/t29/out/subtable_inventory.json`:对 club 每个 nested list 父码(Cafl/Cvfl/Clhs/CSrs/CAmb/CpTI/Tchl/Calt/Cspb/Coin/Camc/Cmti/Cdbt/Cwcl/CNtp/Csme… 以 t24 subtables 实际清单为准),给 {parent_4cc, table_type, archive, rtti_class, reader_va(若 census/t27 有), count, stride, item_field_candidates(从 profile 列+schema 类型语义对出的 L2 候选,标 candidate), confidence, blockers}。
   - 已画像 13 表直接填实测 count/stride/RTTI;parent↔table 配对依据 RTTI 语义+t14 primary_class+stage2 entity+schema item 语义,**配对不确定标 candidate/unknown,不猜**。
   - Cafl/Cvfl 按 t27 scout 标 unknown(双视图歧义,未证独立表)。
   - MLS/Italian 系列(50/51/60/61/63)若不对应 club.xml list 父码,如实标 entity 归属(可能 nation/competition/其他),不强行塞 club 父码。
   - 未画像的父码(如 CAmb/CpTI/Calt 等)标 table_type=unknown + blockers,列入下一批侦察清单。
2. 修 `scratch/t29/out/verify.py`:改为独立复算 13 画像的封口+count+抽样列统计(不依赖重 dump 全表,可用 profile 内 rows_sha256/count/stride 自洽校验 + 抽样行重读);**注意 table34 多 zstd 帧**(+9 空 stub/+34 真 payload,load_payload 取首帧会误空,须用 +34 或按 profile packed_offset)。--help/--selftest;退出码 0/1/2。
3. 写 REPORT.md(已定子表数/候选字段数/unknown 清单/与 t27/t30/t31 衔接)+ DONE.md(一句话状态)。

## 纪律
- 只读已有画像+仓内证据+只读 editor.exe(若需 VA);只写 scratch/t29/out/;不覆盖 profiles。
- 候选不写结论;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- **不重 dump 全表**(画像已在);综合若需抽样验证只读少量行。务必窗口内交付 inventory+REPORT+DONE。

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data。完成跑 verify + t01_anchors.py(7/7)。