# t129: `lang_db_2400.dat` (71.4 MB) & `lang_update_db.dat` (2.3 MB) Binary Format & String Decoder

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t129_lang_db.py` and `scratch/t129/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` to import `zstandard` (do NOT use `ctypes.util.find_library`).

## Inputs (READ-ONLY)
- `D:\tmp2b\fm24\input\lang_db_2400.dat` (71.4 MB)
- `scratch/data/lang_update_db.dat` (2.3 MB)
- Check `scripts/t112_fm24_reader.py` for FMF container reading if either file is an FMF archive (or zstd raw stream).

## Goal (Keep It Focused & Fast!)
1. Inspect headers and container structure of BOTH `lang_db_2400.dat` and `lang_update_db.dat` (in-memory — do NOT write 100MB+ dumps to disk!).
2. Decode the binary framing of `lang_update_db.dat` completely (full byte closure!) and `lang_db_2400.dat` (member directory if FMF, or section headers & record layout if flat zstd stream).
3. Extract exact entry/string counts, encoding (UTF-8 vs UTF-16LE), key/ID structure (e.g. table_type + uid + field_type -> localized string?), and 20 real decoded sample localized entries (clubs/competitions/awards/nations).

## Deliverables
Write `scripts/t129_lang_db.py` (with `--selftest`) and `scratch/t129/out/`:
1. `lang_db_schema.json` — container structure, sizes, framing, entry counts, sample decoded strings
2. `REPORT.md` — concise technical summary
3. `DONE.md` — `DONE type=t129`, key metrics, `--selftest` PASS

Run `py -V:3.12 -B scripts/t129_lang_db.py` and `--selftest` before finishing.
