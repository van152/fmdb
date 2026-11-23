# t67 delivery

- `crosswalk.json`: L2 claim/method/evidence/grade ledger.
- `sensitivity.json`: four-alignment DP controls, t59 sensitivity ports, and client fixed-width controls.
- `verify.py`: independent archive, DP, byte-grammar, identity, footer, template, and t01f verifier.
- `REPORT.md`: human-readable result and negative boundaries.
- `scripts/t67_comp_data_crosswalk.py`: builder with `--help` and `--selftest`.

Commands:

```text
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t67_comp_data_crosswalk.py --build
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t67/out/verify.py --selftest
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t67/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py
```
