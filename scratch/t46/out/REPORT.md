# t46 — Nation Server table_10 Data-Side Profile

Status: `partial_data_profile_server_internal_grammar_open`. No L3 or L4 claims.

## Archive and Payload

- client `table_10`: present, 24,732 B, SHA-256 `7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34`; matches t25 exactly. Client rows were not regenerated.
- server `table_10`: present, 422,345 B, SHA-256 `19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f`; directory record count 251; member `server_db/table_10.dat`.
- archive directories: client 31 members; server 77 members. Frame selection used t38's `data_base + offset`, `packed_size` boundary, and declared `size`.

## Server Rows and Closure

- Server rows bound: 251; spans 141..30993 B, mean 1682.562 B, 195 distinct lengths.
- Identity tail: `ordinal|nation_row_id|repeated_nation_row_id|zero_marker at row_end-13`; all 251 rows uniquely match t25 ordinal/row-ID witnesses and marker `00`.
- L1 arithmetic closure: `14 + sum(row_lens=422323) + 8 = 422345`. Concatenated row SHA-256 `4162770e55007a453c8ac55381458d28b414a0b5ba3836d6365a0887558ea45b`.
- The first 88 rows also satisfy a naive shortest-tail walk, but it stops at row 88/body+62440. That negative result is retained. The delivered walk uses each exact t25-observed row ID as an independent identity witness; it does not use client lengths or counts.

## Grammar Differential

- Whole-row grammar: different. First counterexample is row 0: client span 65 B versus server span 632 B.
- A/B/C/D server segment mapping: unknown. No internal server count positions, count signedness, or item widths were accepted. Same-offset probes are recorded in `grammar_diff_client_server.json`; they falsify copying some client count slots but do not assign server semantics.
- A: client count `signed i8 at row+24`, item 5 B; server unknown. Row-0 same-slot probe at +24: signed -90 vs client count 3.
- B: client count `signed i32le after A items`, item 28 B; server unknown. Row-0 same-slot probe at +40: signed 2 vs client count 0.
- C: client count `signed i32le after B items`, item 28 B; server unknown. Row-0 same-slot probe at +44: signed 0 vs client count 0.
- D: client count `signed i32le after C items`, item 12 B; server unknown. Row-0 same-slot probe at +48: signed 0 vs client count 0.
- Server row prefix/internal lists remain partial: first-row `+32/+36/+40` are small positive i32 probes (28/8/2), but no repeated count-to-span equation or item boundary validates them as counts. A long-string row (ordinal 162) visibly changes these positional bytes; raw example and probes are retained in the profile/rows.

## Column Portrait

- All common start/end offsets profiled for widths 1/2/4/8; signed i8/i16/i32 ranges, -1/all-one sentinels, zero rates, u8 bit masks, date-like packed day/year, cash-range and float32 diagnostics are included.
- Exact reference candidate tests use only the observed nation ordinal set (0..250) and t25 row-ID set; candidates are diagnostic, not field assignments. Other target tables were not read or assigned.
- Candidate counts: bool-like u8 30; packed-day/year 4; nation-ordinal-set 4; nation-ID-set 2; signed cash-range 79.

## Scope and Verification

- t25 is used as client comparison only; t37 `Nagr` remains `client_inline`; no client formula is promoted to server. Schema split has zero explicitly server-only fields and retains unknown/unmarked fields as unknown.
- Evidence: L1 data recomputation and closure; L2 row identity set comparison; L3=0; L4=0.
- Run: `py -V:3.12 -I -B scripts/t46_nation_server10.py --help`; `... --selftest`; `py -V:3.12 -I -B scratch/t46/out/verify.py`; `py -V:3.12 -I -B scripts/t01_anchors.py`.
