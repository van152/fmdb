# 已知实体基数清单(t13e 旁路)

`status`: **partial** —— 旁路资料整理,仅供 t13 主线交叉核对;本表不裁决实体归属。

生成:2026-11-18;每个数字均带出处(文件名 + table_id 或 E 编号)。

## 实体 → 行数(按实体名排序)

| 实体 | 行数 | 出处 | 交叉核对 | 可靠性 | 冲突 |
|---|---:|---|---|---|---|
| agreement (agrm) | 6 | scratch/t05/COVERAGE.json:client table_56 + server table_56 | closure 14+6*13+8=100(client)/server 同式 | high | - |
| award | 3,545 | scratch/t05/COVERAGE.json:client table_0 + server table_0 | scratch/t05/fixtures_truth.json table_0 closure 14+3545*77+8=272987;scratch/t01/LEDGER.json:E38 award 3545 行逐行身份复算 | high | - |
| city | 56,293 | scratch/t05/COVERAGE.json:client table_2 (server table_2 同为 56293) | E42 city 列画像同为 56293;E30/E38/E51 全量 56,293 行走查;fixtures_truth.json closure 14+56293*43+8=2420621 | high | - |
| club | 84,259 | scratch/t05/COVERAGE.json:client table_3 + server table_3 | E33 行框架 84,259/84,259 走通(5B 标准块 84,256 + 3 特例行);E37 独立 walker 复现 server table_3 = 84,259 行,终点 16,595,304+8 | high | - |
| club subtable: 战绩 (t37) | 465,712 | scratch/t05/COVERAGE.json:server table_37 | E56 t37=465712 行(club×赛事);closure 14+465712*40+8=18628502 | mid | - |
| club subtable: 球场/迁建 (t22) | 449 | scratch/t05/COVERAGE.json:server table_22 + client table_22 | E56 t22=449 (df=1 码 Salt/Scam/Scpm/Slhm → club);t13d audit rows_dumped 449/449 | mid | - |
| club subtable: 赛事史 (t34, candidate) | 7,115 | scratch/t05/COVERAGE.json:server table_34 | E56 t34=7115 只有 B 类行数/语义锚,candidate;t13d audit rows_dumped 7115/7115 | low | - |
| club subtable: 转会分期 (t43, candidate) | 535 | scratch/t05/COVERAGE.json:server table_43 | E56 t43=535 (B 类 candidate);closure 14+535*46+8=24632 | low | - |
| competition (comp) | 7,047 | scratch/t05/COVERAGE.json:client table_25 + server table_25 | reports/t01f_comp_row_offsets.md 7,047/7,047 身份块全过;E20 自检 7047 行 | high | - |
| continent (cont) | 7 | scratch/t05/COVERAGE.json:client table_5 + server table_5 | scratch/t02/cont_reference.json closure 14+7*34+8=260;E56 cont=7 | high | - |
| currency (curr) | 173 | scratch/t05/COVERAGE.json:client table_41 + server table_41 | E30 curr 173/173 封口;scratch/t02/curr_reference.json 双 archive byte-identical | high | - |
| derby (drbr) | 1,567 | scratch/t02/drbr_reference.json row_framework.count=1567 (client_db/table_18.dat) | scratch/t05/COVERAGE.json:client table_18 count=1567,server table_18 亦 1567 | mid | - |
| injury (inju) | 115 | scratch/t05/COVERAGE.json:client table_6 + server table_6 | E38/E51 injury 115 行逐行身份;E40 字段命名;fixtures_truth closure 14+115*16+8=1862 | high | - |
| language (lang) | 126 | scratch/t05/COVERAGE.json:client table_8 + server table_8 | scratch/t02/lang_reference.json row_len=4+len+30,走查 126 行;E42 language count=126 | high | - |
| local region (lcrg) | 2,488 | scratch/t05/COVERAGE.json:client table_47 + server table_47 | E37 scripts/t05_lcrg.py 双约束闭合 2,488 行 rdui/duni 2488/2488;E42/E51 2,488 行 csv | high | - |
| media source (mdso) | 208 | scratch/t05/COVERAGE.json:client table_7 + server table_7 | E33 fw7 count208/size36824 client+server 双 closure | high | - |
| nation (nati) | 251 | scratch/t05/COVERAGE.json:client table_10 (server table_10 同为 251) | E34 client 251/251 行精确封口;E21 duni 锚点;E37 未复现项(我的 walker 第129行卡住,不构成否证) | high | - |
| nation name/key companion | 251 | scratch/t05/COVERAGE.json:client table_9 (server table_9 同为 251) | COVERAGE.md '251 行 sentinel+duni 尾锚全封口';server table_9 同行数。同基数不等于同一实体 —— E23 裁定 type 9 = NATIONAL_TEAM_CONTAINER,见 name_conflicts | mid | - |
| person (basic_people_db 全库) | 658,011 | scratch/t05/people/attrs.json count=658011 (basic_people_db.dat) | E25 u32 count=658,011 + 658,011/658,011 行尾身份;E32 独立解压走查 658,011 行封口;docs/BASELINE.md people_db 行链 100% | high | - |
| person subtable: 任职履历 (t49) | 792,149 | scratch/t05/COVERAGE.json:server table_49 | E56 t49=792149 行(df=1 码 ajob/otea/plac → person);scratch/cmd/stage2_candidate_adjudication.json | mid | - |
| player subtable: 伤病/未来状态 (t30) | 72,473 | scratch/t05/COVERAGE.json:server table_30 | E56 t30=72473 (df=1 码 futu/inju/pret/seve → player);t13d audit rows_dumped 72473/72473 | mid | - |
| region (regi) | 28 | scratch/t05/COVERAGE.json:client table_19 + server table_19 | E29 regi 28/28 身份块 + closure 14+28*45+8=1282(client)/46(server) | high | - |
| stadium (stad) | 48,413 | scratch/t05/COVERAGE.json:client table_21 + server table_21 | E38 stadium 48413 行逐行身份;E51 48,413 行 csv;fixtures_truth closure | high | - |
| stage name (stgn) | 278 | scratch/t05/COVERAGE.json:client table_23 + server table_23 | scratch/t02/stgn_reference.json stride 14 双 archive byte-identical;closure 14+278*14+8=3914 | high | - |
| team | 84,507 | scratch/t05/COVERAGE.json:server table_24 | E37 gap:team 84,507 行/8,819,030 B,均值 104.36B 非整数,取数为 L1 走查计数(行边界未闭合) | mid | - |
| weather profile (weat) | 334 | scratch/t05/COVERAGE.json:client table_27 + server table_27 | E27 334 行全量走查(payload 43,345B)+ 身份块 334/334;E42 city off14 max=333 → 落在 [0,334) | high | - |

## 实体身份未定的表(基数可用,名字勿用)

| archive | table_id | 行数 | 出处 |
|---|---:|---:|---|
| client | 35 | 890 | client table_35 |
| server | 12 | 28,597 | server table_12 |
| server | 26 | 90,128 | server table_26 |
| server | 29 | 13,278 | server table_29 |
| server | 31 | 37,283 | server table_31 |
| server | 32 | 315 | server table_32 |
| server | 33 | 32,409 | server table_33 |
| server | 36 | 6,535 | server table_36 |
| server | 38 | 5,241 | server table_38 |
| server | 39 | 117 | server table_39 |
| server | 42 | 17,721 | server table_42 |
| server | 45 | 84,477 | server table_45 |
| server | 46 | 7 | server table_46 |
| server | 48 | 5,210 | server table_48 |
| server | 50 | 45 | server table_50 |
| server | 51 | 59 | server table_51 |
| server | 52 | 0 | server table_52 |
| server | 57 | 0 | server table_57 |
| server | 58 | 8 | server table_58 |
| server | 59 | 9,079 | server table_59 |
| server | 60 | 59 | server table_60 |
| server | 61 | 16 | server table_61 |
| server | 62 | 37,214 | server table_62 |
| server | 63 | 2 | server table_63 |
| server | 64 | 6,946 | server table_64 |
| server | 65 | 1,417 | server table_65 |
| server | 66 | 753 | server table_66 |
| server | 67 | 6,826 | server table_67 |
| server | 68 | 138 | server table_68 |
| server | 69 | 230 | server table_69 |
| server | 70 | 10,075 | server table_70 |
| server | 71 | 616,665 | server table_71 |
| server | 72 | 138 | server table_72 |
| server | 73 | 1 | server table_73 |

## 实体身份被推翻(negative)的表

| table_id | 行数 | 出处 |
|---:|---:|---|
| 31 | 37,283 | scratch/cmd/stage2_candidate_adjudication.json (status=negative) |
| 42 | 17,721 | scratch/cmd/stage2_candidate_adjudication.json (status=negative) |
| 46 | 7 | scratch/cmd/stage2_candidate_adjudication.json (status=negative) |
| 50 | 45 | scratch/cmd/stage2_candidate_adjudication.json (status=negative) |
| 51 | 59 | scratch/cmd/stage2_candidate_adjudication.json (status=negative) |

## 冲突项

- 行数层面:**无冲突**。同一 (archive,table_id) 在 COVERAGE / server_bounds / fixtures_truth / stage2_candidate_adjudication / t13d audit 五个工件的计数全部一致(78 张表参与比对;篡改一份记录作负对照,检测器能报出冲突)。
- table_18 1,567 行:COVERAGE.json: 'city-associated secondary-name data' ↔ scratch/t02/drbr_reference.json: db::DERBY (RTTI .?AVDERBY@db@@)。基数一致(1567),仅实体名冲突;t13 取名时勿同时采纳两种身份
- table_24 84,507 行:COVERAGE.json: team(行边界 open)。行数可用,行边界不可用;若按 82B 定长假设使用会与 E37 的均值 104.36B 冲突
- table_9 251 行:COVERAGE.json: 'nation (name/key companion)' + stage2_three_way entity_tag=nati ↔ LEDGER E23: table_type 9 = NATIONAL_TEAM_CONTAINER,t01e 的 nati 双虚表标签已勘误;table_type 10 才是 NATION。251 与 table_10 同基数,不能据此判定同一实体;若需 nation 主表请用 table_10

## schema / 布局旁证(不参与冲突判定,仅供主线算宽度)

| 实体 | table_type | entity_tag | schema 字段数 | 业务宽度(client/server) | 布局档数(client/server) |
|---|---:|---|---:|---|---|
| agreement (agrm) | 56 | agrm | 8 | - | - |
| award | 0 | awar | 38 | - | - |
| city | 2 | city | 15 | - | - |
| city | 2 | - | - | 30/30 | 9/9 |
| club | 3 | club | 433 | - | - |
| competition (comp) | 25 | comp | 255 | - | - |
| continent (cont) | 5 | cont | 16 | - | - |
| currency (curr) | 41 | curr | 7 | - | - |
| derby (drbr) | 18 | drbr | 22 | - | - |
| injury (inju) | 6 | inju | 27 | - | - |
| injury (inju) | 6 | - | - | 3/27 | 3/21 |
| language (lang) | 8 | lang | 12 | - | - |
| local region (lcrg) | 47 | lcrg | 11 | - | - |
| local region (lcrg) | 47 | - | - | 31/- | 18/- |
| media source (mdso) | 7 | mdso | 22 | - | - |
| nation (nati) | 10 | nati | 346 | - | - |
| nation name/key companion | 9 | nati | 346 | - | - |
| region (regi) | 19 | regi | 6 | - | - |
| region (regi) | 19 | - | - | 32/33 | 8/9 |
| stadium (stad) | 21 | stad | 60 | - | - |
| stadium (stad) | 21 | - | - | 25/- | 19/- |
| stage name (stgn) | 23 | stgn | 8 | - | - |
| stage name (stgn) | 23 | - | - | 1/1 | 1/1 |
| team | 24 | team | 25 | - | - |
| weather profile (weat) | 27 | weat | 94 | - | - |

## 非行数锚点(同表基数一起用)

| 锚点 | 关联基数 | 出处 |
|---|---|---|
| 六大洲 0..5 | continent=7 | docs/BASELINE.md |
| England=139 / China PR=55 | nation=251,值域 [0,251) | docs/BASELINE.md + reports/t01f_comp_row_offsets.md (§ccti/cnti 锚点) |
| parent row 352 | comp=7047 | reports/t01f_comp_row_offsets.md |
| Bernabéu 81,044 | stadium=48413 | docs/BASELINE.md |
| city Cnti=139 (Liverpool/Manchester) | nation=251 | scratch/t05/fixtures_truth.json named_rows |

## 说明

- 已收录 26 个实体/子实体条目,覆盖 t05 COVERAGE 里全部 client 表与全部已有实体名的 server 表
- 34 张实体名未定/被推翻的表以 unidentified_tables 给出基数(含 count=0 的 t52/t57),未强行命名
- 同一 (archive,table_id) 跨 5 个既有工件比对基数(COVERAGE / server_bounds / fixtures_truth / stage2_candidate_adjudication / t13d audit),不一致项 0 个(78 张表参与比对)
- 未收录:history_db / lang_update_db / summary.dat 等非数值主表(不在必查文件范围)
- **club subtable: 球场/迁建 (t22)**:449 行 ≠ stadium 主表 48,413;E47 记录 t22 在 club 覆盖 14/14、在 stadium 仅 3/76
- **club subtable: 赛事史 (t34, candidate)**:实体归属仅有 B 类(行数/语义)证据,E56 明确标 candidate
- **derby (drbr)**:同一张表在 COVERAGE.json 里实体名写作 'city-associated secondary-name data',实体归属未定(见 name_conflicts);基数 1567 无争议
- **nation name/key companion**:实体名本身有争议(COVERAGE 叫 'nation name/key companion',stage2_three_way 给 entity_tag=nati,E23 裁定为 NATIONAL_TEAM_CONTAINER);251 这个基数在任何一种解释下都成立
- **person (basic_people_db 全库)**:分 class 行数:1 ACTUAL_NON_PLAYER=166064 / 2 ACTUAL_PLAYER=476158 / 3=4757 / 4 OFFICIAL=9839 / 5 RETIRED_NAME=1193(同源 attrs.json class_counts)
- **person subtable: 任职履历 (t49)**:实体归属 A 级(schema df=1),但行边界闭合与 entity 名字不是同一层证据
- **player subtable: 伤病/未来状态 (t30)**:72,473 >> injury 主表 115,故是 player 侧伤病例表而非 injury
- **team**:行数已从 header 计数与 payload 长度读出,但 table_24 是全库唯一的边界 open 表;E37 报 '12+82*84507 精确满足 table_extra_24' 为强假设,未验收
