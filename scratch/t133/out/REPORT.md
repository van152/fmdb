# t133 — FM24 `0x0df1` numeric-table reader

| Metric | t112 baseline | t133 |
|---|---:|---:|
| Footer-closed tables | 66/79 | **79/79** |
| Failed / skipped | 0 / 13 | **0 / 0** |
| Rows in footer-closed tables | 1,942,341 | **2,846,936** (+904,595) |
| `--verify-all` elapsed | 6.4 s (brief) | **9.084 s** |

The reader covers the numeric `table_<id>.dat` inventory of the two supplied FMF archives. It validates the payload envelope/version and row count, walks from byte 13, and only sets `footer_closed` when all header rows are consumed at `len(payload)-9`. Every table has `diff=0`. The new grammars also check the ordinal at the identity position reached by the grammar; they never search for an identity or use one to advance. At runtime the reader uses Python, the unmodified t112 module and the vendored `zstandard`; no IDA or Unicorn. The C files are offline evidence, not runtime inputs.

## Newly closed tables and wire grammar

All widths below exclude the leading one-byte row selector; `I` is the three `u32` identity lanes. `B/H/W/Q` are 1/2/4/8 bytes little-endian; `S` is `W` length followed by that many UTF-8 bytes; `V(c; …)` is a count of width `c` then that many records; `sB/sH/sW` indicate signed counts. Complete ordered definitions, including nested gates and opaque fixed reads, are in [`scripts/t133_fm24_reader_v2.py`](../../../scripts/t133_fm24_reader_v2.py).

| Table | Rows | Body bytes | Grammar / C evidence |
|---|---:|---:|---|
| client/0, server/0 AWARD | 3,545 each | 76 | Selector 0; 38 reads in `AWARD_WIDTHS`, ending in `I`. Direct database-reference path of `0x140e48db0`, all 38 widths and positions checked against both t121 traces. |
| client/3 CLUB | 84,259 | 53–155 | Selector 0: `5W, raw6, S, S, B, H, I`. Selector 12 prepends `W,B` (league-body fields at `+0x170,+0x178`); `0x14157d9f0 → 0x14452a1a0`, then `0x140e5b1a0` and `0x1411d1730`. |
| server/3 CLUB | 84,259 | 80–2,617 | Same head and selector-12 prefix; `CLUB_EXT` before terminal `B,H`; server `TEAM_CONTAINER` vectors before `I`. Ordered details below. |
| client/9 NATIONAL_TEAM_CONTAINER | 251 | 57–460 | Selector 0; `NTC_COMMON, B,H,I`. `NTC_COMMON = W,7B,W,16B,V(B;W,5B),V(B;W,4B),V(B;W,4B),4H`. |
| server/9 NATIONAL_TEAM_CONTAINER | 251 | 382–36,513 | Selector 0; `NTC_PREFIX, NTC_COMMON, NTC_SERVER_TAIL`, from `0x14105d510` plus t49. The prefix has count-driven vectors, 20 repeated `V(B;W)` lanes, two `u16`-counted tag-gated `NTC_PREF` lists, and nested tagged records; the server tail adds scalars and counted vectors before `I`. `NTC_TAGGED10` uses a signed `H` tag and its thresholds 2 and 3. |
| server/24 NATIONAL_TEAM / TEAM | 84,507 | 85–665 | Selector 10: `TEAM`. Selector 11: `3W,B,7W,7B,V(sB;B,W,W,B),TEAM`. Element reader `0x141053a80 → 0x143ee68c0` proves the 10-byte stride; no element is live in these 251 rows. TEAM details below. |
| server/25 COMP | 7,047 | 197–1,893 | Selector 0; `COMP` in wire order under `0x140ed1440 → 0x143caa6d0 → 0x140eb7a00`. Header scalars/dates, tag-gated stats and names, scalars and `V(W;H)`, optional A8 record, `+0xe0` gate, vectors and optional E8 and subsequent records, late scalar lanes, `I`. Exact continuation/gates in `COMP_NAMES`, `COMP_STAT_A/B`, `COMP_A8`, `COMP_E8_ITEM`, `COMP_D` and `COMP`. The row0 trace agrees over all 898 body bytes (493 captures). |
| server/29 STARTING_LOAN | 13,278 | 74 | Selector 0; `5W,B,W,W,B,W,Q,B,W,W,H,W,B,W,I`. `0x1415782c0 → 0x144519690`, including `0x14156ab70 → 0x144509ac0`. t121 captures only 50 body bytes on the legacy path; the `0x0df1` fields are bound by actual destination offsets (`LOAN_DESTS`) rather than the legacy wire offsets. |
| server/32 STARTING_FUTURE_TRANSFER | 315 | 59–211 | Selector 0; `FUTURE,I`. `FUTURE = 6W,B,W,B,H,V(sH;8W,B,W,B),3B,Q,V(B;H,W,raw10,B,raw9,W,B),B`. `0x1411919d0` and helpers `0x141191e80`, `0x14156af70` and `0x1412e6ff0`. |
| server/36 STARTING_MANAGER_HOF_RECORD | 6,535 | 62–446 | Selector 0; `W,W,S,S,S,W,V(W;W,W,H,V(W;H)),I`. `0x14157e310 → 0x14452d790`. |
| server/71 STARTING_PAST_TRANSFER | 616,665 | 37–502 | Selector 0; `5W,3B,V(B;FUTURE),B gate,[LOAN if nonzero],I`. `0x141199440` calls `0x1411919d0` per future-transfer element and `0x1415782c0` for the optional loan. Nested forms do not consume a row selector or identity. |
| server/72 STARTING_PAST_TRADE | 138 | 60–105 | Selector 0; `2W,4×V(W;W),2W,A,Bv,A,Bv,I`, where `A=V(W;B,W,B,B,B,W,B,H)` and `Bv=V(W;B,W,W,B,B)`. `0x14153f260 → 0x1444dff00` and counted helper at `0x141726770`. |

Server CLUB `CLUB_EXT`: `B,H,W,B,V(sB;W),B subtype,[W,B,raw3,raw13,W,raw20 if subtype=0],V(sB;B,B,W,W,B,W,H,B,B,B,W),V(sB;W,W,W),H,W`. Subtype 2 has no body. `TEAM_CONTAINER` then contributes `V(B;W),V(B;W),V(sB;W),V(sB;W),V(B;W),V(B;raw16),V(sH;W,W,Q,H,W,W,B,B)`. Both archives have 84,256 selector-0 and 3 selector-12 rows. The report includes the first row of each selector separately.

`TEAM` (`0x1411a1280`): `B,B,H,6W,B,W,V(H;W),W,W,5B,W,B,TEAM_BASE`. `TEAM_BASE` (`0x1411c2780 → 0x143fff990`): `6B,W,S,B,S,B,I`. Both selectors share this tail. `TEAM` starts immediately after the selector or after the selector-11 prefix. Relative to `TEAM`, the squad count is at +33, `Tnod` at `48+4*n`, and `TEAM_BASE` at `53+4*n`. Relative to `TEAM_BASE`, `Ttyp/Tisn` are at +0/+1, owner at +6 and `Tlna` at +10; `Tsna` is at `15+long_len`.

## Validation and limits

- `--selftest` passed 51 checks, including every new table, representative inherited tables, malformed nested controls, body truncation for every new table and all three polymorphic-table selector checks. `--list` and `--dump server 24 --limit 1` also passed.
- Of the 13 new tables, nine had a complete byte-matching t121 row0 capture, three polymorphic table instances had matching prefixes, and LOAN's 50-byte capture matched the corresponding payload prefix but not the current grammar. The traces are not used to infer variable row strides.
- `l3_named_field_total=568` counts names bound on the supported archive sides; the source contains 1,104 joined mappings. Wire closure does not certify all field meanings or other versions. In this fixture the unsupported live `+0x150` subtype in CLUB (`0x141477160`) and the nonempty paths of guarded helpers `0x140839290` / `0x140839480` are not reached. Unexpected use fails closed rather than skipping bytes.
- `check_team_map.py` compared all 84,507 TEAM rows with the independent t79 replay and checked the associated `table_extra_24` rows. The extra member is outside the numeric inventory (`12 + 84,507×82`, no footer). `0x1411a1f80` explicitly calls the four-byte reader `0x140db8980 → 0x143b48db0`: extra row offsets `29,33,37,41,45,57` land at object offsets `+e4,+e8,+ec,+f0,+f4,+e0`; every lane is `0x076c0001` (1900-01-01). `Twhm/Tmhm/Tpvr` at offsets `10/11/21` match the t79 domains. The check and field-map overlay are in `team_field_map_check.json`; no t79 source or prior field map was changed. Recovered C and logs are in `static/` and `recover*.log`, from an offline copy; `editor_merge_v2.i64` was not modified.
