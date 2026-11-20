# t31 — CSrs / table 62 预备队静态 cursor

**当前归档全部闭合：server 37,214 行 × 42 B；client 目录无 table 62；10 项晋级 L3，0 held，L4=0。** 结论限定当前 `0x0df1` 归档与可复验的静态成功路径；不声称真机加载或覆盖通用 loader 的全部运行时行为。

## 归档与逐行闭合

| Archive | 目录条目 | 成员 | Count | Stride | 解压 payload SHA-256 |
|---|---:|---|---:|---:|---|
| client | 31 | 不存在（不是空表） | — | — | — |
| server | 77 | `server_db/table_62.dat` | 37,214 | 42 B | `978066bc07e96f2e75ee8909635052d778322219abc0f266a9a9aa01f0a0a485` |

Server 目录项 offset `26649596`，Zstd frame offset `26649630`，packed size `279272`。两归档 SHA 和原目录项见 `cursor_csrs.json`；client 不迁用任何 server 偏移。直接消费 t29 的 table62 profile 与 `.rows.jsonl`：核对同一 payload、legacy row block SHA、37,214 条逐行原字节与各字段的 unsigned 统计，不重 dump。构建时 `subtable_inventory.json` 尚未交付。

- **Wire**：`13 + 37214 × (1 selector + 29 properties + 12 identity) + 9 = 1563010`。Builder 先按 CFG transfer 推进 cursor，再校验 ordinal 并归纳出 stride。第 `i` 行：selector `13+42i`，body `14+42i`，行尾 exclusive `55+42i`。逐行 trace 摘要包含三条 identity lane、坐标和 body SHA；保留首三行、中间行、末行样本。
- **Legacy**：`14 + 37214 × 42 + 8 = 1563010`。业务 wire 行内坐标为 legacy 偏移加 1；legacy `+41` 借用下一行 selector，最后一行则借 footer 首字节。所有 selector 为 0；loader 消费它并传给 factory，但 table 62 case 不检查它。非零是 replay 的观察域拒绝，不是 native factory 拒绝。
- Identity 从 legacy `+29` / wire `+30` 到对象 `+0x08..+0x13`。原始 lane 0 等于 ordinal `0..37213`，另两 lane 相等、非零，37,214 个 UID 各不相同。以原始 lane 校验，不能用 reader 的 ordinal overwrite 洗掉错误。
- Footer 从绝对 `1563001` 开始：`00 00 00 00 | 01 | 5e 91 00 00`。`0xffa602` 消费 vector count，零时跳过每元素三次 4 B 传输；外层分别读取 1 B 到 `table+0x58`、4 B 到 `table+0x50`。末 u32 `37214` **在本档同时等于 max UID 和行数**，因此数值不能区分二者；真正驱动循环的 count 则明确是头部的独立 u32。未赋予 footer 末 lane 通用含义。

## 静态证据与分支

只读二进制 `<OLD_REPO>\input\editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`，与 `evidence/fm24/reports/qa/IDA_PROVENANCE.md` 对照。冻结 `master.json` SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`；两份快照通过 `evidence/MANIFEST.json`。下文非明确标记的地址是 PE **file offset**；VA、原指令 bytes 见 `instructions.part*.json`。

1. Factory `0xf48b30` 以 rel32 表 `0xf49d38` 的第 62 格入 `0xf49a2b`，`0xf49a58 → 0xf49a5f` 写 vptr VA `0x141884988`，COL `0x18840e0` → TD `.?AVSTARTING_RESERVE_TEAM@db@@`。
2. Slot19 VA `0x14119c960` / offset `0x119bf60` 是 leaf thunk。真属性 reader offset `0x3e5d730` / VA `0x143fc8d30`，PE runtime-function exclusive end `0x3e5d8b4` / VA `0x143fc8eb4`：113 条可达指令、13 块、11 条条件，11 次 stream vtable `+0x28` 共 29 B。成功后 `0x3e5d8af` tail-jump → leaf `0xfae340` → 真 identity reader `0x3c600f0` / VA `0x143dcb6f0`，第二个 runtime-function exclusive end `0x3c6016e` / VA `0x143dcb76e`：43 条指令、11 块、5 条条件，`0x3c60119` 实际读 12 B。合计唯一外部 CFG 边是已追完的 tail-jump，不是零字节 helper。
3. `ReaderCFG` 的两个 extent 没有控制字段布局的 caller mode 条件。Loader 写入的 `rsp+0x30` 模式字节未被 CSrs 测试；R9 经属性 reader 转发，identity tail 在 callback 之前写 `r9b=1`，不以其值分支。无需伪造 t30 的 mode=0/1 fork；唯一可能改变 tail 传输宽度的外部 stream-null 边与已成功完成属性传输的 caller 合约不相容。Footer context 的两条 vector begin/end 边汇合于同一 helper 与 cursor；实测 zero count 与容量无关。

| 谓词来源 | Reader + tail / 外层切片 | 证据及首个反例 |
|---|---:|---|
| `wire_data` | 1 / 5 | `0x3c60131` 以 unsigned lane 0 对 `10000001`，全表走不改写边；注入后首行原样为 `row 0: identity @43 raw=(10000001, 1, 1), stored ordinal=0`，不通过原始 lane 校验。外层是 count/循环与 footer vector count。 |
| `runtime-external` | 0 / 1 | 外层 factory `0xf48b3b` 用 directory 已知 table type=62 检查上界，不是 CSrs body mode，也不是 selector。 |
| `IO-result` | 11 / 11 | 每次属性读后测 stream `+0x10`，失败收敛 `0x3e5d88e`，AL=false；最后一条 `je` 成功为 taken。每个 transfer 保留首行短读，例如 `row 0: short transfer @14 width 1 site 0x3e5d755; IO-result -> 0x3e5d88e (AL=false)`。Identity bulk **无即时 status 检查**：`row 0: short transfer @43 width 12 site 0x3c60119; no immediate native bulk status test`，仅声称 replay 拒绝。 |
| `context-lifecycle` | 4 / 3 | Tail stream-null、callback-null、release-null、refcount；首行属性入口即解引用 stream，null 不是可行布局；callback 指针来自 caller 的 table this，非 R9。保留 live stream/retained-owner 假设，callback 与最终析构体未展开。 |
| `dead` | 0 / 0 | 没有根据数据缺席删除静态边；footer 非零 vector 的显式读及失败边留在外层证据中。 |

`branches.part*.json` 每项有谓词、来源、两条后继和观测结果、首个反例或边界说明。Reader 访问计数是有效归档与存活对象合约下的 replay 结果，不是运行时测量。其余 synthetic negatives（非零 selector、identity lane 不等）同样保留在 `cursor_csrs.json`。

## 三重闸门与 10 项台账

1. `club.xml/CSrs` 的唯一 nested schema occurrence（t24 idx **93–102**），不使用全局重名 4CC 投票。
2. Club 端 `CSrs` compare `0xe8b6f0 → 0xe8e27c`，collection helper `0x152a840 → 0x4354a30` 按子对象 `+0x18` 父 club 指针筛选。该 table class 的 slot 2 getter VA `0x14119d0f0` 以 EDX 精确 4CC 分发到特定对象成员；逐字段保存可执行分发路径和取值指令。
3. Getter 成员接到已走通的真实 sink；在冻结 schema 域、getter sentinel 或 mask 下独立全表画像。`Tdvi` 和 `Tsti` writer 从目标 `+8` 取 ordinal、null 写 `FFFFFFFF`，fixup 转为指针，getter 分别装箱 `comp` 与 `stad`。从 client table25、table21 只读重验实际目标 ordinal 集（7,047、48,413），不按 public UID 判定，不改判目标表。没有 packed day/year 字段；两项 weekday 是有符号 i8 category，不是日期。没有 scoped i16 传输。

| 4CC | 对象 | Legacy / wire | Width | 域与观测 | 等级 |
|---|---:|---:|---:|---|---|
| `Ttyp` | `+0x44` | `+0 / +1` | 1 | `i8`，`-1` sentinel（0 行）；9 个 live code 均在冻结 `Rsty` | L3 |
| `Tdvi` | `+0x20` | `+5 / +6` | 4 | competition ordinal，7,292 live（15..7026），29,922 个 `-1` | L3 |
| `tmno` | `+0x47` | `+27 / +28` | 1 | `0x04`，23,792 true | L3 |
| `tmnv` | `+0x47` | `+27 / +28` | 1 | `0x02`，451 true | L3 |
| `Tsti` | `+0x30` | `+9 / +10` | 4 | stadium ordinal，6,903 live（6..48363），30,311 个 `-1` | L3 |
| `Twhm` | `+0x45` | `+25 / +26` | 1 | `i8`，0 sentinel（33,197 行），live 1..7；不指派星期名称 | L3 |
| `Tmhm` | `+0x46` | `+26 / +27` | 1 | `i8`，0 sentinel（33,899 行），live 1..7；不指派星期名称 | L3 |
| `Catd` | `+0x38` | `+13 / +14` | 4 | `i32`，观测 0..1500；0 是合法整数，不是 sentinel | L3 |
| `Cmna` | `+0x40` | `+21 / +22` | 4 | `i32`，观测 0..300；不按 schema 显示顺序猜 wire 顺序 | L3 |
| `Cmxa` | `+0x3c` | `+17 / +18` | 4 | `i32`，观测 0..3000 | L3 |

两布尔字段是同一 wire byte 的两位，不是两个 byte。raw byte 分布 `{0:13314, 2:108, 4:23449, 6:343}`；不对其余位命名或承诺必须为 0。三个 attendance 字段都通过独立 XML 的 `[0,1000000]`。台账无字段域冲突；未命名的是 parent back-reference、其余 flag 位与对象 `+0x48` / legacy `+28`，不计入 10 项，也不凭分布补名。留待另案：未观察的生命周期边、未命名 byte/bit、通用 footer 末 lane 语义；不影响本次 `.dat` 闭合。

## 复验

- `py -V:3.12 -I -B scripts/t31_csrs_cursor.py` — PASS。
- `py -V:3.12 -I -B scratch/t31/out/verify.py` — PASS；不 import builder 或 `ReaderCFG`，独立重读两归档、反汇编保存的原始指令、重建两个 CFG 并复算全表、目标域、t29 行差和样本。
- 两脚本 `--help` / `--selftest` — PASS；退出码 0 成功、1 检查失败、2 用法或致命错误。
- `py -V:3.12 -I -B scripts/t01_anchors.py` — **7/7 PASS**。
