# IDA / exe 静态证据来源登记表（IDA_PROVENANCE）

生成：2026-11-15，QA 审计整改（对应 `reports/qa/FM_FORMAT_ADVERSARIAL_QA.md` "需核实证据来源"条目）。

目的：把全仓文档中引用 `ida/*.i64`、`input/*.exe`、`editor.exe`/`fm.exe` 静态地址（VA/sub_*/指针表/file offset）的每一处登记为——**文档 → 声称来源 → 实际可行方式 → 关键 VA 清单 → 重放命令**。使任何 VA 证据都可以在不打开游戏的前提下重放核验。

登记方法（grep 证据）：

```
grep -rnE "\.i64|ida/" --include="*.md" reports/ README.md opensource/ archive/
grep -rlE "editor\.exe|fm\.exe|sub_[0-9A-Fa-f]{8,16}|0x14[0-9A-Fa-f]{7}" --include="*.md" reports/ README.md
```

命中文档 25 个（含 `qa/baseline/` 5 个快照镜像）。逐条登记见下；快照镜像统一在 §4 说明。

## 1. IDA 数据库与输入二进制登记

| 资产 | 大小 (B) | SHA-256（登记时点 2026-11-15 08:10） | 状态 |
|---|---:|---|---|
| `ida/fm.i64` | 2,385,800,251 | `00d37232f1ae8253eff3b124d2e52859cbf289d9f77b93ffd5324b5c4e204aa9` | **可打开**（默认库）。注意：登记时存在松散 `fm.id0/id1/id2/nam/til`（并行会话占用中），哈希仅代表登记时点 |
| `ida/editor.i64` | 525,058,572 | `dc4991168cd809610fb6e9afa64ce31512d459291389604f96d6164d3763f236` | **rc=4 打不开**（"Database is empty / error 4"，库损坏/空）。任何把它当证据来源的表述均视为缺陷；见 §5 加注核对 |
| `ida/editor_merge_v2.i64` | 314,123,103 | `7dcd3b57595bd859faef8b18d3e5424a778d1a65c01e8391a6463281740eb341` | 可打开；由 `input/editor.exe` 新建（MULTI_FILE_SEMANTICS_V2 轮），含手工映射的 `.reloc` 代码段（`scripts/ida_load_editor_reloc.py`） |
| `input/fm.exe` | 491,339,776 | `e1059eee82fa7832188831521a3fa633ec3260dd98d03da48b16661147e3ab48` | 与 `reports/manifest.json` 的 `SourceSHA256/CopySHA256` 一致（24.4.2，拷贝于 2026-11-14） |
| `input/editor.exe` | 74,807,296 | `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4` | **此前无任何 manifest 记录**（审计缺口）；哈希以本表为准。ImageBase `0x140000000`；真实代码在 `.rdata`（VA 0x140001000–0x141759000）与 `.reloc`（VA 0x141c64000–0x1447ea752），`.code` 几乎为空 |

工具事实：`scripts/ida_focus.py` 原先固定打开 `ida/fm.i64`；2026-11-15 增加 `--db`（选库/选原始 exe）与 `--pe`（函数边界 unwind 表来源）参数，默认行为不变（仍是 fm.i64，缺库时从 `input/fm.exe` 建 `ida/fm.i64`）。`scripts/focus_disasm.py` 增加 `set_pe()`，默认仍为 `input/fm.exe`，不影响 `pcrel_refs.py` 等既有引用方。

## 2. 逐文档登记（VA 级证据）

### 2.1 reports/DBDAT_FORMAT.md

| 项 | 内容 |
|---|---|
| 声称来源 | `fm.i64` 函数 `sub_1449A06C0`（Ssds 访问 helper）；`sub_1407C5A20`/`sub_144049A20` 来自"新载入 input/editor.exe"的临时静态加载（文档 line 14 已加注 editor.i64 rc=4） |
| 实际可行方式 | fm 侧：`ida/fm.i64` 直接重放。editor 侧：editor.i64 rc=4 不可用 → 用 `input/editor.exe`（unwind 表可用，本表已验证 `0x1407C5A20`/`0x144049A20` 有 RUNTIME_FUNCTION 记录）或 `ida/editor_merge_v2.i64` |
| 关键 VA 清单 | fm.exe：`sub_1449A06C0`（+`0x1449A06F2` capc、`0x1449A070A` exis、`0x1449A080F` indx、`0x1449A081B` iuse、`0x1449A0899` seat、`0x1449A092A` `[item+0]`、`0x1449A07B0` `[item+4]`、`0x1449A098B` `[item+6]`、`0x1449A071A` bit0、`0x1449A0B27` bit2 反相、`0x1449A0ABC` indx 分支）。editor.exe：`sub_1407C5A20`（`0x1407C5B26` fmf. / `0x1407C5B2D` afe. 比较）、`sub_144049A20`（`0x144049A84` tadc）→ `sub_141219BF0` |
| 重放 | `python -u scripts/ida_focus.py 0x1449A06C0`（fm 默认）；editor 侧 `python -u scripts/ida_focus.py --db ida/editor_merge_v2.i64 --pe input/editor.exe 0x1407C5A20 0x144049A20` |

### 2.2 reports/MULTI_FILE_SEMANTICS.md

| 项 | 内容 |
|---|---|
| 声称来源 | 行 25-27/31：`sub_142D02A80`、`sub_142D046A0`、`sub_14242C670`（fm 侧，反编译落盘 `reports/function_*.c`）；editor.exe `.fmf` 字符串 raw `0x19077DD` / VA `0x1419081DD` 及引用 `0x14022D919`(sub_14022CC10)、`0x1402344DD`/`0x140234977`(sub_140234290)；行 32 已加注"旧 ida/editor.i64 不可用" |
| 实际可行方式 | fm 侧 VA（0x142D02A80/0x142D046A0/0x14242C670）经实测属 **fm.exe**（.sdata 段，unwind 表命中）→ `ida/fm.i64` 重放。editor 侧经实测属 **editor.exe** .rdata 段，unwind 表命中 → `ida/editor_merge_v2.i64` 或对 `input/editor.exe` 临时建库 |
| 关键 VA 清单 | fm.exe：`0x142D02A80`、`0x142D046A0`、`0x14242C670`。editor.exe：`0x1419081DD`（.fmf 字符串，raw 0x19077DD）、`0x14022CC10`（unwind 0x14022cc10-0x14022df30）、`0x140234290`（unwind 0x140234290-0x140234b10）、引用点 `0x14022D919`/`0x1402344DD`/`0x140234977` |
| 重放 | fm：`python -u scripts/ida_focus.py 0x142D02A80 0x142D046A0 0x14242C670`；editor：`python -u scripts/ida_focus.py --db ida/editor_merge_v2.i64 --pe input/editor.exe 0x14022CC10 0x140234290` |

### 2.3 reports/MULTI_FILE_SEMANTICS_V2.md

| 项 | 内容 |
|---|---|
| 声称来源 | §2/§4：目录枚举链与有序树（`sub_142D02A80`、vtable `0x145D2E8F8` slot+216 指针 `0x1452EB520`@`0x145D2E9D0`、`sub_1452EB520` 的 `FindFirstFileExW` 调用点 `0x1452EBC24`、`FindNextFileW` `0x1452EBCBF`、`sub_1418CA3A0`、`sub_140FF3650`、`sub_140FF5510`、比较器 `0x1419841B0`、`0x141983CD0`、VM thunk `0x141983F80`→`0x151469FD0`）；editor 侧 `.fmf`/`database changes`(`0x1418ED725`)/`editor data`(`0x1419238B6`) 字符串引用；行 101 已加注 editor.i64 不可用、另建 editor_merge_v2.i64 |
| 实际可行方式 | §2 链路 VA 经实测全部属 **fm.exe**（unwind 命中；`0x151469FD0` 在 fm.exe .arch 段）→ `ida/fm.i64` 重放；文档中 `ida/editor_merge_v2.i64` 只覆盖 §4 的 editor.exe 字符串引用部分，两者不要混同。反编译落盘：`reports/function_142d02a80.c`、`function_1452eb520.c`、`function_140ff3650.c`、`function_140ff5510.c`；函数清单 `reports/editor_fmf/editor_merge_v2_functions.json` |
| 关键 VA 清单 | 见"声称来源"列；其中 `0x1419841B0` 与 thunk `0x141983F80` **无 unwind 记录**（叶函数/跳板），`ida_focus.py` 的 owner() 会跳过，需 capstone 或对邻接函数重放 |
| 重放 | `python -u scripts/ida_focus.py 0x142D02A80 0x1452EB520 0x140FF3650 0x140FF5510`（fm 默认）；editor 字符串引用 `python -u scripts/ida_focus.py --db ida/editor_merge_v2.i64 --pe input/editor.exe 0x14022CC10 0x140234290` |

### 2.4 reports/editor_fmf/AFE_FORMAT.md

| 项 | 内容 |
|---|---|
| 声称来源 | 函数链 `sub_1407C5A20` → `sub_1407C9180` → `sub_1412162C0` → `sub_144067A80`（信封解析）→ `sub_144068C00`（建流）；写侧 `sub_14408E3B0`、随机源 `sub_1415F7F50`（LCG 乘数 `0x5851F42D4C957F2D`）→ `sub_141758450`（间接 seed `0x1419478E8`）。**line 65 已有主控加注**：本节证据是对 `input/editor.exe` 的独立静态加载结果，非 editor.i64 库证据 |
| 实际可行方式 | `input/editor.exe`：上述 VA 经实测除 `0x141758450`/`0x1412162C0`（无 unwind 记录，跳板/叶）外均有 RUNTIME_FUNCTION 记录；可用 `--pe input/editor.exe` 重放或 `ida/editor_merge_v2.i64` |
| 关键 VA 清单 | `0x1407C5A20`(✓unwind 0x1407c5a20-0x1407c612a)、`0x1407C9180`(✓)、`0x1412162C0`(✗unwind)、`0x144067A80`(✓ 0x144067a80-0x144067bcd)、`0x144068C00`(✓)、`0x14408E3B0`(✓)、`0x1415F7F50`(✓)、`0x141758450`(✗)、`0x1419478E8`(数据指针) |
| 重放 | `python -u scripts/ida_focus.py --db ida/editor_merge_v2.i64 --pe input/editor.exe 0x144067A80 0x144068C00 0x14408E3B0 0x1415F7F50`；✗unwind 的两个 VA 用 capstone（`scripts/ida_editor_afe_scan.py` 路线） |

### 2.5 README.md

| 项 | 内容 |
|---|---|
| 声称来源 | "已确认的关键事实"节引用 `sub_144067A80`/`sub_144068C00`（指向 AFE_FORMAT.md）；目录表列 `input/fm.exe`、`ida/fm.i64`；IDA 调用示例 `scripts/ida_focus.py` |
| 实际可行方式 | 同 §2.4（editor 链）与 §2.1（fm 链）；fm.i64 可打开 |
| 重放 | `python -u scripts/ida_focus.py 0x1449A06C0`；IDA 环境变量见 README 原节（IDADIR + idalib PYTHONPATH） |

### 2.6 reports/editor_gen/VALIDATION_V4.md + validation_v4/exe_rule_evidence.md + 批量-边角看台-预判清单.md

| 项 | 内容 |
|---|---|
| 声称来源 | 行 21/182 已加注：`ida/editor.i64` 打开失败（error 4），全部证据来自 **capstone 手工反汇编**（`scripts/editor_rule_scan.py`，对 `input/editor.exe` 的 .rdata/.reloc 两段做 rip 相对引用扫描）；无 IDA 库证据 |
| 实际可行方式 | 不是 IDA 路线——重放即重跑扫描器（只读 exe 字节）；深挖样例的分派函数 0x1414eb608 在 editor.exe .reloc 段 |
| 关键 VA 清单 | 71 条规则的完整串 VA/代码引用 VA/函数估计全量在 `validation_v4/exe_rule_evidence.json`（md 摘要表 69 个 VA：`0x140f98d00`、`0x1414eb608`、`0x141186f72` cmp 'Ssds' → `0x141187a93`、`Invalid change type` 串 `0x14190e157` 等） |
| 重放 | `python -I scripts/editor_rule_scan.py`（工作区；输出 `validation_v4/exe_rule_evidence.json`/`.md`） |

### 2.7 reports/editor_schema/EXE_ENUMS.md

| 项 | 内容 |
|---|---|
| 声称来源 | 行 4 声明"只基于本机安装静态证据（editor.exe / fm.exe 副本…）"；行 126 已注明 `ida_editor_enum.py` 为 IDALIB 尝试脚本，**最终用 capstone 手工反汇编完成，未走 IDA 路径** |
| 实际可行方式 | 原始字节表扫描：`subs` 静态表 .rdata file `0x1867660`–`0x1867B80`（VA `0x141868060`–`0x141868580`，82 项 16B `{ptr,enum_id}`）、名称函数 `0x14156C2C0`；fm.exe 员工职务串表 file `0x5C48045`、位置短名表 file `0x5604718` |
| 重放 | `python -I scripts/exe_enum_probe.py`（引用扫描）+ `python -I scripts/build_enum_extras.py`（重建 enum_extras.json，表来源注明 file offset/VA） |

### 2.8 reports/EDITOR_SCHEMA_FIELDS.md

| 项 | 内容 |
|---|---|
| 声称来源 | 15 张枚举表逐条标注"定义于 input/editor.exe builder function VA ..."（capstone 路线，非 IDA 库）：`0x1400312c0`/`0x1400315f8`(Posi)、`0x141cf6580`(afms/dfms)、`0x141cf6135`(crrp，.reloc builder，Denuvo 未解)、`0x14002fc50`(mdbj/mdjz/mj+c)、`0x140030570`(mdjc/mdnj)、`0x140030eb0`(nprl)、`0x140030a70`(ovrl)、`0x141CAC820`(调用点) 等 |
| 实际可行方式 | 全部来自 `input/editor.exe` capstone/立即数扫描；由 `scripts/build_enum_extras.py` 生成 `reports/editor_schema/enum_extras.json`（每条带 file/VA 来源字段） |
| 重放 | `python -I scripts/build_enum_extras.py`；单点复核用 `python -u scripts/ida_focus.py --db ida/editor_merge_v2.i64 --pe input/editor.exe <VA>`（builder 均有 unwind 记录） |

### 2.9 二级引用（无 VA 或仅 file offset，不需要 IDA 重放）

| 文档 | 引用内容 | 重放 |
|---|---|---|
| reports/editor_presets/DATE_BASE_VERDICT.md | editor.exe 月表 file `0x18669c0`、星期表 file `0x18670f0`（16B/行 `{ptr,enum_id}`；行 20 已注明 PE 头把这些区域标为 `.debug`） | `python -I scripts/exe_enum_probe.py` 或按 16B 行手工读 `input/editor.exe` |
| reports/editor_gen/PRESET_CONVERSION.md、preset_specs/SPEC_FORMAT.md、editor_presets/PRESET_FIELDS_V2.md | 引用 DATE_BASE_VERDICT/EXE_ENUMS 的 file offset 表，无独立 VA | 同上 |
| reports/editor_gen/PROPERTY_MAP.md §8 | .rdata 反序 4CC dword 扫描（108 码 94 命中），无 VA | 由 property_map.json `exe_static_evidence` 字段记录；重扫 `scripts/exe_enum_probe.py` 路线 |
| reports/editor_gen/VALIDATION_V2.md / V3.md | .rdata 信封码表扫描，无 VA | 同上 |
| reports/editor_schema/DB_TESTS.md | 定性引用"editor.exe / 运行时"（exe_only 分级），行 51 明确未定位测试执行函数 | 无 |
| reports/EDITOR_SCHEMA.md、MODDING_FEASIBILITY.md、editor_gen/batch_corner_stands/实测说明.md | 定性引用（"editor.exe 逆向恢复 15 张"等），VA 证据都在上游文档 | 追溯 §2.6/§2.7 |

## 3. qa/baseline/ 快照镜像

`qa/baseline/EDITOR_SCHEMA.md`、`qa/baseline/EDITOR_SCHEMA_FIELDS.md`、`qa/baseline/RULE_TEMPLATES.md`、`qa/baseline/editor_schema/{DB_TESTS,EXE_ENUMS,NAMING_MODEL}.md`、`qa/baseline/rule_templates/patterns.md` 是 QA 分支复跑前的基线快照，其 VA/来源声明与主文档一一对应，不单独登记；核对时以 §2 相应行 + 主文档为准。

## 4. archive/retirement_static/reports/STATIC_ANALYSIS.md

退役轮产物，登记了 `D:\tmp\fm24\ida\fm.i64` 与 fm.exe 的使用（fm 侧通用地貌）。该分支已停止推进，仅作历史索引；其 fm.i64 引用不约束本轮（fm.i64 哈希见 §1）。

## 5. editor.i64（rc=4）条目加注核对

全仓 grep `editor\.i64` 命中文档 6 个，逐一核对加注状态：

| 文档:行 | 内容 | 加注状态 |
|---|---|---|
| reports/DBDAT_FORMAT.md:14 | "editor 侧地址来自对 input/editor.exe 的新建临时静态加载，不是损坏的 i64" | ✅ 原有 |
| reports/DBDAT_FORMAT.md:173 | "ida/editor.i64 仍以 rc=4 失败…没有把它说成原 editor.i64 证据" | ✅ 原有 |
| reports/MULTI_FILE_SEMANTICS.md:32 | "旧 ida/editor.i64 不可用；本次只对 input/editor.exe 做了无自动全库分析的静态定位" | ✅ 原有 |
| reports/MULTI_FILE_SEMANTICS_V2.md:101 | "原 ida/editor.i64 本轮无法作为有效库打开，故另从 input/editor.exe 建立 editor_merge_v2.i64" | ✅ 原有；结论先行第 3 条本轮另加 L3 口径注 |
| reports/editor_fmf/AFE_FORMAT.md:65 | 主控 2026-11-15 已加"证据来源更正"引注 | ✅ 原有（本轮不动该文件） |
| reports/editor_gen/VALIDATION_V4.md:21、182 | "打开失败（Database is empty / error 4）…沿用 capstone 路线"；"本轮全部证据来自 capstone" | ✅ 原有 |

**核对结论：文档层所有 editor.i64 引用均已带"rc=4 不可用 / 来源实为 input/editor.exe"加注，无遗漏。**
遗留（脚本层）：`scripts/ida_editor_enum.py`、`scripts/ida_editor_afe_scan.py`、`scripts/ida_load_editor_reloc.py` 仍指向 `ida/editor.i64`，运行必然 rc=4；属历史工具，未改（如需 editor 侧 IDALIB 重放，用 `ida_focus.py --db ida/editor_merge_v2.i64 --pe input/editor.exe`）。

## 6. 重放命令汇总与环境

```powershell
$env:IDADIR = 'C:\Program Files\IDA Professional 9.4'
$env:PYTHONPATH = 'C:\Program Files\IDA Professional 9.4\idalib\python'

# fm.exe 侧（默认库）
python -u scripts\ida_focus.py 0x1449A06C0 0x142D02A80 0x1452EB520

# editor.exe 侧（editor.i64 rc=4；用 editor_merge_v2.i64 + editor.exe unwind 表）
python -u scripts\ida_focus.py --db ida\editor_merge_v2.i64 --pe input\editor.exe 0x144067A80 0x1407C5A20

# 非 IDA 的 capstone/表扫描重放
python -I scripts\editor_rule_scan.py
python -I scripts\exe_enum_probe.py
python -I scripts\build_enum_extras.py
```

重放边界（实测）：`0x141758450`、`0x1412162C0`（editor.exe）与 `0x1419841B0`、`0x141983F80`（fm.exe）无 unwind 记录，`ida_focus.py` 的 owner() 返回 None 跳过——这些是叶函数/跳板，需 capstone 窗口反汇编或对包含函数重放。editor.exe 的 `.reloc` 代码段虽可由 `--pe input/editor.exe` 提供函数边界，但 Hex-Rays 反编译建议在 `ida/editor_merge_v2.i64`（已含 ida_load_editor_reloc.py 映射段）中进行。

只读声明：本表登记的全部重放命令只读 `input/` 副本与工作区 `ida/` 库，不触碰游戏安装目录，不启动游戏或编辑器进程。

## 7. b42 校验器规则映射（2026-11-16）

注：§1 的 `editor_merge_v2.i64` 大小/hash 是 2026-11-15 登记快照；共享 IDB 此后已重建。本节记录本轮使用的 2026-11-16 版本及其本地副本，避免将两个时点混为一谈。

| 项 | 实际来源 / 状态 |
|---|---|
| IDB | `ida/editor_merge_v2.i64` 是指向 worktree 外共享目录的 junction；本轮先复制到 `tmp_b42/editor_merge_v2.i64` 再交由 IDA 打开。分析后本地副本 SHA-256 `4c101896a78534f9b126839f70f66c300bb3449d15c51cbfe320810b89863900`；共享原件 `<OLD_REPO>\ida\editor_merge_v2.i64` SHA-256 仍为 `c544f79d3e4cbc047cbc7f8c479d4c685cf3113bf9ee4ad3a06b31c38f8a2658`，未被本轮写入。 |
| IDA | IDA 9.4 / Hex-Rays 9.4.0.260610；`idapro.open_database` result 0；94,586 functions、7,042 names。 |
| 引擎伪代码 | `sub_1408DDCC0`、`sub_140981550`、`sub_140C68830`、`sub_140934CF0`、`sub_14093B0C0`；另有 `sub_140C72AB0`、`sub_140A31180`、`sub_140BEC1E0`。归档于 `reports/editor_gen/b42_evidence/engine_decomp_*.c`。 |
| IDB-free disassembly | `engine_disassembly.txt`（5 个引擎函数）、`standard_test_disassembly.txt`（4 个 GUI/test 函数）、`validator_clusters_disassembly.txt`（fixture/squad/cup 函数），均在 `reports/editor_gen/b42_evidence/`。 |
| vtable/xref census | `vtable_name_xref_probe.json`：名字扫描 `??_7`/vftable/vtable 为 0；`sub_140981550` direct xrefs 3 个；`sub_1408DDCC0` 0 个。此处只支持“当前命名/xref 路线未定位”，不证明不存在间接入口或未命名 vftable。 |
| GUI 标准测试 | UI/test 函数反汇编归档同上；字符串与调用点结论见 `reports/editor_gen/VALIDATOR_PARITY_V2.md` §5。 |

复跑（先设置本节 §6 的 `IDADIR`/`PYTHONPATH`；只打开本地副本）：

```powershell
python -u scripts/ida_focus.py --db tmp_b42/editor_merge_v2.i64 --pe input/editor.exe 0x1408DDCC0 0x140981550 0x140C68830 0x140934CF0 0x14093B0C0
python -u scripts/ida_focus.py --db tmp_b42/editor_merge_v2.i64 --pe input/editor.exe 0x140C72AB0 0x140A31180 0x140BEC1E0
py -V:3.12 -I scripts/editor_pe_disasm.py --pe input/editor.exe func 0x1408DDCC0 0x140981550 0x140C68830 0x140934CF0 0x14093B0C0 > reports/editor_gen/b42_evidence/engine_disassembly.txt
py -V:3.12 -I scripts/editor_pe_disasm.py --pe input/editor.exe func 0x1400128A0 0x14009CF00 0x1400464A0 0x1400415A0 > reports/editor_gen/b42_evidence/standard_test_disassembly.txt
py -V:3.12 -I scripts/editor_pe_disasm.py --pe input/editor.exe func 0x1400A2E20 0x140BEC1E0 0x140C07A60 0x140CC11D0 > reports/editor_gen/b42_evidence/validator_clusters_disassembly.txt
```

IDA 生成的 `reports/function_*.c` 中与本任务相关的 8 份已移入 `b42_evidence/`。运行日志里的 `Saved ...\ida\fm.i64` 行不是共享数据库成功落盘的证据：共享 `fm.i64` 不存在，且共享 `editor_merge_v2.i64` 哈希前后不变；不要据此写入 junction 目标。`reports/ida_focus_results.json` 运行前后保持原样。`ida/editor.i64`（rc=4）未使用。
