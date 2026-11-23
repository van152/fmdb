# t133 (`gpt-6.2-sol` max): Upgrade Pure-Python FM24 Reader from 66/79 to 79/79 (100% of `server_db.dat` + `client_db.dat`!)

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or `scripts/t112_fm24_reader.py`. Write ONLY to `scripts/t133_fm24_reader_v2.py` and `scratch/t133/out/`.

## Context
`scripts/t112_fm24_reader.py` ALREADY achieves **66 / 79 tables 100% footer-closed (`diff=0`, 1,942,341 rows in 6.4s)** in pure Python (stdlib + vendored `zstandard` at `D:\tmp2b\fm24\tools\python`, ZERO IDA / ZERO Unicorn at runtime!), leaving **ONLY 13 / 79 tables skipped**:
1. `server/0` `AWARD` (3,545 rows — FIXED 76B body! `13 + 3545*(1+76) == len - 9`!)
2. `client/0` `AWARD` (3,545 rows — FIXED 76B body! `13 + 3545*(1+76) == len - 9`!)
3. `server/32` `STARTING_FUTURE_TRANSFER` (315 rows, variable 59..211B — closed in `t119`!)
4. `server/72` `STARTING_PAST_TRADE` (138 rows, variable 60..105B — closed in `t119`!)
5. `server/36` `STARTING_MANAGER_HOF_RECORD` (6,535 rows, variable — traced in `t96c`!)
6. `server/29` `STARTING_LOAN` (13,278 rows, variable — traced in `t96c`, missing helper `sub_1445195D0` NOW DECOMPILED in `scratch/t132/out/funcs/`!)
7. `server/9` & `client/9` `NATIONAL_TEAM_CONTAINER` (251 / 251 rows — closed in `t96c`!)
8. `server/25` `COMP` (7,047 rows — traced in `t96c`; `client/25` is ALREADY closed in `t112`!)
9. `server/3` & `client/3` `CLUB` (84,259 rows each — traced in `t96c`!)
10. `server/24` `NATIONAL_TEAM` (84,507 rows — traced in `t96c`!)
11. `server/71` `STARTING_PAST_TRANSFER` (616,665 rows — traced in `t119`, shared helper `sub_1411919D0` & `sub_1415782C0` NOW DECOMPILED in `scratch/t132/out/funcs/`!)

## Authoritative Inputs On Disk
- `scripts/t112_fm24_reader.py` (66/79 working pure-Python VM + fixed-stride engine — import or cleanly build upon it!)
- `scratch/t121/out/wire_traces_79of79.json` (**ALL 79/79 tables cleanly traced by Unicorn**, with exact `row0_reads` + `canonical_fields`!)
- `scratch/t121/out/master_79of79_l3.json` (**1,104 L3 4CC mappings** across 56/67 tables!)
- `scratch/t95/funcs/*.c`, `scratch/t124/out/funcs/*.c`, and **`scratch/t132/out/funcs/*.c`** (freshly decompiled `sub_1445195D0`, `sub_1411919D0`, `sub_1415782C0`, `sub_141541000`, `sub_141541480`, `sub_141726770`, etc.!)
- `scratch/t95/vtable_index.json` (exact `slot19` C filenames for all 67 classes)
- `scratch/data/server_db.dat` and `scratch/data/client_db.dat` (READ-ONLY)

## Your Mission (Aim for 79/79 = 100% Pure-Python Byte-Exact Footer Closure!)
Build `scripts/t133_fm24_reader_v2.py` (extending `t112`'s architecture, using `t121`'s `wire_traces_79of79.json` + `master_79of79_l3.json`!) to close ALL 13 remaining tables (`server/client t0 AWARD`, `server/32`, `server/72`, `server/36`, `server/29`, `server/client t9 NTC`, `server/25 COMP`, `server/client t3 CLUB`, `server/24 NATIONAL_TEAM`, `server/71 STARTING_PAST_TRANSFER`):

1. **Tier 1 (Immediate wins — must close 100%!)**:
   - `server/0` & `client/0` `AWARD` (3,545 rows each, fixed 76B + 1B flag, `diff=0`)
   - `server/32` `STARTING_FUTURE_TRANSFER` (315 rows, `diff=0`)
   - `server/72` `STARTING_PAST_TRADE` (138 rows, `diff=0`)
   - `server/36` `STARTING_MANAGER_HOF_RECORD` (6,535 rows, `diff=0`)
   - `server/29` `STARTING_LOAN` (13,278 rows, `diff=0`)
   - `server/9` & `client/9` `NATIONAL_TEAM_CONTAINER` (251 rows each, `diff=0`)
2. **Tier 2 (Big variable tables — push all the way to 79/79!)**:
   - `server/25` `COMP` (7,047 rows, `diff=0`)
   - `server/24` `NATIONAL_TEAM` (84,507 rows, `diff=0` — remember polymorphic `flag == 11`!)
   - `server/3` & `client/3` `CLUB` (84,259 rows each, `diff=0` — remember polymorphic `flag == 12` → `LEAGUE_BODY_CLUB`!)
   - `server/71` `STARTING_PAST_TRANSFER` (616,665 rows, `diff=0` — uses `sub_1411919D0` + `sub_1415782C0`!)
3. **Strict Engineering Rules**:
   - Pure Python ONLY at runtime (stdlib + vendored `zstandard` at `D:\tmp2b\fm24\tools\python`, NO IDA, NO Unicorn!).
   - EVERY table marked `footer_closed == true` MUST actually walk ALL `rows_header` rows from `pos = 13` and land at EXACTLY `pos == len(payload) - 9` (`diff == 0`) with NO heuristic identity-skipping hacks! Every branch must match the real `slot19` C code (and if any single table has a missing sub-callee you cannot prove from `.c` + byte verification, report it honestly as `skipped` with the exact missing callee VA — never fake closure!).
   - Support CLI flags: `--list`, `--dump <archive> <tid> --limit N`, `--verify-all`, `--selftest`.
   - Optimize hot loops (`struct.unpack_from`, local bindings) so `--verify-all` across all closed tables runs in well under 30 seconds!

## Deliverables
Write `scripts/t133_fm24_reader_v2.py` (with `--selftest` and `--verify-all`) and `scratch/t133/out/`:
1. `reader_v2_verify.json` — full verification output across all 79 tables (`tables_closed`, `tables_failed`, `tables_skipped`, `rows_decoded_total`, `elapsed_total_ms`, `l3_named_field_total`, sample rows for newly added tables!)
2. `REPORT.md` — concise engineering report comparing `t112 (66/79, 1,942,341 rows)` vs `t133 (?/79, ? rows)`, documenting each newly closed table's exact wire grammar
3. `DONE.md` — `DONE type=t133`, headline counts (`?/79 tables footer_closed`, total rows decoded, elapsed time, `--selftest` PASS)

Run `py -V:3.12 -B scripts/t133_fm24_reader_v2.py --verify-all` and `py -V:3.12 -B scripts/t133_fm24_reader_v2.py --selftest` before finishing.
