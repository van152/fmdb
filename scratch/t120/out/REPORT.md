# t120: 400 MB `people_db.dat` Native Unicorn Walkthrough

- **Rows walked cleanly**: **`3,000 / 3,000`** (end_offset=`1,216,813`, elapsed=`9.81s`, first_error=`None`)
- **Archive total declared rows**: `658,011`

## Factory & Vtables (`sub_1410992C0`)
| Type | Class | Base->Obj Offset | Vtable VA | `slot19` VA |
|---:|---|---|---|---|
| 1 | `NON_PLAYER` | `0xf8` | `0x141877008` | `0x140dc3f90` |
| 2 | `PLAYER` | `0x278` | `0x141879b18` | `0x140e08730` |
| 3 | `ACTUAL_PLAYER_AND_NON_PLAYER` | `0x368` | `0x1418c5458` | `0x1415d5110` |
| 4 | `OFFICIAL` | `0x138` | `0x1418c0658` | `0x1415856b0` |
| 5 | `RETIRED_PERSON` | `0x0` | `0x14188a548` | `0x141108330` |
| 6 | `JOURNALIST` | `0x88` | `0x1418c5d68` | `0x1415d8630` |

## Walked Person-Type Breakdown
| Type | Class | Rows OK | Body Len Min..Max | Unique Lens |
|---:|---|---:|---|---:|
| 1 | `NON_PLAYER` | 481 | 311..831 | 185 |
| 2 | `PLAYER` | 1,283 | 457..1286 | 375 |
| 3 | `ACTUAL_PLAYER_AND_NON_PLAYER` | 9 | 737..1007 | 9 |
| 4 | `OFFICIAL` | 34 | 115..127 | 3 |
| 5 | `RETIRED_PERSON` | 1,193 | 28..67 | 29 |
