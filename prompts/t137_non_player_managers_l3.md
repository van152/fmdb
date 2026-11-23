# t137: `NON_PLAYER` (166,064 Managers/Coaches/Scouts) Complete Attribute L3 Map + Top-20 World Managers Decoded from 400 MB `people_db.dat`

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t137_non_player_managers_l3.py` and `scratch/t137/out/`.
Keep stdout compact (< 80 lines per command; NEVER dump huge `.c` files to stdout).

## Context & Inputs Already On Disk
`t126` + `t135` just cracked `PLAYER` (`ptype=2`, 54/54 `PDxx` attributes) and decoded 21 world superstar players from 400 MB `people_db.dat`.
Now do the exact same rigorous L3 breakthrough for **`NON_PLAYER` (`ptype=1`, 166,064 managers, coaches, scouts, physios, directors in FM24)**!

Authoritative inputs ALREADY on disk:
1. `scratch/t124/out/funcs/140dca880.c` (`NON_PLAYER::get_prop`, 2,524 lines!)
2. `scratch/t124/out/funcs/140dc8c00.c` (`NON_PLAYER::set_prop`, 1,212 lines!)
3. `scratch/t124/out/funcs/140dc7180.c` (`NON_PLAYER::reg_prop`, 842 lines!)
4. `scratch/t124/out/funcs/140dc40f0.c` (`NON_PLAYER::write`, 335 lines!)
5. `scratch/t120/out/funcs/140dc1d30.c` (`NON_PLAYER::slot19` read, 870 lines!)
6. `scratch/t120/out/people_unicorn_traces.json` (481 walked `NON_PLAYER` rows, 3 full sample read-by-read Unicorn traces; virtual base `obj_offset_from_base = 0xf8`!)
7. `scripts/t120_people_unicorn.py` (working Unicorn runner for `ptype=1` `NON_PLAYER`!)
8. `scripts/t135_star_player_cards.py` (working pattern for scanning `basic_people_db.dat` with `CA` at `+48`, `PA` at `+50`, `birth_year` at `+52`, `uid` at `+75`, then locating `[u32 ordinal][u8 ptype=1]` in 400 MB `people_db.dat` in-memory and resolving names via `scratch/t106/out/payload_server_name_table_extra_{0,1,2}.bin`!)
9. Note: if `NON_PLAYER::get_prop`/`set_prop` delegates coaching/mental/tactical attributes to a sub-handler (just like `PLAYER` delegated `PDxx` to `sub_141465590`/`sub_141467B70`), you MAY run a quick targeted `idalib` call on `scratch/t95/editor_work.i64` (NEVER touch `editor_merge_v2.i64`!) via `sys.path.insert(0, r"C:\Program Files\IDA Professional 9.4\idalib\python")` to decompile that sub-handler into `scratch/t137/out/ida/`.

## Your Mission
1. **Map ALL `NON_PLAYER` Coaching / Tactical / Mental / Scouting / Reputation / CA / PA Attributes to Exact Wire Offsets & 4CCs**:
   - Inspect `140dc1d30.c` (`NON_PLAYER::slot19`) + `t120` Unicorn `samples_by_type["1"]` to map the exact wire layout of `NON_PLAYER` (especially CA/PA/HomeRep/CurrentRep/WorldRep and the coaching/mental/tactical attribute block!).
   - Cross-join with `NON_PLAYER::get_prop` (`140dca880.c`) and `NON_PLAYER::set_prop` (`140dc8c00.c`) (and any sub-handler if delegated) so EVERY attribute byte has exact `(wire_off, obj_off, fourcc, get_line, set_line)` L3 proof!
2. **Decode the Top-20 Highest-CA FM24 Managers/Staff Directly from 400 MB `people_db.dat`**:
   - Scan `basic_people_db.dat` (`ptype == 1`) sorted by `CA` (`u16` at `+48`, `PA` at `+50` — verify against `NON_PLAYER` wire CA/PA just like `t135` did!).
   - Locate all Top-20 managers/staff in decompressed 400 MB `people_db.dat` (in-memory only!) via `[u32 ordinal][u8 1]`, run `t120_people_unicorn` on each hit to verify `ok == True` AND trailing 12B identity `(ordinal, dbid == uid)`, resolve real UTF-8 names via `name_table_extra_{0,1,2}`, and decode ALL mapped `NON_PLAYER` attributes (verify attributes are in valid FM24 `0..20` range!).
   - Expected names in Top-20 FM24 managers: Pep Guardiola, Jürgen Klopp, Carlo Ancelotti, Diego Simeone, José Mourinho, Mikel Arteta, etc.!

## Deliverables
Write `scripts/t137_non_player_managers_l3.py` (with `--selftest` and `--uid <UID>`) and `scratch/t137/out/`:
1. `non_player_attributes_l3.json` — complete `NON_PLAYER` L3 wire + 4CC attribute map (with C source lines)
2. `top20_managers_cards.json` — full decoded attribute cards for Top-20 FM24 managers/staff from 400 MB `people_db.dat` (with CA/PA cross-check, identity verification, resolved real names)
3. `REPORT.md` — clean markdown tables of all mapped `NON_PLAYER` attributes + Top-20 FM24 managers showcase table (Name, UID, CA/PA, Attacking, Defending, Tactical, Judging Ability, Judging Potential, Man Management, Determination, etc.!)
4. `DONE.md` — `DONE type=t137`, count of L3-mapped `NON_PLAYER` attributes, count of verified managers (`20/20`), CA/PA cross-check rate, `--selftest` PASS

Run `py -V:3.12 -B scripts/t137_non_player_managers_l3.py` and `--selftest` before finishing!
