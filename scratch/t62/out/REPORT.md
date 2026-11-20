# t62 — EDfx 上游与 EDsc 精确分发（partial）

**EDsc 的 editor 调用链找到：它不是字面 4CC compare，而是 rel32 表的第 `0x32` 格。按选中对象进入 COMP 或 NATION 的 Schedule 生成器，结果返回 UI。** 这更新了 t53/t55 的「未找到分发」，**没有**在现代 `table_10` 主行新增 wire 槽。**EDfx** 已追到规则输入、内存日期桶与 NATION backlink，但尚未把这些输入中参与结果构造的内容闭合到具体持久化 reader/writer；不分配 backing member。无新字段坐标，L4=0。

## 1. 引用点普查与证据边界

只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。冻结 `master.json` 与 `IDA_PROVENANCE.md` 对 MANIFEST；v8 `v3_baseline` 对其原 v3 JSON/Markdown 的 SHA。除非注明 VA，下文均为 **PE file offset**。`xref.json` 包含全部原始命中、精确 key 回放、rel32 cell 及相邻键；`chain.json` 包含 277 个见证指令的 bytes、VA、分组与逐跳解释。

| 4CC | 全文件原始字节（正/反 ASCII、UTF-16LE/BE） | 分类 |
|---|---|---|
| `EDfx` | 仅反序 `78 66 44 45`，`0x29c39`（VA `0x14002a639`） | `0x29c37 cmp esi,0x45446678` 的 imm32，纯比较。等值才走生成调用；命中本身不是 opener、构造或 stream sink。 |
| `EDsc` | 六种形式均零命中 | 新发现的计算分发 `0x282d6 → 0x29389`（仅已证明的 EDsc key），不是字面引用，归为生成集合分发。 |

全量是指上述原始字节模式；不宣称穷尽所有算术编码、动态资源或间接调用。`0x28150..0x2aa20` 的 PE exception extent：直接可达 1,658 条，8 处未解间接跳转；加入 **仅 EDsc** 的已证边后 1,689 条，7 处未解间接跳转，两者均记录 21 条 extent 外边。它们未被写成死边；可达性是静态 CFG 意义，不是运行观测。无 unwind extent 的 leaf/thunk 仅逐指令见证，不线性吞邻接字节。

## 2. EDsc：正向 key 流与消费者

`0x2b47a/490/49d → 0x2b4a2 → 0x28150` 是一个通用 UI 调用点：传原 key、选中对象、输出槽；`0x28163 mov esi,r9d`。回到 `0x2b4a7/4a9` 检查成功，`0x2b4ab/4ba` 把返回值按原 key 装入调用者结果。此链证明接口与输出用途，不证明哪份外部 schema 资源在实机触发了该调用。

1. `0x281cb/d3 → 0x282a1/ad` 的比较树对 `EDsc=0x45447363` 进入归一化。`0x282b9 add esi,0xbabb8ccf` → `ESI=0x32`；`0x282bf cmp esi,0x43` / `0x282c2 ja` 未越界。`0x282c8 lea` 取表 VA `0x14002b1f0`（off `0x2a7f0`）；`0x282cf movsxd` 取 cell **`0x2a8b8`**，原字节 **`99 eb ff ff`** 即 `-0x1467`；`0x282d3 add` 和 `0x282d6 jmp rdx` 得 **`0x29389`**（VA `0x140029d89`）。在 68 格中只有 `0x32` 指向此目标。邻键反例：`EDsb`/`0x31` → 默认 `0x2a684`，`EDsd`/`0x33` → `0x293e9`。因此不能按邻近常数、同名前缀或槽位范围把整个区段报成 EDsc。
2. `0x29389/8b`：若 `AL=0`，走已初始化输出的成功返回，不构造 schedule；否则 `0x29396/99`、`0x2939f/a2`、`0x293af/b6` 要求 selected 非 null、`BPL=0`、全局 context `+0x54c` 非零。`0x293c2` 调 selected 对象 `vptr+0x38`，`0x293c5/c8` 比较 type 25；失败再在 `0x2a238/23b/246` 比较 type 10，其他类型走默认拒绝 `0x2a684`。这是 **对象/context** 分叉，不是 client/server archive mode。
3. **COMP (25)**：`0x293df → 0x6c120`，`0x293dc` 设 `R9B=1`；`0x6c130/154/157 → 0x6c260` 保留参数，`0x6c273/2f3` 将其用于准备分支。此分支可由 `0x6c2fb/305` 处理 context `+0x1c0`，经 `0x6c30a/36b/391` 挂接规则表示；`0x6c5fa` 可调日历准备 helper，`0x6c692/731` 参与生成项。`0x6c20d/21a` 处理临时项（`0x6c92c/931` 取 `date` key）；`0x6c22a/237 → 0x83d5a0` 将装箱结果交调用者。条件路径保留，不宣称每次请求都生成非空结果。
4. **NATION (10)**：`0x2a252 → 0x6bb00`。`0x6bb37..5b` 的若干全局位均未开启时可直接给空的默认值（`0x6bb6e`）；另一臂用 context `+0x1c0`（`0x6bb9b/0x6bc14`）准备并枚举输入。`0x6be59/5f/62 → 0x6c120` 以挑选的输入和 `R9D=0` 委托逐项处理；`0x6be6a` 取返回列表，`0x6bed6` 追加投影项，`0x6c0d0 → 0x83d5a0` 返回汇总。它没有跳到 t55 主行 reader `0x103fac0` 或把某个 wire stream 传作 NATION。

冻结 schema 的 `nation.xml#nati` idx 344 和 `advanced\database test\comp test.xml#cpts` idx 22 均是 EDsc。它们与双对象分发一致，但**不凭 scope 名字一一断定实际 UI 资源绑定**，也不据 `date` 的键证明 `date/day_of_week/nstr` 的磁盘编码。t55 源台账实际为 **`grade=held, slot=null`**、理由为 t53 未找到分发；任务简称 `no_main_wire_slot` 仅沿用其现代主行范围，**不是原 grade 标签**。原 `held` 行、v3 四条 `negative_regressions` 和 t53 零字面命中等旧证据均不改；「无已验分发」是旧检查的结果，不再作为当前结论。

## 3. EDfx：静态上游走到哪里

| 逐跳 | 本次可引用的结论 |
|---|---|
| `0x29c37/3d` → NATION gate `0x29c66/69/6c` → `0x29c80 → 0x907f0` | exact key，选中 type 10。别的对象类型（如 24）不进这条生成臂。`0x90803/0b/13` 分别保存输出、选中对象和编辑器上下文。 |
| `0x90818 → 0x2cdc0 → 0x1b7a2f0`；`0x90864 → 0x2ce20 → 0x1b7a3c0` | 从 context `+0x20` 的已装箱输入中以 `0x666c6573`（`fles`）取容器并按指针项枚举；缺少该输入的空 fallback 保留。不是 `.dat` 文件名打开器。 |
| `0x9087b/80` → `0x908b0/0x908b8 → 0xa2d350 → 0x37d5c40` | 检查每项 `comp` 再传规则/对象表示；同一 helper 先尝试已有 `+0x18`，缺失才在传入容器上查 `comp`（`0x37d5c70/cbc`）。这是间接内存来源，不足以将规则行内容等同于 `table_25.dat`。 |
| `0x908c3 → 0xafe0f0 → 0x385d630`；`0x908ce → 0x6288b0`；`0x908d8` | 以对象指针比较并移除 `context+0x1c0` 里的对应缓存项（`0x385d681/6a6`），把同一 `+0x1c0` 指针挂到临时 wrapper `+0x38`，再调处理函数。没有在这几跳观察到 I/O 或 write-back。 |
| `0x908f1/0x90906`、`0x909ca → 0xaf8900`；`0x90918/8e/9d` | 以 runtime 年/日期界限准备并遍历日历。备用输入和年份重建不是 archive mode；`0xaf9659/af965c` 取的是内存 vector 的 begin/end。日期边界全局 VA `0x141a80808/0x141a8080c` 的设置来源未绑定。 |
| `0x909d7/0x909d9 → 0x103f9f0 → 0x3d5c080/91`；`0x90a18..24 → 0xb02980` | `EDX=0` 固定取 `NATION+0x108`，**不是** getter 输出向量或 wire 槽；把这个 backlink 给 R9，两日期参数同指当前日，RCX 是 `context+0x1c0`。 |
| `0xb02af1/af5/af9 → 0xb02bf0/bf7/c03 → 0xb02c7e/81` | 日期索引查从 calendar `this+0x38`（editor context `+0x1f8`）开始的桶，随后逐项过滤（`0xb02ca8/cba/ccd/cd4`）；有条件经关联对象 `+0x60`，再比较其 `+0x110` 或 `+0x108` 与 R9 backlink。该 join 不能反推哪个 reader 创建桶，或哪个 writer 保存具体输入。所追路径还有空返回与 fallback。 |
| `0x90aa8` / `0x90f93` → `0x90fc3/0x90fd3 → 0x83d5a0` → `0x29c85/0x29f68` | 投影项进入局部列表，出口把两 qword 移交 caller 输出槽（`0x83d5d2/d6`）。该生成路径未见列表送归档 writer；不外推给所有调用者或输入。 |

**对照而非别名。** t27/t39/t44 的集合范例不因 v3 将 `AXML/EDfx/EDsc/Tchl` 同组而共享 backing：CLUB slot 2 `0xe89a00` 的已知 Tchl 精确比较在 `0xe8c67e`；`0x15e9830 → 0x44d7bf0` 从全局 VA `0x141b60158` 的 table `+0x80` 取指针，`0x44d7cc5/cd1` 比较已修复 owner 的 `+0xc`。与已追的日期桶和 backlink 不是同一已证明对象链。也没有把 t44 的具名附属 reader 借给 EDfx。

**还差的闭环**：从实际进入 bucket 的规则/fixture 内容回溯到一个具体 opener、reader 和字段填充点，再证明反向 writer 消费相同内容，而不仅是同一 COMP identity、日期或共享全局。当前 `reader/writer/member=null`；不把现有数字表、sidecar 或外部规则文件列为已确认来源。`exclusions.json` 提供七项可重开的排除/识别闸门。

## 4. 数据侧与复跑

独立 FMF 解码复核目录：client **31**、server **77** 项，均无 path 包含 `EDfx`/`EDsc`（不区分大小写）。仅排除同名路径，**不排除间接映射、无标签段或外置资源**。以 `data_base + entry.offset`、下一成员/TOC 边界、Zstd EOF 与声明解压尺寸复核 t10/t25 正对照；只读头 count，不重做既有 L3 或猜新的 item 坐标。

| 对照成员 | Client count / 解压字节 | Server count / 解压字节 |
|---|---:|---:|
| `table_10.dat` | 251 / 24,732 | 251 / 422,345 |
| `table_25.dat` | 7,047 / 894,991 | 7,047 / 1,533,972 |

没有可分派给 EDfx/EDsc 的已证归档段，因此没有报告两档的 schedule row 数或 archive mode 差异；对照表尺寸差异不构成其差异。独立 verifier 不 import builder、`ReaderCFG` 或 `fm24_dump`；以原始 opcode 重走四个 key、独立重建 CFG、独立目录遍历与定界解压。两脚本 `--help`/`--selftest`、builder/verify 以及 anchors **7/7** 已通过。退出码 `0` 成功（含证据标记为 partial）、`1` 核验失败、`2` 用法/致命错误。未启动游戏/编辑器/IDA，未联网、未访问 Z:，未改 `reports/` 或旧任务数据。

```bash
export FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t62_edfx_edsc.py --build
py -V:3.12 -I -B scratch/t62/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
