# t117: Big-3 Remaining 294 Gaps Closure (Unicorn + t98 + Sub-object Static Join)

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write only to `scripts/t117_big3_gap_closure.py` and `scratch/t117/out/`.

## Goal
`t109` lifted the Big-3 (`CLUB`, `NATION`, `COMP`) 1,034-field denominator from `110/1034 (10.6%)` to `379/1034 (36.7%)` gross / `379/673 (56.3%)` net persisted, leaving **294 gaps** in `scratch/t109/out/remaining_gaps.json`:
- `gap_off_not_in_read_stream`: 141 (Club 75, Nation 64, Comp 2)
- `gap_helper_computed`: 85 (Club 32, Nation 25, Comp 28)
- `gap_delegated_or_empty`: 34 (Club 21, Comp 13)
- `gap_child_off_not_in_child_stream`: 21 (7 each)
- `gap_other_table_same_tag`: 13

Your job is to systematically analyze and resolve as many of those 294 gaps as strictly provable (L3 or `excluded_non_db_l3` or `l3_subtable_routed` or `l3_unicorn_closed`) using ALREADY-GENERATED authoritative evidence — do NOT guess or fabricate any mapping.

## Authoritative Inputs Already On Disk
1. `scratch/t109/out/big3_l3_join.json`, `coverage_summary.json`, `remaining_gaps.json`
2. `scratch/t110/out/master_67tables_l3.json` (55/67 tables Unicorn × IDA execution-level L3 mappings, including `CLUB`, `NATION`, `NAT_TEAM_CONT`, `COMP`)
3. `scratch/t96c/out/wire_traces_master.json` (74/79 server+client Unicorn runtime traces, incl. `table_3` CLUB, `table_9` NATION 251/251, `table_10` NAT_TEAM_CONT 251/251, `table_25` COMP)
4. `scratch/t98/out/table45_full_schema.json` (100% byte-exact closure of `table_45` `STARTING_RECORD`, all 18 physical columns `this+0x18..0x5e`, 117 accessor ledger)
5. `scratch/t108/out/table_4cc_mem_v2.json` and `scratch/t95/funcs/*.c` (1,173 decompiled Hex-Rays functions from `t95` + `t107`, including `CLUB`/`NATION`/`COMP` sub-object serializers and helpers)
6. `scratch/t105/out/big3_serializers.json` (also check why `scripts/t105_big3_serializers.py --selftest` threw `KeyError: 'NTC::server'` — document the exact fix in your report, do NOT edit `t105_big3_serializers.py` unless clean; focus on `t117`)

## What to Investigate & Close
1. **Unicorn Execution Join on the 141 `gap_off_not_in_read_stream`**:
   - Why were 75 Club + 64 Nation offsets missed by `t109`'s static `read_from_stream` parser?
   - Check `t96c` Unicorn `mem_writes` for `server/client table_3` (`CLUB`), `server/client table_9` (`NATION`), `server/client table_10` (`NAT_TEAM_CONT`), `server/client table_25` (`COMP`) — specifically sub-object/nested struct writes (e.g. `CLUB` base class `TEAM_CONTAINER` / embedded `FINANCES` / `STADIUM` / `KIT` sub-reads, `NATION` embedded `NAT_TEAM_CONT` / `LANGUAGE` / `WEATHER` / vector-of-structs reads).
   - Also check `t95/funcs/` callees of `CLUB::slot19`, `NATION::slot19`, `COMP::slot19` to prove whether each offset is (a) actually read inside a callee sub-serializer (L3!), (b) populated by post-load resolver `slot20` / derived from another table (`excluded_non_db_l3` or `l3_subtable_routed`), or (c) genuinely runtime-only / not in `.dat` (`excluded_non_db_l3` with code citation!).
2. **`t98` `STARTING_RECORD` (`table_45`) Closure on the 21 `gap_child_off_not_in_child_stream`**:
   - Cross-check all 21 `gap_child_off_not_in_child_stream` items against `scratch/t98/out/table45_full_schema.json` (`this+0x18..0x5e` + 18 columns + 117 accessor ledger). Reclassify every provable item accurately.
3. **The 85 `gap_helper_computed` + 34 `gap_delegated_or_empty` + 13 `gap_other_table_same_tag`**:
   - Inspect their actual decompiled functions in `scratch/t95/funcs/`! Separate true persisted fields (via helper/delegate/subtable) from provably runtime/computed/editor-only/empty-setter properties (`excluded_non_db_l3`), citing exact file:line for every single reclassification.
4. **Strict Conservation & Honesty**:
   - Total denominator MUST stay exactly **1,034** (`club=433, nation=346, comp=255`).
   - Every item upgraded from a gap MUST cite verifiable machine evidence (Unicorn trace address + `mem_off` OR decompiled `funcs/<va>.c:line` + callee chain). Any item still unresolved remains in `remaining_gaps_v2.json` with an exact bucket and next-step reason.

## Deliverables
Write to `D:\tmp2b\fm24-db\scripts\t117_big3_gap_closure.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t117\out\`:
1. `big3_l3_v2.json` — full 1,034-entry upgraded classification with exact provenance per 4CC
2. `coverage_summary_v2.json` — before (`t109`) vs after (`t117`) table, per-entity breakdown, gross (`?/1034`) and net persisted (`?/net`) coverage
3. `remaining_gaps_v2.json` — only truly remaining gaps with exact blockers (e.g. which helper VA isn't decompiled yet)
4. `REPORT.md` — concise human-readable engineering report
5. `DONE.md` — `DONE type=t117`, key numbers, `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t117_big3_gap_closure.py` and `--selftest` before finishing.
