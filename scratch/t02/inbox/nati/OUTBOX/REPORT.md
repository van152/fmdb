# t02-g2：nati(type 10) client 变长行框架

## 结论

**行边界已恢复，client 251/251 行精确封口。** 行不是固定 stride：跨度 50–1,199B，共 44 种。边界由四个计数段顺序递推；行末 12B ordinal|ID|重复 ID 和其后 `00` 作为独立校验，不靠全 payload 扫描猜边界。

交付证据等级：reader 宽度/循环为 **L3 静态指令证据**；payload 全量走查、identity、footer 为 **L1 解码自检**。未运行游戏/editor/IDA，未安装依赖。完整机器可读框架在 `framework.json`，只读复验脚本在 `verify.py`。

## 输入与 offset 约定

先读 `scratch/t02/inbox/nati/extract.py`：它经旧 decoder 的 `_entries` 定位 table 10、`_decompress_entry` 解压后从 `raw[0]` 写出 bin。两个 bin 均含头尾；client 数据头 14B，行体从 payload offset `0x0e` 起。

- client `client_db_t10.bin`：24,732B，SHA-256 `7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34`；头 `03 01 74 61 64 2e f1 0d fb 00 00 00 00 00`，count=251；footer 从 `payload+0x6094` 起，`00 00 00 01 ec 7a e4 04`。
- server `server_db_t10.bin`：422,345B，SHA-256 `19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f`；头 count 也为 251。此交付的 closure 判据明确是 client 的 24,732B；没有把 client 行公式外推给 server，也没有把 reader 的另一路径擅自标成 server。
- 下文 `row+N` 是相对该行 body 起点；公式中的 row span **包括** 12B identity 和后续 1B `00` marker。payload 的 14B header、8B footer 不计入 row span。

## 计数驱动边界算法

令 A/B/C/D 为依次读出的 signed counts。所有 client 样本均为非负值。

| 段 | 计数位置 | 每项线上宽度 | 下一段如何定位 |
|---|---|---:|---|
| A | `row+24`，signed i8（已在 25B 前缀内） | 5B：4B transfer + 1B transfer | 项目结束后读 B |
| B | `row+25+5*A`，signed i32le | 28B：五个 4B transfer + 两个嵌套 4B transfer | 项目结束后读 C |
| C | `row+29+5*A+28*B`，signed i32le | 28B，同 B 项目 reader | 项目结束后读 D |
| D | `row+33+5*A+28*(B+C)`，signed i32le | 12B：三个 4B transfer | 项目结束后为 identity |

因此：

```text
identity_start = row + 37 + 5*A + 28*(B+C) + 12*D
row_len        = 50 + 5*A + 28*B + 28*C + 12*D
next_row       = row + row_len
```

逐行走查步骤：从当前 row start 取 25B；按 A 消耗 5B 项；依次读取 B、C、D 的 4B signed count 并分别消耗 28B、28B、12B 项；验证接下来的 12B 是 `ordinal u32le | ID u32le | same ID u32le`，再验证 1B marker 为 `00`，位置即下一行起点。`verify.py` 按此公式从 offset 14 顺序走完 251 行，并检查越界、ordinal、重复 ID、marker 和 footer closure。

### 读者循环与每项宽度证据（editor.exe）

静态来源为只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`；reader slot-19 入口 `file+0x103fac0 / VA 0x1410404c0`。下列 file offset 和原字节均在该二进制中；函数 VA 及链接详情另见 `framework.json` 与 `scratch/t01/inbox/t01g/output.json`。

- **A**：`file+0x104070e / VA 0x14104110e: 41 b8 01 00 00 00` 指定 1B，stream call `+0x1040717: ff 50 28` 执行读取；`+0x1040728 / VA 0x141041128: 48 0f be 54 24 44` 取 signed count。循环增量/比较/回跳为 `+0x1040773 / VA 0x141041173: fe c3`、`+0x1040775 / VA 0x141041175: 3a 5c 24 44`、`+0x1040779 / VA 0x141041179: 7c cc`。每项调用 `+0x104075b / VA 0x14104115b: e8 f0 f3 01 00`，经 thunk 到 VA `0x143ef2d00`；两条宽度指令是 `file+0x3d87713 / VA 0x143ef2d13: 41 b8 04 00 00 00` 和 `file+0x3d87736 / VA 0x143ef2d36: 41 b8 01 00 00 00`，对应 stream calls `+0x3d8771f/+0x3d87742: ff 50 28`，故每项 5B。
- **B、C**：B count 读宽度 `file+0x10407a7 / VA 0x1410411a7: 41 b8 04 00 00 00`，stream call `+0x10407b0: ff 50 28`；零项检查/退出为 `+0x10407d1 / VA 0x1410411d1: 83 7c 24 70 00`、`+0x10407d6 / VA 0x1410411d6: 7e 71`，循环 helper `+0x1040829 / VA 0x141041229: e8 72 ec 58 00`，增量/比较/回跳 `+0x1040841: ff c3`、`+0x1040843: 3b 5c 24 70`、`+0x1040847: 7c a0`。C count 读宽度 `+0x1040863 / VA 0x141041263: 41 b8 04 00 00 00`，stream call `+0x104086c: ff 50 28`；零项检查/退出 `+0x1040890 / VA 0x141041290: 83 bc 24 80 00 00 00 00`、`+0x1040898 / VA 0x141041298: 7e 70`，循环 helper `+0x10408eb / VA 0x1410412eb: e8 b0 eb 58 00`，增量/比较/回跳 `+0x10408ff: ff c3`、`+0x1040901: 3b 9c 24 80 00 00 00`、`+0x1040908: 7c a1`。共同 helper 的 thunk 为 `file+0x15cf4a0: e9 eb b1 02 03`（跳到 VA `0x1445fb090`，file `+0x448fa90`）；该函数有五条 4B 宽度指令：file `+0x448faa3/+0x448fac6/+0x448fae2/+0x448fafe/+0x448fb1a`（VA 分别 `0x1445fb0a3/0x1445fb0c6/0x1445fb0e2/0x1445fb0fe/0x1445fb11a`），各为 `41 b8 04 00 00 00`，对应 stream calls `+0x448faaf/+0x448facf/+0x448faeb/+0x448fb07/+0x448fb23: ff 50 28`；另在 `+0x448fb33: e8 48 d8 7b fc` 与 `+0x448fb4d: e9 2e d8 7b fc` 调/尾跳嵌套 helper。其 4B transfer 是 `file+0x39dd7c8 / VA 0x143b48dc8: 41 b8 04 00 00 00`，stream call `+0x39dd7d4: ff 57 28`。因此 B/C 每项 7×4=28B。
- **D**：count 读宽度 `file+0x104091e / VA 0x14104131e: 41 b8 04 00 00 00`，stream call `+0x1040927: ff 50 28`；零项检查/退出 `+0x104097b / VA 0x14104137b: 83 7c 24 48 00`、`+0x1040980 / VA 0x141041380: 7e 49`；每项 helper 调用 `+0x10409a7 / VA 0x1410413a7: e8 04 f2 01 00`，增量/比较/回跳 `+0x10409be: 48 ff c7`、`+0x10409c6: 48 39 c7`、`+0x10409c9: 7c c8`。helper thunk `file+0x105fbb0: e9 4b 33 e9 02` 跳到 VA `0x143ef3900`（file `+0x3d88300`）；该函数在 `+0x3d88314/+0x3d8833c/+0x3d88380`（VA `0x143ef3914/0x143ef393c/0x143ef3980`）各有 `41 b8 04 00 00 00`，对应 stream calls `+0x3d88320/+0x3d88345/+0x3d8838c: ff 50 28`，每项 12B。
- reader 在 `file+0x10409cb: 80 bc 24 20 01 00 00 00` 检查一个条件，非零分支有额外标量读取；client 计数递推在 251 行都正好落到验证过的 identity 起点，没有该尾段的剩余 wire bytes。这里不把该条件另行命名。

reader 入口还在 `editor.exe+0x103fae6: 0f 84 c4 0a 00 00` 分到上述普通前缀路径；另一路有 2B count / 4B item loop。client 的 25B 前缀与普通路径相符。本报告不基于此把另一路径命名为 client 或 server。

### 逐行 closure 与 identity/duni 对照

全表计数合计及最大值：A=`492 / 7`、B=`214 / 40`、C=`63 / 21`、D=`162 / 2`。于是所有行 span 总和为：

```text
251*50 + 492*5 + (214+63)*28 + 162*12 = 24,710B
payload closure: 14 + 24,710 + 8 = 24,732B
```

identity 校验对每一行成立：ordinal=0..250 的对应行号，后两个 u32 相等，identity 后字节为 `00`。代表边界（均为 payload offset）：行 0 `0x0e`/65B；行 1 `0x4f`/77B；行 11 `0x310`/93B；行 55 `0xfc4`/139B；行 143 `0x2efb`/1,199B；行 250 `0x6058`/60B，恰好结束于 footer `0x6094`。

关键 duni：行 55 identity 从 `payload+0x1042` 开始，原字节 `37 00 00 00 6e 00 00 00 6e 00 00 00`；ordinal=55，ID=110、重复 ID=110。题给锚点 `payload+0x1046` 正好落在该 identity 的 ID 字段，字节 `6e 00 00 00 6e 00 00 00`，吻合。

## 可应用字段偏移（7 个）

复用 t01-g 的 getter→对象成员→reader 游标链；下表的 row offset 是普通 client 行 body 偏移。`editor.exe` 的 SHA-256/来源见上；VA、分支字节和完整链接在 `scratch/t01/inbox/t01g/output.json#row_offset_map`。字段值只是原始 wire bytes，不把未验证的加载后规范化当作结论。

| 4CC / 字段 | row+ / 宽度 | reader destination（file offset；VA；bytes） | width instruction（file offset；VA；bytes） | getter cmp（file offset；VA；bytes） | getter member（file offset；VA；bytes） |
|---|---:|---|---|---|---|
| Ngct / Gain Nationality Type | 0 / 1 | `0x10405b4`; `0x141040fb4`; `49 8d 97 cb 01 00 00` | `0x10405be`; `0x141040fbe`; `41 b8 01 00 00 00` | `0x1042385`; `0x141042d85`; `81 fe 74 63 67 4e` | `0x1042a47`; `0x141043447`; `41 0f be b4 24 cb 01 00 00` |
| Ncti / Continent | 1 / 4 | `0x10405d8`; `0x141040fd8`; `49 8d 97 f0 00 00 00` | `0x10405e2`; `0x141040fe2`; `41 b8 04 00 00 00` | `0x104218a`; `0x141042b8a`; `81 fe 69 74 63 4e` | `0x1042ed7`; `0x1410438d7`; `49 8b 8c 24 f0 00 00 00` |
| Nrgi / Region | 5 / 4 | `0x10405fc`; `0x141040ffc`; `49 8d 97 f8 00 00 00` | `0x1040606`; `0x141041006`; `41 b8 04 00 00 00` | `0x10424e5`; `0x141042ee5`; `81 fe 69 67 72 4e` | `0x10424f1`; `0x141042ef1`; `49 8b 8c 24 f8 00 00 00` |
| Ncur / Currency | 13 / 4 | `0x1040644`; `0x141041044`; `49 8d 97 00 01 00 00` | `0x104064e`; `0x14104104e`; `41 b8 04 00 00 00` | `0x1042196`; `0x141042b96`; `81 fe 72 75 63 4e` | `0x1042c7d`; `0x14104367d`; `49 8b 8c 24 00 01 00 00` |
| Nsod / State Of Development | 17 / 1 | `0x1040668`; `0x141041068`; `49 8d 97 cc 01 00 00` | `0x1040672`; `0x141041072`; `41 b8 01 00 00 00` | `0x1042268`; `0x141042c68`; `81 fe 64 6f 73 4e` | `0x1042e6f`; `0x14104386f`; `41 0f be b4 24 cc 01 00 00` |
| Necf / Economic Factor | 18 / 1 | `0x104068c`; `0x14104108c`; `49 8d 97 d0 01 00 00` | `0x1040696`; `0x141041096`; `41 b8 01 00 00 00` | `0x10421a2`; `0x141042ba2`; `81 fe 66 63 65 4e` | `0x10421ae`; `0x141042bae`; `41 0f be b4 24 d0 01 00 00` |
| Nygn / Years To Gain Nationality | 23 / 1 | `0x10406d4`; `0x1410410d4`; `49 8d 97 cd 01 00 00` | `0x10406de`; `0x1410410de`; `41 b8 01 00 00 00` | `0x1042078`; `0x141042a78`; `81 fe 6e 67 79 4e` | `0x1042aaf`; `0x1410434af`; `41 0f be b4 24 cd 01 00 00` |

row+9 / 4B、row+19 / 4B 和 row+24 / 1B 仍未赋 schema 名；本解析只将 row+24 byte 用作 A count，不把它另猜作业务字段。没有覆盖 346 个 nati 字段。

## 复验 / 保留限制

```powershell
py -V:3.12 -I -B scratch/t02/inbox/nati/OUTBOX/verify.py --help
py -V:3.12 -I -B scratch/t02/inbox/nati/OUTBOX/verify.py --selftest
```

复验结果：`PASS: client nati rows=251; formula spans=24710; closure=14+24710+8=24732`。未解 server 的完整行框架；不把条件尾段含义、alternate path 对应哪个 payload、两个 opaque 前缀槽、或其余 schema 字段写成结论。
