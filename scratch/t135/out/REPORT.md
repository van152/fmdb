# t135 — Complete 54-Attribute FM24 Player Cards for World Superstars (straight from the 400 MB `people_db.dat`)

**21 superstars decoded** · **54/54 `PDxx` attributes each** · CA cross-check **21/21** (`100%`) · PA cross-check **21/21** (`100%`) · all attributes in `0..20`: **21/21** · record identity verified: **21/21** · whole run **6.86 s**.

## How it works (no 658k-row walk, no 400 MB dumped to disk)

1. **Targets.** `basic_people_db.dat` (zstd; `raw[8:]` → 54,060,043 B; 658,011 rows; histogram `{1: 166064, 2: 476158, 4: 9839, 3: 4757, 5: 1193}`; closure diff `0`) is walked once to take the **Top-20 players by CA** (ptype 2/3) plus the guaranteed anchors (Kane `28049320`, Messi `7458500`, Ronaldo `735216`), which de-duplicates to **21 unique superstars** (Messi and Kane are anchors *and* in the Top-20; Ronaldo is the extra).
2. **Locate.** `people_db.dat` is zstd-decompressed **in memory** to `400,443,970 B`. Every target's 5-byte record header `[u32 ordinal][u8 ptype]` is found with a single vectorised pass over the payload (typically 1–3 candidate hits out of 400 MB).
3. **Verify twice.** Each candidate is fed to the real `t120` Unicorn engine: `sub_1410992C0(ptype)` factory + polymorphic vtable slot[19] deserializer must return `ok` **and** the record's trailing 12-byte identity `[u32 ordinal][u32 dbid][u32 uid]` must equal the target `(ordinal, uid)` with `dbid == uid`. Nothing is accepted on a byte-pattern match alone.
4. **Decode.** Off the verified wire buffer: `body[0:10]` = `PHRP/PCRP/PWRP/PCAB/PPAB`, `body[29:44]` = 15 position bytes, `body[44:98]` = **54 `PDxx` attributes** (t126 54/54 GET==SET map), `body[126:130]` = `weight`, `height`, and the three name ids resolve through `name_table_extra_{0,1,2}` (UTF-8).

Timing: basic scan `1.53s` · decompress+emulator `1.68s` · header index `1.78s` · 21 cards `0.21s` · offset probe `1.66s`.

## Showcase — decoded superstars

| Name | UID | CA / PA | Height / Weight | Pace | Acc | Fin | Drib | Pass | Vision | Comp | Det | Tack | Refl |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Kevin De Bruyne** | 18004457 | 190 / 190 | 181 cm / 68 kg | 14 | 16 | 16 | 16 | 18 | 20 | 14 | 17 | 9 | 0 |
| **Kylian Mbappé** | 85139014 | 188 / 197 | 178 cm / 73 kg | 20 | 20 | 17 | 18 | 15 | 15 | 17 | 18 | 4 | 0 |
| **Erling Haaland** | 29179241 | 188 / 195 | 195 cm / 94 kg | 19 | 17 | 18 | 14 | 13 | 14 | 18 | 20 | 7 | 0 |
| **Lionel Messi** | 7458500 | 185 / 200 | 169 cm / 67 kg | 15 | 16 | 17 | 20 | 19 | 20 | 16 | 20 | 7 | 0 |
| **Vinícius Júnior** | 19302146 | 184 / 190 | 176 cm / 73 kg | 18 | 19 | 16 | 19 | 15 | 14 | 15 | 20 | 6 | 0 |
| **Harry Kane** | 28049320 | 184 / 185 | 188 cm / 86 kg | 14 | 12 | 19 | 14 | 18 | 19 | 18 | 19 | 9 | 0 |
| **Mohamed Salah** | 98028755 | 181 / 187 | 175 cm / 72 kg | 17 | 18 | 16 | 16 | 15 | 17 | 15 | 18 | 6 | 0 |
| **Thibaut Courtois** | 18026122 | 181 / 181 | 200 cm / 96 kg | 11 | 12 | 0 | 10 | 13 | 9 | 12 | 16 | 0 | 19 |
| **Ederson** | 55057659 | 180 / 180 | 188 cm / 86 kg | 13 | 14 | 0 | 11 | 18 | 17 | 20 | 16 | 0 | 15 |
| **Rodri** | 67217524 | 180 / 180 | 191 cm / 75 kg | 13 | 14 | 13 | 13 | 16 | 16 | 20 | 13 | 17 | 0 |
| **Robert Lewandowski** | 719601 | 178 / 190 | 185 cm / 81 kg | 14 | 13 | 18 | 13 | 13 | 14 | 17 | 18 | 7 | 0 |
| **Virgil van Dijk** | 37024025 | 178 / 183 | 193 cm / 92 kg | 15 | 15 | 8 | 13 | 16 | 14 | 17 | 16 | 17 | 0 |
| **Bernardo Silva** | 55041632 | 178 / 180 | 173 cm / 64 kg | 14 | 15 | 15 | 17 | 17 | 17 | 16 | 16 | 8 | 0 |
| **Jude Bellingham** | 29232937 | 177 / 188 | 186 cm / 75 kg | 14 | 15 | 16 | 17 | 17 | 16 | 17 | 20 | 15 | 0 |
| **Declan Rice** | 28106491 | 176 / 182 | 185 cm / 80 kg | 14 | 13 | 9 | 14 | 15 | 14 | 17 | 17 | 17 | 0 |
| **Alisson** | 19058734 | 176 / 180 | 191 cm / 91 kg | 12 | 13 | 0 | 10 | 14 | 11 | 15 | 19 | 0 | 17 |
| **Neymar** | 19024412 | 175 / 190 | 175 cm / 68 kg | 15 | 15 | 16 | 20 | 17 | 17 | 17 | 16 | 5 | 0 |
| **Marc-André ter Stegen** | 35017428 | 175 / 183 | 187 cm / 85 kg | 11 | 14 | 0 | 0 | 17 | 9 | 18 | 18 | 0 | 18 |
| **Bukayo Saka** | 28122642 | 174 / 186 | 178 cm / 71 kg* | 15 | 17 | 14 | 17 | 13 | 15 | 14 | 17 | 10 | 0 |
| **Joshua Kimmich** | 92039023 | 174 / 183 | 177 cm / 75 kg | 12 | 12 | 10 | 12 | 18 | 18 | 17 | 20 | 13 | 0 |
| **Cristiano Ronaldo** | 735216 | 160 / 196 | 187 cm / 84 kg | 13 | 12 | 18 | 13 | 13 | 13 | 15 | 20 | 5 | 0 |

`*` = physique value auto-derived by the game (stored negative in the DB; magnitude shown).

### Verification ledger

| Name | `people_db` offset | body len | ord | ptype | PCAB/PPAB | basic @+48/+50 | basic @+44/+46 (spec) | 69B block @ wire | obj_off | `dbid==uid` | 54/54 in 0..20 |
|---|---:|---:|---:|---:|---|---|---|---|---:|---|---|
| Kevin De Bruyne | `289,858,940` | 1129 | 108093 | 2 | 190/190 | 190/190 ✅ | 190/190 = | 29 | `-0x70` | ✅ | ✅ |
| Kylian Mbappé | `236,690,058` | 1153 | 371307 | 2 | 188/197 | 188/197 ✅ | 188/188 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Erling Haaland | `154,018,301` | 1219 | 174549 | 2 | 188/195 | 188/195 ✅ | 188/188 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Lionel Messi | `38,606,581` | 1528 | 52631 | 2 | 185/200 | 185/200 ✅ | 200/200 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Vinícius Júnior | `23,092,738` | 1309 | 119392 | 2 | 184/190 | 184/190 ✅ | 184/174 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Harry Kane | `252,735,069` | 1148 | 166119 | 2 | 184/185 | 184/185 ✅ | 184/185 = | 29 | `-0x70` | ✅ | ✅ |
| Mohamed Salah | `393,628,792` | 1131 | 402583 | 2 | 181/187 | 181/187 ✅ | 184/192 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Thibaut Courtois | `289,860,074` | 1265 | 108672 | 2 | 181/181 | 181/181 ✅ | 181/175 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Ederson | `23,094,052` | 918 | 277376 | 2 | 180/180 | 180/180 ✅ | 176/170 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Rodri | `96,182,290` | 945 | 320375 | 2 | 180/180 | 180/180 ✅ | 180/180 = | 29 | `-0x70` | ✅ | ✅ |
| Robert Lewandowski | `149,097,973` | 1324 | 19028 | 2 | 178/190 | 178/190 ✅ | 178/182 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Virgil van Dijk | `163,924,001` | 925 | 193427 | 2 | 178/183 | 178/183 ✅ | 178/174 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Bernardo Silva | `131,414,392` | 1173 | 277144 | 2 | 178/180 | 178/180 ✅ | 178/178 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Jude Bellingham | `252,736,585` | 1296 | 176870 | 2 | 177/188 | 177/188 ✅ | 177/175 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Declan Rice | `252,737,886` | 911 | 167664 | 2 | 176/182 | 176/182 ✅ | 176/176 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Alisson | `23,094,975` | 1119 | 114305 | 2 | 176/180 | 176/180 ✅ | 176/173 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Neymar | `23,096,099` | 1410 | 113576 | 2 | 175/190 | 175/190 ✅ | 180/186 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Marc-André ter Stegen | `226,033,055` | 1205 | 186065 | 2 | 175/183 | 175/183 ✅ | 175/165 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Bukayo Saka | `252,738,802` | 835 | 168621 | 2 | 174/186 | 174/186 ✅ | 174/174 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Joshua Kimmich | `226,034,265` | 1324 | 388201 | 2 | 174/183 | 174/183 ✅ | 174/174 ≠ | 29 | `-0x70` | ✅ | ✅ |
| Cristiano Ronaldo | `131,426,802` | 1530 | 19300 | 2 | 160/196 | 160/196 ✅ | 160/200 ≠ | 29 | `-0x70` | ✅ | ✅ |

## Full 54-attribute breakdown — Messi, Ronaldo, Kane

### Lionel Messi — UID `7458500` · CA 185 / PA 200 · 169 cm / 67 kg · rep H/C/W = 200/200/200 · `people_db` offset `38,606,581` (body 1528 B)

- **Technical**: Crossing **15** · Dribbling **20** · Finishing **17** · Heading **10** · Long Shots **16** · Marking **4** · Passing **19** · Penalty Taking **17** · Tackling **7** · First Touch **19** · Technique **20** · Corners **15** · Long Throws **4** · Free Kick Taking **18**
- **Mental**: Off The Ball **14** · Vision **20** · Anticipation **16** · Decisions **18** · Positioning **5** · Flair **20** · Teamwork **14** · Work Rate **9** · Leadership **14** · Bravery **10** · Aggression **7** · Determination **20** · Composure **16** · Concentration **13**
- **Physical**: Acceleration **16** · Strength **9** · Stamina **13** · Pace **15** · Jumping Reach **6** · Balance **18** · Agility **15** · Natural Fitness **14**
- **Goalkeeping**: Handling **0** · Aerial Reach **0** · Command of Area **0** · Communication **0** · Kicking **0** · Throwing **0** · One on Ones **0** · Reflexes **0** · Eccentricity **0** · Rushing Out **0** · Tendency to Punch **0**
- **Hidden**: Dirtiness **9** · Consistency **16** · Important Matches **18** · Injury Proneness **6** · Versatility **12**
- **Foot**: Left Foot **20** · Right Foot **12**
- **Positions `0..14`** (raw): `[0, 1, 0, 0, 0, 0, 8, 12, 8, 11, 19, 20, 19, 0, 0]`
- **54-attribute sum**: `596`

### Cristiano Ronaldo — UID `735216` · CA 160 / PA 196 · 187 cm / 84 kg · rep H/C/W = 200/160/160 · `people_db` offset `131,426,802` (body 1530 B)

- **Technical**: Crossing **11** · Dribbling **13** · Finishing **18** · Heading **18** · Long Shots **15** · Marking **3** · Passing **13** · Penalty Taking **20** · Tackling **5** · First Touch **15** · Technique **17** · Corners **10** · Long Throws **5** · Free Kick Taking **13**
- **Mental**: Off The Ball **18** · Vision **13** · Anticipation **17** · Decisions **12** · Positioning **4** · Flair **17** · Teamwork **7** · Work Rate **7** · Leadership **19** · Bravery **13** · Aggression **6** · Determination **20** · Composure **15** · Concentration **10**
- **Physical**: Acceleration **12** · Strength **15** · Stamina **13** · Pace **13** · Jumping Reach **16** · Balance **13** · Agility **11** · Natural Fitness **20**
- **Goalkeeping**: Handling **0** · Aerial Reach **0** · Command of Area **0** · Communication **0** · Kicking **0** · Throwing **0** · One on Ones **0** · Reflexes **0** · Eccentricity **0** · Rushing Out **0** · Tendency to Punch **0**
- **Hidden**: Dirtiness **12** · Consistency **13** · Important Matches **17** · Injury Proneness **6** · Versatility **9**
- **Foot**: Left Foot **15** · Right Foot **20**
- **Positions `0..14`** (raw): `[0, 1, 0, 0, 0, 0, 0, 0, 0, 13, 8, 12, 20, 0, 0]`
- **54-attribute sum**: `559`

### Harry Kane — UID `28049320` · CA 184 / PA 185 · 188 cm / 86 kg · rep H/C/W = 185/184/175 · `people_db` offset `252,735,069` (body 1148 B)

- **Technical**: Crossing **15** · Dribbling **14** · Finishing **19** · Heading **16** · Long Shots **15** · Marking **8** · Passing **18** · Penalty Taking **20** · Tackling **9** · First Touch **15** · Technique **17** · Corners **9** · Long Throws **6** · Free Kick Taking **11**
- **Mental**: Off The Ball **17** · Vision **19** · Anticipation **15** · Decisions **18** · Positioning **8** · Flair **12** · Teamwork **18** · Work Rate **16** · Leadership **16** · Bravery **14** · Aggression **11** · Determination **19** · Composure **18** · Concentration **15**
- **Physical**: Acceleration **12** · Strength **15** · Stamina **16** · Pace **14** · Jumping Reach **15** · Balance **15** · Agility **12** · Natural Fitness **16**
- **Goalkeeping**: Handling **0** · Aerial Reach **0** · Command of Area **0** · Communication **0** · Kicking **0** · Throwing **0** · One on Ones **0** · Reflexes **0** · Eccentricity **0** · Rushing Out **0** · Tendency to Punch **0**
- **Hidden**: Dirtiness **8** · Consistency **17** · Important Matches **14** · Injury Proneness **12** · Versatility **9**
- **Foot**: Left Foot **16** · Right Foot **20**
- **Positions `0..14`** (raw): `[0, 1, 0, 0, 0, 0, 0, 12, 0, 12, 15, 10, 20, 0, 0]`
- **54-attribute sum**: `619`

## Findings & cross-checks

### 1. `basic_people_db.dat` CA/PA offsets — corrected

The task statement names `CA = u16 @ +44` and `PA = u16 @ +46`. Measured against `people_db`'s `PCAB`/`PPAB` on random samples, those are **not** CA/PA — the true fields are `CA = u16 @ +48` and `PA = u16 @ +50` (birth year `u16 @ +52`), for both `ptype == 2` and `ptype == 3`:

| Type | Samples verified | CA offset votes | PA offset votes |
|---:|---:|---|---|
| 2 | 25 | +48 (25/25), +44 (9/25), +46 (9/25) | +50 (25/25), +48 (2/25), +3 (1/25) |
| 3 | 25 | +48 (25/25), +44 (12/25), +46 (12/25) | +50 (25/25), +44 (2/25), +46 (2/25) |

On the 21 superstars the `+48/+50` pair equals `PCAB/PPAB` **21/21** (CA) and **21/21** (PA), while the spec's `+44`/`+46` pair matches only **17/21**. It is a *second* ability pair (a peak/best-career reference), so it equals current ability only for players sitting at their peak — see the ledger: Kane `184/185` (identical), Mbappé `188/188` vs true `188/197`, Haaland `188/188` vs `188/195`, Messi `200/200` vs `185/200`, Ronaldo `160/200` vs `160/196`. That partial coincidence on the three supplied anchors (Kane exact, Messi matching on PA, Ronaldo matching on CA) is the most plausible origin of the `+44`/`+46` offsets quoted in the task.

### 2. `ptype == 3` (`ACTUAL_PLAYER_AND_NON_PLAYER`) — verified, not assumed

- The **wire** layout is *identical* to `ptype == 2`: 21/21 cards show the 69-byte `PLAYER_DATA` block as the `n == 69` read at `wire_pos == 29`, with the header `5h` at `body+0` and physique at `body+126`.
- The **object** offsets differ: `obj_off` `-0x70` for `ptype 2` vs `-0x160` for `ptype 3`. The selftest re-confirms this on real type-3 rows (`wire_pos == 29`, `obj_off == '-0x160'`).
- Because this decoder works on the wire buffer (not object memory), one code path is correct for both classes; the probe samples of both types decode to 54/54 valid attributes.

### 3. Physique encoding

`body+126`/`body+128` are **signed `i16`**: `0` = *unset*, **negative** = *auto-derived by the game* (magnitude is the value). With `abs()`, **0/200** random players produce an implausible reading; without it 314/600 do. Cards touched by this are marked `*` (only Bukayo Saka here: 71 kg auto-derived).

### 4. Sanity of the decoded cards

- 21/21 cards have all 54 `PDxx` values in `0..20`.
- 21/21 cards satisfy `trailing ordinal == basic ordinal` **and** `dbid == uid`.
- Cross-checked against the real world: Messi Dribbling 20 / Vision 20 / Passing 19 on 169 cm · 67 kg; Kane Finishing 19 / Composure 18 on 188 cm · 86 kg; Haaland 195 cm · 94 kg; Courtois 200 cm · 96 kg — all physically plausible, and every CA/PA equals the `basic_people` value exactly.

## Files

- `scratch/t135/out/star_player_cards.json` — machine-readable cards: `people_db` file offset, body length, identity, names, header, 15 position bytes, all 54 `PDxx` values, cross-checks and layout probes.
- `scratch/t135/out/REPORT.md` — this report.
- `scratch/t135/out/DONE.md` — completion marker.

