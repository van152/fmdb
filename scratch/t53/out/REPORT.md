# t53 — TCrs：主档与 getter 后备集合分别闭合

**裁决：`table_9.dat` 持久化 t9 `this+0x188`；Nation `TCrs` getter 用的是 `[this+0xb0]+0x48`，它在 `table_extra_9.dat` 的名字前缀之后另有独立持久化段。** 两成员均 client mode 0 / server mode 1、各 251 行／块闭合；共享 item reader、对象宽度和分配池，不共享已证明的向量。四个 schema 子字段仍 held。EDfx 生成结果在所追路线中只交 UI；EDsc 加固 negative，未裁决不持久化。L4=0。

## 1. 两个向量的静态证据与 wire

静态来源为只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。下文地址是 PE file offset；指令分片附 VA 和原 bytes。冻结 schema 对照 MANIFEST：`master.json` SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`，`nation.xml#nation` idx 64。t51 Nation→t9/base 的 owner 链不改。

| 证据 | t9 主档 `this+0x188` | TCrs getter `[this+0xb0]+0x48` |
|---|---|---|
| 写点 | `0x1059d50` 清零；`0x105dd20` 分配新 24 B 向量头，`0x105dd56` 保存 | `0x11d3429` 写扩展对象指针，`0x11d4b71` 分配新 24 B 头，`0x11d4bad` 写扩展对象 `+0x48`；setter `0x3ebb8c7` 也写该槽 |
| 读点 | 主档反向 writer `0x10608bb/dc` 取该槽生成 presence，`0x10608e9/f8 → 0x155b390` 取该向量写项 | `0x11f15ab → 0x15634b0 → 0x4391e40`；`0x11f3e44/54` 与 `0x11f40a8` 读扩展槽，`0x11f40d8` 投影 |
| 填充／池 | `0x105dd63 → 0x155b450` | `0x11d4bfe → 0x155b450`；setter `0x3ebb8ec/f3` 分配同宽项 |
| 共用部分 | `0x155b450 → 0x4387ab0 → 0x155c120`；`0x155c268/2c5` 从 `VA 0x141b5e150` 分配 **12 B 内存对象**，填后 append 到**各自传入**的向量；不从池地址推别名 | 同左。没有在已检查的调用链中发现把 `+0x188` 迁到 getter 槽的步骤；不声称已证明所有路径永不复制／别名 |

### 主档：兼容 t49 已接受行界

`0xf2ba38/51` 转发外部 mode 进 slot 19；`0x105cb2c` 取 caller 栈 byte，`0x105cbb1` mode 0 直达 `0x105dd70`，不读 presence。`0x105cb49/51` 取 context `+0x588` 并比较 `0xdc3`；现代重放走 `>0xdc3`，包括 `0x105dbc0/c5` 跳过较早 linked-Nation transfer。版本改变前段文法，不是 `0x105dd63` 自己带版本参数；presence 为真才直调共享 vector reader。版本上下文不是运行观测。ReaderCFG 从 PE exception extent 得主 reader 2,141 条、共享 vector reader 91 条、内项 reader 334 条；分片也发布选定的间接 rel32 分发格。

Server **166/85** 行 presence=0/1；row 0 `@673:00`，row 1 `@1726:01` 后 `@1727` vector version=2、`@1731` count=25，25×12 B 从 `@1735` 到 `@2035`，共 **308 B**（不含 presence），紧接 `0x105dd87`。**85/85** 非空段逐项闭合到下一个已接受 transfer，合计 **2,219** 项；没有搜索 identity 去断行。Client mode 0 是 251 行均跳过，不是 251 个零 presence。两档均重读原行尾 identity 和 9 B footer `00000000 | 01 | ec7ae404`；主档 EOF 31,956 / 307,564 B。t49 旁段只作冻结 trace 和边界，不重做八个 parent 或命名其它变长站点。

### Sidecar：名称表形态不排斥后缀中的独立段

`0xf51665/71 → 0xf55120 → 0x3bb9650` 取 context `+0x60` 的表并转发 mode；`0x3bb9698 → 0xffa3b0 → 0x3cefbe0` 拼名字，`0x3bb96d6` open；`0x3bb9708` 读块数、`0x3bb9748` 读 ordinal，`0x3bb97e2/ec` 用该 ordinal 取 t9 对象并调 `0x11d3200`。`0x3b94c5a/5d` 是接现成 stream 的另一入口，固定传 1；不是此命名路径的 mode 来源。`0x1059a48` 给基类构造传 1，`0x3ea15ea` 写 `this+0xba`；`0x11d346b/3472` 因此执行首个名字字符串读。`0x11d413c/43` 才是 mode 分叉，mode 0 不进入 extension 尾部。

**t50 L1 名字证据保持成立。** 双档 251 块，第一块 `@12` 的 `ordinal=0 | len=11 | Les Fennecs` 不包含责任项。此次不扫描块内字节来找项目：从 `@12` 顺序走 `ordinal + string + 2 + string + u8 count × 27 + 8`，mode 1 再走 `i16 count × 20 + i8 count × 6 + 16 + u16 typed_count`。只实现实档出现的 typed selector 9：`0x11d4959 → 0x14cf6d0` rel32 cell → `0x14cf8bc` 写 vptr；`0x11d49b6` 的 vslot `+0x10 → 0x14d5ea0 → 0x42dba50`，消费 `8+2+8+2` 和四个长度前缀字符串。其它 typed selector 不解释。最后 `0x11d4b5a/5f` 读 presence，非零才到 `0x11d4bad/4bfe`。这些非目标站点只用来推进。

Server presence **179/72**；72 个存在的向量中 **39** 个 count=0，33 个有 **76** 个 item。第一实项 row 6：presence `@3235:01`，`@3236` version=2，`@3240` count=1，`[3244,3256)` 为 `0300838e5200aa0005000200`，精确落到下一 ordinal。`12 + Σ spans = 105228`（server）/ `83927`（client），无另拆 footer；两档从头顺序走到 EOF。正是这个 **item 级闭合** 将 getter 槽绑到 sidecar 的后缀；不据此把其它块内未命名数据归给 TCrs。

**t50 歧义双列保留，不改旧文件。** Client 所有 t50 block 边界一致。Server t50 最早候选起点 row 2 `@867` 对照本 reader `@875`，row 82 `@39439` 对照 `@39533`；这两个位置都在 t50 自己保留的四解里。首反例：row 1 `@866:01` 后，`@867:02000000` 是 version=2，后随 `@871:00000000` count=0；故它们一并被 row 1 消费，不能当下一块的 `(ordinal=2,len=0)`。第二处本 reader 在 `@39439` 仍有 94 B 待消费，包括 selector 9 记录及 presence；对应的 4 个相邻块跨度全部双列发布。

| 成员 / reader | Client 错 mode 首例 | Server 错 mode 首例 |
|---|---|---|
| 主档 slot 19 | mode 1 `@28` i32=1543569408，invalid count | mode 0 `@59` raw identity `(0,0,0)`，不是 count |
| Sidecar 命名 reader | mode 1 row 0 `@991` u16=65535，invalid typed count | mode 0 row 1 `@262` 读出 ordinal=67108864，预期 1（不是 count） |
| Sidecar 强套主档 slot 19（旧负例，双档一致） | mode 0 `@1189` i8=-1；mode 1 `@28` i32=762536805 | 同左；raw 逐档原样保留 |

另：禁用 sidecar 对象名字臂，两档均首行 `@18` invalid string count=1699479552；它不是替代 mode。

## 2. 逐项三重闸门

第一闸：parent 64 内四个唯一真实 scope。第二闸：`0x4387250` 发精确 key；`0x155a337/35a` 以 `key-0x50556e49` 查 rel32（格、目标和原 bytes 在 JSON）；对象 load 与 reader 目的相合。第三闸按档内实域判断，**不把 L3 静态槽证据晋升为已通过域的字段**。两个成员的实档 vector version 都是 2，全部 item tag=3：`tag i16 + 4+1+1+2+1+1`。`0x155c378` 在 tag<2 时将 job lane 缩成一 byte；`0x155c3f3` 在 tag<3 时省最后一 byte；故可达 wire 长度 10/11/12 B，不是从 12 B 分配硬套。version≤2 还启用 `0x4387b6f/bad` 的内存清理（对象 `+4==ad`），不能把消费数当 UI 行数。

| Code | tag 3 item 偏移 → 对象 | 域检验／首例 | 判定 |
|---|---|---|---|
| `PUnI` | `+6` u8 → `+4`，`0x155a35c` / `0x155c33d` | 无 scoped `enum_ref`；getter 源首 `@3250=170` | held，不猜标签 |
| `PUnT` | `+7` i8 → `+5`，`0x155a4c1` / `0x155c360` | 无 scoped `enum_ref`；主档首 `@1742:ff` 按 `movsx` 为 -1，getter 缺失；不能以 255 查域 | held |
| `PUnP` | `+2` i32 → `+0`，`0x155a42a` / `0x155c31a` | t49 法走 `basic_people_db.dat` **658,011** 条真实 ordinal tail；只读 identity，不读 PDxx 或把不同的 `people_db.dat` 当成同一文件。主档 2,219/2,219 为 -1，不报 live join 率。Sidecar 76 live：ordinal 12 hit/64 miss（84.21% miss），raw 当 UID 74 hit/2 miss（2.63% miss）；首 `@3246=5410435` 是 UID 命中 ordinal 43514、不是 ordinal。首假同域 row 30 `@17486=15224`：ordinal→UID 523259，UID→ordinal 2590。首 UID miss `@50631=80012188` | held |
| `PUnJ` | `+8` u16 → `+6`，`0x155a3c3` / `0x155c38d` | **有** scoped `ftjn`；sidecar 74/76 命中，首 live 冲突 row 129 `@55950=109`；row 213 为 0，getter 缺失，另记，不能用来抹掉 109。主档 1,794/2,219 命中，首 miss `@1827=100` | held |

`PUnP` 的分叉解释两条数据路径为何不能混：`0x155a464/46e` 或 `0x155a55f` 测对象 `+9`；非零时可走 ordinal 索引向量（例如 `0x155a4b8`），零时走 `Pers` 装箱或另一 runtime 查找分支（`0x155a599–5b1` / `0x155a5b8–5c4`）。实档 main `+9=1` 但全哨兵；getter 后缀 `+9=0`。UID 对照支持区分编码，但不以它代替 ordinal 闸门，亦不解决两条 UID miss。

**状态位不冒充 schema 布尔。** `+10` 对象 `+8` 是整 octet transfer；sidecar 75×`02` / 1×`08`（row 213 `@97610`），`&02` / `&08` 的计数分开，整 byte 非零会把两形态混成同一值；t49 `@291` 的 `07`/`08` 提醒不能这样命名。`+11` 对象 `+9` 在已验 getter 是非零测试，非静态已证的单 bit mask，两档各集合的 raw/掩码计数均记录；schema 无第五个 bool 字段，不晋级未知位。

## 3. EDfx / EDsc

**EDfx：裁决的是生成结果，不是所有上游输入。** `0x29c80 → 0x907f0` 分开传 UI context、type-10 NATION 和 caller 输出槽，`0x90803/0b/13` 分别保存。UI context `+0x1c0` 还接收从 `comp` 取得的视图输入（`0x90880/c3`）；`0x909d9 → 0x103f9f0 → 0x3d5c091` 取得 Nation backlink，再 `0x90a24` 用日期和 context 查询／造当天结果。`0x90a32/ae0` 迭代临时向量，`0x90aa8` 把装箱的 UI 项附到局部列表；无匹配日的 fallback 也构造同类列表项（`0x90f93`）。`0x90e07–1c` 释放／清掉临时范围。唯一已追的产物出口：`0x90fc3` 装箱局部列表，`0x90fc8/0x90fd3 → 0x83d5a0` 移入先前保存的 caller UI 结果槽（`0x83d5d2/d6` 写两 lane）；清理两个局部容器后 `0x29c85 → 0x29f68 → 0x29f7f` 直接以成功状态返回。**此生成输出路径没有 archive opener 或 record sink；editor-only 结论只覆盖该输出。** 作为源的 DB／竞赛规则／日历输入可能持久化，不给 EDfx 一个 backing member 或字段坐标。

**EDsc：仍未找到调用链。** 冻结 Nation idx 344 `allow_add/remove=false`；同 code 另在 `advanced/database test/comp test.xml#cpts`。ASCII 双字节序和两种对应 UTF-16LE 形式在 editor PE 仍零命中。PE 未列 `.rsrc`；资源探针不覆盖外置资源。对 `0x28150` 直接可达 dispatcher 的 ESI/EDX/EAX 算术和 compare 检查相关窗口／EDsc 常数，没有连到 EDsc 的分发边。未解一般 computed dispatch、间接 selector 或外部资源加载，因此是 **「未找到调用链」而非「已有证据证明不持久化」**。`date`、`day_of_week`、`nstr` 不发映射。

## 4. 验收与限制

- `FM24_DB_DIR=<WORKSPACE>/scratch/data`，Python `py -V:3.12 -I -B`。builder + 独立 verifier、两者 `--help` / `--selftest` 通过；`t01_anchors.py` **7/7**。独立 verifier 不导入 builder、ReaderCFG 或 `fm24_dump`，重读归档目录和真实帧、复放四份目标 span、复算 joins、原指令与 PE 工作队列、分派格和旧 SHA。
- t37/t47/t49/t50/t51 negative、held 和 baseline 未改；所追范围的冲突以双列与首例保留。没有开启游戏、编辑器、IDA，没有联网或访问 Z:。静态和实档重放不是 L4。未验证 t9 旧兼容版本、其它 aux typed selector、两种 vector 在未检查路径的潜在合并、完整 EDsc 资源路径。
