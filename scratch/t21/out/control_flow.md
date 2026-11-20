# t21b club control-flow audit

Status: `partial_control_flow_audit_complete_row_cursor_unreconciled`. Static paths are now CFG-based; row cursor remains unreconciled.

## Reachable Reader CFG

- **CLUB** `0xe5a7a0`: 1412 reachable instructions, 268 basic blocks, 41 reachable stream transfers, 167 conditional branches, 35 backedges.
- **LEAGUE_BODY_CLUB** `0x43beba0`: 68 reachable instructions, 5 basic blocks, 2 reachable stream transfers, 3 conditional branches, 1 backedges.

## Linear-Scan Reconciliation

The t05 0x2000-byte scan reports 41 stream-call patterns; t01h reports 21 stream calls and retains 8 entry-function records; the reachable CLUB CFG identifies 41 stream transfers, with 8 t01h sites matching. These scopes are distinct and none is a completed reader cursor.

## Conclusions

- No independent per-row RTTI class discriminator was found in the evidence reviewed.
- `Cccn` remains unpromoted; row+0 equals row+8 in 55868/84259 rows.
- This audit proves bounded static CFG reachability only. It does not establish runtime row/class pairing, a full cursor, or new field offsets.
- Newly promoted row-coordinate fields: 0.

## Reproduction

Run `py -V:3.12 -I scripts/t21b_control_flow.py --help`, `--selftest`, then `FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I scripts/t21b_control_flow.py`.
No game, editor, IDA or network access is used.
