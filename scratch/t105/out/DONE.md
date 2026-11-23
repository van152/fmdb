DONE type=t105

三大主表 + NTC 共 8 个序列化器逐行读取步骤已抽取完毕。

- 函数: 8(`CLUB`/`COMP`/`NATION`/`NATIONAL_TEAM_CONTAINER` × server/client)
- 读取步骤: 274(定长 213 / 变长 61)
- 带版本门控的步骤: 170
- 记录 helper: 22,其中缺反编译 19

| 序列化器 | 步骤 | 定长 | 变长 | 门控 |
|---|---:|---:|---:|---:|
| `CLUB::server` | 26 | 23 | 3 | 24 |
| `CLUB::client` | 7 | 0 | 7 | 1 |
| `COMP::server` | 4 | 0 | 4 | 4 |
| `COMP::client` | 11 | 0 | 11 | 4 |
| `NATION::server` | 43 | 40 | 3 | 28 |
| `NATION::client` | 17 | 0 | 17 | 13 |
| `NATIONAL_TEAM_CONTAINER::server` | 159 | 150 | 9 | 93 |
| `NATIONAL_TEAM_CONTAINER::client` | 7 | 0 | 7 | 3 |

needed_helpers Top 10:`0x140f7ec80`×20, `0x140814b10`×4, `0x140f7f220`×4, `0x140f7fe40`×4, `0x140f7fc40`×3, `0x140f80150`×3, `0x1411d2f80`×2, `0x140839480`×2, `0x140f7ee40`×2, `0x14104f0b0`×2

交付: `big3_serializers.json`, `REPORT.md`, `DONE.md`(本文件)。
