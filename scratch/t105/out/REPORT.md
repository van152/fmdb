# t105 — 三大主表序列化器逐行审计(`CLUB` / `COMP` / `NATION` / `NATIONAL_TEAM_CONTAINER`)

机读产物:`big3_serializers.json`(`status=complete`,schema `t105.big3_serializers.v1`)。
输入:只读 `scratch/t95/funcs/*.c` + `scratch/t95/vtable_index.json`;未触碰 `reports/` 与 `LEDGER.json`。

## 1. 总览

| 序列化器 | VA | C 行数 | 读取步骤 | 定长 | 变长 | 门控步骤 | 栈临时 | 内联 span | 唯一目标偏移 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `CLUB::server` | `0x140e5b1a0` | 944 | 26 | 23 | 3 | 24 | 3 | 2 | 7 |
| `CLUB::client` | `0x140e5cf50` | 199 | 7 | 0 | 7 | 1 | 0 | 0 | 6 |
| `COMP::server` | `0x140eb7a00` | 550 | 4 | 0 | 4 | 4 | 0 | 0 | 3 |
| `COMP::client` | `0x140eb9000` | 89 | 11 | 0 | 11 | 4 | 0 | 0 | 7 |
| `NATION::server` | `0x1410404c0` | 676 | 43 | 40 | 3 | 28 | 12 | 0 | 8 |
| `NATION::client` | `0x143ecb900` | 109 | 17 | 0 | 17 | 13 | 0 | 0 | 4 |
| `NATIONAL_TEAM_CONTAINER::server` | `0x14105d510` | 1588 | 159 | 150 | 9 | 93 | 36 | 0 | 86 |
| `NATIONAL_TEAM_CONTAINER::client` | `0x143ef3bf0` | 82 | 7 | 0 | 7 | 3 | 0 | 0 | 3 |
| **合计** | 8 函数 | — | **274** | 213 | 61 | 170 | — | — | — |

## 2. 每个序列化器的读取构成

### `CLUB::server` — `funcs/140e5b1a0.c`(slot 19,944 行)

```c
__int64 __fastcall sub_140E5B1A0(__int64 a1, __int64 *a2, char a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
```

| read_kind | 次数 |
|---|---:|
| `stream_vcall_40` | 23 |
| `helper_call` | 2 |
| `base_class_call` | 1 |

宽度直方图:`4`×9, `1`×9, `2`×3, `varlen:0x140814b10`×2, `8`×1, `varlen:0x1411d1730`×1, `0`×1

版本门控:`ver>=0xdc4`×2

### `CLUB::client` — `funcs/140e5cf50.c`(slot 20,199 行)

```c
char __fastcall sub_140E5CF50(_QWORD *a1, char a2, __int64 a3, int a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 6 |
| `base_class_call` | 1 |

宽度直方图:`varlen:0x140f7ec80`×5, `varlen:0x140f7fd40`×1, `varlen:0x1411d2f80`×1

### `COMP::server` — `funcs/140eb7a00.c`(slot 19,550 行)

```c
__int64 __fastcall sub_140EB7A00( __int64 a1, __int64 **a2, __int64 a3, __int64 a4, int a5, char a6, __int64 a7, unsigned __int8 a8)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 4 |

宽度直方图:`varlen:0x140814b10`×2, `varlen:0x140eb8850`×1, `varlen:0x140839480`×1

### `COMP::client` — `funcs/140eb9000.c`(slot 20,89 行)

```c
char __fastcall sub_140EB9000(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 11 |

宽度直方图:`varlen:0x140f7ec80`×5, `varlen:0x140f7fe40`×4, `varlen:0x140f7f220`×1, `varlen:0x140f7ee40`×1

### `NATION::server` — `funcs/1410404c0.c`(slot 19,676 行)

```c
__int64 __fastcall sub_1410404C0(_QWORD *a1, _QWORD *a2, __int64 a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
```

| read_kind | 次数 |
|---|---:|
| `stream_vcall_40` | 39 |
| `base_class_call` | 2 |
| `loop_vector` | 1 |
| `helper_call` | 1 |

宽度直方图:`4`×31, `1`×6, `2`×3, `varlen:0x14104f0b0`×1, `varlen:0x141041a50`×1, `varlen:0x140faed40`×1

### `NATION::client` — `funcs/143ecb900.c`(slot 20,109 行)

```c
char __fastcall sub_143ECB900(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 17 |

宽度直方图:`varlen:0x140f7ec80`×7, `varlen:0x140f7f220`×3, `varlen:0x140f7fc40`×3, `varlen:0x140f80150`×3, `varlen:0x140f7f320`×1

### `NATIONAL_TEAM_CONTAINER::server` — `funcs/14105d510.c`(slot 19,1588 行)

```c
__int64 __fastcall sub_14105D510( __int64 a1, volatile signed __int32 **a2, __int64 a3, __int64 a4, int a5, unsigned int a6, char a7, __int64 a8)
```

| read_kind | 次数 |
|---|---:|
| `stream_vcall_40` | 125 |
| `loop_vector` | 29 |
| `helper_call` | 4 |
| `base_class_call` | 1 |

宽度直方图:`4`×66, `1`×63, `2`×21, `varlen:0x14105fa40`×2, `varlen:0x141073d90`×2, `varlen:0x140839290`×1, `varlen:0x140839480`×1, `varlen:0x14104f0b0`×1, `varlen:0x141074100`×1, `varlen:0x141041a50`×1

版本门控:`ver<=0xdc3`×33, `ver>=0xdc4`×26, `ver<0xdc4`×6

### `NATIONAL_TEAM_CONTAINER::client` — `funcs/143ef3bf0.c`(slot 20,82 行)

```c
char __fastcall sub_143EF3BF0(__int64 a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 3 |
| `loop_vector` | 3 |
| `base_class_call` | 1 |

宽度直方图:`varlen:0x140f7ec80`×3, `varlen:0x140f7ee40`×1, `varlen:0x140f7f730`×1, `varlen:0x140f80250`×1, `varlen:0x1411d2f80`×1

## 3. 版本门控总结

版本阈值的唯一来源是 `*(unsigned __int16 *)(a4 + 1416)`(下文记为 `dbver`):

| 门控 | 出现次数(步骤) | 语义 |
|---|---:|---|
| `ver<=0xdc3` | 33 | 旧版本(≤3523)专属字段/回填 |
| `ver>=0xdc4` | 28 | 3569+ 新版本专属字段(旧档不读) |
| `ver<0xdc4` | 6 | 旧版本专属 |

## 4. `needed_helpers` — 下一轮 IDA 补反编译清单(Top 30)

本轮共记录 22 个被调用的 helper;其中 **19 个在 `scratch/t95/funcs/` 中没有反编译体**。

| # | helper VA | 调用次数 | 角色推断 | 有反编译 | 调用方 |
|---:|---|---:|---|---|---|
| 1 | `0x140f7ec80` | 20 | stream_read_descriptor | **no** | CLUB::client, COMP::client, NATION::client, NATIONAL_TEAM_CONTAINER::client |
| 2 | `0x140814b10` | 4 | stream_read_helper | **no** | CLUB::server, COMP::server |
| 3 | `0x140f7f220` | 4 | stream_read_descriptor | **no** | COMP::client, NATION::client |
| 4 | `0x140f7fe40` | 4 | stream_read_descriptor | **no** | COMP::client |
| 5 | `0x140f7fc40` | 3 | stream_read_descriptor | **no** | NATION::client |
| 6 | `0x140f80150` | 3 | stream_read_helper | **no** | NATION::client |
| 7 | `0x1411d2f80` | 2 | class_helper | yes | CLUB::client, NATIONAL_TEAM_CONTAINER::client |
| 8 | `0x140839480` | 2 | stream_read_helper | **no** | COMP::server, NATIONAL_TEAM_CONTAINER::server |
| 9 | `0x140f7ee40` | 2 | stream_read_descriptor | **no** | COMP::client, NATIONAL_TEAM_CONTAINER::client |
| 10 | `0x14104f0b0` | 2 | stream_read_helper | **no** | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 11 | `0x141041a50` | 2 | post_read_fixup | **no** | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 12 | `0x14105fa40` | 2 | value_reader | **no** | NATIONAL_TEAM_CONTAINER::server |
| 13 | `0x141073d90` | 2 | stream_read_helper | **no** | NATIONAL_TEAM_CONTAINER::server |
| 14 | `0x1411d1730` | 1 | class_helper | yes | CLUB::server |
| 15 | `0x140f7fd40` | 1 | stream_read_descriptor | **no** | CLUB::client |
| 16 | `0x140eb8850` | 1 | subobject_reader | **no** | COMP::server |
| 17 | `0x140faed40` | 1 | stream_read_helper | yes | NATION::server |
| 18 | `0x140f7f320` | 1 | stream_read_descriptor | **no** | NATION::client |
| 19 | `0x140839290` | 1 | stream_read_helper | **no** | NATIONAL_TEAM_CONTAINER::server |
| 20 | `0x141074100` | 1 | stream_read_helper | **no** | NATIONAL_TEAM_CONTAINER::server |
| 21 | `0x140f7f730` | 1 | stream_read_descriptor | **no** | NATIONAL_TEAM_CONTAINER::client |
| 22 | `0x140f80250` | 1 | stream_read_helper | **no** | NATIONAL_TEAM_CONTAINER::client |

### 已确认的读取 helper 家族(`varlen` 宽度来源)

| helper | 反编译体 | 语义 |
|---|---|---|
| `0x140f7ec80` | `sub_143d5e790` | 引用字段读取+按 descriptor(第 3 参)解引用 |
| `0x140f7f220` | `sub_143d60090` | 引用字段读取,descriptor @ stream+0x20 |
| `0x140f7f320` | `sub_143d60660` | 引用字段读取,descriptor @ stream+0x30 |
| `0x140f7f730` | `sub_143d61490` | 引用字段读取,descriptor @ stream+0x58 |
| `0x140f7fc40` | `sub_143d61720` | 引用字段读取,descriptor @ stream+0x78 |
| `0x140f7fd40` | `sub_143d624c0` | 引用字段读取(可选),descriptor @ stream+0x80 |
| `0x140f7fe40` | `sub_143d626c0` | 引用字段读取,descriptor @ stream+0x90 |
| `0x140f80150` | `sub_143d64710` | 引用字段读取,descriptor @ stream+0xb8 |
| `0x140f80250` | `sub_143d64820` | 可空引用字段读取,descriptor @ stream+0xc0 |
| `0x140f7ee40` | `sub_143d5ea60` | 引用字段读取(带 type==17 判定) |

## 5. 方法学与口径

- `wire_width` 定长值只来自 vtable slot 40 调用的第 3 个实参(`literal_arg3`);
  走 descriptor 的 helper 一律记 `varlen:<helper_va>`,不用猜测值填充。
- 引擎在 `CLUB::read_server` 里把相邻小字段**合并成一次 span 读**(`v123/v124/v125` 三元组 +
  `(stream, dest)` 双参 flush 调用);这类步骤标 `coalesced_span=true`,宽度取 pending 变量。
- 栈临时变量(`stack:vNN`)额外做一次具化追踪:`materialized_to` 给出随后写入的成员偏移
  (`assign` / `setter:<va>` / `vector_count`),用来把计数读与真正的容器成员对齐。
- `loop_vector` = 该读取步骤位于循环体内(向量元素读);`loop_guard` 给出循环条件。
- 偏移换算:`a1` 为 `_QWORD *` 时 `a1 + N` 记 `N*8`;带 `(_DWORD)` 强转的按字节;
  `*(_QWORD *)(a1 + N) + M` 记 `0xN->0xM`(二级间接)。

