# t131: Non-Numbered Special Members in `server_db.dat` (`club_links`, `common_name_links`, `simple_vars`, `name_table_extra_*`, `table_extra_*`, `table_for_old_save_*`, `fantasy_draft_future_regens`)

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t131_special_members.py` and `scratch/t131/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` to import `zstandard` (do NOT use `ctypes.util.find_library`).

## Inputs (READ-ONLY)
- `scratch/data/server_db.dat` and `scratch/data/client_db.dat` (list EVERY member whose path does NOT match `table_\d+\.dat`!)
- Note: 13 payloads are ALREADY unpacked in `scratch/t106/out/payload_*.bin` (you can read them directly or extract fresh from `server_db.dat`/`client_db.dat` via `scripts/t112_fm24_reader.py`!).
- Check `table_extra_3.dat`, `table_extra_9.dat`, `table_extra_24.dat` (and any `client_db/` non-numbered members too!).

## Goal (Keep It Focused & Fast!)
1. Enumerate EVERY non-numbered member across `server_db.dat` and `client_db.dat` (exact path, compressed/decompressed size, magic/header bytes, version, declared row count).
2. Decode the binary framing & prove exact byte closure (`diff=0`!) for as many special members as possible:
   - `name_table_0`, `name_table_1`, `name_table_2` (first/second/common names — exact row count, UTF-8 string layout, sample names!)
   - `name_table_extra_0`, `name_table_extra_1`, `name_table_extra_2`
   - `club_links`, `common_name_links`, `simple_vars`, `fantasy_draft_future_regens`
   - `table_for_old_save_23`, `table_for_old_save_25`
   - `table_extra_3`, `table_extra_9`, `table_extra_24` (if present in `server_db.dat` or `client_db.dat`!)
3. Report exact closure status (`closed diff=0` vs `header_only/partial`) honestly for every single member.

## Deliverables
Write `scripts/t131_special_members.py` (with `--selftest`) and `scratch/t131/out/`:
1. `special_members_schema.json` — complete catalog + decoded framing + closure checks + sample rows for every non-numbered member
2. `REPORT.md` — concise summary table
3. `DONE.md` — `DONE type=t131`, key counts (`?/N` members byte-closed), `--selftest` PASS

Run `py -V:3.12 -B scripts/t131_special_members.py` and `--selftest` before finishing.
