# t110 全库 L3 总账报告

- Join 输入：wire traces 79 条记录；IDA mem map 67 表。
- Join 覆盖：54 表有执行级 Join，1036 个唯一 4CC/table 映射。
- Unicorn 记录：CLOSED=30；OK_SAMPLE=23；FAIL=10；NOT_IN_SERVER_CLIENT_DB=4。
- 回归：exact=2，within_slot=27，mismatch=23。mismatch 表示既有 L3 坐标未被本次 row0 `this` 读区间覆盖，不能据此推翻原字段结论；逐项 reason 在 coverage JSON。

## 67 表覆盖矩阵

| table_type | class | entity | Unicorn | L3 4CC | server wire | client wire |
|---:|---|---|---|---:|---:|---:|
| 0 | AWARD | awar | FAIL | 12 | 14 | 14 |
| 1 | BASIC_PERSON | pers | NOT_IN_SERVER_CLIENT_DB | 0 | 0 | 0 |
| 2 | CITY | city | OK_SAMPLE (50 rows) | 10 | 10 | 10 |
| 3 | CLUB | club | FAIL | 30 | 12 | 6 |
| 3 | TEAM_CONTAINER | club | FAIL | 0 | 12 | 6 |
| 3 | LEAGUE_BODY_CLUB | club | FAIL | 0 | 12 | 6 |
| 4 | RGB_COLOUR |  | NOT_IN_SERVER_CLIENT_DB | 0 | 0 | 0 |
| 5 | CONTINENT | cont | CLOSED (diff=0) | 13 | 8 | 8 |
| 6 | INJURY | inju | CLOSED (diff=0) | 21 | 22 | 4 |
| 7 | MEDIA_SOURCE | mdso | CLOSED (diff=0) | 10 | 10 | 7 |
| 8 | LANGUAGE | lang | CLOSED (diff=0) | 8 | 9 | 9 |
| 9 | NATIONAL_TEAM_CONTAINER | nati | CLOSED (diff=0) | 102 | 112 | 31 |
| 9 | TEAM_CONTAINER | nati | CLOSED (diff=0) | 0 | 112 | 31 |
| 10 | NATION | nati | CLOSED (diff=0) | 71 | 29 | 10 |
| 12 | STARTING_AWARD_HISTORY | awar | OK_SAMPLE (50 rows) | 50 | 26 | 0 |
| 14 | PLAYING_HISTORY | pers | NOT_IN_SERVER_CLIENT_DB | 0 | 0 | 0 |
| 18 | DERBY | drbr | OK_SAMPLE (50 rows) | 30 | 19 | 16 |
| 19 | REGION | regi | CLOSED (diff=0) | 0 | 10 | 9 |
| 21 | STADIUM | stad | OK_SAMPLE (50 rows) | 114 | 44 | 9 |
| 22 | STADIUM_CHANGE | stad | CLOSED (diff=0) | 21 | 22 | 1 |
| 23 | STAGE_NAME | stgn | CLOSED (diff=0) | 1 | 2 | 2 |
| 24 | NATIONAL_TEAM | team | OK_SAMPLE (50 rows) | 30 | 18 | 0 |
| 24 | TEAM | team | OK_SAMPLE (50 rows) | 0 | 18 | 0 |
| 25 | COMP | comp | OK_SAMPLE (50 rows) | 160 | 70 | 54 |
| 26 | COMP_HISTORY_RECORD | comp | OK_SAMPLE (50 rows) | 20 | 18 | 0 |
| 27 | WEATHER | weat | CLOSED (diff=0) | 89 | 92 | 92 |
| 29 | STARTING_LOAN | pers | OK_SAMPLE (50 rows) | 13 | 14 | 0 |
| 30 | STARTING_INJURY | play | OK_SAMPLE (50 rows) | 8 | 10 | 0 |
| 31 | STARTING_CONFIDENCE | play | OK_SAMPLE (50 rows) | 5 | 4 | 0 |
| 32 | STARTING_FUTURE_TRANSFER | pers | FAIL | 7 | 10 | 0 |
| 33 | STARTING_CLUB_DEBT | club | OK_SAMPLE (50 rows) | 16 | 21 | 0 |
| 34 | STARTING_TEAM_CUP_HISTORY | club | OK_SAMPLE (50 rows) | 9 | 12 | 0 |
| 35 | PLAYER_TYPE | play | CLOSED (diff=0) | 3 | 3 | 3 |
| 36 | STARTING_MANAGER_HOF_RECORD | pers | FAIL | 5 | 4 | 0 |
| 37 | STARTING_TEAM_LEAGUE_HISTORY | club | OK_SAMPLE (50 rows) | 12 | 15 | 0 |
| 38 | STARTING_BAN | pers | OK_SAMPLE (50 rows) | 7 | 9 | 0 |
| 39 | STARTING_AVERAGE_POINTS | team | CLOSED (diff=0) | 1 | 3 | 0 |
| 41 | CURRENCY_RECORD | curr | CLOSED (diff=0) | 3 | 0 | 2 |
| 42 | STARTING_RETIREMENT | pers | OK_SAMPLE (50 rows) | 2 | 4 | 0 |
| 43 | STARTING_MONTHLY_INSTALLMENT | club | CLOSED (diff=0) | 6 | 7 | 0 |
| 44 | NON_PLAYING_HISTORY | pers | NOT_IN_SERVER_CLIENT_DB | 0 | 0 | 0 |
| 45 | STARTING_RECORD |  | FAIL | 0 | 0 | 0 |
| 46 | STARTING_DRAFT_TRANSFER | pers | CLOSED (diff=0) | 5 | 6 | 0 |
| 47 | LOCAL_REGION | lcrg | OK_SAMPLE (50 rows) | 3 | 17 | 17 |
| 48 | STARTING_RECORD |  | FAIL | 18 | 18 | 0 |
| 49 | STARTING_PERSON_HISTORY | pers | OK_SAMPLE (50 rows) | 9 | 4 | 0 |
| 50 | STARTING_MLS_TRADED_SLOT | club | CLOSED (diff=0) | 5 | 5 | 0 |
| 51 | STARTING_MLS_GENERAL_ALLOCATION_MONEY | club | CLOSED (diff=0) | 5 | 4 | 0 |
| 52 | STARTING_PLAYER_HAPPINESS | play | CLOSED (diff=0) | 0 | 0 | 0 |
| 56 | AGREEMENT | agrm | CLOSED (diff=0) | 2 | 1 | 1 |
| 57 | FIXTURE_NAME |  | CLOSED (diff=0) | 0 | 0 | 0 |
| 58 | STARTING_WEEKLY_WAGE_CONTRIBUTION | club | CLOSED (diff=0) | 5 | 6 | 0 |
| 59 | STARTING_MEDIA_EXPECTATIONS | play | OK_SAMPLE (50 rows) | 5 | 3 | 0 |
| 60 | STARTING_MLS_TARGETED_ALLOCATION_MONEY | club | CLOSED (diff=0) | 2 | 4 | 0 |
| 61 | STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT | club | CLOSED (diff=0) | 5 | 4 | 0 |
| 62 | STARTING_RESERVE_TEAM | club | OK_SAMPLE (50 rows) | 15 | 12 | 0 |
| 63 | STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER | club | CLOSED (diff=0) | 5 | 4 | 0 |
| 64 | STARTING_CLUB_STAFF_JOB_STATUS | club | OK_SAMPLE (50 rows) | 5 | 5 | 0 |
| 65 | STARTING_NEWGEN_PARAMETER | pers | CLOSED (diff=0) | 4 | 6 | 0 |
| 66 | STARTING_CLUB_TRANSFER_PREFERENCE | club | CLOSED (diff=0) | 4 | 6 | 0 |
| 67 | STARTING_NEWGEN_PARAMETER | pers | OK_SAMPLE (50 rows) | 4 | 6 | 0 |
| 68 | STARTING_NEWGEN_PARAMETER | pers | CLOSED (diff=0) | 4 | 6 | 0 |
| 69 | STARTING_NEWGEN_PARAMETER | pers | CLOSED (diff=0) | 4 | 6 | 0 |
| 70 | STARTING_VISION_OBJECTIVE | club | OK_SAMPLE (50 rows) | 10 | 13 | 0 |
| 71 | STARTING_PAST_TRANSFER | pers | FAIL | 23 | 9 | 0 |
| 72 | STARTING_PAST_TRADE | pers | FAIL | 0 | 0 | 0 |
| 73 | STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT | play | CLOSED (diff=0) | 5 | 4 | 0 |

## 详细样例

### table_type=3 CLUB — FAIL
wire fields server/client=12/6; joined=30

- Cnat server obj+0xd8 slot+0x0, wire row0 +0 len=4, caller=0x140e5b21d, getter=0x140e834a0
- Cext server obj+0xd8 slot+0x0, wire row0 +0 len=4, caller=0x140e5b21d, getter=0x140e8a400
- Cnti server obj+0xd8 slot+0x0, wire row0 +0 len=4, caller=0x140e5b21d, getter=0x140e8a400
- Cbni server obj+0xe8 slot+0x0, wire row0 +8 len=4, caller=0x140e5b27a, getter=0x140e834a0
- Cccn server obj+0xf0 slot+0x0, wire row0 +12 len=4, caller=0x140e5b2a3, getter=0x140e834a0
- Ccty server obj+0xf8 slot+0x0, wire row0 +16 len=4, caller=0x140e5b2d0, getter=0x140e8a400
- Ccre server obj+0xf8 slot+0x0, wire row0 +16 len=4, caller=0x140e5b2d0, getter=0x140e8a400
- Clri server obj+0xf8 slot+0x0, wire row0 +16 len=4, caller=0x140e5b2d0, getter=0x140e8a400
- CnCV server obj+0x160 slot+0x3, wire row0 +20 len=6, caller=0x140e5b32d, getter=0x140e8a400
- Cnam server obj+0x160 slot+0x0, wire row0 +20 len=6, caller=0x140e5b32d, getter=0x140e834a0
- CiEC server obj+0x160 slot+0x0, wire row0 +20 len=6, caller=0x140e5b32d, getter=0x140e8a400
- Csot server obj+0x160 slot+0x0, wire row0 +20 len=6, caller=0x140e5b32d, getter=0x140e834a0

### table_type=3 TEAM_CONTAINER — FAIL
wire fields server/client=12/6; joined=0


### table_type=3 LEAGUE_BODY_CLUB — FAIL
wire fields server/client=12/6; joined=0


### table_type=9 NATIONAL_TEAM_CONTAINER — CLOSED (diff=0)
wire fields server/client=112/31; joined=102

- TKpA server obj+0x1c0 slot+0x0, wire row0 +66 len=4, caller=0x14105d710, getter=0x1411f1090
- TKpL server obj+0x1c0 slot+0x0, wire row0 +66 len=4, caller=0x14105d710, getter=0x1411f1090
- TLeg server obj+0x1c0 slot+0x0, wire row0 +66 len=4, caller=0x14105d710, getter=0x1411f1090
- Npop server obj+0x1c4 slot+0x0, wire row0 +74 len=4, caller=0x14105d710, getter=0x141042940
- Ngct server obj+0x1c8 slot+0x3, wire row0 +82 len=4, caller=0x14105d710, getter=0x141045d50
- Nndn server obj+0x1c8 slot+0x0, wire row0 +82 len=4, caller=0x14105d710, getter=0x141042940
- Nnam server obj+0x1cc slot+0x2, wire row0 +90 len=4, caller=0x14105d710, getter=0x141045d50
- Nnam server obj+0x1cc slot+0x3, wire row0 +90 len=4, caller=0x14105d710, getter=0x141045d50
- Nygn server obj+0x1cc slot+0x1, wire row0 +90 len=4, caller=0x14105d710, getter=0x141045d50
- Nsod server obj+0x1cc slot+0x0, wire row0 +90 len=4, caller=0x14105d710, getter=0x141045d50
- TCsn server obj+0x1cc slot+0x2, wire row0 +90 len=4, caller=0x14105d710, getter=0x141045d50
- TCsn server obj+0x1cc slot+0x3, wire row0 +90 len=4, caller=0x14105d710, getter=0x141045d50

### table_type=9 TEAM_CONTAINER — CLOSED (diff=0)
wire fields server/client=112/31; joined=0


### table_type=10 NATION — CLOSED (diff=0)
wire fields server/client=29/10; joined=71

- NnsC server obj+0x118 slot+0x0, wire row0 +0 len=4, caller=0x141040511, getter=0x141042940
- NnsR server obj+0x118 slot+0x0, wire row0 +0 len=4, caller=0x141040511, getter=0x141042940
- Nnsi server obj+0x118 slot+0x0, wire row0 +0 len=4, caller=0x141040511, getter=0x141042940
- tcRT server obj+0x118 slot+0x0, wire row0 +0 len=4, caller=0x141040511, getter=0x1411f1090
- Ngct server obj+0x1cb slot+0x0, wire row0 +524 len=1, caller=0x141040fca, getter=0x141045d50
- Ncti server obj+0xf0 slot+0x0, wire row0 +525 len=4, caller=0x141040fee, getter=0x141045d50
- Ncni server obj+0xf0 slot+0x0, wire row0 +525 len=4, caller=0x141040fee, getter=0x141042940
- link server obj+0xf0 slot+0x0, wire row0 +525 len=4, caller=0x141040fee, getter=0x141042940
- Nntp server obj+0xf0 slot+0x0, wire row0 +525 len=4, caller=0x141040fee, getter=0x141063f30
- Nrgi server obj+0xf8 slot+0x0, wire row0 +529 len=4, caller=0x141041012, getter=0x141045d50
- Nntp server obj+0xf8 slot+0x0, wire row0 +529 len=4, caller=0x141041012, getter=0x141063f30
- NcpR server obj+0xe8 slot+0x0, wire row0 +533 len=4, caller=0x141041036, getter=0x141042940

### table_type=24 NATIONAL_TEAM — OK_SAMPLE (50 rows)
wire fields server/client=18/0; joined=30

- tcRT server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- Niaf server obj+0xb8 slot+0x1, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1410668f0
- subt server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TKpA server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TKpL server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TLeg server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TISC server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TISN server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TCng server obj+0xb8 slot+0x0, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- Tvsp server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- TcSs server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f1090
- tNMF server obj+0xb8 slot+0x2, wire row0 +0 len=4, caller=0x1410536d0, getter=0x1411f4f70

### table_type=24 TEAM — OK_SAMPLE (50 rows)
wire fields server/client=18/0; joined=0


### table_type=25 COMP — OK_SAMPLE (50 rows)
wire fields server/client=70/54; joined=160

- levl server obj+0x1a2 slot+0x0, wire row0 +15 len=1, caller=0x140eb7aba, getter=0x140ecb5c0
- Ccre server obj+0x1a4 slot+0x0, wire row0 +17 len=1, caller=0x140eb7b03, getter=0x140ec0a60
- CTty server obj+0x1a5 slot+0x0, wire row0 +18 len=1, caller=0x140eb7b26, getter=0x140ec0a60
- Pctd server obj+0x189 slot+0x0, wire row0 +28 len=1, caller=0x1444a7235, getter=0x140ecb5c0
- cnti server obj+0x58 slot+0x0, wire row0 +52 len=4, caller=0x140eb7c6f, getter=0x140ecb5c0
- ccti server obj+0x58 slot+0x0, wire row0 +52 len=4, caller=0x140eb7c6f, getter=0x140ecb5c0
- Accl server obj+0x60 slot+0x0, wire row0 +56 len=4, caller=0x140eb7c8f, getter=0x140ec0a60
- cnti server obj+0x60 slot+0x0, wire row0 +56 len=4, caller=0x140eb7c8f, getter=0x140ecb5c0
- cnat server obj+0x60 slot+0x0, wire row0 +56 len=4, caller=0x140eb7c8f, getter=0x140ecb5c0
- lbc  server obj+0x70 slot+0x0, wire row0 +60 len=4, caller=0x140eb7caf, getter=0x140ecb5c0
- cpcm server obj+0x68 slot+0x0, wire row0 +64 len=4, caller=0x140eb7ccf, getter=0x140ecb5c0
- crep server obj+0x180 slot+0x0, wire row0 +70 len=2, caller=0x140eb7dbc, getter=0x140ecb5c0

### table_type=32 STARTING_FUTURE_TRANSFER — FAIL
wire fields server/client=10/0; joined=7

- PFcl server obj+0x50 slot+0x0, wire row0 +4 len=4, caller=0x141191a1c, getter=0x141194740
- PFdt server obj+0x68 slot+0x0, wire row0 +8 len=4, caller=0x141191a73, getter=0x141194740
- PFtf server obj+0x6c slot+0x0, wire row0 +12 len=4, caller=0x141191aa7, getter=0x141194740
- PFwa server obj+0x70 slot+0x0, wire row0 +16 len=4, caller=0x141191ac7, getter=0x141194740
- PFed server obj+0x74 slot+0x0, wire row0 +21 len=4, caller=0x143b48dd7, getter=0x141194740
- PFjo server obj+0x7f slot+0x0, wire row0 +25 len=1, caller=0x141191b1b, getter=0x141194740
- PFjo server obj+0x7c slot+0x0, wire row0 +26 len=2, caller=0x141191b3b, getter=0x141194740
- PFcs server obj+0x80 slot+0x0, wire row0 +19096 len=1, caller=0x141191cfb, getter=0x1411925f0

### table_type=71 STARTING_PAST_TRANSFER — FAIL
wire fields server/client=9/0; joined=23

- PLfl server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x1415799b0
- PLic server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLmc server obj+0x48 slot+0x2, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLob server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLoc server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLcm server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLcr server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLct server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PLbr server obj+0x48 slot+0x0, wire row0 +0 len=4, caller=0x141199474, getter=0x141578930
- PPfr server obj+0x38 slot+0x0, wire row0 +4 len=4, caller=0x141199494, getter=0x14119b410
- PLAC server obj+0x38 slot+0x0, wire row0 +4 len=4, caller=0x141199494, getter=0x1415799b0
- PPto server obj+0x40 slot+0x0, wire row0 +8 len=4, caller=0x1411994b4, getter=0x14119b410

## Unicorn FAIL 表清单

- type 0 AWARD
- type 3 CLUB
- type 3 TEAM_CONTAINER
- type 3 LEAGUE_BODY_CLUB
- type 32 STARTING_FUTURE_TRANSFER
- type 36 STARTING_MANAGER_HOF_RECORD
- type 45 STARTING_RECORD
- type 48 STARTING_RECORD
- type 71 STARTING_PAST_TRANSFER
- type 72 STARTING_PAST_TRADE

## 字段范围与限制

- 按 row0 `dst_kind=this` 读取的半开区间 `[obj_off, obj_off+wire_len)` 与 IDA 的 `mem_offsets` / `primary_off_int` 求交；记录槽内偏移 `in_slot_off`。
- server/client 序列独立保留；server_only/shared/client_only 在各表 `field_scope` 中。
- 仅接受来源中显式列出的 IDA 偏移；subobject 基址仅在 `mem_offsets` 明确提供时参与，不猜测继承偏移。
- 进度里程碑以本次实际产物为准：执行级 L3 映射表数见上，不将旧的“6/74”误当作可复算输入。
