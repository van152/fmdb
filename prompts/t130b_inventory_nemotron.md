# t130b (Mechanical Errand): Complete 13-Archive FM24 Database Inventory + 11 Default-Handler Adjudication

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or any existing `scripts/tNN_*.py` files. Write ONLY to `scripts/t130_archive_inventory.py` and `scratch/t130/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` for `zstandard`.

## Goal (Clean, Mechanical, Fast!)
1. Inventory ALL 13 `.dat` files + `2430_fm.xml`:
   - In `scratch/data/`: `server_db.dat`, `client_db.dat`, `people_db.dat`, `basic_people_db.dat`, `summary.dat`, `lang_update_db.dat`, `pl_hist_dt.dat`, `pl_hist_id.dat`, `pl_hist_index.dat`, `non_pl_hist_dt.dat`, `non_pl_hist_id.dat`, `non_pl_hist_index.dat`, `2430_fm.xml`
   - In `D:\tmp2b\fm24\input\`: `lang_db_2400.dat`
   - For each file compute: exact byte size, SHA-256, first 16 bytes hex, container type (`FMF` if starts with `02 01 66 6d 66 2e`, `zstd_prefixed` if `raw[8:12] == 28 b5 2f fd`, `raw_zstd` if `raw[0:4] == 28 b5 2f fd`, or `custom/xml`), and member count if FMF (reuse `_DirectoryReader` / `Archive` from `scripts/t112_fm24_reader.py`).
2. Cross-reference already-verified closure status from our completed artifacts (`t133` 79/79 tables, `t106` 13/13 special members incl. `summary.dat`, `t123` `basic_people_db.dat` 658,011 rows, `t120`/`t126`/`t135` `people_db.dat`).
3. Adjudicate all **11 `default`-handler table IDs** (`11, 13, 15, 16, 17, 20, 28, 40, 53, 54, 55`): prove programmatically by scanning EVERY FMF member path in `server_db.dat` and `client_db.dat` that NONE of those 11 `table_<id>.dat` files exist on disk!

## Deliverables
Write `scripts/t130_archive_inventory.py` (with `--selftest`) and `scratch/t130/out/`:
1. `archive_inventory.json` — complete 14-file inventory + 11 default-handler adjudication
2. `REPORT.md` — clean markdown table of all 14 files + default-handler proof
3. `DONE.md` — first line `DONE type=t130`, `files_inventoried=14`, `default_handlers_absent=11/11`, `--selftest PASS`

Run `py -V:3.12 -B scripts/t130_archive_inventory.py` and `--selftest` before finishing!
