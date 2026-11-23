# t105 — 三大主表序列化器逐行审计(`CLUB` / `COMP` / `NATION` / `NATIONAL_TEAM_CONTAINER`)

机读产物:`big3_serializers.json`(`status=complete`,schema `t105.big3_serializers.v1`)。
输入:只读 `scratch/t95/funcs/*.c` + `scratch/t95/vtable_index.json`;未触碰 `reports/` 与 `LEDGER.json`。

## 1. 总览

| 序列化器 | VA | C 行数 | 读取步骤 | 定长 | 变长 | 门控步骤 | 栈临时 | 内联 span | 唯一目标偏移 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `CLUB::server` | `0x140e5b1a0` | 944 | 4 | 0 | 4 | 2 | 0 | 0 | 2 |
| `CLUB::client` | `0x140e5cf50` | 199 | 7 | 0 | 7 | 1 | 0 | 0 | 6 |
| `COMP::server` | `0x140eb7a00` | 550 | 13 | 0 | 13 | 11 | 1 | 0 | 3 |
| `COMP::client` | `0x140eb9000` | 89 | 13 | 0 | 13 | 5 | 0 | 0 | 7 |
| `NATION::server` | `0x1410404c0` | 676 | 8 | 0 | 8 | 6 | 1 | 0 | 0 |
| `NATION::client` | `0x143ecb900` | 109 | 18 | 0 | 18 | 13 | 0 | 0 | 4 |
| `NATIONAL_TEAM_CONTAINER::server` | `0x14105d510` | 1588 | 20 | 0 | 20 | 20 | 1 | 0 | 7 |
| `NATIONAL_TEAM_CONTAINER::client` | `0x143ef3bf0` | 82 | 10 | 0 | 10 | 3 | 0 | 0 | 3 |
| **合计** | 8 函数 | — | **93** | 0 | 93 | 61 | — | — | — |

## 2. 每个序列化器的读取构成

### `CLUB::server` — `funcs/140e5b1a0.c`(slot 19,944 行)

```c
__int64 __fastcall sub_140E5B1A0(__int64 a1, __int64 *a2, char a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 3 |
| `base_class_call` | 1 |

宽度直方图:`varlen:0x140814b10`×2, `varlen:0x1412e70a0`×1, `varlen:0x1411d1730`×1

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
| `helper_call` | 13 |

宽度直方图:`varlen:0x140814b10`×2, `varlen:0x140eb5f80`×2, `varlen:0x140db8980`×2, `varlen:0x140eb8850`×1, `varlen:0x1409fa4b0`×1, `varlen:0x140839480`×1, `varlen:0x1409f8630`×1, `varlen:0x14155be50`×1, `varlen:0x14155d840`×1, `varlen:0x14155e830`×1

### `COMP::client` — `funcs/140eb9000.c`(slot 20,89 行)

```c
char __fastcall sub_140EB9000(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 13 |

宽度直方图:`varlen:0x140f7ec80`×6, `varlen:0x140f7fe40`×4, `varlen:0x140f7ee40`×2, `varlen:0x140f7f220`×1

### `NATION::server` — `funcs/1410404c0.c`(slot 19,676 行)

```c
__int64 __fastcall sub_1410404C0(_QWORD *a1, _QWORD *a2, __int64 a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 5 |
| `base_class_call` | 2 |
| `loop_vector` | 1 |

宽度直方图:`varlen:0x1415cfea0`×2, `varlen:0x1415cfd70`×1, `varlen:0x14104f0b0`×1, `varlen:0x141060550`×1, `varlen:0x1410605b0`×1, `varlen:0x141041a50`×1, `varlen:0x140faed40`×1

### `NATION::client` — `funcs/143ecb900.c`(slot 20,109 行)

```c
char __fastcall sub_143ECB900(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 18 |

宽度直方图:`varlen:0x140f7ec80`×7, `varlen:0x140f7f220`×3, `varlen:0x140f7fc40`×3, `varlen:0x140f80150`×3, `varlen:0x140f7f320`×1, `varlen:0x140f7fd40`×1

### `NATIONAL_TEAM_CONTAINER::server` — `funcs/14105d510.c`(slot 19,1588 行)

```c
__int64 __fastcall sub_14105D510( __int64 a1, volatile signed __int32 **a2, __int64 a3, __int64 a4, int a5, unsigned int a6, char a7, __int64 a8)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 10 |
| `loop_vector` | 9 |
| `base_class_call` | 1 |

宽度直方图:`varlen:0x14105fa40`×2, `varlen:0x141571860`×2, `varlen:0x141073d90`×2, `varlen:0x14141d570`×2, `varlen:0x1415cfea0`×2, `varlen:0x140839290`×1, `varlen:0x140839480`×1, `varlen:0x1415cfd70`×1, `varlen:0x141060130`×1, `varlen:0x14104f0b0`×1, `varlen:0x141074100`×1, `varlen:0x14155be50`×1, `varlen:0x14141d4a0`×1, `varlen:0x1410605b0`×1, `varlen:0x141041a50`×1

版本门控:`ver>=0xdc4`×9, `ver<=0xdc3`×4, `ver<0xdc4`×1

### `NATIONAL_TEAM_CONTAINER::client` — `funcs/143ef3bf0.c`(slot 20,82 行)

```c
char __fastcall sub_143EF3BF0(__int64 a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
```

| read_kind | 次数 |
|---|---:|
| `helper_call` | 6 |
| `loop_vector` | 3 |
| `base_class_call` | 1 |

宽度直方图:`varlen:0x140f7ec80`×3, `varlen:0x140f7ee40`×1, `varlen:0x140f7f730`×1, `varlen:0x140f7f930`×1, `varlen:0x140f7fc40`×1, `varlen:0x140f7f220`×1, `varlen:0x140f80250`×1, `varlen:0x1411d2f80`×1

## 3. 版本门控总结

版本阈值的唯一来源是 `*(unsigned __int16 *)(a4 + 1416)`(下文记为 `dbver`):

| 门控 | 出现次数(步骤) | 语义 |
|---|---:|---|
| `ver>=0xdc4` | 11 | 3569+ 新版本专属字段(旧档不读) |
| `ver<=0xdc3` | 4 | 旧版本(≤3523)专属字段/回填 |
| `ver<0xdc4` | 1 | 旧版本专属 |

## 4. `needed_helpers` — 下一轮 IDA 补反编译清单(Top 30)

本轮共记录 39 个被调用的 helper;其中 **17 个在 `scratch/t95/funcs/` 中没有反编译体**。

| # | helper VA | 调用次数 | 角色推断 | 有反编译 | 调用方 |
|---:|---|---:|---|---|---|
| 1 | `0x140f7ec80` | 21 | stream_read_descriptor | yes | CLUB::client, COMP::client, NATION::client, NATIONAL_TEAM_CONTAINER::client |
| 2 | `0x140f7f220` | 5 | stream_read_descriptor | yes | COMP::client, NATION::client, NATIONAL_TEAM_CONTAINER::client |
| 3 | `0x140814b10` | 4 | stream_read_helper | yes | CLUB::server, COMP::server |
| 4 | `0x140f7fe40` | 4 | stream_read_descriptor | yes | COMP::client |
| 5 | `0x1415cfea0` | 4 | subobject_reader | **no** | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 6 | `0x140f7fc40` | 4 | stream_read_descriptor | yes | NATION::client, NATIONAL_TEAM_CONTAINER::client |
| 7 | `0x140f7ee40` | 3 | stream_read_descriptor | yes | COMP::client, NATIONAL_TEAM_CONTAINER::client |
| 8 | `0x140f80150` | 3 | stream_read_helper | yes | NATION::client |
| 9 | `0x140f7fd40` | 2 | stream_read_descriptor | yes | CLUB::client, NATION::client |
| 10 | `0x1411d2f80` | 2 | class_helper | yes | CLUB::client, NATIONAL_TEAM_CONTAINER::client |
| 11 | `0x140839480` | 2 | stream_read_helper | yes | COMP::server, NATIONAL_TEAM_CONTAINER::server |
| 12 | `0x14155be50` | 2 | subobject_reader | **no** | COMP::server, NATIONAL_TEAM_CONTAINER::server |
| 13 | `0x140eb5f80` | 2 | subobject_reader | **no** | COMP::server |
| 14 | `0x140db8980` | 2 | stream_read_ref | **no** | COMP::server |
| 15 | `0x1415cfd70` | 2 | subobject_reader | **no** | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 16 | `0x14104f0b0` | 2 | stream_read_helper | yes | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 17 | `0x1410605b0` | 2 | subobject_reader | **no** | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 18 | `0x141041a50` | 2 | post_read_fixup | yes | NATION::server, NATIONAL_TEAM_CONTAINER::server |
| 19 | `0x14105fa40` | 2 | value_reader | yes | NATIONAL_TEAM_CONTAINER::server |
| 20 | `0x141571860` | 2 | subobject_reader | **no** | NATIONAL_TEAM_CONTAINER::server |
| 21 | `0x141073d90` | 2 | stream_read_helper | yes | NATIONAL_TEAM_CONTAINER::server |
| 22 | `0x14141d570` | 2 | subobject_reader | **no** | NATIONAL_TEAM_CONTAINER::server |
| 23 | `0x1412e70a0` | 1 | stream_token | **no** | CLUB::server |
| 24 | `0x1411d1730` | 1 | class_helper | yes | CLUB::server |
| 25 | `0x140eb8850` | 1 | subobject_reader | yes | COMP::server |
| 26 | `0x1409fa4b0` | 1 | subobject_reader | **no** | COMP::server |
| 27 | `0x1409f8630` | 1 | subobject_reader | **no** | COMP::server |
| 28 | `0x14155d840` | 1 | subobject_reader | **no** | COMP::server |
| 29 | `0x14155e830` | 1 | subobject_reader | **no** | COMP::server |
| 30 | `0x141060550` | 1 | subobject_reader | **no** | NATION::server |

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

