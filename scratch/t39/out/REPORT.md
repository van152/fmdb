# t39 — Tchl / table 34 杯赛历史静态 cursor

**Server 7,115 行 × 44 B 全闭合，client 目录无 table 34。表级字段 7/9 L3（含一个双槽枚举），2 项因 XML 域冲突 held；club 独占 L3=0，L4=0。** `Tchl` 编辑分发由 club / nation 共用；本档 **7,084 条非空 owner 全指向 table 24 的 selector 11（完整 Team factory 的 `NATIONAL_TEAM` arm）**，另 31 条 owner 为空。不能沿用旧画像的 `entity_tag=club` 作独占结论，也不把空 owner 归给任一方。

## 双 archive 与 E66

| Archive | 目录项数 | 成员 | Count | Stride | Payload SHA-256 |
|---|---:|---|---:|---:|---|
| client | 31 | 不存在，不是空表 | — | — | — |
| server | 77 | `server_db/table_34.dat` | 7,115 | 44 B | `a07b2bb76fb8796bcbc39dde659610d5257a8801004b6608e4be34beb9a84812` |

目录 `offset=38972269`，archive `data_base=34`，`packed_size=89082`，`size=313082`，版本 `0x0df1`。从旧 `load_payload` 使用的**目录相对 offset** 扫描确有两个相邻帧：

| 相对目录 offset | 绝对 offset | 压缩 B | 解压 B | Count | 判定 |
|---:|---:|---:|---:|---:|---|
| +9 | 38972278 | 25 | 12 | 0 | 原函数确实返回此帧；SHA `600175712b2f553abc27f837a749483f1126b1966ef64d2998223d7cd58b4013`。它其实是前一目录项 `non_player_bans.dat` 的规范帧，不是 table 34 自己的空记录块。 |
| +34 | 38972303 | 89,082 | 313,082 | 7,115 | 以 `entry["size"]` 唯一选中；规范起点是 `data_base + offset`，结束 `39061385` 正好是下一成员规范起点。 |

候选解压同时受从 magic 起算的 `packed_size` 和下一成员边界约束；不扫描到 archive 尾。保留 t13d `quick_audit.md` 的原负例及摘要，不修改公共 loader。直接使用 t29 profile / `.rows.jsonl`：7,115/7,115 条 legacy row byte-for-byte 相等，独立比较列统计和 row-block SHA。目标 t33 路径在本 checkout **没有** table 34 profile 或 rows；本次没有补造 t33 文件。另核对现有 t37 table 34 profile 的同一 payload 和 row block，不把其 `club` 标签当作独立归属证据。

## 静态链、分支和全表 walk

只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`，与冻结 `evidence/fm24/reports/qa/IDA_PROVENANCE.md` 一致。冻结 `evidence/fm24/reports/editor_schema/master.json` SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`；两份快照均通过 `evidence/MANIFEST.json`。下文默认 PE **file offset**；对应 VA、原始指令 bytes 在 `instructions.part*.json`。

- Factory `0xf48b30` 的 rel32 表 `0xf49d38` 第 34 格 → `0xf4949c`；`0xf494b8` / `0xf494bf` 设置 vptr VA `0x1418be628`，COL/TD 给出 `.?AVSTARTING_TEAM_CUP_HISTORY@db@@`。Loader `0xf2ba0e` 每行消费 selector 后传给 factory，case 34 不使用它；合成 selector=1 的首行仍走相同读法，不是 native 拒绝。
- Slot 19 VA `0x14156f9d0` / offset `0x156efd0` 是 leaf thunk → 真 reader `0x43a6890..0x43a6a6f`（VA `0x144511e90..0x14451206f`，右端 exclusive）。PE `RUNTIME_FUNCTION` + `ReaderCFG` 得到 137 条可达指令 / 24 块，无 extent 外边。**Identity tail 内联**于 `0x43a69f8`，真正 12 B read 在 `0x43a6a17`（VA 见指令分片）；不是 Cdbt/Cmti 的第二 extent。
- Mode 是外部：`0xf2b670` 保存 caller R9D 到 R12D，`0xf2ba38` 写 loader `[rsp+0x30]`；改栈后的 reader `0x43a689d` 测 `[rsp+0x70]`，`0x43a68a2` 为零跳过属性。直接 caller `0xf28c13` 置 R9B=1；另一 caller `0xf4d839` 传 R15D。两个分支均对本档的 header count 完整 replay，不把输入 selector 当 mode。**mode=1**：11 次 `4,4,2,2,4,4,1,1,4,1,4` 读 + 12 B identity，全部后置校验通过。**mode=0**：只消费 selector + 12 B identity，首行在绝对 `@14` 误读 `(637,50,132188129)`；7,115/7,115 条均不满足 identity 校验，最后只到 `92508`，该处所谓 vector count 为 `131661824`，不闭合。此负例不排除另一个 archive 使用 identity-only 记录。

| 分支分类 | Reader / 外层切片 | 证据与首反例 |
|---|---:|---|
| `wire_data` | 1 / 5 | `0x43a6a2f` 检查新读的首 lane `<10000001`；若否，覆盖为 caller ordinal。首行合成 `@45 (10000001,103,103)`，覆盖后为 `0`，仍被 raw lane 后置校验拒绝。外层含 count / footer vector count。 |
| `runtime-external` | 1 / 1 | 上述调用方 mode fork；外层 factory 表号上界与记录 selector 无关。 |
| `IO-result` | 11 / 11 | 属性 transfer 后取 stream `+0x10`，非零汇合 `0x43a69f4` 返回 AL=false。首行短读 `@14 width 4`；全 11 处均有合成负例。Bulk 无即时 status test，`@45 width 12` 短读只声称 replay 拒绝。 |
| `context-lifecycle` | 4 / 3 | Stream 空指针、callback table this、release guard、refcount。Mode=1 的空 stream 会在首成员读取前解引用；mode=0 空 stream 会跳过 bulk，非有效观测布局。Callback、最后引用析构不展开，不宣称实机调用。 |
| `dead` | 0 / 0 | 不把未观察到的生命周期、非零 vector 等边删作死代码。 |

Wire 对齐：`13 + 7115 × (1 selector + 31 properties + 12 identity) + 9 = 313082`。第 `i` 行 selector `13+44i`，body `14+44i`，行尾 exclusive `57+44i`。实测 selector `{0:7115}`，raw ordinal 依次 `0..7114`，后两 lane 每行相等且非零、全表唯一。Footer 从 `313073` 开始：`00 00 00 00 | 01 | 0d 00 d8 05`；vector count 0，末 u32 `98041869` 恰等于最大 identity（**不等于** header count；不外推其他档语义）。Legacy 对齐 `14 + 7115 × 44 + 8 = 313082`，legacy `+43` 借下一 selector 或第一个 footer 字节。指令 CFG、每个谓词的证据、边次数与首个反例见 JSON；两种 mode 各有逐行 trace digest 及代表行。

## 排他闸门：代码共享，实际非空 owner 全是 national-team selector

- `CLUB` slot 2 `0xe89a00` 经 `0xe8c67e` 精确匹配 `Tchl`，进入 `0x11f41d0`；`NATION` slot 2 `0x1041f30 → 0x1041f40`，`0x1043322 → 0x1065ef0`，其 `0x1066981` 同 4CC 同样汇入 `0x11f41d0`。包装器取 Team 对象、把 4CC 写回 EDX，经选中 Team slot 2 继续。`NATIONAL_TEAM` slot 2 走 `0x1056a90 → 0x3d7d6c0`，`Tchl` 不在专门覆盖项中，`0x3d7d817` 落普通 `TEAM` getter `0x11af7b0`。`TEAM` / `NATIONAL_TEAM` 共用 slot 3 `0x11b4c30`。
- Team getter `0x11af822 → 0x11b0f62`，setter `0x11b4cc7 → 0x11b5051`，二者都调用集合 helper `0x15e9830 → 0x44d7bf0`。它在全局集合（VA `0x141b60158` 所指 table 的 `+0x80` vector）取子项，比较子项已修复 `+0x20` 的目标 `+0xc` 与当前 Team `+0xc`。对应添加路径 `0x44d8364` 加载**同一个 table 34 子项 vptr**，`0x44d8376` 设 owner `+0x20`，`0x44d83ba` 取同一个全局集合插入。不是仅以两个 schema 里同名作为“共享”证据。
- Owner 是未列为 XML item 的 **i32 ordinal**，legacy `+4` / wire `+5`。Slot 20 `0x43a70e0` 用 team resolver（与 `tcop` 相同）；slot 21 `0x43a87f8` 写目标 `+8` 或 `-1`。目标实表和 sidecar 复核：`table_extra_24` 与 `table_24` count 一样且逐记录覆盖实际 84,507 个序号；在主 payload 中，约束相等 identity 后两 lane、逐序号单调和 Team selector `{10,11}` 后，前向最早 / 反向最迟行尾完全一致。这里只用目标身份边界，不解析其他 Team 属性。Factory case 24 的 full-team arm `0xf49106` 以 `BL=11` 到 `NATIONAL_TEAM`（`0x3d7afdb` 写 vptr），非 11 到 `TEAM`。`0xf49100` 的进程兼容分支明确保留；本任务不宣称观察到了实机配置。
- **Club 独占首反例**：table34 row 0 `@18: 32000000` → table24 ordinal **50**，目标 selector **11** 在 `@6763`，identity `(50,55,55)` 在 `@6886`。统计为 7,084/7,084 个 live owner 都指 selector 11；row 6905 首个 `-1 @303838` 不归因。`tcop` 的 2,629 个 live 也全指 selector 11。所有这些 ordinal 数值都可以落进所谓 club 范围，**范围相符不等于对象类型相符**。只晋级 table34 / 共享类里的坐标，不向 club 独占台账推广。

## 三重闸门与字段台账

冻结 `club.xml/Tchl.list_item_fields` 与 t24 idx **562–570** 一一对应；`nation.xml/Tchl.list_item_fields` 在其自己的 scope 内也唯一且与 club 版本逐项相同。slot 2 getter `0x156f850` 按 EDX 精确分发 4CC；先绑定对象成员，再用 slot 19 的 wire sink 和全表独立画像验域。`held` 项保留静态候选坐标，不发布验收 `row_offset`。

| 4CC | 对象 offset | Legacy / wire | 宽度 | 表级等级与全表验证 |
|---|---:|---:|---:|---|
| `tchc` | `0x18` | `+0 / +1` | 4 | **L3**；competition/t25 i32 ordinal。7,084 命中、31 个 `-1`。首行 637 → target identity 1301390。 |
| `styr` | `0x48` | `+8 / +9` | 2 | **held**；`movzx` 为 u16 年整数（非 packed date）。冻结 XML `[1900,2100]`；所有非零在 1900..2023，但 161 个零。首反例 row 28 `@1254: 0000`。 |
| `edyr` | `0x4a` | `+10 / +11` | 2 | **held**；同为 u16 年整数，21 个零，非零 1900..2023。首反例 row 2695 `@118604: 0000`。两个 getter 均直接装箱，不擅自把 0 定义为哨兵。 |
| `mstn` | `0x30` | `+12 / +13` | 4 | **L3**；stage_name/t23 i32 ordinal。6,956 命中、159 个 `-1`。row 1439 的 274 超出 nation 主表序号域，却落真实 stage 域。 |
| `sstn` | `0x38` | `+16 / +17` | 4 | **L3**；也是 stage_name/t23，但独立 read site 和成员。3,441 命中、3,674 个 `-1`。row 3830 的 0 是有效 ordinal → identity 1。 |
| `dbrt` | `0x4c,0x4d` | `+20,+21 / +21,+22` | 各 1 | **L3 双槽**；u8 flag + signed i8 state，不是 raw byte 枚举。getter jump table 与 setter 19 项反查表互证。 |
| `posi` | `0x4e` | `+26 / +27` | 1 | **L3**；`movsx` i8，显式 `-1` 返回缺失（2,650 次，首 row 1 `@84: ff`）；live 1..16 落 XML `[0,50]`。 |
| `cquf` | `0x28` | `+22 / +23` | 4 | **L3**；competition/t25 i32 ordinal，1,022 命中、6,093 个 `-1`。首个 live row 27 的 633 → identity 1301385。 |
| `tcop` | `0x40` | `+27 / +28` | 4 | **L3**；team/t24 i32 ordinal，2,629 命中、4,486 个 `-1`；不是 club/t3 指针，也不是对手的 DUNI。首个 live row 1 的 36 → national-team selector 11 / identity 41。 |

**引用编码和否证。** 五个独立站点分别只读 4 B 到 `+0x18/+0x30/+0x38/+0x28/+0x40`；slot 21 逐个从 target `+8` 写序号或 `ffffffff`，slot 20 比较有符号值并经各自的索引/映射 resolver 修为指针。Getter 的 `+0xc/+0x10` 组对发生在**目标对象**装箱，不能倒推 wire 是 i32 pair 或单 identity lane。两个 stage 走同一 `stage_name` 目标族和 helper，保留 remap 路径，不把整个 fixup 说成无条件直接索引。通过 client 固定 identity 尾和 server exact triple 顺序见证核验实际 7,047 competition、278 stage_name 序号。把 live wire 值当成目标 UID，会分别漏 `tchc/mstn/sstn/cquf/tcop` **4,378 / 32 / 2 / 937 / 187** 条；JSON 保留各首反例。

**Result 首反例。** state=1 时，row 3 的 `(flag,state)=(0,1)` 返回 10，row 1 的 `(1,1)` 返回 1；不能只读取 state。静态表：state 1..8 在 flag 非零时返回 state，flag 为零时 +9；state 11 返回 9/18，state 12 返回 19，其他（含 `-1`）走默认 0。全表 flag `{0:6499,1:616}`，state `{−1,1,2,3,4,5,6,7,8}`，实际装箱集合 `{0,1,2,3,5,6,7,8,10,11,12,13,14,15,16,17}`。冻结 schema 无 `enum_ref`，不赋 UI 标签。

## 复验与边界

环境 `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`；`py -V:3.12 -I -B` 下 builder、独立 verifier、两者的 `--help` / `--selftest` 均 PASS；`scripts/t01_anchors.py` **7/7 PASS**。Verifier 不 import builder 或 `ReaderCFG`，从原 PE 另建可达图，独立枚举并按大小选帧、执行双 mode、验证原字节和各域反例。退出码 `0/1/2` 分别为成功 / 校验失败 / 用法或致命错误。未启动游戏、编辑器或 IDA，未联网，未访问 Z:；未修改其他任务产物或全局 ledger。
