# t144 (Mechanical Errand): Wave 13+14 Regression Audit & Deliverable SHA-256 Matrix

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or any existing `scripts/tNN_*.py` files. Write ONLY to `scripts/t144_regression_audit.py` and `scratch/t144/out/`.

## Goal (Pure Mechanical Verification — Fast & Clean!)
Write a single clean Python script `scripts/t144_regression_audit.py` (with `--selftest`) that:
1. Runs `py -V:3.12 -B <script> --selftest` (with a 120s per-script timeout, capturing exit code, elapsed seconds, and last 3 stdout/stderr lines) on EVERY completed Wave 13+14 script:
   - `scripts/t01_anchors.py` (baseline anchor regression — note: check if it takes `--selftest` or runs bare!)
   - `scripts/t97_extract_4cc_mem.py --selftest`
   - `scripts/t98_table45_closure.py --selftest`
   - `scripts/t106_special_members.py --selftest`
   - `scripts/t108_extract_4cc_v2.py --selftest`
   - `scripts/t109_big3_l3_join.py --selftest`
   - `scripts/t110_master_l3_schema.py --selftest`
   - `scripts/t112_fm24_reader.py --selftest`
   - `scripts/t115_basic_people_full.py --selftest` (note: check if it needs `zstd` DLL — record exact exit code honestly!)
   - `scripts/t119_unicorn_last5.py --selftest`
   - `scripts/t120_people_unicorn.py --selftest`
   - `scripts/t121_master_79of79.py --selftest`
   - `scripts/t122_people_l3_schema.py --selftest`
   - `scripts/t123_basic_people_l3.py --selftest`
   - `scripts/t125_big3_gap_closure.py --selftest`
   - `scripts/t126_player_attributes_l3.py --selftest`
   - `scripts/t133_fm24_reader_v2.py --selftest`
   - `scripts/t135_star_player_cards.py --selftest`
2. Scans all `scratch/t*/out/DONE.md` files (from `t95` to `t143`), records which tasks have `DONE.md`, reads the first 10 lines of each `DONE.md`, and computes SHA-256 + byte size for every `.json` and `.md` deliverable in those `out/` directories (skipping `.bin`/`.pkl`/`.sqlite` files > 50 MB).
3. Verifies `git status --short reports/ scratch/t01/LEDGER.json` is completely clean (zero modifications to protected paths!).

## Deliverables
Write `scripts/t144_regression_audit.py` (with `--selftest`) and `scratch/t144/out/`:
1. `regression_matrix.json` — per-script exit code, runtime, pass/fail, DONE.md catalog, SHA-256 manifest, protected-path clean check
2. `REPORT.md` — clean markdown table of all regression checks + completed task catalog
3. `DONE.md` — first line `DONE type=t144`, pass count (`?/18`), protected-path clean=True, `--selftest` PASS

Run `py -V:3.12 -B scripts/t144_regression_audit.py` and `--selftest` before finishing!
