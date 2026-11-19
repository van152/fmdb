# t41 — Csme / table 59 变长 cursor 静态核验

**Server 9,079/9,079 行由 reader 语义闭合；client 无 table 59。表级 `Melf` 条件 L3；`Msid` 已静态绑定到双 lane sink，但全表没有 live 引用，保留 held。Club 独占 L3=0，L4=0。** t33 的 payload 和行块摘要不变，但首两行的最短尾启发式边界有误：`19 + 25` 应为 `22 + 22`。

## 两个 archive 与 E66

| Archive | 目录项 | 成员 | Count | reader 行长分布 | 解压 SHA-256 |
|---|---:|---|---:|---|---|
| client | 31 | 缺失，不是 count=0 | — | — | — |
| server | 77 | `server_db/table_59.dat` | 9,079 | 22 B × 6,567；32 B × 2,512 | `7eee0ecc59ee306aefc52eb7a7f7095d439748f3e06ac9d36d3ddc1568c8b1a7` |

Server `entry.offset=38661625`，`data_base=34`，真实 Zstd magic `38661659`，`packed_size=62202`，`entry.size=224880`；帧结束 `38723861`，与下一成员起点相等。以 `entry.size` 唯一选帧，再独立计算 payload SHA；本目录项没有 `sha256` 键。前一成员 `table_52.dat` 在 `38661624` 有 35 B 压缩帧，解压 22 B、count=0。它的 magic 恰在 t59 目录相对扫描起点**前一字节**，所以未修改的 `load_payload` 此处已经返回真实 224880 B。另从 `38661624` 做对照，能看到两帧；first-magic 会取到邻表空帧，按 size 仍选 t59。不能将邻表空帧写成 t59 成员内 stub，也不能照搬 t39 的旧 loader 失效结论。

## 静态链与变长来源

二进制：只读 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。冻结 `evidence/fm24/reports/qa/IDA_PROVENANCE.md` 和 `evidence/fm24/reports/editor_schema/master.json` 均通过 `evidence/MANIFEST.json`；后者 SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`。以下指令地址默认 PE **file offset**；VA 与原始 bytes 在 `instructions.part*.json`。

- loader `0xf2ba0e` 消费 selector，`0xf2ba23` 调 `0xf48b30`。rel32 表 `0xf49d38` 第 59 格 → `0xf49950`；`0xf4996c/0xf49973` 设 vptr VA `0x141882fa8`，COL/TD 为 `.?AVSTARTING_MEDIA_EXPECTATIONS@db@@`。Case 59 不按 selector 分叉。合成 row 0 selector=1 仍消耗 22 B，不代表档内有此 selector。
- Slot 19 **直接**进入 `0x15831a0..0x1583580`（VA `0x141583ba0..0x141583f80`，右端 exclusive），不是 leaf thunk。以 PE `RUNTIME_FUNCTION` + `t21b_control_flow.ReaderCFG` 解出 **260 可达指令、49 块、29 条条件分支，0 extent 外 CFG 边**；调用单列。Identity 在同一 extent 内，`0x1583500` 起，`0x158351f` 将 12 B 读到对象 `+0x8/+0xc/+0x10`。
- `0xf2ba38` 确实转发 caller mode，但该 reader 在调整栈后只用 `rsp+0xc8` 的 ordinal 和 `rsp+0xd8` 的 table context，不读 mode 对应的 `rsp+0xd0`。以 mode=0 和 1 分别完整运行 9,079 行；两份 trace、边计数、footer 一致，**没有 identity-only 分支**。
- 可变项只由 `0x158320a` 新读的 **u32 count** 决定。`0x158322d` 在零时跳过 vector；`0x1583250` 对递增索引与同一 count 作无符号比较。每次循环消费 `1+8+1`；不是按 selector、tag 或 identity 搜索行尾。合成 row 2 count=2 并插入一个 10 B item 后，观察到一次 loop backedge、行长 42 B，identity 后移 10 B。只改 row 0 count、不插数据则在 `@33` 遇到错误 identity，拒绝。

| Slot 19 分支类 | 条数 | 依据与首反例 / 约束 |
|---|---:|---|
| `wire_data` | 4 | count=0 的 row 0 跳过循环；count=1 的 row 2 消费一个 item；合成 count=2 覆盖回边。`0x15832da` 在第二引用 lane 为 0 时复制第一 lane，宽度不变；`0x158353a` 在 raw ordinal ≥10,000,001 时用 caller ordinal 覆盖，合成 row 0 仍被 **raw** lane 校验拒绝。 |
| `IO-result` | 7 | stream `+0x10` 或其 EBP 暂存；失败汇入 `0x1583213` 返回 AL=false。各有首短读，例如 `@14 w4`、row 2 `@68 w8`。`0x158332b` 复查同一 stream status。12 B identity 无即时 status 分支，短读仅声称 replay 拒绝。 |
| `context-lifecycle` | 18 | TLS/pool、追加与扩容、空 stream、refcount、callback。row 2 首次 append 扩容；释放已分配旧 vector 需合成 count=2 才进入。row 0 的假想空 stream 会跳过 bulk，但早先的属性读取已要求 live stream。按 live stream、初始空 vector、成功分配的上下文建模；不声称观察到实机 TLS/refcount/callback，也不把未观测边当死代码。 |
| `runtime-external` / `dead` | 0 / 0 | Slot 19 不读 caller mode。外层切片另存 factory 表号上界、loader count/selector/status、footer vector/flag 等 20 条分支，不将切片冒充整个 loader CFG。 |

### 双坐标与 t33 差分

对每行，设 `s` 为 wire selector 起点，`b=s+1` 为 legacy body 起点，`n` 为新读的 count，`j` 为 0-based item 下标：

| 内容 | Legacy（相对 `b`） | Wire（相对 `s`） | 宽度 |
|---|---:|---:|---:|
| selector | −1 | 0 | 1 |
| 未列入 XML 的 owner / 外层 byte / count | `0 / 4 / 5` | `1 / 5 / 6` | `4 / 1 / 4` |
| item tag / pair / Melf | `9+10j / 10+10j / 18+10j` | `10+10j / 11+10j / 19+10j` | `1 / 8 / 1` |
| identity 三 lane | `9+10n` | `10+10n` | 12 |
| legacy marker | `21+10n` | 跟随本行，非 slot 19 transfer | 1 |

`13 + 6567×22 + 2512×32 + 9 = 224880`；legacy `14 + 224858 + 8 = 224880`。在两种对齐中所有 9,079 个 selector/marker 均为 0；marker 是下一 selector（末行为 footer 首字节）。每行读完才校验 raw lane0=ordinal、后两 lane 相等且非零，后两 lane 的取值在各行之间唯一。真实 footer 从 `224871` 起：`00000000 | 01 | 77230000`。vector count=0，flag=1，末 u32 为 9079，观测上同时等于最大 identity 和 header count，**不足以区分语义**。

直接消费 t33 profile 和 JSONL，未重 dump。原文件的 9,079 条 raw slice 与原 payload 对得上，纠正边界后 9,077 行逐条一致，整个 legacy row-block SHA 仍是 `94b77a7e6863b4ecf15239de7ed1b637620acbba0c88941e53da24031048728a`。

| 行 | t33 legacy 起点 / 长度 / tail | Native legacy 起点 / 长度 / tail |
|---|---|---|
| 0 | `14 / 19 / @20 (0,16777216,16777216)` | `14 / 22 / @23 (0,1,1)` |
| 1 | `33 / 25 / @45 (1,2,2)` | `36 / 22 / @45 (1,2,2)` |

t33 先选了 row 0 的最短合法尾，row 1 在同一尾端重新对齐，所以总字节、tail hit count 和 row-block SHA 都不能检出这类错位。保留 t33 报告原负例：`tail id pair in every row equals 0x01000000, not a plausible media_source id; column semantics stay unresolved`。其“every row”与已有 JSONL 不符；`0x01000000` 是 row 0 的假尾值，不是 Media Source 字段。原文件和原措辞未改。

## 三重闸门、字段台账与排他性

冻结 `club.xml/Csme.list_item_fields` 中唯二 occurrence 对上 t24 idx **174 / 175**。实际路由是 Club slot 2 `0xe89a00` 对 `Csme` 的精确分发 `0xe8cb93` → `0xeb4430` thunk → `0x3b17180`，不是直接在 outer slot 2 搜这两个子字段。集合由全局 VA `0x141b601e8` 的 table `+0x80` 取出，按 outer `+0x30` owner 指针等值筛选，从 outer `+0x18/+0x20` 取 entry 指针。`0x3b173e8 → 0xeb0bd0 → 0x3b0f420` 调枚举 `0x43803c0` 及内层 `0x4381560` getter。Club slot 3 的 `Csme` 分发 `0xe8411d → 0xeafe10` 也取同一集合；可经 `0x4365f50 → 0xf8d120 → 0x3c0d7b0 → 0x1582d60` 创建相同 vptr 的对象，并在 `0x1582dfd` 写同一 owner 成员。

| 4CC | 对象 → reader sink | 全表域与等级 |
|---|---|---|
| `Msid` | `0x438157f/0x438158f` 经 `MedS` helper；entry `+0/+4` → `0x15832d2`，8 B，legacy `10+10j` / wire `11+10j`（静态绑定） | **held：无 live 引用**。6,567 行无 entry，2,512 个 entry 双 lane 全为 `(-1,-1)`，不是有效 ordinal；首个 row 2 `@68 ffffffffffffffff`。`0xfe68cd` 负 lane0 返回缺失；lane1=0 才复制 lane0，0 不是 −1。泛型 setter 转换可从目标对象 `+0xc/+0x10` 打包，区别于 owner 的 target `+8` ordinal。XML 可选允许 null，不把全空写成域冲突、live join 或单槽 ordinal。 |
| `Melf` | `0x4381577 → 0x4381596` 对 entry `+8` `movzx` → `0x1583317`，1 B，legacy `18+10j` / wire `19+10j` | **条件 L3**，仅 `0≤j<n`。2,512 个值 1..33，符合 XML max=127；0 个 raw 0、0 个 raw `ff`。无掩码或 −1 哨兵：合成 `ff` 装箱为 255（超 XML 上限），合成 0 仍是存在的整数 0；没有 entry 是 count=0，非默认值 1 或 0 的 wire 表示。 |

**引用实表与别名否证。** 用 table 7 的 `MEDIA_SOURCE` factory/RTTI、slot19 `0x15457c0` 和 base identity read `0x3c60119`，只回放长度以提取目标键；client/server 均读到相同的 208 个实际 ordinal→identity 映射。实际序号 0 对应 identity 1，−1 不在目标集合中。把 outer legacy `+0` 当 `Msid` 只有 99/9,079 落入实表序号集；首 miss row 99 `@2662 d0000000`=208，实际是 Team ordinal。把 outer `+4` 当 `Melf`，首个可对照的 row 2 `@62`=2，而内层 `@76`=4；没有 4CC 路径支持 count=0 时用外层 byte 回填。外层 byte 实测 `0..4`（114 个 0）；循环内 tag 全为 `0x01`，只读入 `[rsp+0x47]` 并弃置，未发现取值测试或 bit mask，不能命名布尔。合成 tag=`0x80` 仍走同样读法。

**不晋级 club 独占。** Outer `+0x30` 的 slot 21 从目标对象 `[+8]` 写 i32 ordinal，空时写 −1；slot 20 经 `0x43d2bb0 → 0xf7e440 → 0x3bf3460` 是 Team resolver，含运行时 guard/remap，不宣称总是直接索引。在 server `table_24` 中，以 `table_extra_24` 的 84,507 个实际 ordinal 校验边界，并使用重复尾 lane 和 full-team selectors `{10,11}` 得到唯一顺序链，未用 footer 末 u32 推断界限。t59 的 9,079 个不同 owner 全命中：**8,941 selector 10、138 selector 11**。独占首反例 row 0 `@14 00000000` → table24 ordinal 0，selector **11 @13**，identity `(0,5,5) @136`。Case 24 的 full-team arm `0xf49106` 将 11 路由到 `NATIONAL_TEAM`，其余至 `TEAM`；`0xf49100` 进程兼容分支保留，不宣称观察到实机配置。已证实 Club 编辑路由和实际 Team 家族归属，未证实另一个 Player getter；t33 `entity_tag=play` 不是 Player 指针或独占证据。

## 复验与剩余

`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`，`py -V:3.12 -I -B`：builder、独立 verifier、两者的 `--help`/`--selftest` 与 `scripts/t01_anchors.py` **7/7 PASS**。Verifier 不 import builder 或 `ReaderCFG`；另建 PE 可达图，重读两目录，用顺序计数解码独立验全表、双 mode、帧及负例。返回码 0/1/2 为成功 / 检查未过 / 用法或致命错误。未启动游戏、编辑器、IDA，未联网，未访问 Z:。剩余：需要含非空 `Msid` 的合法档或授权交叉证据才能验 live 编码及目标命中；外层 byte 未命名，不进入字段台账。此文件为 t41 实验交接，不改公共 loader、既有 ledger 或其他任务结论。
