# t37 Nation Subtable Inventory

Status: `partial_nation_parent_identity_coverage`

Frozen-schema inventory: 29 list parents, 20 with item fields and 9 with zero item fields.

One server table (34 / STARTING_TEAM_CUP_HISTORY) is retained as a low-confidence shared-schema candidate for nation Tchl. Four client inline collections remain linked by the existing t28 evidence. Seven t33 profiles were cross-checked; table58 remains unassigned to nation NWGv. No new L3 or L4 claims were made.

Verification commands:

```text
py -V:3.12 -I -B scratch/t37/out/verify.py --selftest
py -V:3.12 -I -B scratch/t37/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```

Verification results (Python 3.12): generator `--help` and `--selftest` PASS; verifier `--help`, `--selftest`, and full run PASS (7,115 table34 rows, 65 candidate columns, 29 parents, t28 links, and manifest pin checked); `t01_anchors.py` PASS, 7/7.

See `REPORT.md` for parent-by-parent coverage and blockers.
