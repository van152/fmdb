# t140 (S+ Benchmark): FM24 `.dat` Bidirectional Re-Encoder, FMF/zstd Repacker & Dual Round-Trip Verification Engine

You are working in `D:\tmp2b\fm24-db`.
**Strict Safety Rules (Read-Only Guardrails):**
- **NEVER** modify `scratch/data/*`, `D:\tmp2b\fm24\input\*`, `Z:\SteamLibrary\*`, `reports/`, `scratch/t01/LEDGER.json`, or any existing `scripts/tNN_*.py` files.
- Write **ONLY** to `scripts/t140_fm24_roundtrip.py` and `scratch/t140/out/` (you may put temporary helper modules inside `scratch/t140/` if needed).
- Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` to import `zstandard` (do NOT rely on `ctypes.util.find_library`).
- Never start FM24 game or FM24 Editor.

---

## Authoritative Inputs Already Verified On Disk
1. `scripts/t133_fm24_reader_v2.py` + `scripts/t112_fm24_reader.py` — Pure-Python **79/79** numbered-table decoders (`2,846,936` rows, `0` failed, `0` skipped, all `diff=0`) for `scratch/data/server_db.dat` and `scratch/data/client_db.dat`.
2. `scripts/t106_special_members.py` — **13/13** non-numbered special members (`name_table_*`, `club_links`, `common_name_links`, `simple_vars`, `table_for_old_save_*`, `fantasy_draft_future_regens`, `summary.dat`).
3. `scripts/t96c_unicorn_master.py` + `scripts/t119_unicorn_last5.py` — Native Unicorn x86_64 `editor.exe` `slot19` harness (79/79 clean).
4. `scripts/t120_people_unicorn.py` + `scripts/t126_player_attributes_l3.py` + `scratch/t135/out/star_player_cards.json` — Native Unicorn `people_db.dat` harness + verified **54/54 `PDxx`** attribute map + Harry Kane (`uid=28049320`, `people_db` offset `252,735,069`, body `1,148 B`, `PCAB=184`, `PPAB=185`, `PDfn=19`).
5. `scratch/t95/funcs/*.c`, `scratch/t124/out/funcs/*.c`, `scratch/t132/out/funcs/*.c` — Decompiled Hex-Rays C for `slot19` (read) and `slot21` (write).

---

## Your S+ Mission: Build a Real Bidirectional FM24 Database Writer & Prove Bit-Exact + Mutated Dual Closure

Implement `scripts/t140_fm24_roundtrip.py` covering **ALL THREE STAGES** below (zero cheating: never pass through unparsed raw row blobs on any table you claim is structurally re-encoded!).

### Stage 1 — Structural Decode → Re-Encode Identity Round-Trip (Aim for 79 / 79 Tables = 0-Byte SHA-256 Exact!)
- Build a structural serializer/encoder matching `t133_fm24_reader_v2.py`'s exact grammar (fixed-stride tables AND variable-length nested/polymorphic tables: `AWARD`, `CLUB` server/client incl. selector-12, `NTC` server/client, `NATION` server/client, `COMP` server/client, `TEAM`/`NATIONAL_TEAM` incl. selector-11, `STADIUM`, `CITY`, `STARTING_RECORD` `t45`/`t48`, `STARTING_PAST_TRANSFER` `t71`, `STARTING_PAST_TRADE` `t72`, `STARTING_FUTURE_TRANSFER` `t32`, `STARTING_LOAN` `t29`, `STARTING_MANAGER_HOF_RECORD` `t36`, etc.).
- Re-encode the 13-byte table header (`03 01 tad. <ver=0x0df1> <row_count> <reserved>`), every decoded row (`[1B selector][encoded body ending in 12B identity]`), and the exact 9-byte footer (`[0x00][8B footer]`).
- **Verification target**: Prove **`sha256(reencoded_payload) == sha256(original_payload)`** (`diff_bytes == 0`) across **ALL 79 / 79** numbered tables (`2,846,936` rows)! Report exact per-table SHA-256 match count (`?/79`) honestly.

### Stage 2 — Full FMF/zstd Archive Repacker + Semantic Mutations (Including Variable-Length String Changes!)
- Implement a clean, spec-compliant **FMF archive writer** (inspect `scripts/t112_fm24_reader.py` `_DirectoryReader` & `scripts/t38_multiframe.py` to reproduce the exact FMF header `02 01 66 6d 66 2e 08 00 00`, `data_base`, zstd-compressed directory tree with recalculated `offset` / `size` / `packed_size` for every member, and zstd-compressed member frames — preserving all non-numbered special members byte-for-byte!).
- Produce **real patched FMF archives** in `scratch/t140/out/patched_server_db.dat` and `scratch/t140/out/patched_client_db.dat` with at least **6 concrete semantic mutations** across different table classes (including **string length changes** that shift every subsequent row offset AND member `size`/`packed_size`!):
  1. `server/3` & `client/3` (`CLUB`): Change row 0's UTF-8 club name string to a **longer** test string (e.g., append `" [T140-PATCHED]"`, +15 bytes!)
  2. `server/45` (`STARTING_RECORD`): Change row 0's `namelen` + UTF-8 string to a **different length** string
  3. `server/21` (`STADIUM`): Mutate row 0's numeric capacity/attribute field (using a verified L3 4CC offset from `t121/out/master_79of79_l3.json`)
  4. `server/0` & `client/0` (`AWARD`): Mutate a verified L3 scalar field on row 0
  5. `server/10` & `client/10` (`NATION`): Mutate a verified L3 scalar field on row 0
  6. `server/25` & `client/25` (`COMP`): Mutate a verified L3 field on row 0
- **Stage 2B (Bonus Crown Jewel — `people_db.dat` Superstar Mutation)**:
  - Extract Harry Kane (`uid=28049320`, `people_db` offset `252,735,069`, body `1,148 B`), mutate:
    - `PCAB` (CA, `body[6:8]`): `184 → 190`
    - `PPAB` (PA, `body[8:10]`): `185 → 195`
    - `PDfn` (Finishing, `body[29+17]` = `body[46]`): `19 → 20`
    - `PDpc` (Pace, `body[29+53]` = `body[82]`): `14 → 17`
  - Save the mutated `PLAYER` record (and verify byte-exact length & framing).

### Stage 3 — Dual Independent Verification (`t133` Pure Python + REAL `editor.exe` Native x86_64 Machine Code via Unicorn!)
1. **Unmodified `t133` Pure-Python Verification**:
   - Point `t133_fm24_reader_v2.py`'s archive reader at `scratch/t140/out/patched_server_db.dat` and `scratch/t140/out/patched_client_db.dat`!
   - Prove **ALL 79 / 79 tables** in the repacked patched FMF archives still decode to **`footer_closed == True` (`diff == 0`, `2,846,936` rows)**, ALL non-numbered special members (`t106`) remain intact, ALL 6 mutated fields read back with the EXACT new values, and ALL unmutated rows remain bit-identical!
2. **REAL `editor.exe` Native x86_64 Machine-Code Verification (Unicorn `slot19`)**:
   - Feed the re-encoded/mutated binary rows from `patched_server_db.dat` & `patched_client_db.dat` (`CLUB` with longer name, `STARTING_RECORD` `t45` with changed name length, `STADIUM`, `AWARD`, `NATION`, `COMP`) into **real `editor.exe` `slot19` x86_64 code** using `t119_unicorn_last5.setup_patched_emulator()` + `t96c_unicorn_master.construct_via_factory()` / `run_one_row()`!
   - Prove `editor.exe` natively consumes the EXACT new row lengths (`err == None`, `rip == STOP_ADDR`, `bytes_consumed == new_row_len`) AND inspect the emulated C++ object memory (`emu.mu.mem_read(obj + off, ...)`) to confirm `editor.exe` stored the mutated string/scalar values cleanly!
   - Feed Harry Kane's mutated `PLAYER` record into `t120_people_unicorn.run_person_row()` and prove `editor.exe` (`PLAYER::slot19`) returns `ok == True`, consumes all `1,148` bytes, and writes `CA=190` at `obj - 0x78`, `PA=195` at `obj - 0x76`, `PDfn=20` at `obj - 0x70 + 17`, `PDpc=17` at `obj - 0x70 + 53` directly into C++ object RAM!

---

## CLI & Deliverables
Write `D:\tmp2b\fm24-db\scripts\t140_fm24_roundtrip.py` supporting:
- `--roundtrip-all` (Stage 1: bit-exact SHA-256 round-trip across all 79 tables)
- `--build-patched` (Stage 2 + Stage 3: build `patched_server_db.dat` + `patched_client_db.dat`, mutate Kane, run dual `t133` + Unicorn `editor.exe` verification)
- `--selftest` (fast end-to-end verification exiting 0 on PASS, 1 on FAIL)

Write deliverables to `D:\tmp2b\fm24-db\scratch\t140\out\`:
1. `roundtrip_79_report.json` — per-table Stage 1 SHA-256 match results (`?/79` bit-exact, timing, row counts)
2. `patched_dual_verify.json` — Stage 2 mutations + Stage 3 `t133` 79/79 verification + Unicorn `editor.exe` native C++ RAM readback proof (including Harry Kane!)
3. `patched_server_db.dat` & `patched_client_db.dat` — genuine repacked patched FMF/zstd archives
4. `REPORT.md` — concise engineering report with Stage 1 / Stage 2 / Stage 3 verification tables
5. `DONE.md` — first line `DONE type=t140`, headline metrics (`?/79 SHA-256 bit-exact`, `79/79 patched FMF t133 closed`, `Unicorn native editor.exe readback PASS`, `--selftest PASS`)

Run `--roundtrip-all`, `--build-patched`, and `--selftest` before finishing!
