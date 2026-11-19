# t42 — Club/Nation Subtable Schema v2

Date: 2026-11-19

## Result

Upgraded `reports/club_nation_subtable_schema.{json,md}` from the accepted t40 schema v1 to v2 by appending only the accepted t39 `Tchl` table and explicit frozen `master.json` provenance. No new archive, executable, or schema parsing was performed.

| Measure | v2 result |
|---|---:|
| Club/shared table entries | 7 |
| Accepted L3 fields | 51 |
| Held fields | 15 |
| Original negative regressions | 4 |
| Cstc non-business slots | 2 |
| L4 | 0 |
| Nation-only new L3 claims | 0 |

The six original t40 table objects (44 L3 fields, 13 held fields, and both Cstc non-business records) and all four negative-regression records compare structurally equal to the frozen v1 snapshot. The original `binary_provenance` is unchanged. Nation-side coverage retains the t37 partial inventory and its zero-new-L3 summary.

## Tchl Addition

`t39` E78 identifies table type 34, RTTI `STARTING_TEAM_CUP_HISTORY`, in shared club/nation editor scope. Its seven L3 fields are `tchc`, `mstn`, `sstn`, `dbrt`, `posi`, `cquf`, and `tcop`. The two year fields, `styr` and `edyr`, remain held and are not promoted.

The consolidated fields retain the original t39 source record and digest, schema index, row/wire coordinates, physical widths, interpretation, reader transfer sites, getter accesses, and source task. The table and every field record the t39 reader extent: file offset `0x43a6890..0x43a6a6f` (end exclusive), VA `0x144511e90..0x14451206f` (end exclusive). The `dbrt` compound field remains two 1-byte lanes at row offsets 20/21 and wire offsets 21/22.

Server payload evidence: 7,115 rows, stride 44, length 313,082, SHA-256 `a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812`; closure is `13 + 7115 * 44 + 9 = 313082`. Client table 34 is absent, not an empty table.

`styr` is a u16 year integer with 161 zero values outside frozen XML `[1900,2100]`; its first counterexample remains row 28 at offset 1,254. `edyr` has 21 such zero values; its first counterexample remains row 2,695 at offset 118,604. Neither zero is reclassified as a sentinel.

The t39 owner evidence is recorded under `reference_domains`: 7,084 non-null owner ordinals resolve to table 24 selector 11 `NATIONAL_TEAM`, while 31 owners are null. Club-exclusive L3 remains 0. The exclusivity note uses owner ordinal/selector and factory-arm evidence and explicitly does not use `entity_tag` as an exclusivity criterion. Tchl's competition/table 25, stage_name/table 23, and team/table 24 ordinal target-domain witnesses are retained; none are reinterpreted as UIDs.

## Frozen Schema Provenance

`schema_provenance` records:

- `evidence/fm24/reports/editor_schema/master.json`, 2,900,594 bytes, SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`.
- Matching `evidence/MANIFEST.json` entry with the same SHA-256 and byte count; `manifest_match` is true. Snapshot date: 2026-11-18.
- Acceptance references to t39 E78 and t40 E79 in `scratch/t01/LEDGER.json`.

The manifest, master file, t39 source ledger/cursor/report, instruction shards, branch shards, and acceptance ledger are registered in the schema's `source_artifacts` with current SHA-256 and byte count.

## Preservation and Verification

Exact v1 inputs were preserved before report replacement:

- `club_nation_subtable_schema.v1.json`: SHA-256 `963bfec0ee13ecff23fe05cb1a622841eaff46735fbda2a5dcbda72f9fdc5a7c`.
- `club_nation_subtable_schema.v1.md`: SHA-256 `3e713d47daecc05e72bf077e719ef41e71525456af91edf97b70ae01949ea163`.

Executed with `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data` and Python 3.12 isolated/no-bytecode mode:

- `py -V:3.12 -I -B scratch/t42/out/consolidate_v2.py --help` — PASS.
- `py -V:3.12 -I -B scratch/t42/out/verify.py --help` — PASS.
- `py -V:3.12 -I -B scratch/t42/out/consolidate_v2.py --selftest` — PASS: 7 tables, 51 L3, 15 held, 4 negatives, two Cstc non-business records, L4=0, v1 preserved, master SHA matched.
- `py -V:3.12 -I -B scratch/t42/out/verify.py --selftest` — PASS: independent verifier; it does not import the builder.
- `py -V:3.12 -I -B scripts/t01_anchors.py` — PASS, 7/7.

No game/editor UI or IDA session was started; no network or Z: access occurred. `t01_anchors.py` was run as required against its configured read-only regression inputs.
