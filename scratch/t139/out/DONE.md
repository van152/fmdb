DONE type=t139

- database: `fm24_core.sqlite` (191,741,952 B, integrity_check `ok`, built 2026-11-22 19:11:38Z in 55.0s)
- total rows exported: **1,952,416** across 24 data tables + table_inventory + export_meta
- core (t133): nations 251 · clubs 84,259 · competitions 7,047 · stadiums 48,413 · cities 56,293 · awards 3,545 · languages 126 · injuries 115 · weather 334 · currencies 173 · starting_records 84,477 · teams 84,507
- basic_people: 658,011 (t123 framing, ca@48/pa@50/year@52, closure diff=0)
- name pools (t106): name_first 245,981 · name_second 542,060 · name_common 85,668 · common_name_links 12,056 · club_links 9,261 · simple_vars 28,552 · fantasy_draft_names 40
- star players (t135): 21 cards × 54 PDxx = 1134 attribute rows
- table_inventory: 92 entries (79/79 numbered tables closed + 13 special members)
- indexes: 25 (uid lookups < 5ms)
- selftest: PASS (0 failures)

boundary: competition/nation/city/stadium display names are not stored in these archives (verified) — `--search-name` covers club names, the three person name pools, and fantasy-draft names.
