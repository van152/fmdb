# t15d 任务书:D-锚-only 表的数据侧抽查(轻量)

先读 [AGENTS.md](../AGENTS.md)。t14 的 stage2_map 有 54 张 resolved,其中一批**只有 RTTI D 锚、没有 A/B 类**。t15 已覆盖 10 张(26/29/30/32/36/38/39/45/48/49),你抽查剩下里面挑得出的 12 张。

## 环境

数据已本地化:`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`(已设)。**不许读 Z:。**

## 抽查对象(从 stage2_map 挑,建议这批,可按数据可得性替换)

`42(STARTING_RETIREMENT)` `43(STARTING_MONTHLY_INSTALLMENT)` `46(STARTING_DRAFT_TRANSFER)` `50(STARTING_MLS_TRADED_SLOT)` `51(STARTING_MLS_GENERAL_ALLOCATION_MONEY)` `58(STARTING_WEEKLY_WAGE_CONTRIBUTION)` `62(STARTING_RESERVE_TEAM)` `64(STARTING_CLUB_STAFF_JOB_STATUS)` `66(STARTING_CLUB_TRANSFER_PREFERENCE)` `70(STARTING_VISION_OBJECTIVE)` `37(STARTING_TEAM_LEAGUE_HISTORY)` `34(STARTING_TEAM_CUP_HISTORY)`

每张做轻量画像:`--limit 2000` 级别的抽样导出就够,**不要全量 dump**(52/57 空表跳过;行数见 COVERAGE.json)。

## 判据(每张表给一句)

类名语义 ↔ 列画像是否自洽:
- 引用列落进谁的 ID 空间(person 658,011 / club 84,259 / team 84,507 / comp 7,047 / injury 115)?
- 有没有明显的"金额/日期/枚举"列与类名语义对得上(如 WEEKLY_WAGE 应见钱样数值)?
- 值域法边界(E42)继续有效:只给 `plausible | implausible | silent`,**不许据此升降实体裁决**——那是晨裁的事。

## 纪律

- 只写 `scratch/t15d/out/`;py -V:3.12 -I;脚本 --help/--selftest;退出码 0/1/2。
- 输出预算:单次写盘 ≤300 行;单表 CSV 只留抽样 ≤2000 行。
- 每张限时 2 分钟,超时就标 silent 跳过;整体 25 分钟做不完落盘 partial。

## 交付(scratch/t15d/out/)

1. `dspot.json` —— 逐表 `{"table_type","rtti_class","verdict":"plausible|implausible|silent","evidence":"一句话+关键数字"}`,顶层 status
2. `dspot.md` —— 人读表
