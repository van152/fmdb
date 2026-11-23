# t45 Schema v3 Consolidation

Date: 2026-11-19

## Scope

This task only consolidates the accepted t41 Csme evidence into the frozen t42 schema v2. No new payload decode, executable analysis, game/editor run, network access, or external-library access was performed. The seven v2 table objects, their field records, the four t20 negative regressions, and both Cstc non-business records remain verbatim.

## Result

- Schema v3 contains 8 tables, 52 accepted L3 fields, 16 held fields, 4 original negative regressions, and L4=0.
- Csme/table 59 is appended from t41 E82. Its server payload has 9,079 rows and closes as `13 + 6567*22 + 2512*32 + 9 = 224880`; payload SHA-256 is `7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7`. The row length is `22 + 10*n`, with `n` read at wire+6. Client table 59 is absent.
- Melf is the one new L3 field. Its byte coordinate is legacy `18+10*j` / wire `19+10*j`, for `0 <= j < n`. The observed rows have n=0 or 1; only the 2,512 count=1 rows contain Melf. Count=0 means no value, not an inferred default.
- Msid remains held at `held_no_live_media_reference`. The sink is statically bound, but all materialized pairs are null and no live media-source reference establishes the key semantics.
- All 9,079 owners are in the table24 Team family (selector 10: 8,941; selector 11/NATIONAL_TEAM: 138). Therefore Csme club-exclusive L3 remains 0.
- The t41 t33 false-tail negative and its original clarification are retained as supplemental evidence, separate from the unchanged four t20 regressions.
- Nation inventory remains partial with zero new nation-only L3 claims.

## Provenance and Validation

The public schema records reader VA extent `0x141583ba0..0x141583f80` (end exclusive), field source records and their canonical digests, t41 instruction/branch shards, and source artifact hashes. The t42 v2 JSON and Markdown are frozen in this directory. Because the v2 artifact list contains an earlier LEDGER hash, the current E82 ledger is preserved separately as `LEDGER.E82.json`; the earlier v2 artifact entry is unchanged.

Validation passed:

- `consolidate_v3.py --help`
- `consolidate_v3.py --selftest`
- `verify.py --help`
- `verify.py --selftest` (independent; does not import the builder)
- `scripts/t01_anchors.py` with `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`: 7/7 checks

Frozen input hashes: v2 JSON `a08b013a060724bef6e0c8ea1e0c4b16e57a7438a8fa53d7ed519c6f77611ab7`; v2 Markdown `da02f1062172d0ca9ae5f44ee3061cb06962a2255c95af0b76617156bf700dbd`; E82 ledger snapshot `20fb4a99a955b800a49078ede30700221ca7a9b32fd98db49b8a2fed981af749`.
