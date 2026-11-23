# t113 delivery status: PARTIAL

DONE type=t113

- `people_db.dat`: 67,502,767 compressed B; 400,443,970 decompressed B.
- `basic_people_db.dat`: 12,934,775 compressed B; 54,060,043 decompressed B; 658,011 rows validated; class histogram 166,064 / 476,158 / 4,757 / 9,839 / 1,193; row chain and footer close.
- RTTI classes/vtables and slots: 0 verified in this run.
- `people_db.dat` person_type histogram: unavailable; variable record framing not established.
- Hex-Rays function sources / 4CC coverage: none produced.

The completion gate is intentionally not marked complete. The requested remaining evidence needs an IDA-backed RTTI scan and a validated people-record walker.

Delivered: `people_vtables.json`, `people_archives_inventory.json`, `REPORT.md`, `DONE.md`. Script: `scripts/t113_people_db_ida.py` (supports `--help` and `--selftest`). No `funcs/*.c` generated.