# t67 - COMP table_25 data-side crosswalk

Status: complete. Evidence target: L2 data-side cross-validation. L3=0, L4=0.

## Native envelope

- client: 7,047 rows, 127 B each, 13 B header + 894,969 B rows + 9 B footer.
- server: 7,047 rows, variable 198..1,894 B, 13 B header + 1,533,950 B rows + 9 B footer.
- Both independent four-alignment scans and ordinal-layer non-overlap DP recover exactly one path with 12 B identity and UID nonzero/strictly increasing.
- UID lanes equal: True; 12 B identity bytes equal: True; footer equal: True.
- Footer bytes: client `ae14d97c7ef951f197d885cc6f925cf13d13b09f7f2d9d04925fb17dcefb4a4d`; server `98bb59ad08a6de9bc73992d8e7bf400ea6697159bf5911b5e56742a6bdb1d8f5`; both end in `00000000014ec43a77`.

## Selectors and templates

- Client selector histogram: `{0:7047}`.
- Server selector histogram: `{0:7047}`.
- The byte-level row grammar yields one client template and 25 server templates. Sequence/count comparison to t59 `field_slots.json` is exact; no CFG is rebuilt here.

## Sensitivity

| control | client paths | server paths |
|---|---:|---:|
| `identity_12_footer_7` | 0 | 0 |
| `identity_12_footer_8` | 0 | 0 |
| `identity_12_footer_9` | 1 | 1 |
| `identity_12_footer_10` | 0 | 0 |
| `identity_12_footer_12` | 0 | 0 |
| `marker_0_footer_7` | 0 | 0 |
| `marker_0_footer_8` | 1 | 1 |
| `marker_0_footer_9` | 0 | 0 |
| `marker_0_footer_10` | 0 | 0 |
| `marker_0_footer_12` | 0 | 0 |
| `triple_footer_7` | 0 | 0 |
| `triple_footer_8` | 0 | 0 |
| `triple_footer_9` | 1 | 1 |
| `triple_footer_10` | 0 | 0 |
| `triple_footer_12` | 0 | 0 |
| `header_11` | 1 | 1 |
| `header_12` | 1 | 1 |
| `header_13` | 1 | 1 |
| `header_14` | 1 | 1 |
| `header_15` | 1 | 1 |
| `selector_lookahead` | 1 | 1 |
| `no_marker` | 1 | 1 |
| `allow_zero` | 1 | 1 |
| `no_uid_order` | 1 | 1 |
| `both_relaxed` | 1000000 | 4 |
| `wire_triple` | 1 | 1 |
| `triple_no_lookahead` | 1 | 1 |
| `native_identity` | 1 | 1 |

The `both_relaxed` client result is capped at 1,000,000; server remains 4. `allow_zero` and `no_uid_order` are single-relaxation controls in the t59 model. The client fixed-width controls are recorded in `sensitivity.json`: tail-aligned 12B, 13B, and 8B assumptions plus the explicit 13B lookahead/footer-8 control.

## t01f fixtures

- Live continent ordinals are exactly `{0,1,2,3,4,5}` on both sides.
- Rows 707 and 708 point to parent ordinal 352; ordinal 352 has UID 150990.
- England `cnti` ordinal 139 and China PR `cnti` ordinal 55 reclose in comp rows on both sides; target nation UIDs 765 and 110 are the frozen t59 L2 fixture values (table_10 is not read here).
- The 10 named continent/nation anchors and 2 parent anchors are rechecked with client coordinates and server values.

## Boundaries

- This is a data-side crosswalk for table_25 only. It does not change `reports/`, `scratch/t59/`, or any schema semantic assignment.
- Candidate alternatives and negative controls remain in `sensitivity.json`; they are not promoted to native framing.
- No game, editor, IDA, network, or `Z:` access was used.

## Reproduction

```text
FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scripts/t67_comp_data_crosswalk.py --build
FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scratch/t67/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py
```
