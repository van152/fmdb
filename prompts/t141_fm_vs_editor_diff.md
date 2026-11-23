# t141: 491 MB `fm.exe` (Game Engine) vs 74 MB `editor.exe` Database Kernel Diff Audit

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, `D:\tmp2b\fm24\input\*`, or any existing `scripts/tNN_*.py` files. Write ONLY to `scripts/t141_fm_vs_editor_diff.py` and `scratch/t141/out/`.
Keep stdout compact (< 50 lines per command). Do NOT launch IDA on `fm.exe` (491 MB would be slow/huge) — use fast pure-Python binary scanning (`pefile`, `capstone`, `re`, `struct`) directly on the read-only PE files!

## Inputs (READ-ONLY)
- `D:\tmp2b\fm24\input\fm.exe` (491,339,776 B — FM24 game executable)
- `D:\tmp2b\fm24\input\editor.exe` (74,807,296 B — FM24 pre-game editor executable)
- `scratch/t95/vtable_index.json` (67 `DATABASE::` table classes in `editor.exe`)
- `scratch/t113/out/people_vtables_full.json` & `scratch/t120/out/people_unicorn_traces.json` (`db::` person hierarchy)

## Mission
Perform a rigorous, machine-verifiable binary comparison between **`fm.exe` (491 MB)** and **`editor.exe` (74 MB)** focusing specifically on the **FM24 Database Layer**:
1. **PE Layout & Section Comparison**:
   - SHA-256, ImageBase, TimeDateStamp, PE sections (names, sizes, virtual addresses, characteristics — e.g. does `fm.exe` have `.reloc` obfuscation/Denuvo/anti-tamper sections that `editor.exe` lacks?).
2. **Complete MSVC RTTI Class Census (`DATABASE::`, `db::`, and `STARTING_*`)**:
   - Scan BOTH `fm.exe` and `editor.exe` for ALL MSVC RTTI type descriptor strings matching `\.\?AV[A-Za-z0-9_@]+(DATABASE|db)@@` (and any `STARTING_` / `TABLE` / `ARCHIVE` classes).
   - Produce exact set diffs:
     - `common_database_classes` (present in both)
     - `fm_only_database_classes` (in `fm.exe` but NOT `editor.exe`!)
     - `editor_only_database_classes` (in `editor.exe` but NOT `fm.exe`!)
     - Same 3-way set diff for `@db@@` classes!
   - Note explicitly if `fm.exe`'s `.rdata`/code is packed/encrypted (Denuvo/SteamStub) — if RTTI strings are plaintext vs packed, prove it quantitatively!
3. **Database String & Format-Anchor Comparison (`server_db.dat`, `client_db.dat`, `people_db.dat`, `basic_people_db.dat`, `lang_db_2400.dat`, `pl_hist_dt.dat`, `table_%d.dat`, `tad.`, `fmf.`, `0x0DF1`)**:
   - Search BOTH binaries for all database archive filenames, magic signatures (`tad.`, `fmf.`), and `PDxx` / Big-3 4CC immediate literals or ASCII strings!
   - Document clearly what database loader strings/structures are shared vs unique to `fm.exe` (e.g. savegame / match engine / live DB tables) vs unique to `editor.exe` (e.g. XML/DBC editor export)!
4. **Honesty & Precision**:
   - Never speculate beyond what is directly observed in the PE bytes. Clearly state whether `fm.exe` has packed/protected code sections (if so, document which sections are plaintext vs high-entropy).

## Deliverables
Write `scripts/t141_fm_vs_editor_diff.py` (with `--selftest`) and `scratch/t141/out/`:
1. `fm_vs_editor_diff.json` — PE metadata, section entropy/layout, full RTTI 3-way set diffs (`DATABASE::` & `db::`), DB filename/magic string comparison
2. `REPORT.md` — concise engineering comparison report with summary tables
3. `DONE.md` — first line `DONE type=t141`, exact RTTI counts (`fm` vs `editor`, common/fm-only/editor-only), entropy/packing finding, `--selftest PASS`

Run `py -V:3.12 -B scripts/t141_fm_vs_editor_diff.py` and `--selftest` before finishing!
