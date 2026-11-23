# t127b: Finish `t127` — `pl_hist_{dt,id,index}.dat` (Playing History 3-File System) Full Closure + Star Career Histories

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write ONLY to `scripts/t127_pl_hist.py` and `scratch/t127/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` for `zstandard`. Keep stdout compact (< 50 lines per command).

## Context
A prior run ALREADY explored `scratch/data/pl_hist_{dt,id,index}.dat` and decoded Harry Kane's (`uid=28049320`, `ordinal=138595`, 17 seasons, e.g., 2010–11 Leyton Orient loan `club=674, comp=13, 18 apps, 5 goals`) and other stars' career histories into `scratch/t127/out/_stars.json`!
Do NOT keep temporary `.bin`/`.pkl` dumps as dependencies of your final script — `scripts/t127_pl_hist.py` MUST read directly from `scratch/data/pl_hist_{dt,id,index}.dat` (in-memory zstd decompression, READ-ONLY)!

## Mission
1. Inspect `scratch/t127/out/_stars.json` (and any small notes) to reuse the discovered layout, then independently verify against `scratch/data/pl_hist_{dt,id,index}.dat`:
   - Exact container headers, compressed/decompressed sizes, record counts, record strides, and footer closure (`diff=0`!) of ALL 3 files (`pl_hist_index.dat`, `pl_hist_id.dat`, `pl_hist_dt.dat`).
   - Exact index-to-data linkage across the ENTIRE dataset (verify every single indexed entry's offset/count stays within bounds and closes cleanly!).
   - Exact byte layout of a single playing-history season row (`y0`, `y1`, `apps`, `goals`, `club_id`, `comp_id`, dates, flags — honestly distinguishing verified fields vs candidate fields).
2. Decode and cross-check full career histories for **Harry Kane (`28049320`)**, **Lionel Messi (`7458500`)**, **Cristiano Ronaldo (`735216`)**, **Kevin De Bruyne (`18004457`)**, and **Kylian Mbappé (`85139014`)** (resolve club names via `t133_fm24_reader_v2.py` `server/3` if clean, or include exact `club_id` & `comp_id`!).

## Deliverables
Write `scripts/t127_pl_hist.py` (with `--selftest` and `--uid <UID>`) and `scratch/t127/out/`:
1. `pl_hist_schema.json` — full 3-file framing, closure (`diff=0`), linkage integrity stats, field layout, and 5 decoded star career histories
2. `REPORT.md` — concise technical summary + Harry Kane / Messi / Ronaldo career season tables
3. `DONE.md` — first line `DONE type=t127`, key metrics (total players indexed, total career season rows, closure `diff`, `--selftest` PASS)

Run `py -V:3.12 -B scripts/t127_pl_hist.py` and `--selftest` before finishing!
