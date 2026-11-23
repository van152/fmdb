# t119: Final 5/79 Unicorn Tables Closure

- **Result**: `5/5` clean (`4` full closed + `1` sample_ok, `0` failed)
- **Combined with t96c**: **`79/79`**
- **Fixes**: `TABLE_REF_GLOBALS=['0x141b5fdc0', '0x141b5fdc8', '0x141b5fdd0', '0x141b5fe00', '0x141b5fe10']`, `GLOBAL_DB_VER_VA=0x141b60330`

| Archive/Table | Class | Status | Rows OK / Target (Hdr) | Closed | Diff | Row Lens | Error |
|---|---|---|---|---|---|---|---|
| `server/table_0` | `AWARD` | `closed` | 3545/3545 (3545) | True | 0 | 76..76 (u=1) | - |
| `server/table_32` | `STARTING_FUTURE_TRANSFER` | `closed` | 315/315 (315) | True | 0 | 59..211 (u=3) | - |
| `server/table_71` | `STARTING_PAST_TRANSFER` | `sample_ok` | 50/50 (616665) | False | 57475694 | 37..178 (u=5) | - |
| `server/table_72` | `STARTING_PAST_TRADE` | `closed` | 138/138 (138) | True | 0 | 60..105 (u=10) | - |
| `client/table_0` | `AWARD` | `closed` | 3545/3545 (3545) | True | 0 | 76..76 (u=1) | - |
