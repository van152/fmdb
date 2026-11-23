# t106 — 非编号特殊成员格式解析与闭合验证

- 成员数 **13**，字节精确闭合 **13/13**
- 解包：`scripts/t38_multiframe.py`（E80：`data_base + offset` 定位、`packed_size` 界定、`size` 选帧）
- 脚本：`scripts/t106_special_members.py`（`--help` / `--selftest`，退出码 0/1/2）

## 闭合汇总表

| 成员 | 载荷字节 | 记录数 | 头 | 行/记录 | footer | 闭合算式 | OK |
|---|---:|---:|---:|---|---:|---|---|
| `name_table_0` | 2,951,784 | 245,981 | 12B | 12B 定长 | 0B | `12 + 245981*12 = 2951784` | ✅ |
| `name_table_1` | 6,504,732 | 542,060 | 12B | 12B 定长 | 0B | `12 + 542060*12 = 6504732` | ✅ |
| `name_table_2` | 1,028,028 | 85,668 | 12B | 12B 定长 | 0B | `12 + 85668*12 = 1028028` | ✅ |
| `name_table_extra_0` | 3,837,439 | 245,981 | 12B | variable_stride | 0B | `12 + sum(8+len) = 3837439` | ✅ |
| `name_table_extra_1` | 8,713,837 | 542,060 | 12B | variable_stride | 0B | `12 + sum(8+len) = 8713837` | ✅ |
| `name_table_extra_2` | 1,636,017 | 85,668 | 12B | variable_stride | 0B | `12 + sum(8+len) = 1636017` | ✅ |
| `common_name_links` | 120,572 | 12,056 | 12B | 10B 定长 | 0B | `12 + 12056*10 = 120572` | ✅ |
| `club_links` | 435,279 | 9,261 | 12B | 47B 定长 | 0B | `12 + 9261*47 = 435279` | ✅ |
| `simple_vars` | 82,385 | 28,552 | 34B | variable_stride | 0B | `34 + sum(2+len) = 82385` | ✅ |
| `summary` | 1,648,018 | 54,087 | 40B | separator_framed | 4B | `40 + sum(body+5) [1637014] + tail 11004 = 1648018` | ✅ |
| `table_for_old_save_23` | 3,914 | 278 | 15B | 14B 定长 | 7B | `15 + 278*14 + 7 = 3914` | ✅ |
| `table_for_old_save_25` | 1,464,951 | 7,047 | 12B | variable_stride | 9B | `12 + sum(rowlen) [1464740] + 9 = 1464951` | ✅ |
| `fantasy_draft_future_regens` | 5,657 | 40 | 12B | variable_stride | 31B | `12 + sum(rowlen) [5614] + 31 = 5657` | ✅ |

## 逐成员格式

### `name_table_0.dat`

- 来源：server_db.dat；载荷 2,951,784 B；SHA-256 `62b793469ec0aae6…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d dd c0 03 00`
- 结构：12 B 定长行 × 245,981
  - `+0` u16 `meta_a` — unresolved
  - `+2` u32 `string_ordinal` — row index == name_table_extra_<pool> record uid
  - `+6` u16 `meta_b` — unresolved (243 distinct, 0..249: nation-like)
  - `+8` u16 `meta_c` — unresolved (1..max: frequency/weight-like)
  - `+10` u16 `meta_d` — unresolved flag word (0xFF00-family + small codes)
- 闭合：`12 + 245981*12 = 2951784` → leftover 0 B
- 事实：`{"ordinal_equals_row_index": true, "meta_b_distinct": 243, "meta_b_max": 65535, "meta_c_max": 4817, "meta_d_distinct": 73, "string_join": "ordinal -> name_table_extra_0 uid"}`

前 10 条解码样本：

```json
[
 {
  "ordinal": 0,
  "meta_a": 65535,
  "meta_b": 65535,
  "meta_c": 1,
  "meta_d": 776,
  "meta_d_hex": "0x0308",
  "name": "Sabri"
 },
 {
  "ordinal": 1,
  "meta_a": 65535,
  "meta_b": 122,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Oldřich"
 },
 {
  "ordinal": 2,
  "meta_a": 65535,
  "meta_b": 123,
  "meta_c": 1,
  "meta_d": 0,
  "meta_d_hex": "0x0000",
  "name": "Miko"
 },
 {
  "ordinal": 3,
  "meta_a": 65535,
  "meta_b": 123,
  "meta_c": 1,
  "meta_d": 1792,
  "meta_d_hex": "0x0700",
  "name": "Lucas"
 },
 {
  "ordinal": 4,
  "meta_a": 65535,
  "meta_b": 123,
  "meta_c": 1,
  "meta_d": 8,
  "meta_d_hex": "0x0008",
  "name": "Jesper"
 },
 {
  "ordinal": 5,
  "meta_a": 65535,
  "meta_b": 123,
  "meta_c": 1,
  "meta_d": 264,
  "meta_d_hex": "0x0108",
  "name": "Ezequiel"
 },
 {
  "ordinal": 6,
  "meta_a": 65535,
  "meta_b": 124,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Mistake"
 },
 {
  "ordinal": 7,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 2,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Helmut"
 },
 {
  "ordinal": 8,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Fritz"
 },
 {
  "ordinal": 9,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Max"
 }
]
```

### `name_table_1.dat`

- 来源：server_db.dat；载荷 6,504,732 B；SHA-256 `2f7df4fd121eb18d…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d 6c 45 08 00`
- 结构：12 B 定长行 × 542,060
  - `+0` u16 `meta_a` — unresolved
  - `+2` u32 `string_ordinal` — row index == name_table_extra_<pool> record uid
  - `+6` u16 `meta_b` — unresolved (243 distinct, 0..249: nation-like)
  - `+8` u16 `meta_c` — unresolved (1..max: frequency/weight-like)
  - `+10` u16 `meta_d` — unresolved flag word (0xFF00-family + small codes)
- 闭合：`12 + 542060*12 = 6504732` → leftover 0 B
- 事实：`{"ordinal_equals_row_index": true, "meta_b_distinct": 243, "meta_b_max": 65535, "meta_c_max": 1891, "meta_d_distinct": 64, "string_join": "ordinal -> name_table_extra_1 uid"}`

前 10 条解码样本：

```json
[
 {
  "ordinal": 0,
  "meta_a": 65535,
  "meta_b": 65535,
  "meta_c": 1,
  "meta_d": 776,
  "meta_d_hex": "0x0308",
  "name": "Ramadhan"
 },
 {
  "ordinal": 1,
  "meta_a": 65535,
  "meta_b": 122,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Nejedlý"
 },
 {
  "ordinal": 2,
  "meta_a": 65535,
  "meta_b": 124,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Mistakesson"
 },
 {
  "ordinal": 3,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Walter"
 },
 {
  "ordinal": 4,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Morlock"
 },
 {
  "ordinal": 5,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Rahn"
 },
 {
  "ordinal": 6,
  "meta_a": 65535,
  "meta_b": 125,
  "meta_c": 1,
  "meta_d": 65288,
  "meta_d_hex": "0xff08",
  "name": "Haller"
 },
 {
  "ordinal": 7,
  "meta_a": 65535,
  "meta_b": 198,
  "meta_c": 15,
  "meta_d": 1024,
  "meta_d_hex": "0x0400",
  "name": "Kumar"
 },
 {
  "ordinal": 8,
  "meta_a": 65535,
  "meta_b": 198,
  "meta_c": 13,
  "meta_d": 1024,
  "meta_d_hex": "0x0400",
  "name": "Saravanan"
 },
 {
  "ordinal": 9,
  "meta_a": 65535,
  "meta_b": 198,
  "meta_c": 8,
  "meta_d": 1024,
  "meta_d_hex": "0x0400",
  "name": "Ganesan"
 }
]
```

### `name_table_2.dat`

- 来源：server_db.dat；载荷 1,028,028 B；SHA-256 `636ee1bb393ac046…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d a4 4e 01 00`
- 结构：12 B 定长行 × 85,668
  - `+0` u16 `meta_a` — unresolved
  - `+2` u32 `string_ordinal` — row index == name_table_extra_<pool> record uid
  - `+6` u16 `meta_b` — unresolved (243 distinct, 0..249: nation-like)
  - `+8` u16 `meta_c` — unresolved (1..max: frequency/weight-like)
  - `+10` u16 `meta_d` — unresolved flag word (0xFF00-family + small codes)
- 闭合：`12 + 85668*12 = 1028028` → leftover 0 B
- 事实：`{"ordinal_equals_row_index": true, "meta_b_distinct": 190, "meta_b_max": 244, "meta_c_max": 237, "meta_d_distinct": 7, "string_join": "ordinal -> name_table_extra_2 uid"}`

前 10 条解码样本：

```json
[
 {
  "ordinal": 0,
  "meta_a": 65535,
  "meta_b": 92,
  "meta_c": 1,
  "meta_d": 65280,
  "meta_d_hex": "0xff00",
  "name": "DJ Buffonge"
 },
 {
  "ordinal": 1,
  "meta_a": 65535,
  "meta_b": 93,
  "meta_c": 1,
  "meta_d": 65280,
  "meta_d_hex": "0xff00",
  "name": "Steven Rua"
 },
 {
  "ordinal": 2,
  "meta_a": 65535,
  "meta_b": 96,
  "meta_c": 1,
  "meta_d": 65280,
  "meta_d_hex": "0xff00",
  "name": "Tre' Ming"
 },
 {
  "ordinal": 3,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 15,
  "meta_d": 65408,
  "meta_d_hex": "0xff80",
  "name": "Juanito"
 },
 {
  "ordinal": 4,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 10,
  "meta_d": 65408,
  "meta_d_hex": "0xff80",
  "name": "Lucho"
 },
 {
  "ordinal": 5,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 10,
  "meta_d": 65408,
  "meta_d_hex": "0xff80",
  "name": "Leo"
 },
 {
  "ordinal": 6,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 10,
  "meta_d": 65408,
  "meta_d_hex": "0xff80",
  "name": "Cundo"
 },
 {
  "ordinal": 7,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 10,
  "meta_d": 65408,
  "meta_d_hex": "0xff80",
  "name": "Villo"
 },
 {
  "ordinal": 8,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 1,
  "meta_d": 65280,
  "meta_d_hex": "0xff00",
  "name": "Emilio Paisan"
 },
 {
  "ordinal": 9,
  "meta_a": 65535,
  "meta_b": 100,
  "meta_c": 1,
  "meta_d": 65280,
  "meta_d_hex": "0xff00",
  "name": "Daniel Luis"
 }
]
```

### `name_table_extra_0.dat`

- 来源：server_db.dat；载荷 3,837,439 B；SHA-256 `fe25bc10d8bb230a…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d dd c0 03 00`
- 结构：variable_stride，245,981 条记录
  - `+0` u32 `string_uid` — pool-local zero-based ordinal, pairs 1:1 with name_table_<pool> row index
  - `+4` u32 `byte_len`
  - `+8` utf8 `text`
- 闭合：`12 + sum(8+len) = 3837439` → leftover 0 B
- 事实：`{"uid_equals_row_index": true, "max_byte_len": 30, "ascii_only_rows": 224254}`

前 10 条解码样本：

```json
[
 {
  "uid": 0,
  "byte_len": 5,
  "text": "Sabri"
 },
 {
  "uid": 1,
  "byte_len": 8,
  "text": "Oldřich"
 },
 {
  "uid": 2,
  "byte_len": 4,
  "text": "Miko"
 },
 {
  "uid": 3,
  "byte_len": 5,
  "text": "Lucas"
 },
 {
  "uid": 4,
  "byte_len": 6,
  "text": "Jesper"
 },
 {
  "uid": 5,
  "byte_len": 8,
  "text": "Ezequiel"
 },
 {
  "uid": 6,
  "byte_len": 7,
  "text": "Mistake"
 },
 {
  "uid": 7,
  "byte_len": 6,
  "text": "Helmut"
 },
 {
  "uid": 8,
  "byte_len": 5,
  "text": "Fritz"
 },
 {
  "uid": 9,
  "byte_len": 3,
  "text": "Max"
 }
]
```

### `name_table_extra_1.dat`

- 来源：server_db.dat；载荷 8,713,837 B；SHA-256 `30d41d937d060ab1…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d 6c 45 08 00`
- 结构：variable_stride，542,060 条记录
  - `+0` u32 `string_uid` — pool-local zero-based ordinal, pairs 1:1 with name_table_<pool> row index
  - `+4` u32 `byte_len`
  - `+8` utf8 `text`
- 闭合：`12 + sum(8+len) = 8713837` → leftover 0 B
- 事实：`{"uid_equals_row_index": true, "max_byte_len": 44, "ascii_only_rows": 470488}`

前 10 条解码样本：

```json
[
 {
  "uid": 0,
  "byte_len": 8,
  "text": "Ramadhan"
 },
 {
  "uid": 1,
  "byte_len": 8,
  "text": "Nejedlý"
 },
 {
  "uid": 2,
  "byte_len": 11,
  "text": "Mistakesson"
 },
 {
  "uid": 3,
  "byte_len": 6,
  "text": "Walter"
 },
 {
  "uid": 4,
  "byte_len": 7,
  "text": "Morlock"
 },
 {
  "uid": 5,
  "byte_len": 4,
  "text": "Rahn"
 },
 {
  "uid": 6,
  "byte_len": 6,
  "text": "Haller"
 },
 {
  "uid": 7,
  "byte_len": 5,
  "text": "Kumar"
 },
 {
  "uid": 8,
  "byte_len": 9,
  "text": "Saravanan"
 },
 {
  "uid": 9,
  "byte_len": 7,
  "text": "Ganesan"
 }
]
```

### `name_table_extra_2.dat`

- 来源：server_db.dat；载荷 1,636,017 B；SHA-256 `67457d2fee9e385b…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d a4 4e 01 00`
- 结构：variable_stride，85,668 条记录
  - `+0` u32 `string_uid` — pool-local zero-based ordinal, pairs 1:1 with name_table_<pool> row index
  - `+4` u32 `byte_len`
  - `+8` utf8 `text`
- 闭合：`12 + sum(8+len) = 1636017` → leftover 0 B
- 事实：`{"uid_equals_row_index": true, "max_byte_len": 38, "ascii_only_rows": 75004}`

前 10 条解码样本：

```json
[
 {
  "uid": 0,
  "byte_len": 11,
  "text": "DJ Buffonge"
 },
 {
  "uid": 1,
  "byte_len": 10,
  "text": "Steven Rua"
 },
 {
  "uid": 2,
  "byte_len": 9,
  "text": "Tre' Ming"
 },
 {
  "uid": 3,
  "byte_len": 7,
  "text": "Juanito"
 },
 {
  "uid": 4,
  "byte_len": 5,
  "text": "Lucho"
 },
 {
  "uid": 5,
  "byte_len": 3,
  "text": "Leo"
 },
 {
  "uid": 6,
  "byte_len": 5,
  "text": "Cundo"
 },
 {
  "uid": 7,
  "byte_len": 5,
  "text": "Villo"
 },
 {
  "uid": 8,
  "byte_len": 13,
  "text": "Emilio Paisan"
 },
 {
  "uid": 9,
  "byte_len": 11,
  "text": "Daniel Luis"
 }
]
```

### `common_name_links.dat`

- 来源：server_db.dat；载荷 120,572 B；SHA-256 `5af63c436d587fd7…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d 18 2f 00 00`
- 结构：10 B 定长行 × 12,056
  - `+0` u32 `name_ordinal` — ordinal into the three name pools; 0xFFFFFFFF = no name
  - `+4` u8 `flag` — 0/1
  - `+5` u8 `opaque_b5` — unresolved (256 distinct)
  - `+6` u16 `nation` — nation code, 0..max
  - `+8` u16 `lang_x256` — language code shifted left 8 (low byte always 0)
- 闭合：`12 + 12056*10 = 120572` → leftover 0 B
- 事实：`{"sentinel_rows": 279, "flag_distinct": [0, 1], "nation_max": 308, "nation_distinct": 64, "lang_distinct": 94}`

前 10 条解码样本：

```json
[
 {
  "row": 0,
  "name_ordinal": 176147,
  "name_ordinal_raw": 176147,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 51,
  "nation": 198,
  "lang_code": 10
 },
 {
  "row": 1,
  "name_ordinal": 226835,
  "name_ordinal_raw": 226835,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 138,
  "nation": 290,
  "lang_code": 10
 },
 {
  "row": 2,
  "name_ordinal": 226864,
  "name_ordinal_raw": 226864,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 214,
  "nation": 290,
  "lang_code": 10
 },
 {
  "row": 3,
  "name_ordinal": 175901,
  "name_ordinal_raw": 175901,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 21,
  "nation": 197,
  "lang_code": 10
 },
 {
  "row": 4,
  "name_ordinal": 176161,
  "name_ordinal_raw": 176161,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 202,
  "nation": 197,
  "lang_code": 10
 },
 {
  "row": 5,
  "name_ordinal": 175764,
  "name_ordinal_raw": 175764,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 113,
  "nation": 195,
  "lang_code": 10
 },
 {
  "row": 6,
  "name_ordinal": 226840,
  "name_ordinal_raw": 226840,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 146,
  "nation": 290,
  "lang_code": 10
 },
 {
  "row": 7,
  "name_ordinal": 183253,
  "name_ordinal_raw": 183253,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 6,
  "nation": 198,
  "lang_code": 10
 },
 {
  "row": 8,
  "name_ordinal": 177865,
  "name_ordinal_raw": 177865,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 113,
  "nation": 195,
  "lang_code": 10
 },
 {
  "row": 9,
  "name_ordinal": 183180,
  "name_ordinal_raw": 183180,
  "is_sentinel": false,
  "flag": 1,
  "opaque_b5": 3,
  "nation": 197,
  "lang_code": 10
 }
]
```

### `club_links.dat`

- 来源：server_db.dat；载荷 435,279 B；SHA-256 `8933328064b13a9d…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d 2d 24 00 00`
- 结构：47 B 定长行 × 9,261
  - `+0` u32 `club_uid` — club identity, all < 300000
  - `+4` bytes `opaque_a`
  - `+9` u32 `linked_uid` — linked club identity, all < 300000
  - `+13` bytes `wire_subobject` — fixed-shape sub-object carrying repeated marker 0x076c0001
- 闭合：`12 + 9261*47 = 435279` → leftover 0 B
- 事实：`{"club_uid_max": 83927, "linked_uid_max": 84247, "rows_with_equal_uids": 0, "constant_byte_positions": 23}`

前 10 条解码样本：

```json
[
 {
  "row": 0,
  "club_uid": 1270,
  "linked_uid": 11272,
  "mid_bytes": "04 e2 01 80 04",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 1,
  "club_uid": 1250,
  "linked_uid": 11288,
  "mid_bytes": "04 e2 c7 89 01",
  "tail_const_prefix": "b6 00 aa 07 01 00 6c 07"
 },
 {
  "row": 2,
  "club_uid": 1251,
  "linked_uid": 15901,
  "mid_bytes": "04 e2 01 80 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 3,
  "club_uid": 1234,
  "linked_uid": 13218,
  "mid_bytes": "10 34 48 08 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 4,
  "club_uid": 1405,
  "linked_uid": 3711,
  "mid_bytes": "03 6c 06 00 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 5,
  "club_uid": 9601,
  "linked_uid": 11157,
  "mid_bytes": "10 00 00 00 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 6,
  "club_uid": 4182,
  "linked_uid": 14883,
  "mid_bytes": "18 f6 c7 00 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 7,
  "club_uid": 1269,
  "linked_uid": 1255,
  "mid_bytes": "04 e2 01 80 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 8,
  "club_uid": 3126,
  "linked_uid": 8579,
  "mid_bytes": "04 e2 c1 89 00",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 },
 {
  "row": 9,
  "club_uid": 1282,
  "linked_uid": 1257,
  "mid_bytes": "04 e2 81 80 13",
  "tail_const_prefix": "01 00 6c 07 01 00 6c 07"
 }
]
```

### `simple_vars.dat`

- 来源：server_db.dat；载荷 82,385 B；SHA-256 `5f704d400f865935…`
- 头（34 B）：`03 01 74 61 64 2e f1 0d 00 00 08 00 00 00 f1 0d 04 00 00 00 32 34 33 30 4b 32 e8 07 97 94 04 00 e7 07`
- 结构：variable_stride，28,552 条记录
  - `+0` u8 `key` — opaque variable id; 169 of 256 codes used
  - `+1` u8 `len`
  - `+2` bytes `value`
- 文法：unique closing grammar: among all (key,width) x (len,width) x (unit 1/2/4) x base 34..38 variants, only base=34,key=1,len=1,unit=1 consumes the payload exactly; key/length semantics remain unresolved
- 闭合：`34 + sum(2+len) = 82385` → leftover 0 B
- 事实：`{"distinct_keys": 169, "zero_length_records": 26630, "key_histogram_top": [[0, 24942], [1, 1565], [2, 243], [4, 234], [255, 229], [3, 196], [6, 132], [8, 120], [10, 104], [5, 99]]}`

前 10 条解码样本：

```json
[
 {
  "record": 0,
  "offset": 34,
  "key": 114,
  "len": 28,
  "value_hex": "01 00 6c 07 00 00 00 00 00 00 00 00 01 0f 01 01",
  "value_ascii": "..l............."
 },
 {
  "record": 1,
  "offset": 64,
  "key": 0,
  "len": 0,
  "value_hex": "",
  "value_ascii": ""
 },
 {
  "record": 2,
  "offset": 66,
  "key": 0,
  "len": 0,
  "value_hex": "",
  "value_ascii": ""
 },
 {
  "record": 3,
  "offset": 68,
  "key": 0,
  "len": 0,
  "value_hex": "",
  "value_ascii": ""
 },
 {
  "record": 4,
  "offset": 70,
  "key": 1,
  "len": 0,
  "value_hex": "",
  "value_ascii": ""
 },
 {
  "record": 5,
  "offset": 72,
  "key": 0,
  "len": 0,
  "value_hex": "",
  "value_ascii": ""
 },
 {
  "record": 6,
  "offset": 74,
  "key": 3,
  "len": 0,
  "value_hex": "",
  "value_ascii": ""
 },
 {
  "record": 7,
  "offset": 76,
  "key": 0,
  "len": 1,
  "value_hex": "08",
  "value_ascii": "."
 },
 {
  "record": 8,
  "offset": 79,
  "key": 6,
  "len": 6,
  "value_hex": "05 05 03 03 0a 04",
  "value_ascii": "......"
 },
 {
  "record": 9,
  "offset": 87,
  "key": 5,
  "len": 8,
  "value_hex": "01 01 00 00 00 00 02 01",
  "value_ascii": "........"
 }
]
```

### `summary.dat`

- 来源：summary.dat (standalone tad file)；载荷 1,648,018 B；SHA-256 `966eea20bf8d261c…`
- 头（40 B）：`03 01 74 61 64 2e f1 0d 07 00 00 00 01 00 00 00 02 00 00 00 03 00 00 00 04 00 00 00 05 00 00 00 06 00 00 00 07 00 00 00`
- 结构：separator_framed，54,087 条记录
  - `+0` u32 `lead_u32` — body lead word; dominant 17B bodies lead with a small u32 id
  - `+4` bytes `body_payload`
- footer（4 B）：`ff ff ff ff`
- 尾块：11,004 B = 12 B 前缀 + 2,621 × u32 + 63 × (u32,f32) + 4 B 终止符；`ff ff ff ff`
- 闭合：`40 + sum(body+5) [1637014] + tail 11004 = 1648018` → leftover 0 B
- 事实：`{"separator_count": 54087, "body_size_top": [[17, 53742], [28, 92], [41, 7], [1019, 7], [161, 5]], "dominant_body_len": 17, "trailing_words": 2621, "trailing_pairs": 63, "trailing_asc_runs": [2488, 126]}`

前 10 条解码样本：

```json
[
 {
  "record": 0,
  "offset": 40,
  "byte_len": 33,
  "lead_u32": 251,
  "hex_head": "fb 00 00 00 03 00 00 00 00 05 00 00 00 65 02 00 00 01 00 00"
 },
 {
  "record": 1,
  "offset": 78,
  "byte_len": 17,
  "lead_u32": 134637,
  "hex_head": "ed 0d 02 00 02 04 03 0b 0b 03 06 02 ff 7f ff 7f 00"
 },
 {
  "record": 2,
  "offset": 100,
  "byte_len": 17,
  "lead_u32": 529013,
  "hex_head": "75 12 08 00 01 04 22 0c 0d 03 00 70 ff 7f ff 7f 00"
 },
 {
  "record": 3,
  "offset": 122,
  "byte_len": 17,
  "lead_u32": 5340068,
  "hex_head": "a4 7b 51 00 02 04 34 0b 0c 03 06 02 00 70 ff 7f 00"
 },
 {
  "record": 4,
  "offset": 144,
  "byte_len": 17,
  "lead_u32": 5340069,
  "hex_head": "a5 7b 51 00 01 04 03 0b 0c 03 21 04 ff 7f 00 70 00"
 },
 {
  "record": 5,
  "offset": 166,
  "byte_len": 17,
  "lead_u32": 5340070,
  "hex_head": "a6 7b 51 00 02 04 0b 0b 0c 03 5a 01 00 70 00 70 00"
 },
 {
  "record": 6,
  "offset": 188,
  "byte_len": 17,
  "lead_u32": 5340071,
  "hex_head": "a7 7b 51 00 01 04 01 0d 0e 03 21 04 28 43 28 43 00"
 },
 {
  "record": 7,
  "offset": 210,
  "byte_len": 17,
  "lead_u32": 5340072,
  "hex_head": "a8 7b 51 00 01 04 32 0d 0e 03 c0 7f 06 02 06 02 00"
 },
 {
  "record": 8,
  "offset": 232,
  "byte_len": 17,
  "lead_u32": 5340073,
  "hex_head": "a9 7b 51 00 01 04 04 0e 0f 03 27 06 ff 7f 00 70 00"
 },
 {
  "record": 9,
  "offset": 254,
  "byte_len": 17,
  "lead_u32": 5340074,
  "hex_head": "aa 7b 51 00 02 04 24 0c 0d 03 ff 7f 5a 01 5a 01 00"
 }
]
```

### `table_for_old_save_23.dat`

- 来源：server_db.dat；载荷 3,914 B；SHA-256 `e3d1c1df7bf3f866…`
- 头（15 B）：`03 01 74 61 64 2e f1 0d 16 01 00 00 00 00 00`
- 结构：14 B 定长行 × 278
  - `+0` u32 `ordinal` — equals row index
  - `+4` u32 `uid_a`
  - `+8` u32 `uid_b` — always == uid_a
  - `+12` u16 `flag` — always 0
- footer（7 B）：`00 00 01 94 5b 3a 77`
- 闭合：`15 + 278*14 + 7 = 3914` → leftover 0 B
- 事实：`{"ordinal_equals_row_index": true, "rows_with_equal_uids": 278, "rows_with_zero_flag": 278}`

前 10 条解码样本：

```json
[
 {
  "row": 0,
  "ordinal": 0,
  "uid_a": 1,
  "uid_b": 1,
  "flag_u16": 0
 },
 {
  "row": 1,
  "ordinal": 1,
  "uid_a": 2,
  "uid_b": 2,
  "flag_u16": 0
 },
 {
  "row": 2,
  "ordinal": 2,
  "uid_a": 3,
  "uid_b": 3,
  "flag_u16": 0
 },
 {
  "row": 3,
  "ordinal": 3,
  "uid_a": 4,
  "uid_b": 4,
  "flag_u16": 0
 },
 {
  "row": 4,
  "ordinal": 4,
  "uid_a": 5,
  "uid_b": 5,
  "flag_u16": 0
 },
 {
  "row": 5,
  "ordinal": 5,
  "uid_a": 6,
  "uid_b": 6,
  "flag_u16": 0
 },
 {
  "row": 6,
  "ordinal": 6,
  "uid_a": 7,
  "uid_b": 7,
  "flag_u16": 0
 },
 {
  "row": 7,
  "ordinal": 7,
  "uid_a": 8,
  "uid_b": 8,
  "flag_u16": 0
 },
 {
  "row": 8,
  "ordinal": 8,
  "uid_a": 9,
  "uid_b": 9,
  "flag_u16": 0
 },
 {
  "row": 9,
  "ordinal": 9,
  "uid_a": 10,
  "uid_b": 10,
  "flag_u16": 0
 }
]
```

### `table_for_old_save_25.dat`

- 来源：server_db.dat；载荷 1,464,951 B；SHA-256 `86f081ca60df38f2…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d 87 1b 00 00`
- 结构：variable_stride，7,047 条记录
  - `+0` bytes `body`
  - `+row_len-12` u32 `ordinal` — equals row index (row-frame witness)
  - `+row_len-8` u32 `uid_a`
  - `+row_len-4` u32 `uid_b` — always == uid_a
- footer（9 B）：`00 00 00 00 01 4e c4 3a 77`
- 闭合：`12 + sum(rowlen) [1464740] + 9 = 1464951` → leftover 0 B
- 事实：`{"unique_dp_path": true, "missing_ordinals": [], "row_len_min": 97, "row_len_max": 1634, "row_len_mode": 190, "identity_candidates_total": 76119}`

前 10 条解码样本：

```json
[
 {
  "row": 0,
  "start": 12,
  "byte_len": 97,
  "identity_offset": 97,
  "ordinal": 0,
  "uid_a": 4294967295,
  "uid_b": 4294967295
 },
 {
  "row": 1,
  "start": 109,
  "byte_len": 1634,
  "identity_offset": 1731,
  "ordinal": 1,
  "uid_a": 2,
  "uid_b": 2
 },
 {
  "row": 2,
  "start": 1743,
  "byte_len": 462,
  "identity_offset": 2193,
  "ordinal": 2,
  "uid_a": 3,
  "uid_b": 3
 },
 {
  "row": 3,
  "start": 2205,
  "byte_len": 462,
  "identity_offset": 2655,
  "ordinal": 3,
  "uid_a": 4,
  "uid_b": 4
 },
 {
  "row": 4,
  "start": 2667,
  "byte_len": 766,
  "identity_offset": 3421,
  "ordinal": 4,
  "uid_a": 6,
  "uid_b": 6
 },
 {
  "row": 5,
  "start": 3433,
  "byte_len": 751,
  "identity_offset": 4172,
  "ordinal": 5,
  "uid_a": 7,
  "uid_b": 7
 },
 {
  "row": 6,
  "start": 4184,
  "byte_len": 751,
  "identity_offset": 4923,
  "ordinal": 6,
  "uid_a": 8,
  "uid_b": 8
 },
 {
  "row": 7,
  "start": 4935,
  "byte_len": 345,
  "identity_offset": 5268,
  "ordinal": 7,
  "uid_a": 11,
  "uid_b": 11
 },
 {
  "row": 8,
  "start": 5280,
  "byte_len": 230,
  "identity_offset": 5498,
  "ordinal": 8,
  "uid_a": 12,
  "uid_b": 12
 },
 {
  "row": 9,
  "start": 5510,
  "byte_len": 205,
  "identity_offset": 5703,
  "ordinal": 9,
  "uid_a": 13,
  "uid_b": 13
 }
]
```

### `fantasy_draft_future_regens.dat`

- 来源：server_db.dat；载荷 5,657 B；SHA-256 `e62837b7bdbd1fe0…`
- 头（12 B）：`03 01 74 61 64 2e f1 0d 28 00 00 00`
- 结构：variable_stride，40 条记录
  - `+0` bytes `body` — starts with u32 len + utf8 stadium/club/person names
  - `+row_len-4` bytes `terminator`
- footer（31 B）：`10 ff ff 07 01 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff 9b 05 00 00 01 00 00`
- 行终止标记：`01 00 6c 07` × 40
- 闭合：`12 + sum(rowlen) [5614] + 31 = 5657` → leftover 0 B
- 事实：`{"header_count": 40, "markers_found": 40, "rows_derived": 40, "tail_len": 31}`

前 10 条解码样本：

```json
[
 {
  "row": 0,
  "start": 12,
  "byte_len": 99,
  "hex_head": "05 08 00 00 00 4b 75 64 73 6b 20 46 43 0d 00 00 00 4b 75 64 73 6b 20 53"
 },
 {
  "row": 1,
  "start": 111,
  "byte_len": 143,
  "name2": "\u0000",
  "hex_head": "10 ff ff 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 2,
  "start": 254,
  "byte_len": 145,
  "hex_head": "10 ff ff 07 01 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 3,
  "start": 399,
  "byte_len": 139,
  "hex_head": "10 ff ff 07 03 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 4,
  "start": 538,
  "byte_len": 140,
  "hex_head": "10 ff ff 0d 01 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 5,
  "start": 678,
  "byte_len": 147,
  "hex_head": "10 ff ff 10 03 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 6,
  "start": 825,
  "byte_len": 141,
  "hex_head": "10 ff ff 07 01 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 7,
  "start": 966,
  "byte_len": 136,
  "hex_head": "10 ff ff 0a 03 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 8,
  "start": 1102,
  "byte_len": 143,
  "hex_head": "10 ff ff 0d 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 },
 {
  "row": 9,
  "start": 1245,
  "byte_len": 134,
  "hex_head": "10 ff ff 10 01 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff"
 }
]
```

## 证据边界

- `simple_vars` 的 (u8 key, u8 len) 是**唯一能精确闭合**的定前缀文法；key/长度语义仍未定型，
  不把 key 当业务字段名，也不把 value 当已解类型。
- `name_table_*` 的 `meta_a` / `meta_b` / `meta_c` / `meta_d` 保留原始槽位语义（未命名）；
  `string_ordinal` 已证与同序 `name_table_extra_*` 的 uid 1:1。
- `club_links` 第 13..46 字节是定形 wire 子对象（含重复常量 `0x076c0001`），只列常量位置，不命名字段。
- `summary.dat` body 内部字段语义未解，只给分隔符框定与尾块结构；尾块中 2,621 个 u32 词含
  两段长升序 id 串（2,488 / 126 个），语义未定，不当作已解字段。
- `table_for_old_save_23` 尾为 7 B（非 9 B）；`table_for_old_save_25` 为 9 B footer；
  `fantasy_draft_future_regens` 为 31 B 尾块，无 9 B footer —— 各表 footer 宽度逐表自证，未互相照抄。
