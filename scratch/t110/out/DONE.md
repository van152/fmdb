DONE type=t110

- Deliverables: `master_67tables_l3.json`, `coverage_milestone.json`, `REPORT.md`, `verify.py`.
- Inputs genuinely consumed: t96c wire traces and t108 fourcc memory map; source regression checked against club/nation schema.
- Ledger: 67 IDA table records; 54 records with at least one Join; 1,036 unique table-record/4CC mappings.
- Unicorn status across records: CLOSED (diff=0)=30, OK_SAMPLE (50 rows)=23, FAIL=10, NOT_IN_SERVER_CLIENT_DB=4. The 10 FAIL entries are enumerated in REPORT.md; total table rows include IDA class variants.
- Existing-L3 regression: exact=2, within_slot=27, mismatch=23. Each mismatch has a per-field explanation in `coverage_milestone.json`; these are uncovered coordinates, not zero-mismatch verification.
- Verification: `python -I -B scripts/t110_master_l3_schema.py --selftest` PASS; `python -I -B scratch/t110/out/verify.py` PASS.
- `master_67tables_l3.json` size: approximately 1.22 MiB (<15 MiB).
