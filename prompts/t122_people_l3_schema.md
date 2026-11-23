# t122: `people_db.dat` Full L3 Schema (All 5 Person Types + 69-Byte `PLAYER_DATA` + `PERSON`/`CONTRACT` Join)

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t122_people_l3_schema.py` and `scratch/t122/out/`.

## Goal
`t120` just achieved a **3,000 / 3,000 (`err=None`, 9.81s)** native Unicorn walkthrough across ALL 5 on-disk person types in the 400 MB `people_db.dat` archive:
- Type 1 (`NON_PLAYER`): 481 rows (body 311..831 B, 185 unique lengths)
- Type 2 (`PLAYER`): 1,283 rows (body 457..1,286 B, 375 unique lengths)
- Type 3 (`ACTUAL_PLAYER_AND_NON_PLAYER`): 9 rows (body 737..1,007 B, 9 unique lengths)
- Type 4 (`OFFICIAL`): 34 rows (body 115..127 B, 3 unique lengths)
- Type 5 (`RETIRED_PERSON`): 1,193 rows (body 28..67 B, 29 unique lengths)

And `t120b` decompiled ALL 9 core readers/writers into `scratch/t120/out/funcs/`:
- `140e06ec0.c` (`PLAYER_slot19_body`, 712L)
- `14145f800.c` (`PLAYER` sub-object reader, 425L)
- `140dc1d30.c` (`NON_PLAYER_slot19_body`, 870L)
- `1415d5110.c` (`ACTUAL_PLAYER_AND_NON_PLAYER_slot19`, 21L)
- `1415856b0.c` (`OFFICIAL_slot19`, 253L)
- `143f891c0.c` (`RETIRED_PERSON_slot19`, 56L)
- `1415d8630.c` (`JOURNALIST_slot19`, 77L)
- `143f2b820.c` (`PERSON_slot19_base`, 76L)
- `143f2bc10.c` (`PERSON_slot21_write`, 32L)

## Authoritative Inputs On Disk
1. `scratch/t120/out/people_unicorn_traces.json` (factory table + 3,000-row stats + full read-by-read Unicorn traces for 3 real sample rows of EACH of types 1, 2, 3, 4, 5!)
2. `scratch/t120/out/funcs/*.c` (the 9 freshly decompiled `people_db.dat` readers/writers)
3. `scratch/t118/out/people_4cc_mem.json` (754 extracted getter/setter 4CC ↔ `mem_off` records) and `scratch/t113/out/funcs/*.c` (`14109ad50.c` `PERSON::get_prop`, `141201ae0.c` `CONTRACT::get_prop`, `140eec1b0.c`, `140ee0800.c`, etc.)

## Required Analysis
1. **Unicorn × IDA L3 Range-Aware Join for ALL 5 Person Types (`NON_PLAYER`, `PLAYER`, `ACTUAL_PLAYER_AND_NON_PLAYER`, `OFFICIAL`, `RETIRED_PERSON`)**:
   - For each sample trace in `scratch/t120/out/people_unicorn_traces.json`, classify every read step (`wire_pos`, `n`, `base_off`, `obj_off`, `caller_va`, `hex`) into:
     - Subclass header/fixed section (e.g., `PLAYER` CA/PA/Reps at `wire 0..10`, flags, 69-byte `PLAYER_DATA` block at `wire 29..98`, dates, weight/height, `sub_14145F800`, etc.)
     - Embedded sub-objects (`CONTRACT`, `PERSON` base class, `name_id` triplet, trailing 12B identity `[ordinal, dbid, uid]`)
   - Join every `obj_mem` read (`base_off` / `obj_off` range `[off, off+n)`) against `scratch/t118/out/people_4cc_mem.json` (`PERSON`, `CONTRACT`, `PLAYER`, `BASIC_PERSON`) — explicitly tracking virtual-base offset adjustment (`obj_offset_from_base` from `t120/out/people_unicorn_traces.json`: e.g. `NON_PLAYER=+0xf8`, `PLAYER=+0x278`, `ACTUAL_PLAYER_AND_NON_PLAYER=+0x368`, `OFFICIAL=+0x138`, `RETIRED_PERSON=+0x0`)!
2. **Exact `PLAYER` Fixed-Header & 69-Byte Attribute Block Map**:
   - From `140e06ec0.c` + `t120` Unicorn `PLAYER` traces (`samples_by_type["2"]`), produce the exact byte-by-byte map of `PLAYER` wire offsets `0..147` (before `sub_14145F800`), including the exact `base_off` and `obj_off` of every field (`a1 - 126` = 10B CA/PA/HomeRep/CurrentRep/WorldRep, `a1 - 112` = 69B attribute block, `a1 - 304` = weight/height, etc.), and cross-reference against `t118`'s `people_4cc_mem.json` + `scratch/t113/out/funcs/` for any `PDxx` / `Pxxx` 4CCs that map into `a1 - 112 .. a1 - 43`!
3. **Strict Honesty**:
   - Distinguish L3-joined (Unicorn read + IDA offset/4CC match) vs Unicorn-wire-verified (exact byte width + `obj_off` verified by `t120`, 4CC not yet decompiled) vs static-only. Do NOT invent attribute names unless backed by a 4CC/C-code citation.

## Deliverables
Write `D:\tmp2b\fm24-db\scripts\t122_people_l3_schema.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t122\out\`:
1. `people_l3_schema.json` — structured L3 schema for all 5 person types (`1..5`), virtual-base offsets, `PLAYER` 0..147 byte map, and all joined 4CCs
2. `REPORT.md` — clear markdown report with tables for all 5 person types and the `PLAYER` header/69B attribute region
3. `DONE.md` — `DONE type=t122`, key counts (joined 4CCs per person type, verified wire fields), `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t122_people_l3_schema.py` and `--selftest` before finishing.
