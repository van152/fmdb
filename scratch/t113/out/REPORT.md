# t113 — people database reconnaissance (partial)

## Status
The requested full RTTI sweep, vtable slot analysis, Hex-Rays output and real `people_db.dat` person-type histogram are **not complete**. `people_vtables.json` explicitly records partial status; an empty class list is not evidence that classes are absent. No fabricated slot or person-type data is reported. `scratch/t95/editor_work.i64` and all source data remain untouched.

## Archive findings
Both files use a 13-byte `tad.`/Zstandard wrapper (`03017461642e` + 3-byte metadata + Zstd frame at offset 8), not the FMF directory-entry format handled by `t38_multiframe.py`; therefore it cannot truthfully list internal FMF members.

| Archive | Compressed file | Decompressed payload | Header / findings |
|---|---:|---:|---|
| `people_db.dat` | 67,502,767 B | 400,443,970 B | prefix `00005b0a0a004b080a00050000`; first 4 bytes are not a row count (would be 173,735,936). Variable-record walk/type distribution not established. |
| `basic_people_db.dat` | 12,934,775 B | 54,060,043 B | count 658,011, flag 0; row grammar closes exactly. |

`basic_people_db.dat` validated layout: 5-byte count/flag prefix; each row starts `11 <class>` with widths `{1:83, 2:83, 3:83, 4:34, 5:22}`; 9-byte footer `00000000014cbd5477`. Class counts: 1=166,064; 2=476,158; 3=4,757; 4=9,839; 5=1,193 (sum 658,011). These are BASIC_PERSON row classes, **not** the `people_db.dat` person_type distribution requested.

## Architecture
```text
PERSON hierarchy (requested; RTTI edges not established here)
  PERSON
  ├─ PLAYER
  ├─ NON_PLAYER
  ├─ OFFICIAL
  ├─ JOURNALIST
  └─ HUMAN
Other requested classes: BASIC_PERSON, PLAYER_DATA, NON_PLAYER_DATA, CONTRACT,
SPOKESPERSON — relationships/vtables require IDA RTTI validation.
```

Per-class 4CC totals are unavailable; no Hex-Rays files were generated. Existing `scratch/t95/funcs/140e4fd70.c` describes `BASIC_PERSON::slot19`, but was not misrepresented as t113's batch result.

## Reproduction / limitations
`python -I -B scripts/t113_people_db_ida.py --selftest` passes archive framing and the complete basic-person row walk. The normal run returns 1 to signal partial completion. `t38_multiframe.py --selftest` independently passes its own checks, but its FMF assumptions do not fit these standalone `tad.` archives.