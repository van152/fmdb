# t140 — FM24 `.dat` 双向回写 / FMF 重打包 / 双路回读验收

脚本：`scripts/t140_fm24_roundtrip.py`（`--roundtrip-all` / `--build-patched` / `--selftest`）
产物目录：`scratch/t140/out/`　构建耗时 `37.5s`

## Stage 1 — 结构化解码 → 值模型 → 重编码（载荷 SHA-256 位级相同）

**79/79** 张编号表重编码后 `sha256(reencoded) == sha256(original)`；共 **2,846,936** 行、**186,135,899** 字节载荷（fixed 48 / variable 29 / empty 2），耗时 `21.8s`。

| archive/id | class | kind | rows | payload B | SHA-256 相同 | row0 值节点 |
|---|---|---|---:|---:|---|---:|
| `client/0` | `AWARD` | fixed | 3,545 | 272,987 | YES | 40 |
| `client/2` | `CITY` | fixed | 56,293 | 2,420,621 | YES | 12 |
| `client/3` | `CLUB` | variable | 84,259 | 6,932,082 | YES | 11 |
| `client/5` | `CONTINENT` | fixed | 7 | 260 | YES | 16 |
| `client/6` | `INJURY` | fixed | 115 | 1,862 | YES | 6 |
| `client/7` | `MEDIA_SOURCE` | variable | 208 | 36,824 | YES | 36 |
| `client/8` | `LANGUAGE` | variable | 126 | 5,248 | YES | 10 |
| `client/9` | `NATIONAL_TEAM_CONTAINER` | variable | 251 | 31,956 | YES | 168 |
| `client/10` | `NATION` | variable | 251 | 24,732 | YES | 20 |
| `client/18` | `DERBY` | variable | 1,567 | 139,891 | YES | 20 |
| `client/19` | `REGION` | fixed | 28 | 1,282 | YES | 11 |
| `client/21` | `STADIUM` | fixed | 48,413 | 1,839,716 | YES | 11 |
| `client/22` | `STADIUM_CHANGE` | fixed | 449 | 5,859 | YES | 3 |
| `client/23` | `STAGE_NAME` | fixed | 278 | 3,914 | YES | 4 |
| `client/25` | `COMP` | fixed | 7,047 | 894,991 | YES | 66 |
| `client/27` | `WEATHER` | variable | 334 | 43,345 | YES | 94 |
| `client/35` | `PLAYER_TYPE` | fixed | 890 | 13,372 | YES | 5 |
| `client/41` | `CURRENCY_RECORD` | variable | 173 | 74,352 | YES | 100 |
| `client/47` | `LOCAL_REGION` | variable | 2,488 | 109,505 | YES | 20 |
| `client/56` | `AGREEMENT` | fixed | 6 | 100 | YES | 3 |
| `server/0` | `AWARD` | fixed | 3,545 | 272,987 | YES | 40 |
| `server/2` | `CITY` | fixed | 56,293 | 2,420,621 | YES | 12 |
| `server/3` | `CLUB` | variable | 84,259 | 16,595,312 | YES | 39 |
| `server/5` | `CONTINENT` | fixed | 7 | 358 | YES | 24 |
| `server/6` | `INJURY` | fixed | 115 | 4,622 | YES | 24 |
| `server/7` | `MEDIA_SOURCE` | variable | 208 | 38,280 | YES | 40 |
| `server/8` | `LANGUAGE` | variable | 126 | 5,248 | YES | 10 |
| `server/9` | `NATIONAL_TEAM_CONTAINER` | variable | 251 | 307,564 | YES | 500 |
| `server/10` | `NATION` | variable | 251 | 422,345 | YES | 202 |
| `server/12` | `STARTING_AWARD_HISTORY` | variable | 28,597 | 3,739,570 | YES | 29 |
| `server/18` | `DERBY` | variable | 1,567 | 149,293 | YES | 23 |
| `server/19` | `REGION` | fixed | 28 | 1,310 | YES | 12 |
| `server/21` | `STADIUM` | fixed | 48,413 | 8,762,775 | YES | 81 |
| `server/22` | `STADIUM_CHANGE` | fixed | 449 | 35,493 | YES | 24 |
| `server/23` | `STAGE_NAME` | fixed | 278 | 3,914 | YES | 4 |
| `server/24` | `NATIONAL_TEAM` | variable | 84,507 | 8,819,030 | YES | 52 |
| `server/25` | `COMP` | variable | 7,047 | 1,533,972 | YES | 494 |
| `server/26` | `COMP_HISTORY_RECORD` | fixed | 90,128 | 6,218,854 | YES | 21 |
| `server/27` | `WEATHER` | variable | 334 | 43,345 | YES | 94 |
| `server/29` | `STARTING_LOAN` | variable | 13,278 | 995,872 | YES | 19 |
| `server/30` | `STARTING_INJURY` | fixed | 72,473 | 2,464,104 | YES | 12 |
| `server/31` | `STARTING_CONFIDENCE` | fixed | 37,283 | 782,965 | YES | 6 |
| `server/32` | `STARTING_FUTURE_TRANSFER` | variable | 315 | 19,112 | YES | 18 |
| `server/33` | `STARTING_CLUB_DEBT` | fixed | 32,409 | 2,560,333 | YES | 23 |
| `server/34` | `STARTING_TEAM_CUP_HISTORY` | fixed | 7,115 | 313,082 | YES | 14 |
| `server/35` | `PLAYER_TYPE` | fixed | 890 | 13,372 | YES | 5 |
| `server/36` | `STARTING_MANAGER_HOF_RECORD` | variable | 6,535 | 562,794 | YES | 13 |
| `server/37` | `STARTING_TEAM_LEAGUE_HISTORY` | fixed | 465,712 | 18,628,502 | YES | 17 |
| `server/38` | `STARTING_BAN` | fixed | 5,241 | 204,421 | YES | 11 |
| `server/39` | `STARTING_AVERAGE_POINTS` | fixed | 117 | 4,936 | YES | 9 |
| `server/41` | `CURRENCY_RECORD` | variable | 173 | 74,352 | YES | 100 |
| `server/42` | `STARTING_RETIREMENT` | fixed | 17,721 | 460,768 | YES | 6 |
| `server/43` | `STARTING_MONTHLY_INSTALLMENT` | fixed | 535 | 24,632 | YES | 9 |
| `server/45` | `STARTING_RECORD` | variable | 84,477 | 7,608,748 | YES | 19 |
| `server/46` | `STARTING_DRAFT_TRANSFER` | fixed | 7 | 197 | YES | 8 |
| `server/47` | `LOCAL_REGION` | variable | 2,488 | 109,505 | YES | 20 |
| `server/48` | `STARTING_RECORD` | variable | 5,210 | 446,049 | YES | 19 |
| `server/49` | `STARTING_PERSON_HISTORY` | fixed | 792,149 | 28,517,386 | YES | 6 |
| `server/50` | `STARTING_MLS_TRADED_SLOT` | fixed | 45 | 1,192 | YES | 7 |
| `server/51` | `STARTING_MLS_GENERAL_ALLOCATION_MONEY` | fixed | 59 | 1,379 | YES | 6 |
| `server/52` | `STARTING_PLAYER_HAPPINESS` | empty | 0 | 22 | YES | 0 |
| `server/56` | `AGREEMENT` | fixed | 6 | 100 | YES | 3 |
| `server/57` | `FIXTURE_NAME` | empty | 0 | 22 | YES | 0 |
| `server/58` | `STARTING_WEEKLY_WAGE_CONTRIBUTION` | fixed | 8 | 382 | YES | 8 |
| `server/59` | `STARTING_MEDIA_EXPECTATIONS` | variable | 9,079 | 224,880 | YES | 4 |
| `server/60` | `STARTING_MLS_TARGETED_ALLOCATION_MONEY` | fixed | 59 | 1,379 | YES | 6 |
| `server/61` | `STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT` | fixed | 16 | 342 | YES | 6 |
| `server/62` | `STARTING_RESERVE_TEAM` | fixed | 37,214 | 1,563,010 | YES | 14 |
| `server/63` | `STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER` | fixed | 2 | 62 | YES | 6 |
| `server/64` | `STARTING_CLUB_STAFF_JOB_STATUS` | fixed | 6,946 | 145,888 | YES | 7 |
| `server/65` | `STARTING_NEWGEN_PARAMETER` | fixed | 1,417 | 43,949 | YES | 9 |
| `server/66` | `STARTING_CLUB_TRANSFER_PREFERENCE` | fixed | 753 | 18,094 | YES | 8 |
| `server/67` | `STARTING_NEWGEN_PARAMETER` | fixed | 6,826 | 211,628 | YES | 9 |
| `server/68` | `STARTING_NEWGEN_PARAMETER` | fixed | 138 | 4,300 | YES | 9 |
| `server/69` | `STARTING_NEWGEN_PARAMETER` | fixed | 230 | 7,152 | YES | 9 |
| `server/70` | `STARTING_VISION_OBJECTIVE` | fixed | 10,075 | 403,022 | YES | 15 |
| `server/71` | `STARTING_PAST_TRANSFER` | variable | 616,665 | 57,480,729 | YES | 45 |
| `server/72` | `STARTING_PAST_TRADE` | variable | 138 | 9,400 | YES | 30 |
| `server/73` | `STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT` | fixed | 1 | 45 | YES | 6 |

编码规则（与 `t133_fm24_reader_v2.py` 的 op 语法逐条对应，不存在原始行字节搬运）：

- 13B 表头：`03 01 tad.` + `u16 ver=0x0df1` + `u32 row_count` + `1B reserved(0)` 逐字段重写；
- 每行：`[1B selector]` + 行体。行体按值重编码——u8/16/32/64 与 9/10/16 字节整数走 `int.from_bytes` ↔ `to_bytes`，字符串走 `u32 len + utf-8`（长度前缀按重新编码后的字节数重算），向量计数由实际发射的元素个数回填，identity 为 3×u32；
- 9B footer：`0x00` 终止符 + 8B trailer（以 u64 读入后重新写出；其语义未解，按原值保真）。

## Stage 2 — FMF/zstd 重打包 + 语义改写

| # | archive/table | class | 字段 | L3 4CC | wire off | 原值 → 新值 | 载荷 Δ |
|---|---|---|---|---|---:|---|---:|
| M6 | `client/0` | `AWARD` | AWwh (u8 award scalar) | `AWwh` | 39 | 200 → 251 | +0 B |
| M2 | `client/3` | `CLUB` | club long name (first UTF-8 string of CLUB_HEAD) | `TCln` | 26 | `Klubi i Futbollit Albpetrol Patos` → `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | +15 B |
| M8 | `client/10` | `NATION` | NcpR (u32, client-side NATION tail block) | `NcpR` | 9 | 1187 → 1587 | +0 B |
| M10 | `client/25` | `COMP` | cmnl (min pitch length, u16) | `cmnl` | 76 | 1050 → 1150 | +0 B |
| M5 | `server/0` | `AWARD` | AWwh (u8 award scalar) | `AWwh` | 39 | 200 → 251 | +0 B |
| M1 | `server/3` | `CLUB` | club long name (first UTF-8 string of CLUB_HEAD) | `TCln` | 26 | `Klubi i Futbollit Albpetrol Patos` → `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | +15 B |
| M7 | `server/10` | `NATION` | Npop (population, u32) | `Npop` | 604 | 43851044 → 45000000 | +0 B |
| M4 | `server/21` | `STADIUM` | Scas (stadium capacity-class u32) | `Scas` | 12 | 11464 → 22464 | +0 B |
| M9 | `server/25` | `COMP` | cmnl (min pitch length, u16) | `cmnl` | 848 | 1050 → 1150 | +0 B |
| M3 | `server/45` | `STARTING_RECORD` | record name (u32 namelen + UTF-8) | `stnm` | 37 | `Markelian Xhai` → `M. Xhai` | -7 B |

| archive | 成员数 | 重压缩 | 逐字节复制 | 载荷总字节 | 目录原始字节 | 目录重序列化 | 打包后大小 |
|---|---:|---:|---:|---:|---:|---|---:|
| `server` | 77 | 6 | 71 | 57,725,295 | 4,784 | 字节相同 | 57,726,522 |
| `client` | 31 | 4 | 27 | 13,232,679 | 1,954 | 字节相同 | 13,233,246 |

字符串改写使后续每一行偏移、成员 `size`/`packed_size` 与整包偏移全部重算；未改写的成员以**原始 zstd 帧字节**整体复制，因此 t106 的 13 个特殊成员解码结果不变。

## Stage 3a — 未改动的 t133 纯 Python 回读（重打包归档）

**79/79** 张表 `footer_closed == True`（`diff == 0`，共 **2,846,936** 行），失败 `0`。

| # | 表 | 字段 | wire off | 回读值 | 目标 | 结果 |
|---|---|---|---:|---|---|---|
| M1 | `server/3` | CLUB | 26 | `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | Klubi i Futbollit Albpetrol Patos [T140-PATCHED] | PASS |
| M2 | `client/3` | CLUB | 26 | `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | Klubi i Futbollit Albpetrol Patos [T140-PATCHED] | PASS |
| M3 | `server/45` | STARTING_RECORD | 37 | `M. Xhai` | M. Xhai | PASS |
| M4 | `server/21` | STADIUM | 12 | 22464 | 22464 | PASS |
| M5 | `server/0` | AWARD | 39 | 251 | 251 | PASS |
| M6 | `client/0` | AWARD | 39 | 251 | 251 | PASS |
| M7 | `server/10` | NATION | 604 | 45000000 | 45000000 | PASS |
| M8 | `client/10` | NATION | 9 | 1587 | 1587 | PASS |
| M9 | `server/25` | COMP | 848 | 1150 | 1150 | PASS |
| M10 | `client/25` | COMP | 76 | 1150 | 1150 | PASS |

## Stage 3b — 真机 `editor.exe` x86_64（Unicorn）回读

| archive/table | class | slot19 | 原行 B | 新行 B | CPU 消费 B | 框架尾 B | 状态 |
|---|---|---|---:|---:|---:|---:|---|
| `client/3` | `CLUB` | `0x140e5b1a0` | 94 | 109 | 79 → **94** | 15 | PASS |
| `server/3` | `CLUB` | `0x140e5b1a0` | 197 | 212 | 154 → **169** | 43 | PASS |
| `server/45` | `STARTING_RECORD` | `0x141544130` | 93 | 86 | 93 → **86** | 0 | PASS |
| `server/21` | `STADIUM` | `0x141184930` | 180 | 180 | 180 → **180** | 0 | PASS |
| `server/0` | `AWARD` | `0x140e48db0` | 76 | 76 | 76 → **76** | 0 | PASS |
| `client/0` | `AWARD` | `0x140e48db0` | 76 | 76 | 76 → **76** | 0 | PASS |
| `server/10` | `NATION` | `0x1410404c0` | 631 | 631 | 631 → **631** | 0 | PASS |
| `client/10` | `NATION` | `0x1410404c0` | 64 | 64 | 64 → **64** | 0 | PASS |
| `server/25` | `COMP` | `0x140ed1440` | 898 | 898 | 898 → **898** | 0 | PASS |
| `client/25` | `COMP` | `0x140ed1440` | 126 | 126 | 126 → **126** | 0 | PASS |

说明：`CLUB` 的 `slot19` 在框架尾部（`u8 + u16 + 12B identity`，server 43 B / client 15 B）之前返回——该尾部由外层行循环读取，不属于 `slot19` 的职责。上表同时给出尾部字节数，因此 `CPU 消费 + 框架尾 == 新行长度` 对 10/10 张表逐张成立；且尾部字节在改写前后逐字节相同（见 JSON 的 `framework_trailer_hex_original/_mutated`）。

C++ 对象内存回读（`emu.mu.mem_read`，数值为 CPU 真正写入的值）：

| 表 | 字段 | 目的地址 | obj 偏移 | CPU 写入 | 目标 | 结果 |
|---|---|---|---:|---:|---|---|
| `client/3` | club long name (first UTF-8 string | `0x300002174` | 0xc0 | `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | PASS |
| `server/3` | club long name (first UTF-8 string | `0x300002174` | 0xc0 | `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | `Klubi i Futbollit Albpetrol Patos [T140-PATCHED]` | PASS |
| `server/45` | record name (u32 namelen + UTF-8) | `0x300002064` | 0x38 | `M. Xhai` | `M. Xhai` | PASS |
| `server/21` | Scas (stadium capacity-class u32) | `0x300000078` | 0x78 | 22464 | 22464 | PASS |
| `server/0` | AWwh (u8 award scalar) | `0x300000091` | 0x91 | 251 | 251 | PASS |
| `client/0` | AWwh (u8 award scalar) | `0x300000091` | 0x91 | 251 | 251 | PASS |
| `server/10` | Npop (population, u32) | `0x3000001c4` | 0x1c4 | 45000000 | 45000000 | PASS |
| `client/10` | NcpR (u32, client-side NATION tail | `0x3000000e8` | 0xe8 | 1587 | 1587 | PASS |
| `server/25` | cmnl (min pitch length, u16) | `0x300000154` | 0x154 | 1150 | 1150 | PASS |
| `client/25` | cmnl (min pitch length, u16) | `0x300000154` | 0x154 | 1150 | 1150 | PASS |

### Harry Kane（`people_db.dat` `PLAYER::slot19`）

- 记录：`ordinal=166119` `ptype=2`，body `1148` B（framing 5B 头 + body，改写后长度不变），只改了 `4` 个字节；
- `PLAYER::slot19=0x140e08730`：CPU 消费 **1148** B / 1148 B，`ok=True`，`rip==STOP`，对象基址 `0x300000278`；

| 4CC | 字段 | obj 偏移 | 原值 | 目标 | CPU RAM | 结果 |
|---|---|---|---:|---:|---:|---|
| `PCAB` | CA | `obj - 0x78` | 184 | 190 | **190** | PASS |
| `PPAB` | PA | `obj - 0x76` | 185 | 195 | **195** | PASS |
| `PDfn` | Finishing | `obj - 0x70 + 17` | 19 | 20 | **20** | PASS |
| `PDpc` | Pace | `obj - 0x70 + 53` | 14 | 17 | **17** | PASS |

## 结论

- Stage 1：`79/79` 表位级相同。
- Stage 2：10 处语义改写（6 个表类，其中 3 处为字符串：2 处 +15 B、1 处 −7 B），`patched_server_db.dat` / `patched_client_db.dat` 可被 t133 完整解析。
- Stage 3：t133 `79/79` 闭合 + editor.exe `10/10` 目标与 Kane 全部通过。
- 断言 `69/69` 通过。

