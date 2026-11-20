# t57 — Club `table_3` 主行槽位普查

**当前双档行框和外层序列全闭合：client / server 各 84,259 行，34 个逻辑位置。字段命名仍是 partial。** 冻结 `club.xml#club` 433 个顶层 occurrence 中，18 个与外层槽或投影对齐，13 个通过本轮 L3 闸门，其中 **5 个新增：`Cext`、`Cedp`、`Cncl`、`CIns`、`Ctsi`**。11 held、10 个独立成员父项跳过、399 unmapped。原 t24 client 证据不撤销；其 `Csnm`、`PLgn` 不计入本轮 13 个双档门槛结果。L4=0。

## 行框：数据侧先验与 reader 互证

| 档 | 封口 `header + Σrow + footer` | 原生行宽 | payload SHA-256 |
|---|---|---|---|
| client | `13 + 6,932,060 + 9 = 6,932,082` | 54–156 B | `db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f` |
| server | `13 + 16,595,290 + 9 = 16,595,312` | 81–2,618 B | `77ebce41936acd17ac798def913c456aa78db77a9acf01f6f440d4b9867716bc` |

以 `data_base+entry.offset` 的成员界限解压，逐帧按目录声明大小唯一选中。四种对齐遍历所有候选 triple，按 ordinal 分层做非重叠路径计数；不把行号喂给 reader 选择分支。原生行真正末尾为 **12 B** `ordinal | UID | UID`。两档末尾之后均为 `00000000 | 01 | e3c03a77`；`ordinal=0..84258`、UID `57..2000339171` 非零严格递增且唯一，重复 lane 与双档逐行相等。`field_slots.json` 附两套原点的敏感性与原生游标的逐行摘要。

- 强制 t50 式 **13 B 且末 byte==0** 的假设两档均在 ordinal **69705** 断开：首反例 client `@5705237` / server `@14067615`，raw `491001003145d8053145d8050c`。末 `0c` 是**下一条记录的 selector**；三条 derived 为 69706–69708，而非前移一条。把 lookahead 放宽到 `{0,12}`，13 B / footer 8 的数据分区与 12 B / footer 9 等价；这不是 13 B native identity read。
- 不检查 lookahead、但保持非零及递增，双档仍各 1 路；放开 UID 递增则 **4 / 96** 路，放开非零则 **1 / 23** 路，两者都放开 **4 / 2,400** 路（client/server）。12 B 判据下，footer **7/8/9/10/12** 的完整铺法均为 **0/0/1/0/0**。header 11–15 在数据侧都可用，**不由 triple 唯一决定**；loader 的首 selector 与逐 transfer replay 才把原生 header 定在 13。
- t44 的 `CLUB_LINK` 用过 t3 键身份；本轮数据侧先从各档独立枚举，reader 随后从 `@13` 顺读，不靠寻找 identity 修补游标。全档强制交换 mode 均失败：client mode 1 首错 row 0 `@3718`，`base78` 读出 −43；server mode 0 首错 row 0 `@96`，误读 identity `(4294967295,2785017856,2)`。

## 静态链与槽位数

只读 `<OLD_REPO>/input/editor.exe` SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。冻结 master SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`；master、`IDA_PROVENANCE.md`、`db_tables_big.json` 和 `DB_TABLES_BIG.md` 对 MANIFEST 核验。下文代码地址为 **PE file offset**；VA、原始 bytes、后继见指令分片。

- Factory `0xf48b30` 的 `0xf49d38` rel32 表格 case 3 (`0xf49d44`) → `0xf48daf`。`BL!=0x0c` 到 `0xf49c34`，`0xf49c3f` 调构造器 `0xe59a40`，经 `0x3aad0fd` 取 `CLUB` vptr VA `0x14187cd08`。`BL==0x0c` 先调用同一构造器再写 derived vptr VA `0x1418bfbf8`。`CLUB` slot 2 是 `0xe89a00`（不是 t39 的 NATION `0x1041f30`）；slot 19 `0xe5a7a0`（VA `0x140e5b1a0`），PE exception extent `0xe5a7a0..0xe5bfca`，**1,412 条可达指令 / 167 条条件 / 0 extent 外边**。Derived slot 19 `0x157cff0 → 0x43beba0`，后者 68 条指令，`0x43bec5b` 是到 base `0x11d0d30` 的 tail jump，不是循环。
- `ReaderCFG` 对主、derived、限定的字符串、flush、base、tag-0 与日期 reader 生成可达图。CLUB extent 的 **41 次直接 `stream+0x28`** 分开记为 16 scalar/count（含 compact 替代 flush）、17 collection item/终止 flush、8 替代路径或现代成功路径无 pending width 的站点；**不等于 41 个外层业务字段**。共交付 407 条条件的谓词/后继；生命周期或目前不明的分支保留，不按未观测推断死边。
- `0xf2ba0e` selector 与 `0xf2ba38` 转发的外部 mode 分离；`0xe5a9ba`、`0x11d0fa4` 控制 CLUB 与 base 扩展；`0xe5bc3c` 控制 base 调用归属。Mode 0/1 按实档封口反证，不主张实机已观测。两档均有 **84,256 条 selector 0、3 条 selector 12**。逐 ordinal 配对后，84,259/84,259 条 server 行比 client 长，加长 26–2,547 B。每条 client 行有 **14 个**逻辑事件（compact 用两个 derived 前缀替代两个空文本 payload 事件）；server 普通行 **32 个**、compact **31 个**。集合按 `count + item spans` 记一个外层位置，物理 call 可能合并 flush；`execution_index` 按实际模板，不按地址或 XML 排序。带前缀的字符串分别记 len 和有内容时的 payload。`field_slots.json` 的坐标 SHA 含全表 `(ordinal, absolute, span)`，可用游标重建。
- Server 新增：`+0x16a/+0x166/+0x148/+0x16c`；`+0x110` count×4；`+0x150` tag 0→`0xe5aef1 → 0x1476470 → 0x423fef0` 的 `4+1+3+13+4+20=45 B`（84,256 次），tag 2 无该项（三条 compact），tag 1 仅静态存在、未重放；`+0x130` count×24；`+0x138` count×12；`+0x168/+0x140`；base 的 `+0x18/+0x30/+0x60/+0x78/+0x90/+0x48/+0xa8` 七段（item 宽 `4/4/4/4/4/16/28`）。`+0x30` 计数有站点、item 此档全空。除下表经 proof 的投影，不给 opaque item 命名。
- 跳过 v6 的 `Cstc/Clhs/CSrs/Cmti/CNtp/Cdbt/Tchl/Csme`；v6 按本地 git 对象 `8b04fc2` 固定，以免共享报告滚动到 v7 改变依据。`Cafl/Cvfl` 是 t44 同一个具名 `club_links.dat`，`+0x118/+0x120` 不作 t3 wire 槽。t39 的 `Tchl` helper / 共享且本档 live owner 属 national-team selector 的结论原样保留。`base48` 是 **别的**内嵌集合，不是上述边界的替代。

## 映射与闸门

冻结顶层唯一 occurrence → 精确 4CC / 同对象成员 → reader sink → 全档值域。对齐子集出现 **72 对倒置**（同物理槽不人为排序），首例是 `Cext` wire 位置 3 / XML 13 早于 `Cnam` 位置 10 / XML 6；全表倒置记在 `field_map.json`，不硬配。XML 显式域逐字段使用，`Cprs`、`PLgn` 无 scoped `enum_ref`，不补标签；未绑定的整数/real 不用数值“像”来晋级。实表 ordinal 集：t2 56,293、t3 84,259、t10 251、t21 48,413、t25 7,047，各双档逐实际 triple 验证。t10 只复核 t47 既有身份坐标，t25 server 用 client exact triples 的前向最早/后向最迟一致性，不命名 comp 业务字段。Nullable lane、有效 0 和 UID 控制分开计数。

| 新 L3 | 路径与全档证据 |
|---|---|
| `Cext` | `0xe8c8ef → 0xe8d972/0xe8d982` 检验修复后 `CLUB+0xd8` 为空。与 `Cnti` 共用 `0xe5a81a`，不是额外 Boolean byte；每档 28,331 真 / 55,928 假。 |
| `CIns` | `0xe8afac → 0xe8dc37/48/4b`，`+0x160` dword 的 bit 10（6 B block 的 byte 1 / `0x04`）；每档 1,285 真 / 82,974 假。 |
| `Ctsi` | Training Ground，`0xe8c57d → 0xe8c589` 取 `+0x140`，`0xe5bc6b` 或 derived `0xe5bccc` 读，`0xe5c626/0xe5c633` 接 stadium fixup。Server 9,403 live 全命中，74,856 null；首 row 0 `@164` ordinal 44,133 → UID 2,000,127,458。Client 缺站点。**不是 `Csti`**。 |
| `Cncl` | `0xe8ab01 → 0xe8d39d → 0xe74ff0 → 0x3ae4a50`；从 base `+0x48` 取 item `+0xb==0x37` 且 `+0xa==1`，首 dword 为 club ordinal。`0x11d2aa9 → 0x1105860` 按 **`+0xa` 而不是 `+0xb`** 走 rel32 case 1 `0x110589d`，取 context `+0x10`、调用 `0x11058b4 → 0xf7e440 → 0x3bf3460`，与 t44 的已知 club resolver context 同位。保留兼容/重映射分支。Server 3,021 个 type-1 live 全命中、81,238 无该投影、0 多 tag；首 row 43 `@30177:39340000` 即 ordinal 13,369 → UID 5,605,072；若误读 UID 只命中 262 个 live。Client 缺站点。 |
| `Cedp` | `0xe8c3b2 → 0xe8c3c1 → 0xe63110 → 0x3ac1f90` 在同一 `+0x48` 集合按 item `+0xb==0x6f`、用 `+0xc==3` 投影；不是独立一字节。首 true row 1432 item `@860924:5e060000000000000000046f03ff00ff`。Server 28 真 / 84,231 假，0 多 tag。Client 无集合，不发布该档坐标。L3 限于 wire item 投影，不声称实机引用修复后的 Team 指针状态。 |

其余通过本轮 L3：`duni`、`Cnti`、`Cbni`、`Cccn`、`Ccty`、`CASt`、`Csot`、`CnCV`。`Cccn@旧row+8` 的 E60 negative 原文保留；真正绑定的是 `+0xf0` 第四次 u32 transfer，`+0xe8` 第三次为 `Cbni`。`Ccty` 每档 74,079 live / 10,180 null，0 miss。`Cbni` getter fallback 不改变 raw lane。

**Held 首反例与边界。** `Csnm` 槽保持 t24 静态证据，但 XML max 25 下每档 537 条越界，首 client row 1428 `@107960` 27 个 Unicode code points；`Cnam` 的 `+0xc0` backing text 不等同本地化 getter，首 `@44`；`PLgn` 无 scoped enum，首 client `@95:00`；`Cprs` `+0x16a` 首 server `@93:02`，不把 raw 当完整枚举语义；`Cdof` `+0x148` 首 `@96:ffffffff`，不读 person 表扩域。`CLat/CLon` 的精确 getter 分支装箱 0，不能把城市/球场坐标贴成 club 坐标；`Csti` 的单样本正探针和控制负结果不足；`Crep` 和 `Cdvi` getter 走首 Team 间接对象，不映射到 t3 同一对象原始 lane。`Cyfn` getter `0xe8e6a9/e8e6b1` 是 `CLUB+0x100 → extra+0xd8`，不写成主行槽。其余 399 项未对齐，不判定无 wire。

## 回归、复跑与交付

- Liverpool club ordinal 460 / UID 676 → city ordinal 1061 / UID 100047，双档同值。City `53.408371,-2.991573`，Anfield `53.430820,-2.960832` 是不同对象；Bernabéu ordinal 430 / UID 1056 容量和座位均 **81,044**。Old Trafford 74,031 ≠ 74,140 原样保留。冻结旧样本 Shanghai Port 的 *candidate order index* 32354 实际是 Urumqi Hatira（city 10149）；按准确名称定位 ordinal 32356，双档均指 Shanghai 1693。原错误坐标和反例保留，不通过换偏移“修复”全列。
- 成立年仅复验冻结 14 个 `client/table_extra_3` 同 ordinal witness（不重新普查 sidecar）：Liverpool 1892、Arsenal 1886 等 13 个精确，Manchester City 保留档值 1894 / 外部起源 1880 的约定差异。Competition 只读 t01f 接受的字节夹具与 identity：England=139→765、China=55→110、parent=352→150990；不解析 comp 业务槽。
- `verify.py` 独立解目录、重建 PE CFG、反向数据 DP、重放全量行/坐标/字段域及旧锚点。不 import builder、`ReaderCFG`、`fm24_dump`。`--help` / `--selftest` 双脚本通过；全量 verifier 通过；`t01_anchors.py` **7/7**。退出码 0 成功 / 1 检查失败 / 2 用法或致命错误。未启动游戏、编辑器、IDA；未联网或访问 Z:。

```text
FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t57_clubmain_fields.py --build
py -V:3.12 -I -B scratch/t57/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
