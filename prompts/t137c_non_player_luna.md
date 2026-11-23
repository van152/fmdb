# t137c: Finish `t137` — `NON_PLAYER` Attribute L3 Map + Top-20 World Managers Decoded from 400 MB `people_db.dat`

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t137_non_player_managers_l3.py` and `scratch/t137/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` for `zstandard`.

## All Decompilations & Offset Algebra ALREADY VERIFIED On Disk!
1. **Decompiled `NON_PLAYER` C files**:
   - `scratch/t124/out/funcs/140dca880.c` (`NON_PLAYER::get_prop`, 2,524L)
   - `scratch/t124/out/funcs/140dc8c00.c` (`NON_PLAYER::set_prop`, 1,212L)
   - `scratch/t124/out/funcs/140dc7180.c` (`NON_PLAYER::reg_prop`, 842L)
   - `scratch/t120/out/funcs/140dc1d30.c` (`NON_PLAYER::slot19`, 870L)
   - **`scratch/t137/out/ida/140dc4db0.c`** (`sub_140DC4DB0`, 16.8 KB — `NON_PLAYER` attribute index block `idx 0..29` & `33..39`! Helper receives `this - 248`, so `obj_off = helper_byte_off - 248`, e.g., `Npja` idx 15 → `obj_off = -196`, matching `set_prop` `*(_BYTE *)(a1 - 196)`!)
   - **`scratch/t137/out/ida/140dca530.c`** (`sub_140DCA530`, 5.9 KB — `NTxx` → id dispatcher, 54 codes)
2. **Verified Unicorn `NON_PLAYER` Wire Trace (`scratch/t120/out/people_unicorn_traces.json`)**:
   - `samples_by_type["1"]` has 3 full read-by-read traces (`obj_offset_from_base = 0xf8`, `obj_off = base_off - 0xf8`).
   - Do NOT call live `get_prop`/`set_prop` in Unicorn (`0x140dca8bc` touches uninitialized `qword_141B5EC88`); use static C parse (`get_prop` + `set_prop` + `140dc4db0.c`) joined to `samples_by_type["1"]` `(obj_off -> wire_off)` + empirical `0..20` range verification on decoded Top-20 managers!
3. **Verified Exact Top-20 Manager Locating Predicate in 400 MB `people_db.dat` (in-memory only!)**:
   - Scan `scratch/data/basic_people_db.dat` (`ptype == 1`, `CA` at `+48`, `PA` at `+50`, `birth_year` at `+52`, `uid` at `+75`) and take the **Top-20 highest-CA `ptype == 1` managers/staff**.
   - For each `(ordinal, uid)`: search decompressed 400 MB `people_db.dat` for trailing 12B identity `struct.pack('<III', ordinal, uid, uid)` → `ident_pos`, then find preceding 5B header `struct.pack('<IB', ordinal, 1)` at `hit` with `0 < ident_pos - hit - 5 <= 2600`, run `t120_people_unicorn.call_people_factory(ut, emu, 1)` + `t120_people_unicorn.run_person_row(ut, emu, obj, s19, buf[hit+5:hit+5+65536])`, and verify `res["ok"] and res["bytes_consumed"] - 12 == ident_pos - hit - 5`!
   - Resolve real UTF-8 names via Unicorn caller `0x143b93527` (3 name IDs: first, second, common) joined to `scratch/t106/out/payload_server_name_table_extra_{0,1,2}.bin` (reuse `load_name_pools()` from `scripts/t126_player_attributes_l3.py`).

## Deliverables
Write `scripts/t137_non_player_managers_l3.py` (with `--selftest` and `--uid <UID>`) and `scratch/t137/out/`:
1. `non_player_attributes_l3.json` — complete `NON_PLAYER` 4CC ↔ `(obj_off, wire_off, get_line, set_line)` L3 map (clearly flagging composite/computed 4CCs like `NRCJ`, `NRLS`, `NSCR`, `NTxx`)
2. `top20_managers_cards.json` — all 20 decoded world-famous managers/staff (Pep Guardiola, Jürgen Klopp, Carlo Ancelotti, etc.) with verified `(ordinal, dbid == uid)`, CA/PA 20/20 cross-check vs `basic_people` `+48/+50`, resolved UTF-8 names, and all mapped scalar attributes verified in `0..20`
3. `REPORT.md` — clean markdown tables of mapped `NON_PLAYER` attributes + Top-20 FM24 managers showcase table
4. `DONE.md` — first line `DONE type=t137`, counts (`L3 attributes`, `20/20 verified managers`, `CA/PA cross-check`, `--selftest PASS`)

Run `py -V:3.12 -B scripts/t137_non_player_managers_l3.py` and `--selftest` before finishing!
