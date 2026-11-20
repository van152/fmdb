# t35 Done

Status: `partial_no_semantic_candidate`. The requested semantic scan completed, but no Cafl/Cvfl child table was joined to an archive member. `client table_type 3` was profiled only as parent-container context. No field was assigned an offset or promoted to L3.

Run verification with:

```text
py -V:3.12 -I -B scratch/t35/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
