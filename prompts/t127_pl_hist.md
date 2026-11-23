# t127: `pl_hist_{dt,id,index}.dat` (Playing History 3-File System) Binary Format & Star Verification

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t127_pl_hist.py` and `scratch/t127/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` to import `zstandard` (do NOT use `ctypes.util.find_library`).

## Inputs (READ-ONLY)
- `scratch/data/pl_hist_dt.dat` (57.0 MB)
- `scratch/data/pl_hist_id.dat` (4.1 MB)
- `scratch/data/pl_hist_index.dat` (3.1 MB)
- Star UIDs from `t115`: Harry Kane (`28049320`), Cristiano Ronaldo (`735216`), Lionel Messi (`7458500`)
- Check `scratch/t95/funcs/` for any `PLAYING_HISTORY` / `pl_hist` readers if present (optional).

## Goal (Keep It Focused & Fast!)
1. Inspect headers and decompress (in-memory — do NOT dump huge uncompressed blobs to disk!) all 3 files: `pl_hist_dt.dat`, `pl_hist_id.dat`, `pl_hist_index.dat`.
2. Determine the exact binary format, record count, record stride/framing, and footer closure of each of the 3 files:
   - How `pl_hist_index.dat` maps a person (`uid` or `ordinal` or `dbid`) to an offset/range in `pl_hist_dt.dat` and/or `pl_hist_id.dat`.
   - Exact byte layout of a single career-season history row in `pl_hist_dt.dat` (year, club_id, comp_id, apps, goals, etc. — mark verified fields vs candidate fields honestly!).
3. Verify the index-to-data linkage on at least 1,000 people AND extract the career season history rows for Harry Kane (`28049320`), Cristiano Ronaldo (`735216`), and Lionel Messi (`7458500`) if indexed by UID or ordinal!

## Deliverables
Write `scripts/t127_pl_hist.py` (with `--selftest`) and `scratch/t127/out/`:
1. `pl_hist_schema.json` — headers, sizes, decompressed sizes, record counts, field layout, linkage stats, star career samples
2. `REPORT.md` — concise technical summary
3. `DONE.md` — `DONE type=t127`, key metrics, `--selftest` PASS

Run `py -V:3.12 -B scripts/t127_pl_hist.py` and `--selftest` before finishing.
