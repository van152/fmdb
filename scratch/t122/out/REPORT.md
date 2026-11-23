# t122 — people_db.dat Full L3 Schema

Evidence rows: 3,000; samples: 15; overall 4CC mappings: 177 type-specific joins.

## Person types

| Type | Class | Rows | Virtual base offset | Sample reads | Joined 4CCs |
|---:|---|---:|---:|---:|---:|
| 5 | RETIRED_PERSON | 1193 | 0x0 | 18 | 41 |
| 2 | PLAYER | 1283 | 0x278 | 543 | 35 |
| 1 | NON_PLAYER | 481 | 0xf8 | 452 | 35 |
| 3 | ACTUAL_PLAYER_AND_NON_PLAYER | 9 | 0x368 | 690 | 35 |
| 4 | OFFICIAL | 34 | 0x138 | 111 | 31 |

## PLAYER wire 0..147 (end-exclusive 148)

| Wire | Bytes | base_off | obj_off | Classification | Evidence |
|---:|---:|---|---|---|---|
| 0..9 | 10 | 0x1fa | -0x7e | PLAYER CA/PA/reputation fixed header | Unicorn trace; 3 observations |
| 10..10 | 1 | 0x265 | -0x13 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 11..14 | 4 | 0x261 | -0x17 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 15..16 | 2 | 0x266 | -0x12 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 17..20 | 4 | 0x128 | -0x150 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 21..28 | 8 | 0x130 | -0x148 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 29..97 | 69 | 0x208 | -0x70 | PLAYER_DATA 69-byte attribute block (unnamed bytes absent 4CC proof) | Unicorn trace; 3 observations |
| 98..101 | 4 | 0x1d0 | -0xa8 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 102..102 | 1 | 0x25f | -0x19 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 103..116 | 14 | 0x1ec | -0x8c | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 117..120 | 4 | 0x204 | -0x74 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 121..124 | 4 | 0x25b | -0x1d | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 125..125 | 1 | None | None | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 126..127 | 2 | 0x14c | -0x12c | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 128..129 | 2 | 0x14e | -0x12a | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 130..133 | 4 | 0x148 | -0x130 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 134..137 | 4 | 0x1e8 | -0x90 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 138..138 | 1 | 0x260 | -0x18 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 139..142 | 4 | None | None | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 143..146 | 4 | 0x1d4 | -0xa4 | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |
| 147..147 | 1 | None | None | PLAYER fixed header/date/physical fields (IDA callsite required for semantic label) | Unicorn trace; 3 observations |

### 69-byte PLAYER_DATA region

Wire bytes 29..97 inclusive are read as a single 69-byte block into `obj_off=-0x70` (`base_off=0x208` in the supplied representative trace). Available 4CC joins are reported separately in JSON; no PDxx/Pxxx labels are asserted without a matching numeric `mem_off` and C evidence.

## Evidence levels

- **L3-joined:** observed Unicorn object-memory range overlaps an IDA 4CC mapping with numeric offset and width.
- **Unicorn-wire-verified:** exact wire width and destination offset are observed; no 4CC semantic join is claimed.
- **Static-only:** code/source claims are not promoted to runtime field semantics.

## Caveats

Range join uses `base_off - obj_offset_from_base` to express reads relative to each dynamic type. Pointer/helper-only 4CCs cannot be range-joined. Sample reads are preserved in JSON.
