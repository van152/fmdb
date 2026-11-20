# t24 任务书:club 全行 cursor 闭合(最高难度,司令官点名攻坚)

先读 `AGENTS.md`。这是 t19→t21→t21b 的接力终点战:把 CLUB 混合 reader 的完整行 cursor 闭合,让 433 个 club schema 字段尽可能多地拿到行偏移 L3 定名。

## 已确认基线(不要重复验证,直接引用)

- **行框架已封口**(t19/t21):client table_3 共 84,259 行 = 84,256 标准行 + 3 compact 行(ordinal 69706/69707/69708);`row_length = 50 + N + M`;row end = footer = `0x69c66a`。全量走查见 `scratch/t21/out/audit.json`,独立复核脚本 `scripts/t21_club_cursor.py`。
- **CFG 已建好**(t21b):CLUB reader `0xe5a7a0` 可达 1412 指令/268 基本块/41 stream transfer/167 条件分支/35 backedge;LEAGUE_BODY_CLUB thunk `0x157cff0`→body `0x43beba0`(68 指令/5 块/2 transfer/count-loop)。全部证据在 `scratch/t21/out/control_flow.json`,生成器 `scripts/t21b_control_flow.py`。
- **Cccn@row+8 已降级**(E60):row+0==row+8 在 55,868/84,259 行成立,不得作为锚点或已名字段使用。
- **行坐标台账**:t18 `scratch/t18/out/fields_club*.json` + `bridge.json`(golden 113/113 已过,但 club 不在 golden 三实体内);t19 `scratch/t19/out/cursor_club.json` + `fields_club*.json`(partial)。
- **schema 目录**:`reports/t12_field_names.json`(club 433 字段,含 4CC getter code)。
- **历史手法**:nation 四段计数算法(t02g2,`scratch/t02/inbox/nati/OUTBOX/verify.py`)证明"读出的计数/宽度驱动后续分支"这条路在变长行上可行;t18 的 cursor 步骤累加法(46 步粒度,含版本字节与条件块)是行侧定名的正典方法。

## 唯一目标

构建**可执行的分支感知行 cursor**:对每一行,用已读出的字节值(计数、宽度、标志位)决定 CFG 中哪些条件分支被走,逐 transfer 消费字节,做到:

1. **全量闭合**:84,259 行每行消费恰好 `row_length` 字节,footer 精确封口;3 个 compact 行的 body 文法单独解出。
2. **class 判定字节化**:CLUB(5B class-split)vs LEAGUE_BODY_CLUB(4B)的每行选择必须由行内字节驱动并全量验证;**禁止**用连续 ordinal split(69705 附近)当 discriminator——t21 已明确这是数据现象不是证据。若找不到字节级 selector,如实输出 negative 并给出两轨各自能覆盖的行集。
3. **字段定名**:每个消费步骤绑定 CFG transfer site(VA+原始 bytes+file offset);凡 4CC getter 证据链(schema 名→object_off→cursor 行偏移)闭合的字段晋级 L3,写入台账。目标是把 club 命名数从个位数大幅提升;不设"全解"验收线,但**每一步都要有字节证据**。
4. **子对象下沉边界**:E39/E40 已确认 672 字段不在主行在子表;主行 cursor 闭合后,明确列出哪些 schema 字段属于子表(给引用槽位),不要在主行里硬找。

## 方法和纪律

- 只读 `<OLD_REPO>\input\editor.exe`(SHA-256 须对照 `evidence/fm24/reports/qa/IDA_PROVENANCE.md`);本地数据 `FM24_DB_DIR=<WORKSPACE>/scratch/data`;PE 换算用 `scripts/t05_pe.py`,禁止固定 delta。
- 建议路径:以 `control_flow.json` 的 CFG 为底,写符号化 walker——把 stream read 建模为"消费 width 字节→产出值→值喂给后续分支条件"。对 167 个条件分支逐个归类:数据驱动(可执行)/ 运行时外部状态(不可静态判定,须标出并给数据侧反推)/ 死代码。
- 数据侧反推允许且鼓励:84,259 行全量字节在手,分支假设可以用全表分布验证(如 nation 四段计数那样),但**假设→全量验证→晋级**三步缺一不可;候选不写成结论。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;只写 `scratch/t24/out/` 与 `scripts/t24_*.py`;不覆盖 t19/t21/t21b 既有产物。
- 新脚本 `--help`/`--selftest`,退出码 0/1/2;单次打印 ≤400 行;大 JSON 分片(`*.partNNN.json`)。
- 状态词:`complete_*` / `partial_*` / `negative_*`(带限定词);负结果原文保留。
- 卡壳就把已有进度落盘 partial,不要空转。

## 交付

1. `scratch/t24/out/cursor.json`:每行消费轨迹的机读摘要(可按行分片)+ 分支归类表 + class selector 证据或 negative。
2. `scratch/t24/out/fields_club.json`(可分片):晋级字段台账,逐字段 {name, code, row_offset, width, object_off, VA, bytes, grade, 验证统计}。
3. `scratch/t24/out/verify.py`:独立复算全量闭合 + 抽样字段字节重读;`--selftest` 须过。
4. `scratch/t24/out/REPORT.md`:结论、证据等级、命名增量统计、未闭合项、负结果。

完成后先跑自己的 verify,再跑 `py -V:3.12 -I scripts/t01_anchors.py`(7/7 锚点回归)确认无矛盾。打印交付清单。