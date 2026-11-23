# t01-m 任务书:stad(table_21)行偏移 —— 直线型第三站,带旧库锚交叉验证

> 交给 pi gpt-6-luna max。t01l 已达第二实体验收线(weat 89 字段);type 21 = STADIUM@db@@ 是下一个干净目标:**census 判定 straight-line,client_db.dat 有 table_21,且旧库已独立解码其行结构** —— 你的结果可与旧库 L1 锚逐字段交叉验证,证据等级最高。
> 规则不变:只读输入、不启动游戏本体/FM 编辑器(IDA 静态分析允许)、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 已知锚点(直接引用,勿重复)

- t01h census type-21:RTTI `.?AVSTADIUM@db@@`(精确匹配);type query 返回 21;alloc `mov edx,0xb0`(0xb0=176B);reader `0x1183f30`(straight-line,**77 条宽度指令**,首条 `0x1183f65: mov r8d,4`)
- **旧库 L1 锚**(`evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md`,只读引用):table_21 client 行 stride 38、server stride 181;client `rdui@+25`(注意 E20 勘误:+25 实为行序号,非原生 rdui)、`duni@+29`(重复 u32)、`Scti@+3`(城市引用,值=table_2 的 rdui);四组城市锚(Anfield/Liverpool 等)与 48,413/48,413 引用合法;server row[143:181] ≡ client 38B 逐字节
- 方法论:t01f REPORT §2;t01l 的修正经验(模式描述要区分"字面直线"与"固定循环",循环也无妨,只要确定性);t01k 教训(getter 扫描用全寄存器 cmp imm32:81 f8..ff + 3d)
- 码表:master.json `stadium.xml#stad` 60 码

## 任务(按序)

1. **行框架**:解压 client_db.dat/table_21.dat,恢复 count、行起、stride;对照旧库 stride 38(L1)—— 一致即双源互证
2. **宽度累加**:沿 reader 0x1183f30 的 77 条宽度指令走查;77 条宽度 ≈ client 38B 装不下 —— **先解释宽度指令总数与 client 行宽的关系**(部分字段只在 server 行/扩展区传输?参照 t01f comp 的 client/server 模式与 t01g 的参数分支)
3. **4CC 对齐**:getter 窗口全寄存器扫描;建 4CC→对象偏移→行偏移三元组(client 行内 + server 扩展区分别给出)
4. **旧库交叉**:Scti@+3、行序号@+25、duni@+29 逐一用 reader 链印证或修正;四组城市锚抽验
5. **验收线**:**≥10 个字段**行内偏移 L3(与旧库 L1 一致或修正有据)+ 5 行抽验;或负结果给差异证据

## 交付

`scratch/t01/inbox/t01m/`:`output.json`(同 t01f 形状)、`REPORT.md` ≤110 行、`verify.py --selftest`(只读,全量行走查+旧库锚交叉+负对照)。

## 纪律

深度优先一条线;45 分钟无进展记录现状换线;候选不写成结论;勿重做已证部分。
