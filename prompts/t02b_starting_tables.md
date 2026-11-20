# t02-b 任务书:33 个 STARTING_* 无名直线型实体 —— 项目最大空白区

> 交给 pi devseek(deepseek-v4.1-flash-free)。这批表**从未被解析过**:它们在 server_db.dat 里真实存在、驱动游戏开局逻辑,但不在 editor 的 property_map 里(editor 不可编辑),所以历史工作全部跳过了它们。
> 规则:只读输入、不启动游戏/编辑器/IDA、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 先读方法论(照抄,勿重新发明)

- `scratch/t01/inbox/t01l/REPORT.md` —— weat/table_27(89 字段):行框架 + 固定循环 + 4CC 范围跳表
- `scratch/t01/inbox/t01m/REPORT.md` —— stad/table_21(16 字段):client/server 双行宽 + 旧库 L1 双源互证
- `scratch/t01/inbox/t01h/output.json` —— 74 项全 census(本批每张表的 handler/alloc/reader 入口都在里面)

核心五步:解压 archive 成员 → 行框架封口(count/行起/stride) → reader 宽度累加(`mov r8d,N` + `lea reg,[rbx+disp]`) → getter 4CC 对齐(全寄存器 `81 f8..ff` + `3d`;4CC 小端作 imm32) → 5 行抽验。

## 与 t02a 的关键区别

这些实体**没有 editor schema 码表**。所以:
- **字段语义没有现成 4CC 名单** —— 但 getter 里仍会有 `cmp r32,imm32` 的 4CC 字面量,把它们**照原字节记录下来**就是字段标识(如 `Pdob` 这种)。不要因为是"未知名"就跳过
- RTTI 类名 + reader 字段顺序 + 宽度组合,可以用来**推断**语义(如 `STARTING_INJURY` 的 5 个字段大概率是 person_ref/injury_type/date_from/date_to/severity)。**推断必须标注为 candidate,不能写成结论**
- 验收以**位置与宽度**为准(第 n 个字段在 row+X 宽 W 字节),语义命名是加分项

## 本批 33 张表(按宽度指令数从小到大,建议顺序)

| type | RTTI 类 | 宽度指令数 |
|---:|---|---:|
| 31 | STARTING_CONFIDENCE | 4 |
| 51 | STARTING_MLS_GENERAL_ALLOCATION_MONEY | 4 |
| 60 | STARTING_MLS_TARGETED_ALLOCATION_MONEY | 4 |
| 73 | STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT | 4 |
| 46 | STARTING_DRAFT_TRANSFER | 5 |
| 50 | STARTING_MLS_TRADED_SLOT | 5 |
| 52 | STARTING_PLAYER_HAPPINESS | 5 |
| 57 | FIXTURE_NAME | 5 |
| 64 | STARTING_CLUB_STAFF_JOB_STATUS | 5 |
| 66 | STARTING_CLUB_TRANSFER_PREFERENCE | 5 |
| 43 | STARTING_MONTHLY_INSTALLMENT | 6 |
| 38 | STARTING_BAN | 8 |
| 65 | STARTING_NEWGEN_PARAMETER | 8 |
| 67 | STARTING_NEWGEN_PARAMETER | 8 |
| 68 | STARTING_NEWGEN_PARAMETER | 8 |
| 69 | STARTING_NEWGEN_PARAMETER | 8 |
| 30 | STARTING_INJURY | 9 |
| 62 | STARTING_RESERVE_TEAM | 11 |
| 34 | STARTING_TEAM_CUP_HISTORY | 12 |
| 61 | STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT | 12 |
| 63 | STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER | 12 |
| 70 | STARTING_VISION_OBJECTIVE | 12 |
| 42 | STARTING_RETIREMENT | 14 |
| 29 | STARTING_LOAN | 15 |
| 37 | STARTING_TEAM_LEAGUE_HISTORY | 15 |
| 45 | STARTING_RECORD | 17 |
| 48 | STARTING_RECORD | 17 |
| 26 | COMP_HISTORY_RECORD | 19 |
| 33 | STARTING_CLUB_DEBT | 19 |
| 58 | STARTING_WEEKLY_WAGE_CONTRIBUTION | 20 |
| 12 | STARTING_AWARD_HISTORY | 25 |
| 49 | STARTING_PERSON_HISTORY | 32 |
| 22 | STADIUM_CHANGE | 45 |

**注意别名**:45/48 同为 STARTING_RECORD,65/67/68/69 同为 STARTING_NEWGEN_PARAMETER(t01h 记录为 handler 别名)——同一实体多个 type-id 时,只解一次,然后在报告里注明"N 个 type-id 共用"。

## 分批纪律(重要)

**不要一次做 33 张。** 按顺序做,**每完成 8 张就落盘一次**(写 output.json + REPORT.md 追加),然后继续。这样即使中途掉线,已完成的部分可验收。

优先级:宽度少的先做。**做到第 20 张时间不够就停,如实报告进度。**

## 验收判据

- **至少 20 张表**各给出:行框架(count/行起/stride 或变长公式,总量封口)+ 全部字段的位置与宽度 + ≥3 行抽验
- 字段数少的表(4-5 宽度)应做到 100% 覆盖,不许留半成品
- 语义命名尽量给,但必须标 `candidate`
- 身份块:行末 12B 是否 `ordinal|ID|重复ID`(五张表已验证此惯例),成立就记,不成立如实说

## 交付

`scratch/t02/inbox/b/`:
- `output.json` —— 按 type-id 分键:`{rtti, aliases, row_framework, row_offset_map[{idx,row_off,width,object_off,getter_cmp_hex,semantic_candidate}], identity_block, samples, unclosed}`
- `REPORT.md` —— 每表 ≤12 行
- `verify.py --selftest` —— 只读,重跑行框架封口 + 抽验 + 静态字节,含负对照

## 纪律

- **不改任何目录外文件**(账本/晨报/t01 产物一律不动)
- 每表 15 分钟上限;卡住就记录状态跳过
- 候选不写成结论;宁可诚实少,不要凑数
- 完成后打印:成功几张、每张几个字段、哪几张卡住及原因
