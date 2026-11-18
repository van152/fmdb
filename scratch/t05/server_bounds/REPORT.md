# t05a — server_db 变长表行边界复算报告

## 结论

- 59 张数值表均由本任务脚本从只读 `server_db.dat` 重新定位并解压；目录项 `payload_size` 全部匹配。普查提供的 58 个非空 `payload_sha256` 全部匹配；table_21 的普查 SHA 字段为 `null`，因此无外部期望值可比较。本次独立计算出的 table_21 SHA-256 为 `c107156116d3cd16b25fafc424261dcc54bef700f12587322918d1a5f6a50f62`。
- **58/59 张 `verified: true`**，超过 52 张验收线。两张 empty 表按 `14+0+8==22` 验证；其它通过项均逐行 identity 检验。
- 上游原标 `variable_or_nonstandard` 的 18 张中 **17 张完成整表走查**：`3,7,8,9,10,12,18,25,27,32,36,45,47,48,59,71,72`。table_41 另以显式字段文法独立完成；table_24 保留负结果。
- 每张已解变长表都在 `boundaries.json` 记录最后一行 payload 结束位置与 footer 的精确等式；没有用“约等于”代替 closure。

## 复算方法与边界

1. `common.py` 用 `runpy.run_path()` 只读加载上游 `modding_read_dbdat.py`，调用 `list_tables()`、`_resolve_table()`、`_stream_decompress()`；目录 offset 后 64 字节内扫描 `28 b5 2f fd`，从 magic 位置解压。
2. 每个 payload 独立复核 header、count、目录大小、SHA-256；比较 SHA 时只使用普查中实际提供的 hash。header 的 +12 两字节保留原值，不强制为 `0000`（table_24 实际为 `000b`）。
3. 固定表只有在 `14 + count*stride + 8 == payload_len` 且全行找到 `rdui==ordinal` 或唯一 repeated-u32 identity 后才标 verified。变长通用 walker 同时尝试正序与 footer 倒序，要求每行尾锚为 `ordinal | ID | same-ID | marker`、ordinal 按 `0..count-1` 严格递增，并且首/末行精确贴合 header/footer。table_41 单独解析四个 UTF-8 length-prefixed 字符串、f32、history count/7-byte items 和 13-byte trailer。
4. 通用后缀 walker 只证明边界和 identity；其余 body 字段不据此命名或推断 schema。

## 全表摘要

identity offset 相对行起点；变长表的 `row_end-13` 表示动态尾部位置。完整 closure 字符串、哈希和证据均见 `boundaries.json`。

| table | model | count | payload bytes | stride | identity | verified |
|---:|---|---:|---:|---:|---|:---:|
| 0 | fixed | 3545 | 272987 | 77 | rdui@64 | yes |
| 2 | fixed | 56293 | 2420621 | 43 | rdui@30 | yes |
| 3 | variable | 84259 | 16595312 | — | rdui@row_end-13 | yes |
| 5 | fixed | 7 | 358 | 48 | rdui@35 | yes |
| 6 | fixed | 115 | 4622 | 40 | rdui@27 | yes |
| 7 | variable | 208 | 38280 | — | rdui@row_end-13 | yes |
| 8 | variable | 126 | 5248 | — | rdui@row_end-13 | yes |
| 9 | variable | 251 | 307564 | — | rdui@row_end-13 | yes |
| 10 | variable | 251 | 422345 | — | rdui@row_end-13 | yes |
| 12 | variable | 28597 | 3739570 | — | rdui@row_end-13 | yes |
| 18 | variable | 1567 | 149293 | — | rdui@row_end-13 | yes |
| 19 | fixed | 28 | 1310 | 46 | rdui@33 | yes |
| 21 | fixed | 48413 | 8762775 | 181 | rdui@168 | yes |
| 22 | fixed | 449 | 35493 | 79 | rdui@66 | yes |
| 23 | fixed | 278 | 3914 | 14 | rdui@1 | yes |
| 24 | unresolved | 84507 | 8819030 | — | rdui@row_end-13 (529 rows only) | no |
| 25 | variable | 7047 | 1533972 | — | rdui@row_end-13 | yes |
| 26 | fixed | 90128 | 6218854 | 69 | rdui@56 | yes |
| 27 | variable | 334 | 43345 | — | rdui@row_end-13 | yes |
| 29 | fixed | 13278 | 995872 | 75 | rdui@62 | yes |
| 30 | fixed | 72473 | 2464104 | 34 | rdui@21 | yes |
| 31 | fixed | 37283 | 782965 | 21 | rdui@8 | yes |
| 32 | variable | 315 | 19112 | — | rdui@row_end-13 | yes |
| 33 | fixed | 32409 | 2560333 | 79 | rdui@66 | yes |
| 34 | fixed | 7115 | 313082 | 44 | rdui@31 | yes |
| 35 | fixed | 890 | 13372 | 15 | rdui@2 | yes |
| 36 | variable | 6535 | 562794 | — | rdui@row_end-13 | yes |
| 37 | fixed | 465712 | 18628502 | 40 | rdui@27 | yes |
| 38 | fixed | 5241 | 204421 | 39 | rdui@26 | yes |
| 39 | fixed | 117 | 4936 | 42 | rdui@29 | yes |
| 41 | variable | 173 | 74352 | — | rdui@row_end-13 | yes |
| 42 | fixed | 17721 | 460768 | 26 | rdui@13 | yes |
| 43 | fixed | 535 | 24632 | 46 | rdui@33 | yes |
| 45 | variable | 84477 | 7608748 | — | rdui@row_end-13 | yes |
| 46 | fixed | 7 | 197 | 25 | rdui@12 | yes |
| 47 | variable | 2488 | 109505 | — | rdui@row_end-13 | yes |
| 48 | variable | 5210 | 446049 | — | rdui@row_end-13 | yes |
| 49 | fixed | 792149 | 28517386 | 36 | rdui@23 | yes |
| 50 | fixed | 45 | 1192 | 26 | rdui@13 | yes |
| 51 | fixed | 59 | 1379 | 23 | rdui@10 | yes |
| 52 | empty | 0 | 22 | — | none (0/0 rows) | yes |
| 56 | fixed | 6 | 100 | 13 | rdui@0 | yes |
| 57 | empty | 0 | 22 | — | none (0/0 rows) | yes |
| 58 | fixed | 8 | 382 | 45 | rdui@32 | yes |
| 59 | variable | 9079 | 224880 | — | rdui@row_end-13 | yes |
| 60 | fixed | 59 | 1379 | 23 | rdui@10 | yes |
| 61 | fixed | 16 | 342 | 20 | rdui@7 | yes |
| 62 | fixed | 37214 | 1563010 | 42 | rdui@29 | yes |
| 63 | fixed | 2 | 62 | 20 | rdui@7 | yes |
| 64 | fixed | 6946 | 145888 | 21 | rdui@8 | yes |
| 65 | fixed | 1417 | 43949 | 31 | rdui@18 | yes |
| 66 | fixed | 753 | 18094 | 24 | rdui@11 | yes |
| 67 | fixed | 6826 | 211628 | 31 | rdui@18 | yes |
| 68 | fixed | 138 | 4300 | 31 | rdui@18 | yes |
| 69 | fixed | 230 | 7152 | 31 | rdui@18 | yes |
| 70 | fixed | 10075 | 403022 | 40 | rdui@27 | yes |
| 71 | variable | 616665 | 57480729 | — | rdui@row_end-13 | yes |
| 72 | variable | 138 | 9400 | — | rdui@row_end-13 | yes |
| 73 | fixed | 1 | 45 | 23 | repeated_u32@11 | yes |

## 未解表：table_24

- 上游标记的 table_24 是 team 候选，header count=84,507，header extra=`000b`。该额外两字节与常见 `0000` 不同，但不影响 `tad.` header/count/size/hash 校验。
- 后缀 walker 连续验证到 ordinal 528（529 行）；之后 row 529 起，向后 1 MiB 搜索不到 `ordinal | repeated-u32 | marker`。首个满足后缀条件的候选离当前行起点 8,391,221 bytes，不能安全地把它当作下一行边界。
- 倒序在 ordinal 84505 处也失败：1 MiB 范围内不存在 `ordinal | repeated-u32 | marker` 尾锚。正序卡在 row 529，首个满足条件的候选距该行起点 8,391,221 bytes（上限 1 MiB）。因此不猜 stride、不声称封口；`boundaries.json` 保留 529/84,507 partial 与双向失败位置。payload SHA 与普查一致。

## 上游结论修订

- **table_25（server）**：不能把 client 的 127-byte 行步长外推到 server。server payload 实际由 7,047 个变长 opaque bodies + ordinal/repeated-u32/marker 尾锚封口：`1533964 + 8 == 1533972`。
- **table_10（server）**：边界已逐行封口 251/251；这里只确认后缀 frame 与 identity，不把 client 的 nati 计数段公式或业务字段语义移植到 server。
- **table_3（server）**：本次独立封口 84,259 行；这不是对 client `club_v2` walker 输出的复用。3 个 `0x0c` marker 行与其它 84,256 个 `0x00` marker 行均纳入同一完整 closure。
- **table_59**：上游 unresolved，本次以逐行尾锚独立封口 9,079 行。
- **table_24** 仍 unresolved；其余 17 张原 `variable_or_nonstandard` 已获得完整边界文法。变长 walker 仅恢复 row boundary，不等于字段 schema 全解。

## 复现

```powershell
py -V:3.12 -I -B scratch/t05/server_bounds/verify.py --selftest
py -V:3.12 -I -B scratch/t05/server_bounds/verify.py
```

`--selftest` 纯离线覆盖固定 identity、empty closure、变长 identity suffix/markers、table_41 类字符串/历史向量语法与精确 footer 等式。默认模式重新读 archive，不从本报告或 `boundaries.json` 取数字作为验证输入，并在每处理一表后更新 `boundaries.json`。
