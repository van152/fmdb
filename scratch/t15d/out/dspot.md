# t15d 抽查汇总(t15e 收尾)

判据:`prompts/t15d_dspot.md` —— 类名语义 ↔ 列画像(ID 空间 / 金额 / 日期)是否自洽。
只给 `plausible | implausible | silent`,**不据此升降实体裁决**(E42 边界仍有效)。

参照 ID 空间:person 658,011 / club 84,259 / team 84,507 / comp 7,047 / injury 115。

数据来源全部为 `scratch/t15d/out/` 既有产物(`measure.json`、`prof/f*.json`、`prof/p*.json`、`grid/*.txt`、`fk_hits.json`),**未重跑任何导出**。

## 结果总表

| table_type | rtti_class | 行数 | verdict | 关键数字 |
|---:|---|---:|---|---|
| 34 | STARTING_TEAM_CUP_HISTORY | 7,115 | plausible | u32@0 低 16 位落 comp 域 0.9956(d_lo=89);起止年 0..2023 |
| 37 | STARTING_TEAM_LEAGUE_HISTORY | 465,712 | plausible | comp 0..7044 全落 7,047;team 51..84,481 全落 84,507;积分 0..330 |
| 42 | STARTING_RETIREMENT | 17,721 | plausible | person duni 命中 100%,d=16,756,lift=3,092;YMD 命中 1.0 |
| 43 | STARTING_MONTHLY_INSTALLMENT | 535 | plausible | person duni 533/533(lift=3,176);月数 2..84;金额 1,041..3,861,111 |
| 46 | STARTING_DRAFT_TRANSFER | 7 | silent | 引用列 1,907..72,052,048 不落任何 ID 空间;表仅 7 行 |
| 50 | STARTING_MLS_TRADED_SLOT | 45 | silent | low16 判据在 club 基准 >65,535 时失效;无金额列,日期 d=3~4 |
| 51 | STARTING_MLS_GENERAL_ALLOCATION_MONEY | 59 | plausible | 金额 1,520,812..2,241,197(d=3);YMD 1.0;year 2021..2024 |
| 58 | STARTING_WEEKLY_WAGE_CONTRIBUTION | 8 | plausible | person duni 8/8(lift=226.5);周薪样 603..1,871 / 658..1,733 / 1,400..38,800 |
| 62 | STARTING_RESERVE_TEAM | 37,214 | plausible | u32@1 全行 ≤84,258,正好压在 club 基准上界 |
| 64 | STARTING_CLUB_STAFF_JOB_STATUS | 6,946 | plausible | u32@0 = 11..82,188(753 个 club);job_type 枚举 d=67 |
| 66 | STARTING_CLUB_TRANSFER_PREFERENCE | 753 | silent | person duni 仅 7.7% 行命中;无 club/team 引用列、无 0..20 偏好档 |
| 70 | STARTING_VISION_OBJECTIVE | 10,075 | silent | person duni 1.19% / 5.36%(lift 79 / 356);其余为高位带标记复合值 |

**合计 12 张:plausible 8 / implausible 0 / silent 4**

## 逐表说明

### plausible(8)

- **34 CUP_HISTORY** — comp 锚点成立:`u32@0` 低 16 位 99.56% 落在 0..7,046(基准 7,047),另有 `u16@8`/`u16@10` 起止年 0..2023(d=110)。杯赛历史 = (comp, 起年, 止年) 结构自洽。
- **37 LEAGUE_HISTORY** — 本轮最强锚点:`u16@0` 取值 0..7,044,全部落在 comp 域;`u32@4` 取值 51..84,481,全部落在 team 域(84,507);`u16@12` 年列 0..2024;`u16@5` 0..330 像积分/场次。联赛历史 = (comp, team, 年, 积分) 完全自洽。
- **42 RETIREMENT** — `u32@0` 100% 落 person duni(distinct 16,756 / 命中 16,756,lift 3,092 = 基准密度 0.000323 的 3,092 倍);另有 packed YMD(`off=8` 命中 1.0)与 year 1900..2031(d=56)。人 + 退役日期自洽。
- **43 MONTHLY_INSTALLMENT** — person duni 533/533(lift 3,176);`u32@24` = 2..84(d=14)是分期月数,`u32@28` = 1,041..3,861,111(d=106)是金额。人 + 月数 + 金额三件套齐全。
- **51 MLS_GENERAL_ALLOCATION_MONEY** — `u32@4` = 1,520,812..2,241,197(仅 3 种取值),量级符合 GAM 货币额;packed YMD 命中 1.0,`u16@8` year 2021..2024。名字里的 MONEY 对得上。**注意样本薄(59 行 / 3 个金额值)。**
- **58 WEEKLY_WAGE_CONTRIBUTION** — 8 行全落 person duni(lift 226.5);三组小整数 603..1,871、658..1,733、1,400..38,800 呈典型周薪/贡献额形状。**样本仅 8 行,结论强度受限于样本。**
- **62 RESERVE_TEAM** — `u32@1` 全部 ≤84,258(distinct 25,034),恰好压在 club 基准 84,259 的上界而非 team 的 84,507,即落 club 域;与 RESERVE_TEAM→club 语义不矛盾。**但 team 84,507 与 club 84,259 只差 248,本列无法区分二者,只能算"不矛盾"。**
- **64 CLUB_STAFF_JOB_STATUS** — `u32@0` = 11..82,188(753 个 distinct club,全部 ≤84,259);`u8@4` job_type 0..255(d=67)、`u8@6` 枚举 0..3。纯 club 引用 + 岗位枚举,语义最干净的一张。

### silent(4)

- **46 DRAFT_TRANSFER** — 全表 7 行,`u32@0/@4` 取值 1,907..72,052,048,高位带 8bit 标记,不落 person / club / team / comp 任一 ID 空间(low16 判据对 club 基准 84,259 > 65,535 天然失效)。虽见 packed YMD 1.0 与 year 2024..2025,引用列无法确证 → silent。
- **50 MLS_TRADED_SLOT** — 45 行,`u32@0/@4` 值域 1,903..2,000,153,732;日期列去重仅 3~4 个值,无金额列。既无可用引用锚点也无金额语义 → silent。
- **66 CLUB_TRANSFER_PREFERENCE** — 753 行,`u32@0` 仅 7.7% 行落 person duni(29 distinct 命中 / 343 distinct),`u32@4` 的 low16 落 club 域 100% 但 24 位截断后退化到 0.9801,无鉴别力;未观察到 0..20 偏好滑杆列 → 列画像与类名无法对接,标 silent。
- **70 VISION_OBJECTIVE** — 10,075 行,`u32@0` / `u32@4` 的 person duni 行命中率仅 1.19% / 5.36%(lift 79 / 356,均不构成引用证据);`@0..@12` 全是高位带标记的复合值,只解出 year 1900..2033(d=15) → silent。

## 与 fk_hits.json 的一致性

`fk_hits.json` 只在 42 / 43 / 58 三张表报了强命中(42 列 lift 3,092、43 lift 3,176、58 lift 226.5),与本表把三张判 plausible 的结论一致;34 / 37 / 62 / 64 的锚点来自 `measure.json` 的 mask / 值域区间判据(非 duni),66 / 70 在 fk_hits 里为空,也与 silent 判断一致。

## 产物缺口(未补数据)

- `prof/p34.json`、`prof/p37.json` 不存在;`prof/e34.txt` 是 `dspot.py` 的 closure 异常回溯(`closure fail t34: 12 != 313082`),`prof/e37.txt` 缺失。34 / 37 的结论改由 `measure.json` + `grid/t34.txt` / `grid/t37.txt` 支撑。
- `scratch/t15d/out/idset/` 为空目录,club/team 真实 ID 集合未落盘;故 62 / 64 只能用值域上界判据(已注明不可区分 team 84,507)。

以上缺口一律按任务书纪律标 silent 而不重跑;34 / 37 因有等价数值证据,仍给 plausible。

## 边界声明

- 本表是抽查级的自洽性判读,不是实体裁决,不得据此升降 t14 的 stage2 判定。
- `silent` 表示"现有产物不足以判定",不代表该表无用;四张 silent 表的阻断原因均已逐条写明。
- 无 `implausible`:没有任何一张表出现"类名要求的引用/金额/日期列与画像明确矛盾"的情形。
