# t37 — Nation Subtable Data-Side Inventory

Status: `partial_nation_parent_identity_coverage`. This is data-side reconnaissance only; no static cursor work, new L3, or L4.

## Coverage

- Frozen nation schema: 346 fields and 29 list parents.
- Item-bearing / zero-item parents: 20 / 9.
- Existing t28 links: 4 parents; new server-table candidate: table 34.
- L2 candidate fields / column matches: 7 / 65.
- New L3 claims: 0; L4: 0.

## Schema Baseline Difference

The supplied baseline enumerated 17 item-bearing and 8 zero-item parents (25 total). The frozen `nation.xml` schema actually has 20 item-bearing and 9 zero-item list fields (29 total). The additional schema parents included here are `EDfx`, `Tchl`, `EDsc`, and `AXML`; none is silently dropped.

## Candidate and Existing Links

- `Tchl` → server table 34 / `STARTING_TEAM_CUP_HISTORY`: low-confidence shared-schema candidate. Nation and club Tchl item signatures match exactly; t29's existing association is club-side, and stage2 entity identity is still candidate. Table 34 closes as `14 + 7115 * 44 + 8 = 313082`. Candidate columns remain ambiguous and are referenced with full statistics in `profiles/table_server_34.profile.json`.
- `Nlns`, `Nefr`, `Nnfr`, `Nagr`: `linked_by_t28`; existing client table_10 inline collections, not redumped here. Counts and wire strides are carried from the t28 collection evidence.

## Parent Inventory

| Parent | Items | Table | Archive | Count | Stride | Status |
|---|---:|---:|---|---:|---:|---|
| `Nagr` | 3 | `10` | client_inline | 162 | 12 | `complete_linked_by_t28` |
| `TCrs` | 4 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nchi` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Nphi` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Tko1` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Tkg1` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Tko2` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Tkg2` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Tko3` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Tkg3` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |
| `Nrvn` | 2 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nefr` | 7 | `10` | client_inline | 214 | 28 | `complete_linked_by_t28` |
| `Nnfr` | 7 | `10` | client_inline | 63 | 28 | `complete_linked_by_t28` |
| `Nntp` | 6 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nctp` | 5 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nrtp` | 5 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nlns` | 2 | `10` | client_inline | 492 | 5 | `complete_linked_by_t28` |
| `NTRv` | 2 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `NWGv` | 2 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `NSps` | 2 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `NCro` | 2 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Ntxr` | 9 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nfmp` | 6 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Nftb` | 7 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Calt` | 2 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `EDfx` | 7 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `Tchl` | 9 | `34` | server | 7115 | 44 | `partial_shared_schema_candidate` |
| `EDsc` | 6 | `unknown` | unknown | unknown | unknown | `partial_parent_to_table_unknown` |
| `AXML` | 0 | `unknown` | unknown | unknown | unknown | `partial_zero_item_schema` |

## Tchl L2 Column Candidates

Offsets are row-relative diagnostics, not field assignments. Full all-row column statistics, including sentinels, value domains, packed day/year, signed cash-range, float32 and u8 masks, are in the profile JSON. Multiple matching offsets are intentionally retained.

- `tchc` (database_record_unique_id, competition): +0/w4 (1.000), +12/w4 (1.000), +16/w4 (1.000), +22/w4 (1.000), +31/w4 (0.990), +4/w4 (0.982), +27/w4 (0.977).
- `styr` (integer, no table type): none observed.
- `edyr` (integer, no table type): none observed.
- `mstn` (database_record_unique_id, stage_name): +12/w4 (1.000), +16/w4 (1.000).
- `sstn` (database_record_unique_id, stage_name): +12/w4 (1.000), +16/w4 (1.000).
- `dbrt` (enum, no table type): +2/w1 (0.500), +3/w1 (0.500), +6/w1 (0.500), +7/w1 (0.500), +9/w1 (0.500), +11/w1 (0.500), +14/w1 (0.500), +15/w1 (0.500), ... (27 total).
- `posi` (integer, no table type): +9/w1 (1.000), +11/w1 (1.000), +20/w1 (1.000), +32/w1 (1.000), +33/w1 (1.000), +34/w1 (1.000), +38/w1 (1.000), +42/w1 (1.000), ... (12 total).
- `cquf` (database_record_unique_id, competition): +0/w4 (1.000), +12/w4 (1.000), +16/w4 (1.000), +22/w4 (1.000), +31/w4 (0.990), +4/w4 (0.982), +27/w4 (0.977).
- `tcop` (database_record_unique_id, team): +0/w4 (1.000), +4/w4 (1.000), +12/w4 (1.000), +16/w4 (1.000), +22/w4 (1.000), +27/w4 (1.000), +31/w4 (1.000), +11/w4 (0.978).

## Unknowns and Blockers

- All non-t28 parents other than Tchl lack an independent parent-to-table join in the consumed evidence. Unknown values stay `unknown`; semantic names, numeric shape and counts are not used as standalone identity proof.
- The t14 census has no exact `NATION_TRANSFER_PREFERENCE`, `TAX_RULE`, or `FAMOUS_PLAYER` primary-class match for Nntp, Ntxr, or Nfmp, respectively.
- Nation Tchl ownership of table 34 is unresolved. The row profile proves data availability and arithmetic closure only, not the schema parent.
- Empty-item parents may be ref-only, embedded, or shared; no storage model is inferred.

## Static Handoff

- For Tchl, confirm whether the nation collection reader reaches table_34's STARTING_TEAM_CUP_HISTORY reader/sink; t29 only covers the club-side candidate.
- For Nntp/Ntxr/Nfmp and the other unknowns, establish direct parent collection to serialized member/reader links before profiling additional tables.
- Keep Nlns/Nefr/Nnfr/Nagr linked_by_t28; do not spend static work duplicating their closed client-tail fields.

## Verification

Run `py -V:3.12 -I -B scratch/t37/out/verify.py --selftest` and then `py -V:3.12 -I -B scratch/t37/out/verify.py`. The verifier independently recalculates table34 row closure and candidate-column statistics from the source full-row dump.
