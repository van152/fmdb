# t137d — Full `NON_PLAYER` L3 Coaching/Scouting/Mental/Tactical Attributes & Top-20 Manager Cards

- Verified `NON_PLAYER` L3 scalar attributes: **34** (`32` GET==SET exact across `140dca880.c`, `140dc8c00.c`, `140dc4db0.c`)
- Decoded via live `editor.exe` x86_64 Unicorn (`NON_PLAYER::slot19` exact consumption `20/20`)
- CA / PA cross-check vs `basic_people_db.dat`: **20/20** & **20/20**
- All 34 attributes strictly within `0..20`: **20/20**

## Top-20 Highest-CA FM24 Managers & Staff (Live Decoded Attributes)

| # | Name | UID | CA/PA | C.Att | C.Def | C.Tac | C.Tec | C.Men | TacK | J.PA | J.PP | ManM | Motiv | Disc | Young | Det | Press |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **Pep Guardiola** | 1120 | 190/200 | 20 | 17 | 20 | 20 | 17 | 20 | 20 | 19 | 20 | 20 | 15 | 16 | 18 | 20 |
| 2 | **Jürgen Klopp** | 9318 | 190/195 | 19 | 15 | 18 | 17 | 19 | 16 | 18 | 17 | 20 | 20 | 16 | 17 | 20 | 19 |
| 3 | **Alex Ferguson** | 2020287 | 188/195 | 17 | 12 | 14 | 14 | 20 | 13 | 18 | 18 | 18 | 19 | 19 | 17 | 20 | 15 |
| 4 | **Daniel Levy** | 141932 | 185/190 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 6 | 12 | 0 | 0 | 15 | 20 | 0 |
| 5 | **Rinat Akhmetov** | 5311850 | 180/190 | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 0 | 19 | 18 | 18 | 0 | 17 | 1 |
| 6 | **Ricard Pruna** | 67065354 | 180/185 | 1 | 1 | 1 | 1 | 1 | 5 | 11 | 12 | 20 | 20 | 19 | 20 | 19 | 19 |
| 7 | **Neil Bath** | 5006673 | 180/180 | 0 | 0 | 0 | 0 | 13 | 0 | 14 | 16 | 14 | 15 | 0 | 20 | 0 | 12 |
| 8 | **Giuseppe Marotta** | 705257 | 179/186 | 0 | 0 | 0 | 0 | 0 | 9 | 20 | 19 | 18 | 19 | 0 | 14 | 18 | 0 |
| 9 | **Ricardo Sasaki** | 316514 | 175/185 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 0 | 0 | 0 |
| 10 | **Evgeny Giner** | 486064 | 175/180 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 | 18 | 15 | 0 | 17 | 0 |
| 11 | **Aurélio Pereira** | 745495 | 175/180 | 0 | 0 | 0 | 0 | 0 | 0 | 19 | 20 | 18 | 17 | 0 | 20 | 0 | 0 |
| 12 | **Juanjo Brau** | 7445017 | 175/180 | 5 | 5 | 5 | 5 | 6 | 5 | 6 | 5 | 16 | 19 | 20 | 20 | 15 | 15 |
| 13 | **Domingos Soares de Oliveira** | 84100002 | 175/180 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17 | 15 | 14 | 0 | 15 | 0 |
| 14 | **Diego Simeone** | 707720 | 175/179 | 12 | 14 | 16 | 11 | 19 | 15 | 16 | 14 | 16 | 18 | 16 | 13 | 20 | 13 |
| 15 | **Txiki Begiristain** | 7449788 | 175/175 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 14 | 0 | 0 | 0 | 14 | 15 | 0 |
| 16 | **Rodolfo Borrell** | 67046405 | 175/175 | 17 | 13 | 14 | 18 | 14 | 14 | 15 | 18 | 14 | 16 | 14 | 20 | 16 | 14 |
| 17 | **John Henry** | 82015127 | 175/175 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19 | 0 |
| 18 | **Lieven Maesschalck** | 538614 | 173/190 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 15 | 18 | 1 | 1 | 17 | 1 |
| 19 | **Aurelio De Laurentiis** | 1405352 | 172/174 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17 | 0 | 18 | 0 |
| 20 | **Paul Mitchell** | 4001459 | 171/171 | 0 | 0 | 0 | 0 | 0 | 0 | 18 | 18 | 0 | 0 | 0 | 15 | 16 | 0 |

## Complete 34-Attribute L3 Layout (`v8 = obj - 248`)

| 4CC | Label | Category | `obj_off` | `v8_off` | Dispatch | GET==SET |
|---|---|---|---:|---:|---|---|
| `Ncha` | Coaching Attacking | coaching | `-190` | `+58` | `sub_140DC4DB0(v8, 5)` | YES |
| `Nchd` | Coaching Defending | coaching | `-189` | `+59` | `sub_140DC4DB0(v8, 6)` | YES |
| `Nchf` | Coaching Fitness | coaching | `-188` | `+60` | `sub_140DC4DB0(v8, 7)` | YES |
| `Nchm` | Coaching Mental | coaching | `-187` | `+61` | `sub_140DC4DB0(v8, 8)` | YES |
| `Ncte` | Coaching Technical | coaching | `-186` | `+62` | `sub_140DC4DB0(v8, 9)` | YES |
| `Ncta` | Coaching Tactical | coaching | `-185` | `+63` | `sub_140DC4DB0(v8, 10)` | YES |
| `Ncsp` | Coaching Set Pieces | coaching | `-173` | `+75` | `sub_140DC4DB0(v8, 11)` | YES |
| `Npgh` | GK Handling | coaching_gk | `-183` | `+65` | `sub_140DC4DB0(v8, 1)` | YES |
| `Npgd` | GK Distribution | coaching_gk | `-182` | `+66` | `sub_140DC4DB0(v8, 2)` | YES |
| `Npgs` | GK Shot Stopping | coaching_gk | `-197` | `+51` | `sub_140DC4DB0(v8, 0)` | GET-only |
| `Npja` | Judging Player Ability | scouting | `-196` | `+52` | `sub_140DC4DB0(v8, 15)` | YES |
| `Npjp` | Judging Player Potential | scouting | `-195` | `+53` | `sub_140DC4DB0(v8, 16)` | YES |
| `Npmm` | Man Management | mental | `-194` | `+54` | `sub_140DC4DB0(v8, 4)` | YES |
| `Npmo` | Motivating | mental | `-193` | `+55` | `sub_140DC4DB0(v8, 18)` | YES |
| `Npph` | Physiotherapy | medical | `-192` | `+56` | `sub_140DC4DB0(v8, 19)` | YES |
| `Nptk` | Tactical Knowledge | mental | `-191` | `+57` | `sub_140DC4DB0(v8, 12)` | YES |
| `Npld` | Level of Discipline | mental | `-220` | `+28` | `sub_140DC4DB0(v8, 17)` | YES |
| `Npwy` | Working With Youngsters | coaching | `-212` | `+36` | `sub_140DC4DB0(v8, 3)` | YES |
| `Npde` | Determination | mental | `-211` | `+37` | `sub_140DC4DB0(v8, 14)` | GET-only |
| `Natt` | Attacking Tendency | tactical | `-224` | `+24` | `*(char*)(a1 -224)` | YES |
| `Ndir` | Directness | tactical | `-221` | `+27` | `*(char*)(a1 -221)` | YES |
| `Nint` | Interference / Use of Subs | tactical | `-218` | `+30` | `*(char*)(a1 -218)` | YES |
| `Npat` | Patience / Tempo | tactical | `-215` | `+33` | `*(char*)(a1 -215)` | YES |
| `Npre` | Pressing | tactical | `-214` | `+34` | `*(char*)(a1 -214)` | YES |
| `Nres` | Resources / Squad Building | tactical | `-213` | `+35` | `*(char*)(a1 -213)` | YES |
| `Nbpl` | Buying Players | tactical | `-210` | `+38` | `*(char*)(a1 -210)` | YES |
| `Nmig` | Mind Games | tactical | `-209` | `+39` | `*(char*)(a1 -209)` | YES |
| `Ndep` | Depth | tactical | `-205` | `+43` | `*(char*)(a1 -205)` | YES |
| `Nfla` | Flamboyancy | tactical | `-204` | `+44` | `*(char*)(a1 -204)` | YES |
| `Nflx` | Flexibility | tactical | `-203` | `+45` | `*(char*)(a1 -203)` | YES |
| `Nhat` | Hardness of Training | tactical | `-202` | `+46` | `*(char*)(a1 -202)` | YES |
| `Nrot` | Squad Rotation | tactical | `-201` | `+47` | `*(char*)(a1 -201)` | YES |
| `Ntem` | Tempo | tactical | `-200` | `+48` | `*(char*)(a1 -200)` | YES |
| `Nwid` | Width | tactical | `-199` | `+49` | `*(char*)(a1 -199)` | YES |
