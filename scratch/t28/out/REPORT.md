# t28 — Nation client 变量尾 reader → wire

**结论：`arg8=0` 的 nation client 路径闭合 251/251 行、931 个 item；新增 L3 23 个（4 个 list 父字段、19 个子字段）。** 加上 t25 的 `Ncti`、`Ncur`，本分母为 **25/49 L3**：direct **6/21**，nested **19/28**。L4=0。

## 路径、分支与坐标

只读 `D:/tmp2b/fm24/input/editor.exe`：SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`；NATION vtable `0x1418893b8`，slot 19 `file+0x103fac0 / VA 0x1410404c0`，slot 2 `file+0x1041f30`。`master.json` 与二进制来源快照均对照 `evidence/MANIFEST.json`。client table_10 member SHA-256 `7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34`。

- CFG 由 PE runtime-function 边界构建。主 reader 有 992 条可达指令、154 个基本块；另有 item、date、identity 和内存辅助函数。证据分片共 1,912 条指令、184 个条件（`wire_data` 10、`runtime_external` 105、`dead` 10、`unresolved` 59）。每个条件给出 flags producer（可追时）、两个后继及选中路径的命中数。`dead` 只标记该条件的不可行 taken 边：例如 XOR 后 `jne`，或 NULL-stream 跳过读却立即解引用 NULL（`0x39dd7bc`、`0x3d8832f`、`0x3d88373`）。未走的分支不因此判死。分片标注中 `file_offset`、`VA` 和引用键都使用十进制整数。
- loader 在 `0xf2ba0e` 先读一字节 selector；`0xf2ba38` 独立传入 `R12B`。reader 的 `0x103fae6`、`0x10409d3` 测同一个外部栈参数，不是行内 selector。以 `arg8=0` 解释 client：由入口跳到公共前缀，D 后跳过 43B 额外标量块。仅强制走 D 后额外块的对照在 row 0 就读到假 identity：`@0x6d = (83, 21574, 17920)`，而不是 `(0,5,5)`。这不是对 `arg8!=0` 入口路径的重放，也不将该路径归到 client 或 server。
- 在线性列举的 40 个顶层 `vcall +0x28` 中，**0-based calls 24–27**（1-based 25–28）读 A/B/C/D 计数；**0-based 28–39**（1-based 29–40）是上述跳过的 43B 标量块，没有 client 坐标。1-based call 24 即最后一个 1B 前缀 transfer `0x10406e7 @ row+23`。item 调用及内部 stream transfer 另计，不掺进这个线性编号。
- walker 按 CFG 和签名计数反复执行 item helper，按成功 I/O、有效 stream 和活跃引用的上下文推进。reserve、alloc、append、indexed copy 和 `0x1040ba5` 的 `Ntxr` 对象整理不接收 stream wrapper，按零消耗处理；没有把内存维护或 callback 当作字段，未展开传递分配器/回调体。`0x1040bcf → 0xfae340 → 0x3c600f0` 后由 `0x3c60119` 一次读 12B identity 到 `object+8`。`0x3c60131` 比较刚读的序号与 `10000001`，本表全走保留线上的值。行号仅为后置校验。
- t25 坐标原点不变：`row_start=selector+1`，第一行为 payload+14。t25 的每行末尾零字节在 loader 坐标系中是下一行 selector，末行的零则属于 footer 的首字节。全表每个 count、identity、span 均与 t25 对账；物理闭合为 **`13 + 24710 + 9 = 24732`**（原 t25 为 `14+24710+8`）。row 55 的 identity 仍为 `@0x1042 = (55,110,110)`。

## 集合绑定

`A/B/C/D` 在下表公式中表示该行的计数。`j` 从 0 起；子字段的行内坐标为 `items_start + stride*j + item_offset`。list 父字段的宽度指 count 的宽度，不是整个 list 的宽度。

| 集合 → schema | count call / item call（file offset） | count 坐标 | items 起点 | wire / 内存 item 步长 | nation 成员 | 非空行 / item 数 |
|---|---|---|---|---|---|---|
| A → `Nlns` | `0x1040717` / `0x104075b` | 24, i8 | 25 | 5 / 16 | `+0x48` | 237 / 492 |
| B → `Nefr` | `0x10407b0` / `0x1040829` | `25+5A`, i32 | `29+5A` | 28 / 48 | `+0xa8` | 43 / 214 |
| C → `Nnfr` | `0x104086c` / `0x10408eb` | `29+5A+28B`, i32 | `33+5A+28B` | 28 / 48 | `+0x90` | 20 / 63 |
| D → `Nagr` | `0x1040927` / `0x10409a7` | `33+5A+28B+28C`, i32 | `37+5A+28B+28C` | 12 / 16 | `+0xc0` | 126 / 162 |

B/C 同用 `0x15cf4a0 → 0x448fa90`，**不能靠宽度互相区分**：`Nefr` getter `0x1042047` 写 selector 0，选对象 `+0xa8`；`Nnfr` getter `0x104222e` 写 1，选 `+0x90`。`0x3d75dc0–0x3d75ddb` 给出选择及元素解引用。`Nlns` getter 从 `+0x48` 取 16B 步长元素；`Nagr` 从 `+0xc0` 取 16B 步长元素。子 getter 从各自父调用链进入，B/C 的四个嵌套 jump-table cell 单独保存 RVA 关系和原字节。

| 适用集合 | 每个 item 的 wire 偏移：`4CC / 宽度 → item object_off`（递增排列） |
|---|---|
| A | `0:lang/4→0x00`, `4:perc/1→0x08` |
| B、C | `0:nfrn/4→0x00`, `4:nfrc/4→0x08`, `8:fren/4→0x10`, `12:nfrr/4→0x18`, `16:nfra/4→0x20`, `20:stdt/4→0x28`, `24:endt/4→0x2c` |
| D | `0:NGag/4→0x00`, `4:NGsd/4→0x08`, `8:NGed/4→0x0c` |

B/C 前五次各读 4B，末两次分别普通调用 `0x448fb33` 和尾跳 `0x448fb4d`，经同一 date thunk 落到 `0x39dd7d4` 各读 4B；因此是 `(5+2)×4=28`，不是 20B 或 24B。

## 规则核验与未晋级项

- 4B 引用值用目标 client member 的 ordinal 域逐值验证，`0xffffffff` 只准作可选项的空值。B/C 的每个 item 恰好一个 selector 引用非空（214/214、63/63）。`Nnfr/nfrc` 63/63 空，仍有独立 getter 和 reader 槽位证据；没有声称在本表观察到其非空值。
- `Nlns/perc` 的 492 个 wire 值为 1–100，全部在 schema 的 0–100 内。`0x104078d` 检查 A 容器只有一个元素时，`0x104078f` 将对象百分比改写为 100：命中 91 行，其中 17 行 wire 值不等于 100。台账画像保留原 wire 值。
- 六个日期列逐值按 getter 的位拆分核验：高 16 位年、低 9 位年内日、其余 7 位本表为零。保存年分布、日范围、`1900-001` 默认值频次。`Nagr/NGed` 162/162 为默认值；日期位置由 getter 区分，而不是由该常量推断。本次四个集合没有晋级的 schema enum 或 bool；不把引用或日期低位当 enum/bool。
- **Direct 剩余 15**：6 个语言标记字段 `Nnam/Nsnm/TCnn/TCht/N3ln/Nnty` 为 candidate（无行内绑定）；`ttcl/tbcl`、六个 `Tko*/Tkg*`、`Ntxr` 未解。**Nested 剩余 9**：`Ntxr/lowa,uppa,capa,perc,txty,ppty,year,fram,leve` 未解。`Ntxr` getter 的对象容器是 `+0x60`；post-D 整理不构成读入证据。不把 list 名称或同名 `perc` 当作坐标。
- t25 的七个 prefix 锚点照旧，其中只有 `Ncti/Ncur` 进入 49 分母。t01g 的 negative 原样保留；`Ncpi` 单独归 t22，不计分母。392 unmarked 不做新归属，不读 server table_10，不运行 editor 或游戏。

## 复验

```text
py -V:3.12 -I -B scripts/t28_nation_tail.py --selftest
py -V:3.12 -I -B scripts/t28_nation_tail.py
py -V:3.12 -I -B scratch/t28/out/verify.py --selftest
py -V:3.12 -I -B scratch/t28/out/verify.py
```

Verifier 不 import builder，用独立的 frame 算术从 `scratch/data/client_db.dat` 重读，重核全部坐标、全表画像、首/中/末 item 样本、row 55、分支计数、静态字节/VA、PE CFG 边和 scoped getter 链。两脚本均提供 `--help`，退出码 `0/1/2`。旧仓 `fm24/scripts/modding_read_dbdat.py` 仅被只读引用作 archive codec，不作为新字段语义证据。
