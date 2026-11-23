# t121: Merge t96c (74/79) + t119 (5/5) into Unified 79/79 (100%) Master Trace & L3 Schema

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, `scratch/t96c/out/`, or `scratch/t110/out/`. Write ONLY to `scripts/t121_master_79of79.py` and `scratch/t121/out/`.

## Goal
`t119` closed the final 5/79 Unicorn database tables (`server/t0 AWARD` 3,545/3,545 `diff=0`, `client/t0 AWARD` 3,545/3,545 `diff=0`, `server/t32 STARTING_FUTURE_TRANSFER` 315/315 `diff=0`, `server/t72 STARTING_PAST_TRADE` 138/138 `diff=0`, `server/t71 STARTING_PAST_TRANSFER` 50/50 `sample_ok`), bringing Unicorn database coverage to **79/79 (100.0%, 0 failures)**.

Your job is to build a clean, deterministic merger + L3 schema refresh script `scripts/t121_master_79of79.py` (with `--selftest`) that:
1. **Merges `wire_traces_master.json` (`scratch/t96c/out/wire_traces_master.json`) + `last5_traces.json` (`scratch/t119/out/last5_traces.json`)** into `scratch/t121/out/wire_traces_79of79.json`:
   - Replace the 5 failed entries (`server/0`, `client/0`, `server/32`, `server/71`, `server/72`) with their clean `t119` counterparts.
   - Verify exact counts: **79 total tables**, **46 closed (`diff=0`)**, **33 `sample_ok`**, **0 failed** (`79/79 = 100.0%`).
2. **Extends the `t110` Range-Aware Unicorn × IDA L3 Join** (inspect `scripts/t110_master_l3_schema.py` to reuse its exact matching semantics and range rules!) across all 79 clean tables (including the 4 newly-closed table classes: `t0 AWARD`, `t32 STARTING_FUTURE_TRANSFER`, `t71 STARTING_PAST_TRANSFER`, `t72 STARTING_PAST_TRADE`):
   - Join `wire_traces_79of79.json` against `scratch/t108/out/table_4cc_mem_v2.json` and `scratch/t95/vtable_index.json`.
   - Report exact before (`t110`: 55/67 tables, 1,056 L3 4CC mappings) vs after (`t121`: how many tables joined & how many total L3 4CC mappings, plus the exact list of new L3 4CCs unlocked in `AWARD`, `t32`, `t71`, `t72`).
3. **Also check `t112` reader compatibility**:
   - Check which of the 5 newly-closed tables are fixed-length (`server/t0 AWARD` 76B, `client/t0 AWARD` 76B — exact `13 + 3545*(1+76) == len - 9`!) vs variable-length (`t32`, `t71`, `t72`), and document the exact `t112` upgrade spec in `REPORT.md`.

## Deliverables
Write `D:\tmp2b\fm24-db\scripts\t121_master_79of79.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t121\out\`:
1. `wire_traces_79of79.json`
2. `master_79of79_l3.json`
3. `REPORT.md` — concise summary table of all 79/79 tables + L3 uplift on `AWARD`/`t32`/`t71`/`t72`
4. `DONE.md` — `DONE type=t121`, key counts (`79/79`, `46 closed`, `33 sample_ok`, `0 failed`, L3 counts), `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t121_master_79of79.py` and `py -V:3.12 -B scripts/t121_master_79of79.py --selftest` before finishing.
