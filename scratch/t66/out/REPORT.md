# t66 — COMP 主行内派生集合普查

**双档母行闭合；7 个非空集合的物理文法 L3，4 条带活值的 ordinal lane L3。** 三个没有实项的集合和四条引用 lane 保持 held；未把集合或 item 映射为业务字段，未绑定新的独立子表，未声称 getter 后缀已解。L4=0。

## 母行与双档差异

集合和行界只取 t59 `REPORT.md` / `field_slots.json` / `field_map.json`。双档分别为 `13 + 894969 + 9 = 894991` 和 `13 + 1533950 + 9 = 1533972`；各 7,047 行、12 B `ordinal|UID|UID`、UID 双档逐行一致，selector 均为 0。Builder 重放 t59 冻结轨迹并核对所有槽的坐标及内容 SHA；独立 verifier 用原始 triple 反向 DP 各得一路，再借用 t59 固定槽宽和执行顺序逐项读，不以交付台账或扫描结果修补游标。每集合末端与后继槽、每母行 identity 与 footer 同时对齐。`census.json` 按档发布全部母行坐标、presence/count 位置、每个 item 的半开区间；`+0xc0` 另有每个内项的半开区间。`collections.json` 含每 lane 原值直方图、非空 ordinal、count/宽度分布及绝对界。所有 `@` 和表中区间都是**解压成员**绝对坐标。

静态来源：只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`；旧快照沿 t59 校验 MANIFEST。下文静态站点是 PE file offset，JSON 提供 VA 和原指令字节。`0xf2ba38/51` 把外部 mode 送入 COMP slot 19：`0xed0a40 → 0x3b3f0d0 → 0xeb7000`。`0xeb7394/9d/a0` 将 mode 0 直接跳到 `0xeb7a21`，**连 count / presence 都不消费**；因此 client 不是 7,047 个零 count，亦非相同路径读了 7,047 个假 presence。公共 71 B（含 selector）和后 56 B 两档逐行逐字节相同。实档 mode 1 则走扩展，`0xeb770e` 进入 `vec18` count，区别于 wrapper 把另一个 flag 清 0 的路径控制。模式是静态与数据反证，不是运行观测。t59 交换 mode 的负例原样保留并复现：

```text
vec30: row 0 @129: invalid count 16777216
row 0 @128: identity (255, 4294901760, 131071)
```

## 逐集合文法

| t59 槽 | Server 非空母行 / 项数 | payload 半开总界 | 消费文法（LE；presence 不计入 payload） |
|---|---:|---|---|
| `vec18` | 32 / 1,405 | `[143,1533899)` | `i32 N`；`i8 tag + 4+2+1 + [1 if tag>=2]`。`0xeb7dd2` count；`0xeb7e1b → 0x9f7c30 → 0x37b8710`，`0x37b8797/9c` 有符号比较。实档全 tag 2 / 9 B；首 row 117 `@32808` count 94，第一 item `@32812`。 |
| `+0xe8` | 149 / 6,597 | `[148,1518114)` | `u32 version + u32 N`；`i16 tag + 4+1+1 + (tag>=2 ? 2 : 1) +1 + [1 if tag>=3]`。`0xeb7776/83 → 0x155b450 → 0x4387ab0 → 0x155c120`；`0x155c378/3f3` 两阈值。全 version 2 / tag 3 / 12 B；首 row 0 `@148`，count 44。10/11 B 是静态兼容分支，不是第二档的实项。 |
| `+0xc0` | 315 / 1,069 外项、2,072 内项 | `[685,1512737)` | `u8 version + u32 N`；每外项 `u8 tag + octet + u32 M`；每内项 `u8 tag + 1+1+1+4+4`。`0xeb77f7/804 → 0x155ce40 → 0x438b680 → 0x155d010`，`0x155d053/28d` 两 count，`0x155d412..4b9` 内 transfers。版本/两层 tag 均为 1；外 count 1/2/3/4 各 31/32/34/218，内 count 1/2/3 各 326/483/260；首 row 0 `@685`。 |
| `+0xc8` | 366 / 1,464 六字节子项 | `[811,1453682)` | **不是 count**：`u8 tag + 4×(u8 tag + 5×u8)`；`0xeb7853/60 → 0x155de30 → 0x438e850`，四个固定 call (`0x438e880/90/a0/b3`) 各进 `0x155dad0 → 0x438bfd0`；全 tag 1。首 row 0 `@811` 到 `@836`；把首 `01` 当 count=1 会误停在 `@818`。 |
| `+0xd0` | 121 / 121 | `[838,1383171)` | presence 后**单项** `4+4+1+1+4+1`，无序列化 count/tag。`0xeb78e2/f2 → 0xeb5580 → 0x3b1e790`；首 row 0 `@838`。 |
| `+0xd8` | 51 / 51 | `[5271,1447143)` | 同 helper，不合并两对象槽；`0xeb7951/61`，首 row 7 `@5271`。 |
| `+0x100` | 129 / 212 | `[854,1533907)` | `i16 N + N×(1+2+2)`，无 item tag；`0xeb7982/95`，`0xeb79f9 → 0x9f9840 → 0x37be3a0`，按对象 `+4,+0,+2` 依次传输。实档 count 0/1/2/3/5/6 为 6918/62/56/9/1/1，首非空 row 47 `@17364`。 |
| `vec30` | 0 / 0 | `[129,1533885)` | `0xeb750e → 0xeb7e50 → 0x3b1f030` 静态 `u32 N + 2N`；实档 7,047 个零 count，首 `@129:00000000`。held、不赋语义。 |
| `+0xa8` / `+0xe0` | 各 0 / 0 | 无 payload 坐标 | 首 `@133:00` / `@142:00`，每档 server 各 7,047 个零 presence；`0xeb7544` / `0xeb76d2` 绕开 payload。这两条是静态可选分支，不判死，不升级 item 文法。 |

**请求中的计数与 t59 不一致**：按 t59 槽坐标、静态对象写点和原字节，`+0xc0/+0xc8/+0xd0/+0xd8` 的 present/nonempty 是 **315/366/121/51**，不沿用 brief 的 366/121/51/51。`+0xc8` 的 4、`+0xd0/+0xd8` 的 1 是结构项数，非 wire count；跳过的 presence 行不伪造 count=0。L3 针对物理形态及观察到的修订；未用 raw 数值范围冒充 enum/业务域。因 client 跳过，不存在双档共同 live item 的正向对值。

## 引用闸门

只读真实 t2/t3/t10/t21/t25 identity，档内各 56,293 / 84,259 / 251 / 48,413 / 7,047 个 ordinal；只验 t47 的 t10 原坐标和 t59 的 target identity digest，不重新开 club/nation 层。额外读取**实际静态 resolver 指向**的 t23（双档各 278）和 t24（server 84,507；client 无该 entry）：按 t39 既有末尾 triple / ordinal 见证独立核验；`table_extra_24.dat` 仅取 ordinal，不解其余数据。`0xffffffff` 与合法 0 分列；对于待定 lane，all-ones 只表示诊断分桶，不声明 null 语义。

- **`vec18:item+1` → t24，而不是 t3。** `0xeb88a4/a8/b1/cb → 0xf7e440 → 0x3bf3460` 使用 context `+0x98`；`0x37b81ee → 0x37b820d` 反向 writer 取被引用记录 `+8`，无对象写 `ffffffff`。`0xfb19b/1a2 → 0xefee00 → 0xf026c0` 绑定同一 context VA `0x141b5fda8`；`0xf0419b/a3 → 0xff9910` 传 type 24，`0xf042c3` 把结果写 `context+0x98`。实表 1,405/1,405 ordinal 命中，UID 误查仅 559 命中且 **559 全指别行**；首 row 117 `@32813=78`，t24 ordinal→UID 88，反向 UID→ordinal 70；首 UID miss `@32831=84`。t3 也 1,405/1,405 命中，不能据此写 Club。
- **`+0xd0/+0xd8:item+0/+4` → t23。** `0xeb87a8..8809 → 0xf7f440 → 0x3bf70c0` 用 context `+0x90`；`0xf0405c/64` 传 type 23，`0xf04184` 写同一 context 槽。`0x3b1e7c0/828` 的替代路径也用同一表，却查 `+0xc`（UID）；现代 slot 19 wrapper 清 flag，取 `0x3b1e7e2/7fc` 的 ordinal transfer。反向 writer `0xeb90fb/9149 → 0xeb5440 → 0x3b1e480` 区分 `+8` / `+0xc`。t23 ordinal 命中 / live / null 依序为 `31/31/90`、`0/0/121`、`8/8/43`、`3/3/48`；后者三条带活值的 lane（`+0xd0:+0`、`+0xd8:+0/+4`）的错误 UID 查找**也全中，但全指别行**。首 `@33663=71` → UID 73，反查 UID 71 → ordinal 69。`+0xd0:+4` 未见活值，保留 `@842:ffffffff`，静态目标明确，活域晋级仍 held。
- **`+0xe8:item+2` held**：6,597/6,597 为 `ffffffff`，首 row 0 `@158`。共享 t53 item reader 不同于共享对象，也不能搬用 t53 的 getter 域或其他 archive 绑定。
- **`+0xc0:inner+4/+8` held**：首活值 row 23 `@11151=312` 和 row 30 `@12621=680` 均不入 t10 ordinal；全档分别 31、172 次 t10 miss。t2/t3/t21/t25 多域同时全中（1,479 / 1,537 个非全一值，其中 0 分别出现 1,087 / 873 次），不能任选目标。首 `312` 当 t3 ordinal 得 UID 492，当 t3 UID 得 ordinal 188；错查不等于无命中。

## 归档绑定与复跑

FMF 目录 31/77 项逐 entry 记录，按 `data_base + offset`、`packed_size`、下一成员界和 `size` 唯一选帧。七套物理文法都从 **同一主档行、同一 stream** 直接消费，不是另开文件；t23/t24 是引用目标，不是 COMP 子表来源。双档没有 `table_extra_25.dat`；双档确有 `table_for_old_save_25.dat`，只是独立 entry 存在，不把它分配给任何集合，也不从缺同名 sidecar 推断没有其他 client getter 来源。无新的 opener→entry→payload 正链，不发布独立成员绑定。采用 t46/t51 的独立原字节交叉验证和 t53 的主读器/后缀分层；v8 的 8 个 club 子表、`CLUB_LINK`、`nation_t9_wire` 和 t59 主行结论不变，旧负例原样附在 JSON。

```text
FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t66_comp_subtable_discovery.py --build
py -V:3.12 -I -B scratch/t66/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```

两脚本均支持 `--help`/`--selftest`；0 成功、1 核验失败、2 用法/致命错误。独立 verifier 不 import builder、ReaderCFG 或 `fm24_dump`。没有启动游戏、编辑器或 IDA，没有访问 Z:。
