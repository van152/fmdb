# t137b: Finish `t137` — `NON_PLAYER` Attribute L3 Map + Top-20 World Managers Decoded from 400 MB `people_db.dat`

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t137_non_player_managers_l3.py` and `scratch/t137/out/`.
CRITICAL: Keep stdout tiny (< 40 lines per command) so you NEVER trigger auto-compaction! Go straight to writing code and staging JSON outputs!

## Already Verified in `scratch/t137/out/` (DO NOT RE-EXPLORE!)
- `scratch/t137/out/_explore_getprop.py`, `_explore2.py`, and `scratch/t137/out/ida/` already exist.
- Verified exact locating predicate for Top-20 `ptype == 1` (`NON_PLAYER`) records in 400 MB `people_db.dat`:
  - Search for trailing 12B identity `struct.pack('<III', ordinal, uid, uid)` -> `ident_pos`, then find preceding header `[u32 ordinal][u8 1]` at `hit` with `0 < ident_pos - hit - 5 <= 2600`, verify `res["ok"] and res["bytes_consumed"] - 12 == ident_pos - hit - 5`!
- Verified inputs on disk:
  - `scratch/t124/out/funcs/140dca880.c` (`NON_PLAYER::get_prop`, 2,524L), `140dc8c00.c` (`NON_PLAYER::set_prop`, 1,212L), `140dc7180.c` (`reg_prop`), `140dc40f0.c` (`write`)
  - `scratch/t120/out/funcs/140dc1d30.c` (`NON_PLAYER::slot19`, 870L)
  - `scratch/t120/out/people_unicorn_traces.json` (`samples_by_type["1"]`, virtual base `0xf8`)
  - `scratch/t106/out/payload_server_name_table_extra_{0,1,2}.bin` (UTF-8 name pools)
  - `basic_people_db.dat`: `CA` at `+48`, `PA` at `+50`, `birth_year` at `+52`, `uid` at `+75`!

## Immediate Execution Steps (Write Deliverables Directly!)
1. Extract ALL `NON_PLAYER` 4CC ↔ `(obj_off, wire_off, get_line, set_line)` mappings from `140dca880.c` / `140dc8c00.c` / `scratch/t137/out/ida/` (if `sub_140DCA530` or any attribute-block sub-handler is needed, decompile it in 10s via `idalib` on `scratch/t95/editor_work.i64`, NEVER `editor_merge_v2.i64`, OR use Unicorn `get_prop`/`set_prop` memory-diffing on a live deserialized `NON_PLAYER` object!).
2. Locate and decode the **Top-20 highest-CA `ptype == 1` managers/staff** from 400 MB `people_db.dat` (in-memory only via `zstandard` from `D:\tmp2b\fm24\tools\python`), verify `ok == True`, `dbid == uid`, `CA/PA` 20/20 cross-check against `basic_people` `+48/+50`, resolve UTF-8 names via `name_table_extra_{0,1,2}`, and verify all decoded attributes fall in `0..20`.
3. Write `scripts/t137_non_player_managers_l3.py` (with `--selftest` and `--uid <UID>`), run BOTH `py -V:3.12 -B scripts/t137_non_player_managers_l3.py` and `--selftest`, and produce all 4 deliverables in `scratch/t137/out/`:
   - `non_player_attributes_l3.json`
   - `top20_managers_cards.json`
   - `REPORT.md`
   - `DONE.md` (first line `DONE type=t137`, counts, `--selftest` PASS)
