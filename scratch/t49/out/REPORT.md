# t49 — NATIONAL_TEAM_CONTAINER（t9）双档主表 wire 验收（partial）

**`table_9.dat`：client mode 0、server mode 1，各 251/251 行闭合；17 L3、13 held、L4=0。** `table_extra_9.dat` 在两档都存在，但两种 slot 19 读法均拒绝，未定位其正向 reader/mode。`NCro` 的 server presence 有实档覆盖，但全为 0，没有 live item。本报告不把这两项写成闭合。

## 成员、mode 与游标

静态来源：只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。地址默认 PE file offset；分片存 VA、原 bytes、直接转移目标。冻结 `master.json` 与 `IDA_PROVENANCE.md` 对照 MANIFEST；t37 inventory `8af89c72…` 及 t37/t47 原结论未改。归档用目录 `34+entry.offset`、`packed_size`/邻接上界枚举帧，按 `entry.size` 唯一选帧；`entry.sha256` 对应压缩区，另记 payload SHA。

- `0xf2ba0e` 先读 selector；`0xf2ba23 → 0xf48b30`，rel32 第 9 格 `0xf49d5c → 0xf48f12 → 0x1059a30`，构造写 vptr `VA 0x1418898d8`，RTTI `.?AVNATIONAL_TEAM_CONTAINER@db@@`。slot 19 `0x105cb10..0x105f040`，PE `RUNTIME_FUNCTION` + `ReaderCFG`：2,141 条可达指令、0 extent 外 CFG 边。`0x11d0d30` 共 1,508 条、同样 0 extent 外边。
- Loader `0xf2b670` 从 R9D 保存 mode，`0xf2ba38` 放入 caller 栈，`0xf2ba51` 调 slot 19；`0x105cb2c` 读 callee `[rsp+0x140]`。`0x105cbb1` mode 0 跳过长前缀，`0x105e695` 跳过后置扩展；`0x105eef7 → 0x105ef12 → 0x11d0fa4` 再按同一 mode 分叉。以现代版本臂复放；`[context+0x588]` 是进程上下文，本次没有运行它，也不把 payload 的版本字节当作运行观测。兼容臂不外推。
- `0x11d21df` 收尾读取 12 B identity，**在读完后**检查 raw ordinal=行号、后两 lane 相等且非零、跨行不重复。两档全部三 lane 相同；251 selectors 均为 0。没有以 identity 搜索 t9 行边界。`wire13` 含行首 selector；`legacy14` 以行体起点为基准，最后 byte 借下一 selector／末行借 footer 首 byte。不按 item 对象内存宽度推母表 stride。

| 档 | 成功方式和长度 | 首个错误 mode 反例 |
|---|---|---|
| client `table_9.dat` | mode 0；`13 + 31934 + 9 = 31956`，行长 58–461 B | mode 1：row 0 `@28`，i32 `1543569408`，要求每项至少 8 B，越界 |
| server `table_9.dat` | mode 1；`13 + 307542 + 9 = 307564`，行长 383–36,514 B | mode 0：row 0 `@59`，读完短路径后 raw identity `(0,0,0)`；这里不是 invalid count，保留真实首反例 |
| 两档 `table_extra_9.dat` | client 83,927 B / server 105,228 B；**未绑定** | mode 0：两档 row 0 `@1189` i8 `−1` 不符合有效 count 检查；mode 1：两档 row 0 `@28` i32 `762536805` 越界。前者是严格游标的拒绝，不宣称编辑器会对每个负 count 返回 IO 失败。 |

兼容的 legacy 式统一是 `14 + Σrow_len + 8`。两档 footer 均 `00000000 | 01 | ec7ae404`：loader footer vector count=0、flag=1、末 u32=82,082,540，恰等于本档最大 identity；不外推。`table_extra_10.dat` 双档缺失。Extra9 在 `@12` 起可见 `00000000 0b000000 4c65732046656e6e656373`，只作为排查线索；不凭 header 251、字符串或目录名给 sidecar 分配任一 parent。

## Parent 与字段

顺序按 count 和 PE transfer；表内 offset 都是 **item-relative**：`collection.start + j*wire_stride + item_offset`。Client mode 0 只执行 transfer 三件；未执行其余 count 不是“写入零 count”。Server `NCro` 对 251 行执行 presence 读取，未读任何 tag/count/item。逐 parent JSON 保留绝对坐标、signedness、4CC、对象 load、reader sink、目标表命中及首反例。

| Parent | client / server wire items | 通过三闸门的 L3：wire item offset | Held |
|---|---:|---|---|
| `Nntp` | 1,136 / 1,136 | `nati +0` i32；`mina +6`、`maxa +7` i8 | `sckn +4`、`rati +5`、`affl +8`，同名 enum 探针不是 scoped 域 |
| `Nctp` | 640 / 640 | `cont +0` i32；`rati +4`、`mina +5`、`maxa +6` i8 | `affl +7` |
| `Nrtp` | 254 / 254 | `regi +0` i32；`rati +4`、`mina +5`、`maxa +6` i8 | `affl +7` |
| `NTRv` | 跳过 / 2,280 | `valu +0` cash i32（0..171,492,928） | `repu` 是 UI 生成索引，不持久化 |
| `NWGv` | 跳过 / 2,280 | `valu +0` cash i32（0..1,500,000） | 同上 |
| `NSps` | 跳过 / 360 | `valu +0` cash i32（0..150,056,304） | 同上 |
| `Nfmp` | 跳过 / 2,658 | `pers +0` i32，符号扩展；`perm +7` mask `08`；`rtng +8` i8，1..20 | `desc +4` i16、`heig +6` i8、`side +7` mask `07` |
| `NCro` | 跳过 / 0 可见 | — | `comp`、`crep`：无实档 item；不发布坐标 |

**类型纠偏。** 冻结 XML 中 `mina/maxa` 是整数年龄（14–44/15–45），实际 getter `movsx` signed byte，不是 cash i32；`valu` 才是 cash i32，不推币种／缩放。`Nntp.rati` 是 enum，另两件是整数（实档 −2..18，冻结范围 −2..20）；`heig` 是枚举，不解释为身高单位。Repu getter `0x4496fdb` 写循环索引、`0x4496fb7/bb` 读并投影金额，`0x4497217/0x449721f` 精确分发 `valu/repu`。有数组时 wire 读 count 次，当前为 0/20，非无条件 20×4；无数组时 getter 可造 20 个零值 UI 行，不混同实档 item。

**引用不是 UID。** 实档读取独立目标 ordinal 集：t10 Nation 从 t47 已接受行尾重读 251 键；t5 CONTINENT 7 键、t19 REGION 28 键从双档实际 identity lanes 重读；`basic_people_db.dat` 以 5 类行长读取 658,011 个 ordinal。由本类 slot 20 `0x3d885f0` 的 displacements 确认三个 transfer resolver 与 person resolver，引用依次 1,136/0、640/0、254/0（各档同值）、2,658/0（server）。错误用 public UID 时 server 首 miss：Nation row 0 `@706`=4，Continent row 0 `@824`=0，Region row 55 item 7 `@50706`=11，Person row 0 `@284`=43016。Person 命中不局限 class 2：class 1/2/3/5 分别 1,160/285/20/1,193。不读 person 属性。Club/t3 的 84,259 个实际 ordinal 仅作 `affl` 反证：正值都可数值命中，但 `0x41bdbce` 装箱 signed byte，0 缺失，无 Club resolver；不是 Club FK。`NCro.comp` 没有 live 引用可 join；t25 client 7,047 条真实 identity 仅供目标基线，不宣称实档验证 server comp 引用。Nation owner 修复和 `+0xb9` backlink 原有条件不变，不声称所有行选第 0 侧。

**掩码与枚举。** `0x1077d57/65/68` 得 `(byte>>3)&1`，setter `0x107730d/0x107737e` 单独 set/clear `08`；`0x1077e50/56` 取同 byte 的 `07`。server 首 item `@291 0c` 同时 `perm=1, side=4`，直接反驳“整字节布尔”；全表 1,731 个真、927 个假。同名枚举试验不当作专属 ref：`desc` 首不匹配 row 23 item 3 `@22298 0000`、`heig` 同项 `@22300 00`；不重编码或推断 UI 默认。`side` 经 mask 与同名值域相交，因无 scoped `enum_ref` 保留 held，其 raw/解码值分别记账。

## 五类分支：覆盖与反例

- **wire_data**：三个 transfer count 独立，`Nntp` 多一次 byte 读；repu count-1 合成并插 4 B 后整表 EOF 平移 4，单改 count 在 `@3575` 首次 identity 失败。Server `NCro` 首 presence `@281=0`；合成 gate=1、tag/count/item 后 EOF +14，仅验证静态形状。Nfmp 首 lane `@284` 改零，EOF 不动，`0x105da2d` 不 append，不等于项未消费。
- **runtime-external**：mode 分叉见上，mode 0 少读并非 selector 值导致。版本阈值、长度上限均是外部上下文与 wire 值的条件，不将 guard 常数视为档内字段。
- **IO-result**：stream `+0x10` / helper AL；截断到 server `@705`（首 Nntp count）得到 short transfer；各成功读点另存首 witness。不把 I/O 失败解释成第二布局。
- **context-lifecycle**：`0x11d21c6` 空 stream 跳过 identity，不能成为有效行；TLS、内存分配、append、refcount 与 callback 只抽象为成功有效上下文，并不声称实机观察。
- **dead**：`0x11d23df/0x11d23fd` 的 JNE taken 要求紧邻 `xor eax,eax; test al,al` 后 AL 非零，矛盾。未观测不等于 dead。

分片共记录 833 条条件分支：`wire_data` 56、`runtime-external` 31、`IO-result` 260、`context-lifecycle` 9、`dead` 2，另有 475 条只保存谓词及边、尚未归因。尤其 `0x360e3ce/0x838b6b` 两个 typed-container count 本档只走零路径，非零保留拒绝；没有把其通用语法或 sidecar reader 当作已证明。变长推进只记录长度与分支，未命名任何非目标字段。

## 复验和交接

`FM24_DB_DIR=<WORKSPACE>/scratch/data`；`py -V:3.12 -I -B` 运行 builder、独立 `verify.py`、各自 `--help`/`--selftest`，`t01_anchors.py` **7/7**。独立 verifier 不 import builder，分别做顺序跨度解析从真实输入重算边界／四对 mode 尝试、PE 符号与字节、字段档内画像和 ordinal join。未启动游戏、编辑器或 IDA，未联网、未访问 Z:。下一步需正向证明 Extra9 loader/sidecar reader、合法 presence 非零的 `NCro` 档以及 scoped enum 域。6 个 unknown 与 t10 已验收父项不改。
