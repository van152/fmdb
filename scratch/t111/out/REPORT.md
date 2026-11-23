# t111 — Unicorn 最后 11 张表修复报告 (冲刺 79/79)

- 耗时: `110.3s` | 本轮结果: **整表 `diff==0` 闭合 45** | 大表样本干净 33 | 失败 1 / 共 79 对
- **总进度: t96c 基线 68/79 干净 (41 CLOSED + 27 OK_SAMPLE + 11 FAIL) → t111 78/79 干净 (45 CLOSED + 33 OK_SAMPLE + 1 FAIL)**
- 修复根因: **R1** dbctx 全局家族 (0x141B5FDB0-FE60 簇 + 0x141BF7E10 ← db_a3 空向量页) · **R2** 版本全局 (0x141B60330/32/34 ← 0x0DF1) · **R3** OBJ/CTX 隔离区 (ctx+0x588 不再被 blob 覆写) · **R4** 行切片止于 footer · **R5** 内部堆回退分配器拦截 (t72 div/0) · **R6** t72 流标志 bit1 + 配置全局 (15B 元素布局)

## 11 对目标表 修复前后对比

| pair | class | t96c 基线 | t111 结果 | rows | diff | 根因 |
|---|---|---|---|---|---:|---|
| server/t0 | `AWARD` | FAIL 1/3545 row 1 flag=0xc8 rip=0x140f92cc4 addr=0x80 | **OK_SAMPLE** | 3545/3545 | 163691 | R1 |
| client/t0 | `AWARD` | FAIL 1/3545 row 1 flag=0xc8 rip=0x140f92cc4 addr=0x80 | **OK_SAMPLE** | 3545/3545 | 163691 | R1 |
| server/t3 | `CLUB` | FAIL 3/84259 row 3 huge_read n=104418048 rip=0x14371be8d | **FAIL** | 20/84259 (target 200) | 15927552 | R3 |
| client/t3 | `CLUB` | FAIL 12/84259 row 12 flag=0x4d huge_read rip=0x14371be8d | **OK_SAMPLE** | 200/84259 (target 200) | 506194 | R3 |
| server/t32 | `STARTING_FUTURE_TRANSFER` | FAIL 1/315 row 1 pos 19111 >= footer 19103 (diff=-8) | **CLOSED** | 315/315 | 0 | R2+R4 |
| server/t36 | `STARTING_MANAGER_HOF_RECORD` | FAIL 1/6535 row 1 consumed=18 UC_ERR_READ_UNMAPPED rip=0x14371bf6e | **OK_SAMPLE** | 200/6535 (target 200) | 545509 | R3 |
| server/t41 | `CURRENCY_RECORD` | FAIL 0/173 row 0 consumed=16 UC_ERR_READ_UNMAPPED rip=0x14371bf6e | **CLOSED** | 173/173 | 0 | R3 |
| server/t45 | `STARTING_RECORD` | FAIL 0/84477 row 0 consumed=55 UC_ERR_READ_UNMAPPED rip=0x14371bf6e | **OK_SAMPLE** | 200/84477 (target 200) | 7589645 | R3 |
| server/t48 | `STARTING_RECORD` | FAIL 3/5210 row 3 consumed=55 UC_ERR_READ_UNMAPPED rip=0x14371bf6e | **CLOSED** | 5210/5210 | 0 | R3 |
| server/t71 | `STARTING_PAST_TRANSFER` | FAIL 9/616665 row 9 consumed=29393 _Xlength_error rip=0x141d19401 | **OK_SAMPLE** | 50/616665 (target 50) | 57475694 | R2+R4 |
| server/t72 | `STARTING_PAST_TRADE` | FAIL 0/138 row 0 rip=0x140f83b02 addr=0x80 | **CLOSED** | 138/138 | 0 | R1+R5+R6 |

## 全表结果 (本轮)

| archive | tt | class | 状态 | rows_ok/total | diff | uniq_lens | fields | 备注 |
|---|---:|---|---|---:|---:|---:|---:|---|
| server | 0 | `AWARD` | **OK_SAMPLE** | 3545/3545 | 163691 | 8 | 47 |  |
| server | 2 | `CITY` | **OK_SAMPLE** | 50/56293 | 2418449 | 1 | 10 |  |
| server | 3 | `CLUB` | **FAIL** | 20/84259 | 15927552 | 7 | 30 | row 20 flag=0x1 s19=0x140e5b1a0 consumed=203176 err=Unhandled CPU exception (UC_ |
| server | 5 | `CONTINENT` | **CLOSED** | 7/7 | 0 | 1 | 16 |  |
| server | 6 | `INJURY` | **CLOSED** | 115/115 | 0 | 1 | 22 |  |
| server | 7 | `MEDIA_SOURCE` | **CLOSED** | 208/208 | 0 | 126 | 29 |  |
| server | 8 | `LANGUAGE` | **CLOSED** | 126/126 | 0 | 16 | 11 |  |
| server | 9 | `NATIONAL_TEAM_CONTAINER` | **CLOSED** | 251/251 | 0 | 211 | 188 |  |
| server | 10 | `NATION` | **CLOSED** | 251/251 | 0 | 195 | 63 |  |
| server | 12 | `STARTING_AWARD_HISTORY` | **OK_SAMPLE** | 50/28597 | 3733429 | 16 | 30 |  |
| server | 18 | `DERBY` | **OK_SAMPLE** | 50/1567 | 144939 | 12 | 27 |  |
| server | 19 | `REGION` | **CLOSED** | 28/28 | 0 | 1 | 10 |  |
| server | 21 | `STADIUM` | **OK_SAMPLE** | 50/48413 | 8753703 | 1 | 74 |  |
| server | 22 | `STADIUM_CHANGE` | **CLOSED** | 449/449 | 0 | 1 | 20 |  |
| server | 23 | `STAGE_NAME` | **CLOSED** | 278/278 | 0 | 1 | 2 |  |
| server | 24 | `NATIONAL_TEAM` | **OK_SAMPLE** | 50/84507 | 1265220 | 22 | 41 |  |
| server | 25 | `COMP` | **OK_SAMPLE** | 50/7047 | 1516130 | 25 | 106 |  |
| server | 26 | `COMP_HISTORY_RECORD` | **OK_SAMPLE** | 50/90128 | 6215382 | 1 | 19 |  |
| server | 27 | `WEATHER` | **CLOSED** | 334/334 | 0 | 33 | 28 |  |
| server | 29 | `STARTING_LOAN` | **OK_SAMPLE** | 50/13278 | 992700 | 1 | 18 |  |
| server | 30 | `STARTING_INJURY` | **OK_SAMPLE** | 50/72473 | 2462382 | 1 | 10 |  |
| server | 31 | `STARTING_CONFIDENCE` | **OK_SAMPLE** | 50/37283 | 781893 | 1 | 4 |  |
| server | 32 | `STARTING_FUTURE_TRANSFER` | **CLOSED** | 315/315 | 0 | 3 | 18 |  |
| server | 33 | `STARTING_CLUB_DEBT` | **OK_SAMPLE** | 50/32409 | 2556361 | 1 | 20 |  |
| server | 34 | `STARTING_TEAM_CUP_HISTORY` | **OK_SAMPLE** | 50/7115 | 310860 | 1 | 12 |  |
| server | 35 | `PLAYER_TYPE` | **CLOSED** | 890/890 | 0 | 1 | 3 |  |
| server | 36 | `STARTING_MANAGER_HOF_RECORD` | **OK_SAMPLE** | 200/6535 | 545509 | 60 | 16 |  |
| server | 37 | `STARTING_TEAM_LEAGUE_HISTORY` | **OK_SAMPLE** | 50/465712 | 18626480 | 1 | 15 |  |
| server | 38 | `STARTING_BAN` | **OK_SAMPLE** | 50/5241 | 202449 | 1 | 9 |  |
| server | 39 | `STARTING_AVERAGE_POINTS` | **CLOSED** | 117/117 | 0 | 1 | 7 |  |
| server | 41 | `CURRENCY_RECORD` | **CLOSED** | 173/173 | 0 | 81 | 14 |  |
| server | 42 | `STARTING_RETIREMENT` | **OK_SAMPLE** | 50/17721 | 459446 | 1 | 4 |  |
| server | 43 | `STARTING_MONTHLY_INSTALLMENT` | **CLOSED** | 535/535 | 0 | 1 | 7 |  |
| server | 45 | `STARTING_RECORD` | **OK_SAMPLE** | 200/84477 | 7589645 | 17 | 18 |  |
| server | 46 | `STARTING_DRAFT_TRANSFER` | **CLOSED** | 7/7 | 0 | 1 | 6 |  |
| server | 47 | `LOCAL_REGION` | **OK_SAMPLE** | 50/2488 | 106773 | 2 | 20 |  |
| server | 48 | `STARTING_RECORD` | **CLOSED** | 5210/5210 | 0 | 28 | 18 |  |
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
| server | 71 | `STARTING_PAST_TRANSFER` | **OK_SAMPLE** | 50/616665 | 57475694 | 5 | 28 |  |
| server | 72 | `STARTING_PAST_TRADE` | **CLOSED** | 138/138 | 0 | 10 | 17 |  |
| server | 73 | `STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT` | **CLOSED** | 1/1 | 0 | 1 | 4 |  |
| client | 0 | `AWARD` | **OK_SAMPLE** | 3545/3545 | 163691 | 8 | 47 |  |
| client | 2 | `CITY` | **OK_SAMPLE** | 50/56293 | 2418449 | 1 | 10 |  |
| client | 3 | `CLUB` | **OK_SAMPLE** | 200/84259 | 506194 | 63 | 10 |  |
| client | 5 | `CONTINENT` | **CLOSED** | 7/7 | 0 | 1 | 14 |  |
| client | 6 | `INJURY` | **CLOSED** | 115/115 | 0 | 1 | 4 |  |
| client | 7 | `MEDIA_SOURCE` | **CLOSED** | 208/208 | 0 | 126 | 25 |  |
| client | 8 | `LANGUAGE` | **CLOSED** | 126/126 | 0 | 16 | 11 |  |
| client | 9 | `NATIONAL_TEAM_CONTAINER` | **CLOSED** | 251/251 | 0 | 92 | 46 |  |
| client | 10 | `NATION` | **CLOSED** | 251/251 | 0 | 44 | 25 |  |
| client | 18 | `DERBY` | **OK_SAMPLE** | 50/1567 | 135837 | 12 | 24 |  |
| client | 19 | `REGION` | **CLOSED** | 28/28 | 0 | 1 | 9 |  |
| client | 21 | `STADIUM` | **OK_SAMPLE** | 50/48413 | 1837794 | 1 | 9 |  |
| client | 22 | `STADIUM_CHANGE` | **CLOSED** | 449/449 | 0 | 1 | 1 |  |
| client | 23 | `STAGE_NAME` | **CLOSED** | 278/278 | 0 | 1 | 2 |  |
| client | 25 | `COMP` | **OK_SAMPLE** | 50/7047 | 888619 | 1 | 47 |  |
| client | 27 | `WEATHER` | **CLOSED** | 334/334 | 0 | 33 | 28 |  |
| client | 35 | `PLAYER_TYPE` | **CLOSED** | 890/890 | 0 | 1 | 3 |  |
| client | 41 | `CURRENCY_RECORD` | **CLOSED** | 173/173 | 0 | 81 | 14 |  |
| client | 47 | `LOCAL_REGION` | **OK_SAMPLE** | 50/2488 | 106773 | 2 | 20 |  |
| client | 56 | `AGREEMENT` | **CLOSED** | 6/6 | 0 | 1 | 1 |  |
