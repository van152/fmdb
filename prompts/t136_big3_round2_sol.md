# t136 (`gpt-6.2-sol` max): Big-3 Final Gap Push (`512/672 = 76.2%` -> `85%+`) + `table_extra_9` & 2nd-Hop Blockers

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or `scratch/t125/out/`. Write ONLY to `scripts/t136_big3_final_closure.py` and `scratch/t136/out/`.

## Context
Your `t125` run jumped Big-3 (1,034-field denominator) from `379/1034 (36.7%)` gross / `379/673 (56.3%)` net persisted to **`512/1034 (49.5%)` gross / `512/672 (76.2%)` net persisted**, cutting remaining gaps from `294` -> **`160`** (`club 84`, `nation 47`, `comp 29`).

Now we have **THREE major new evidence sources** on disk that directly attack those remaining 160 gaps:
1. **ALL 11 `priority_undecompiled` 2nd-hop VAs from `t125/out/remaining_gaps_v3.json` are NOW DECOMPILED** in `scratch/t132/out/funcs/` (`scratch/t132/out/ida_hop2_index.json`):
   - `0x14083dfa0` (`14083dfa0.c`, 17L — **38 held occurrences!**)
   - `0x1411eacb0` (`144028d40.c`, 109L — 4 held occurrences)
   - `0x144026350` (`144026350.c`, **4,641L!!** — 3 held occurrences)
   - `0x1407e4490` (`143671d70.c`, 47L), `0x14083b0a0` (`14377a980.c`, 78L), `0x14083db80` (`14083db80.c`, 36L), `0x140e58670` (`143c18010.c`, 63L), `0x140e5f8c0` (`143c1aa40.c`, 23L), `0x140fc9d50` (`143e007a0.c`, 21L), `0x141078de0` (`141078de0.c`, 193L), `0x141521aa0` (`1444ad080.c`, 41L)!
2. **100% Pure-Python Full-Table Decoders (`t133`)** in `scripts/t133_fm24_reader_v2.py` + `scratch/t133/out/reader_v2_verify.json` + `team_field_map_check.json`:
   - We now have **100% full-table wire grammars** (ZERO partial-trace ambiguity!) for ALL 84,259 `CLUB` rows (server & client), ALL 7,047 `COMP` rows (server & client), ALL 251 `NATION` & 251 `NTC` rows (server & client), ALL 84,507 `TEAM`/`NATIONAL_TEAM` rows, and ALL `STARTING_*` tables!
   - Also check `table_extra_9.dat` (and `table_extra_3.dat` / `table_extra_24.dat`) directly in `scratch/data/server_db.dat` (and `scratch/t133/out/static/` or `scratch/t95/funcs/`) — determine `table_extra_9`'s exact binary layout & whether any of the 47 Nation gaps bind to `table_extra_9`!
3. **13/13 Special Members Closed (`t106`)** in `scratch/t106/out/special_members_schema.json` (`club_links` 9,261×47B, `common_name_links` 12,056×10B, `simple_vars`, `name_table_*`) — check whether any `CLUB`/`NATION`/`COMP` gaps (e.g., club links / affiliations / names / non-DB runtime flags) are proven by `t106` or `t133`!

## Your Mission (Same Strict Rigor as `t125` — Zero Guessing, Every Upgrade Machine-Proven!)
Write `scripts/t136_big3_final_closure.py` (with `--selftest`) starting from `scratch/t125/out/big3_l3_v3.json` (preserving all 512 L3 rows & 362 exclusions unless a genuine bug is proven) and systematically resolve as many of the **160 remaining gaps** as strictly provable:
1. Analyze every newly decompiled 2nd-hop VA in `scratch/t132/out/funcs/` — especially `14083dfa0.c` (38 occurrences), `144028d40.c`, `144026350.c` (4,641L!), and `141078de0.c`! Note: if `0x14083dfa0` is a variant-assignment wrapper (value-boxing helper like `variant::assign`), trace the **upstream operand** passed into `0x14083dfa0` in each of the 38 branches inside `CLUB`/`NATION`/`COMP` `get_prop`!
2. Use `t133`'s **complete** `CLUB` (`server/client table_3`), `COMP` (`server/client table_25`), `NATION`/`NTC` (`table_9`/`table_10`), and `TEAM` (`table_24`) wire grammars to distinguish:
   - True persisted fields (L3 closed via main row, embedded base class, or `t133` verified sub-object/collection!)
   - True subtable-routed fields (including `table_extra_9`, `club_links`, `table_24`, `table_45`/`48`, `STARTING_*`!)
   - True non-persisted / computed / runtime-only / editor-only / savegame-only fields (**`excluded_non_db_l3`** — remember in `t125`, partial 50-row traces couldn't prove absence, whereas `t133` has the **COMPLETE** `CLUB`/`COMP`/`NATION`/`NTC` `slot19` C-derived wire grammar covering ALL 84,259 clubs & 7,047 comps!! If an offset is provably NEVER written in `CLUB::slot19` server OR client OR any of its callees AND is initialized to default/runtime-computed in ctor/get_prop, you can prove `excluded_non_db_l3` with exact C-code citations!).
3. You are also permitted to inspect `editor.exe` PE bytes (read-only) or run targeted `idalib` on `scratch/t95/editor_work.i64` (NEVER touch `editor_merge_v2.i64`!) ONLY if a tiny handful (< 15) of crucial 3rd-hop VAs unlock many gaps!
4. Strictly maintain **1,034 conservation** (`club 433 + nation 346 + comp 255 = 1,034`).

## Deliverables
Write `scripts/t136_big3_final_closure.py` (with `--selftest`) and `scratch/t136/out/`:
1. `big3_l3_v4.json` — full 1,034-entry classification with exact provenance
2. `coverage_summary_v4.json` — full progression table: `Baseline (110/1034 = 10.6%)` -> `t109 (379/1034, 56.3% net)` -> `t125 (512/1034, 76.2% net)` -> `t136 (?/1034, ?% net)`
3. `remaining_gaps_v4.json` — only truly irreducible/remaining gaps with exact blockers
4. `REPORT.md` — concise, rigorous engineering report
5. `DONE.md` — `DONE type=t136`, headline progression numbers, `--selftest` PASS

Run `py -V:3.12 -B scripts/t136_big3_final_closure.py` and `--selftest` before finishing!
