# t01-f：COMP 的 4CC → 对象成员 → `.dat` 行偏移

**达标：在 table_25 client 的两段原未命名 packed 区内新增 18 个 L3 业务字段。** 其中 14 个在 `master.json` 标注 `is_client_field`；另 4 个区域边界字段由二进制读写链定位，不依赖该标记。5 个既有**字节**锚点全部复现；身份块的旧命名与原生 4CC 有别（见 §4）。

**行偏移不存于所谓 0x38 描述符槽。** COMP 的读写器按固定指令顺序和分支逐项传输；对当前样本累加实际调用宽度，即得行偏移。字段分发提供 4CC→对象成员，序列化器提供对象成员→流位置。旧的 `mov [row+N]` 联合搜索无命中是预期结果，不能推出存在行偏移数组。

- 交付：`scratch/t01/inbox/t01f/{REPORT.md,output.json,verify.py}`；正式成对工件 `reports/t01f_comp_row_offsets.{md,json}`。JSON 含逐项 file offset、VA、原字节和实际 payload 样例；下文裸代码偏移均为 **editor.exe file offset**，除非另注明。
- PE 来源：只读 `D:/tmp2b/fm24/input/{editor.exe,fm.exe}`，SHA-256 与 `evidence/fm24/reports/qa/IDA_PROVENANCE.md` 一致；editor 为 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。分段地址：`RVA=off+0xA00`（相关 `.rdata/.debug`）或 `off+0x16B600`（`.reloc`）。
- 数据来源：只读安装库 `2430/2430_fm`，`client_db.dat@0x4bc277`、`server_db.dat@0x7f27b9` 均为 `28 b5 2f fd`；复用旧库的只读 `scripts/modding_read_dbdat.py` 在内存解包。下文 payload 偏移指**解压后的成员**，不与 archive file offset 混用。旧结论只引 `evidence/fm24/` 快照，以 `evidence/MANIFEST.json` 校验。

## 1. 两种对象、两个虚表；helperB 不返回字段数组

- 记录类 `db::COMP`：RTTI 名在 `0x1aaccb0: 2e 3f 41 56 43 4f 4d 50 40 64 62 40 40 00`。构造器 `0xeb5dd5: 48 8d 05 dc 74 9c 00 48 89 01` 写 vptr `0x14187dcb8`（`off 0x187d2b8`）；`0x187d2b0` 是紧邻的 RTTI 指针，不是函数槽。`0x187d2e0: 40 fa eb 40 01 00 00 00` 是 **0-based slot 5**（原护栏从 RTTI 指针起数作 slot6，字节不变）。类型查询 `0xed0a30: b8 19 00 00 00 c3` 返回 25。
- 表类 `db::DATABASE_TABLE<db::COMP>`：RTTI 名在 `0x1aad160`（前缀 `2e 3f 41 56 3f 24 44 41 54 41 42 41 53 45 5f 54 41 42 4c 45`；全串见 JSON）。`0xf02aa7: ba 19 00 00 00` 传表号，构造落点 `0x3ceb8e2: 89 7e 54` 写 `[table+0x54]`，随后表初始化设置另一 vptr `0x14187f6d8`（`off 0x187ecd8`）。记录工厂跳表的 type-25 项 `0xf49d9c: f1 f3 ff ff` 落到 `0xf49129: b9 b0 01 00 00`，分配 0x1b0 字节、在 `0xf49139: e8 72 cc f6 ff` 调 COMP 构造器。二者不是同一对象的前后 vptr。
- `helperB`：`0x83caf0: e9 7b 0e f4 02` → VA `0x14377e370` / off `0x3612d70`，是可追的明文。`0x3612d74: 48 8b 05 15 c1 3d fe` 读全局 `0x141b5a490`；非空快返。慢路径 `0x3612dc0: b9 d8 00 00 00` 分配，填入 `sicore::TYPED_TRAITS_MANAGER` RTTI 对应 vptr（`0x3612e17`，名字 `0x1aa8480`），`0x3612f01: 48 89 05 88 bf 3d fe` 发布到同一全局。
- `0x3612e4a: c6 40 40 02`、`0x3612e4e: 48 8d 0d 93 1c 0e fe`、`0x3612e55: 48 89 48 38`：manager `+0x38` 是内嵌 `RAW_TYPED_TRAITS<unsigned int>`（RTTI `0x1aa85d0`），其 `+0` 为 vptr、`+8` 为初始化类型字节 `02`。共 13 个 traits 每隔 16B，剩余字节不赋义。相比之下 `cmnl` 的 getter 读对象 `+0x154`，另在 `0xec33d4: 48 83 c0 68` 取 manager `+0x68` 的 float traits 来装箱；两个偏移不是同类量。
- 51 个 COMP 注册块逐块核验：如 `0xebf057: e8 94 da 97 ff 48 83 c0 38` 后 `0xebf060: c7 45 f0 6e 67 4c 50 48 89 45 e8`，每个都是重新调用 helperB 后取同一 `+0x38`，不是跨对象累加。`0x83ad52: 49 8b 06 49 8b 4e 08 48 89 4b 08 48 89 03` 复制 `{trait*, value}`，4CC 在 value 低 dword；`0x83ad65` 复位源到 NULL trait（`+8`）；`0x83ad7e: 48 89 1f 49 83 47 08 08` 追加指针、end 加 8。不存在从这些 pair 读行偏移的证据。

## 2. 找到顺序读写链，按调用宽度推导偏移

1. 表循环样本：`0xf2ad00: ff 50 28`（R8D=4）读计数、`0xf2ad1f: ff 50 28`（R8D=1）读表级字节；每条先在 `0xf2af2f: ff 50 28` 读 1B，再从 `[table+0x54]` 取表号调用工厂（`0xf2af41: 8b 4e 54 e8 e7 db 01 00`），`0xf2af72: ff 95 98 00 00 00` 调记录 slot 19。这是表循环与 COMP 工厂/读器的接口证据，不冒称已追到 archive opener 对该实例的调用。
2. COMP slot 19 `0x187d350: 40 14 ed 40 01 00 00 00` → `0xed0a40: e9 8b 92 dd 02` → `0x3b3f0f9: c6 44 24 38 00 45 31 c0` 置第 8 参数为 0 → `0x3b3f101: e8 fa d2 20 fd` → **读主体 `off 0xeb7000` / VA `0x140eb7a00`**。`0xeb7016: 48 89 cb` 令 RBX=COMP `this`；流 slot `+0x28` 接收缓冲地址和 R8D 字节数。写侧 slot 21 `0x187d360: 80 14 ed 40 01 00 00 00` → `0xed0a86: e9 95 7e fe ff` → **写主体 `off 0xeb8920` / VA `0x140eb9320`**。
3. 读主体共用前缀：先 2B；颜色 helper（`0xeb706b` → `0x150ec50: e9 8b cc f8 02`）收 `1+5×2+1=12B`；5 个独立 byte；`0x4339eb4: 80 7c 24 2f 01` 对 tag `02` 走 7B 值；`0x433bbfc`（选长指令见 JSON）对 tag `03` 走 15B 值；再 1B 和两个 4B 日期。总计 `2+12+5+8+16+1+8=52`，不是搜索已知偏移得到的。
4. 当前数据 `row+14 != 4`，跳过内联名称（`0xeb71b9: 80 7d 00 04 75 38`）。`0xeb7202: 74 55`（arg8=0）进入四个 4B 引用，顺序 `obj+58/60/70/68`（十六进制）。写侧 `0xeb8b51: 8b 40 08` 取被引用对象的 ordinal，空引用 `0xeb8b8f: b8 ff ff ff ff`。再读 2B；`0xeb7394: 44 0f b6 ac 24 e8 00 00 00` 取第 6 参数，`0xeb73a0: 0f 84 7b 06 00 00` 在 client 布局跳过 server 扩展，恢复于 row+70。
5. `+70` 后按 `4,2,2,2,2,2` → `+84`；四个 4B 城市引用 → `+100`；1B 有无色标记 + 2B 颜色 + 两个 4B 日期 + 3 个 byte → `+114`；基类读 12B 至 `+125`。逐步目标寄存器、分支、宽度与样例见 `row_codec.cursor_layout`。`+126` 不是 COMP 成员：写侧 `0xeb893b: c6 44 24 28 00`、`0xeb8952: ff 50 28` 在主体**之前**输出 0；样本的前导标记在 `13+i*127`。沿用 `14+i*127` 为 row+0，`+126` 是边界字节，最后一条之后剩余 9B（payload `0xda806: 00 00 00 00 01 4e c4 3a 77`），未给末记录后的这些字节另赋义。
6. fm 旁证仅核对形状：fm off `0x22e8cb3: 6e 67 4c 50 48 89 45 e8 48 8d 7d e8 48 89 f1 48` 与 editor `0xebf063` 相同；fm off `0x22dfa8c: 48 8d 91 5c 01 00 00` 首次读的对象成员一致，`0x22e16ab: c6 44 24 28 00` 同样写前导标记。不以此冒称 fm 全调用链逐项同构。

## 3. 客户端新增 18 个业务槽（L3）

偏移和宽度为十进制字节，成对的对象偏移为十六进制。`访问` 为 4CC 等值分支上的成员访问；其前置 `cmp`、分支字节和完整 I/O 片段均在 JSON `row_offset_map` / `row_codec.cursor_layout`。

| 4CC | row+ / 宽度 | COMP+ | 访问：off / bytes | 流：对应宽度指令 off / bytes |
|---|---:|---:|---|---|
| `cfcl` | 3 / 2 | 0x120 | `ec0f7b: 41 8b 8c 24 20 01 00 00` | `4330d19: 41 b8 02 00 00 00` |
| `cbcl` | 5 / 2 | 0x124 | `ec353a: 41 8b 8c 24 24 01 00 00` | `4330d5e: 41 b8 02 00 00 00` |
| `ctcl` | 7 / 2 | 0x128 | `ec38f7: 41 8b 8c 24 28 01 00 00` | `4330da4: 41 b8 02 00 00 00` |
| `levl` | 15 / 1 | 0x1a2 | `ec4672: 41 0f be b4 24 a2 01 00 00` | `eb70ab: 41 b8 01 00 00 00` |
| `CTty` | 18 / 1 | 0x1a5 | `ec47b8: 41 0f be b4 24 a5 01 00 00` | `eb711a: 41 b8 01 00 00 00` |
| `cmnl` | 76 / 2 | 0x154 | `ec33aa: 41 0f bf 84 24 54 01 00 00` | `eb7a74: 41 b8 02 00 00 00` |
| `cmnw` | 78 / 2 | 0x156 | `ec3576: 41 0f bf 84 24 56 01 00 00` | `eb7a9a: 41 b8 02 00 00 00` |
| `cmxl` | 80 / 2 | 0x158 | `ec37a4: 41 0f bf 84 24 58 01 00 00` | `eb7ac2: 41 b8 02 00 00 00` |
| `cmxw` | 82 / 2 | 0x15a | `ec212c: 41 0f bf 84 24 5a 01 00 00` | `eb7aea: 41 b8 02 00 00 00` |
| `cnor` | 84 / 4 | 0x80 | `ec0fe7: 49 8b 8c 24 80 00 00 00` | `eb7bd0: 41 b8 04 00 00 00` |
| `csou` | 88 / 4 | 0x88 | `ec39f4: 49 8b 8c 24 88 00 00 00` | `eb7bf6: 41 b8 04 00 00 00` |
| `cwes` | 92 / 4 | 0x90 | `ec38e5: 49 8b 8c 24 90 00 00 00` | `eb7c19: 41 b8 04 00 00 00` |
| `ceas` | 96 / 4 | 0x98 | `ec3416: 49 8b 8c 24 98 00 00 00` | `eb7c3c: 41 b8 04 00 00 00` |
| `wbcl` | 101 / 2 | 0x14c | `ec3221: 41 8b 8c 24 4c 01 00 00` | `3502604: 41 b8 02 00 00 00` |
| `wbst` | 103 / 4 | 0x140 | `ec07af: 41 0f b7 8c 24 40 01 00 00` | `eb7cba: 48 8d 8b 40 01 00 00` → `39dd7c8: 41 b8 04 00 00 00` |
| `wben` | 107 / 4 | 0x144 | `ec3262: 41 0f b7 8c 24 44 01 00 00` | `eb7cd1: 48 8d 8b 44 01 00 00` → 同上 |
| `cuae` | 111 / 1 | 0xf7 | `ec10bc: 41 8a 9c 24 f7 00 00 00` | `eb7cf5: 41 b8 01 00 00 00` |
| `csso` | 112 / 1 | 0xf8 | `ec21e9: 41 8a 9c 24 f8 00 00 00` | `eb7d18: 41 b8 01 00 00 00` |

- 例：row 7 基址 payload `0x387`，`cmnl` 在 `0x3d3: 1a 04` → 1050；getter `0xec33ba: f3 0f 5e 35 6e 17 8b 00` 除以 `0x1774b30: 00 00 20 41`（10.0）。`levl` 在 `0x396: 00` → tier 1（`0xec467b: 83 fe 64` 排除空值 100，`0xec4c84: ff c6` 加 1）。
- 颜色是 2B 中的 3 个 5-bit 通道，不是内存里的 4B（例 `0x4330d36: c1 e9 07 80 e1 f8 88 4f 02`）。`wbcl` 只有 `row+100 != 0` 时占 2B（`0xeb7c9c: 80 7c 24 48 00 74 17`）；本样本全行标记为 1。row 7 的 `0x3eb: 01 c0 7f`、`0x3ee: 31 01 e1 07`、`0x3f2: 3b 00 e2 07` 分别是标记+颜色、起止日期原字节；两日期的写 helper 各传 2+2B。
- 内部码 `Ccre@+17`、`lbc␠@+60`、`cosr@+113` 有机器链，但未与 `comp.xml#comp` 的 schema 名对齐，**不计入 18**。`+0..1`、第 4/5 个颜色、两组版本化 byte 数组等保留为已知宽度/未命名；不按数值范围猜字段。

## 4. 五个原锚点与身份命名勘误

- `ccti@+52`（对象 `+0x58`，`0xeb725c: 48 8d 53 58`）、`cnti@+56`（`+0x60`，`0xeb727c: 48 8d 53 60`）、`cpcm@+64`（`+0x68`，`0xeb72bc: 48 8d 53 68`）分别传 4B。全量复验 b47 的 10 组洲/国家锚点和两组 parent：row 7 payload `0x3bb: 02 00 00 00`、`0x3bf: 8b 00 00 00`；row 250 `0x7c48: 01 00 00 00`、`0x7c4c: 37 00 00 00`；row 639 `0x13d47: ff ff ff ff`；North/South 两行 `0x15f0b` / `0x15f8a` 均为 `60 01 00 00`（parent row 352）。
- `+114` 的 4B 行号和 `+118` 的 8B 重复 ID 块确认 7,047/7,047，全部 ID 唯一；row 7 payload `0x3f9: 07 00 00 00 0b 00 00 00 0b 00 00 00`。`0xeb7d84: e8 b7 65 0f 00` 经 thunk 到 `0x3c60106: 48 8d 5f 08` / `0x3c6010d: 41 b8 0c 00 00 00`，一次读 12B 到 COMP `+8/+0xc/+0x10`。
- **保留 b47 字节锚点的标签，不把标签当原生属性。** COMP getter 在 `0xec4820: e9 fb ec 11 00` 委托基类。`dsha` 读 `obj+8`（`0xfe3c5d: 41 8b 74 24 08`）→ `+114`；`duni` 读 `obj+0xc`（`0xfe3bff: 41 8b 74 24 0c`）→ `+118`；原生 `rdui` 比较 `obj+0x10` 与 `obj+0xc`（`0xfe389d: 41 8b 74 24 10 41 39 74 24 0c`），对应保存的 `+122`。基类写侧 `0x3cc14da: 83 7e 10 00` 测第三 dword 为 0 时改写出第二 dword；不能因此把磁盘重复的两 dword 当成单一 64-bit getter。

## 5. server 交叉验证、标签勘误与边界

- 按 12B 身份进行有序 join：7,047/7,047 行都验证 `client[0:70] + 扩展 + client[70:127]`，含约定的行界字节。扩展众数 71B（6,340 行），所以 198B 是**众数，不是固定步长**。若扩展长 E，尾部身份起点为 server row+114+E。例 row 7 在 `0x1380`，E=226，身份在 `0x14d4: 07 00 00 00 0b 00 00 00 0b 00 00 00`。
- 扩展首槽是 server `crep@+70`：`0xeb73a6: 48 8d 93 80 01 00 00` / `0xeb73b3: 41 b8 02 00 00 00`，与 getter `0xec3808: 41 0f bf b4 24 80 01 00 00` 会合。server row 7 payload `0x13c6: b9 00`（185），row 639 `0x25982: c8 00`（200）。client 此处已跳过扩展；不能把 `crep/PLgn/dbty` 的扩展位置当 client 槽，也未给全部 server 扩展赋义。
- `ccti` 的引用包装 `0xfe6e90: ba 74 6e 6f 63` 传 `cont` 给 `0xfe68b0`（VA `0x140fe72b0`）；同类 `cnti/Nnat`、`cpcm/comp`、`csou/city` 逐一核验。`0xfe68e4: 8b 43 04 48 c1 e0 20 48 63 1b 48 09 c3` 合并两个 ID dword，`0xfe68f6: 48 83 c0 48` 取 i64 trait；就此调用，`cont` 是**大洲引用标签**，不是 container，也不是 `.dat` 行 wire type。17 标签旧普查仍可比对，不能推出 DBC/XML→工厂→`.dat` 的完整路径。
- 仍开放：未命名成员的 schema 语义、其他版本/模式、精确 archive opener→表循环实例、helperA 的外层消费者和 server 扩展全解析。未改既有账本或冻结证据；未安装依赖、启动游戏/编辑器/IDA 或做加载试验（**L4=0**）。

## 复验（从 `fm24-db` 根目录）

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01f/verify.py --selftest
py -V:3.12 -I -B scripts/t01_anchors.py --json
```

`--selftest` 校验静态字节、行宽/分支、7,047 行及 server join，包含错版本、内联名称、缺冬球色和错误边界标记的负对照，比对既有 `output.json`。`--write` 只重建 inbox 的 JSON。原锚点护栏 7/7；这不是游戏读写验证。
