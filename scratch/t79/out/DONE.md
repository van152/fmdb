DONE type=t79 status=complete

## Deliverables
- `scripts/t79_stad_team_harvest.py`
- `scratch/t79/out/xref_stad_team.json`
- `scratch/t79/out/field_map.json`
- `scratch/t79/out/verify.py`
- `scratch/t79/out/REPORT.md`
- `scratch/t79/out/DONE.md`

## Summary
- stadium (`table_21.dat`, 48,413 rows, client 38B / server 181B): 41 L3 + 4 held (`rdui`, `Sdtr`, `Splr`, `Ssds`) + 15 non-wire/subtable/unhandled; 143B server prefix statically proven (`STADIUM::read 0x1183f49..0x1183f54`); 37B common+identity 100% byte-identical across client & server; client anchors `Scti@3/Slat@17/Slon@21/ordinal@25/duni@29` reconciled.
- team (`table_24.dat`, server-only, 84,507 rows = 251 `NATIONAL_TEAM` + 84,256 `TEAM`): 11 L3 + 2 held (`rdui`, `PLgn`) + 12 non-wire/forwarded/computed; exact EOF + 9B footer closure.
- `table_extra_24.dat` (server-only, 6,929,586 B = `12 + 84,507*82 + 0`): statically bound to `TEAM+0xa0` (`0x11a15fa`, loader `0x3bb9b00`, reader `0x11a1580`); unique `(12, 82, 0)` framing self-certified + 82B grammar closed; `Twhm@10`, `Tmhm@11` L3 + `Tpvr@21` L3 internal.
- `CLUB+0x18` forwarding chain: `Crep/Cdvi/Cldi/Cndi/Codi/Csti` (all 6 t63 held fields) upgraded to L3 (`经 +0x18 转发的投影`) with full getter + setter chains and 82,515/82,515 bidirectional club-team integrity verified.
- Verification: `t79_stad_team_harvest.py --selftest --build` PASS, independent `verify.py` 12/12 PASS (0 forbidden imports), `t01_anchors.py` 7/7 PASS; L4=0.
