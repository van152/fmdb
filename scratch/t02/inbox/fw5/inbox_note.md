# t02-f / TID=5 行框架

## 结果

| 侧 | member | count | stride | rows_offset | payload_len | closure |
|---|---|---|---|---|---|---|
| client | `client_db/table_5.dat` | 7 | **34** | 0xe | 260 | 14 + 7*34 + 8 = 260 ✔ |
| server | `server_db/table_5.dat` | 7 | **48** | 0xe | 358 | 14 + 7*48 + 8 = 358 ✔ |

统一头 `03 01 74 61 64 2e f1 0d`,`count` @payload+8 (u32le) = 7,+12..13 为 `00 00`,
尾部 8B `00 00 00 01 e4 33 03 00` 两侧一致。两侧都是定长行(stride 整除,无变长迹象)。

## 行列关系(7/7 行验证,L1)

```
server_row == client_row[:21] + 14*0x00 + client_row[21:]
```

即 server 行比 client 行多 14 字节,插在行内 +21 处;table_5 里这 14 字节全为 0,
说明它是 server-only 槽位块(值列),不是被复制的业务数据。两侧 count/header/tail 完全一致。

## 复现

```
py -V:3.12 -I scratch/t02/inbox/fw5/fw5.py --selftest
py -V:3.12 -I scratch/t02/inbox/fw5/fw5.py --tid 5
py -V:3.12 -I scratch/t02/inbox/fw5/verify.py        # 结构 + closure
py -V:3.12 -I scratch/t02/inbox/fw5/relation2.py     # 21 + 14 + 13 关系,ALL PASS
```

只读输入;未启动游戏/编辑器/IDA;未安装任何包。
