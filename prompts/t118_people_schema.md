# t118: `people_db.dat` & `PERSON`/`CONTRACT`/`PLAYER` Full Static Schema Extraction

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/` or `scratch/t01/LEDGER.json`. Write only to `scripts/t118_people_schema.py` and `scratch/t118/out/`.

## Goal
`t113b` decompiled the `db::` person hierarchy (`PERSON`, `CONTRACT`, `BASIC_PERSON`, `PLAYER`, `ACTUAL_PLAYER`, `ACTUAL_PLAYER_AND_NON_PLAYER`, `VIRTUAL_PLAYER`) and factory `sub_1410992C0`, producing 428 unique person 4CCs in `scratch/t113/out/funcs/` (`14109ad50.c` = 338KB `PERSON::get_prop`, `141201ae0.c` = 104KB `CONTRACT::get_prop`, `140eec1b0.c`, `140ee0800.c`, `140e50cd0.c`, `140ef0670.c`, `141084920.c`, `140e52de0.c`, `1410992c0.c`, etc.).
`t115` already achieved 100% byte-exact closure of `basic_people_db.dat` (all 658,011 rows, diff=0) and decoded the top-level framing of `people_db.dat` (400,443,970 B decompressed: `[2B zero][u32 count=658,011]` + `[u32 ordinal][u8 person_type][body]`).

Your job is to extract the COMPLETE static field schema, serialization order, and person-type dispatch map of the `db::` person hierarchy from the decompiled `.c` corpus in `scratch/t113/out/funcs/` and `scratch/t95/funcs/`, AND cross-verify against real sample records from `people_db.dat` (e.g., row 0 `Zarko Serafimovski` type=5, plus sample rows of types 1, 2, 3, 4, 5, 6 and known stars Harry Kane `uid=28049320`, Cristiano Ronaldo `uid=735216`, Lionel Messi `uid=7458500` if reachable by scanning or header probing).

## Authoritative Inputs Already On Disk
1. `scratch/t113/out/people_vtables_full.json` and ALL `.c` files in `scratch/t113/out/funcs/`
2. `scratch/t115/out/` (`basic_people_db.dat` full schema + star anchors: Kane `uid=28049320`, Ronaldo `uid=735216`, Messi `uid=7458500`)
3. `scratch/t95/funcs/` (1,173 decompiled functions — check for any shared stream/string/date/contract helpers)
4. Real `.dat` file: locate `people_db.dat` via `scratch/t115/out/` or `D:\tmp2b\fm24\input\` (READ-ONLY — never modify input `.dat` files!).

## Required Analysis
1. **Factory `sub_1410992C0` (`1410992c0.c`) Complete Class Table**:
   - Map every `person_type` (`case 1..6` and any others) to: C++ class name, allocation size in bytes, constructor VA, vtable VA, `read_from_stream` / `write_to_stream` / `get_prop` / `set_prop` VAs.
   - Identify any missing/un-decompiled critical VAs (especially `PLAYER::read_from_stream` `0x140e3fb20`, `ACTUAL_PLAYER::get_prop` `0x140e1c630`, `PLAYER_DATA` / `NON_PLAYER` serializers) so a follow-up 20-second `idalib` batch can grab them with zero guesswork.
2. **Full 4CC ↔ `mem_off` Extraction across ALL `t113/out/funcs/`**:
   - Parse `PERSON::get_prop` (`14109ad50.c`, 315+ 4CCs), `CONTRACT::get_prop` (`141201ae0.c`, 60+ 4CCs), and every other `get_prop`/`set_prop` in `scratch/t113/out/funcs/`.
   - Extract: `class_name`, `fourcc`, `hex_id`, `mem_off`, `width/type`, `direct_or_helper`, `helper_va`, `file:line`.
   - Reuse proven extraction patterns from `scripts/t108_extract_4cc_v2.py` (handle byte-cast arithmetic properly — do NOT scale `(_DWORD)a1 + N` by 8!).
3. **Wire Serialization Order for `PERSON`, `BASIC_PERSON`, `CONTRACT`, `ACTUAL_PLAYER` (`slot19` / `slot20` / `slot21`)**:
   - Parse every decompiled `slot19` (read) and `slot21` (write) in `scratch/t113/out/funcs/` into ordered field steps (`step_idx`, `stream_op`, `width`, `mem_off`, `version_gate`, `callee_va`, `linked_4ccs`).
   - Cross-check with the first 20 rows of `people_db.dat` (decompressed in-memory via `zlib` streaming — do NOT write a 400MB decompressed dump to disk!) to verify exact byte-level parsing of at least `PERSON` header fields (`uid`, `first_name_id`, `second_name_id`, `common_name_id`, `dob`, `nation`, etc.) and report exact offsets where `PLAYER` / `NON_PLAYER` subclass bodies begin.
4. **Honesty & Precision**:
   - Clearly distinguish L3-verified (code + byte-verified on `people_db.dat`) vs static-only (decompiled `get_prop` ↔ `read_from_stream`) vs missing-decompilation (`need_ida_vas` list).

## Deliverables
Write to `D:\tmp2b\fm24-db\scripts\t118_people_schema.py` (with `--selftest`) and `D:\tmp2b\fm24-db\scratch\t118\out\`:
1. `people_factory_map.json` — complete `person_type` dispatch table + `need_ida_vas` prioritized list
2. `people_4cc_mem.json` — all extracted `PERSON`/`CONTRACT`/`BASIC_PERSON`/etc. 4CC ↔ `mem_off` mappings
3. `people_wire_steps.json` — ordered `read_from_stream`/`write_to_stream` steps + sample `people_db.dat` row probe results
4. `REPORT.md` — concise technical summary
5. `DONE.md` — `DONE type=t118`, key metrics, `--selftest` PASS confirmation

Run `py -V:3.12 -B scripts/t118_people_schema.py` and `--selftest` before finishing.
