# t25 Nation Client Field Expansion

## Status

Client table_10 cursor coordinates are complete for the verified 251-row payload. Static reader-tail binding and schema field coverage remain partial. The cursor is data-side only; it does not assign the arg8!=0 path or claim a server format.

## Schema Classification

- Active schema fields: 441
- Direct client-marked: 21
- Nested list items inheriting a client-marked parent: 28
- Client-scoped total including inherited list items: 49
- Explicit server-only: 0
- Unmarked/unknown: 392
- The 6 language-marked client fields are listed in `schema_split.json`; table_9/text-reference semantics remain a hypothesis.
- `Ncpi` is separately recorded as a commented-out schema field from t22, not part of the active 441.

## Cursor

- Rows: 251; row spans: 24710 bytes.
- Closure: `14 + 24710 + 8 = 24732`; footer: `00 00 00 01 ec 7a e4 04`.
- Per-row body/payload offsets, A/B/C/D count locations, item starts, identity and marker offsets are in `cursor_nation.json`.
- Existing frame verifier's row 55 identity/duni anchor is rechecked; count totals are A/B/C/D = 492/214/63/162.

## Field Mapping

- Active schema fields mapped: 7/441 (2 directly client-marked; 5 have no client flag).
- Schema-confirmed client-scope mapping rate: 2/49 (4.1%) (two mapped fields out of 49 client-marked top-level/list-item fields).
- The seven prefix mappings retain t01g's L3 reader/getter chains. Their row coordinates were decoded across all 251 client rows; per-field ranges and samples are in the shards.
- No other field received a row coordinate. Schema membership, client flags and list ownership alone are not treated as byte-offset evidence.
- Field ledger: `fields_nation.json` index plus five hash-checked shards; `Ncpi` is in `fields_nation_supplemental.json`.

## Open Items

- Reconcile reader calls 24-39 and all counted-loop bodies to row-frame coordinates; the cursor artifact currently gives complete client data coordinates, not a complete static call-to-wire trace.
- Map collection payload members to nested schema list-item fields; none are inferred from parent names.
- Investigate the 392 unmarked fields without classifying them as server-only.
- Verify all unmarked candidates against additional independent anchors before promotion; retain server table_10, arg8!=0, and XML-comment editability boundaries.

## Verification

```text
py -V:3.12 -I -B scripts/t25_nation_fields.py --selftest
py -V:3.12 -I -B scripts/t25_verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```

Source schema SHA-256: `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda` (matched against `evidence/MANIFEST.json`).
Client payload SHA-256: `7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34`.
