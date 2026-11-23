# t28 — nation client 变量尾:reader→wire 坐标绑定(子代理静态攻坚)

你是受指挥官委派的子代理。目标:**把 nation client reader 的变量尾(A/B/C/D 集合 + reader calls 24-39)绑定到行内 wire 坐标,晋级 client schema 的 49 个字段(21 direct + 28 nested list item)中可证实者**。t25 已把数据帧完全闭合,但 reader→wire 未对账;本任务补这一层,方法同 t24/t27(branch-aware symbolic cursor)。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;只读 editor.exe,PE 换算 scripts/t05_pe.py)
- D:\tmp2b\fm24-db\scratch\t27\out\replication.md(t27 子表方法模板,刚验收 33/33 绿)
- D:\tmp2b\fm24-db\scripts\t27_stadium_cursor.py、t24_club_cursor.py(branch-aware walker + 独立 verify 范例)
- D:\tmp2b\fm24-db\scratch\t25\out\cursor_nation.json(数据帧 + reader_evidence:reader_entry foff `0x103fac0`/VA `0x1410404c0`;prefix 10 transfers;A-count reader `0x1040728` movsx + helper `0x1040731` + count_test `0x1040736`;per_item helper;B/C/D count/item 线索)
- D:\tmp2b\fm24-db\scratch\t25\out\schema_split.json(client_fields=49:21 direct + 28 nested,各 type/list_item_fields;unmarked=392)
- D:\tmp2b\fm24-db\scratch\t25\out\fields_nation.json(已 7 个 L3 prefix 字段 + 数据画像)
- D:\tmp2b\fm24-db\scripts\t22_nation_capital.py(Ncpi getter 链方法;nation.xml 抽取)
- evidence/fm24/reports/editor_schema/master.json(nation.xml 字段类型;list_item_fields)

## 已知事实(勿重做)
- nation client member 251 行,变长;前缀 25B 固定 + A(i8 count@row+24,items@row+25,5B/item)+ B(i32 count,28B/item)+ C(i32 count,28B/item)+ D(i32 count,12B/item)+ identity。span=50+5A+28B+28C+12D。A/B/C/D 全表 492/214/63/162。
- prefix 7 字段已 L3(Nnam/Nsnm/TCnn/TCht/N3ln/Nnty/Ncti 等,见 fields_nation.json)。t01g 对 prefix 内 4B 候选的 negative 保留,不得翻案。
- arg8!=0 的 u16-count/4B-item reader **不归属 client/server**,本任务不绑定它。
- Ncpi 是 schema 注释字段(is_client_field 不可信),getter 链 t22 已做,不计入 client 分母。

## 任务
1. 从 reader_entry `0x103fac0` 建 CFG,定位 prefix 之后的变量尾 reader(calls 24-39 区间,A/B/C/D 的 count 读 + per-item helper + item 内 transfer)。逐分支分类 wire_data / runtime-external / dead / 未解,给证据。
2. 把 A/B/C/D 四个集合分别对到 schema 的 list 父字段(用 list_item_fields 的子字段类型/宽度与 item 内 transfer 宽度+object_off 互证;5B/28B/28B/12B 是强约束)。
3. item 内逐 transfer 给 row-frame 坐标(相对 item start)+ object_off + getter 4CC 链;跨 251 行全表数据画像验证(enum 值域/integer min-max/date 分布/bool)。
4. 晋级标准同 t27:getter 4CC + 行坐标 + 全表 schema 规则一致 → L3;仅部分证据 → candidate,不晋级。21 direct 中未晋级的与 28 nested 分别记账。
5. 独立 verify.py(不 import builder):重读归档字节 + 静态字节/VA + 全表画像 + 抽样;--help/--selftest;退出码 0/1/2。builder scripts/t28_nation_tail.py 同规范。

## 边界
- 只 nation client;不碰 server table_10;不绑定 arg8!=0 路径;392 unmarked 不强行归属。
- 候选不写结论;negative 原样保留;L4=0。
- 若变量尾 reader 跨函数/helper 过深无法在预算内闭合,诚实 partial + 已绑定子集 + 剩余清单,不硬凑。

## 交付 scratch/t28/out/
- cursor_nation_tail.json(CFG + 分支分类 + A/B/C/D→list 父绑定 + item transfer 坐标)
- fields_nation_client.json(49 字段台账:row_offset/width/object_off/getter 链/数据画像/grade;direct vs nested)
- instructions.part*.json、branches.part*.json(分片字节证据)
- verify.py、REPORT.md
- scripts/t28_nation_tail.py(builder)
- 完成后写 scratch/t28/out/DONE.md(一句话状态 + 晋级数 + 关键结论)

Python:`py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data。只读外部;只写 scratch/t28/ 与 scripts/t28_*.py。