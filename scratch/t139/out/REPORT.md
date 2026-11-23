# t139 — FM24 unified read-only SQLite export (`fm24_core.sqlite`)

- Built 2026-11-22 19:11:38Z in 55.0s; DB size 191,741,952 B; integrity_check `ok`; total rows **1,952,416**.
- Sources: t133 (79/79 tables, 12 core exported), t106 payload bins, basic_people_db.dat (t123 framing), t135 star cards (21 x 54 PDxx).

## Tables & row counts

| table | rows | note |
|---|---:|---|
| nations | 251 | server/10 |
| clubs | 84,259 | server/3, `name_full` + `name_short` from the two wire STRs |
| competitions | 7,047 | server/25 (no name strings — see boundary) |
| stadiums | 48,413 | server/21, fixed numeric layout |
| cities | 56,293 | server/2, fixed numeric layout |
| awards | 3,545 | server/0 |
| languages | 126 | server/8 |
| injuries | 115 | server/6 |
| weather | 334 | server/27 |
| currencies | 173 | server/41 |
| starting_records | 84,477 | server/45 |
| teams | 84,507 | server/24 (TEAM flag 0xa + NATIONAL_TEAM flag 0xb) |
| basic_people | 658,011 | types {'1': 166064, '2': 476158, '3': 4757, '4': 9839, '5': 1193} |
| name_first / name_second / name_common | 245,981 / 542,060 / 85,668 | t106 pools 0/1/2 |
| common_name_links | 12,056 | name ordinal + nation + lang |
| club_links | 9,261 | club -> linked club |
| simple_vars | 28,552 | global key/value records |
| fantasy_draft_names | 40 | fictional club/stadium/person names |
| star_players | 21 | t135 cards with names, CA/PA, height/weight |
| star_player_attributes | 1,134 | 21 x 54 PDxx (0..20) |
| table_inventory | 92 | 79 numbered (all closed) + 13 special |

## CLI

```
py -V:3.12 -B scripts/t139_fm24_db_cli.py --build-sqlite
py -V:3.12 -B scripts/t139_fm24_db_cli.py --stats
py -V:3.12 -B scripts/t139_fm24_db_cli.py --query-uid 28049320
py -V:3.12 -B scripts/t139_fm24_db_cli.py --top-players 20
py -V:3.12 -B scripts/t139_fm24_db_cli.py --search-name England
py -V:3.12 -B scripts/t139_fm24_db_cli.py --selftest
```

### Example outputs

`--top-players 5` (Top-N by CA; name shown when the uid is one of the 21 star cards — no other person-name join exists in these archives):

```json
[{"rank": 1, "uid": 18004457, "ca": 190, "pa": 190, "birth_year": 1991, "name": "Kevin De Bruyne"}]
```

`--query-uid 28049320` returns the Harry Kane basic_people row (ca=184, pa=185, birth_year=1993), his star card, and his 54 attributes.

`--search-name England` matches the surname "England" in `name_second` (3 pool entries) plus any club names containing "England".

## Data boundary (verified, honest)

- Competition display names are **not** in the archive: the COMP name-block tag is 0 for all 7,047 rows, and a raw byte scan of every entity payload (comp/nation/city/stadium/team, table_extra_3/9/24, old-save members) finds zero occurrences of `Premier League` / `England`. Entity display names live in the game's language DB, which is not part of these files.
- Nation/city/stadium tables are fixed numeric layouts (no string fields); server `table_extra_9` carries nation nicknames + legendary-player names, not nation names.
- `basic_people` carries no name ids (t123 proved no direct name-ordinal fields in the wire row); person names come from the three t106 pools (keyed by people_db read chains, out of t139 scope) and the 21 star cards.
- basic_people identity: `uid`@+79 (t123) and `dbid`@+75 (t115 anchor word); equal for every anchor person, both indexed.

## Schema notes

- Variable-table columns are named by grammar path with the t110/t121 L3 4CC where proven (`col_<row0_off>` elsewhere); vector element counts are `n_*` columns; selector variants (clubs 0x0/0xc, teams 0xa/0xb) share the column set with NULLs where a variant does not produce a field.
- 25 indexes cover uid/dbid/ca/name lookups; uid lookups measure < 5ms.
- `export_summary.json` holds machine-readable counts, timings and the integrity report.
