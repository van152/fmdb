# t55 — Nation `table_10` 主行槽位普查（字段命名 partial）

**现代双档外层序列闭合：server 40 个位置，client 执行其中 15 个；各 251/251 行。** 冻结 schema 15/346 个字段连到候选槽位（4.34%），其中 5 个标量通过本次 L3 闸门（1.45%）：`Ncti/Nrgi/Ncur` 沿用既有静态绑定并补全双档实表域，`Nnsi/Nndn` 在本次通过。4 个已定位标量 held，另有无分发证据的 `EDsc` held、`Nftb` 父 getter held。L4=0。`Ncpi` 是 t22 已验、在冻结活动 schema 中未出现的补充回归，不计入 346 或本次 L3。

## CFG 与坐标

静态输入为只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。下文指令地址为 PE file offset；指令分片附 VA、原字节和后继。冻结 `master.json` SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda` 与 `IDA_PROVENANCE.md` 对 MANIFEST 核验。

- NATION slot 19 `0x103fac0`（VA `0x1410404c0`），PE exception extent `0x103fac0..0x1040be4`：992 条可达指令、109 条条件分支、0 条 extent 外 CFG 边。40 个直接 stream `+0x28` 站点中，37 个属于外层；3 个是 opaque loop 内部（`0x103fcbd`/`0x103ff79`/`0x1040529`）。另列 `+0x78` 集合 helper 的 count、loader selector 和 identity，共 40 个外层位置。不是 40 个业务字段，也不把内存维护、分配、读失败路径当新字段。对未归类的分支只发谓词和边，不宣称其不可行。
- `0xf2ba38` 转发外部 mode；`0x103fae6` 和 `0x10409d3` 分别跳过首、尾扩展。双档 selector 都为 0，不能把它当 mode。Client 强制 mode 1 首反例 `@7188` count 1,507,845；server 强制 mode 0 首反例 `@38` A count −90。旧版、helper 的未观测分支及实际运行时状态均不外推。
- 两档从 selector 顺序消费到 identity，验证其三 lane 后才闭合行：server `13 + 422323 + 9 = 422345`，client `13 + 24710 + 9 = 24732`。两档首 identity `(0,5,5)`、251 组三 lane 一致，footer `00000000 | 01 | ec7ae404`。`legacy14` 行体原点是 selector 后 1 B，末位借下一 selector 或 footer 首 byte。JSON 坐标为 `[绝对起点, 消费跨度]`，用 `execution_index` 取 mode 内次序。
- `Nftb` 只做父跨度及四条字节长前缀画像（7 项，长度范围依次 5–7、4–11、0、0）；`Ntxr` 按 t47 的 tag/跨度口径重放，不重新命名。`+0xd8` opaque 每项 12 B：4B 未命名、两个 `db7f80 → 39dd7b0` packed date 读；各有 27,178 个日期，两 LE u16 的低 9 位为年内日、高 word 为年，此档余 7 位均 0，没有日历越界。首例 `@262`、`@266` 都为 2023 年第 182 日。不把它们归给 transfer window 或其他 XML 日期。`TCrs` 不在 t10 主行槽位序列。

## XML 对齐与三重闸门

统计分母仅为冻结的 346 个顶层 occurrence。15 个候选用 4CC/同对象成员或已有父集合证据对齐；**不是按 XML 序号对齐**。比较这个子集即有 46 对顺序倒置，涉及全部 15 项：首例 wire `Nnsi` position 1 先于 `Ncti` position 15，XML 21 却晚于 16。`field_map.json` 保留倒置与首反例；独立静态证成的字段不因 XML 展示顺序被重排。`debug_only` 不等于无 wire 槽；反例 `Nftb` 的 server row 162 `@278809:0700`。`EDfx` 只判定已追的生成输出无槽；其输入不作推论。`EDsc` 保留未找到分发的负结果。

| L3 标量 | 站点 / NATION 位移 | 实档域（live hit / miss / null） |
|---|---|---|
| `Nnsi` | `0x103fb0e` / `+0x118` | server t21 Stadium 208 / 0 / 43；client 跳过 |
| `Ncti` | `0x10405eb` / `+0xf0` | 两档各 t5 Continent 228 / 0 / 23 |
| `Nrgi` | `0x104060f` / `+0xf8` | 两档各 t19 Region 234 / 0 / 17 |
| `Ncur` | `0x1040657` / `+0x100` | 两档各 t41 Currency 229 / 0 / 22 |
| `Nndn` | `0x1040b58` / `+0x1c8` | server u16 的 `0x0200`：239 假、12 真；client 跳过 |

引用按目标档实际身份尾得到 ordinal 集，不按 UID、表头上界或值域相似猜表。各目标按双档走到 EOF；t41 用变长行走法。零和 `0xffffffff` 不混同；保存 wrong-UID 控制和首歧义。`Nndn` 借 getter `0x10435f3/605/608` 的确定掩码，而不是把此档碰巧等价的整字非零当算法；同字其余 bit 不命名。

- `Necf` `[1,20]` 却有 28 个 `0`，首 client row 121 `@8628`（server `@99394`）；`Nygn` `[0,100]` 却有 26 个 `−1`，首 client row 29 `@2102`（server `@17005`）。保留静态槽并 held，不自拟哨兵。
- `Ngct`、`Nsod` 有精确 getter 和 reader sink；冻结 occurrence 无显式 `enum_ref`，同名枚举只作线索，未作为 scoped 引用晋级。首 client row 0 `@14:01`、`@31:02`。`Npop` 有精确 key/同位移却不在活动冻结 schema，server 首 row 0 `@618`，补充 held，不报成 XML 名称。
- 17 个未命名标量保持 raw 宽度。比如 server `@590:6b011442` 可作有限 f32 probe，不足以证明 schema `real` 或业务含义；`@622:ffffffff` 所在列 251/251 都是全 1，不据此猜引用、金额或特殊日期。未找到通过闸门的顶层 cash、自引用、club/comp 或命名日期，不发布映射；不扩大到这些表侧。

## t46 A/B/C/D 收口

复用 t28 的集合绑定，两档都出现在**共同 24 B 前缀后**、server 43 B 尾扩展前。Server 增加可变长前置块，不能复用 client body 偏移。

| 段 → 字段簇 | Count site / 成员 | span | 首行 client / server 绝对 count | items（每档） |
|---|---|---|---|---:|
| A → `Nlns` 语言 | `0x1040717` / `+0x48` | `1 + 5A` | `38 / 562` | 492 |
| B → `Nefr` 视为欧盟 | `0x10407b0` / `+0xa8` | `4 + 28B` | `54 / 578` | 214 |
| C → `Nnfr` 视作非外籍 | `0x104086c` / `+0x90` | `4 + 28C` | `58 / 582` | 63 |
| D → `Nagr` 协议 | `0x1040927` / `+0xc0` | `4 + 12D` | `62 / 586` | 162 |

两档四段的 count 和完整消费字节逐行一致。B/C 共用 item helper，靠各自对象位移及 getter selector 区分，不能按 stride 命名。Server 首行 count 序列位于 legacy body `+548/+564/+568/+572`；旧 `+24` 的 `a6` 确实不是 A count。原 t46 文字和四条探针原样保留，`abc_closure.json` 给出解释；此收口不解释 server 未命名标量。

## 回归与复跑

`Ncpi` 复核 client body+9、t22 六个 holdout，双档各 231 个 city ordinal 命中、20 个空、仅 25 个错误 UID 控制命中、5 个异国 owner。England=139/UID 765、China=55/UID 110；parent 352 只验 t01f 已接受的字节夹具，不读 t25 成员。`Ntxr` 7 L3 不变；`TCrs` 4 held 不变。独立 verifier 不 import builder、ReaderCFG 或 fm24_dump。未启动游戏、编辑器、IDA；未联网或访问 Z:。

```text
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data
py -V:3.12 -I -B scripts/t55_natmain_fields.py --build
py -V:3.12 -I -B scratch/t55/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```

Builder、独立 verifier、两者 `--help`/`--selftest` 通过；t01 anchors **7/7**。退出码：0 成功，1 检查失败，2 用法/致命错误。
