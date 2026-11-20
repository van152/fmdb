# t34 — CNtp / table 66 静态 cursor 验收证据

**Server 753 行 × 24 B 全闭合；client 无 table 66。`nati`、`rati` 晋级 L3；`mina`、`maxa` 的静态字节槽已绑定，但与冻结 schema 的值域冲突，保留 held。L4=0。**

## 归档与行边界

| Archive | 目录条目数 | 成员 | Count | Stride | 解压 payload SHA-256 |
|---|---:|---|---:|---:|---|
| client | 31 | 不存在，不是空表 | — | — | — |
| server | 77 | `server_db/table_66.dat` | 753 | 24 B | `3ddd47bbeec04ff6789dafdfe40148367abc4373700b082452fc79be06e02911` |

Server 目录项 offset `24307967`，首 Zstd 帧 offset `24308001`（与 t29 `packed_offset` 相同），packed size `5834`。`load_payload` 从首帧得到完整 `18094 B`，不是 E66 空 stub 情形。两 archive 的 SHA-256、目录项及版本 `0x0df1` 见 `cursor_cntp.json`。

- **Wire**：`13 + 753 × (1 selector + 11 properties + 12 identity) + 9 = 18094`。先按可达 CFG 的传输顺序推进，再检查 identity、归纳 stride。零基行 `i` 的 selector 在 `13+24i`，body 在 `14+24i`，行尾 exclusive `37+24i`。753 条 selector 都为 `0`；loader 将它传入 factory，case 66 不检查该值。注入非零只触发 replay 的观察域限制，不是 native factory 拒绝。
- **Legacy**：`14 + 753 × 24 + 8 = 18094`。同一业务槽 wire 坐标 = legacy + 1；legacy `+23` 借下一条 selector，末条借 footer 首字节。直接比对 t29 的 profile、legacy block SHA、753 条 `.rows.jsonl` 原字节和各命名槽的 unsigned 统计，未重 dump。`subtable_inventory.json` 的 CNtp 页核对表号、RTTI、reader、idx 及文件哈希；其 `link_status=candidate` 原样保留，未用候选槽投票。
- **Identity**：legacy `+11` / wire `+12`，12 B 写对象 `+0x08..+0x13`。原始 lane0 等于 ordinal `0..752`；后两 lane 相等、非零且每条 UID 唯一，范围 `1..753`。先以原始 lane0 执行 native 阈值谓词，再对原始三 lane 做后置校验；不让 native ordinal overwrite 掩盖反例。
- **Footer**：绝对 offset `18085`，`00 00 00 00 | 01 | f1 02 00 00`。`0xffa602` 读 vector count，零时绕过每元素的三次 4 B 读。`0xf2baa2` 读 1 B 至 `table+0x58`，`0xf2bac2` 读 4 B 至 `table+0x50`。末 u32 `753` 同时等于最大 UID 和头部行数，不能判定其通用含义；独立的头部 u32 才驱动行循环。

## PE 静态链与五类分支

二进制仅只读 `<OLD_REPO>/input/editor.exe`（SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`）。`evidence/fm24/reports/qa/IDA_PROVENANCE.md` 及 `evidence/fm24/reports/editor_schema/master.json` 已比对 `evidence/MANIFEST.json`，后者 SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`。下文地址除标注 VA 外均为 **PE file offset**；对应原指令、bytes 与 VA 见 `instructions.part*.json`。

1. Factory `0xf48b30` 通过 `0xf49d38` rel32 表第 66 项进 `0xf49b18`；`0xf49b3c → 0xf49b43` 写 vptr VA `0x141884e08`。COL `0x1885660` → TD `.?AVSTARTING_CLUB_TRANSFER_PREFERENCE@db@@`。
2. Slot 19 VA `0x141530120` / offset `0x152f720` 是 leaf thunk；真 reader extent `0x43583b0..0x435847a`（VA `0x1444c39b0..0x1444c3a7a`，末地址 exclusive），69 条可达指令、7 块；实际 stream `vtable+0x28` 读宽依次为 `4,4,1,1,1`。成功处 `0x4358475 → 0xfae340`（leaf thunk）→ identity tail extent `0x3c600f0..0x3c6016e`（VA `0x143dcb6f0..0x143dcb76e`），43 条可达指令、11 块；`0x3c60119` 读 12 B。两个 extent 由 PE `RUNTIME_FUNCTION` 定界，以 `ReaderCFG` 建图；唯一外部 CFG 边是已追完的 tail jump。
3. **无 caller mode 谓词，不需 fork。** Loader 写入 stack `rsp+0x30` 的模式字节不读；属性 reader 保存/转发 R8D 和 R9，identity tail 从刚读的 lane0（超阈值时用 caller stack ordinal）重取 R8D、在 callback 前置 `r9b=1`。模式参数不改变传输宽度。

| 谓词来源 | Reader + tail / 外层切片 | 证据与首个反例 |
|---|---:|---|
| `wire_data` | 1 / 5 | `0x3c60131` 将刚读的 lane0 与 `10000001` 做 unsigned 比较。注入该阈值：`row 0: identity @25 raw=(10000001, 1, 1), stored ordinal=0`，仍不通过。外层是 count、循环、footer vector count。 |
| `runtime-external` | 0 / 1 | Factory `0xf48b3b` 用目录传入的 table type 检查上界；首行 type 66，不来自 selector 或 body mode。 |
| `IO-result` | 5 / 11 | 五次属性读后检查 `stream+0x10`，失败汇合 `0x4358452`，AL=false。首行短读：`row 0: short transfer @14 width 4 site 0x43583d9; IO-result -> 0x4358452 (AL=false)`。Identity bulk 短读 `@25 width 12` 无即时 native status test，仅声称 replay 拒绝。 |
| `context-lifecycle` | 4 / 3 | Tail 的 stream/null、callback/null、release/null、refcount。首行若注入 null stream，属性路径早在 `0x43583cd` 解引用，不是合法短布局。Callback 来自 caller stack 的 table this；callback、最终析构不展开，计数是 live retained-stream 合约下的 replay。 |
| `dead` | 0 / 0 | 不因观测中未走就删掉静态边，包括 footer 非零 vector 的传输与失败路径。 |

`branches.part*.json` 逐条记录谓词、来源、后继、首个反例或合约、reader/tail 分支访问次数；外层仅审计与本行游标有关的切片，不声称覆盖整个通用 loader。`cursor_cntp.json` 保存转移模板、两套坐标、全表 trace SHA、样本和合成负例。

## 三重闸门与字段台账

冻结 `club.xml/CNtp.list_item_fields` 与 t24 nested idx **46–49** 一一对应。Club 的 `CNtp` compare `0xe83d9a → 0xe84f11` 调 `0xea6420`；同一个 list helper 以父对象 `+0xc` 匹配子项 `+0x18`，构造时也写入该 UID（`0xea66cc → 0xea66f4`），并使用与 factory 相同的 vptr（`0xea66ea`）。其 item 4CC 写入与 class slot 3 一致。Class slot 2 getter VA `0x141530440` 以 EDX 精确分发四个 4CC；下表由 getter 的对象成员与实际 reader sink 相接，不按 schema 顺序或低基数命名。

| 4CC | 对象 | Legacy / wire | Width | 全表画像与等级 |
|---|---:|---:|---:|---|
| `nati` | `+0x1c` | `+4 / +5` | 4 | **L3**。单个 `i32` nation UID；753/753 命中实际 nation identity，131 个 distinct。`-1` 为构造缺省位型，和 `0` 区分；两值均未观察到。 |
| `rati` | `+0x20` | `+8 / +9` | 1 | **L3**。`movsx` 有符号 i8；`{0:34, 1:263, 2:211, 3:114, 4:88, 5:43}`。零走 getter 专门路径，不走普通数值装箱；`-1` 无该测试且未观察到。冻结 schema 无 `enum_ref`，不指派标签或断言全集。 |
| `mina` | `+0x21` | `+9 / +10` | 1 | **held**。静态 `movzx` 读 u8，非零 `14..32` 均在 `[14,44]`，但 436 个 `0` 不在域内。首反例 row 0 `@23=00`。 |
| `maxa` | `+0x22` | `+10 / +11` | 1 | **held**。静态 `movzx` 读 u8，非零 `17..45` 均在 `[15,45]`，但 395 个 `0` 不在域内。首反例 row 0 `@24=00`。 |

**`nati` 不是 ordinal，也不是 Cmti 式 pair。** `0x43583d9`、`0x43583f5` 是两个独立的 4 B transfer，各有状态检查；前者是父 club UID，后者才进入 `nati` getter `0x152faf0`。首行若误拼为 pair 得 `(13208139,133)`，第一 lane 来自父对象；无 copy-lane 规则。Slot 21 writer `0x4358a6e` 直接写出同一 4 B 成员；slot 20 为 `AL=true; ret`，没有 ordinal fixup。用 t25 已闭合的 client table 10 位置从本地归档重读 251 条 `(ordinal,UID,UID)`，实际 ordinal 域为 `0..250`；同时在 server table 10 中复核 251 个同序且唯一的原始三元组，不声称独立解析了 server nation 的行布局。Ordinal 假说共 **602** miss：首个 row 1，`@42 = 73 06 00 00`，值 `1651` 对应的 nation ordinal 实为 `189`。这是独立域检验，不是数值落在范围内作证；不推断其他运行时 alias 机制。

**年龄未证明 `0` 是 sentinel。** 两个 getter 直接 zero-extend 后装箱；保存原始 `0`，不改成 `-1`、不替换默认年龄。389 行两者都为零，47 行只 min 为零，6 行只 max 为零，311 行两者非零。原始 `min>max` 有 6 行，首例 row 57 `@1391` 为 `12 00`（18,0）；311 条双非零均满足 `min≤max`。两个 held 保留静态 `sink`，不发布通过三重闸门的 `row_offset`。无 scoped i16、bool 或掩码字段。

## 复验

使用本地镜像 `FM24_DB_DIR=<WORKSPACE>/scratch/data`，`py -V:3.12 -I -B`。Builder、独立 `verify.py`、两者的 `--help` / `--selftest` 均 PASS；独立 verifier 不 import builder 或 `ReaderCFG`，从 PE 重建两段可达图，从归档复算每行路径、边计数、反例、t29 差分和实际 nation 域。退出码 0=成功、1=检查失败、2=用法或致命错误（非法参数实测 2）。`scripts/t01_anchors.py` **7/7 PASS**。没有启动游戏、编辑器或 IDA，没有联网或访问 Z:。
