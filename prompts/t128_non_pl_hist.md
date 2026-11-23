# t128: `non_pl_hist_{dt,id,index}.dat` (Non-Playing / Staff History 3-File System) Binary Format & Closure

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t128_non_pl_hist.py` and `scratch/t128/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` to import `zstandard` (do NOT use `ctypes.util.find_library`).

## Inputs (READ-ONLY)
- `scratch/data/non_pl_hist_dt.dat` (27.6 MB)
- `scratch/data/non_pl_hist_id.dat` (6.0 MB)
- `scratch/data/non_pl_hist_index.dat` (4.2 MB)

## Goal (Keep It Focused & Fast!)
1. Inspect headers and decompress (in-memory — do NOT dump huge uncompressed blobs to disk!) all 3 files: `non_pl_hist_dt.dat`, `non_pl_hist_id.dat`, `non_pl_hist_index.dat`.
2. Determine the exact binary format, record count, record stride/framing, and footer closure of each of the 3 files:
   - Exact byte layout of a non-playing career history row (dates, club_id, job role, etc. — separate byte-verified framing from semantic candidates!).
   - Verify index-to-data linkage across the full dataset (row count closure, offset bounds, no out-of-range pointers).
3. Emit 10 decoded sample staff career histories (with raw hex + parsed columns).

## Deliverables
Write `scripts/t128_non_pl_hist.py` (with `--selftest`) and `scratch/t128/out/`:
1. `non_pl_hist_schema.json` — headers, compressed/decompressed sizes, record counts, stride/layout, closure verification, 10 samples
2. `REPORT.md` — concise technical summary
3. `DONE.md` — `DONE type=t128`, key metrics, `--selftest` PASS

Run `py -V:3.12 -B scripts/t128_non_pl_hist.py` and `--selftest` before finishing.
