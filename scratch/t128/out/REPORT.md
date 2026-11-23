# t128: `non_pl_hist_{index,id,dt}.dat` — Non-Playing / Manager & Staff History Closure

## 1. Container & Zero-Byte Closure Summary

| File | Compressed (B) | Decompressed (B) | Header | Records | Notes |
|---|---:|---:|---|---:|---|
| `non_pl_hist_index.dat` | 4,153,253 | 6,037,508 | `03 01 74 61 64 2e f1 0d` | 754,688 | 746,543 valid ordinals + 8,145 `0xFFFFFFFF` sentinels |
| `non_pl_hist_id.dat` | 5,972,352 | 5,972,344 | `03 01 74 61 64 2e 01 00` | 746,543 | raw `[first, last]` inclusive u32 byte offsets |
| `non_pl_hist_dt.dat` | 27,607,915 | 77,098,632 | `03 01 74 61 64 63 03 00` | 3,212,443 | 18,823 × 4 KiB zstd frames + `0x184D2A5E` skippable chunk table |

- **Closure diff**: **`0`** (`77,098,632 B == 3,212,443 × 24 B`)
- **Linkage**: `offsets_in_bounds=True`, `misaligned=0`, `contiguity_violations=0`, `uid_non_decreasing=True` (`673,317` unique UIDs, `81,371` multi-chain entries, `0` inversions), `valid_ordinals_bijection=True`
- **Chain**: `2,465,900` valid `next_row` links + `746,543` `0xFFFFFFFF` terminators, `malformed=0`, `closed=True`
- **Mean spells / person**: `4.3031` (max `85`)

## 2. 24-Byte Row Layout (`non_pl_hist_dt.dat`)

| Offset | Width | Field | Status | Notes |
|---:|---:|---|---|---|
| 0 | 4 | `club_or_nation_id` | verified | club UID (or nation UID for national-team spells) |
| 4 | 2 | `join_day` | verified | day-of-year 1..366 (0 = year-only; 1 with 1900 = empty) |
| 6 | 2 | `join_year` | verified | spell start year (1900 = empty) |
| 8 | 2 | `leave_day` | verified | day-of-year 1..366 (0 = year-only; 1 with 1900 = ongoing/empty) |
| 10 | 2 | `leave_year` | verified | spell end year (1900 = ongoing/empty) |
| 12 | 2 | `extra_day` | unknown | secondary date day-of-year (1 with 1900 sentinel in 99.83% of rows) |
| 14 | 2 | `extra_year` | unknown | secondary date year (1900 in 99.83% of rows, 2024 in 5,480 rows) |
| 16 | 1 | `job_role` | verified | primary job role code (53 unique values: 1=Player, 16=Manager, 6=Director, ...) |
| 17 | 1 | `job_subcode` | candidate | job role subcode / category paired with job_role |
| 18 | 1 | `flag_a` | unknown | boolean 0/1 flag (1 in 1,463 rows) |
| 19 | 1 | `flag_b` | unknown | boolean 0/1 flag (1 in 242,195 rows) |
| 20 | 4 | `next_row` | verified | absolute byte offset of next 24B row in career chain; 0xFFFFFFFF terminates |

## 3. Verified Manager Career Timelines

### Pep Guardiola (UID `1120`, ordinal `143858`, `11` spells)

| # | Entity (ID) | Join | Leave | Role | Raw Hex |
|---:|---|---|---|---|---|
| 1 | Barcelona B (`1668`) | 1989-07-01 | 1989 | Player | `84060000b600c5070000c50701006c07010b000048d73700` |
| 2 | Barcelona (`1708`) | 1990 | 2001-07-01 | Player | `ac0600000000c607b600d10701006c07010b000060d73700` |
| 3 | Brescia (`1113`) | 2001-07-01 | 2002-06-19 | Player | `59040000b600d107aa00d20701006c07010b000078d73700` |
| 4 | Associazione Sportiva Roma (`1100`) | 2002-06-19 | 2003-01-02 | Player | `4c040000aa00d2070200d30701006c07010b000090d73700` |
| 5 | Brescia (`1113`) | 2003-01-02 | 2003-01-30 | Player | `590400000200d3071e00d30701006c07010b0000a8d73700` |
| 6 | Al-Ahli Sports Club Doha (`135410`) | 2003-01-30 | 2005-12-01 | Player | `f21002001e00d3074f01d50701006c07010b0000c0d73700` |
| 7 | Dorados de Sinaloa (`5666338`) | 2005-12-20 | 2006-06-30 | Player | `227656006201d507b500d60701006c07010b0000d8d73700` |
| 8 | Barcelona B (`1668`) | 2007-07-16 | 2008-05-07 | Manager | `84060000c500d7078000d80701006c0710050000f0d73700` |
| 9 | Barcelona (`1708`) | 2008-05-08 | 2012-06-30 | Manager | `ac0600008100d807b600dc0701006c071005000008d83700` |
| 10 | FC Bayern München (`915`) | 2013-07-01 | 2016-06-30 | Manager | `93030000b600dd07b600e00701006c071005000020d83700` |
| 11 | Manchester City (`679`) | 2016-07-01 | present | Manager | `a7020000b700e00701006c0701006c0710050000ffffffff` |

### Jurgen Klopp (UID `9318`, ordinal `145116`, `7` spells)

| # | Entity (ID) | Join | Leave | Role | Raw Hex |
|---:|---|---|---|---|---|
| 1 | 1. CfR Pforzheim (`101148`) | 1986-07-01 | 1987-07-01 | Player | `1c8b0100b600c207b600c30701006c07010b000020603d00` |
| 2 | Eintracht Frankfurt II (`3607261`) | 1987-07-01 | 1988-06-30 | Player | `dd0a3700b600c307b600c40701006c07010b000038603d00` |
| 3 | SG Rot-Weiss Frankfurt (`877209`) | 1989-07-01 | 1990-07-01 | Player | `99620d00b600c507b600c60701006c07010b000050603d00` |
| 4 | 1. FSV Mainz 05 (`918`) | 1990-07-01 | 2000 | Player | `96030000b600c6070000d00701006c07010b000068603d00` |
| 5 | 1. FSV Mainz 05 (`918`) | 2001-02-28 | 2008-06-30 | Manager | `960300003b00d107b600d80701006c071005000080603d00` |
| 6 | Borussia Dortmund (`907`) | 2008-07-01 | 2015-06-30 | Manager | `8b030000b700d807b500df0701006c071005000098603d00` |
| 7 | Liverpool (`676`) | 2015-10-08 | present | Manager | `a40200001901df0701006c0701006c0710050000ffffffff` |

### Sir Alex Ferguson (UID `2020287`, ordinal `176317`, `12` spells)

| # | Entity (ID) | Join | Leave | Role | Raw Hex |
|---:|---|---|---|---|---|
| 1 | Queen's Park (`1591`) | 1958-02-28 | 1960-06-10 | Player | `370600003b00a607a200a80701006c07010b0000507bb800` |
| 2 | St Johnstone (`1596`) | 1960-06-11 | 1964-07-03 | Player | `3c060000a300a807b900ac0701006c07010b0000687bb800` |
| 3 | Dunfermline Athletic (`1557`) | 1964-07-04 | 1967-08-05 | Player | `15060000ba00ac07d900af0701006c07010b0000807bb800` |
| 4 | Rangers (`1570`) | 1967-08-05 | 1969-11-20 | Player | `22060000d900af074401b10701006c07010b0000987bb800` |
| 5 | Falkirk (`1563`) | 1969-11-21 | 1973-09-02 | Player | `1b0600004501b107f500b50701006c07010b0000b07bb800` |
| 6 | Ayr United (`1542`) | 1973-09-03 | 1973 | Player | `06060000f600b5070000b50701006c07010b0000c87bb800` |
| 7 | East Stirlingshire (`1559`) | 1974-06-01 | 1974-10-19 | Manager | `170600009800b6072401b60701006c0710050000e07bb800` |
| 8 | St Mirren (`1597`) | 1974-10-21 | 1978-05-31 | Manager | `3d0600002601b6079700ba0701006c0710050000f87bb800` |
| 9 | Aberdeen (`1536`) | 1978-06-30 | 1986-11-06 | Manager | `00060000b500ba073601c20701006c0710050000107cb800` |
| 10 | Scotland (National Team) (`793`) | 1985-10-20 | 1986-07-09 | Manager | `190300002501c107be00c20701006c0710050000287cb800` |
| 11 | Manchester UFC (`680`) | 1986-11-06 | 2013-06-30 | Manager | `a80200003601c207b500dd0701006c0710050000407cb800` |
| 12 | Manchester UFC (`680`) | 2013-07-01 | present | Director | `a8020000b600dd0701006c0701006c0706260000ffffffff` |

### Diego Simeone (UID `707720`, ordinal `161603`, `15` spells)

| # | Entity (ID) | Join | Leave | Role | Raw Hex |
|---:|---|---|---|---|---|
| 1 | Club Atlético Vélez Sarsfield (`98`) | 1987-01-01 | 1989 | Player | `620000000100c3070000c50701006c07010b000060ad8200` |
| 2 | Pisa (`2215`) | 1990-07-01 | 1992-07-01 | Player | `a7080000b600c607b700c80701006c07010b000078ad8200` |
| 3 | Sevilla (`1759`) | 1992-07-01 | 1994-07-01 | Player | `df060000b700c807b600ca0701006c07010b000090ad8200` |
| 4 | A. Madrid (`1687`) | 1994-07-01 | 1996 | Player | `97060000b600ca070000cc0701006c07010b0000a8ad8200` |
| 5 | FC Internazionale Milano (`1135`) | 1997-07-01 | 1999-07-01 | Player | `6f040000b600cd07b600cf0701006c07010b0000c0ad8200` |
| 6 | S.S. Lazio (`1140`) | 1999-07-01 | 2002 | Player | `74040000b600cf070000d20701006c07010b0000d8ad8200` |
| 7 | A. Madrid (`1687`) | 2003-07-01 | 2004 | Player | `97060000b600d3070000d40701006c07010b0000f0ad8200` |
| 8 | Racing Club de Avellaneda (`93`) | 2004-07-02 | 2005 | Player | `5d000000b800d4070000d50701006c07010b000008ae8200` |
| 9 | Racing Club de Avellaneda (`93`) | 2006-02-18 | 2006-05-16 | Manager | `5d0000003100d6078800d60701006c071005000020ae8200` |
| 10 | Club Estudiantes de La Plata (`85`) | 2006-05-18 | 2007-12-07 | Manager | `550000008a00d6075501d70701006c071005000038ae8200` |
| 11 | Club Atlético River Plate (`94`) | 2007-12-15 | 2008-11-09 | Manager | `5e0000005d01d7073a01d80701006c071005000050ae8200` |
| 12 | Club Atlético San Lorenzo de Almagro (`96`) | 2009-04-15 | 2010-04-04 | Manager | `600000006900d9075e00da0701006c071005000068ae8200` |
| 13 | Catania Football Club (`2193`) | 2011-01-18 | 2011-05-30 | Manager | `910800001200db079600db0701006c071005000080ae8200` |
| 14 | Racing Club de Avellaneda (`93`) | 2011-05-30 | 2011-12-19 | Manager | `5d0000009600db076101db0701006c071005000098ae8200` |
| 15 | A. Madrid (`1687`) | 2011-12-23 | present | Manager | `970600006501db0701006c0701006c0710050000ffffffff` |

### Daniel Levy (UID `141932`, ordinal `150350`, `1` spells)

| # | Entity (ID) | Join | Leave | Role | Raw Hex |
|---:|---|---|---|---|---|
| 1 | Tottenham Hotspur (`728`) | 2001-02-28 | present | role(4,1) | `d80200003b00d10701006c0701006c0704010000ffffffff` |

### Giuseppe Marotta (UID `705257`, ordinal `161150`, `12` spells)

| # | Entity (ID) | Join | Leave | Role | Raw Hex |
|---:|---|---|---|---|---|
| 1 | Città di Varese (`700173`) | 1978-07-01 | 1979-06-30 | role(14,9) | `0daf0a00b600ba07b500bb0701006c070e090000987d8000` |
| 2 | Città di Varese (`700173`) | 1979-07-01 | 1986-06-30 | role(6,3) | `0daf0a00b600bb07b500c20701006c0706030000b07d8000` |
| 3 | Brianza (`1149`) | 1986-07-01 | 1990-06-30 | role(6,3) | `7d040000b600c207b500c60701006c0706030000c87d8000` |
| 4 | Como 1907 (`1123`) | 1990-07-01 | 1993-06-30 | role(6,3) | `63040000b600c607b500c90701006c0706030000e07d8000` |
| 5 | Ravenna Football Club 1913 (`1163`) | 1993-07-01 | 1995-06-30 | role(6,3) | `8b040000b600c907b500cb0701006c0706030000f87d8000` |
| 6 | Venezia Football Club (`1179`) | 1995-07-01 | 2000-06-30 | role(6,3) | `9b040000b600cb07b600d00701006c0706030000107e8000` |
| 7 | Atalanta (`1106`) | 2000-07-01 | 2002-06-30 | role(6,3) | `52040000b700d007b500d20701006c0706030000287e8000` |
| 8 | U.C. Sampdoria (`1167`) | 2002-07-01 | 2004-06-30 | role(6,3) | `8f040000b600d207b600d40701006c0706030000407e8000` |
| 9 | U.C. Sampdoria (`1167`) | 2004-07-01 | 2010-06-30 | role(8,2) | `8f040000b700d407b500da0701006c0708020000587e8000` |
| 10 | Juventus (`1139`) | 2010-07-01 | 2018-10-25 | role(8,2) | `73040000b600da072a01e20701006c0708020000707e8000` |
| 11 | FC Internazionale Milano (`1135`) | 2018-12-13 | present | role(8,2) | `6f0400005b01e20701006c0701006c0708020000887e8000` |
| 12 | FC Internazionale Milano (`1135`) | 2018-12-13 | present | role(88,239) | `6f0400005b01e20701006c0701006c0758ef0000ffffffff` |

## 4. Honest Unknowns / Unresolved Bytes

- `extra_day` / `extra_year` (`bytes 12..15`): `(1, 1900)` empty sentinel in `99.83%` of rows; non-sentinel in `5,480` rows (all year `2024`, likely scheduled/contract-extension or future-move date).
- `flag_a` (`byte 18`): `1` in `1,463` rows; `flag_b` (`byte 19`): `1` in `242,195` rows (not yet proven against IDA code).
- `job_role` (`byte 16`, `53` values) & `job_subcode` (`byte 17`): `(1,11)=Player`, `(16,5)=Manager`, `(6,38)=Director` verified via real manager histories; remaining staff role enum IDs not exhaustively mapped.
