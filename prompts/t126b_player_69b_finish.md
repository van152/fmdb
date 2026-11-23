# t126b: Finish `t126` — Extract 69-Byte `PLAYER_DATA` Attribute Map (`d_141465590.c` + `test_141467b70.c`) + All-5-Types L3 + Player Cards

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t126_player_attributes_l3.py` and `scratch/t126/out/`.

## ALREADY DISCOVERED & DECOMPILED ON DISK (DO NOT RE-DECOMPILE!)
In `scratch/t126/out/ida/`, the prior turn ALREADY found and decompiled BOTH exact `PLAYER_DATA` 69-byte attribute handlers:
- **GET side**: `scratch/t126/out/ida/d_141465590.c` (`sub_141465590(char *a1, int a2, __int64 *a3)`, 1,150 lines — reads `a1[0..68]`!)
- **SET side**: `scratch/t126/out/ida/test_141467b70.c` (`sub_141467B70` — 54+ 4CC→index cases, clamp 1..20!)
- **Also present**: `scratch/t126/out/ida/d_1414622c0.c` (2,593 lines) and check any other `.c` files in `scratch/t126/out/ida/`!

Plus `scratch/t124/out/funcs/` (`PLAYER::get_prop` `140e27b10.c`, `PLAYER::set_prop` `140e24f30.c`, `NON_PLAYER::get_prop` `140dca880.c`, `OFFICIAL::get_prop` `1415870a0.c`, `RETIRED_PERSON::get_prop` `143f8b4b0.c`), `scratch/t120/out/people_unicorn_traces.json` (3,000 rows, 15 sample traces across all 5 person types), and `scratch/t106/out/payload_server_name_table_{0,1,2}.bin` (name tables).

## Your Immediate Execution Plan (Go Straight to Code & Deliverables!)
1. Programmatically parse `d_141465590.c` (get) and `test_141467b70.c` (set) — plus check `d_1414622c0.c` — to build the COMPLETE `(byte_idx 0..68 ↔ 4CC ↔ hex_id ↔ get_line / set_line ↔ range/clamp)` table for all 69 bytes of `PLAYER_DATA` (`wire 29..97` of `PLAYER`, `obj_off -0x70..-0x2c`). Also check `editor.exe` strings or existing repo files (`scratch/t01/`, `reports/` READ-ONLY) for any grounded FM24 attribute names matching those 4CCs (mark ungrounded ones clearly as 4CC-only).
2. Reconcile the `PLAYER` wire header `0..147` (`CA/PA/Rep` at `wire 0..9`, `69B PLAYER_DATA` at `wire 29..97`, `weight/height` at `wire 126..133`, etc.) using `scratch/t124/out/funcs/140e27b10.c` + `140e24f30.c` + `scratch/t120/out/funcs/140e06ec0.c`.
3. Extract `NON_PLAYER` (`140dca880.c` + `140dc1d30.c`), `ACTUAL_PLAYER_AND_NON_PLAYER` (`1415d5750.c` + `1415d5110.c`), `OFFICIAL` (`1415870a0.c` + `1415856b0.c`), and `RETIRED_PERSON` (`143f8b4b0.c` + `143f891c0.c`) 4CC ↔ `mem_off` ↔ Unicorn wire joins.
4. Decode the 3 sample `PLAYER` rows in `scratch/t120/out/people_unicorn_traces.json` into full readable FM24 player attribute cards (all 69 bytes labeled by 4CC, CA/PA/Rep, Height/Weight, UID, and resolved First/Second/Common name from `scratch/t106/out/payload_server_name_table_{0,1,2}.bin`).
5. Write `scripts/t126_player_attributes_l3.py` (with `--selftest`), run BOTH `py -V:3.12 -B scripts/t126_player_attributes_l3.py` and `--selftest`, and write all 4 deliverables in `scratch/t126/out/`:
   - `player_69b_attributes_l3.json`
   - `people_all5_l3_master.json`
   - `REPORT.md`
   - `DONE.md` (starting with `DONE type=t126`)
