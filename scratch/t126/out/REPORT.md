# t126: 400 MB `people_db.dat` 69-Byte `PLAYER_DATA` (54/54 `PDxx` L3) + All-5-Types Master

- **69-Byte `PLAYER_DATA` Block (`wire 29..97`, `obj_off -0x70..-0x2c`, `base_off 0x208..0x24c`)**:
  - **Bytes `15..68`**: **54 / 54 `PDxx` attributes 100% L3-verified** with identical offsets in BOTH GET (`sub_141465590` `d_141465590.c`) and SET (`sub_141467B70` `test_141467b70.c`)!
  - **Bytes `0..14`**: Position/flag block (`idx 0 = GK`, 128/1,283 players == 20; `idx 1 = const 1` across all 1,283 players; `idx 2..14 = 13 outfield position ratings 0..20`, not exposed via `PDxx` switch).
- **All-5-Classes L3 Joins**: **`374`** total L3 4CC joins across `NON_PLAYER`, `PLAYER`, `ACTUAL_PLAYER_AND_NON_PLAYER`, `OFFICIAL`, `RETIRED_PERSON`.
- **Real Decoded FM24 Player Cards**: **`5`** real players decoded with resolved UTF-8 names (`name_table_extra_0/1/2`), CA/PA, height/weight, and all 54 `PDxx` values verified in `0..20` (`all_valid=True`).

## 1. All-5-Classes Summary
| Type | Class | Walked Rows | Unicorn-Joined 4CCs | +54 `PDxx` | Total L3 4CCs |
|---:|---|---:|---:|---:|---:|
| 1 | `NON_PLAYER` | 481 | 83 | 0 | **83** |
| 2 | `PLAYER` | 1,283 | 100 | 54 | **154** |
| 3 | `ACTUAL_PLAYER_AND_NON_PLAYER` | 9 | 63 | 54 | **117** |
| 4 | `OFFICIAL` | 34 | 18 | 0 | **18** |
| 5 | `RETIRED_PERSON` | 1,193 | 2 | 0 | **2** |

## 2. Complete 54/54 `PDxx` Attribute Map (Bytes `15..68`, Wire `44..97`)
| Idx | Wire | `obj_off` | 4CC | Attribute | Category | GET Line | SET Line |
|---:|---:|---|---|---|---|---:|---:|
| 15 | 44 | `-0x61` | `PDcr` | Crossing | Technical | 1099 | 446 |
| 16 | 45 | `-0x60` | `PDdr` | Dribbling | Technical | 694 | 270 |
| 17 | 46 | `-0x5f` | `PDfn` | Finishing | Technical | 860 | 337 |
| 18 | 47 | `-0x5e` | `PDhd` | Heading | Technical | 789 | 310 |
| 19 | 48 | `-0x5d` | `PDls` | Long Shots | Technical | 459 | 167 |
| 20 | 49 | `-0x5c` | `PDmr` | Marking | Technical | 493 | 179 |
| 21 | 50 | `-0x5b` | `PDmv` | Off The Ball | Mental | 517 | 192 |
| 22 | 51 | `-0x5a` | `PDps` | Passing | Technical | 604 | 224 |
| 23 | 52 | `-0x59` | `PDpn` | Penalty Taking | Technical | 588 | 219 |
| 24 | 53 | `-0x58` | `PDtk` | Tackling | Technical | 314 | 99 |
| 25 | 54 | `-0x57` | `PDvs` | Vision | Mental | 227 | 67 |
| 26 | 55 | `-0x56` | `PDhn` | Handling | Goalkeeping | 808 | 318 |
| 27 | 56 | `-0x55` | `PDae` | Aerial Reach | Goalkeeping | 926 | 370 |
| 28 | 57 | `-0x54` | `PDca` | Command of Area | Goalkeeping | 1035 | 426 |
| 29 | 58 | `-0x53` | `PDcm` | Communication | Goalkeeping | 1067 | 436 |
| 30 | 59 | `-0x52` | `PDkc` | Kicking | Goalkeeping | 392 | 133 |
| 31 | 60 | `-0x51` | `PDth` | Throwing | Goalkeeping | 298 | 94 |
| 32 | 61 | `-0x50` | `PDan` | Anticipation | Mental | 974 | 385 |
| 33 | 62 | `-0x4f` | `PDdc` | Decisions | Mental | 647 | 245 |
| 34 | 63 | `-0x4e` | `PDoo` | One on Ones | Goalkeeping | 549 | 202 |
| 35 | 64 | `-0x4d` | `PDpt` | Positioning | Mental | 620 | 229 |
| 36 | 65 | `-0x4c` | `PDrf` | Reflexes | Goalkeeping | 129 | 24 |
| 37 | 66 | `-0x4b` | `PDft` | First Touch | Technical | 876 | 342 |
| 38 | 67 | `-0x4a` | `PDtc` | Technique | Technical | 282 | 89 |
| 39 | 68 | `-0x49` | `PDlf` | Left Foot | Foot | 443 | 162 |
| 40 | 69 | `-0x48` | `PDri` | Right Foot | Foot | 148 | 32 |
| 41 | 70 | `-0x47` | `PDfl` | Flair | Mental | 844 | 332 |
| 42 | 71 | `-0x46` | `PDcs` | Corners | Technical | 1115 | 451 |
| 43 | 72 | `-0x45` | `PDtm` | Teamwork | Mental | 330 | 104 |
| 44 | 73 | `-0x44` | `PDwr` | Work Rate | Mental | 259 | 77 |
| 45 | 74 | `-0x43` | `PDlt` | Long Throws | Technical | 475 | 172 |
| 46 | 75 | `-0x42` | `PDec` | Eccentricity | Goalkeeping | 728 | 282 |
| 47 | 76 | `-0x41` | `PDro` | Rushing Out | Goalkeeping | 169 | 42 |
| 48 | 77 | `-0x40` | `PDtp` | Tendency to Punch | Goalkeeping | 346 | 109 |
| 49 | 78 | `-0x3f` | `PDac` | Acceleration | Physical | 902 | 357 |
| 50 | 79 | `-0x3e` | `PDfk` | Free Kick Taking | Technical | 828 | 327 |
| 51 | 80 | `-0x3d` | `PDst` | Strength | Physical | 201 | 52 |
| 52 | 81 | `-0x3c` | `PDsm` | Stamina | Physical | 185 | 47 |
| 53 | 82 | `-0x3b` | `PDpc` | Pace | Physical | 572 | 214 |
| 54 | 83 | `-0x3a` | `PDjm` | Jumping Reach | Physical | 373 | 125 |
| 55 | 84 | `-0x39` | `PDld` | Leadership | Mental | 413 | 143 |
| 56 | 85 | `-0x38` | `PDdt` | Dirtiness | Hidden | 710 | 275 |
| 57 | 86 | `-0x37` | `PDbl` | Balance | Physical | 992 | 392 |
| 58 | 87 | `-0x36` | `PDbr` | Bravery | Mental | 1011 | 400 |
| 59 | 88 | `-0x35` | `PDcy` | Consistency | Hidden | 1131 | 456 |
| 60 | 89 | `-0x34` | `PDag` | Aggression | Mental | 942 | 375 |
| 61 | 90 | `-0x33` | `PDal` | Agility | Physical | 958 | 380 |
| 62 | 91 | `-0x32` | `PDim` | Important Matches | Hidden | 771 | 303 |
| 63 | 92 | `-0x31` | `PDij` | Injury Proneness | Hidden | 752 | 295 |
| 64 | 93 | `-0x30` | `PDvt` | Versatility | Hidden | 243 | 72 |
| 65 | 94 | `-0x2f` | `PDnf` | Natural Fitness | Physical | 533 | 197 |
| 66 | 95 | `-0x2e` | `PDde` | Determination | Mental | 678 | 265 |
| 67 | 96 | `-0x2d` | `PDcp` | Composure | Mental | 1083 | 441 |
| 68 | 97 | `-0x2c` | `PDcc` | Concentration | Mental | 1051 | 431 |

## 3. Decoded Real FM24 Player Cards (with Resolved Names from `name_table_extra_{0,1,2}`)
| Row | UID | Name | CA / PA | Height / Weight | Key Attributes (Pace / Fin / Pass / Drib / Det / Tack) |
|---:|---:|---|---|---|---|
| 1230 | 5796076 | **Milan Mijatović** | 116 / 119 | 190cm / 92kg | Pac=9 Fin=5 Pas=10 Dri=6 Det=12 Tck=9 |
| 1241 | 62176200 | **Lazar Carević** | 114 / 123 | 195cm / 85kg | Pac=8 Fin=0 Pas=9 Dri=0 Det=13 Tck=0 |
| 1309 | 5790256 | **Vlado Giljen** | 106 / 110 | 188cm / 85kg | Pac=11 Fin=0 Pas=0 Dri=11 Det=12 Tck=11 |
| 1463 | 62031598 | **Milan Jelovac** | 99 / 100 | 190cm / 83kg | Pac=9 Fin=4 Pas=10 Dri=9 Det=8 Tck=8 |
| 1492 | 5750067 | **Bojan Zogović** | 98 / 103 | 192cm / 85kg | Pac=10 Fin=3 Pas=3 Dri=5 Det=13 Tck=11 |
