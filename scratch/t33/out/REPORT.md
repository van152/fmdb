# t33 — club/team 子表数据侧画像 batch II

状态：`batch_ii_data_side_profiles`。本批 7 张 server 子表全部获得完整行 dump 与逐字节列画像；**parent↔table 连接全部停留在 candidate/unknown，L3=0、L4=0**，不做静态 cursor。

## 行封口(独立算术 + 每行尾锚)

| table | RTTI | model | count | stride | 封口方程 | rows_sha256 前 16 |
|---:|---|---|---:|---:|---|---|
| 12 | `STARTING_AWARD_HISTORY` | variable | 28597 | — | 14 + sum(row_lens=3739548) + 8 = 3739570 | `ba55a89deb901bc7` |
| 39 | `STARTING_AVERAGE_POINTS` | fixed | 117 | 42 | 14 + 117 * 42 + 8 = 4936 | `1647286698dc389e` |
| 45 | `STARTING_RECORD` | variable | 84477 | — | 14 + sum(row_lens=7608726) + 8 = 7608748 | `601a061c05eae23b` |
| 48 | `STARTING_RECORD` | variable | 5210 | — | 14 + sum(row_lens=446027) + 8 = 446049 | `eca0240ffaf66d62` |
| 58 | `STARTING_WEEKLY_WAGE_CONTRIBUTION` | fixed | 8 | 45 | 14 + 8 * 45 + 8 = 382 | `cd7997c03ed5cfff` |
| 59 | `STARTING_MEDIA_EXPECTATIONS` | variable | 9079 | — | 14 + sum(row_lens=224858) + 8 = 224880 | `94b77a7e6863b4ec` |
| 73 | `STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNE` | fixed | 1 | 23 | 14 + 1 * 23 + 8 = 45 | `c1c3b24b708240e9` |

固定表同时试过 `14+n*s+8` 与 `13+n*s+9` 两种约定；只有通过逐行尾锚(`ordinal|id|id|marker`) 的那一种被采用，另一种的算术结果保留在 `row_closure.conventions_tried` 里备查。变长表用 tail-13 帧前向走查，每行 ordinal 严格等于行号、相邻两个 u32 相等、末字节为 0x00/0x0C，并要求 `14 + Σrow + 8 == payload_len` 精确闭合。

### 帧歧义(E66 相邻问题)

变长走查取**最短可行帧长**；若同一行还有更长的长度也满足帧条件，计入 `frame_ambiguity`：

- table_12: 多解行 34 / 28597，最多 5 个候选长度
- table_45: 多解行 1 / 84477，最多 3 个候选长度
- table_48: 多解行 2 / 5210，最多 2 个候选长度
- table_59: 多解行 1 / 9079，最多 5 个候选长度

## parent↔table 连接判断

| table | 候选父码 | confidence | 主要 blocker |
|---:|---|---|---|
| 12 | `AWsh` | **candidate** | variable rows 31..203 B do not expose one fixed slot per AWsh item |
| 39 | `csap` | **unknown** | constant u32 at +4/+8 in every row is unexplained |
| 45 | `Plhs`, `Pnph`, `Pacl` | **unknown** | t14 adjudication for table 45 is `candidate`, entity_tag null |
| 48 | `Plhs`, `Pnph`, `Pacl` | **unknown** | identical RTTI identity to table 45 forbids a unique list claim |
| 58 | `Cwcl` | **candidate** | 5-field item list (icom/play/club/wage/wend) is not reproducible from the 45-byte row with a sin |
| 59 | `Csme` | **candidate** | tail id pair in every row equals 0x01000000, not a plausible media_source id; column semantics s |
| 73 | — | **unknown** | no schema list node in the frozen master.json |

### 逐表理由

- **table_12** `STARTING_AWARD_HISTORY` — candidate
  - 依据：rows carry length-prefixed person-name strings plus u32 id pairs and packed dates, matching an award-history item (AH1n/First Placed Name etc.), but only a subset of the 26 AWsh items is reachable
  - blocker：variable rows 31..203 B do not expose one fixed slot per AWsh item
  - blocker：no reader join from table 12 to award.AWsh collection
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - 已排除 `Cafl`：Cafl is club.Current Affiliations (club ref + booleans + fees); table 12 is RTTI-tagged awar and its rows carry award-history strings/positions
  - 已排除 `Calt`：Calt is club.Alternative Stadiums (competition+stadium refs+dates); no stadium-domain column exists in table 12
  - schema `award.xml#awar.AWsh` item 字段 5/27 有列候选
- **table_39** `STARTING_AVERAGE_POINTS` — unknown
  - 依据：entity team is resolved by RTTI+stage2, but the 42-byte row shows the same u32 at +4 and +8 in all 117 rows and only 3 u16 value slots, which does not line up with team+6 integer csap items
  - blocker：constant u32 at +4/+8 in every row is unexplained
  - blocker：csap item needs 6 numeric slots; only 3 u16 slots admit the integer filter
  - blocker：csap lives on comp.xml, table_39 entity is team: ownership direction (comp->team vs team->comp) is unresolved
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - 已排除 `CPsL`：CPsL is club.Player Partnerships (2 person fields); table 39 is RTTI-tagged team and its row carries a team-domain id, so a player-pair list cannot be the item type
  - schema `comp.xml#comp.csap` item 字段 1/7 有列候选
- **table_45** `STARTING_RECORD` — unknown
  - 依据：person names + packed dates + a repeated u32 pair appear in every row, consistent with a per-person career record; entity pers is only the stage2 adjudication (t14 keeps the entity tag null)
  - blocker：t14 adjudication for table 45 is `candidate`, entity_tag null
  - blocker：three schema lists (Plhs/Pnph/Pacl) remain compatible
  - blocker：row body is variable (80..122 B) and contains an unexplained person-name string copy
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - schema `person.xml#pers.Plhs` item 字段 10/14 有列候选
  - schema `person.xml#pers.Pnph` item 字段 3/4 有列候选
  - schema `person.xml#pers.Pacl` item 字段 4/8 有列候选
- **table_48** `STARTING_RECORD` — unknown
  - 依据：same RTTI class/handler/vtable as table 45, so the two tables are the same C++ type; which schema list each one instantiates is undetermined
  - blocker：identical RTTI identity to table 45 forbids a unique list claim
  - blocker：rows 79..130 B, u32 pairs + u16 year + person-name string
  - blocker：no reader join; entity resolution rests on the older stage2 note
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - schema `person.xml#pers.Plhs` item 字段 10/14 有列候选
  - schema `person.xml#pers.Pnph` item 字段 3/4 有列候选
  - schema `person.xml#pers.Pacl` item 字段 4/8 有列候选
- **table_58** `STARTING_WEEKLY_WAGE_CONTRIBUTION` — candidate
  - 依据：row framing (45 B, 8 rows) is consistent with a small per-club contribution list, but two u32 pairs + u16 year + u32 value do not reproduce the 5-field Cwcl item list; no reader join
  - blocker：5-field item list (icom/play/club/wage/wend) is not reproducible from the 45-byte row with a single admissible layout
  - blocker：only 8 rows: too few to separate sender/player/club id columns
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - schema `club.xml#club.Cwcl` item 字段 5/5 有列候选
- **table_59** `STARTING_MEDIA_EXPECTATIONS` — candidate
  - 依据：9,079 short rows (19..32 B) of small integers match the 2-field Csme item (media source id + predicted finish <= 127)
  - blocker：tail id pair in every row equals 0x01000000, not a plausible media_source id; column semantics stay unresolved
  - blocker：row body length varies 19/22/25/32 so no single 2-field layout holds for all rows
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - schema `club.xml#club.Csme` item 字段 1/2 有列候选
- **table_73** `STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT` — unknown
  - 依据：single 23-byte row; u16 year 2023 and one u32 in the club id domain, which fits the Italian non-EU slot event, but the frozen master.json exposes no matching schema list and one row cannot support a column map
  - blocker：no schema list node in the frozen master.json
  - blocker：count=1: every column statistic is degenerate
  - blocker：u32 at +0 (80,864,099) is outside the person reference domain
  - blocker：no reader/collection join was performed; RTTI class + data shape are not a join
  - blocker：no L3/L4 evidence in this task (L4=0 by instruction)
  - blocker：no schema list node in the frozen master.json matches this class

## 列候选方法

- 列画像覆盖每个 byte offset × {u8,u16,u32,u64}，固定表用 `row_start` 帧，变长表同时用 `row_start` 与 `row_end` 帧；u32 额外算 signed i32、引用域命中率、packed day/year 有效率、float32 重解释。
- 走查器自身的尾锚字节(`row_end-1..-13`)与常量列在匹配前被剔除(`is_frame_column`)，否则边界机器码会被当成字段证据。
- 引用域候选要求列值真分散(≥50% distinct 且 max≥32)，只落在`[0,domain)` 不算证据。整数候选要求列真有范围，不是两值旗标。
- 所有匹配一律 `evidence_level=L2_candidate` / `claim_status=candidate`；域相似性从不单独决定字段身份。

## 口径与限制

- 只读 `scratch/data`(与冻结 `dat_headers.json` 的 size/SHA-256 校验一致)与仓内证据；未读写 Z:，未启动游戏/编辑器/IDA，L4=0。
- `master.json` 快照 SHA-256 与 `evidence/MANIFEST.json` 比对通过，写入 provenance。
- t14 census 无 `reader_va` 字段，本批一律记 `null`，未从 handler VA 推导。
- t14 `entity_tag` 为 null 的表(45/48)保留 null，不借 stage2 的 pers 结论改写 RTTI 身份。
- 负结果保留：table_73 在冻结 schema 中找不到对应 list 节点，标 unknown 而非猜。

## 验证

```
py -V:3.12 -I -B scratch/t33/out/verify.py
```

独立重读 archive、重新走查行边界、复算 payload/rows SHA-256、复核列统计抽样。
