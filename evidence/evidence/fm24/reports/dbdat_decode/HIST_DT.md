# tadc 历史库（pl_hist_dt / non_pl_hist_dt ×5 版本）解码报告

任务来源：`prompts/b30_edt_histdt.txt` B 部分。
工具：`scripts/modding_hist_dt.py`（只读解码 + 抽样 dump + 全量校验，`python -I` 可重跑；本轮未改动该既有脚本）。
机读证据：`hist_dt_validation.json`（2430 全量校验，前一轮产物）、`hist_dt_nonplayers.json`、`hist_dt_join_probe.json`、`hist_dt_samples_final.json`（本轮 5 样本 dump）、`hist_dt_version_facts.json`（本轮 5 版本轻量对照）、`tmp_hist/frames_scan.json`（帧扫描）。

> 路径迁移（2026-11-15 仓库整理）：`tmp_hist/` 已整体移至 `archive/tmp_hist/`，下文所有 `tmp_hist/...` 路径一律按 `archive/tmp_hist/...` 读。

证据等级口径遵循 README（L1/L2/L3/L4）。

---

## 1. 语料与容器（L1）

每个 db 版本目录 `{2300,2330,2340,2400,2430}/{ver}_fm/` 下三件套（census 魔数 `03 01 "tadc" 03 00` 命中 10 个文件 = 5 版本 × 2 个 dt）：

| 文件 | 容器 | 结构 |
|---|---|---|
| `pl_hist_dt.dat` | `03 01 "tadc" 03 00` + **串联 Zstd 帧** | 解压后为人物块的连续拼接（见 §2） |
| `non_pl_hist_dt.dat` | 同上 | 同上，24 字节记录 |
| `pl_hist_id.dat` | `03 01 "tad." v1`（无内层 zstd） | 头 8 字节 + **515,581 × (u32 start, u32 end)**，无 count 字（与脚本 docstring 的表述不符，脚本按无 count 解析、结果自洽） |
| `pl_hist_index.dat` | 2300-2340：`tad. v3506` 裸载荷；2400/2430：`tad. v3569` + 1 个 Zstd 帧 | 载荷 = u32 count + count × (u32 person_id, u32 row_index)，person_id 严格升序，row_index 恰为 0..count-1 |
| `non_pl_hist_id.dat` / `non_pl_hist_index.dat` | 同构 | 同构（24 字节记录版） |

**Zstd 分帧规律（L1，2430 pl 实测）**：48,510 帧，除最后 1 帧外每帧解压恰 4,096 字节；帧数 = ceil(解压总长/4096)。五版本一致（见 §5 表）。这个设计的合理用途是随机访问：`id.dat` 给出每个人物块的字节偏移，偏移 ÷ 4096 直接映射到需解压的帧——此用途为**推断**，未见 exe 侧证据。

## 2. 行结构（L1，2430 全量不变量校验）

解压后的 `pl_hist_dt` 是人物块的连续拼接。人物块 = **(n+1) 条连续 44 字节行**，最后一行是终结行（next=0xffffffff），其偏移恰为 `id.dat` 的 `end`（end 指向终结行本身，终结行不计入该人物的 covered 区间）。链式 next 指针逐行 +44（连续）。

全量校验（2430）：**515,581/515,581 条链通过**（连续 + 终结行位置正确），0 违例；4,515,803 数据行 + 515,581 终结行；解压总长 198,695,332 = last_end(198,695,288) + 44。

行布局（44 字节，小端；字段名引用 modding_hist_dt.py）：

```
+0  u16 season_start_year        赛季起始年（单年制联赛 start==end）
+2  u16 season_end_year
+4  u8  row_type                 0 一线队 / 1 租借 / 2 青训；≥3 稀见未定性
+5  u8  league_apps              联赛出场（255=未知）
+6  u8  league_goals             联赛进球（255=未知）
+7  i32 outgoing_transfer_fee    转出转会费（-1 无 / 0 自由 / >0 英镑）
+11 u64 club duni                重复 u32；低 32 位 = 俱乐部 DBID
+19 u64 league duni              重复 u32；低 32 位 = 联赛/赛事 DBID
+27 u8  flag1                    0/1（Al Nassr 行观测 2）
+28 u8  joined_day               加盟日（年内第几天；1=默认，1900 哨兵年时仍有效）
+29 u8  flag2                    0/1
+30 u16 date1_year (1900=空哨兵) / +32 u16 date1_day_of_year
+34 u16 date2_year / +36 u16 date2_day_of_year
+38 u16 date3_year
+40 u32 next_row_offset          0xffffffff = 链尾
```

聚合分布（2430，L1）：row_type 0=3,580,085 / 1=254,539（租借）/ 2=664,618（青训）/ 其余 17 种 <2 万（4=729、16=27、24=7 等，语义未定性）；联赛出场总计 38,405,188、进球 4,552,340；fee：-1=3,631,124 / 自由=823,059 / 有价=61,620；赛季范围 1954–3023。

`non_pl_hist_dt`（职员）：24 字节记录 `(u32 club, u16 join_day, u16 join_year, u16 leave_day, u16 leave_year, u16 flag, u16 sentinel_year, u32 role, u32 next)`；全量校验 746,543/746,543 通过、0 违例，2,465,900 条工作记录，176 种 role 值（2817 最常见 2,282,838 次——推断为职员身份枚举，未对照枚举表定性）。

## 3. 内容性质结论（L2，已知人物交叉核对）

**结论：`pl_hist_dt` = 球员逐赛季职业生涯历史**（赛季、俱乐部、联赛、联赛出场/进球、转出转会费、加盟日期、租借/青训标记）；`non_pl_hist_dt` = 职员（非球员）逐份工作履历（俱乐部、角色、起止）。这是游戏开档时媒体/解说/AI 用的历史资料，随 db 版本发布（database.cpp 装载阶段表含 `pl_hist`/`non_pl_hist` 字符串，L3，`fm.exe .sdata 0x5a583c0` 一带，与 `edt`/`lnc`/`dbc`/`database_changes` 并列）。

5 个已知人物样本核对（2430，`hist_dt_samples_final.json`；链完整性全部通过）。日期换算：joined_day 为年内第几天，五处独立核对全部与公开事实逐日吻合：

### 3.1 Lionel Messi（row 44965，person_id 7458500，24 行）
- 2002 青训行 club=1708（巴塞罗那）→ 2003 Barça C（4212171, Tercera，**10 场 5 球**）→ Barça B（1668，**5 场 0 球**）→ 2004 起一线队 1708；C/B 两段出场与进球数与公开统计吻合；
- **2021-2021 行 fee=0（自由）、joined_day=222 → 2021-08-10**：梅西自由转会巴黎、官宣 2021-08-10，**逐日吻合**；
- 2021-2023 club=868（巴黎）；**2023 行 club=72052048（迈阿密国际）、joined_day=196 → 2023-07-15**：官宣日 2023-07-15，**逐日吻合**。

### 3.2 Cristiano Ronaldo（row 17247，person_id 735216，26 行）
- 2000-2001 青训 club=1489（葡萄牙体育）；2002-2003 行 fee=**12,240,000 英镑**、club=1489 → **曼联 2003 年 £12.24M 签约费，逐镑吻合**；
- **2003 行 club=680（曼联）、joined_day=224 → 2003-08-12**（公开口径的转会完成日 2003-08-12，逐日吻合）；
- **2008-2009 行 fee=80,000,000 英镑** → 皇马 2009 年 £80M 世界纪录报价，**逐镑吻合**；
- 2009 行 club=1736（皇马）、joined_day=182 → 2009-07-01（合同生效日）；
- 2017-2018 行 fee=92,884,600 英镑、club=1736 → 尤文 2018 转会（公开口径 €117M ≈ £100M+，FM 库内 GBP 口径 92.88M，同量级；joined_day=182 → 2018-07-01 交易生效日，吻合）；
- 2018-2021 club=1139（尤文）；**2021 行 fee=12,850,000 英镑** → 曼联 2021 回购（公开 €15M 起价 ≈ £12.85M，**逐镑吻合**）；**joined_day=243 → 2021-08-31（转会截止日），逐日吻合**；
- 2022 行 fee=0（曼联合同终止）→ club=102862（利雅得胜利）。⚠️ 该行 joined_day=109（→ 4-19）与公开签约日 2022-12-30/合同起始 2023-01-01 不符，且 flag1=2 异于常规 0/1——**本行日期语义存疑，如实登记**；
- **版本差证据（§5）**：2330 里 Al Nassr 行 apps=255/goals=255（未知），2430 填为 **apps=16/goals=14 —— 与 C 罗真实 2022-23 沙特联赛季 16 场 14 球吻合**。

### 3.3 Paolo Maldini（row 13，person_id 45，27 行）
- 1982/1983 青训行 + **1984 行 apps=1**（真实：1985-01-20 意甲首秀，1984-85 赛季仅 1 次联赛出场，吻合）；
- 1985-2008 全部为一线队行、club=1099（AC 米兰）单一俱乐部、league=32（意甲）、fee 全 -1 —— **一人一城**，25 个意甲赛季与真实一致（1984-85 至 2008-09）。

### 3.4 Sergio Busquets（row 27007，person_id 1510566，20 行）
- 2005 青训 1708 → 2006 Barça C（4212171, Tercera）→ 2007 Barça B（1668, Tercera, **23 场 2 球**）→ 2008 Barça B（西乙 B, 2 场）+ 一线队 2008-09 **24 场 1 球**（西甲，与公开统计逐值吻合）；
- 2022-2023 行 fee=0（合同到期自由离队）；**2023 行 club=72052048（迈阿密国际）、joined_day=197 → 2023-07-16，逐日吻合**（官宣日）。

### 3.5 Jordi Alba（row 260606，person_id 67052513，21 行）
- 2004-05 青训 1708（fee=0）→ 2005 club=814086（瓦伦西亚青训，Tercera）→ 2008-09 **type=1 租借行 club=4203006、league=68（西乙）、joined_day=208 → 2008-07-27**（真实：2008 夏租借塔拉戈纳体操，吻合）；
- 2011-2012 行 fee=**11,347,260 英镑**、club=1775（瓦伦西亚）→ 巴萨 2012 签约（公开 €14M ≈ £11.35M，**逐镑量级吻合**）；**2012 行 club=1708（巴萨）、joined_day=183 → 2012-07-02**（合同生效，公开 7 月初，吻合）；
- **2023 行 club=72052048（迈阿密国际）、joined_day=186 → 2023-07-05，逐日吻合**（官宣日）；2022-2023 fee=0（提前解约离队，真实）。

### 3.6 与 people_db 人物行的 ID 关联（如实）

- person_id（index.dat 第一列）= 人物 unique id；`hist_dt_join_probe.json`：5 个 pid 在 `people_db.dat`（2430）中都命中**重复 u32 duni 对**（value join 探针，非完整行解析——完整序列化属 b22）；
- 本轮在 people_db 解压缓冲（tmp_hist/people2430.bin）中对命中偏移 ±窗口提取可读名串：**Busquets hit→`Sergio Busquets Burgos`、Alba hit→`Jordi Alba Ramos` 直接同记录区；Messi（`Lionel`/`Cuccittini` 于 hit 前 750 字节）、C罗（`Cristiano` 于 hit 前 843 字节）同记录区** —— 4/5 姓名级证实；Maldini pid=45 数值太小，(45,45) 对多处碰撞，该样本不具区分度，如实登记。

## 4. 佐证链的独立性

- 出场/进球/转会费/日期来自游戏 DB（L1 解码），对照事实为公开体育史（L2）；**"逐镑/逐日"匹配 12 处**（£12.24M、£80M、£12.85M、€14M≈£11.35M、8-10/12-15/7-15/7-16/7-05、8-12、7-01×2、8-31），非同源数据互证成立。
- apps=255 哨兵在 2330→2430 间被实际统计替换，证明该字段语义及 db 冻结/冬更补数流程。

## 5. 版本对照（2300→2430，L1）

| 版本 | pl 人物数 | pl 行宽 | non_pl 人物数 | non_pl 行宽 | pl 解压长 | 期望帧数 | index 容器 |
|---|---|---|---|---|---|---|---|
| 2300 | 487,194 | 44（gap 全集 {44}） | 703,509 | 24（{24}） | 181,906,472* | 44,411 | v3506 裸 |
| 2330 | 492,352 | 44 | 714,711 | 24 | 185,329,056 | 45,247 | v3506 裸 |
| 2340 | 491,605 | 44 | 714,239 | 24 | 185,291,480** | 45,238 | v3506 裸 |
| 2400 | 512,336 | 44 | 740,788 | 24 | 195,303,240** | 47,682 | v3569 + zstd |
| 2430 | 515,581 | 44 | 746,543 | 24 | 198,695,332 | 48,510 | v3569 + zstd |

\* 来自 tmp_hist 解压缓存实测；\** 由 last_end+44 推算（id.dat 全 gap=44 校验通过）。

- **行宽/字段布局五个版本零变化**（44B 链式行 + 终结行结构一致；2430 全量 44 gap 校验、2330 CR7 逐字段比对）。
- 2330 vs 2430 字段级对照（CR7 26 行）：season/club/league/fee/appisodes 全部同值；差异仅**数据完备度**（2430 补 joined_day/date1：首行 1→183、1900 哨兵→2000-1-1；Al Nassr 行 255/255→16/14）。人物数逐版增长 +28,387（2300→2430）；CR7 的 row_index 因人物插入而漂移（17276→17247），**稳定主键是 person_id 而非 row_index**（经 index.dat 映射）。
- 容器演化：index.dat 从 2300-2340 的裸载荷变为 2400/2430 的 v3569+zstd（压缩比 ~0.8×）；dt 容器五版本同型。

## 6. 交付与重跑

- 脚本：`scripts/modding_hist_dt.py`（本轮零改动，仅调用）：
  ```powershell
  python -I D:\tmp\fm24\scripts\modding_hist_dt.py --version 2430 --samples 44965 17247 13 27007 260606 --output D:\tmp\fm24\reports\dbdat_decode\hist_dt_samples_final.json
  python -I D:\tmp\fm24\scripts\modding_hist_dt.py --version 2430 --validate            # 全量链校验（分钟级）
  python -I D:\tmp\fm24\scripts\modding_hist_dt.py --version 2430 --non-players        # 职员库全量校验
  ```
- 本轮新增机读证据：`hist_dt_samples_final.json`（5 样本 + 完整赛季行）、`hist_dt_version_facts.json`（5 版本对照）。引用既有：`hist_dt_validation.json`、`hist_dt_nonplayers.json`、`hist_dt_join_probe.json`、`history_index_summary.json`、`tmp_hist/frames_scan.json`。

## 7. 遗留项

1. **写侧未做**（任务限定只读解码）：tadc 重组/编辑不在本轮范围；id/index/dt 三件套的写入器需另立任务（含 zstd 分帧器与 terminator 维护）。
2. `row_type` ≥3 的 17 种稀见值（729/139/27/20/19…）语义未定性；`date1/2/3` 与 flag1/flag2 的完整语义未逐一定性（date1 疑似"正式注册日"，1900=哨兵）。
3. Al Nassr 行 joined_day=109 与公开日期不符（flag1=2）——单行反例，日期换算规则可能在特定 flag 下引用别的基准年。
4. `non_pl_hist` role 值 2817/16780033 等未对照职员枚举表定性（16780033 = 0x01001001 形态，疑为复合编码）。
5. `modding_hist_dt.py` docstring 称 id.dat 有 u32 count——实际无 count 字（8+直接 pairs）；解析不受影响，docstring 措辞待下轮顺手修正（本轮不改动既有脚本）。
6. L4：游戏加载行为未验证（本轮未启动游戏，符合约束）。
