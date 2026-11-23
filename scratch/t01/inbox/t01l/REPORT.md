# t01-l：WEATHER(table_27) 行偏移

## 结论 / 验收

- **达标：89 个业务字段获得 L3 wire-offset 映射**：`weather.xml#weat` 的 88 个季节字段（4 季 × 22 字段）及 `wnam`。`duni/rdui/NDBC/FDBC/dbnm` 未映射；不将尾部 12B 身份块猜作字段。
- 行并非定长：行首 UTF-8 字节串带 u32 长度；每行另有 1B 边界标记。334 行全量走查封口。每个映射都把 getter 4CC → 对象成员 → reader 目的地址 → payload 行公式串联；**这些是线上的原始字节偏移，不保证等于 reader 后的最终内存值**（见 §5）。
- 证据等级：exe 静态链为 **L3**，归档/行走查为 **L1**；未做游戏加载，**L4=0**。t01f 的 COMP 锚点/负对照未重做；此表的差异是变长名称 + 固定四季循环。

## 1. 输入与行框架

- 只读 `Z:/SteamLibrary/steamapps/common/Football Manager 2024/data/database/db/2430/2430_fm/client_db.dat`，SHA-256 `5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1`。`client_db/table_27.dat` 压缩成员位于**归档 file offset `0xc70766`**，开头 `28 b5 2f fd 04 60 e5 7d 02 2e 48 04 2b 0d 50 10`，packed=20,425B。
- 解压成员 43,345B，SHA-256 `aaf5f170938babd755f9e020226d3dfcb437c3cd5bdb01796f30acee18e48770`。**以下 payload offset 均为解压成员内偏移**：头 `payload+0: 03 01 74 61 64 2e f1 0d 4e 01 00 00 00 00`（count=334）；首标记 `+0xd: 00`，首行起 `+0xe`。
- 每行 body：`u32le(name_byte_length) + UTF-8 name + 3B 未命名 + 4×23B 季节块 + 12B 未命名尾块`，之后 `00` 边界标记。递推式：`start[0]=14; start[i+1]=start[i]+112+u32le(payload+start[i])`。名称长度 5..44B（合计 5,915B），形成 **33 种行跨度**，无固定 stride。全量算式：`14 + 334×112 + 5,915 + 8 = 43,345`。
- 最后一个标记在 `payload+0xa948: 00`；8B footer 从 `payload+0xa949` 起：`00 00 00 01 1f ee 37 77`。5 行抽验（行起均为 payload offset）：`0 @0xe English Coastal`、`1 @0x8d English Inland`、`2 @0x10b English Northern`、`139 @0x467f BLR-Southern`、`333 @0xa8b3 NGA - Tropical Rainforest Climate Zone`。名称长度、边界/身份原字节及每行 12 个字段抽样值见 `output.json.five_row_samples`。

## 2. Reader 宽度与分支：修正 census 的“straight-line”概括

- `editor.exe` SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。下述代码地址均为 file offset，VA 与逐条字节记录在 `output.json`。type-27 锚点复核：RTTI `editor.exe+0x1aae200: 2e 3f 41 56 57 45 41 54 48 45 52 40 64 62 40 40 00`；分配 `+0x3bd750c: ba 88 00 00 00`；type query `+0xfb37f0: b8 1b 00 00 00 c3`；slot-19 指针 `+0x1882480: 70 c3 58 41 01 00 00 00` → reader `+0x158b970`（VA `0x14158c370`）。
- t01h 报 27 条静态立即宽度 / 28 次流调用，并标为 straight-line；直接重走发现它**不是字面直线**：`+0x158ba21: 45 31 e4` 初始化 R12；`+0x158ba27: 4e 8d 74 23 20` 取季节块；`+0x158bcf9: 49 83 c4 18`、`+0x158bcfd: 49 83 fc 60`、`+0x158bd01: 0f 85 1d fd ff ff` 是固定 4 次循环（对象块步长 24B）。每轮 wire 为 `2B + 21×1B = 23B`，目的从 `+0x20`、`+0x22..+0x36`；例如 `+0x158ba2f: 41 b8 02 00 00 00`，首个 byte 目的 `+0x158ba47: 4a 8d 54 23 22`、宽度 `+0x158ba4f: 41 b8 01 00 00 00`。
- 27 条静态立即宽度组成：名称 helper `+0x35b0822: 41 b8 04 00 00 00`，reader 主体 25 条（先 3×1B，再四轮各 2B+21×1B），identity helper `+0x3c6010d: 41 b8 0c 00 00 00`。名称内容宽度是运行时长度：`+0x35b0879: 44 8b 45 f4`。流调用重算为 reader 25 + 名称 helper 2 + 尾 helper 1 = 28。全序列、分支及 helper 字节在 `output.json.reader_widths`。
- 结论：保留 t01h 的类型/宽度计数，修正其模式描述——这是**固定 4 季循环**，没有全局状态宽度选择器；名称长度是行长变量。其余条件边是流状态退出或读后日期规范化，不选择 transfer width。

## 3. 4CC → 对象成员 → 行偏移

- getter 原始扫描覆盖 `81 f8..ff` 全寄存器 immediate compare 与 `3d`（EAX）；命中有 16 条 `81` 指令、无 `3d` 命中。weather 标量比较使用 EDX，例如 `+0x158e91c: 81 fa 64 73 30 77`（`w0sd`），不是限定 ESI。12 组向量 getter 以 4CC 数值减范围基址、检查上界，再通过 rel32 jump table 选择季节/子字段；每条范围运算、表项及 handler 原字节均在 `output.json`。
- 例 `w0p1`：范围减法 `+0x158e7d9: 8d 82 d0 8f cf 88`，边界 `+0x158e7df: 83 f8 04`，table LEA `+0x158e7e8: 48 8d 0d c9 04 00 00`；index=1 的 rel32 表项 `editor.exe+0x158ecbc: bc fe ff ff` 落到 `+0x158eb74: 48 83 c7 20`，内部码 `+0x158ebab: ba 31 65 72 70`（`pre1`）。Reader 对应 `+0x158ba64: 4a 8d 54 23 23`，`+0x158ba6c: 41 b8 01 00 00 00`，故 wire 为 row+`7+name_len+3`。
- 代表三元组（object offset 为十六进制；payload 公式中 `N=name_byte_length`）：

| 4CC | object+ / bytes | payload row offset |
|---|---:|---:|
| `w0sd` | `0x20 / 2` | `row+N+7` |
| `w0p1` | `0x23 / 1` | `row+N+10` |
| `w0w4` | `0x2b / 1` | `row+N+18` |
| `w0te`, `w0tv`, `w0t0`, `w0t3` | `0x2c`, `0x2d`, `0x2e`, `0x31 / 1` | `row+N+19`, `+20`, `+21`, `+24` |
| `w0dn` | `0x36 / 1` | `row+N+29` |
| `w3sd`, `w3t7`, `w3dn` | `0x68/2`, `0x7d/1`, `0x7e/1` | `row+N+76`, `row+N+97`, `row+N+98` |
| `wnam` | `0x18 / variable string` | u32 length `row+0`；UTF-8 bytes `row+4` |

- `wnam` getter：`+0x158e971: 81 fa 6d 61 6e 77`，object member `+0x158e979: 48 83 c7 18`；reader string destination `+0x158b98c: 4c 8d 43 18`。89 字段完整映射（所有 getter/table-entry/sink 证据及 VA）在 `output.json.row_offset_map`。

## 4. 读后规范化边界

- 每季 helper 在循环内调用：`editor.exe+0x158bcf4: e8 77 00 00 00`，thunk `+0x158bd70: e9 9b 6c fc 02` → `+0x43e7e10`。helper 对降水、风、温度组求和；若不为 100 会改写对象值（代表写点 `+0x43e7e40: 88 51 02`、`+0x43e7e7c: 88 51 07`、`+0x43e7ef5: 88 51 11`）。当前原始 1,336 组中非 100 计数分别为 **降水76、风67、温度468**；因此本报告只认原始 wire bytes 的偏移，不把所有原始值冒称为加载后值。
- 日期不是一律常量：reader 比较四季 word（`+0x158bd0b: 66 3b 43 38`、`+0x158bd11: 66 3b 43 50`、`+0x158bd17: 66 3b 43 68`）；不相等的 `jne`（`+0x158bd0f: 75 24` 等）跳过覆盖。仅四个 wire word 全相等的 12 行执行 `+0x158bd1d/23/29/2f` 写入 55/145/230/300；其余 322 行保留各自日期。

## 5. 复验与交付

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01l/verify.py --help
py -V:3.12 -I -B scratch/t01/inbox/t01l/verify.py --selftest
```

`--selftest` 只读重建 JSON、全量走 334 行并检查静态字节；含固定 stride 反例、内存合成的错误长度/非零标记反例及 `81 f8..ff` / `3d` 扫描负对照。`--write` 仅重建本目录 `output.json`。未写外部输入、未安装依赖、未启动游戏/editor/IDA。
