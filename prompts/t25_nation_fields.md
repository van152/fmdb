# t25 任务书:nation client 字段放量(441 schema → 行偏移台账)

先读 `AGENTS.md`。nation client 行框架已三方对账闭合(t23),现在把 schema 字段批量映射到行内偏移——这是阶段三(批量字段映射)在 nation 上的主力推进。

## 已确认基线(直接引用,不要重复证明)

- **行框架 closed**(t02g2/t23):client table_10 共 251 行,`14 + 24710 + 8 = 24732`,四段计数 A/B/C/D 总量 `[492,214,63,162]`、单行上限 `[7,40,21,2]`;payload SHA-256 `7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34`。独立 verifier:`scratch/t02/inbox/nati/OUTBOX/verify.py`(已过)。对账总纲:`scratch/t23/out/nation_status.json`。
- **前缀 25B 已解**(t01g/t19):widths `[1,4,4,4,4,1,1,4,1,1]`;已名字段含 Ngct@row+0、Ncti@row+1、Nrgi@row+5 等 7 个(t19 `scratch/t19/out/fields_nation*.json`)+ **Ncpi@row+9**(t22,L3,指向 city 零基行号,`reports/t22_nation_capital.json` 含完整 VA/bytes 证据与 nation.xml 提取方法)。
- **reader 静态区域**(t22 已复核):client nation 普通行读取在 `0x141040fb4` 起(1+4+4 连续读),getter 分支区 `0x141042ac5`..`0x141043bc4`(Ncac/Ncpi/NcpR 等,均取 NATION+0xe8 流对象)。t01g 的 prefix-only 负结果原文保留,不要推翻其"未宣称全行"的边界。
- **schema**:`reports/t12_field_names.json` 的 nation 441 字段;原始 XML 在 `comp editor.fmf` 的 `comp editor/format/database/nation.xml`(t22 脚本 `scripts/t22_nation_capital.py` 有解包先例)。**XML 记录带 `is_client_field` 标志**——先按标志把 441 字段分成 client / server-only / 未知三类,只映射 client 类;server-only 字段不在 client 行里,不要硬找。
- **行坐标正典**:t18 `scratch/t18/out/fields_nati*.json` + `bridge.json`(步骤累加法);t19 `scratch/t19/out/cursor_nation.json`(partial:tail 与 loops 未闭合——这正是你要补的)。

## 唯一目标

1. **分类先行**:441 字段按 is_client_field 分类,输出三类清单(机读)。client 字段数才是本任务的分母。
2. **补全 cursor**:在 25B 前缀之后,用四段计数(A/B/C/D)驱动变长段的分支感知 walk,把 251 行每行消费到 footer;每步绑定 reader 指令(VA+bytes+file offset,PE 换算用 `scripts/t05_pe.py`)。t19 未闭合的 tail/loops 是主攻点。
3. **字段晋级**:4CC getter 证据链(schema 名→object_off→行偏移)闭合 + 251 行全量数据侧 sanity(值域/哨兵/引用落界)→ L3 晋级。引用类字段用已知连接验证:Ncpi→city 行号(t22 范式)、语言表 8_9 国家名、六大洲 0..5、England duni=139、China PR duni=55、Israel duni=775=row 149。
4. **诚实计量**:交付时报告 client 字段命名率(已名/client 总数),未闭合项逐条列出;不设全解验收线。

## 边界(不许跨)

- **server table_10 文法不在本任务**(开放问题,另派);不得把 client 公式套到 server。
- arg8!=0 的备用 reader 路径角色未定(t23),不要给它赋义。
- Ncpi 的 XML 记录在注释里——字段名可信,UI 可编辑性不可推断;其他注释字段同理,定名可以、行为断言不行。
- 不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:;只写 `scratch/t25/out/` 与 `scripts/t25_*.py`;不覆盖既有产物。

## 纪律

- 新脚本 `--help`/`--selftest`,退出码 0/1/2;单次打印 ≤400 行;大 JSON 分片。
- 状态词 `complete_*`/`partial_*`/`negative_*` 带限定词;候选不写成结论;负结果保留;卡壳落盘 partial。
- 数据侧假设必须全量(251 行)验证后才晋级。

## 交付

1. `scratch/t25/out/schema_split.json`:441 字段三分类。
2. `scratch/t25/out/cursor_nation.json`:全量行消费轨迹摘要 + 每步指令证据。
3. `scratch/t25/out/fields_nation.json`(可分片):晋级台账 {name, code, row_offset, width, object_off, VA, bytes, grade, 验证统计}。
4. `scratch/t25/out/verify.py` + `REPORT.md`:独立复算闭合 + 命名率 + 未闭合项。

完成后跑自己的 verify 与 `py -V:3.12 -I scripts/t01_anchors.py`(7/7)。打印交付清单。