# t130: `summary.dat` Binary Decoder + Complete 12-Archive FM24 Database Inventory

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t130_archive_inventory.py` and `scratch/t130/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` to import `zstandard` (do NOT use `ctypes.util.find_library`).

## Inputs (READ-ONLY)
- ALL `.dat` and `.xml` files in `scratch/data/`:
  - `server_db.dat`, `client_db.dat`, `people_db.dat`, `basic_people_db.dat`, `summary.dat`, `lang_update_db.dat`, `pl_hist_dt.dat`, `pl_hist_id.dat`, `pl_hist_index.dat`, `non_pl_hist_dt.dat`, `non_pl_hist_id.dat`, `non_pl_hist_index.dat`, `2430_fm.xml`
- Plus `D:\tmp2b\fm24\input\lang_db_2400.dat`
- Reuse FMF reader logic from `scripts/t112_fm24_reader.py` where applicable.

## Goal (Keep It Focused & Fast!)
1. Build a complete, authoritative SHA-256 + container-type + header + compressed/decompressed size + member-count inventory of ALL 13 `.dat` files + `2430_fm.xml`.
2. Completely decode `summary.dat` (1.6 MB) — inspect its container/payload framing, extract what tables/counts/metadata it holds, and verify byte closure.
3. Also verify the 11 `default`-handler table IDs (`11, 13, 15, 16, 17, 20, 28, 40, 53, 54, 55`) — prove programmatically whether ANY of them exist in `server_db.dat`, `client_db.dat`, or ANY other archive.

## Deliverables
Write `scripts/t130_archive_inventory.py` (with `--selftest`) and `scratch/t130/out/`:
1. `archive_inventory.json` — complete 13-file inventory + `summary.dat` decoded structure + 11 default-handler adjudication
2. `REPORT.md` — concise markdown table of all 13 `.dat` archives + `summary.dat` breakdown
3. `DONE.md` — `DONE type=t130`, key counts, `--selftest` PASS

Run `py -V:3.12 -B scripts/t130_archive_inventory.py` and `--selftest` before finishing.
