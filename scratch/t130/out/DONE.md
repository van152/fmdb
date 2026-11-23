DONE type=t130b files_inventoried=14 default_handlers_absent=11/11 --selftest PASS

## t130b — 14-Archive FM24 Database Inventory + 11 Default-Handler Adjudication

- `scripts/t130_archive_inventory.py` written (with `--selftest`).
- `scratch/t130/out/archive_inventory.json` — complete 14-file inventory: byte size,
  SHA-256, head-16 hex, container type, FMF member count.
- `scratch/t130/out/REPORT.md` — markdown inventory + default-handler proof + closure cross-ref.
- `--selftest`: **PASS** (all checks re-derived independently).

Core stats:
- files_inventoried=14
- default_handlers_absent=11/11 (server_db 77 members / client_db 31 members fully scanned)
- selftest=PASS
