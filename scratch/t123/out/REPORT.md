# t123 — basic_people_db.dat L3 decoder

**Status:** byte-exact record grammar and BASIC_PERSON/PERSON byte map complete. Name resolution is verified indirectly through the people read chain and `name_table_extra_0/1/2`; the direct `basic_people` row-to-name-ID join remains negative.

## Closure

The zstandard payload contains **658,011** rows. The parser ended at `54060034` and `len(payload)-9` is the same value (`diff=0`). Type counts are `{'1': 166064, '2': 476158, '3': 4757, '4': 9839, '5': 1193}` and widths are `{'1': 83, '2': 83, '3': 83, '4': 34, '5': 22}`.

## Byte Map

Types 1/2/3 are 83 bytes. Their semantic sequence is `Pnti` (reference pair), `Pcti`, `Pnai`, the unresolved `sub_140FB2BA0` helper, `Pdva`, `Pcww`, `PWRP`, `PCRP`, `PHRP`, `PCAB`, `PPAB`, `Pdob`, the remaining BASIC_PERSON fields, then PERSON +24 and identity `[ordinal, dbid, uid]`.

Type 4 is 34 bytes: marker/type, 8-byte `Pnti`, 2-byte `PCRP` at object +82, 2-byte `Pdob`, PERSON +24, and the 12-byte identity. The reader copies the short reputation into object +80 and +84.

Type 5 is 22 bytes: marker/type, PERSON +24, and the 12-byte identity. The generated JSON contains one entry for every byte, including prefix and base-PERSON bytes.

### CA/PA correction

The prior t115 probes at row+44/+46 are preserved as legacy candidates. The 4CC map makes row+48/+50 the actual `PCAB`/`PPAB` values. This changes Messi from the old candidate `200/200` to semantic `185/200`, and changes Ronaldo's semantic PA to `196`; the old `160/200` probe remains visible in the anchor record.

## Name Tables

- `name_table_0`: 245,981 fixed 12-byte rows; extra pool closure `True`; UTF-8 bytes `1,869,579`.
- `name_table_1`: 542,060 fixed 12-byte rows; extra pool closure `True`; UTF-8 bytes `4,377,345`.
- `name_table_2`: 85,668 fixed 12-byte rows; extra pool closure `True`; UTF-8 bytes `950,661`.

The direct row bytes do not contain any of the three anchor name ordinals, and the +56 helper definition is absent from the supplied decompilation set. The verified path is the people read-chain's three 4-byte name IDs followed by the three extra pools. The resulting anchor names are Harry Kane, Cristiano Ronaldo, and Lionel Messi.

## Verified Top 50 by PCAB (CA)

| # | Name | UID | Type | CA | PA | Birth date | Nation (ordinal/UID) | Club (ordinal/UID) |
|---:|---|---:|---:|---:|---:|---|---|---|
| 1 | Kevin De Bruyne | 18004457 | 2 | 190 | 190 | 1991-06-28 | 131/757 | 589/679 |
| 2 | Kylian Mbappé | 85139014 | 2 | 188 | 197 | 1998-12-20 | 143/769 | 763/868 |
| 3 | Erling Haaland | 29179241 | 2 | 188 | 195 | 2000-07-21 | 160/786 | 589/679 |
| 4 | Lionel Messi | 7458500 | 2 | 185 | 200 | 1987-06-24 | 187/1649 | 63234/72052048 |
| 5 | Vinícius Júnior | 19302146 | 2 | 184 | 190 | 2000-07-12 | 189/1651 | 1495/1736 |
| 6 | Harry Kane | 28049320 | 2 | 184 | 185 | 1993-07-28 | 139/765 | 800/915 |
| 7 | Mohamed Salah | 98028755 | 2 | 181 | 187 | 1992-06-15 | 11/16 | 586/676 |
| 8 | Thibaut Courtois | 18026122 | 2 | 181 | 181 | 1992-05-11 | 131/757 | 1495/1736 |
| 9 | Ederson | 55057659 | 2 | 180 | 180 | 1993-08-17 | 189/1651 | 589/679 |
| 10 | Rodri | 67217524 | 2 | 180 | 180 | 1996-06-22 | 170/796 | 589/679 |
| 11 | Robert Lewandowski | 719601 | 2 | 178 | 190 | 1988-08-21 | 161/787 | 1480/1708 |
| 12 | Virgil van Dijk | 37024025 | 2 | 178 | 183 | 1991-07-08 | 158/784 | 586/676 |
| 13 | Bernardo Silva | 55041632 | 2 | 178 | 180 | 1994-08-10 | 162/788 | 589/679 |
| 14 | Jude Bellingham | 29232937 | 2 | 177 | 188 | 2003-06-29 | 139/765 | 1495/1736 |
| 15 | Declan Rice | 28106491 | 2 | 176 | 182 | 1999-01-14 | 139/765 | 513/602 |
| 16 | Alisson | 19058734 | 2 | 176 | 180 | 1992-10-02 | 189/1651 | 586/676 |
| 17 | Neymar | 19024412 | 2 | 175 | 190 | 1992-02-05 | 189/1651 | 3019/102852 |
| 18 | Marc-André ter Stegen | 35017428 | 2 | 175 | 183 | 1992-04-30 | 145/771 | 1480/1708 |
| 19 | Bukayo Saka | 28122642 | 2 | 174 | 186 | 2001-09-05 | 139/765 | 513/602 |
| 20 | Joshua Kimmich | 92039023 | 2 | 174 | 183 | 1995-02-08 | 145/771 | 800/915 |
| 21 | Martin Ødegaard | 53095137 | 2 | 173 | 180 | 1998-12-17 | 160/786 | 513/602 |
| 22 | Lautaro Martínez | 14110660 | 2 | 173 | 177 | 1997-08-22 | 187/1649 | 985/1135 |
| 23 | Rúben Dias | 55070299 | 2 | 173 | 177 | 1997-05-14 | 162/788 | 589/679 |
| 24 | Antoine Griezmann | 67086656 | 2 | 172 | 180 | 1991-03-21 | 143/769 | 1467/1687 |
| 25 | Luka Modrić | 653054 | 2 | 171 | 180 | 1985-09-09 | 135/761 | 1495/1736 |
| 26 | Jan Oblak | 64016316 | 2 | 171 | 178 | 1993-01-07 | 169/795 | 1467/1687 |
| 27 | Bruno Fernandes | 43124203 | 2 | 171 | 174 | 1994-09-08 | 162/788 | 590/680 |
| 28 | Eduardo Camavinga | 49056243 | 2 | 170 | 180 | 2002-11-10 | 143/769 | 1495/1736 |
| 29 | Ronald Araujo | 78085068 | 2 | 170 | 176 | 1999-03-07 | 195/1657 | 1480/1708 |
| 30 | Heung-Min Son | 92020288 | 2 | 170 | 173 | 1992-07-08 | 80/135 | 638/728 |
| 31 | Phil Foden | 28108494 | 2 | 169 | 180 | 2000-05-28 | 139/765 | 589/679 |
| 32 | Victor Osimhen | 13158205 | 2 | 169 | 175 | 1998-12-29 | 33/38 | 998/1150 |
| 33 | Leroy Sané | 91138280 | 2 | 169 | 172 | 1996-01-11 | 145/771 | 800/915 |
| 34 | Rodrygo | 19306929 | 2 | 168 | 178 | 2001-01-09 | 189/1651 | 1495/1736 |
| 35 | Federico Valverde | 78074594 | 2 | 168 | 175 | 1998-07-22 | 195/1657 | 1495/1736 |
| 36 | Ousmane Dembélé | 85140178 | 2 | 167 | 174 | 1997-05-15 | 143/769 | 763/868 |
| 37 | İlkay Gündoğan | 91003875 | 2 | 167 | 167 | 1990-10-24 | 145/771 | 1480/1708 |
| 38 | John Stones | 28060397 | 2 | 166 | 170 | 1994-05-28 | 139/765 | 589/679 |
| 39 | Éder Militão | 19273276 | 2 | 166 | 168 | 1998-01-18 | 189/1651 | 1495/1736 |
| 40 | Antonio Rüdiger | 92023410 | 2 | 166 | 166 | 1993-03-03 | 145/771 | 1495/1736 |
| 41 | Karim Benzema | 8435089 | 2 | 165 | 185 | 1987-12-19 | 143/769 | 3122/106063 |
| 42 | Frenkie de Jong | 37047745 | 2 | 165 | 181 | 1997-05-12 | 158/784 | 1480/1708 |
| 43 | Gabriel Jesus | 19220266 | 2 | 165 | 175 | 1997-04-03 | 189/1651 | 513/602 |
| 44 | Bruno Guimarães | 19297055 | 2 | 165 | 170 | 1997-11-16 | 189/1651 | 598/688 |
| 45 | William Saliba | 49039004 | 2 | 164 | 182 | 2001-03-24 | 143/769 | 513/602 |
| 46 | Jack Grealish | 28067800 | 2 | 164 | 175 | 1995-09-10 | 139/765 | 589/679 |
| 47 | Kyle Walker | 28009441 | 2 | 164 | 164 | 1990-05-28 | 139/765 | 589/679 |
| 48 | Rafael Leão | 83111483 | 2 | 163 | 176 | 1999-06-10 | 162/788 | 952/1099 |
| 49 | Thiago | 67022040 | 2 | 163 | 173 | 1991-04-11 | 170/796 | 586/676 |
| 50 | Marquinhos | 19163495 | 2 | 163 | 165 | 1994-05-14 | 189/1651 | 763/868 |

The complete byte map, all anchor probes, raw helper probes, and name-pool closure statistics are in `basic_people_l3_complete.json`.
