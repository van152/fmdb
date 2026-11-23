# t126c: Land `t126` Deliverables — Complete 69-Byte `PLAYER_DATA` (54 `PDxx` + 15 Positions) + All-5-Types L3 + Real Player Cards

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t126_player_attributes_l3.py` and `scratch/t126/out/`.

## IMPORTANT EXECUTION RULE (KEEP CONTEXT SMALL!)
- Do **NOT** print large `.c` files (`140e27b10.c`, `140dca880.c`, `d_141465590.c`, etc.) to stdout! Use small Python scripts to parse them programmatically and print only compact summary stats (< 80 lines per command).
- Stage deliverables directly into `scripts/t126_player_attributes_l3.py` and `scratch/t126/out/` so you finish cleanly in 1 attempt!

## Exact Verified Facts Already On Disk
1. **69-Byte `PLAYER_DATA` Block** (`wire 29..97`, `obj_off = -0x70..-0x2c`, `a1 - 112 .. a1 - 44` in `PLAYER::slot19` `scratch/t120/out/funcs/140e06ec0.c`):
   - **Bytes `15..68` (54 attributes)**: BOTH GET (`scratch/t126/out/ida/d_141465590.c`, 1,150L) and SET (`scratch/t126/out/ida/test_141467b70.c`, 462L) map ALL 54 `PDxx` 4CCs (including the 7 `else`-branch indices `20, 26, 30, 40, 46, 58, 62` — handle `else` branches carefully so ALL 54/54 indices `15..68` match identically on GET and SET!).
   - **Bytes `0..14` (15 bytes, `a1 - 112 .. a1 - 98`)**: Check `scratch/t124/out/funcs/140e27b10.c` (`PLAYER::get_prop`) and `140e24f30.c` (`PLAYER::set_prop`) for `a1 - 112 .. a1 - 98` (e.g., position ratings `Pgoa`/`Pswp`/`Pdlf`/etc. or `PPxx` 4CCs!). If any 4CCs map to `a1 - 112 .. a1 - 98`, extract them with exact line numbers; otherwise mark any unmapped bytes honestly.
2. **Real `name_table_extra_{0,1,2}` UTF-8 Strings (`t106` ALREADY CLOSED 13/13!)**:
   - Note from `scratch/t106/out/REPORT.md`: `name_table_{0,1,2}` has 12B metadata rows (`245,981 / 542,060 / 85,668`), while **`scratch/t106/out/payload_server_name_table_extra_{0,1,2}.bin`** holds the actual UTF-8 strings (`uid == ordinal == row index`, format `12B header + [u32 uid][u32 slen][utf8 bytes]`)!
   - You can import or reuse `scripts/t106_special_members.py` to resolve `first_name_id`, `second_name_id`, `common_name_id` directly to **REAL PLAYER NAMES**!
3. **All 5 Person Classes (`scratch/t120/out/people_unicorn_traces.json` + `scratch/t124/out/funcs/` + `scratch/t120/out/funcs/`)**:
   - `PLAYER` (`140e27b10.c` / `140e24f30.c` / `140e06ec0.c`, virtual base `+0x278`)
   - `NON_PLAYER` (`140dca880.c` / `140dc8c00.c` / `140dc1d30.c`, virtual base `+0xf8`)
   - `ACTUAL_PLAYER_AND_NON_PLAYER` (`1415d5750.c` / `1415d5110.c`, virtual base `+0x368`)
   - `OFFICIAL` (`1415870a0.c` / `1415856b0.c`, virtual base `+0x138`)
   - `RETIRED_PERSON` (`143f8b4b0.c` / `143f891c0.c`, virtual base `+0x0`)
   - For the 3 sample `PLAYER` rows in `people_unicorn_traces.json`, recover their full 69-byte `PLAYER_DATA` slice directly from `scratch/data/people_db.dat` (decompressed prefix via `zstandard` from `D:\tmp2b\fm24\tools\python`) using `file_off + 5 + 29` (length 69), plus CA/PA/Rep (`+0..+9`), Height/Weight (`+126..+133`), Name IDs (`first_name_id`, `second_name_id`, `common_name_id`), and `identity` (`uid`).

## Deliverables
Write `scripts/t126_player_attributes_l3.py` (with `--selftest`) and `scratch/t126/out/`:
1. `player_69b_attributes_l3.json` — exact byte-by-byte map of all 69 bytes (`0..68`, wire `29..97`, `obj_off -0x70..-0x2c`), proving 54/54 `PDxx` GET==SET agreement + bytes `0..14` findings + `PLAYER` `0..147` header map
2. `people_all5_l3_master.json` — all 5 person classes' 4CC ↔ `mem_off` ↔ Unicorn wire L3 joins + 3 fully decoded FM24 player cards with real names & all 54 `PDxx` values validated in `0..20`
3. `REPORT.md` — clean markdown tables of all 69 bytes (`PLAYER_DATA`), `NON_PLAYER`/`OFFICIAL`/`RETIRED` L3 counts, and the 3 decoded FM24 player attribute cards
4. `DONE.md` — first line `DONE type=t126`, headline metrics (`54/54 PDxx GET==SET`, bytes `0..14` count, total L3 4CCs across all 5 classes, `--selftest` PASS)

Run `py -V:3.12 -B scripts/t126_player_attributes_l3.py` and `py -V:3.12 -B scripts/t126_player_attributes_l3.py --selftest` before finishing!
