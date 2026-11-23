# t118 People Schema Extraction

**Status: partial, evidence-bounded.** The supplied t113 directory contains 30 C listings (not the 428-function corpus described in the task brief). Available code, the seven-vtable index, and the real archive were analyzed; missing functions are not inferred as decompiled.

## Factory

`sub_1410992c0` has 13 explicit cases: `1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19`. All cases are emitted in `people_factory_map.json`; class labels without a vtable identity are explicitly marked as hints.

| Type | Class label | Allocation bytes | Constructor VA | Vtable VA |
|---:|---|---:|---|---|
| 1 | NON_PLAYER | 616 | inline/unknown | 0x141889da8 |
| 2 | PLAYER | 1000 | 0x140e06100 | 0x14187a428 |
| 3 | ACTUAL_PLAYER_AND_NON_PLAYER | 1240 | 0x1415d4e50 | 0x1418c4f38 |
| 4 | OFFICIAL | 344 | 0x141585480 | unresolved |
| 5 | unresolved | 48 | inline/unknown | 0x14188a548 |
| 6 | JOURNALIST | 168 | inline/unknown | 0x1418c5d28 |
| 7 | VIRTUAL_PLAYER | 80 | inline/unknown | 0x1418c18d8 |
| 8 | unresolved | 168 | inline/unknown | 0x1418c5d28 |
| 9 | unresolved | 1472 | 0x1410050f0 | unresolved |
| 16 | unresolved | 48 | inline/unknown | 0x14188ada8 |
| 17 | BASIC_PERSON | 112 | inline/unknown | 0x14187bd28 |
| 18 | unresolved | 224 | 0x141434f00 | unresolved |
| 19 | unresolved | 56 | inline/unknown | 0x14188b5b8 |

## 4CC Map

Extracted 754 getter/setter branch records and 628 distinct 4CCs across present vtable-root property handlers. PERSON and CONTRACT getter evidence is static-only; helper-only branches remain labeled as helper/computed and preserve source lines. The extractor reuses `t97`'s cast-aware `CFunc` offset analysis.

## Wire and Archive Probe

Basic archive byte closure: 658,011 rows, diff 0; class histogram: 1=166,064, 2=476,158, 3=4,757, 4=9,839, 5=1,193.

`people_db.dat`: 400,443,970 in-memory decompressed bytes; header is two zero bytes plus count 658,011. The first 1,193 records have byte-verified type 5 bodies and close exactly at offset 55,750; the next record is type 2 at that offset, with body beginning at 55,755. First 20 names include row 0 `Zarko Serafimovski`. The type-5 grammar is not used to guess later record boundaries.

Byte-verified type-5 fields are ordinal/type, a zero u32, UTF-8 name length and bytes, eight zero bytes, repeated ordinal, and two equal opaque u32 values. Semantic first/second/common-name IDs, DOB, nation, and UID are **not** established. Star UID byte hits are included as unvalidated raw occurrences, not asserted row membership.

The stream-step output is static source-order evidence only. The missing PERSON/PLAYER readers prevent L3 closure of their common/subclass serialization order and prevent a verified type 1..6 histogram or exact player/non-player body ends.

## IDA Follow-up

Prioritized missing VAs:

- P0: `PERSON::slot19_read_server` at `0x141084540`: base PERSON reader absent; blocks semantic wire-field closure
- P0: `PLAYER::slot19_read_server` at `0x140e3fb20`: PLAYER subclass reader absent; blocks player-body closure
- P0: `PLAYER::slot19_read_server` at `0x143beccd0`: vtable function has no matching t113/t95 decompiled C file
- P1: `ACTUAL_PLAYER::slot03_set_prop` at `0x140e0f380`: vtable function has no matching t113/t95 decompiled C file
- P1: `ACTUAL_PLAYER::slot02_get_prop` at `0x140e1c630`: vtable function has no matching t113/t95 decompiled C file
- P1: `PERSON::slot21_write` at `0x141084680`: PERSON writer absent; needed to cross-check serialization order
- P2: `ACTUAL_PLAYER::slot05_reg_prop` at `0x140e0f350`: vtable function has no matching t113/t95 decompiled C file
- P2: `ACTUAL_PLAYER_AND_NON_PLAYER::slot05_reg_prop` at `0x140e0f350`: vtable function has no matching t113/t95 decompiled C file
- P2: `ACTUAL_PLAYER_AND_NON_PLAYER::slot03_set_prop` at `0x140e0f380`: vtable function has no matching t113/t95 decompiled C file
- P2: `ACTUAL_PLAYER_AND_NON_PLAYER::slot02_get_prop` at `0x140e1c630`: vtable function has no matching t113/t95 decompiled C file
- P2: `VIRTUAL_PLAYER::slot19_read_server` at `0x143beccd0`: vtable function has no matching t113/t95 decompiled C file

`PLAYER_DATA` / `NON_PLAYER_DATA` serializers have no grounded VA in the supplied vtable JSON; the machine-readable output asks for a targeted symbol/vtable search without fabricating addresses.

## Evidence Levels

- **L3 byte-verified:** basic_people frame closure; first 1,193 type-5 records in people_db; first 20 raw row boundaries/names; next type-2 body start.
- **Static-only:** factory cases, property 4CC-to-memory-offset candidates, and stream calls in decompiled functions.
- **Open:** semantic names/DOB/nation/UID fields in PERSON, types 1/3/4/6 sample boundaries, PLAYER/NON_PLAYER body ends, and missing reader/writer implementations.

Input `.dat` files were read-only; decompressed bytes remained in memory.
