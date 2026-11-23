# t135: Extract Complete 54-Attribute FM24 Player Cards for World Superstars Directly from 400 MB `people_db.dat`

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t135_star_player_cards.py` and `scratch/t135/out/`.
Keep stdout compact (< 80 lines per command).

## Goal
Using our verified `t120` Unicorn `people_db.dat` engine + `t126` 54/54 `PDxx` attribute map + `t106` `name_table_extra_{0,1,2}` UTF-8 name pools + `basic_people_db.dat` (`scratch/data/basic_people_db.dat`), locate and decode the **COMPLETE 54-attribute FM24 player cards** directly from the 400 MB `scratch/data/people_db.dat` archive for **20+ real FM24 superstars** (starting with the Top-20 highest-CA players in `basic_people_db.dat` PLUS guaranteed anchors Harry Kane `28049320`, Lionel Messi `7458500`, Cristiano Ronaldo `735216`)!

## Fast, Exact Algorithm (Runs in < 5 Seconds Total — No Need to Walk 658k Rows!)
1. **Step 1 — Get Target `(ordinal, uid, person_type, basic_CA, basic_PA)` from `basic_people_db.dat`** (use `zstandard` from `D:\tmp2b\fm24\tools\python`, NOT `ctypes.util.find_library`):
   - `basic_people_db.dat` framing (verified by `t115`): `raw[8:]` zstd-decompresses to `54,060,043 B`; `count = 658,011`; records start at offset `5` with marker `0x11`, `ptype = b[p+1]`, widths `{1:83, 2:83, 3:83, 4:34, 5:22}`; for types `1,2,3`: `uid = u32 at r+75`, `CA = u16 at r+44`, `PA = u16 at r+46`, `birth_year = u16 at r+52`.
   - Select the Top-20 players (`ptype in (2, 3)`) by `CA` PLUS guaranteed UIDs `28049320` (Harry Kane), `7458500` (Lionel Messi), `735216` (Cristiano Ronaldo).
2. **Step 2 — Locate Each Star's Exact Record in Decompressed 400 MB `people_db.dat` (in-memory, NEVER write 400 MB to disk!)**:
   - In `people_db.dat`, every record starts with the 5-byte header `[u32 ordinal][u8 ptype]` AND ends with the 12-byte identity `[u32 ordinal][u32 dbid][u32 uid]` (with `dbid == uid`)!
   - For each target `(ordinal, ptype, uid)`: search `buf` (using `buf.find(struct.pack('<IB', ordinal, ptype), start)`) — there are typically only 1–3 matches in 400 MB! Verify the true match by running `t120_people_unicorn.call_people_factory(ut, emu, ptype)` + `t120_people_unicorn.run_person_row(ut, emu, obj, s19, buf[hit+5:hit+5+65536])` and asserting `res['ok']` AND trailing 12B identity `(ordinal, uid)` matches EXACTLY!
   - Also double-check that `body[6:10]` (`PCAB` CA & `PPAB` PA from `t126`: `<5h` at `body+0` = `PHRP, PCRP, PWRP, PCAB, PPAB`) matches `basic_people_db.dat`'s CA/PA!
3. **Step 3 — Decode Complete 54-Attribute Cards + Names**:
   - Resolve `first_name_id`, `second_name_id`, `common_name_id` (caller `0x143b93527` in `res['reads']`) via `scratch/t106/out/payload_server_name_table_extra_{0,1,2}.bin` (reuse `load_name_pools()` from `scripts/t126_player_attributes_l3.py`).
   - Decode ALL 54 `PDxx` attributes from `body[29+15 : 29+69]` using `scratch/t126/out/player_69b_attributes_l3.json`, plus `weight_kg, height_cm` (`<HH` at `body+126`), `PHRP/PCRP/PWRP/PCAB/PPAB`, `positions_0_14`, and cross-check every single attribute is in `0..20`!
   - Note: if `ptype == 3` (`ACTUAL_PLAYER_AND_NON_PLAYER`), check whether its `PLAYER` header/69B offset differs from `ptype == 2` (`PLAYER`) via `res['reads']` — verify rather than assuming!

## Deliverables
Write `scripts/t135_star_player_cards.py` (with `--selftest` and `--uid <UID>`) and `scratch/t135/out/`:
1. `star_player_cards.json` — complete 54-attribute decoded cards for all 20+ superstars (including Lionel Messi, Cristiano Ronaldo, Harry Kane, Erling Haaland, Kylian Mbappé, Kevin De Bruyne, etc.), with exact `people_db.dat` file offset, body length, `basic_people` CA/PA cross-check, and all 54 `PDxx` values
2. `REPORT.md` — clean markdown showcase table of the decoded superstars (Name, UID, CA/PA, Height/Weight, Pace, Acceleration, Finishing, Dribbling, Passing, Vision, Composure, Determination, Tackling, Reflexes) + full 54-attribute breakdown for Messi, Ronaldo, and Kane!
3. `DONE.md` — `DONE type=t135`, count of verified superstars, CA/PA exact cross-check rate, `--selftest` PASS

Run `py -V:3.12 -B scripts/t135_star_player_cards.py` and `py -V:3.12 -B scripts/t135_star_player_cards.py --selftest` before finishing!
