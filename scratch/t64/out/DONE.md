# t64 Done

Generated deliverables:

- `scripts/t64_comp_unmapped_r2.py`
- `scratch/t64/out/helpers.json`
- `scratch/t64/out/field_map_r2.json`
- `scratch/t64/out/exclusions.json`
- `scratch/t64/out/verify.py`
- `scratch/t64/out/REPORT.md`
- `scratch/t64/out/DONE.md`

Acceptance recorded by the builder:

- 196/196 t59 unmapped occurrences surveyed.
- t59 summary `{L3: 49, held: 10, unmapped: 196}` and 818 inversions unchanged.
- 55 main-reader direct stream calls accounted for; 52 outer slots plus 3 alternate m58/m60/m68 calls. The one-call discrepancy against the t59 report is recorded without changing t59 mappings or inversions.
- `+0xa8` and `+0xe0` static entry conditions recorded; both are zero-present in all 7,047 server rows and absent from client extension mode.
- `+0xd0` / `+0xd8` retained separately at 121 / 51 server rows.

Post-build checks completed:

- `scratch/t64/out/verify.py`: PASS.
- `scripts/t01_anchors.py`: PASS, 7/7 checks.
- Builder `--help` and `--selftest`: PASS.
