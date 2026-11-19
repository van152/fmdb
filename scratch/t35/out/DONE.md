# t35 Done

Status: `partial_no_semantic_candidate`. The t14 and stage2 semantic scan found no affiliation/link child-table candidate. `client table_type 3` was profiled only as parent-container context; Cafl/Cvfl table identity and item columns remain unknown. No static cursor was analyzed and no field was promoted to L3.

Verification:

```text
py -V:3.12 -I -B scripts/t35_cafl_cvfl.py --selftest
py -V:3.12 -I -B scratch/t35/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
