# t127 / t127b — FM24 Playing History (3-file) closure + star career histories

All numbers below are produced by `scripts/t127_pl_hist.py`, which decompresses `scratch/data/pl_hist_{index,id,dt}.dat` in memory (read-only) and re-verifies every container, every index entry and every row chain on each run.

## 1. Container framing (all three files)

| File | On disk | Header (8 B) | Payload | Compression | Decompressed | Records | Stride |
|---|---:|---|---:|---|---:|---:|---:|
| `pl_hist_index.dat` | 3,081,975 | `03 01 74 61 64 2e f1 0d` | 3,081,967 | zstd, 1 frame | 4,124,652 | 515,581 | 8 |
| `pl_hist_id.dat` | 4,124,656 | `03 01 74 61 64 2e 01 00` | 4,124,648 | none (raw u32 pairs) | 4,124,648 | 515,581 | 8 |
| `pl_hist_dt.dat` | 56,996,116 | `03 01 74 61 64 63 03 00` | 56,996,108 | zstd × 48,510 chunk frames (4,096 B each) + 1 skippable chunk-table frame | 198,695,332 | 4,515,803 | 44 |

All three files share bytes 0..4 = `03 01 74 61 64` (u16 version 0x0103 + ASCII `tad`). Byte 5 is a per-file variant byte (`0x2e '.'` index/id, `0x63 'c'` dt) and bytes 6..7 a per-file u16 tag (`0x0df1` / `0x0001` / `0x0003`), so nothing past byte 4 is a shared stamp.

**dt chunk framing (self-describing):** the dt payload is 48,510 zstd chunk frames (4,096 B decompressed each, last 2,468 B) followed by one **skippable frame** (`0x184D2A5E`) holding a chunk table: 48,510 × 12 B records of `u32 compressed_size, u32 decompressed_size, u32 opaque checksum`. The table's compressed sizes match **48,510/48,510** and decompressed sizes **48,510/48,510** of the frames actually inflate-scanned, its entry count equals the data-frame count (**True**), and 9 tail bytes (`7e bd 00 00 80 b1 ea 92 8f`) close the frame → the dt container accounts for every byte, no hidden payload.

## 2. Linkage + closure across the ENTIRE dataset

- players indexed (`index` records) = **515,581**, `id` records = **515,581** (1:1: True)
- uids strictly increasing: **True**, range 3 … 2,002,040,995; ordinal column == position in all rows: **True**
- all offsets in bounds and first ≤ last: **True**; misaligned offsets (any %44 ≠ 0): **0**
- block contiguity violations (`first[i+1] == last[i]+44`): **0**; bytes after last block: **0**
- **closure diff = 0** (Σ per-player bytes = 198,695,332 = dt size 198,695,332)
- row-chain: 4,000,222 valid `next_row` links, 515,581 terminators (exactly one per player, all at block ends: **True**), malformed links **0** → chain closed: **True**
- career rows: **4,515,803** × 44 B (min 1, max 57, mean 8.759 per player)

## 3. Row layout (44 B, little endian)

| Off | W | Field | Role | Meaning |
|---:|---:|---|---|---|
| 0 | 2 | `year_from` | verified | period start year (u16) |
| 2 | 2 | `year_to` | verified | period end year (u16); == year_from for single-season rows |
| 4 | 1 | `flags` | candidate | bitfield: 0x01=partial/supplementary spell (loan, mid-season move), 0x02=youth/academy row; bits >=0x04 rare (~940 rows), unresolved |
| 5 | 1 | `apps` | verified | appearances over the period; 255 = null |
| 6 | 1 | `goals` | verified | goals over the period; 255 = null |
| 7 | 4 | `fee_gbp` | verified | transfer fee / value in GBP at period end; 0xFFFFFFFF = null (0xFFFFFFFE/-2, 0xFFFFFFFD/-3 also seen), 0 = explicit zero |
| 11 | 4 | `club_id` | verified | club (or synthetic non-club team) id; 0xFFFFFFFF = null |
| 15 | 4 | `club_id_dup` | duplicate | byte-identical copy of club_id in 100% of rows |
| 19 | 4 | `comp_id` | verified | competition id; 0xFFFFFFFF = null |
| 23 | 4 | `comp_id_dup` | duplicate | byte-identical copy of comp_id in 100% of rows |
| 27 | 1 | `seq_in_year` | candidate | 1..k when several rows share one start year, else 0 |
| 28 | 2 | `join_day` | verified | day-of-year (1..366); 1 with year 1900 = empty |
| 30 | 2 | `join_year` | verified | year; 1900 = empty |
| 32 | 2 | `leave_day` | verified | day-of-year (1..366); 1 with year 1900 = empty |
| 34 | 2 | `leave_year` | verified | year; 1900 = empty |
| 36 | 2 | `tail_a` | unknown | 4-byte tail word; (1,1900) sentinel in 99.2% of rows |
| 38 | 2 | `tail_b` | unknown | see tail_a |
| 40 | 4 | `next_row` | verified | absolute offset of next row in the same career chain; 0xFFFFFFFF terminates |

**Verified semantics** (each one corroborated by independent real-world facts, not just
self-consistency):

- `year_from`/`year_to` — the period covered by the row. Granularity is per season for tracked
  players (Kane: 18 rows for 2009→2023) and per multi-season spell for coarser records
  (e.g. 2008→2010 with matching `joined` = 2008-07-01, `left` = 2010-07-01).
- `apps`/`goals` — u8, 255 = null (28.9% of rows). Live maximum is 75, i.e. season-sized totals.
- `join_*`/`leave_*` — **day-of-year + year**; (1, 1900) = empty. Corroborations:
  Kane 2010-11 Leyton Orient (7, 2011) = 2011-01-07; Millwall (1, 2012) = 2012-01-01;
  Norwich (244, 2012) = 2012-08-31; Leicester (52, 2013) = 2013-02-21;
  Messi's Barcelona deal ends (181, 2021) = 2021-06-30 and PSG starts (222, 2021) = 2021-08-10;
  Ronaldo's Juventus row ends (243, 2021) = 2021-08-31, Man Utd row starts the same day.
- `fee_gbp` — £ amount attached to the end of the period, corroborated by five famous transfers:
  CR7 2002-03 Sporting → **12,240,000** (real £12.24 m), 2008-09 Man Utd → **80,000,000**
  (real £80 m), 2017-18 Real Madrid → **92,884,600**; 2021 Juventus → **12,850,000**;
  De Bruyne Genk → Chelsea **6,484,148** (Jan-2012) and Wolfsburg → Man City **54,406,964**
  (Aug-2015). 0xFFFFFFFF = null (3.63 M rows), 0 = explicit zero.
- `club_id`, `comp_id` — team / competition ids; `club_id_dup` and `comp_id_dup` are
  **byte-identical in 100% of 4,515,803 rows** (redundant serialized slots, not a second value).
- `flags` — bitfield. `0x01` marks a supplementary spell (loan or mid-season move: all four of
  Kane's loan rows, Mbappé's 2017-18 PSG half-season, De Bruyne's loan-back to Genk);
  `0x02` marks youth/academy rows (Kane 2009, Messi 2002, CR7 2000-01, De Bruyne 2005-07,
  Mbappé 2014: all 0 apps at a boyhood club). Bits ≥ 0x04 exist in only ~940 rows
  (0.02%) and stay **unresolved**.
- `seq_in_year` — 1..k when several rows share the same start year, else 0 (candidate).
- `tail_a`/`tail_b` — 4-byte tail word, `(1, 1900)` in 99.16% of rows; the remaining 38,096 rows
  hold values that are not valid dates. **Unknown / reserved.**

## 4. Harry Kane — career (uid 28049320)

| From | To | Club | Comp | Apps | Goals | Flags | Joined | Left | Fee £ |
|---:|---:|---|---|---:|---:|---:|---|---|---:|
| 2009 | 2009 | Tottenham | Premier League | 0 | 0 | 2 | 2009-07-01 | — | — |
| 2010 | 2010 | Tottenham | Premier League | 0 | 0 | 0 | — | — | — |
| 2010 | 2011 | Leyton Orient | League One | 18 | 5 | 1 | 2011-01-07 | 2011-05-31 | — |
| 2011 | 2011 | Tottenham | Premier League | 0 | 0 | 0 | — | — | — |
| 2011 | 2012 | Millwall | Championship | 22 | 7 | 1 | 2012-01-01 | 2012-05-10 | — |
| 2012 | 2012 | Tottenham | Premier League | 1 | 0 | 0 | — | — | — |
| 2012 | 2013 | Norwich | Premier League | 3 | 0 | 1 | 2012-08-31 | 2013-02-01 | — |
| 2012 | 2013 | Leicester | Championship | 13 | 2 | 1 | 2013-02-21 | 2013-05-31 | — |
| 2013 | 2013 | Tottenham | Premier League | 10 | 3 | 0 | — | — | — |
| 2014 | 2014 | Tottenham | Premier League | 34 | 21 | 0 | — | — | — |
| 2015 | 2015 | Tottenham | Premier League | 38 | 25 | 0 | — | — | — |
| 2016 | 2016 | Tottenham | Premier League | 30 | 29 | 0 | — | — | — |
| 2017 | 2017 | Tottenham | Premier League | 37 | 30 | 0 | — | — | — |
| 2018 | 2018 | Tottenham | Premier League | 28 | 17 | 0 | — | — | — |
| 2019 | 2019 | Tottenham | Premier League | 29 | 18 | 0 | — | — | — |
| 2020 | 2020 | Tottenham | Premier League | 35 | 23 | 0 | — | — | — |
| 2021 | 2021 | Tottenham | Premier League | 37 | 17 | 0 | — | — | — |
| 2022 | 2023 | Tottenham | Premier League | 38 | 30 | 0 | — | 2023-08-12 | 85,746,464 |


## 5. Lionel Messi — career (uid 7458500)

| From | To | Club | Comp | Apps | Goals | Flags | Joined | Left | Fee £ |
|---:|---:|---|---|---:|---:|---:|---|---|---:|
| 2002 | 2002 | Barcelona | La Liga | 0 | 0 | 2 | 2000-12-14 | — | — |
| 2003 | 2003 | Barcelona C | #67023614 | 10 | 5 | 0 | — | — | — |
| 2003 | 2003 | Barcelona B | #71 | 5 | 0 | 0 | — | — | — |
| 2004 | 2004 | Barcelona B | #71 | 17 | 6 | 0 | — | — | — |
| 2004 | 2004 | Barcelona | La Liga | 7 | 1 | 0 | — | — | — |
| 2005 | 2005 | Barcelona | La Liga | 17 | 6 | 0 | — | — | — |
| 2006 | 2006 | Barcelona | La Liga | 26 | 14 | 0 | — | — | — |
| 2007 | 2007 | Barcelona | La Liga | 28 | 10 | 0 | — | — | — |
| 2008 | 2008 | Barcelona | La Liga | 31 | 23 | 0 | — | — | — |
| 2009 | 2009 | Barcelona | La Liga | 35 | 34 | 0 | — | — | — |
| 2010 | 2010 | Barcelona | La Liga | 33 | 31 | 0 | — | — | — |
| 2011 | 2011 | Barcelona | La Liga | 37 | 50 | 0 | — | — | — |
| 2012 | 2012 | Barcelona | La Liga | 32 | 46 | 0 | — | — | — |
| 2013 | 2013 | Barcelona | La Liga | 31 | 28 | 0 | — | — | — |
| 2014 | 2014 | Barcelona | La Liga | 38 | 43 | 0 | — | — | — |
| 2015 | 2015 | Barcelona | La Liga | 33 | 26 | 0 | — | — | — |
| 2016 | 2016 | Barcelona | La Liga | 34 | 37 | 0 | — | — | — |
| 2017 | 2017 | Barcelona | La Liga | 36 | 34 | 0 | — | — | — |
| 2018 | 2018 | Barcelona | La Liga | 34 | 36 | 0 | — | — | — |
| 2019 | 2019 | Barcelona | La Liga | 33 | 25 | 0 | — | — | — |
| 2020 | 2021 | Barcelona | La Liga | 35 | 30 | 0 | — | 2021-06-30 | 0 |
| 2021 | 2021 | Paris SG | Ligue 1 | 26 | 6 | 0 | 2021-08-10 | — | — |
| 2022 | 2023 | Paris SG | Ligue 1 | 32 | 16 | 0 | — | 2023-06-30 | 0 |
| 2023 | 2023 | Inter Miami | #40 | 6 | 1 | 0 | 2023-07-15 | — | — |


## 6. Cristiano Ronaldo — career (uid 735216)

| From | To | Club | Comp | Apps | Goals | Flags | Joined | Left | Fee £ |
|---:|---:|---|---|---:|---:|---:|---|---|---:|
| 2000 | 2000 | Sporting CP | Liga Portugal | 0 | 0 | 2 | 2000-07-01 | — | — |
| 2001 | 2001 | Sporting CP | Liga Portugal | 0 | 0 | 2 | — | — | — |
| 2002 | 2002 | Sporting CP B | #55020402 | 2 | 0 | 0 | — | — | — |
| 2002 | 2003 | Sporting CP | Liga Portugal | 25 | 3 | 0 | — | 2003-08-12 | 12,240,000 |
| 2003 | 2003 | Man UFC | Premier League | 29 | 4 | 0 | 2003-08-12 | — | — |
| 2004 | 2004 | Man UFC | Premier League | 33 | 5 | 0 | — | — | — |
| 2005 | 2005 | Man UFC | Premier League | 33 | 9 | 0 | — | — | — |
| 2006 | 2006 | Man UFC | Premier League | 34 | 17 | 0 | — | — | — |
| 2007 | 2007 | Man UFC | Premier League | 34 | 31 | 0 | — | — | — |
| 2008 | 2009 | Man UFC | Premier League | 33 | 18 | 0 | — | 2009-07-01 | 80,000,000 |
| 2009 | 2009 | R. Madrid | La Liga | 29 | 26 | 0 | 2009-07-01 | — | — |
| 2010 | 2010 | R. Madrid | La Liga | 34 | 40 | 0 | — | — | — |
| 2011 | 2011 | R. Madrid | La Liga | 38 | 46 | 0 | — | — | — |
| 2012 | 2012 | R. Madrid | La Liga | 34 | 34 | 0 | — | — | — |
| 2013 | 2013 | R. Madrid | La Liga | 30 | 31 | 0 | — | — | — |
| 2014 | 2014 | R. Madrid | La Liga | 35 | 48 | 0 | — | — | — |
| 2015 | 2015 | R. Madrid | La Liga | 36 | 35 | 0 | — | — | — |
| 2016 | 2016 | R. Madrid | La Liga | 29 | 25 | 0 | — | — | — |
| 2017 | 2018 | R. Madrid | La Liga | 27 | 26 | 0 | — | 2018-07-01 | 92,884,600 |
| 2018 | 2018 | Juventus | Serie A | 31 | 21 | 0 | 2018-07-01 | — | — |
| 2019 | 2019 | Juventus | Serie A | 33 | 31 | 0 | — | — | — |
| 2020 | 2020 | Juventus | Serie A | 33 | 29 | 0 | — | — | — |
| 2021 | 2021 | Juventus | Serie A | 1 | 0 | 0 | — | 2021-08-31 | 12,850,000 |
| 2021 | 2021 | Man UFC | Premier League | 30 | 18 | 0 | 2021-08-31 | — | — |
| 2022 | 2022 | Man UFC | Premier League | 10 | 1 | 0 | — | 2022-11-22 | 0 |
| 2022 | 2022 | Al-Nassr (KSA) | #7920263 | 16 | 14 | 0 | 2022-12-31 | — | — |


## 7. Kevin De Bruyne (uid 18004457) and Kylian Mbappe (uid 85139014)

**Kevin De Bruyne**

| From | To | Club | Comp | Apps | Goals | Flags | Joined | Left | Fee £ |
|---:|---:|---|---|---:|---:|---:|---|---|---:|
| 2005 | 2006 | AA Gent | #1 | 0 | 0 | 2 | 1999-07-01 | 2006-07-01 | 0 |
| 2006 | 2006 | KRC Genk | #1 | 0 | 0 | 2 | 2006-07-01 | — | — |
| 2007 | 2007 | KRC Genk | #1 | 0 | 0 | 2 | — | — | — |
| 2008 | 2008 | KRC Genk | #1 | 2 | 0 | 0 | — | — | — |
| 2009 | 2009 | KRC Genk | #1 | 35 | 3 | 0 | — | — | — |
| 2010 | 2010 | KRC Genk | #1 | 32 | 5 | 0 | — | — | — |
| 2011 | 2012 | KRC Genk | #1 | 15 | 6 | 0 | — | 2012-01-31 | 6,484,148 |
| 2011 | 2011 | Chelsea | Premier League | 0 | 0 | 0 | 2012-01-31 | — | — |
| 2011 | 2012 | KRC Genk | #1 | 13 | 2 | 1 | 2012-02-01 | 2012-06-30 | 0 |
| 2012 | 2013 | SV Werder | Bundesliga | 33 | 10 | 1 | 2012-08-02 | 2013-06-30 | 450,000 |
| 2013 | 2014 | Chelsea | Premier League | 3 | 0 | 0 | — | 2014-01-18 | 17,726,782 |
| 2013 | 2013 | VfL Wolfsburg | Bundesliga | 16 | 3 | 0 | 2014-01-18 | — | — |
| 2014 | 2014 | VfL Wolfsburg | Bundesliga | 34 | 10 | 0 | — | — | — |
| 2015 | 2015 | VfL Wolfsburg | Bundesliga | 2 | 0 | 0 | — | 2015-08-30 | 54,406,964 |
| 2015 | 2015 | Man City | Premier League | 25 | 7 | 0 | 2015-08-30 | — | — |
| 2016 | 2016 | Man City | Premier League | 36 | 6 | 0 | — | — | — |
| 2017 | 2017 | Man City | Premier League | 37 | 8 | 0 | — | — | — |
| 2018 | 2018 | Man City | Premier League | 19 | 2 | 0 | — | — | — |
| 2019 | 2019 | Man City | Premier League | 35 | 13 | 0 | — | — | — |
| 2020 | 2020 | Man City | Premier League | 25 | 6 | 0 | — | — | — |
| 2021 | 2021 | Man City | Premier League | 30 | 15 | 0 | — | — | — |
| 2022 | 2022 | Man City | Premier League | 32 | 7 | 0 | — | — | — |


**Kylian Mbappe**

| From | To | Club | Comp | Apps | Goals | Flags | Joined | Left | Fee £ |
|---:|---:|---|---|---:|---:|---:|---|---|---:|
| 2014 | 2014 | AS Monaco | Ligue 1 | 0 | 0 | 2 | 2013-07-03 | — | — |
| 2015 | 2015 | AS Monaco | Ligue 1 | 11 | 1 | 0 | — | — | — |
| 2016 | 2016 | AS Monaco | Ligue 1 | 29 | 15 | 0 | — | — | — |
| 2017 | 2018 | AS Monaco | Ligue 1 | 1 | 0 | 0 | — | 2018-07-01 | 159,230,736 |
| 2017 | 2018 | Paris SG | Ligue 1 | 27 | 13 | 1 | 2017-08-31 | 2018-06-30 | — |
| 2018 | 2018 | Paris SG | Ligue 1 | 29 | 33 | 0 | 2018-07-01 | — | — |
| 2019 | 2019 | Paris SG | Ligue 1 | 20 | 18 | 0 | — | — | — |
| 2020 | 2020 | Paris SG | Ligue 1 | 31 | 27 | 0 | — | — | — |
| 2021 | 2021 | Paris SG | Ligue 1 | 35 | 28 | 0 | — | — | — |
| 2022 | 2022 | Paris SG | Ligue 1 | 34 | 29 | 0 | — | — | — |


## 8. Known anomalies, limits and open questions

| Item | Extent | Status |
|---|---|---|
| `apps`/`goals` = 255 (null) | 1306191 / 4515803 rows | verified sentinel, excluded from maxima |
| `fee_gbp` = 0xFFFFFFFF / 0xFFFFFFFE / 0xFFFFFFFD | 3631124 / 24518 / 1113 rows | sentinels; only 35989 rows carry a real amount |
| `year_to < year_from` | 11525 rows (0.26%) | dirty legacy data, left as stored (mostly pre-1995 records) |
| `year_to > year_from + 1` | 160274 rows | genuine multi-season spells, dates in `joined`/`left` agree |
| `goals > apps` (both live) | 9497 rows | internally inconsistent source rows, not a decode error |
| `flags` >= 0x04 | 962 rows | **unresolved** — club ids look synthetic, comp usually null |
| `tail_a`/`tail_b` | 38096 rows non-sentinel | **unknown** — values are not valid dates |
| `club_id_dup`/`comp_id_dup` | identical in 100% of rows | redundant serialized slots (no second meaning found) |
| competition names | 8 hints only | no competition name table decoded; ids beyond the hints stay numeric |

## 9. Correction relative to the earlier exploratory dump

The previous run's `scratch/t127/out/_stars.json` reported Kane 17, Messi 23 and Ronaldo 25 rows
because it read the `id` pair as a half-open `[start, end)` range. The `id` pair is in fact
**`[first_row_offset, last_row_offset]` inclusive** (so `nrows = (end-start)//44 + 1`). Proof, both
independent of any assumption:

1. block contiguity — `first[i+1] == last[i] + 44` for all 515,580 consecutive pairs, and
   `last[-1] + 44 == len(dt)` exactly (closure diff 0), which only works if `last` *is* a row offset;
2. the extra row is real data, not padding: Kane's extra row is 2022-23 Tottenham, 38 apps / 30 goals,
   and its `next_row` is the chain terminator 0xFFFFFFFF.

Corrected counts: Kane **18**, Messi **24**, Ronaldo **26**, De Bruyne **22**, Mbappe **10**.

## 10. Field statistics (whole dataset)

```
rows                         4515803
flags_histogram              {0: 3580085, 1: 254539, 2: 664618, 3: 15599, 4: 729, 5: 3, 6: 20, 8: 139, 9: 2, 10: 1, 12: 19, 16: 27, 20: 5, 24: 7, 28: 3, 32: 6, 34: 1}
apps_null                    1306191
goals_null                   1307490
apps_max_live                75
goals_max_live               75
goals_gt_apps_live           9497
fee_null_FFFFFFFF            3631124
fee_FE                       24518
fee_FD                       1113
fee_zero                     823059
fee_real_rows                35989
fee_real_min                 1
fee_real_max                 4294967291
year_from_min                1954
year_from_max                2025
year_span_hist_-5..10        {-5: 1174, -4: 634, -3: 1065, -2: 2195, -1: 6457, 0: 3235206, 1: 1108798, 2: 124444, 3: 18816, 4: 7419, 5: 3713, 6: 2066, 7: 1218, 8: 787, 9: 530, 10: 1281}
join_null                    2201627
leave_null                   2699923
join_day_out_of_range        0
leave_day_out_of_range       0
tail_sentinel_rows           4477707
tail_other_rows              38096
club_null                    16057
comp_null                    869507
club_dup_mismatch            0
comp_dup_mismatch            0
```

## 11. Reproduce

```
py -V:3.12 -B scripts/t127_pl_hist.py --selftest
py -V:3.12 -B scripts/t127_pl_hist.py            # rebuild all deliverables
py -V:3.12 -B scripts/t127_pl_hist.py --uid 28049320
```
