# t97 — Hex-Rays 4CC ↔ 内存偏移全量抽取 + 1,034 分母分诊

> 只读输入：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（Hex-Rays 反编译 C）、
> `reports/xml_denominator_coverage.json`。**本任务不修改 `reports/` 与 `LEDGER.json`**。

## 0. 交付物

| 文件 | 内容 |
|---|---|
| `fourcc_mem_map.json` | 67 张表的 4CC → `mem_off` / `access_kind` / `func_va` / `line_no`（`"status": "complete"`） |
| `xml_triage.json` | 1,034 条分母逐条分诊 + 分桶变化汇总 + 对已验收 L3 的回归验证 |
| `static_read_join.json` | 4CC ↔ `mem_off` ↔ slot19/slot20 行号 的静态交叉表 |
| `REPORT.md` / `DONE.md` | 本报告 / 完成标记（`DONE type=t97`） |

## 1. 覆盖与规模

- 表条目（`vtable_index.tables`）：**67**
- 唯一 4CC：**2219**（t95 初扫曾见 1,897；本任务因追踪基类/子对象 get_prop 而扩大）
- 表×4CC 分支记录：**6219**，其中有明确字节偏移：**1808**（29.1%）
- 纯静态：只解析 t95 的反编译产物，无数据库 dump、无第三方依赖

| access_kind | 分支数 | 含义 |
|---|---|---|
| `helper_computed` | 2525 | 值由 helper 子函数计算（helper 未反编译时无字节偏移） |
| `delegated_or_empty` | 2225 | 分支仅 `return sub_X(this, code, out)` 或直接 `goto`/`break` |
| `direct_field` | 1255 | 分支内直接解引用 `this + N` 的标量/指针字段 |
| `bitfield` | 125 | 同一字段带 `& mask` / `>> n` 位域操作 |
| `subobj_deref` | 89 | 先取 `this + N` 处的子对象指针，再读其内部字段 |

## 2. 每张大表命中率

| tt | class | 链上函数数 | 4CC | 有明确 mem_off | read_server 命中 | slot19 偏移数 |
|---|---|---|---|---|---|---|
| 21 | STADIUM | 5 | 771 | 209 (27%) | 103 | 43 |
| 3 | CLUB | 6 | 767 | 171 (22%) | 27 | 27 |
| 3 | LEAGUE_BODY_CLUB | 6 | 767 | 171 (22%) | 60 | 27 |
| 24 | NATIONAL_TEAM | 6 | 414 | 155 (37%) | 5 | 19 |
| 9 | NATIONAL_TEAM_CONTAINER | 8 | 396 | 122 (31%) | 44 | 106 |
| 10 | NATION | 7 | 396 | 122 (31%) | 5 | 18 |
| 25 | COMP | 2 | 394 | 35 (9%) | 28 | 63 |
| 27 | WEATHER | 2 | 334 | 89 (27%) | 5 | 9 |
| 3 | TEAM_CONTAINER | 2 | 221 | 37 (17%) | 19 | 25 |
| 9 | TEAM_CONTAINER | 2 | 221 | 37 (17%) | 19 | 25 |
| 32 | STARTING_FUTURE_TRANSFER | 2 | 149 | 21 (14%) | 1 | 1 |
| 24 | TEAM | 2 | 72 | 44 (61%) | 16 | 21 |
| 1 | BASIC_PERSON | 2 | 63 | 35 (56%) | 31 | 20 |
| 12 | STARTING_AWARD_HISTORY | 2 | 53 | 27 (51%) | 27 | 29 |
| 4 | RGB_COLOUR | 2 | 52 | 6 (12%) | 1 | 1 |
| 31 | STARTING_CONFIDENCE | 2 | 52 | 6 (12%) | 1 | 4 |
| 36 | STARTING_MANAGER_HOF_RECORD | 2 | 52 | 6 (12%) | 0 | 7 |
| 46 | STARTING_DRAFT_TRANSFER | 2 | 52 | 6 (12%) | 1 | 6 |
| 50 | STARTING_MLS_TRADED_SLOT | 2 | 52 | 6 (12%) | 1 | 5 |
| 51 | STARTING_MLS_GENERAL_ALLOCATION_MONEY | 2 | 52 | 6 (12%) | 1 | 4 |
| 52 | STARTING_PLAYER_HAPPINESS | 2 | 52 | 6 (12%) | 1 | 6 |
| 57 | FIXTURE_NAME | 2 | 52 | 6 (12%) | 1 | 6 |
| 59 | STARTING_MEDIA_EXPECTATIONS | 2 | 52 | 6 (12%) | 1 | 6 |
| 61 | STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT | 2 | 52 | 6 (12%) | 1 | 4 |

其余 43 张表见 `fourcc_mem_map.json`（多为 2–30 个 4CC 的档案表）。

### 2.1 解析器要点（为什么 `helper_computed` 占比高）

- CLUB/COMP 这类 4,500 行的 `get_prop` 把大量 4CC 直接转交给子对象或 helper，例如
  `return sub_143CA2E60(v21, 11, code, a3)`（COMP）、`v214 = sub_140E73FB0(a1)`（CLUB）。
  这些 helper 不在 t95 的 352 份反编译产物中，因此只能记录到 `helper_calls`，无法给出字节偏移。
- 尾调用到**基类** handler（`CLUB → TEAM_CONTAINER`、`NATIONAL_TEAM_CONTAINER → TEAM_CONTAINER`、
  `NATION → 1410668F0 / 141063F30 / 141045D50`）已按「同对象」规则追踪至 depth 3，结果标 `delegated`。
- 共享对象协议 handler（`0x140FE3F20` / `0x140FE2700`，被 13–14 个表条目复用）**不作为基类 getter 追踪**，
  否则 `BaCP/COPY/DELE/Duni/HiSe/ISTP` 等通用协议码会污染全部 67 张表。

## 3. NATION (tt=10) 专项核对

| 槽 | 函数 | depth | 分支数 | 关系 |
|---|---|---|---|---|
| `slot02_get_prop` | `0x141042940` (`funcs/141042940.c`) | 0 | 33 | 自身槽 |
| `slot03_set_prop` | `0x143ecd5c0` (`funcs/143ecd5c0.c`) | 0 | 0 | 自身槽 |
| `slot02_get_prop` | `0x1410668f0` (`funcs/1410668f0.c`) | 1 | 140 | 跨对象（子对象 / hop1 精选） |
| `slot02_get_prop` | `0x1411f1090` (`funcs/1411f1090.c`) | 2 | 187 | 同对象基类/尾调用 |
| `slot03_set_prop` | `0x141045d50` (`funcs/141045d50.c`) | 1 | 28 | 同对象基类/尾调用 |
| `slot03_set_prop` | `0x141063f30` (`funcs/141063f30.c`) | 1 | 82 | 跨对象（子对象 / hop1 精选） |
| `slot03_set_prop` | `0x1411f4f70` (`funcs/1411f4f70.c`) | 2 | 139 | 同对象基类/尾调用 |

任务书点名的四份 nation 侧文件：

- `141042940.c`：在链上 ✔
- `141045d50.c`：在链上 ✔
- `141063f30.c`：在链上 ✔
- `1410668f0.c`：在链上 ✔

`NATION`/`NATIONAL_TEAM_CONTAINER` 的 `missing_subcalls`：**8** 条（转发 4CC 但无反编译文件的直接子调用）

| class | slot | from | 未反编译目标 | arg0 是 this |
|---|---|---|---|---|
| NATIONAL_TEAM_CONTAINER | `slot02_get_prop` | `0x1411f1090` | `0x1411ea620` | True |
| NATIONAL_TEAM_CONTAINER | `slot03_set_prop` | `0x141063f30` | `0x1411e9540` | True |
| NATIONAL_TEAM_CONTAINER | `slot03_set_prop` | `0x1411f4f70` | `0x1411d00e0` | False |
| NATIONAL_TEAM_CONTAINER | `slot03_set_prop` | `0x1411f4f70` | `0x1411eaaa0` | True |
| NATION | `slot02_get_prop` | `0x1411f1090` | `0x1411ea620` | True |
| NATION | `slot03_set_prop` | `0x141063f30` | `0x1411e9540` | True |
| NATION | `slot03_set_prop` | `0x1411f4f70` | `0x1411d00e0` | False |
| NATION | `slot03_set_prop` | `0x1411f4f70` | `0x1411eaaa0` | True |

## 4. 1,034 分母分诊

分母：**1034** 条（club 433 / nation 346 / comp 255）。
分桶变化全部落在候选标签上，`reports/` 未被改写（`proposed_bucket` 是静态候选，不是已接受的桶）。

| 原桶（`bucket_after`） | 总数 | 直接 mem_off | subobj_deref | helper_computed | delegated/empty | 同类同 tag 其它表 | 仅共享 handler | 其它表另有 | 全 67 表皆无 |
|---|---|---|---|---|---|---|---|---|---|
| `held` | 59 | 24 | 4 | 20 | 6 | 1 | 0 | 3 | 1 |
| `independent_member` | 11 | 2 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |
| `mapped_l3` | 99 | 39 | 5 | 9 | 10 | 1 | 0 | 2 | 33 |
| `no_wire_evidence` | 564 | 46 | 0 | 217 | 2 | 0 | 0 | 32 | 267 |
| `re_routed_table_45` | 117 | 0 | 0 | 117 | 0 | 0 | 0 | 0 | 0 |
| `ui_or_derived` | 24 | 0 | 0 | 4 | 7 | 3 | 0 | 0 | 10 |
| `unresolved_wire_slot` | 160 | 41 | 4 | 85 | 17 | 4 | 0 | 0 | 9 |

### 4.1 三个关键桶的突破

- **`unresolved_wire_slot`（160 条）**：明确 `mem_off` **41** 条；`subobj_deref` 4 条；`helper_computed` 85 条；delegated/empty 17 条；链上不存在 9 条（其中全 67 表皆无 9 条 = 强证据：纯 UI / 编辑器派生 / 仅存档字段）
- **`held`（59 条）**：明确 `mem_off` **24** 条；`subobj_deref` 4 条；`helper_computed` 20 条；delegated/empty 6 条；链上不存在 4 条（其中全 67 表皆无 1 条 = 强证据：纯 UI / 编辑器派生 / 仅存档字段）
- **`no_wire_evidence`（564 条）**：明确 `mem_off` **46** 条；`subobj_deref` 0 条；`helper_computed` 217 条；delegated/empty 2 条；链上不存在 299 条（其中全 67 表皆无 267 条 = 强证据：纯 UI / 编辑器派生 / 仅存档字段）

### 4.2 分实体

| entity | 直接 mem_off | helper_computed | delegated/empty | 同类同 tag | 其它表另有 | 全表皆无 |
|---|---|---|---|---|---|---|
| club | 63 | 205 | 28 | 9 | 0 | 116 |
| comp | 25 | 134 | 13 | 0 | 5 | 78 |
| nation | 64 | 122 | 1 | 0 | 32 | 126 |

## 5. 对已验收 L3 的独立回归（防自欺）

来源：`reports/club_nation_subtable_schema.json`（只读），逐字段对比 `object_displacement`：

- 检查 **18** 条：exact **12**、within_slot **3**、no_static_hit **2**、mismatch **1**

> 已验收值是**线槽起点**（slot_width 字节宽），t97 报的是**字段字节偏移**；位域可能落在槽内几字节处，故单列 `within_slot`。

| section | code | 已验收 disp | 宽度 | t97 off | access_kind | 判定 |
|---|---|---|---|---|---|---|
| club | `duni` | 8 | 12 | 12 | `helper_computed` | within_slot |
| club | `Cext` | 216 | 4 | 216 | `subobj_deref` | exact |
| club | `Cedp` | 72 | 1 | — | `helper_computed` | no_static_hit |
| club | `Cnti` | 216 | 4 | 185 | `direct_field` | mismatch |
| club | `Cbni` | 232 | 4 | 232 | `subobj_deref` | exact |
| club | `Cccn` | 240 | 4 | 240 | `subobj_deref` | exact |
| club | `Cncl` | 72 | 1 | — | `helper_computed` | no_static_hit |
| club | `Ccty` | 248 | 4 | 248 | `direct_field` | exact |
| club | `CIns` | 352 | 6 | 352 | `bitfield` | exact |
| club | `CASt` | 352 | 6 | 353 | `bitfield` | within_slot |
| club | `Csot` | 352 | 6 | 352 | `direct_field` | exact |
| club | `Ctsi` | 320 | 4 | 320 | `direct_field` | exact |
| club | `CnCV` | 352 | 6 | 355 | `bitfield` | within_slot |
| nation | `Nnsi` | 280 | None | 280 | `direct_field` | exact |
| nation | `Ncti` | 240 | None | 240 | `direct_field` | exact |
| nation | `Nrgi` | 248 | None | 248 | `direct_field` | exact |
| nation | `Ncur` | 256 | None | 256 | `direct_field` | exact |
| nation | `Nndn` | 456 | None | 456 | `direct_field` | exact |

`no_static_hit` 的两条（`Cedp` / `Cncl`）其值由未反编译 helper 计算；`duni` 是基类序列化的身份列，
不走 4CC 分派，属已知特例。

## 6. slot19/slot20 静态偏移交叉

- slot02/03 有明确 `mem_off` 的分支：**1808**
- 与 `slot19_read_server` 偏移集合相交：**724**
- 与 `slot20_read_client` 偏移集合相交：**250**
- 至少命中一侧：**802**

| tt | class | 有 off | slot19 命中 | slot20 命中 | 至少一侧 |
|---|---|---|---|---|---|
| 21 | STADIUM | 209 | 103 | 12 | 103 |
| 3 | LEAGUE_BODY_CLUB | 171 | 60 | 2 | 62 |
| 9 | NATIONAL_TEAM_CONTAINER | 122 | 44 | 14 | 46 |
| 24 | TEAM | 44 | 16 | 28 | 36 |
| 0 | AWARD | 36 | 31 | 5 | 31 |
| 1 | BASIC_PERSON | 35 | 31 | 8 | 31 |
| 10 | NATION | 122 | 5 | 27 | 29 |
| 25 | COMP | 35 | 28 | 1 | 28 |
| 3 | CLUB | 171 | 27 | 8 | 27 |
| 12 | STARTING_AWARD_HISTORY | 27 | 27 | 6 | 27 |
| 24 | NATIONAL_TEAM | 155 | 5 | 21 | 26 |
| 71 | STARTING_PAST_TRANSFER | 36 | 23 | 15 | 23 |
| 6 | INJURY | 23 | 21 | 0 | 21 |
| 22 | STADIUM_CHANGE | 21 | 21 | 4 | 21 |
| 7 | MEDIA_SOURCE | 24 | 20 | 11 | 20 |

## 7. `missing_subcalls` 清单

合计 **135** 条（去重：表 × 槽 × 目标）。这些是 `slot02`/`slot03`（含追踪到的基类）里
**转发 4CC 但无反编译文件**的直接子调用，是后续扩大反编译的第一优先目标。
完整清单见 `fourcc_mem_map.json#/missing_subcalls`。

| class | 条数 |
|---|---|
| CLUB | 25 |
| LEAGUE_BODY_CLUB | 25 |
| STADIUM | 18 |
| COMP | 10 |
| TEAM_CONTAINER | 8 |
| NATIONAL_TEAM_CONTAINER | 4 |
| NATION | 4 |
| NATIONAL_TEAM | 4 |
| TEAM | 4 |
| BASIC_PERSON | 2 |
| RGB_COLOUR | 2 |
| STARTING_CONFIDENCE | 2 |
| STARTING_FUTURE_TRANSFER | 2 |
| STARTING_MANAGER_HOF_RECORD | 2 |
| STARTING_DRAFT_TRANSFER | 2 |
| STARTING_MLS_TRADED_SLOT | 2 |
| STARTING_MLS_GENERAL_ALLOCATION_MONEY | 2 |
| STARTING_PLAYER_HAPPINESS | 2 |
| FIXTURE_NAME | 2 |
| STARTING_MEDIA_EXPECTATIONS | 2 |
| STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT | 2 |
| STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER | 2 |
| STARTING_CLUB_STAFF_JOB_STATUS | 2 |
| STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT | 2 |
| CONTINENT | 1 |
| PLAYER_TYPE | 1 |
| AGREEMENT | 1 |

出现最多的未反编译目标：

| 目标 VA | 出现次数 | 存在 this 直传 |
|---|---|---|
| `0x14100c380` | 14 | False |
| `0x1410224e0` | 13 | False |
| `0x1411ea620` | 7 | True |
| `0x1411d00e0` | 6 | False |
| `0x1411e9540` | 6 | True |
| `0x1411eaaa0` | 6 | True |
| `0x14151e3b0` | 4 | False |
| `0x14151ef00` | 4 | False |
| `0x140f4aef0` | 4 | False |
| `0x140e60a80` | 3 | True |
| `0x140e60ae0` | 3 | True |
| `0x140e623a0` | 3 | True |

明细（前 40 条）：

| tt | class | slot | from | 目标 | arg0=this |
|---|---|---|---|---|---|
| 1 | BASIC_PERSON | `slot03_set_prop` | `0x140e52de0` | `0x140f4aaf0` | False |
| 1 | BASIC_PERSON | `slot03_set_prop` | `0x140e52de0` | `0x141084920` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e60a80` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e60ae0` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e623a0` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e62640` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e69670` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e72100` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e72d40` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e75ff0` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e79030` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e97410` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e97920` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e98410` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x1411eaa10` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x1411f4bd0` | True |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x14151e3b0` | False |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x14151ef00` | False |
| 3 | CLUB | `slot02_get_prop` | `0x140e8a400` | `0x141520a50` | False |
| 3 | CLUB | `slot02_get_prop` | `0x1411f1090` | `0x1411ea620` | True |
| 3 | CLUB | `slot03_set_prop` | `0x140e834a0` | `0x140e587e0` | False |
| 3 | CLUB | `slot03_set_prop` | `0x140e834a0` | `0x140e87c00` | True |
| 3 | CLUB | `slot03_set_prop` | `0x140e834a0` | `0x140e882d0` | True |
| 3 | CLUB | `slot03_set_prop` | `0x140e834a0` | `0x140f4aef0` | False |
| 3 | CLUB | `slot03_set_prop` | `0x1411f4f70` | `0x1411d00e0` | False |
| 3 | CLUB | `slot03_set_prop` | `0x1411f4f70` | `0x1411e9540` | True |
| 3 | CLUB | `slot03_set_prop` | `0x1411f4f70` | `0x1411eaaa0` | True |
| 3 | TEAM_CONTAINER | `slot02_get_prop` | `0x1411f1090` | `0x1411ea620` | True |
| 3 | TEAM_CONTAINER | `slot03_set_prop` | `0x1411f4f70` | `0x1411d00e0` | False |
| 3 | TEAM_CONTAINER | `slot03_set_prop` | `0x1411f4f70` | `0x1411e9540` | True |
| 3 | TEAM_CONTAINER | `slot03_set_prop` | `0x1411f4f70` | `0x1411eaaa0` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e60a80` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e60ae0` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e623a0` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e62640` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e69670` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e72100` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e72d40` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e75ff0` | True |
| 3 | LEAGUE_BODY_CLUB | `slot02_get_prop` | `0x140e8a400` | `0x140e79030` | True |

## 8. 方法与已知限制

1. **分支定位**：`case <int>:`（含多标签 fallthrough）、`if (V == N) {…}`、`if (V != N) <guard>; <body>`，
   以及 `switch` 表；`V` 取第二个形参及其别名（如 CLUB 的 `v4 = (int)a2`）。
2. **分支体**：花括号匹配 + 同层终止符（`break` / `goto` / `return` / 下一个 `case` / `}`）。
3. **字节偏移**：按 base 变量**声明元素宽度**换算（整型局部/形参 = 1 字节寻址，`_DWORD *` = ×4，
   `_QWORD *` = ×8），并对 `this` 的别名做**逐行 reaching-definition 判定**（Hex-Rays 会复用临时变量，
   例如 COMP 的 `v5` 在某行之后已改指别的对象，其后不得再当作 `this`）。
4. **`primary_off`**：分支体内最小的「带宽度解引用」偏移；64 位 `lo|hi` 拼接（如 `a1+40` / `a1+44`）取低位。
5. **不追踪共享协议 handler**（`0x140FE3F20` / `0x140FE2700`），避免跨表污染；其下 `COPY/DELE/BaCP` 等
   通用协议码因此不会出现在各表 4CC 集合里。
6. **限制**：`helper_computed` 分支无字节偏移（helper 未反编译，见第 7 节）；位域偏移可能比已验收
   线槽起点深 1–5 字节（记 `within_slot`）；`duni` 这类身份列走基类序列化，不在 4CC 分派中。

## 9. 复现

```
py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --selftest   # 25 项断言，含 STARTING_RECORD 三条
py -V:3.12 -I -B scripts/t97_extract_4cc_mem.py --run        # 写 4 个交付物到 scratch/t97/out
```

> 备注：任务书示例写 `1869899892 == 0x6F737474 == 'ostt'`，实际 `0x6F746874 = 'otht'`；
> 自检按真实字节 `'otht' -> 0x28` 断言（偏移结论不受影响）。

