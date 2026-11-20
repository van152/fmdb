# t77 verify_log — build / verify / regression evidence

Generated 2026-11-21. All commands run as `py -V:3.12 -I -B` from `D:\tmp2b\fm24-db`.
Raw outputs: `selftest_raw.txt`, `verify_raw.txt` (this directory).

## 1. Selftest

```
py -V:3.12 -I -B scripts/t77_schema_v11.py --selftest
```

7/7 checks passed, exit 0. Covers: SHA-256 empty vector, canonical claim digest is
key-order stable and type-sensitive, JSON serialiser round-trips, guard id range is
E111–E120, the pinned ledger table covers the guard set, the accepted-artifact pin
table is non-trivial (57 files).

## 2. Build

```
py -V:3.12 -I -B scripts/t77_schema_v11.py --build
```

| Output | Bytes | Note |
|---|---:|---|
| `reports/club_nation_subtable_schema.json` | 29,884,088 | v11, 36 root keys |
| `reports/club_nation_subtable_schema.md` | 87,373 | 77,028 B v10 prefix + t77 appendix |
| `reports/other_tables_schema.json` | 286,605 | 13 non-main tables |
| `reports/xml_denominator_coverage.json` | 297,905 | 1,034 occurrences |
| `scratch/t77/out/v11_diff_summary.json` | 7,559 | per-section before/after |

v10 baseline before the fold: 29,511,808 B JSON / 77,028 B MD, SHA-256
`7c351608…` / `b9ba0bb3…`. Net JSON growth +372,280 B (+1.26%) for 10 new sections
and two split-file pointers — the byte-preserved v10 sections account for the rest.

## 3. Verify (63/63, exit 0)

Five groups, all re-derived from disk (nothing is trusted from the build run):

**Group A — baseline and accepted inputs (2).** v10 baseline identity and SHA-256
pin; 57 accepted artifacts re-hashed with 0 drift (t71/t72/t73/t74/t75/t76a/t76c/t78/t79).

**Group B — ledger guards (3).** E111–E120 entries found; kinds are 9 acceptance +
1 `probe_negative` (E119); levels are E111 L3 / E112 L2 / E113 L2 / E114 L3 /
E115 L2 / E116 L1 / E117 L3 / E118 L2 / E119 L2 / E120 L2.

**Group C — section counts vs ledger claims (20).**

| E | Check | Result |
|---|---|---|
| E111 | promotes 24 records = 22 cnst + `Cebd` + `Cyfn` | 24 / 22 / `['Cebd','Cyfn']` |
| E111 | dual-archive row frame closes | client 13,053,908 / server 35,009,248 |
| E111 | row count identical both archives | 84,259 |
| E112 | slot inventory club 34 / comp 84 / nation 40 | match |
| E112 | unnamed 20 / 36 / 24 | match |
| E112 | 10 escalations handed to t75 | `slot_2,3,4,11,12,13,23,24,25,26` |
| E113 | 8/8 archives closed | 8 |
| E113 | 10 distinct (table, field, offset) triples | 10 (14 archive records, claim states 17) |
| E113 | frozen anchors 14 / 0 conflicts | match |
| E113 | alias-group negative preserved | `header_origin_data_unique` all False |
| E114 | 10 grammars / 8 closed / 2 held_no_items | match, held = `slot_2, slot_3` |
| E114 | 99 slots adjudicated / 0 new named L3 | match |
| E114 | held split nation 34 / club 25 / comp 40 | match |
| E114 | t71 4CC excluded, not double-counted | 24 |
| E115 | 9 tables / 17 closed archives / 0 escalations | match |
| E115 | team(24) client entry documented absent | present, reason recorded |
| E117 | stadium 41 / team 11 / extra_24 3 / club 6 | match |
| E120 | stadium 12 client / 47 server, 0 uncovered bytes | match |
| E120 | stadium verify 49 checks / 0 failed | match |
| E118 | 4 tables × 2 archives closed, slots 10/25/11/9 | match |
| E116 | denominator 1,034 / carried 110 / ratio 10.6% | match |
| E116 | entity split 433 / 346 / 255 | match |
| E116 | buckets 99/11/0/24/59/277/564 | sums to 1,034 |

**Group D — published files (24).** `schema_version` 11, `generated_by` t77, all 10
new sections present; **22 v10 root sections byte-identical** (only the four mutable
roots — `schema_version`, `generated_by`, `coverage`, `incremental_provenance` —
differ); root keys are exactly v10 ∪ 10 new; existing coverage numbers untouched
except `club_main_row_L3` 21→43; L4=0; both split files exist and their on-disk
SHA-256 match the pointers in `pointer_artifacts`; the denominator file carries all
1,034 occurrences and its buckets sum to 1,034; the Markdown keeps the 77,028 B v10
bytes as a strict prefix and the appendix header is present.

**Group E — provenance (5).** 26 prior v10 ledger rows preserved verbatim; E111–E120
appended; the t70 ledger snapshot kept intact; the t77 snapshot records the guard set;
E121 declared out of scope (t87).

## 4. Regressions

```
py -V:3.12 -I -B scripts/t01_anchors.py            -> 7/7 checks passed, exit 0
py -V:3.12 -I scripts/baseline_coverage.py --check -> CHECK OK, exit 0
```

Frozen aggregates unchanged: splitting the denominator into its own report file does
not touch the 2026-11-18 snapshot numbers that `baseline_coverage.py --check` pins.
The club main-row L3 rise (21→43) is recorded in `coverage` and in `docs/BASELINE.md`,
not in the frozen snapshot.

## 5. Honest negatives carried into v11

- E119 is `probe_negative`: the t80 enum-supplement premise was refuted (snapshot and
  master enumerations are 100% identical), the lane was closed. It is recorded as a
  negative probe, **not** as an acceptance.
- t76b (award / language / media) hit three walls with zero delivery and was dropped;
  those three tables exist in `other_tables_schema.json` with
  `slots_status: pending:t76b(由 t83 接收)` and carry t74 row frames only.
- E113's alias-group negative stands verbatim: `header_origin_data_unique` is False for
  every fixed-stride simple table, so the data side cannot determine header origin.
- E113 claim accounting: the ledger says 17 L2 slots but the artifacts enumerate 10
  distinct (table, field, offset) triples over 14 graded archive records. Both numbers
  are published; the difference is recorded as an open accounting note, not smoothed.
- E114 delivered **zero** new named L3 across 99 adjudicated slots — a negative result
  kept as such.
- E112 is a partial delivery: the fingerprint list does not claim slot closure.
- E115 records team(24)'s client entry as genuinely absent per t66, not as unmapped.
- L4 = 0 everywhere: no game, editor or IDA was started for this fold, and no `.dat`
  payload was decoded.
