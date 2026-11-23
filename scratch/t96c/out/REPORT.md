# t96c — Unicorn 全表（79 对 server+client）真机微执行闭合报告

- 耗时：`208.8s`
- 总表对：`79` | **整表 `diff==0` 精确闭合：`41`** | **大表 50 行零异常：`27`** | **合计干净跑通：`68/79`** | 失败：`11`
- `table_9` 双端 251/251 闭合：`True`
- `table_10` 双端 251/251 闭合：`True`

## 全表结果汇总

| archive | tt | class | 状态 | rows_ok / total | diff | uniq_lens | fields | 备注 |
|---|---:|---|---|---:|---:|---:|---:|---|
| server | 0 | `AWARD` | **FAIL** | 1/3545 | 272923 | 1 | 28 | row 1 flag=0xc8 s19=0x140e48db0 consumed=25 err=Invalid memory read (UC_ERR_READ |
| server | 2 | `CITY` | **OK_SAMPLE** | 50/56293 | 2418449 | 1 | 10 |  |
| server | 3 | `CLUB` | **FAIL** | 3/84259 | 16529639 | 3 | 28 | row 3 flag=0x0 s19=0x140e5b1a0 consumed=62498 err=Invalid memory write (UC_ERR_W |
| server | 5 | `CONTINENT` | **CLOSED** | 7/7 | 0 | 1 | 16 |  |
| server | 6 | `INJURY` | **CLOSED** | 115/115 | 0 | 1 | 22 |  |
| server | 7 | `MEDIA_SOURCE` | **CLOSED** | 208/208 | 0 | 126 | 23 |  |
| server | 8 | `LANGUAGE` | **CLOSED** | 126/126 | 0 | 16 | 11 |  |
| server | 9 | `NATIONAL_TEAM_CONTAINER` | **CLOSED** | 251/251 | 0 | 211 | 214 |  |
| server | 10 | `NATION` | **CLOSED** | 251/251 | 0 | 195 | 63 |  |
| server | 12 | `STARTING_AWARD_HISTORY` | **OK_SAMPLE** | 50/28597 | 3733429 | 16 | 28 |  |
| server | 18 | `DERBY` | **OK_SAMPLE** | 50/1567 | 144939 | 12 | 21 |  |
| server | 19 | `REGION` | **CLOSED** | 28/28 | 0 | 1 | 10 |  |
| server | 21 | `STADIUM` | **OK_SAMPLE** | 50/48413 | 8753703 | 1 | 79 |  |
| server | 22 | `STADIUM_CHANGE` | **CLOSED** | 449/449 | 0 | 1 | 22 |  |
| server | 23 | `STAGE_NAME` | **CLOSED** | 278/278 | 0 | 1 | 2 |  |
| server | 24 | `NATIONAL_TEAM` | **OK_SAMPLE** | 50/84507 | 7337866 | 23 | 42 |  |
| server | 25 | `COMP` | **OK_SAMPLE** | 50/7047 | 1516130 | 25 | 123 |  |
| server | 26 | `COMP_HISTORY_RECORD` | **OK_SAMPLE** | 50/90128 | 6215382 | 1 | 19 |  |
| server | 27 | `WEATHER` | **CLOSED** | 334/334 | 0 | 33 | 94 |  |
| server | 29 | `STARTING_LOAN` | **OK_SAMPLE** | 50/13278 | 993300 | 1 | 16 |  |
| server | 30 | `STARTING_INJURY` | **OK_SAMPLE** | 50/72473 | 2462382 | 1 | 10 |  |
| server | 31 | `STARTING_CONFIDENCE` | **OK_SAMPLE** | 50/37283 | 781893 | 1 | 4 |  |
| server | 32 | `STARTING_FUTURE_TRANSFER` | **FAIL** | 1/315 | -8 | 1 | 23 | row 1: pos 19111 >= footer 19103 |
| server | 33 | `STARTING_CLUB_DEBT` | **OK_SAMPLE** | 50/32409 | 2556361 | 1 | 21 |  |
| server | 34 | `STARTING_TEAM_CUP_HISTORY` | **OK_SAMPLE** | 50/7115 | 310860 | 1 | 12 |  |
| server | 35 | `PLAYER_TYPE` | **CLOSED** | 890/890 | 0 | 1 | 3 |  |
| server | 36 | `STARTING_MANAGER_HOF_RECORD` | **FAIL** | 1/6535 | 562702 | 1 | 12 | row 1 flag=0x0 s19=0x14157e310 consumed=18 err=Invalid memory read (UC_ERR_READ_ |
| server | 37 | `STARTING_TEAM_LEAGUE_HISTORY` | **OK_SAMPLE** | 50/465712 | 18626480 | 1 | 15 |  |
| server | 38 | `STARTING_BAN` | **OK_SAMPLE** | 50/5241 | 202449 | 1 | 9 |  |
| server | 39 | `STARTING_AVERAGE_POINTS` | **CLOSED** | 117/117 | 0 | 1 | 7 |  |
| server | 41 | `CURRENCY_RECORD` | **FAIL** | 0/173 | 74329 | 0 | 0 | row 0 flag=0x0 s19=0x14157f750 consumed=16 err=Invalid memory read (UC_ERR_READ_ |
| server | 42 | `STARTING_RETIREMENT` | **OK_SAMPLE** | 50/17721 | 459446 | 1 | 4 |  |
| server | 43 | `STARTING_MONTHLY_INSTALLMENT` | **CLOSED** | 535/535 | 0 | 1 | 7 |  |
| server | 45 | `STARTING_RECORD` | **FAIL** | 0/84477 | 7608725 | 0 | 0 | row 0 flag=0x0 s19=0x141544130 consumed=55 err=Invalid memory read (UC_ERR_READ_ |
| server | 46 | `STARTING_DRAFT_TRANSFER` | **CLOSED** | 7/7 | 0 | 1 | 6 |  |
| server | 47 | `LOCAL_REGION` | **OK_SAMPLE** | 50/2488 | 106773 | 2 | 20 |  |
| server | 48 | `STARTING_RECORD` | **FAIL** | 3/5210 | 445786 | 1 | 19 | row 3 flag=0x0 s19=0x141544130 consumed=55 err=Invalid memory read (UC_ERR_READ_ |
| server | 49 | `STARTING_PERSON_HISTORY` | **OK_SAMPLE** | 50/792149 | 28515564 | 1 | 4 |  |
| server | 50 | `STARTING_MLS_TRADED_SLOT` | **CLOSED** | 45/45 | 0 | 1 | 5 |  |
| server | 51 | `STARTING_MLS_GENERAL_ALLOCATION_MONEY` | **CLOSED** | 59/59 | 0 | 1 | 4 |  |
| server | 52 | `STARTING_PLAYER_HAPPINESS` | **CLOSED** | 0/0 | 0 | 0 | 0 |  |
| server | 56 | `AGREEMENT` | **CLOSED** | 6/6 | 0 | 1 | 1 |  |
| server | 57 | `FIXTURE_NAME` | **CLOSED** | 0/0 | 0 | 0 | 0 |  |
| server | 58 | `STARTING_WEEKLY_WAGE_CONTRIBUTION` | **CLOSED** | 8/8 | 0 | 1 | 6 |  |
| server | 59 | `STARTING_MEDIA_EXPECTATIONS` | **OK_SAMPLE** | 50/9079 | 223608 | 2 | 7 |  |
| server | 60 | `STARTING_MLS_TARGETED_ALLOCATION_MONEY` | **CLOSED** | 59/59 | 0 | 1 | 4 |  |
| server | 61 | `STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT` | **CLOSED** | 16/16 | 0 | 1 | 4 |  |
| server | 62 | `STARTING_RESERVE_TEAM` | **OK_SAMPLE** | 50/37214 | 1560888 | 1 | 12 |  |
| server | 63 | `STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER` | **CLOSED** | 2/2 | 0 | 1 | 4 |  |
| server | 64 | `STARTING_CLUB_STAFF_JOB_STATUS` | **OK_SAMPLE** | 50/6946 | 144816 | 1 | 5 |  |
| server | 65 | `STARTING_NEWGEN_PARAMETER` | **CLOSED** | 1417/1417 | 0 | 1 | 7 |  |
| server | 66 | `STARTING_CLUB_TRANSFER_PREFERENCE` | **CLOSED** | 753/753 | 0 | 1 | 6 |  |
| server | 67 | `STARTING_NEWGEN_PARAMETER` | **OK_SAMPLE** | 50/6826 | 210056 | 1 | 7 |  |
| server | 68 | `STARTING_NEWGEN_PARAMETER` | **CLOSED** | 138/138 | 0 | 1 | 7 |  |
| server | 69 | `STARTING_NEWGEN_PARAMETER` | **CLOSED** | 230/230 | 0 | 1 | 7 |  |
| server | 70 | `STARTING_VISION_OBJECTIVE` | **OK_SAMPLE** | 50/10075 | 401000 | 1 | 13 |  |
| server | 71 | `STARTING_PAST_TRANSFER` | **FAIL** | 9/616665 | 57460110 | 3 | 51 | row 9 flag=0x0 s19=0x141199440 consumed=29393 err=Unhandled CPU exception (UC_ER |
| server | 72 | `STARTING_PAST_TRADE` | **FAIL** | 0/138 | 9377 | 0 | 0 | row 0 flag=0x0 s19=0x14153f260 consumed=25 err=Invalid memory read (UC_ERR_READ_ |
| server | 73 | `STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT` | **CLOSED** | 1/1 | 0 | 1 | 4 |  |
| client | 0 | `AWARD` | **FAIL** | 1/3545 | 272923 | 1 | 28 | row 1 flag=0xc8 s19=0x140e48db0 consumed=25 err=Invalid memory read (UC_ERR_READ |
| client | 2 | `CITY` | **OK_SAMPLE** | 50/56293 | 2418449 | 1 | 10 |  |
| client | 3 | `CLUB` | **FAIL** | 12/84259 | 6861934 | 7 | 9 | row 12 flag=0x4d s19=0x140e5b1a0 consumed=30 err=Invalid memory write (UC_ERR_WR |
| client | 5 | `CONTINENT` | **CLOSED** | 7/7 | 0 | 1 | 14 |  |
| client | 6 | `INJURY` | **CLOSED** | 115/115 | 0 | 1 | 4 |  |
| client | 7 | `MEDIA_SOURCE` | **CLOSED** | 208/208 | 0 | 126 | 19 |  |
| client | 8 | `LANGUAGE` | **CLOSED** | 126/126 | 0 | 16 | 11 |  |
| client | 9 | `NATIONAL_TEAM_CONTAINER` | **CLOSED** | 251/251 | 0 | 92 | 46 |  |
| client | 10 | `NATION` | **CLOSED** | 251/251 | 0 | 44 | 25 |  |
| client | 18 | `DERBY` | **OK_SAMPLE** | 50/1567 | 135837 | 12 | 18 |  |
| client | 19 | `REGION` | **CLOSED** | 28/28 | 0 | 1 | 9 |  |
| client | 21 | `STADIUM` | **OK_SAMPLE** | 50/48413 | 1837794 | 1 | 9 |  |
| client | 22 | `STADIUM_CHANGE` | **CLOSED** | 449/449 | 0 | 1 | 1 |  |
| client | 23 | `STAGE_NAME` | **CLOSED** | 278/278 | 0 | 1 | 2 |  |
| client | 25 | `COMP` | **OK_SAMPLE** | 50/7047 | 888619 | 1 | 64 |  |
| client | 27 | `WEATHER` | **CLOSED** | 334/334 | 0 | 33 | 94 |  |
| client | 35 | `PLAYER_TYPE` | **CLOSED** | 890/890 | 0 | 1 | 3 |  |
| client | 41 | `CURRENCY_RECORD` | **CLOSED** | 173/173 | 0 | 81 | 8 |  |
| client | 47 | `LOCAL_REGION` | **OK_SAMPLE** | 50/2488 | 106773 | 2 | 20 |  |
| client | 56 | `AGREEMENT` | **CLOSED** | 6/6 | 0 | 1 | 1 |  |
