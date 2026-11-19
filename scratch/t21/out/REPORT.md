# t21 club cursor follow-up

## Result

- Status: `partial_row_audit_complete_cursor_unreconciled`. This follow-up independently walks the local table and rechecks existing static reader evidence; it does not claim a complete serializer cursor.
- Row framing: 84259 rows, 84256 standard rows, compact ordinals [69706, 69707, 69708]; row end `0x69c66a` matches footer `0x69c66a`: `True`.
- u32 at row+0 equals u32 at row+8 in 55868/84259 rows. This is counterevidence to treating row+8 as a distinct Cccn field without a stronger class-specific explanation; the field remains unpromoted.
- New schema-to-row mappings: 0. The ordinal transition around 69,705 is data only, not an RTTI class discriminator.

## Static Reader Recheck

- `CLUB`: reader `0xe5a7a0` to `0xe5a7a0`; source trace has 16 width instructions, 21 stream calls and 5 backedges; fresh byte/instruction checks 19/19 pass.
- `LEAGUE_BODY_CLUB`: reader `0x157cff0` to `0x43beba0`; source trace has 16 width instructions, 20 stream calls and 5 backedges; fresh byte/instruction checks 18/18 pass.

Static instruction checks confirm recorded bytes and disassembly at cited addresses. They do not prove which branch executes for each row or align either reader to the complete row cursor.

## Remaining Blockers

- Recover an independently supported per-row class selector or reconcile both class tracks against row bytes without assuming the contiguous ordinal split.
- Resolve the mixed CLUB reader's conditional/helper paths and the separate LEAGUE_BODY_CLUB count-loop path.
- Decode the three compact row bodies and preserve the exact footer closure.
- Keep `Cccn@row+8` unpromoted until its duplicate-ID behavior is explained.

## Inputs and Reproduction

- Local decoded payload from `FM24_DB_DIR` via `scripts/fm24_dump.py`; read-only `editor.exe`; frozen `scratch/t01/inbox/t01h/output.json` trace.
- Run `py -V:3.12 -I scripts/t21_club_cursor.py --help`, `--selftest`, then `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I scripts/t21_club_cursor.py`.
- No game, editor, IDA or network access is used.
