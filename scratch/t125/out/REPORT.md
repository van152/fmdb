# t125 — Big-3 persisted field closure

Original 110/1034 = 10.6%; t109 → t125: gross **379/1034 → 512/1034 (49.5%)**, net **379/673 → 512/672 (76.2%)**, gaps **294 → 160**.
All 379 t109 L3 rows and 361 exclusions are unchanged. Counts are top-level XML occurrences, not unique tags or physical columns.

| Entity | N | L3 old → new | Net denominator old → new | Excluded old → new | Gaps old → new |
|---|---:|---:|---:|---:|---:|
| club | 433 | 139 → 197 | 281 → 281 | 152 → 152 | 142 → 84 |
| nation | 346 | 112 → 164 | 211 → 211 | 135 → 135 | 99 → 47 |
| comp | 255 | 128 → 151 | 181 → 180 | 74 → 75 | 53 → 29 |

## Reclassified gaps

| Class | Occurrences |
|---|---:|
| `L3_helper_inlined_closed` | 1 |
| `L3_subtable_routed` | 94 |
| `L3_unicorn_or_subobject_closed` | 38 |
| `excluded_non_db_l3` | 1 |

Persisted target distribution: `10`: 3, `24`: 3, `45`: 24, `48`: 23, `9`: 36, `table_extra_24`: 1, `table_extra_3`: 43.

| Prior gap class | Resolved | Remaining |
|---|---:|---:|
| `gap_child_off_not_in_child_stream` | 20 | 1 |
| `gap_delegated_or_empty` | 3 | 31 |
| `gap_helper_computed` | 32 | 53 |
| `gap_off_not_in_read_stream` | 78 | 63 |
| `gap_other_table_same_tag` | 1 | 12 |

## Evidence and receiver boundaries

- `140e8a400`/`140e834a0` are CLUB get/set dispatchers. CLUB server slot19 calls the TEAM_CONTAINER base reader on the same `this`. That base serializer does not make `[CLUB+0xb0]` or `[CLUB+0x100]` into main-row data: `table_extra_3` leaf paths are imported only from matched t71/t82 occurrence proofs and checked against dispatch/PE sites. `table_extra_24` is a separate TEAM sidecar. `table_extra_9` remains unbound.
- `141063f30`/`1410668f0` operate on the table-9 NATIONAL_TEAM_CONTAINER. The table-9 setter thunk (`143f00000.c:31–39`) can try the linked table-10 NATION and then an NTC before falling back to the incoming NTC. Shared Nation XML is not identity of runtime receivers. `14105d510.c:449–463` reads a counted vector through a temporary, so the trace must not be mistaken for inline bytes at the vector pointer; each `Neu*` index is bound to its branch. Table-10 collection proofs retain the t55 client/server cursors and distinct object displacements.
- `1411f1090`/`1411f4f70` dispatch TEAM_CONTAINER properties; some select a STARTING_RECORD type rather than a container member. `140ec0a60`/`140ecb5c0` do the analogous COMP dispatch through a different record manager. `144026550.c:10–18` and `143ca4a20.c:11–23` select by `(parent UID, rec_type)` before calling `141545680`; table 48 is distinguished from table 45 by controls against decoded CLUB/NTC/COMP identity sets, not the shared row vtable. The PE constructor bytes corroborate table IDs; they are not claimed to be assignments to the record-manager globals.
- `141545680.c:134` stores `gams`/`apps` at `STARTING_RECORD+0x54` (u16); `:200` stores `stdt` at `+0x40` (date). t109’s `:89` anchor is not the `gams` store. `CMCs` routes to **`gams` in the proved CLUB and COMP branches**; the name/t98 hint is not allowed to overrule the actual dispatch. No owner-compatible NATION branch was proved for that occurrence. `1415446a0` is the corresponding getter; t98 semantic/profile claims and this physical routing result are separate.
- `140fe3f20` is also a base property handler. Its appearance in the table-4 map is not a receiver proof. Conversely a `this` trace span at a reused offset does not imply that a property accesses the same field. `IsAC` is a positive no-op getter case, not excluded because a trace missed it.

### Reader / trace audit

The machine-readable audit fingerprints all 33 t124 gap helpers. The call census inventories both registered reader slots, all visible direct callsites at each root and bounded same-`this` continuations. Indirect virtual sites, unresolved aliases and unproven composed arguments cannot establish a new field on their own.

| Table | Server reader | Client reader | Trace rows client / server | Footer client / server |
|---|---|---|---|---|
| 3 | `0x140e5b1a0` | `0x140e5cf50` | 50 / 50 | False / False |
| 9 | `0x14105d510` | `0x141060660` | 251 / 251 | True / True |
| 10 | `0x1410404c0` | `0x141041b30` | 251 / 251 | True / True |
| 25 | `0x140ed1440` | `0x140eb9000` | 50 / 50 | False / False |

## Remaining work

A held row keeps its original class and gives exact dispatch sites, candidate trace hits (never closure by themselves), and any branch-local call targets. Partial traces cannot prove absence. A missing decompilation is not necessarily the only blocker.

- `0x14083dfa0`: 38 held occurrence(s)
- `0x1411eacb0`: 4 held occurrence(s)
- `0x144026350`: 3 held occurrence(s)
- `0x1407e4490`: 2 held occurrence(s)
- `0x14083b0a0`: 1 held occurrence(s)
- `0x14083db80`: 1 held occurrence(s)
- `0x140e58670`: 1 held occurrence(s)
- `0x140e5f8c0`: 1 held occurrence(s)
- `0x140fc9d50`: 1 held occurrence(s)
- `0x141078de0`: 1 held occurrence(s)

Inputs are read-only. The t108 filename used is `fourcc_mem_map_v2.json` (on disk). No game/editor/IDA execution or live collection was needed.

```text
py -V:3.12 -B scripts/t125_big3_gap_closure.py
py -V:3.12 -B scripts/t125_big3_gap_closure.py --selftest
```
