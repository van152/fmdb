DONE type=t83 status=complete

## Deliverables
- `scripts/t83_five_tables_l3.py`
- `scratch/t83/out/field_map.json`
- `scratch/t83/out/xref_award.json`
- `scratch/t83/out/xref_language.json`
- `scratch/t83/out/xref_weather.json`
- `scratch/t83/out/xref_derby.json`
- `scratch/t83/out/xref_media.json`
- `scratch/t83/out/domain_stats.json`
- `scratch/t83/out/verify.py`
- `scratch/t83/out/REPORT.md`
- `scratch/t83/out/DONE.md`

## Summary
- XML denominator (MANIFEST-verified `master.json`, 5 tables): **188/188** fields accounted -> **152 L3**, **17 held** (each with static chain + exact `first_counterexample`), **19 non-wire/meta/subtable** (`10 editor_metadata`, `6 non_wire_computed`, `2 non_wire_language_layer`, `1 subtable_backed`), **21 internal wire slots** (0 uncovered bytes across all 5 tables in both client & server archives); **L4=0**.
- `award` (`table_0.dat`, 3,545 rows x 77B fixed, client==server): L2 77B column profile + multi-table FK matrix (`t5/t6/t10/t47/t25/t30/t3` with wrong-UID control) + **24 L3** / **7 held** (`rdui`, `AWsc`, `AWty`, `AWdr`, `AWfo`, `AWxa`, `AWbr`) / 7 non-wire-subtable (`AWna/AWsn` language layer, `AWsh` -> `table_12`); 64B body 0-gap closed.
- `language` (`table_8.dat`, 126 rows, client==server): L2 17B suffix + 13B identity profile + multi-table FK matrix + **5 L3** (`duni`, `Lnam`, `Linf`, `Ldff`, `Lnat`->`t10` `[db+0x28]`, Chinese->55 / English->139) / **4 held** (`rdui`, `Lfam`, `Lgro`, `Lsub`) / 3 non-wire; 17B suffix 0-gap closed.
- `derby` (`table_18.dat`, 1,567 rows, client 36B / server 42B): t76c upgraded to **18 L3** / **1 held** (`rdui`) / 3 non-wire; `DERBY::read` (`0x3d00950`) always reads 4 lstrings (`Dnam, Dsnm, Dasn, Danm`); server +6B gate (`0x3d00aae`) = `D1tw@s28(+0x70)`, `D1td@s30(+0x72)`, `D1tl@s32(+0x74)`; `Dtm1/Dtm2` bound to `[db+0x98]` = `table_24 TEAM` (correcting t76c club fit); `Dwdr@c34/s40`, `Dntr@c35/s41` (correcting t76c `slots_client_18.json` typo).
- `weather` (`table_27.dat`, 334 rows, client==server): t76c upgraded to **90 L3** / **1 held** (`rdui`) / 3 non-wire; quadruple static proof corrects wind/precip swap in both `t01l(E27)` and `t76c(E118)` (`blk+2..6` = `w{b}w0..w4`, `blk+7..11` = `w{b}p0..p4`), proves `w{b}sd` is 2B i16@`blk+0..1` and `w{b}dn` (`tend`) is `blk+22` with `0x64` explicit null sentinel; normalizer `0x43e7e10` (76/67/468) verified.
- `media` (`table_7.dat`, 208 rows, client 36,824B / server 38,280B): `MEDIA_SOURCE::read` (`0x15457c0`) closes 208/208 rows on both archives; server +7B gate (`0x1545cfe`) = `1B Mper + 1B Mscp + 4B Mdlp + u8 cnt_jor(=0)`; `Mcli` stores 8B CLUB `(duni, rdui)` UID pairs (450/450 in `table_3` UIDs) + `lstr curl`; t74 pre-identity 5B 16 distinct values 100% decomposed (`u32(cnt_lnm=0 or last Mlnm ordinal) + u8(Mapc)`); **15 L3** / **4 held** (`rdui`, `Mper`, `Mscp`, `Mdlp`) / 3 non-wire.
- Verification: `t83_five_tables_l3.py --selftest --build` 5/5 PASS; independent `scratch/t83/out/verify.py --selftest` **11/11 PASS** (+ 741 `editor.exe` instruction/rel32 cross-checks, 10/10 t74 & 4/4 t76c SHA-256, tamper rejection PASS); `scripts/t01_anchors.py` **7/7 PASS**; `L4=0`.
