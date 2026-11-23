# t40: Club/Nation Subtable Schema Consolidation

## Outcome

Consolidated the six accepted club-subtable field ledgers into `reports/club_nation_subtable_schema.json` and its readable companion `reports/club_nation_subtable_schema.md`.

| Source task | Parent/table | Accepted L3 | Held | Other retained evidence |
|---|---|---:|---:|---|
| t27 | Cstc / 22 | 14 | 6 | 2 non-business slots; 4 negative regressions |
| t30 | Clhs / 37 | 8 | 4 | — |
| t31 | CSrs / 62 | 10 | 0 | — |
| t32 | Cmti / 43 | 5 | 1 | — |
| t34 | CNtp / 66 | 2 | 2 | — |
| t36 | Cdbt / 33 | 5 | 0 | — |
| **Total** | **6 tables** | **44** | **13** | **4 negatives; L4=0** |

## Method and Evidence

- Consumed the six accepted field ledgers, their existing cursor JSON, and referenced instruction shards. Cursor extraction and payload/EXE parsing were not rerun.
- Preserved accepted field records, held source records, negative regression labels, source-file hashes, and reader/getter VA evidence in the JSON output.
- Checked all six server payload closures. Each is `13 + row_count * stride + 9 = payload_len`; the payload SHA-256 values are copied from the accepted cursor records.
- Cstc table 22 has a client identity-transfer observation (449/449 exact matches, 12 bytes). It is retained as transport evidence, not promoted as a business field or foreign key. Client tables are absent for the other five sources.
- Did not infer offset equivalence across archives. The t37 nation inventory remains partial and contributes zero accepted nation-child L3 fields. No L4 claim is made.
- Binary provenance is tied to the `evidence/fm24/reports/qa/IDA_PROVENANCE.md` snapshot and checked against `evidence/MANIFEST.json`; the external executable was not read by consolidation.

## Validation

- `py -V:3.12 -I -B -m py_compile scratch/t40/out/consolidate.py scratch/t40/out/verify.py` — passed.
- `py -V:3.12 -I -B scratch/t40/out/consolidate.py --selftest` — passed: 6 tables, 44 L3, 13 held, 4 negatives, L4=0; provenance and closures complete.
- `py -V:3.12 -I -B scratch/t40/out/consolidate.py --force` — regenerated both report files.
- `py -V:3.12 -I -B scratch/t40/out/verify.py --selftest` — passed independently, including source hashes, field sets, VA provenance, client/server framing, and closure arithmetic.
- `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t01_anchors.py` — passed 7/7.

## Reproduction

From the repository root, run the commands above in order. `verify.py` is independent of the builder and does not import it.
