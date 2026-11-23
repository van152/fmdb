# t143 (`gpt-6.2-sol` max): `lang_db_2400.dat` (71.4 MB) + `lang_update_db.dat` (2.3 MB) Full 352-Member FMF Decoding & Entity Name Join

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or any existing `scripts/tNN_*.py` files. Write ONLY to `scripts/t143_lang_db.py` and `scratch/t143/out/`.
Use `sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")` for `zstandard`. Keep input `.dat` files strictly READ-ONLY (decompress in-memory only; never dump 100MB+ blobs to disk).

## Breakthrough Discovery Already On Disk (`t130b`)
`scratch/t130/out/archive_inventory.json` just proved that BOTH `D:\tmp2b\fm24\input\lang_db_2400.dat` (71.4 MB) AND `scratch/data/lang_update_db.dat` (2.3 MB) are **FMF archives with an 8-byte `tad.` prefix (`raw[8:14] == 02 01 66 6d 66 2e`) containing 352 FMF members EACH**!
(Also feel free to inspect `scratch/t129/out/_probe*.py` only if helpful, or inspect the two FMF archives directly with `_DirectoryReader` / `archive_layout` from `scripts/t112_fm24_reader.py`.)
If you need to inspect `editor.exe`'s localization loader to confirm any record format, you may read `scratch/t95/funcs/*.c` or run read-only `idalib` on `scratch/t95/editor_work.i64` (NEVER touch `editor_merge_v2.i64`!).

## Your Mission
1. **Enumerate ALL 352 FMF members** in `lang_db_2400.dat` and ALL 352 FMF members in `lang_update_db.dat`:
   - Exact member paths, compressed/decompressed sizes, and groupings (e.g., by language code / table type / entity type!).
2. **Decode the Binary Record Grammar of the Language Members & Prove Byte-Exact Closure (`diff=0`)**:
   - Determine the exact header, record framing, key/ID layout (`uid`, `table_type`, `field_type`/slot, gender/plurality flags, UTF-8 / UTF-16LE strings), and footer closure across ALL 352 members of `lang_update_db.dat` AND `lang_db_2400.dat`!
   - Report exact closure rate (`?/352` members closed `diff=0` in `lang_update_db.dat`, `?/352` in `lang_db_2400.dat`), total localized string entries decoded, and per-language entry counts!
3. **Cross-Join Decoded Localized Names Against `t133` Core Entities (`CLUB`, `COMP`, `NATION`, `AWARD`, `STADIUM`, `CITY`)**:
   - Join decoded English + Chinese (Simplified/Traditional, if present!) localized names from `lang_db_2400.dat` + `lang_update_db.dat` onto real `uid`s from `t133_fm24_reader_v2.py` (`server/10` Nations, `server/25` Competitions, `server/3` Clubs, `server/0` Awards, `server/21` Stadiums)!
   - Emit 25+ verified multi-language showcase rows (e.g. Premier League, Champions League, England, Manchester City, Real Madrid, Arsenal, Bayern Munich, Ballon d'Or / Golden Boot, Wembley, etc. — exact English + Chinese localized names matched by `uid`!).

## Deliverables
Write `scripts/t143_lang_db.py` (with `--selftest`, `--lookup <UID>`) and `scratch/t143/out/`:
1. `lang_db_schema.json` — full 352+352 member inventory, exact binary record grammar, closure statistics (`?/352` & `?/352`), language breakdown, and 25+ verified multi-language entity joins
2. `REPORT.md` — concise engineering report with language table, grammar spec, and English/Chinese entity showcase table
3. `DONE.md` — first line `DONE type=t143`, headline closure metrics (`?/352` lang_update + `?/352` lang_db_2400, total localized strings decoded, `--selftest PASS`)

Run `py -V:3.12 -B scripts/t143_lang_db.py` and `--selftest` before finishing!
