DONE type=t125

- Gross L3: **512/1034 (49.5%)**, up from 379/1034 (36.7%).
- Net persisted L3: **512/672 (76.2%)**, up from 379/673 (56.3%).
- Gaps: **294 → 160**. New L3: **133** (94 subtable, 38 Unicorn/subobject, 1 helper). New non-DB exclusion: **1**.
- All 379 prior L3 entries and 361 prior exclusions were preserved. Denominator: club 433, nation 346, comp 255. L4 = 0.
- Build: PASS (`py -V:3.12 -B scripts/t125_big3_gap_closure.py`).
- `--selftest`: PASS (`py -V:3.12 -B scripts/t125_big3_gap_closure.py --selftest`).

Deliverables: `scripts/t125_big3_gap_closure.py`; `big3_l3_v3.json`, `coverage_summary_v3.json`, `remaining_gaps_v3.json`, `REPORT.md`, and this file under `scratch/t125/out/`.
