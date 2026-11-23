# t126: 400 MB `people_db.dat` Complete 69-Byte `PLAYER_DATA` Attribute Map + All-5-Types L3 4CC Schema + Star Verification

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t126_player_attributes_l3.py` and `scratch/t126/out/`.

## Breakthrough Inputs Just Decompiled by IDA 9.4 (`t124`)
We now have BOTH the **3,000-row 0-error native Unicorn walkthrough** of `people_db.dat` (`scratch/t120/out/people_unicorn_traces.json`) AND the **COMPLETE Hex-Rays decompilations** of ALL 6 person classes' `get_prop`, `set_prop`, `reg_prop`, `slot19` (read), and `slot21` (write)!!

Look at `scratch/t124/out/funcs/` (and `scratch/t124/out/ida_index.json`):
- `140e27b10.c` — **`PLAYER::get_prop`** (**3,287 lines!**)
- `140e24f30.c` — **`PLAYER::set_prop`** (**1,974 lines!**)
- `143bdeaf0.c` — **`PLAYER::reg_prop`** (143 lines)
- `140e089c0.c` — **`PLAYER::write`** (777 lines)
- `140dca880.c` — **`NON_PLAYER::get_prop`** (**2,524 lines!**)
- `140dc8c00.c` — **`NON_PLAYER::set_prop`** (**1,212 lines!**)
- `140dc7180.c` — **`NON_PLAYER::reg_prop`** (842 lines)
- `140dc40f0.c` — **`NON_PLAYER::write`** (335 lines)
- `1415870a0.c` — **`OFFICIAL::get_prop`** (1,083 lines) & `141586a80.c` (`set_prop`) & `141585e80.c` (`write`)
- `1415d9070.c` — **`JOURNALIST::get_prop`** (651 lines) & `1415d8da0.c` (`set_prop`) & `1415d8860.c` (`write`)
- `143f8b4b0.c` — **`RETIRED_PERSON::get_prop`** (133 lines) & `143f8b380.c` (`set_prop`)
- `1415d5750.c` — **`ACTUAL_PLAYER_AND_NON_PLAYER::get_prop/set_prop/write`**

Plus `scratch/t120/out/funcs/`:
- `140e06ec0.c` (`PLAYER::slot19` 712L), `14145f800.c` (425L), `140dc1d30.c` (`NON_PLAYER::slot19` 870L), `1415856b0.c` (`OFFICIAL::slot19` 253L), `143f891c0.c` (`RETIRED_PERSON::slot19` 56L), `143f2b820.c` (`PERSON::slot19` 76L).

## Your Mission
1. **Map ALL 69 Bytes of `PLAYER_DATA` (`wire 29..97` ↔ `obj_off = -0x70..-0x2c`, i.e., `a1 - 112 .. a1 - 44` in `140e06ec0.c`) + Full `PLAYER` Wire Header (`0..147`) to Exact 4CCs**:
   - Parse `PLAYER::get_prop` (`140e27b10.c`, 3,287L) and `PLAYER::set_prop` (`140e24f30.c`, 1,974L)!
   - Remember virtual-base adjustment: in `PLAYER` (`obj_offset_from_base = 0x278` from `t120`), `PLAYER::slot19` receives `a1 = DATABASE_OBJECT*` (`base + 0x278`), so `a1 - 126` (`-0x7e`, `base + 0x1fa`) is the 10-byte CA/PA/Rep header (`wire 0..9`), and **`a1 - 112` (`-0x70`, `base + 0x208`) is byte 0 of the 69-byte `PLAYER_DATA` block (`wire 29..97`)**! Check the exact `this`-adjustment in `140e27b10.c` (`PLAYER::get_prop`) so every single byte `0..68` of the 69-byte block (Technical, Mental, Physical, Goalkeeping, Hidden, Positions, Preferred Foot, etc.) is matched to its exact 4CC and human-readable FM24 attribute name (if grounded in `editor.exe` / XML / `t01` / 4CC mnemonic — mark any unconfirmed mnemonic clearly as 4CC-only!).
2. **Extract Full 4CC ↔ `mem_off` ↔ Unicorn Wire Schema for ALL 5 On-Disk Person Classes**:
   - `PLAYER` (`140e27b10.c` + `140e24f30.c` + `140e06ec0.c` + `t120` traces)
   - `NON_PLAYER` (`140dca880.c` + `140dc8c00.c` + `140dc1d30.c` + `t120` traces — including all staff/manager attributes!)
   - `ACTUAL_PLAYER_AND_NON_PLAYER` (`1415d5750.c` + `1415d5110.c` + `t120` traces)
   - `OFFICIAL` (`1415870a0.c` + `1415856b0.c` + `t120` traces)
   - `RETIRED_PERSON` (`143f8b4b0.c` + `143f891c0.c` + `t120` traces)
3. **Decode Real FM24 Player Cards from `t120`'s Sample `PLAYER` Records (and Cross-Verify with `name_table_0/1/2` if available)**:
   - Using the extracted 69-byte `PLAYER_DATA` byte map + CA/PA/Rep (`wire 0..9`) + Weight/Height (`wire 126..133`) + Name IDs (`first_name_id`, `second_name_id`, `common_name_id` in `t120` trace!), decode the 3 sample `PLAYER` rows in `scratch/t120/out/people_unicorn_traces.json` into full readable FM24 player attribute cards (showing every byte value `0..20`, CA, PA, Height, Weight, UID, and name if resolved via `scratch/t106/out/payload_server_name_table_{0,1,2}.bin`)!
   - Verify every decoded attribute is in its valid FM24 range (`0..20` for standard attributes, `0..200` for CA/PA, plausible height/weight in cm/kg)!

## Deliverables
Write `D:\tmp2b\fm24-db\scripts\t126_player_attributes_l3.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t126\out\`:
1. `player_69b_attributes_l3.json` — exact byte-by-byte map of all 69 bytes of `PLAYER_DATA` (`wire 29..97`) + `PLAYER` `0..147` header with 4CCs & C source lines
2. `people_all5_l3_master.json` — full Unicorn × IDA L3 join across all 5 person classes (`PLAYER`, `NON_PLAYER`, `ACTUAL_PLAYER_AND_NON_PLAYER`, `OFFICIAL`, `RETIRED_PERSON`) + decoded real player cards
3. `REPORT.md` — clean markdown tables showing the complete 69-byte `PLAYER_DATA` attribute map, `NON_PLAYER` attribute map, and decoded real player cards
4. `DONE.md` — `DONE type=t126`, exact counts (`?/69` `PLAYER_DATA` bytes L3-mapped, total L3 4CCs per person class), `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t126_player_attributes_l3.py` and `py -V:3.12 -B scripts/t126_player_attributes_l3.py --selftest` before finishing.
