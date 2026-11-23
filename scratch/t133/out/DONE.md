DONE type=t133

- **79/79** numeric tables `footer_closed`, all `diff=0`; **0 failed, 0 skipped**.
- **2,846,936** rows decoded, all in footer-closed tables (+904,595 vs t112).
- `--verify-all`: **9.084 s**, vendored `zstandard`; `--selftest`: **PASS** (51 checks).
- `--list` and `--dump server 24 --limit 1`: PASS.
- Offline t79 cross-check: **84,507** TEAM rows and **84,507** `extra_24` rows, six packed-date lanes checked. `extra_24` is separate from the 79 numeric tables.

Deliverables: `scripts/t133_fm24_reader_v2.py`, `scratch/t133/out/reader_v2_verify.json`, `scratch/t133/out/REPORT.md`, `scratch/t133/out/selftest.log`, and `scratch/t133/out/team_field_map_check.json` with its offline reproducer and static evidence.
