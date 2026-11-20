# t14 RTTI 构造锚普查与阶段二全图

状态：`complete`。server 表 59 张；resolved 54、candidate 3、negative 0、empty 2。

## 方法与交叉检查

- factory 跳表由 `0xF49D38 + signed_rel32@ (0xF49D38 + 4*t)` 从 editor.exe 原字节复算；RTTI 使用相对 RVA 的 COL，地址映射经 `scripts/t05_pe.py`。
- dedicated 63/63 类型全部有类名；default 11/11。fm.exe TD 字符串缺失类：0；可确认的均记为 `td-only`（未声称 vtable/ref 交叉）。
- 8 个指定实体交叉：0 AWARD、2 CITY、8 LANGUAGE、18 DERBY、19 REGION、23 STAGE_NAME、27 WEATHER、56 AGREEMENT；均与跳表 RTTI 主类零矛盾。
- E56/RTTI 冲突不强行裁决；class tag 不明确时保留 candidate；count 本身不作实体锚。52/57 保留 empty。

## 逐表结论（COVERAGE server 59 张）

| type | count | entity_tag | status | RTTI primary class | D / other evidence |
|---:|---:|---|---|---|---|
| 0 | 3545 | awar | resolved | AWARD | A, D |
| 2 | 56293 | city | resolved | CITY | A, D |
| 3 | 84259 | club | resolved | LEAGUE_BODY_CLUB | A, D |
| 5 | 7 | cont | resolved | CONTINENT | A, D |
| 6 | 115 | inju | resolved | INJURY | A, D |
| 7 | 208 | mdso | resolved | MEDIA_SOURCE | A, D |
| 8 | 126 | lang | resolved | LANGUAGE | A, D |
| 9 | 251 | nati | resolved | NATIONAL_TEAM_CONTAINER | A, D |
| 10 | 251 | nati | resolved | NATION | A, D |
| 12 | 28597 | awar | resolved | STARTING_AWARD_HISTORY | A, D |
| 18 | 1567 | drbr | resolved | DERBY | A, D |
| 19 | 28 | regi | resolved | REGION | A, D |
| 21 | 48413 | stad | resolved | STADIUM | A, D |
| 22 | 449 | — | candidate | STADIUM_CHANGE | A, D |
| 23 | 278 | stgn | resolved | STAGE_NAME | A, D |
| 24 | 84507 | team | resolved | NATIONAL_TEAM | A, D |
| 25 | 7047 | comp | resolved | COMP | A, D |
| 26 | 90128 | comp | resolved | COMP_HISTORY_RECORD | D |
| 27 | 334 | weat | resolved | WEATHER | A, D |
| 29 | 13278 | pers | resolved | STARTING_LOAN | D |
| 30 | 72473 | play | resolved | STARTING_INJURY | A, D |
| 31 | 37283 | play | resolved | STARTING_CONFIDENCE | D |
| 32 | 315 | pers | resolved | STARTING_FUTURE_TRANSFER | D |
| 33 | 32409 | club | resolved | STARTING_CLUB_DEBT | A, D |
| 34 | 7115 | club | resolved | STARTING_TEAM_CUP_HISTORY | B, D |
| 35 | 890 | — | candidate | PLAYER_TYPE | A, D |
| 36 | 6535 | pers | resolved | STARTING_MANAGER_HOF_RECORD | D |
| 37 | 465712 | club | resolved | STARTING_TEAM_LEAGUE_HISTORY | A, D |
| 38 | 5241 | pers | resolved | STARTING_BAN | D |
| 39 | 117 | team | resolved | STARTING_AVERAGE_POINTS | D |
| 41 | 173 | curr | resolved | CURRENCY_RECORD | A, D |
| 42 | 17721 | pers | resolved | STARTING_RETIREMENT | D |
| 43 | 535 | club | resolved | STARTING_MONTHLY_INSTALLMENT | B, D |
| 45 | 84477 | pers | resolved | STARTING_RECORD | A, D |
| 46 | 7 | pers | resolved | STARTING_DRAFT_TRANSFER | D |
| 47 | 2488 | lcrg | resolved | LOCAL_REGION | A, D |
| 48 | 5210 | pers | resolved | STARTING_RECORD | A, D |
| 49 | 792149 | pers | resolved | STARTING_PERSON_HISTORY | A, D |
| 50 | 45 | club | resolved | STARTING_MLS_TRADED_SLOT | D |
| 51 | 59 | club | resolved | STARTING_MLS_GENERAL_ALLOCATION_MONEY | D |
| 52 | 0 | — | empty | STARTING_PLAYER_HAPPINESS | A |
| 56 | 6 | agrm | resolved | AGREEMENT | A, D |
| 57 | 0 | — | empty | FIXTURE_NAME | A |
| 58 | 8 | — | candidate | STARTING_WEEKLY_WAGE_CONTRIBUTION | D |
| 59 | 9079 | play | resolved | STARTING_MEDIA_EXPECTATIONS | D |
| 60 | 59 | club | resolved | STARTING_MLS_TARGETED_ALLOCATION_MONEY | D |
| 61 | 16 | club | resolved | STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT | D |
| 62 | 37214 | club | resolved | STARTING_RESERVE_TEAM | D |
| 63 | 2 | club | resolved | STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER | D |
| 64 | 6946 | club | resolved | STARTING_CLUB_STAFF_JOB_STATUS | D |
| 65 | 1417 | pers | resolved | STARTING_NEWGEN_PARAMETER | D |
| 66 | 753 | club | resolved | STARTING_CLUB_TRANSFER_PREFERENCE | D |
| 67 | 6826 | pers | resolved | STARTING_NEWGEN_PARAMETER | D |
| 68 | 138 | pers | resolved | STARTING_NEWGEN_PARAMETER | D |
| 69 | 230 | pers | resolved | STARTING_NEWGEN_PARAMETER | D |
| 70 | 10075 | club | resolved | STARTING_VISION_OBJECTIVE | D |
| 71 | 616665 | pers | resolved | STARTING_PAST_TRANSFER | D |
| 72 | 138 | pers | resolved | STARTING_PAST_TRADE | D |
| 73 | 1 | play | resolved | STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT | D |

## 六张 t13 negative 表的正式裁决

以下旧负结果按原字段保留；新 D 锚只作为后续证据，不改写旧结论。拒绝候选理由也逐字包含。

### type 26: `comp` / resolved — D `COMP_HISTORY_RECORD`

原 `why_unresolved`（原文）：

> 负结果：scratch/t05/reader_widths.json 中 type 26 的 seq=[12]、obj_seq=[null]，没有可关联到 schema 字段的成员偏移；scratch/t08/out/chains.json 的邻近链未提供与该 reader 相连的唯一 df=1 字段码。闭合行数据虽可读，当前未找到独立 A/B/C 锚点；不以候选硬定实体。

> 原拒绝 `club`：与独立已知 club 基数 84,259（server table_3）相差 5,869 / 6.97%；reader 只有 12-byte opaque call、没有 object_off，邻近 4CC 链也无与该 reader 成员相连的唯一 schema 码。数量接近不足以作锚。

新裁决：handler `0xf49143` → COMP_HISTORY_RECORD; RTTI D tag `comp`。数量线索未作为锚。

### type 29: `pers` / resolved — D `STARTING_LOAN`

原 `why_unresolved`（原文）：

> 负结果：type 29 的 reader_widths 只有一个 12-byte call 且无 object_off；邻近 player 码簇仅是位置候选，不能按邻近投票定案。现有工件没有独立的 4CC、独立基数或已验证 ID 域锚点。

> 原拒绝 `player`：reader 附近可见 player 字段码簇，但 type 29 reader 的 obj_seq=[null]，不能证明这些码属于本表 reader；最近候选链距离不构成成员映射。与 comp 7,047 行相差 6,231 / 88.42%，也不支持基数锚。

新裁决：handler `0xf492de` → STARTING_LOAN; RTTI D tag `pers`。数量线索未作为锚。

### type 32: `pers` / resolved — D `STARTING_FUTURE_TRANSFER`

原 `why_unresolved`（原文）：

> 负结果：type 32 为变长 count-loop 行，reader_widths 的 obj_seq=[null]；邻近链中没有能与本 reader 直接关联的唯一 df=1 schema 字段。weather 334 对 315 的差异不能单独定案，未找到其他独立锚点。

> 原拒绝 `weather`：独立已知 weather 为 334 行（scratch/t05/COVERAGE.json，client table_27）；差 19 / 5.69%。该差距只是数量线索，未达到可独立定案的基数吻合，且 reader 无可关联到该表的唯一 schema 4CC。

新裁决：handler `0xf493f1` → STARTING_FUTURE_TRANSFER; RTTI D tag `pers`。数量线索未作为锚。

### type 36: `pers` / resolved — D `STARTING_MANAGER_HOF_RECORD`

原 `why_unresolved`（原文）：

> 负结果：type 36 的行边界已闭合，但 reader_widths 只有 object_off 24、64 两个无语义的 4-byte 访问；周边 injury/player 码簇未出现与该 reader 成员可复核的唯一字段锚。comp 基数差 7.27%，不作硬配。

> 原拒绝 `comp`：独立已知 comp 为 7,047 行（scratch/t05/COVERAGE.json，server table_25）；差 512 / 7.27%。type 36 reader 仅有两个 4-byte calls，无法据此识别实体；差值本身不是 B 锚。

> 原拒绝 `injury/person`：样本中的可读姓名或日期外观没有 schema 唯一码/已验证 ID 空间配合，语义不足以排除其它实体。

新裁决：handler `0xf49543` → STARTING_MANAGER_HOF_RECORD; RTTI D tag `pers`。数量线索未作为锚。

### type 38: `pers` / resolved — D `STARTING_BAN`

原 `why_unresolved`（原文）：

> 负结果：type 38 的 7 个 reader object_off 只能给出结构位置；最近链候选码经 schema_inventory 去重后均不是唯一实体码，值域也未形成有语义来源且哨兵/fill 同时吻合的 C 锚。

> 原拒绝 `language`：独立已知 language 为 126 行（scratch/t05/COVERAGE.json，server table_8）；本表多 5,115 / 4,059.52%，不吻合。邻近 4CC 码均跨实体共享，不能作 A 锚。

> 原拒绝 `club/comp/player`：邻近链中的 club、comp、nati、endt、type 均跨实体出现；没有 df=1 码与本表 reader 成员形成独立对应。

新裁决：handler `0xf495af` → STARTING_BAN; RTTI D tag `pers`。数量线索未作为锚。

### type 39: `team` / resolved — D `STARTING_AVERAGE_POINTS`

原 `why_unresolved`（原文）：

> 负结果：117 行与 injury 的 115 行接近但不相等；type 39 的混合 reader 有 null object_off，邻近链接的代码簇未建立到本表的唯一 schema 字段关系。没有独立值域锚，保留 injury 为已拒绝的数量候选。

> 原拒绝 `injury`：独立已知 injury 为 115 行（scratch/t05/COVERAGE.json，client table_6）；差 2 / 1.74%。仅有数量接近，reader 成员码不提供 injury 专属 4CC，故不当作 B 锚。

新裁决：handler `0xf49608` → STARTING_AVERAGE_POINTS; RTTI D tag `team`。数量线索未作为锚。

## E56 十二张候选表裁决

| type | E56 entity/status | D class/tag | t14 status | 结论 |
|---:|---|---|---|---|
| 22 | club / resolved | STADIUM_CHANGE / stad | candidate | 冲突：STADIUM_CHANGE vs club；保守 candidate |
| 30 | player / resolved | STARTING_INJURY / play | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 31 | — / negative | STARTING_CONFIDENCE / play | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 34 | club / candidate | STARTING_TEAM_CUP_HISTORY / club | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 37 | club / resolved | STARTING_TEAM_LEAGUE_HISTORY / club | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 42 | — / negative | STARTING_RETIREMENT / pers | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 43 | club / candidate | STARTING_MONTHLY_INSTALLMENT / club | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 46 | — / negative | STARTING_DRAFT_TRANSFER / pers | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 49 | person / resolved | STARTING_PERSON_HISTORY / pers | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 50 | — / negative | STARTING_MLS_TRADED_SLOT / club | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 51 | — / negative | STARTING_MLS_GENERAL_ALLOCATION_MONEY / club | resolved | D 与 E56 同向或 D 独立补足；resolved |
| 58 | — / candidate | STARTING_WEEKLY_WAGE_CONTRIBUTION / club | candidate | E56 保留 person/club 两解；D 未消歧，保留 candidate |

## 冲突清单

- type 22: D class STADIUM_CHANGE maps to stad, conflicting with independent entity club
- type 26: Historical negative preserved verbatim; new D evidence is a later independent adjudication.
- type 29: Historical negative preserved verbatim; new D evidence is a later independent adjudication.
- type 32: Historical negative preserved verbatim; new D evidence is a later independent adjudication.
- type 35: D class PLAYER_TYPE maps to play, conflicting with independent entity dscr
- type 36: Historical negative preserved verbatim; new D evidence is a later independent adjudication.
- type 38: Historical negative preserved verbatim; new D evidence is a later independent adjudication.
- type 39: Historical negative preserved verbatim; new D evidence is a later independent adjudication.
- type 58: E56 leaves person/club open; weekly-wage class does not independently identify its owning entity.

## RTTI census 缺口 / class-family 裁决

- 63 个 dedicated 类型均有至少一个通过 COL→TD 自洽校验的类名；17/18/20/28/40 等 default 表仍按默认 handler 标记，不当作 dedicated 缺失。
- 非 schema 主实体/特殊记录名按 class-family 映射时以 schema entity tag 为目标；`STARTING_RECORD`、`FIXTURE_NAME` 等泛型类不单独决定 entity，依赖既有 A 锚或保持 candidate。
- handler alias 需谨慎解释：45/48 共用 `0xf48ba6`；65/67/68/69 共用 `0xf48b55`。这些 D 锚只证明共享构造类，不宣称 RTTI 单独区分同 handler 的表；身份分辨沿用对应独立表证据/dispatch table_type。
- 35 的旧 E22 entity=`dscr` 与 RTTI `PLAYER_TYPE`→`play` 冲突；22 的 E56 `club` 与 RTTI `STADIUM_CHANGE`→`stad` 冲突；两者均未写成 resolved。
- 52、57 的 handler RTTI 不改变 COVERAGE 中 0 行的 empty 判决。

## 验证状态

运行：`py -V:3.12 -I scratch/t14/out/verify.py --help`、`--selftest`、默认全量验证。
当前 stage2 resolved=54/59（验收线 ≥45）；census dedicated 命名=63/63；fm TD 缺失=0。
