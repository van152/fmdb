# t14 任务书:RTTI 构造锚普查 —— factory 跳表 → 类名 → 阶段二表→实体全图收口

先读 [AGENTS.md](../AGENTS.md)(证据分级、只读纪律、py -V:3.12 -I、退出码 0/1/2)。

## 一句话目标

把司令官已验证的 RTTI 硬指针链固化成正式工具,补齐 census 缺口,对 6 张 negative 表(26/29/32/36/38/39)与 E56 遗留候选正式裁决,产出**阶段二 machine-readable 全图** `stage2_map.json`。

## 已验证机制(司令官 2026-11-18 深夜实测,当输入用,不要重推导)

### 1. factory 跳表(类 = archive table_type,已交叉验证)

- editor.exe(D:\tmp2b\fm24\input\editor.exe,只读)`.rdata` 段内有 rel32 数组,**文件偏移基址 `0xF49D38`**。
- `handler_off(t) = 0xF49D38 + rel32(小端)@ (0xF49D38 + 4*t)`,t = archive table_type。
- 负对照:t10 → 0xf48f27 == t01g handler;t25 → 0xf49129 == t01f/t01g COMP handler(见 `scratch/t01/t01h_jump_table_anchor.json`)。
- 实体交叉验证(8 个精确命中,零矛盾):t0→AWARD、t2→CITY、t8→LANGUAGE、t18→DERBY、t19→REGION、t23→STAGE_NAME、t27→WEATHER、t56→AGREEMENT(对应 E22 的 awar/city/lang/drbr/regi/stgn/weat/agrm)。
- dispatch:`cmp ecx,0x49` @ file_off `0xf48b38`;63 个 dedicated 类型;每块以 `jmp 0x140f4a6a9`(default handler)结尾。

### 2. 地址口径(全仓一致,别搞错)

- `.rdata`:**file_off + 0xA00 = RVA**;VA = RVA + 0x140000000。
- 既有工件里 `0xf48bxx` 这类地址一律是**文件偏移**,不是 RVA/VA。
- RTTI 数据落在 .debug/.sbss 段区(delta 与 .rdata 不同),换算必须走 `scripts/t05_pe.py` 的 `r2f/f2r/va2f`,不要自己算 delta。
- 布局细节见 `scratch/t01/t01e_vtables.json` 的 meta.va_maps。

### 3. RTTI 链(vtable → COL → 类名)

- 块内模式 A(内联):`call <alloc>` 后 `lea rax,[rip+X]; mov [rsi],rax` —— X 即 vtable VA。
- 块内模式 B(callee 构造):`call <init>` —— 类在 callee 里构造,要深追(司令官追到第 2 层已见命中;用 BFS,深度上限 4,防止循环)。
- vtable slot 前 8 字节 qword → COL VA。**本二进制的 COL 是相对形态**:
  - `sig dword == 1` @ COL+0
  - `tdRVA = dword @ COL+0xC`(**image-relative RVA,不是 64 位 VA** —— 这就是 t01e 当年 63 个只匹配上 4 个的原因)
  - `chdRVA = dword @ COL+0x10`
  - TD:C 字符串 @ TD+16,形如 `.?AV<NAME>@db@@`
- 用 `capstone`(CS_ARCH_X86, CS_MODE_64)+ `t05_pe` 反汇编与映射;参考 PoC 流程(要点如上,不另发脚本)。

### 4. 司令官已抽出的类名(你的第一件事是逐条复核,然后补缺)

内联直接命中(41 条,按 table_type):

```
0=AWARD, 2=CITY, 3=LEAGUE_BODY_CLUB, 4=RGB_COLOUR, 8=LANGUAGE, 18=DERBY,
19=REGION, 23=STAGE_NAME, 26=COMP_HISTORY_RECORD, 27=WEATHER, 30=STARTING_INJURY,
31=STARTING_CONFIDENCE, 34=STARTING_TEAM_CUP_HISTORY, 35=PLAYER_TYPE,
37=STARTING_TEAM_LEAGUE_HISTORY, 38=STARTING_BAN, 42=STARTING_RETIREMENT,
43=STARTING_MONTHLY_INSTALLMENT, 45=STARTING_RECORD, 46=STARTING_DRAFT_TRANSFER,
48=STARTING_RECORD(与45同 handler 0xf48ba6), 49=STARTING_PERSON_HISTORY,
50=STARTING_MLS_TRADED_SLOT, 51=STARTING_MLS_GENERAL_ALLOCATION_MONEY,
52=STARTING_PLAYER_HAPPINESS, 56=AGREEMENT, 57=FIXTURE_NAME,
58=STARTING_WEEKLY_WAGE_CONTRIBUTION, 59=STARTING_MEDIA_EXPECTATIONS,
60=STARTING_MLS_TARGETED_ALLOCATION_MONEY,
61=STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT,
62=STARTING_RESERVE_TEAM, 63=STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER,
64=STARTING_CLUB_STAFF_JOB_STATUS, 65=STARTING_NEWGEN_PARAMETER,
66=STARTING_CLUB_TRANSFER_PREFERENCE, 67=68=69=STARTING_NEWGEN_PARAMETER(同块),
70=STARTING_VISION_OBJECTIVE,
73=STARTING_ITALIAN_SERIE_A_NON_EU_PLAYER_SIGNED_FOR_RESTRICTED_SLOT
```

callee 追到(深度 2):32→STARTING_FUTURE_TRANSFER(callee VA 0x140f734b0)、39→STARTING_AVERAGE_POINTS(callee VA 0x140f730d0)。

尚缺(dedicated 但未命名):1, 5, 6, 7, 9, 10, 12, 14, 21, 22, 24, 25, 29, 33, 36, 41, 44, 47, 71, 72(以上 callee 深追);53/54/55 是 default/null-return(t01h E24 已解释,标 default)。

已知线索:t12 与 t33 的 A 锚(4CC)分别指向 award/club —— 它们的构造 callee 深追后应看到 AWARD/CLUB 家族;若看到别的,记 conflict,**不许推翻 A 锚**。t1=BASIC_PERSON(E24),t24=team,t25=comp(E20)。`scratch/t02/drbr_reference.json` 有 `.?AVDERBY@db@@` 旧引用可对照。

### 5. fm.exe 交叉(D:\tmp2b\fm24\input\fm.exe,只读,491MB)

- 同族封装(.sdata 大代码段 + .arch 371MB packed),274 个 `.?AV...@db@@` 类名(editor 只有 257),**COL 同为相对 RVA 形态**(司令官已验证 STARTING_BAN/CITY/COMP_HISTORY_RECORD 三条链)。
- 没有 `cmp ecx,0x49` dispatch,布局不同;交叉路线:类名字符串 → TD → COL → vtable → 全文件扫指向 vtable 的 8 字节 VA → 引用代码。
- 验收要求:每个 editor 抽出的类名在 fm.exe 确认 TD 存在且字符串一致;能拿到 vtable/引用交叉就记入,拿不到就写"TD-only"。

## 裁决规则

- 新增锚点类型 **D(RTTI 构造锚,L3)**:证据 = handler_off + vtable 赋值指令地址 + vtable VA + COL 文件偏移 + TD 类名 + independence(为什么该类名独属于该 table_type 的构造块)。与 A/B/C 并列;`resolved` 的组合要求仍按 AGENTS.md(不能只有 C)。
- 类名 → entity_tag:去 STARTING_ 前缀、与 schema XML tag 对齐(已验证 8 例);CLUB 家族→club、PERSON 家族→pers;拿不准标 candidate,列出证据与反证。
- 数量接近本身不是锚(t13 报告里 6 条拒绝理由继续有效);E42 值域法边界继续有效。
- 6 张 negative 裁决预期:26=COMP_HISTORY_RECORD、32=STARTING_FUTURE_TRANSFER、38=STARTING_BAN、39=STARTING_AVERAGE_POINTS 应能升 resolved(D 锚 + t15 的 C 类佐证可选);29/36 若深追仍无类名,保留 negative 并写清追到哪一层。**不许把 candidate 写成 resolved。**
- E56 的 12 张候选表(22,30,31,34,37,42,43,46,49,50,51,58)若 D 锚与 `scratch/cmd/stage2_candidate_adjudication.json` 一致,升级为 resolved 并注明双源;冲突则保守保留 candidate。已知三处精确吻合可直接引用:t30 E56"player伤病" ↔ STARTING_INJURY;t37 E56"club战绩" ↔ STARTING_TEAM_LEAGUE_HISTORY;t49 E56"person履历" ↔ STARTING_PERSON_HISTORY。注意 E59(23:55 撤回 t30/t49 循环论证交叉项):t30/t49 尚无独立数据侧确认,D 锚 + E56 A 级(df=1 唯一码)双源即可定案,不需要数据侧。

## 纪律

- **只写** `scratch/t14/out/`;只读调用 scripts/ 与 scratch/t05..t13。**允许新增** `scripts/t14_*.py`(带 --help/--selftest,退出码 0/1/2),不许改任何既有脚本。
- 不联网、不启动游戏本体/FM 编辑器(IDA 静态分析允许)。editor.exe/fm.exe 只读。
- **大文件分批落盘**:census.json/stage2_map.json 若超 50KB,按表分片(`census_<NN>.json`)+ 顶层索引;单次工具写盘 ≤400 行;exe 反汇编输出只许脚本抽样,不许大段贴进对话。
- 40 分钟内做不完就分批落盘,`"status":"partial_<限定词>"`,宁可 partial 不要烂尾。

## 交付(写 scratch/t14/out/)

1. `census.json` —— 0..73 全量:`{"table_type":N,"status":"dedicated|default","handler_off":"0x...","vtables":[{"inst_off":"0x...","vtable_va":"0x...","col_off":"0x...","class":"<NAME>","depth":k,"fm_cross":"td-only|vtable-confirmed|n/a"}],"entity_tag":"...","adjudication":"resolved|candidate|negative|default"}`
2. `stage2_map.json` —— 以 COVERAGE.json 的 59 张 server 表为骨架,每表 `{"table_type","archive","count","entity","status","evidence":[{"kind":"A|B|C|D","source":"..."}],"conflicts":[...]}`;top-level `"status"`。
3. `verify.py` —— 从 editor.exe 原字节 + 既有工件**独立复算**:每个 D 锚在 handler_off 反汇编出声明指令、COL 结构自洽(sig=1、TD 字符串、self 校验)、跳表 rel32 重解码一致、8 个已知实体交叉不矛盾;`--help`/`--selftest`。
4. `REPORT.md` —— 逐表结论 + 缺口 + 冲突清单;负结果原文保留。

## 验收线

1. 63 个 dedicated 类型全部拿到类名或明确 negative(含追到哪层)。
2. `stage2_map.json` 中 server 表 resolved ≥ 45/59。
3. 每个 D 锚可被 verify.py 从原始 exe 复算;8 个已知实体交叉零矛盾。
4. 2 张空表(52/57)标 empty 保留;负结果不删不改。
