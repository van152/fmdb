# EXE_ENUMS.md — 15 个缺失编辑器枚举的逆向恢复报告

分支：编辑器字段 schema 补全（comp editor.fmf 引用但资源 XML 未定义的枚举表）。
日期：2026-11-14。所有结论只基于本机安装静态证据（editor.exe / fm.exe 副本、解包资源、语言数据库容器），未启动游戏或编辑器。

## 0. 结论总览

| 枚举 | 字段语义 | 值来源 | 值数 | 名称（显示文本） |
|---|---|---|---|---|
| `subs` | subs_rules 换人规则 | exe 静态表（字符串+id 全量） | 82（id 0..81 完整） | 未取到（翻译运行时解析） |
| `mdbj` | PCJO 人员俱乐部职务 | exe 构建函数 0x14002FC50 | 177 | id→名称未锚定（见 §3.3） |
| `mdjz` | PFjo/PSJO 俱乐部职务（含 0） | 同上（0 特例） | 178 | 同上 |
| `mj+c` | tjob 出场记录职务 | 同上（追加 63,62） | 179 | 同上 |
| `mdjc` | RJ00..RJ99 预期职务 | 构建函数 0x140030570 | 87 | 同上 |
| `mdnj` | PNJO 国家队职务 | 同上（85 值表） | 85 | 同上 |
| `ovrl` | Porl 用于补齐属性的角色 | 构建函数 0x140030A70 | 45（位置/角色位掩码） | 引擎生成，未静态还原 |
| `nprl` | PRDr 非球员战术角色 | 构建函数 0x140030EB0 | 44（位掩码，0="None"） | 引擎生成，未静态还原 |
| `Posi` | PRDp 非球员战术角色位置 | 构建函数 0x1400312C0 | 15（位置位，0="None"） | 0x1..0x400 已锚定（GK/D/WB/DM/M/AM/ST/L/R/C） |
| `foms` | AWfo 奖项阵型 | 阵型构建器 0x141CF6580 (type 0) | 32 | 由运行时游戏数据库生成 |
| `pfms` | Nppf 首选阵型 | 同上（type 0） | 32 | 同上 |
| `sfms` | Npsf 第二首选阵型 | 同上（type 1，与 type 0 同掩码） | 32 | 同上 |
| `afms` | Npaf 进攻阵型 | 同上（type 2） | 38 | 同上 |
| `dfms` | Npdf 防守阵型 | 同上（type 3） | 19 | 同上 |
| `crrp` | NTRv repu 声望区间 | 构建器 `0x141cf5f10`（静态全解） | 20 | `[10i+1]-[10i+10]` 格式化 |

机读数据：`reports/editor_schema/enum_extras.json`（与 master.json enums 同构，另加 `provenance`）；crrp 的 20 条值由 `reports/editor_schema/enum_crrp_static.json`（`scripts/b38_crrp_probe.py` 产物）供给，单一真源、不手抄常量。

## 1. 方法（如何定位）

1. **资源侧确认引用点**：15 个代码全部通过 `<flags id="enum_values" value="…"/>` 引用（数据库字段 + 规则组字段），字段语义由 XML name/hint 注释确定（见 §2）。
2. **字符串探针**：4 字节代码在 editor.exe 中不以 ASCII 存在（`subs`/`Posi` 的命中均为长字符串误命中）。
3. **换人规则值字符串命中**：`ten_from_eleven`、`*_max_three_stoppages` 等在 editor.exe 有独立字符串；这些字符串的 8 字节指针密集出现在 .rdata 表区 0x1867660–0x1867B80 → 发现 `subs` 完整静态表 `{const char* value_string; int enum_id}`（16 字节/项，哨兵 `{ptr 0x1419435F1, flag}` 分隔多张表）。
4. **字节序反转 4cc 搜索**：`mov edx, imm32` 形式的 4cc 以大端立即数出现，即内存字节为逆序（如 `mdjc` → `cjdm`）。15 个代码全部命中两类位置：
   - **运行时注册函数**（VA 0x141CAC800 起，.reloc 段内的真实代码）：依次以 `mov edx,<4cc>` 调用各构建函数；
   - **构建函数内部的 cmp 守卫**（如 `cmp ebp,0x6D646A7A`('mdjz')）。
5. **构建函数解码**（capstone 手工反汇编，非 IDA；编辑器 exe 的 .rdata 段含真实代码，Denuvo 只虚拟化部分辅助函数）：
   - 0x14002FC50：职务构建器（服务 mdbj/mdjz/mj+c；`mov cx,<id>; call 0x140032660` 逐项加值，`call 0x140835380` 把表挂到 4cc 属性上）；
   - 0x140030570：mdnj+mdjc 构建器（同一值表挂两个键，mdjc 多 [63,62]）；
   - 0x140030A70 / 0x140030EB0：ovrl/nprl 构建器（记录结构 `{enum, enid, name}`，首项 name 取翻译 414515 / 292641，其余值经虚拟化辅助函数 0x140032B30 添加）；
   - 0x1400312C0：Posi 构建器（0 + 2 的幂循环，显式跳过 2；名称经格式串 `[%position#1-short]` 由引擎生成）；
   - 0x141CF6580：阵型构建器（枚举 id 0..0x40，按 list_type 0/1/2/3 经有效性与静态回退掩码过滤，0x14087A3B0 为**未虚拟化**的有效性函数）；
   - 0x140031640：subs 构建器（**已虚拟化**，但静态表已足够）。
6. **XML 枚举结构对应关系**：exe 侧 `enum`/`enid`/`name`/`envl` 属性与 enums.xml 的 `<record enum="…" enum_id="…">` 一一对应，说明 exe 表就是资源 XML 枚举表的编译版。

## 2. 引用点与字段语义（comp editor format XML）

| 枚举 | 引用文件（comp editor/format/） | 字段 | 含义 |
|---|---|---|---|
| Posi | database/non player.xml:20 | PRDp | 非球员战术角色 Position |
| nprl | database/non player.xml:28 | PRDr | 非球员战术角色 Role |
| pfms | database/non player.xml:291（club.xml/nation.xml 同） | Nppf | Preferred Formation |
| sfms | database/non player.xml:302 | Npsf | Second Preferred Formation |
| dfms | database/non player.xml:313 | Npdf | Defensive Formation |
| afms | database/non player.xml:324 | Npaf | Attacking Formation |
| crrp | database/nation.xml:2714 | repu（NTRv 列） | Transfer Values 的 Reputation Range |
| foms | database/award.xml:739 | AWfo | 奖项 Formation |
| mdbj | database/person.xml:1101 | PCJO | Job（俱乐部） |
| mdjz | database/contract.xml:12; person.xml:1112 | PFjo / PSJO | Job / Secondary Job |
| mdnj | database/person.xml:2168; database ui/person ui.xml:389 | PNJO / PFjo | Job（国家队）/ New Job（不含球员） |
| mdjc | database/club.xml、nation.xml 各 50 处 RJ00..RJ99 | RJ** | Expected Job（球队职责预期职务） |
| mj+c | database/person.xml:5118 | tjob | 出场记录 Job |
| ovrl | database/player.xml:1701 | Porl | Role Used To Fill Empty Attributes |
| subs | 规则组 17 处（basic league fixture rules.xml:13 等） | subs_rules | 换人规则 |

## 3. 逐枚举结果

### 3.1 subs（换人规则）— 完整恢复
- 来源：editor.exe .rdata 静态表 file 0x1867660–0x1867B80（VA 0x141868060–0x141868580），82 项 `{char* value, int id}`，id 0..81 无缺号。
- 样例：`three_from_seven`=0、`three_from_five`=1、`three_from_three`=2、`five_from_twelve_max_three_stoppages`=61、`ten_from_eleven`=65、`five_from_fifteen_max_three_stoppages_plus_one_et_sub`=75、`all_from_all`=18、`none`=19、`use_lowest_division_rules`=31、`use_highest_division_rules`=42、`use_home_team_rules`=53。
- 表按 value 字符串字典序存放，id 是真实枚举值（非顺序）。
- **交叉验证**：basic comps 57 国样例中观察到的 29 个不同取值、用户编辑器数据（世界 0.26.1 等）中 6 个取值，全部是本表成员。
- 显示名称：不在 exe 中（翻译系统运行时解析；本机未安装语言包 depot 2252572，无法还原文本）。

### 3.2 职务族（mdbj / mdjz / mj+c / mdjc / mdnj）— 数值完整
构建器值序即编辑器下拉显示序（非数字排序）。公共基表（177 项，mdbj）：
```
1, 157, 2, 38, 5, 100, 6, 8, 26, 55, 264, 245, 247, 4, 239, 34, 9, 243, 240, 36, 10, 173, 179,
172, 178, 7, 501, 101, 159, 160, 162, 161, 249, 163, 185, 184, 102, 103, 104, 105, 251, 106,
191, 190, 221, 222, 224, 223, 225, 261, 226, 229, 228, 107, 108, 109, 110, 111, 253, 112, 197,
196, 113, 114, 115, 116, 117, 255, 118, 203, 202, 119, 120, 121, 122, 123, 257, 124, 209, 208,
24, 125, 30, 126, 127, 259, 43, 215, 214, 170, 11, 21, 20, 39, 12, 129, 263, 13, 15, 27, 58,
246, 248, 128, 241, 35, 19, 242, 37, 23, 176, 182, 175, 181, 14, 500, 164, 165, 167, 166, 250,
168, 188, 187, 130, 131, 132, 133, 134, 252, 135, 194, 193, 42, 45, 46, 47, 48, 49, 59, 22,
136, 137, 138, 139, 140, 254, 141, 200, 199, 142, 143, 144, 145, 146, 256, 147, 206, 205, 148,
149, 150, 151, 152, 258, 153, 212, 211, 25, 154, 31, 155, 156, 44, 260, 218, 217
```
差异：`mdjz` = [0] + 基表；`mj+c` = 基表 + [63, 62]；`mdnj` = 85 项子表（见 JSON）；`mdjc` = mdnj 表 + [63, 62]。
证据：构建函数反汇编（守卫 `cmp ebp,…` 与值添加调用的相对位置即分支归属）。

**名称（未完全锚定，如实说明）**：职务 id 属 FM 职务类型体系。英文标题在两处编译字符串中可见——
- editor.exe 名称函数 0x14156C2C0（`lea rdx,[rip+…]` 字面量序列）：Manager, Chairperson, Assistant Manager, Gk Coach, Fitness Coach, Set Piece Coach, Coach, Physio, Scout, Director of Football, Head of Youth Development, Technical Director, Doctor, Data Analyst, Sports Scientist, Head of Player Development；
- fm.exe 员工职务串表 file 0x5C48045（Chairperson…Head of Player Development，14 项）。
- XML 侧职务标题翻译 id 家族：Manager=227980/227981、Assistant Manager=227983、Coach=227985、Scout=227987、Physio=227989、Director of Football=227972、Fitness Coach=227927、Technical Director=482629、Head of Player Development=482630、Chairperson=521008、Data Analyst=412817、Doctor=412819、Sports Scientist=412822（均在 resources_modding 面板 XML 中使用）。
- **未解决**：数字 id → 标题/翻译 id 的逐项映射藏在 Denuvo 混淆的调度链（case 分发）中，静态还原成本过高，本轮未完成。没有用推测填充映射。

### 3.3 位置/角色位掩码族（ovrl / nprl / Posi）
- 值是 FM 引擎的位置/角色位掩码常量（单值位 0x1..0x4000 + 64 位大掩码）。
- Posi：`0 + 2^k (k=0..14, 跳过 2)`。名称：0="None"（翻译 292641，文本已在 enums.xml 确认）；0x1..0x400 依据 fm.exe 位置短名表（file 0x5604718：`GK,D,WB,DM,M,AM,S,L,R,C`，与位序一致）锚定为 GK/D/WB/DM/M/AM/ST/L/R/C；0x800..0x4000 名称未定。
- nprl：44 值（0="None" + 43 掩码）；ovrl：45 值（0 + 44 掩码，首项翻译 id 414515，文本未取到）。名称由引擎按掩码生成（角色定义在虚拟化代码中），未静态还原。

### 3.4 阵型族（foms / pfms / sfms / afms / dfms）— 值集完整（静态回退语义）
- 构建器 0x141CF6580 未虚拟化：遍历阵型 id 0..0x40，`call 0x14087A3B0(id, list_type)` 过滤后逐项生成 `{enum,enid,name}` 记录。
- 有效性函数 0x14087A3B0（未虚拟化）：优先使用运行时表（游戏数据库加载后的 per-id 标志字节，位 0/1/8/4 分别对应 list_type 0/2/3/1）；**静态回退**（表为空时）为编译进 exe 的位掩码：
  - type 0（foms、pfms）与 type 1（sfms）：id<0x2F 且 `mask 0x75FFFFFF19F` 命中，另预排除 {1,13,17,37,43,44,45,48,49}；
  - type 2（afms）：id<0x2E 且 `mask 0x7DFFFFFFFFF`；
  - type 3（dfms）：id<0x36 且 `mask 0x13864FC3DAA007`；id 0 一律被范围预检排除。
- 结果：foms=pfms=sfms 32 值；afms 38 值；dfms 19 值（JSON）。
- **重要限制**：编辑器加载游戏数据库后用运行时标志表覆盖静态回退；静态集应是基础库的镜像，但逐 id 与实际 DB 的对应未做二次验证。名称由运行时按阵型定义生成（如 4-4-2 等），id 0 的名称走翻译 291387（文本未安装）。

### 3.5 crrp（声望区间）— 已解析（L3 exe 静态）

- 构建器：`0x141cf5f10-0x141cf616e`（`.reloc`，长 0x25e）。前一轮“Denuvo 虚拟化不可还原”的结论已推翻：函数体是普通 x86-64，`prrc` 立即数 `0x141cf6135` 只是 `crrp` 键注册点，不是混淆证据。
- 循环：计数器在 `[rsp+0x2c]`，`cmp eax,0x13 ; jge` 比较**自增前**的值 → 循环体执行 **20 次**（c=0..19）。
- 数值链（寄存器取 `mov eax,[rsp+0x2c]` → `add eax,eax` → `lea ecx,[rax+rax*4]` → `or ecx,1`）= `10c+1`；`lea eax,[rax+rax*4+0xa]` = `10c+10`。两条链分别经 `0x14081d7c0`（→ `0x14372f3e0`）写入对象 field 1 / field 2。
- 显示格式：`.debug` 模板 `[%number#1]-[%number#2]`（`0x141926a52`，全镜像只有 1 个 RIP 引用，owner 就是本构建器；RefIndex 交叉确认）。
- 结果：id 0..19 ↔ `1-10 / 11-20 / … / 191-200`（分桶连续无缝、互不重叠；脚本 self_check 全 true）。
- 佐证：用户与 basic comps 观察到的 repu 值 `[14,15,16,17,18,19]` 全部落在 `1..200` 内，且都命中 id 1 桶（11-20）。
- 残余风险（如实标注）：未证明 `repu` 字段序列化的是“桶 id”还是“区间下界”。观察值 14-19 落在 11-20 桶，与“下界”一致；要钉死需要一份含 ≥21 值的 dump。
- 方法：`scripts/b38_crrp_probe.py` 用**符号（仿射）求值**还原常量，并与观察值交叉校验；`build_enum_extras.py` 直接读它的输出，避免手抄。。

## 4. 佐证与交叉验证汇总
1. subs：29（basic comps）+ 6（用户数据）个观察值全部落在恢复表中（脚本校验，0 缺失）。
2. XML↔exe 结构同构：exe 值记录属性 `enum`/`enid`/`name` 与 enums.xml `<record enum=… enum_id=…><translation id="name"…>` 完全对应。
3. 已解析枚举（如 tvts）的 XML 定义不在 exe 表区，说明 exe 表区只补 XML 缺失的部分；blob 中其余表（月份、星期、比赛类型、联赛命运等）与 enums.xml 已有表互补，互不相重。
4. 翻译还原尝试：游戏 data/languages 不存在（语言包 depot 2252572 未安装）；database/db/2400/2400_fm/lang_db.dat 为 "tad." 容器内嵌 fmf（已解包 352 个文件，23 张 DB 文本表 × 15 语言），仅含 DB 行翻译（人名/俱乐部/奖项名等），无 29xxxx UI 翻译段 → UI 枚举显示名不可从本机文件还原，报告如实标注。

## 5. 产物与脚本
- `reports/editor_schema/enum_extras.json` — 15 枚举机读表（含 provenance；crrp 为 20 条区间桶 + L3 证据等级）。
- `reports/editor_schema/enum_crrp_static.json` — crrp 静态恢复明细（循环/符号链/self_check/观察值校验）。
- `scripts/b38_crrp_probe.py` — crrp 构建器静态恢复 + 交叉校验脚本（`python -I` 可重跑）。
- `reports/editor_schema/EXE_ENUMS.md` — 本报告。
- `scripts/build_enum_extras.py` — 由提取数据组装 JSON。
- `scripts/exe_enum_probe.py` — RIP 相对引用扫描器。
- `scripts/ida_editor_enum.py` — editor.exe IDALIB 打开脚本（本轮最终用 capstone 手工反汇编完成，未走 IDA 路径）。
- `reports/editor_schema/builder_values.json`、`_subs_table.json`、`exe_blob_dump.txt`、`exe_enum_functions.txt`、`exe_enum_final_extract.txt` — 中间证据。
- `input/editor.exe`（游戏目录只读副本）、`input/lang_db_2400.dat`、`extracted/lang_db/`（解包）。

## 6. 后续可做（未做，超出本轮范围）
- 用 IDA 数据库 + 反虚拟化跟踪 job id→标题映射（0x14156C2C0 调度链）；crrp 值表已完成（见 §3.5）。
- 从带语言包的安装（depot 2252572）还原 29xxxx/4xxxxx 翻译文本，补齐全部显示名。
- 阵型运行时标志表与游戏数据库（formation 定义）逐 id 对表。
