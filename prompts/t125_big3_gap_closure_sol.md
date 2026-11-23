# t125 (`gpt-6.2-sol` max): Big-3 Remaining 294 Gaps Deep Evidence Closure (with Newly Decompiled 33 Blocker Helpers!)

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t125_big3_gap_closure.py` and `scratch/t125/out/`.

## Context & Breakthrough Inputs
Earlier, `t109` raised the Big-3 (`CLUB`, `NATION`, `COMP`) 1,034-field denominator from `110/1034 (10.6%)` to `379/1034 (36.7%)` gross / `379/673 (56.3%)` net persisted, leaving **294 gaps** in `scratch/t109/out/remaining_gaps.json`:
- `gap_off_not_in_read_stream`: 141 (Club 75, Nation 64, Comp 2)
- `gap_helper_computed`: 85 (Club 32, Nation 25, Comp 28)
- `gap_delegated_or_empty`: 34 (Club 21, Comp 13)
- `gap_child_off_not_in_child_stream`: 21 (Club 7, Nation 7, Comp 7)
- `gap_other_table_same_tag`: 13 (Club 7, Nation 3, Comp 3)

Previously `t117` upgraded 0/294 because the **top 33 blocker helper functions** listed in `remaining_gaps.json` (`0x140e8a400` 131 rows, `0x140ec0a60` 69 rows, `0x141063f30` 54 rows, `0x1411f1090` 32 rows, `0x141545680` 28 rows, `0x140fe3f20` 15 rows, `0x1410668f0` 15 rows, `0x1415446a0` 14 rows, `0x1411f4f70` 12 rows, etc.) were **NOT DECOMPILED**!

**NOW ALL 33 BLOCKER HELPERS HAVE BEEN DECOMPILED BY IDA PRO 9.4 HEX-RAYS!**
- See `scratch/t124/out/ida_index.json` and `scratch/t124/out/funcs/*.c`!
- Plus the full 1,173-file corpus in `scratch/t95/funcs/*.c`!
- Plus `scratch/t121/out/wire_traces_79of79.json` (100% 79/79 Unicorn runtime traces, including `CLUB` `table_3`, `NATION` `table_9` + `NAT_TEAM_CONT` `table_10` 251/251, `COMP` `table_25`!)
- Plus `scratch/t98/out/table45_full_schema.json` (100% byte-exact closure of `table_45` `STARTING_RECORD`, all 18 physical columns `this+0x18..0x5e` and 117 accessors!)
- Plus `scratch/t108/out/table_4cc_mem_v2.json` and `scratch/t109/out/{big3_l3_join.json, remaining_gaps.json, coverage_summary.json}`!

## Your Mission (Be Thorough, Rigorous, Machine-Proven — Do NOT Punt, Do NOT Guess)
Write a real static+Unicorn evidence-resolution engine `scripts/t125_big3_gap_closure.py` (with `--selftest`) that ACTUALLY READS AND ANALYZES the newly decompiled C code in `scratch/t124/out/funcs/` + `scratch/t95/funcs/` + `scratch/t121/out/wire_traces_79of79.json` + `scratch/t98/out/table45_full_schema.json` to classify EVERY ONE of the 294 gaps with verifiable citations (`file:line` or Unicorn trace `(archive, table_id, wire_off, obj_off, caller_va)`):

1. **Crack the 141 `gap_off_not_in_read_stream` (Club 75, Nation 64, Comp 2)**:
   - Why were 75 Club offsets and 64 Nation offsets in `get_prop/set_prop` not directly visible in `t109`'s top-level `read_from_stream` scan?
   - Check EVERY callee of `CLUB::slot19` (`140e5b1a0.c` / `140e5cf50.c`), `NATION::slot19` (`141063f30.c` / `1410668f0.c` / `table_9` + `table_10` `NATIONAL_TEAM_CONTAINER`!), and `COMP::slot19`, AND cross-check against `t121/out/wire_traces_79of79.json` (`table_3`, `table_9`, `table_10`, `table_25`)!
   - Crucial architectural check: Remember `NATION` (`table_10`) inherits from or embeds `NATIONAL_TEAM_CONTAINER` (`table_9`) / `TEAM_CONTAINER`! And `CLUB` (`table_3`) inherits from `TEAM_CONTAINER` (`0x140e8a400` = 131 rows!! `0x140ec0a60` = 69 rows!!)!
   - When a 4CC accesses an offset that IS read by an embedded base/sub-object serializer OR by `table_9`/`table_10`/`table_3`/`table_25` Unicorn `obj_off` range `[off, off+n)`, upgrade it to **`L3_unicorn_or_subobject_closed`** with exact `(va, file:line, obj_off, width)` proof!
   - When the decompiled code proves an offset is NEVER read from `.dat` (e.g., only set at runtime, editor-only, computed from other tables in `slot20`, or zero-initialized transient state), classify it as **`excluded_non_db_l3`** with exact code citation!

2. **Crack the 85 `gap_helper_computed` & 34 `gap_delegated_or_empty`**:
   - Parse the newly decompiled helpers in `scratch/t124/out/funcs/` (`0x140e8a400`, `0x140ec0a60`, `0x141063f30`, `0x1411f1090`, `0x141545680`, `0x140fe3f20`, `0x1410668f0`, `0x1415446a0`, `0x1411f4f70`, etc.)!
   - For every 4CC routed through those helpers, trace the helper body:
     - Does it read/write a persisted `mem_off` on `CLUB`/`NATION`/`COMP`? -> **`L3_helper_inlined_closed`**!
     - Does it delegate to a persisted child/subtable (e.g., `table_45 STARTING_RECORD`, `table_24 TEAM`, `table_21 STADIUM`, `table_33 DEBT`, `table_62 RESERVE_TEAM`, `table_66 TRANSFER_PREF`, `table_70 VISION`, `table_extra_3/9/24`, etc.)? -> **`L3_subtable_routed`** (naming exact target table + code citation)!
     - Does it perform pure runtime calculation / empty stub / editor-only / save-only operation? -> **`excluded_non_db_l3`** (with exact `file:line` citation)!

3. **Crack the 21 `gap_child_off_not_in_child_stream` & 13 `gap_other_table_same_tag`**:
   - Cross-check the 21 child-off items directly against `scratch/t98/out/table45_full_schema.json` (the 18 physical columns `this+0x18..0x5e` + 117 accessors) AND `scratch/t124/out/funcs/141545680.c` / `1415446a0.c` (`STARTING_RECORD` helpers!).
   - Cross-check the 13 `gap_other_table_same_tag` items against the actual `CLUB`/`NATION`/`COMP` handlers to determine whether they belong to a subtable or are non-DB.

4. **Strict Conservation & Zero Fabrication**:
   - Total denominator MUST stay exactly **1,034** (`club=433, nation=346, comp=255`).
   - Do NOT downgrade any of the 379 already-closed L3 items unless you discover a provable bug (if so, document explicitly).
   - Every single reclassification out of the 294 gaps MUST carry concrete machine-verifiable evidence (`source_file`, `line_no`, `helper_va`, `mem_off` or `target_table` or `exclusion_reason`).
   - Any gap that genuinely requires a 2nd-hop undecompiled VA stays honestly in `remaining_gaps_v3.json` with the exact next-hop VA list!

## Deliverables
Write `D:\tmp2b\fm24-db\scripts\t125_big3_gap_closure.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t125\out\`:
1. `big3_l3_v3.json` — full 1,034-entry upgraded classification with exact provenance per 4CC
2. `coverage_summary_v3.json` — exact `old (110/1034 = 10.6%)` -> `t109 (379/1034 gross, 379/673 = 56.3% net)` -> `t125` before/after comparison, per-entity breakdown (`club 433`, `nation 346`, `comp 255`), and breakdown of every upgraded class
3. `remaining_gaps_v3.json` — only truly remaining gaps + prioritized list of any 2nd-hop undecompiled VAs
4. `REPORT.md` — clear engineering summary with before/after tables and key helper findings (e.g., what `0x140e8a400`, `0x140ec0a60`, `0x141063f30`, `0x1411f1090`, `0x141545680` actually are!)
5. `DONE.md` — `DONE type=t125`, exact headline numbers (`gross ?/1034`, `net ?/?`, `gaps reduced 294 -> ?`), `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t125_big3_gap_closure.py` and `py -V:3.12 -B scripts/t125_big3_gap_closure.py --selftest` before finishing.
