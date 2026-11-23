# t98 table_45/table_48 closure

Status: complete for the byte frame, 18-column layout, rec_type census, and the 117-code evidence ledger.

## Results

- `table_45`: 84,477 rows, 7,608,748 bytes, SHA-256 `46799e2f79acc276cc2e349fa4724de917428e07d960d8d6059dc32b1fd58bf9`.
- `table_48`: 5,210 rows, 446,049 bytes, SHA-256 `f86bf6ee0bcc253fdc5b95a396e3a2fd433ccf92e1f769dbc742cdfcf73de8a5`.
- Both tables decode with `rowlen = 80 + namelen`, 26-byte body, and 13-byte identity trailer; table_45 has 37 observed rec_type values and table_48 has 31.
- 117 accessor rows: 34 mapped L3, 3 derived L2, 80 held.

## Footer ruling

The byte-exact row walk ends at `payload_len - 8` for both tables. The observed footer is therefore 8 bytes: `table_45 = 00000001775f0100`, `table_48 = 000000019f180000`. The requested 9-byte closure is verified as the 9-byte window `00 + footer8`; its first zero is the final row terminator byte, not an independent footer field. `verify.py` asserts both forms.

## Physical columns

| Column | Wire location | this offset | Read source | Write source |
|---|---|---:|---|---|
| `key_u32` | `row+0` | `0x4c` | `scratch/t95/funcs/141544130.c:22` | `scratch/t95/funcs/1444e4b00.c:27` |
| `rec_type` | `row+4` | `0x5e` | `scratch/t95/funcs/141544130.c:26` | `scratch/t95/funcs/1444e4b00.c:31` |
| `uid_slot_0` | `row+5` | `0x18` | `scratch/t95/funcs/141544130.c:33` | `scratch/t95/funcs/1444e4b00.c:35-39` |
| `uid_slot_1` | `row+13` | `0x20` | `scratch/t95/funcs/141544130.c:46` | `scratch/t95/funcs/1444e4b00.c:43-47` |
| `uid_slot_2` | `row+21` | `0x28` | `scratch/t95/funcs/141544130.c:59` | `scratch/t95/funcs/1444e4b00.c:50` |
| `uid_slot_3` | `row+29` | `0x30` | `scratch/t95/funcs/141544130.c:68` | `scratch/t95/funcs/1444e4b00.c:52` |
| `name` | `row+37: [u32 length][utf8 bytes]` | `0x38` | `scratch/t95/funcs/141544130.c:70` | `scratch/t95/funcs/1444e4b00.c:54` |
| `date_0` | `tail+0 = row+41+namelen` | `0x40` | `scratch/t95/funcs/141544130.c:73` | `scratch/t95/funcs/1444e4b00.c:57` |
| `date_1` | `tail+4 = row+45+namelen` | `0x44` | `scratch/t95/funcs/141544130.c:75` | `scratch/t95/funcs/1444e4b00.c:59` |
| `date_2` | `tail+8 = row+49+namelen` | `0x48` | `scratch/t95/funcs/141544130.c:77` | `scratch/t95/funcs/1444e4b00.c:61` |
| `scalar_u32` | `tail+12 = row+53+namelen` | `0x50` | `scratch/t95/funcs/141544130.c:80` | `scratch/t95/funcs/1444e4b00.c:64` |
| `scalar_u16_0` | `tail+16 = row+57+namelen` | `0x54` | `scratch/t95/funcs/141544130.c:84` | `scratch/t95/funcs/1444e4b00.c:68` |
| `scalar_u16_1` | `tail+18 = row+59+namelen` | `0x56` | `scratch/t95/funcs/141544130.c:88` | `scratch/t95/funcs/1444e4b00.c:72` |
| `scalar_u16_2` | `tail+20 = row+61+namelen` | `0x58` | `scratch/t95/funcs/141544130.c:92` | `scratch/t95/funcs/1444e4b00.c:76` |
| `scalar_u8_0` | `tail+22 = row+63+namelen` | `0x5a` | `scratch/t95/funcs/141544130.c:96` | `scratch/t95/funcs/1444e4b00.c:80` |
| `scalar_u8_1` | `tail+23 = row+64+namelen` | `0x5b` | `scratch/t95/funcs/141544130.c:100` | `scratch/t95/funcs/1444e4b00.c:84` |
| `scalar_u8_2` | `tail+24 = row+65+namelen` | `0x5c` | `scratch/t95/funcs/141544130.c:104` | `scratch/t95/funcs/1444e4b00.c:88` |
| `scalar_u8_3` | `tail+25 = row+66+namelen` | `0x5d` | `scratch/t95/funcs/141544130.c:108` | `scratch/t95/funcs/1444e4b00.c:92` |

The identity trailer is structural at `row_end-13`: ordinal u32, two uid u32 values, and a zero terminator byte. It is excluded from the 18 persisted columns.

## Direct STARTING_RECORD 4CCs

The following aliases are from `STARTING_RECORD::slot02_get_prop` and `slot03_set_prop`; `get`/`set` behavior is kept separate from the outer router's tag names.

| 4CC | Physical column | this offset | Wire location | GET lines | SET lines |
|---|---|---:|---|---:|---:|
| `otht` | `uid_slot_2` | `0x28` | `wire+21` | `79-95` | `delegated` |
| `rati` | `scalar_u8_0` | `0x5a` | `tail+22` | `96-112` | `delegated` |
| `rrea` | `scalar_u8_2` | `0x5c` | `tail+24` | `113-130` | `delegated` |
| `info` | `scalar_u8_1` | `0x5b` | `tail+23` | `135-151` | `256-259` |
| `ogls` | `scalar_u16_2` | `0x58` | `tail+20` | `154-174` | `261-268` |
| `team` | `uid_slot_1` | `0x20` | `wire+13` | `180-196` | `226-229` |
| `stnm` | `name` | `0x38` | `wire+37` | `197-221` | `230-243` |
| `stid` | `uid_slot_0` | `0x18` | `wire+5` | `222-243` | `245-248` |
| `stdb` | `date_2` | `0x48` | `tail+8` | `244-275` | `141-170` |
| `stdt` | `date_0` | `0x40` | `tail+0` | `276-317` | `172-220` |
| `fsgt` | `scalar_u16_2` | `0x58` | `tail+20` | `318-336` | `84-88` |
| `gams` | `scalar_u16_0` | `0x54` | `tail+16` | `337-338` | `122-136` |
| `gols` | `scalar_u16_1` | `0x56` | `tail+18` | `339-366` | `89-98` |
| `endt` | `date_1` | `0x44` | `tail+4` | `367-424` | `27-75` |
| `etin` | `scalar_u8_3` | `0x5d` | `tail+25` | `369-381` | `77-81` |
| `apps` | `scalar_u16_0` | `0x54` | `tail+16` | `425-467` | `122-136` |
| `atte` | `scalar_u32` | `0x50` | `tail+12` | `427-468` | `124-129` |
| `cash` | `scalar_u32` | `0x50` | `tail+12` | `469-485` | `107-109` |
| `cnst` | `scalar_u8_3` | `0x5d` | `tail+25` | `486-502` | `110-112` |
| `comp` | `uid_slot_3` | `0x30` | `wire+29` | `503-520` | `113-116` |

## rec_type activity

`active_payload_columns` means a value is not one of the data defaults (zero, all-ones, or the packed date sentinel `0x076c0001`). It is a data-side profile only and never promotes a held accessor to L3.

| rec_type | table_45 rows | table_48 rows | active table_45 payload columns |
|---:|---:|---:|---|
| `1` | 2,043 | 13 | `key_u32`, `uid_slot_0`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `10` | 1,688 | 227 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `11` | 1,549 | 222 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_1` |
| `12` | 1,358 | 210 | `key_u32`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0` |
| `13` | 1,223 | 191 | `key_u32`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0`, `scalar_u16_1` |
| `14` | 1,490 | 222 | `key_u32`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0` |
| `15` | 1,282 | 193 | `key_u32`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0` |
| `16` | 68 | 4 | `key_u32`, `uid_slot_0`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0` |
| `17` | 58 | 1 | `key_u32`, `uid_slot_0`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0` |
| `18` | 931 | 158 | `key_u32`, `uid_slot_0`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0` |
| `19` | 823 | 121 | `key_u32`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0` |
| `2` | 2,151 | 19 | `key_u32`, `uid_slot_0`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `20` | 1,783 | 166 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `21` | 879 | 8 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `22` | 1,280 | 343 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `23` | 989 | 354 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `24` | 653 | 147 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1`, `scalar_u16_2` |
| `25` | 1,811 | 574 | `key_u32`, `uid_slot_2`, `uid_slot_3`, `date_0`, `scalar_u16_1`, `scalar_u16_2` |
| `253` | 314 | 0 | `key_u32`, `date_0`, `scalar_u8_1` |
| `254` | 199 | 0 | `key_u32`, `date_0`, `scalar_u8_1` |
| `255` | 38,968 | 0 | `key_u32`, `uid_slot_0`, `name`, `scalar_u8_0`, `scalar_u8_1`, `scalar_u8_2`, `scalar_u8_3` |
| `26` | 946 | 157 | `key_u32`, `uid_slot_2`, `uid_slot_3`, `date_0`, `scalar_u32`, `scalar_u16_1` |
| `27` | 1,265 | 188 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `28` | 1,243 | 175 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `29` | 936 | 89 | `key_u32`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u32`, `scalar_u16_0`, `scalar_u16_1` |
| `3` | 2,127 | 45 | `key_u32`, `uid_slot_0`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `30` | 1,538 | 0 | `key_u32`, `uid_slot_2`, `uid_slot_3`, `date_0`, `scalar_u16_1`, `scalar_u16_2` |
| `31` | 82 | 0 | `key_u32`, `uid_slot_0`, `uid_slot_1`, `uid_slot_2`, `name`, `date_0`, `date_2`, `scalar_u32`, `scalar_u16_0`, `scalar_u16_1` |
| `32` | 43 | 0 | `key_u32`, `uid_slot_0`, `uid_slot_1`, `uid_slot_2`, `name`, `date_0`, `date_2`, `scalar_u32`, `scalar_u16_0`, `scalar_u16_1` |
| `33` | 39 | 0 | `key_u32`, `uid_slot_0`, `uid_slot_1`, `uid_slot_2`, `name`, `date_0`, `date_2`, `scalar_u32` |
| `34` | 631 | 74 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `35` | 0 | 3 | - |
| `4` | 2,221 | 65 | `key_u32`, `uid_slot_0`, `uid_slot_3`, `name`, `date_0`, `date_1`, `date_2`, `scalar_u16_0`, `scalar_u16_1` |
| `5` | 1,207 | 68 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `name`, `date_0`, `date_2`, `scalar_u32`, `scalar_u16_0`, `scalar_u16_1` |
| `6` | 1,514 | 76 | `key_u32`, `uid_slot_0`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `date_2`, `scalar_u32` |
| `7` | 2,392 | 276 | `key_u32`, `uid_slot_1`, `uid_slot_2`, `uid_slot_3`, `name`, `date_0`, `scalar_u32`, `scalar_u16_0`, `scalar_u16_1` |
| `8` | 3,391 | 660 | `key_u32`, `uid_slot_2`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0`, `scalar_u16_1`, `scalar_u16_2` |
| `9` | 3,362 | 161 | `key_u32`, `uid_slot_2`, `uid_slot_3`, `date_0`, `date_1`, `scalar_u16_0`, `scalar_u16_1`, `scalar_u16_2` |

## 117-code ledger

Each mapped/derived row carries the tuple `(rec_type, physical_col, mem_off, wire_off)` plus the hub-side route offset from the frozen slots asset. Held rows have a null tuple and an explicit no-promotion reason. The complete machine-readable list is in `table45_full_schema.json`.

The L3 dispatch families are evidenced in `scratch/t95/funcs/1411f1090.c` at the CFG/CHA/CHS/CLA/COS/CYP/CYS case blocks and the `LABEL_394 -> 0x144026350` hub. `LABEL_362` fallback and the absence criterion remain held for the other families.

## Verification

Run:

```text
C:\Users\oak\AppData\Local\Programs\Python\Python312\python.exe -I -B scripts/t98_table45_closure.py --selftest
C:\Users\oak\AppData\Local\Programs\Python\Python312\python.exe -I -B scratch/t98/out/verify.py
```
