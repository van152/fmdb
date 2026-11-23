# t123: `basic_people_db.dat` (658,011 Rows) Full L3 Semantic Decoder + `name_table_0/1/2` Join + Real FM24 Top-50 Players

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t123_basic_people_l3.py` and `scratch/t123/out/`.

## Goal
`t115` proved 100% byte-exact closure of `basic_people_db.dat` (all **658,011 rows**, `diff=0`, widths `{1:83, 2:83, 3:83, 4:34, 5:22}`) and anchored Harry Kane (`28049320`: CA=184, PA=185, 1993), Cristiano Ronaldo (`735216`: CA=160, PA=200, 1985), and Lionel Messi (`7458500`: CA=200, PA=200, 1987), but left semantic columns and name-table joins unresolved.

Now we have ALL the missing pieces on disk:
1. `scratch/t113/out/funcs/140e4fd70.c` (`BASIC_PERSON::slot19_read_server`, 174 lines — COMPLETE exact byte layout!)
2. `scratch/t113/out/funcs/140e50cd0.c` (`BASIC_PERSON::get_prop`, 30KB) and `140e52de0.c` (`BASIC_PERSON::set_prop`, 17KB) and `140e50250.c` / `140e50880.c`
3. `scratch/t120/out/funcs/143f2b820.c` (`PERSON::slot19_base` = `sub_141084540`, 76 lines — exact trailing 8B + 12B identity!)
4. `scratch/t106/out/payload_server_name_table_0.bin`, `payload_server_name_table_1.bin`, `payload_server_name_table_2.bin` (already unpacked `name_table_0/1/2` payloads from `server_db.dat`!) — note: use `D:\tmp2b\fm24\tools\python` (`zstandard`) to decompress `scratch/data/basic_people_db.dat` cleanly on Windows (do NOT rely on `ctypes.util.find_library('zstd')` which fails on Windows without DLL on PATH!).
5. `scratch/t118/out/people_4cc_mem.json` (already parsed `BASIC_PERSON` 4CC ↔ `mem_off` mappings!)

## Required Work
1. **Exact L3 Byte Map of `basic_people_db.dat` (All 5 Widths: 83B, 34B, 22B)** from `140e4fd70.c` + `143f2b820.c` + `140e50cd0.c`:
   - Map EVERY SINGLE BYTE of the 83-byte record (`row+0` marker `0x11`, `row+1` `person_type`, `row+2..+82`) to its exact `BASIC_PERSON` `mem_off` (`+32, +40, +48, +56, +72..+104`, plus base `PERSON` `+24` 8B and `+8` 12B identity `[ordinal, dbid, uid]`) and its exact `BASIC_PERSON` 4CC from `140e50cd0.c`!
   - Verify exact byte arithmetic:
     - Types `1, 2, 3` (`_bittest` bit NOT set in `589856`/`852336`): total **83 bytes** (explain every single byte `0..82`!)
     - Type `4` (`OFFICIAL`): total **34 bytes** (explain every single byte `0..33` from `140e4fd70.c` lines 148–164 + `143f2b820.c`!)
     - Type `5` (`RETIRED_PERSON`): total **22 bytes** (explain every single byte `0..21` from `140e4fd70.c` line 41 + `143f2b820.c`!)
2. **Decode `name_table_0/1/2` (`first_name`, `second_name`, `common_name`) & Join with `basic_people_db.dat`**:
   - Inspect and decode `scratch/t106/out/payload_server_name_table_{0,1,2}.bin` (verify row count, exact footer closure, UTF-8 name strings).
   - Also check `sub_140FB2BA0(a2, a1 + 56)` (the 3 name IDs or name struct read at `140e4fd70.c` line 80 — check if `140fb2ba0.c` or similar is in `scratch/t95/funcs/`, or inspect bytes directly on Harry Kane / Cristiano Ronaldo / Lionel Messi!).
   - Verify that joining `basic_people_db.dat` with `name_table_0/1/2` resolves the **REAL FULL NAMES** of Harry Kane (`28049320`), Cristiano Ronaldo (`735216`), Lionel Messi (`7458500`), and produces a verified **Top-50 FM24 Players by CA** (with real Full Name, UID, person_type, CA, PA, birth year/date, nation/club IDs)!
3. **High-Speed Pure-Python CLI + `--selftest`**:
   - Support `--selftest`, `--uid <UID>`, `--search <NAME>`, `--top 50`, and full dump generation to `scratch/t123/out/`.
   - Must decompress `basic_people_db.dat` via `zstandard` (from `D:\tmp2b\fm24\tools\python`) so it runs reliably on Windows with zero external DLL dependencies.

## Deliverables
Write `D:\tmp2b\fm24-db\scripts\t123_basic_people_l3.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t123\out\`:
1. `basic_people_l3_complete.json` — complete byte-by-byte L3 schema for all 5 types + `name_table_0/1/2` stats + verified star anchors + Top-50 FM24 players with real names
2. `REPORT.md` — concise technical report + Top-50 FM24 players markdown table
3. `DONE.md` — `DONE type=t123`, key verification metrics, `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t123_basic_people_l3.py` and `--selftest` before finishing.
