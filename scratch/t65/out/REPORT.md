# t65 — Nation `table_10` 主行第二轮投影普查

**327 个 E94 unmapped occurrence：9 转入本轮 held，318 仍 unmapped，新增 L3=0，L4=0。** 新增静态同成员绑定只有 `rdui`，但两档均无可见 getter 值；另外 8 项有精确 getter gate、没有证明同对象主行 cursor。其余 19 条非 `unmapped` 基线记录不动，包含 5 项 L3 和 `Necf/Nygn/Ngct/Nsod` 四个既有定位 held；后两者的 scoped enum 结论引用 t61，不重判。实际公共 schema 是 **v9**，`nation_main_row_fields` 与 t55 嵌入记录一致，未改。

## 静态扫描与裁决

静态输入为只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`；指令按 **PE file offset** 引用，JSON 附 VA 和原字节。master 与 `IDA_PROVENANCE.md` 均对照 `evidence/MANIFEST.json`；master SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`。

- **沿用 t55 唯一行框/主 CFG**：slot 19 `0x103fac0..0x1040be4`（入口 VA `0x1410404c0`），992 条可达指令、109 条条件分支、0 条 extent 外边。先用冻结 CFG 裁掉两个 mode 分支的 server 边，再证 25 个缺席位置不可达。未把内存维护、I/O 失败边或 3 个 loop 内直接调用列成额外外层位置。
- **按 case-sensitive 4CC 查 gate、按对象查 sink**：slot 2 `0x1041f30 → 0x1041f40` 本地 getter 1,894 条可达指令；`0x104334d → 0xfe3520` 基类 fallback 1,397 条。两者共 24 个命中冻结 4CC 的 `cmp` + 等值分支，其中 9 个在本轮目标集。`0x1043322` 转发给 `this+0x108` 所指对象，不追；基类有 `0xfe3560` runtime registry 和三条间接尾边，不外推其所有分派。`0xfe4b47` 的 `+0x50` 虚调用在 NATION vtable 落到 `0x1041eb0`，取 `this+0xf0`，不是未知 raw 列的通用 accessor。没有按 XML 顺序或直方图相似度配字段。
- **gate→helper→cursor**：发布 10 条集合/计数三元组（含 A/B/C/D 的已接受主行 span），以及 9 条新 4CC 尝试。例：`+0x78` 从首 mode gate 到 `0x1040592 → 0x104e6b0 → 0x3d74e30`，`0x3d74e62` 读 count，非零才进 `0x3d74f9c → 0x1072560 → 0x3daa110`。item 八个转移是 `1+4+4+1+1+1+1+1=14` B；58 个 item 首 byte 均为 `01`，首例 server row 52 `@33627`。首 byte 读到栈上，不给它凭空造类型化 4CC。`+0xd8` 则是 count 非零后 `0x1040529` 的 4 B 与 `0x104053f/0x1040554 → 0xdb7f80 → 0x39dd7b0@0x39dd7d4` 两次 packed date；维持 t55 的 12 B item 口径，不命名日期。
- **位投影**：在 t55 主 extent、两 getter 及 4 个相关 reader/helper extent 共列 47 条 shift/mask 指令。`0x1043605/08` 是既有 `Nndn` 的 u16 `shr 9 / and 1`，不是全字非零，也没有复评级。`0x10427a9/0x10427db` 的 `&0x1ff` 在 `+0xc0` 集合项/上下文日期比较；其他候选是向量步长或句柄/上下文装箱。`nhrl` 的 `setne` 比较另一对象的首尾指针，不是 byte bit。未得到 t59 的新 byte `shr/and` 或 `cnst` 类结论；327 项中 53 项声明 scoped `enum_ref`，没有 `cnst`，这 53 项均无本轮绑定，不能从旁边字节填枚举域。
- **按 t53 TCrs 的裁决格式区分来源**：getter 对象路径与 `table_10` sink 分列。`rdui` 两者在同一个 `this+0x10` 闭合；名称类等只有 getter 一列。未找到 Nation `table_10` 主行里能闭合到这些 getter 的 TCrs 式类型化后缀；不因此把别的成员宣称无存储，也未进入 `t9/extra_9` 查后缀。

| 新 held | gate → 首个反证或证据缺口 |
|---|---|
| `rdui` | `0xfe3862 → 0xfe389d/0xfe38a2/0xfe38a7`：比较 `this+0x10` 与 `this+0xc`，相等即跳过输出。reader `0x1040bcf → 0xfae340 → 0x3c60119` 向 `this+8` 读 12 B，末 lane 是该值。首 client `@74:05000000`，server `@641:05000000`；两档各 251/251 抑制。|
| `Nnam` | `0x1042222`；`0x1042cde` 把对象装进 wrapper，`0x1042d62` 给 `long` selector，`0x1042daf` 调 formatter；非内联串 cursor。|
| `Nsnm` | `0x104225c → 0x1042fde/0x1042ff8`，`this+0x20` 字符串指针，无 t10 写点。|
| `N3ln` | `0x10420a1 → 0x10425a3/0x10425bd`，`this+0x28` 字符串指针，无 t10 写点；不能把 XML 的 3 字符上限应用到未知 raw 列。|
| `Nnty` | `0x1041f9c → 0x1042627/0x1042641`，`this+0x30` 字符串指针，无主行 sink。|
| `nhrl` | `0x104251e → 0x104252a..0x1042548`，比较 `[this+0x108]` 所指对象的 `+0x4a0/+0x4a8`。|
| `dbnm` | `0xfe375d → 0xfe3774/0xfe3796`，虚拟名称 provider 加 formatter，未闭到主行 sink。|
| `ttcl` | `0xfe35bc → 0xfe35d4/0xfe35ea`，转发到对象查找或 `fcol` fallback，未闭到本行颜色 sink。|
| `tbcl` | `0xfe3980 → 0xfe3f37/0xfe3f4d`，转发到对象查找或 `bcol` fallback，未闭到本行颜色 sink。|

后 8 条的首反证是静态地址，不填伪造的实档 offset。318 条 `unmapped` 意为在有界扫描中未见可对接的精确 getter gate，不是持久化不存在。`field_map_r2.json` 为 346 条逐 occurrence 台账；只在原 327 条内记本轮状态及冻结 XML `min/max/max_length/enum_ref` 等。没有同对象 wire 绑定就没有可检域样本，不能靠 raw 值看似落界晋级。`rdui` 冻结 XML 只给 `integer`，无 min/max/enum_ref；两档 raw 范围 `5..82082540`，但 0 条可见 getter 值，故 held。

## 双档封口与负对照

从成员目录的 `data_base+offset` 起、在 packed 边界内按声明大小选唯一 frame。双档各 251 行，**client `13+24710+9=24732`，server `13+422323+9=422345`**；15 个共同位置每位置 251/251 字节一致。13 B 是历史借用下一 selector/末行借 footer 首 byte 的坐标；原生 identity 三 lane 是 **12 B**，footer `00000000 | 01 | ec7ae404`。`Nftb/Ntxr` 仅消费 t55 冻结 opaque span，不重读子项。

引用对照按目标实表逐行 identity 得 ordinal/UID 两集，不按头部上限。没有新的具名引用达到读写链。本轮只把既有 `Nnsi` 作正控，不重新裁决：server t21 有 48,413 个实际目标，`208 hit / 0 miss / 43 null`；当 UID 用只命中 79，首错 row 1 `@646:da2f0000=12250`。两档 `rdui` 则相反：与实际 t10 ordinal 集碰巧 92 命中、159 miss，但与 UID 集 251 全中；`5` 解释为 ordinal→UID 10、按 UID→ordinal 0。它是 identity lane，**不是**引用。保留 pos 5/6/7/21 的假 t10 引用控制及首 miss；pos 35/36 全 `ffffffff`，0 live 不算通过。合法 ordinal `0` 不混入 `ffffffff` 哨兵。

## Client 缺席的 25 个 server 站点

`0xf2ba38` 转发 caller mode；reader 在 `0x103fae6`（前置）和 `0x10409d3`（后置）对同一个栈 byte 判零。下表前 13 项只在前门 **mode≠0** 执行，后 12 项只在后门 **mode≠0** 执行。两档 selector 都是 0，不能拿它当 mode。每项都有 **server 251 次外层消费 / client 0 次**；表中为首行 raw，全集的坐标来自 t55，重读所得总字节数、区段 SHA、范围、distinct 和 count 直方图见 JSON。t55 强套错模式的反例字节也复查：client mode 1 `@7188:05021700` → count 1,507,845；server mode 0 `@38:a6` → A count −90。

| Pos | 转移 / NATION 成员 | 定性 | Server row 0 `@offset:raw`；全档摘要 |
|---:|---|---|---|
| 1 | `0x103fb0e / +0x118` | `Nnsi`，原引用 | `@14:ffffffff`；208 live |
| 2 | `0x103fb37 / +0x128` | i16 count + 4B/item，不命名 | `@18:0000`；251 count=0，`0x103fc63` 未进 payload |
| 3 | `0x103fe72 / +0x158` | i32 count + 4B/item，不命名 | `@20:00000000`；251 count=0，`0x103ff2a` 未进 payload |
| 4 | `0x104011f / +0x170` | `Nftb` 父跨度冻结 | `@24:0000`；7 项、250 空行，首非空 row 162 `@278809` |
| 5 | `0x1040360 / +0x184` | raw32 | `@26:2ad60000`；243 种 |
| 6 | `0x1040384 / +0x188` | raw32 | `@30:bffa0100`；243 种 |
| 7 | `0x10403a8 / +0x18c` | raw32 | `@34:da0a0000`；191 种 |
| 8 | `0x10403cc / +0x190` | raw32 | `@38:a6040000`；222 种 |
| 9 | `0x10403f0 / +0x194` | raw32 | `@42:1f0e0000`；225 种 |
| 10 | `0x1040414 / +0x198` | raw32 | `@46:1c000000`；89 种 |
| 11 | `0x1040462 / +0x60` | `Ntxr` 父跨度冻结 | `@50:08000000`；1,899 项、30 空行 |
| 12 | `0x10404d1 / +0xd8` | u32 count + 12B/item opaque | `@254:17000000`；27,178 项、87 空行 |
| 13 | `0x3d74e62 / +0x78` | helper u32 count + 14B/item opaque | `@534:00000000`；58 项、232 空行；首非空 row 52 `@33623` |
| 27 | `0x10409f0 / +0x1a4` | raw32 | `@590:6b011442`；231 种 |
| 28 | `0x1040a14 / +0x1a8` | raw32 | `@594:ae47b641`；231 种 |
| 29 | `0x1040a38 / +0x1b0` | raw32 | `@598:ddc11741`；231 种 |
| 30 | `0x1040a5c / +0x1ac` | raw32 | `@602:006f02c1`；231 种 |
| 31 | `0x1040a80 / +0x1b8` | raw32 | `@606:d5030000`；201 种 |
| 32 | `0x1040aa4 / +0x1bc` | raw32 | `@610:cb030000`；200 种 |
| 33 | `0x1040ac8 / +0x1c0` | raw32 | `@614:e7880e00`；225 种 |
| 34 | `0x1040aec / +0x1c4` | `Npop`，不在冻结 XML | `@618:241d9d02`；232 种 |
| 35 | `0x1040b10 / +0x17c` | raw32 | `@622:ffffffff`；常量 |
| 36 | `0x1040b34 / +0x180` | raw32 | `@626:ffffffff`；常量 |
| 37 | `0x1040b58 / +0x1c8` | `Nndn`，原 u16 位投影 | `@630:0000`；整字 2 种 |
| 38 | `0x1040b7c / +0x1ca` | raw8，未证 bit | `@632:00`；常量 |

## 复跑

独立 verifier 不 import builder、ReaderCFG 或 `fm24_dump`：自解 FMF 目录和成员帧，对冻结 t55 分区校验全档边界，独立重算 ordinal/UID 对照、profile 和 getter 抑制，并核对 PE 原字节、辅助 extent 可达范围和静态 gate。两脚本 `--help` / `--selftest`、build / verify 均过；`t01_anchors.py` **7/7**。未启动游戏、编辑器、IDA，未联网、未读写 Z:，未读 person/PDxx、t9、extra_9 或改动公共 schema。

```bash
export FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data
py -V:3.12 -I -B scripts/t65_nation_unmapped_r2.py --build
py -V:3.12 -I -B scratch/t65/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py
```

退出码：0 通过，1 校验未过，2 用法或致命错误。
