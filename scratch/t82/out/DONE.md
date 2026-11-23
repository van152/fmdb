DONE type=t82 status=complete

## Deliverables
- `scripts/t82_extra3_remaining.py`
- `scratch/t82/out/xref_extra3.json`
- `scratch/t82/out/field_map.json`
- `scratch/t82/out/domain_stats.json`
- `scratch/t82/out/verify.py`
- `scratch/t82/out/REPORT.md`
- `scratch/t82/out/DONE.md`

## Summary
- **Scope**: `table_extra_3.dat` remaining payload (`CLUB+0x100` `CLUB_IN_GAME_DATA` + `CLUB+0xb0` `TEAM_CONTAINER_IN_GAME_DATA`), excluding t71's 24 already-L3 items (`Cyfn[26]`, `Cebd[48]`, 22 `cnst[155..176]`); zero t57/t63 negatives overturned; `L4=0`.
- **New `L3` (35)**:
  - `CLUB+0x100` direct scalars (6, server-only): `Ctlv`, `Cmle`, `Cyim`, `Cyfb`, `Cytv`, `Crcb`.
  - `CLUB+0x100 -> +0x78` election (5, server-only, 11,963 present rows; `elec_club == row_ordinal` 11,963/11,963, `elec_flag==1 iff Cown∈{3,7}` 84,259/84,259): `Cetl`, `Cmtm`, `Cect`, `Cemn`, `Cemx`.
  - `CLUB+0x100 -> +0xf8` supporter profile (6, server-only): `Csly`, `Csps`, `Cspt`, `Csaf`, `Cste`, `Cspe`.
  - `CLUB+0x100 -> +0x48` UEFA coeff ring buffer (10, server-only, 569 present rows): `Cuf1..Cuf9`, `Cf10`.
  - `CLUB+0xb0` attendance & common-tail hashtag (4): `Catd`, `Cmna`, `Cmxa` (server-only) + `TCht` (client+server, 100% identical).
  - Lists & polymorphic `base+0x00` (4, server-only, full item-level validation & wrong-UID negative controls): `Cbbl` (tag 7, 75 items), `Csoc` (tag 5, 2,616 items), `pcpt` (tag 38, 29 items), `CPsL` (`extra+0x68`, 694 items).
- **`held` (39, every item carries exact `first_counterexample`)**: `Csth` (3 rows `-1 < 0`, row 69706), `CScP/Cown/Chti/Cepr` (no scoped `enum_ref`), `Cpfr/C2pf/Cdfo/Cafo` (78/90/1441/99 out-of-domain), `TCnn` (0 populated), `ttcl/tbcl` (duplicate XML + 6,586 zero fallbacks), `1scl..3tbc` (10 derived read-only), `Cscm` (118/15,360 `slsn=0` not in `table_23`), `Cspb/Cren` (unscoped sub-enums), `Camc` (973/1,601 `apfr=0 < 1` + unscoped `type`), `TCrs` (2,709/23,027 `PUnJ` outside `ftjn` + unscoped `PUnI/PUnT`), `Tko1..3/Tkg1..3` (405,204 items cleanly 6-partitioned & client==server, held for missing `list_item_fields`), `CssT..E` (4 preserved t63 `held`, tag 35 0/84,259 rows).
- **Critical Negative Proof**: `CBW*/CBD*` and all 117 `club.xml[211..327]` record 4CCs route via `TC_GET2`/`CLUB_GET` → `0x11e8af0` → `TC_RECORD_GET 0x3ebad50` on global `VA 0x141b60190` (`DATABASE_TABLE<STARTING_RECORD>`, type `0x2d=45` → `server_db/table_45.dat`, 84,477 rows), NOT `table_extra_3.dat` (0 bytes).
- **Verification**: `t82_extra3_remaining.py --selftest --build` PASS; independent `verify.py` (0 forbidden imports, pure-struct PE32+, 296 static witnesses, 84,259×2 byte-exact EOF replay) **9/9 PASS**; `t01_anchors.py` **7/7 PASS**.
