# t142 (`gpt-6.2-sol` max): FM24 全库 79 表 + 65.8 万人外键关系图谱、匿名列语义破译与一致性体检

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or any existing `scripts/tNN_*.py` files. Write ONLY to `scripts/t142_fk_graph_audit.py` and `scratch/t142/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` for `zstandard`.

## Authoritative Inputs Already Verified On Disk
1. `scripts/t133_fm24_reader_v2.py` — Pure-Python **79/79** numbered tables (`2,846,936` rows, `0` failed, `0` skipped, all `diff=0`) in `scratch/data/server_db.dat` & `client_db.dat`.
2. `scripts/t123_basic_people_l3.py` — **658,011** people in `scratch/data/basic_people_db.dat` (`ordinal`, `person_type`, `uid`, `nation`, `club`, `CA`, `PA`, `birth_date`).
3. `scripts/t106_special_members.py` — **13/13** special members (`name_table_0/1/2`, `club_links`, `common_name_links`, `simple_vars`, `summary.dat`).
4. `scripts/t143_lang_db.py` — **704/704** language members (`10,290,726` strings across 22 languages).
5. `scratch/t121/out/master_79of79_l3.json` (1,104 Unicorn × IDA L3 4CC mappings) and `scratch/t95/funcs/*.c` + `scratch/t124/out/funcs/*.c` + `scratch/t132/out/funcs/*.c` (for code-corroborating any newly discovered foreign keys!).

## Your Mission (Rigorous Relational Graph Discovery + Zero False Positives!)
Build `scripts/t142_fk_graph_audit.py` (with `--selftest`) that walks ALL 79 tables (`server_db` 59 + `client_db` 20) + `basic_people` (658,011) + `club_links` (9,261) + `name_table_0/1/2` (873,709) to construct the **authoritative FM24 Relational Foreign-Key Graph & Referential Integrity Audit**:

1. **Identity Domain Registry (Every Target Entity Table's `ordinal` & `uid` Key Sets)**:
   - Build exact `(min, max, count, set)` domains for `ordinal` and `uid` across ALL entity tables (`AWARD` t0, `CITY` t2, `CLUB` t3, `CONTINENT` t5, `INJURY` t6, `MEDIA_SOURCE` t7, `LANGUAGE` t8, `NTC` t9, `NATION` t10, `DERBY` t18, `REGION` t19, `STADIUM` t21, `STADIUM_CHANGE` t22, `STAGE_NAME` t23, `TEAM` t24, `COMP` t25, `WEATHER` t27, `PLAYER_TYPE` t35, `CURRENCY_RECORD` t41, `LOCAL_REGION` t47, `AGREEMENT` t56, `BASIC_PERSON` 658k, `NAME_0/1/2`!).
   - Verify uniqueness invariants on EVERY table: is `ordinal` strictly `0..N-1` (or sparse)? Is `uid` globally unique within each table, and where do cross-table `uid` collisions occur (like `UID 676` = Liverpool FC in `CLUB` AND Anfield in `STADIUM` discovered by `t143`!)?
2. **Verified Foreign-Key Edges & Referential Integrity Audit (Both Known L3 Columns AND Unnamed `col_N` Columns!)**:
   - Audit EVERY integer scalar column across the 79 tables (especially the 46 fixed-stride tables + core variable tables `CLUB`, `COMP`, `NATION`, `NTC`, `TEAM`, `STARTING_RECORD` `t45`/`t48`, `STARTING_PERSON_HISTORY` `t49`, `STARTING_TEAM_LEAGUE_HISTORY` `t37`, `STARTING_CLUB_DEBT` `t33`, `STARTING_INJURY` `t30`, `STARTING_LOAN` `t29`, `STARTING_PAST_TRANSFER` `t71`, `STARTING_PAST_TRADE` `t72`, `STARTING_FUTURE_TRANSFER` `t32`, `STARTING_RESERVE_TEAM` `t62`, `STARTING_VISION_OBJECTIVE` `t70`!).
   - For EVERY foreign-key edge (`src_table.col -> dst_table.{ordinal|uid}`):
     - Distinguish **Code-Corroborated L3 FK** (matches `t121` 4CC / `t95`/`t132` C `DATABASE_OBJECT_REF` global table pointer `0x141B5FDxx` or `slot20` resolver!) vs **Statistical Candidate FK** (strictly require non-trivial cardinality, high non-sentinel hit rate `>= 99%`, domain specificity — NEVER promote small 0..10 enum flags as `CONTINENT`/`AGREEMENT` FKs!).
     - Compute exact `non_sentinel_rows`, `valid_hits`, `hit_rate`, `orphan_count` (and sample orphan IDs if any!), `sentinel_values` (e.g., `-1 / 0xFFFFFFFF`), and whether the FK targets `ordinal` vs `uid`!
3. **Anonymous Column (`col_N`) Semantic Breakthrough**:
   - Specifically highlight EVERY previously-unnamed `col_N` column across `t133`'s 79 tables that you can now **prove** is a real Foreign Key (citing BOTH empirical `99%–100%` hit rate AND C-code / `slot19` / `slot20` evidence where available)!
4. **Full Database Health & Consistency Report**:
   - Report total entities, total verified FK edges, exact orphan/broken-reference count across the real shipping FM24 `24.3.0` database, and cross-table `uid` namespace overlap statistics!

## Deliverables
Write `scripts/t142_fk_graph_audit.py` (with `--selftest`) and `scratch/t142/out/`:
1. `fk_graph_master.json` — full identity domain registry, all verified FK edges (code-corroborated vs statistical-candidate separated), anonymous `col_N` upgrades, orphan audit, cross-table UID overlap matrix
2. `REPORT.md` — concise engineering report with mermaid ER diagram (`erDiagram` or `flowchart LR` of top core entities!), verified FK table, newly decoded `col_N` FKs, and DB health/orphan summary
3. `DONE.md` — first line `DONE type=t142`, total tables audited, verified FK edges, newly decoded `col_N` FKs, orphan count, `--selftest PASS`

Run `py -V:3.12 -B scripts/t142_fk_graph_audit.py` and `--selftest` before finishing!
