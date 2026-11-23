# t137d: Complete `NON_PLAYER` Coaching / Scouting / Mental Attributes L3 Map & Full Top-20 Manager Cards

You are working in `D:\tmp2b\fm24-db`. Do NOT modify `reports/`, `scratch/t01/LEDGER.json`, or `scripts/t137_non_player_managers_l3.py`. Write ONLY to `scripts/t137d_manager_cards_full.py` and `scratch/t137d/out/`.
Keep stdout compact (< 50 lines per command).

## Exact Root Cause Found in `t137c` (ALREADY DIAGNOSED!)
`t137c` (`scripts/t137_non_player_managers_l3.py`) successfully verified 20/20 Top FM24 managers with 20/20 exact CA/PA cross-check (`Pep Guardiola 190/200`, `Jürgen Klopp 190/195`, `Alex Ferguson 188/195`, `Diego Simeone 175/179`, etc.), **but only resolved 8 scalar L3 attributes** (`Nbpl, Ndep, Nfla, Nhat, Nint, Nmig, Npre, Nrot`) and left `Attacking, Defending, Tactical, Judging Ability, Judging Potential, Man Management, Determination` blank (`-`) because it missed TWO simple patterns in `NON_PLAYER::get_prop` (`scratch/t124/out/funcs/140dca880.c`) and `NON_PLAYER::set_prop` (`scratch/t124/out/funcs/140dc8c00.c`):
1. **Direct `*(char *)(a1 - N)` / `*(_BYTE *)(a1 - N)` reads** (signed `char`, NOT only `unsigned __int8`!), e.g.:
   - `140dca880.c:1347`: `case 1315987828` (`Npat` = Attacking) → `*(char *)(a1 - 215)` (`obj_off = -0xd7`)!
   - `140dca880.c:1359`: `case 1315987814` (`Npaf`) → `*(char *)(a1 - 26)`!
   - `140dca880.c:1370`: `case 1315988339` (`Npcs`) → `*(char *)(a1 - 23)`!
   - `140dca880.c:1395`: `case 1315988582` (`Npdf`) → `*(char *)(a1 - 27)`!
2. **Helper table dispatch `sub_140DC4DB0(v8, a2=idx, a3=1)`** (where `v8 = a1 - 248`! Check `v8` definition at top of `140dca880.c`!), e.g.:
   - `140dca880.c:1326`: `case 1315987812` (`Npad` = Adaptability) → `sub_140DC4DB0(v8, 13, 1)`
   - `140dca880.c:1380`: `case 1315988581` (`Npde` = Defending) → `sub_140DC4DB0(v8, 14, 1)`
   - And **`scratch/t137/out/ida/140dc4db0.c`** (484 lines, ALREADY DECOMPILED!) has the COMPLETE `switch (a2)` mapping every `idx` to `*(BYTE *)(v8 + offset)` (so `obj_off = (v8 - a1) + offset = -248 + offset`)!!
   - Also check `scratch/t137/out/ida/140dc4e30.c` (sibling getter/setter) and `scratch/t137/out/ida/140dc1d30.c` / `140dc40f0.c` / `140dca530.c`!

## Mission (Fast & Exact!)
1. Parse `scratch/t124/out/funcs/140dca880.c` (`NON_PLAYER::get_prop`), `scratch/t124/out/funcs/140dc8c00.c` (`NON_PLAYER::set_prop`), and `scratch/t137/out/ida/140dc4db0.c` (+ `140dc4e30.c` / `140dca530.c`) to extract **EVERY single `NON_PLAYER` scalar attribute 4CC -> `obj_off`**, verifying GET == SET agreement!
   - Specifically confirm all major FM24 staff attributes (`Npat` Attacking, `Npde` Defending, `Npta` Tactical, `Nptk` Tactical Knowledge, `Npad` Adaptability, `Npja` Judging Player Ability, `Npjp` Judging Player Potential, `Npjr` Judging Staff/Player Rep, `Npmm` Man Management, `Npmo` Motivating, `Npld` Level of Discipline, `Npwy` Working With Youngsters, `Nppf`/`Npph` Physiotherapy/Fitness, `Npgd`/`Npgh`/`Npgs` GK Coaching, `Npsf`/`Npcs`, `Ndal`/`Ndet` Determination, `Nbus`/`Ndir`/`Necc`/`Nfla`/`Nflx`/`Nhat`/`Nhmr`/`Nint`/`Nmig`/`Nneg`/`Npre`/`Nres`/`Nrot`/`Ntem`/`Nwid`/`Nwrr`, `Nbpl`/`Ndep`, etc.)!
2. Join each `obj_off` against the real Unicorn `NON_PLAYER::slot19` memory-write traces (using `scripts/t120_people_unicorn.py` or `scripts/t137_non_player_managers_l3.py` — check how `NON_PLAYER::slot19` writes those exact object offsets from `people_db.dat`!) so you have exact **`4CC -> (obj_off, wire_off_or_traced_byte, width, signed/unsigned)`**!
   - IMPORTANT: Check whether any attributes in `NON_PLAYER` are stored on a `0..20` scale OR `0..200` / `-1` / `0` unset convention (just like `PLAYER` attributes, or FM's `0..20` direct u8). Verify directly on **Pep Guardiola (UID 1120)**, **Jürgen Klopp (UID 9318)**, **Alex Ferguson (UID 2020287)**, **Diego Simeone (UID 707720)**, AND **Carlo Ancelotti**, **José Mourinho**, **Mikel Arteta**!
3. Decode COMPLETE attribute cards for **20 top FM24 managers/staff** (include the Top-10 from `t137c` + famous head coaches like Guardiola, Klopp, Ancelotti, Mourinho, Simeone, Arteta, Nagelsmann, Xabi Alonso, Emery, Tuchel — look up their UIDs in `scratch/t139/out/fm24_core.sqlite` or `basic_people_db.dat`!), showing their **real decoded coaching/mental/tactical/scouting numbers** (Attacking, Defending, Tactical, Technical/Mental, Judging Ability, Judging Potential, Man Management, Motivating, Discipline, Working With Youngsters, Tactical Knowledge, Adaptability, Determination)!
   - Cross-check all 20/20 CA & PA against `basic_people_db.dat`, and sanity-check domain anchors (e.g., Pep Guardiola & Jürgen Klopp must have world-class Attacking/Tactical/Man Management/Motivating ~16–20, NOT random garbage!).

## Deliverables
1. `scripts/t137d_manager_cards_full.py` (with `--selftest` asserting >= 25 L3 `NON_PLAYER` scalar attributes GET==SET, 20/20 CA/PA exact cross-check, and Guardiola/Klopp/Simeone/Ancelotti realistic world-class attribute checks!)
2. `scratch/t137d/out/non_player_l3_full.json`
3. `scratch/t137d/out/top20_managers_full_cards.json`
4. `scratch/t137d/out/REPORT.md` (with a full readable Markdown table of all 20 managers' real coaching/mental/tactical attributes!)
5. `scratch/t137d/out/DONE.md` (`DONE type=t137d`, count of verified L3 attributes, 20/20 managers, `--selftest PASS`)

Run `py -V:3.12 -B scripts/t137d_manager_cards_full.py` and `--selftest` and verify 0 failures before finishing!
