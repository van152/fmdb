# t01-l 任务书:weat(table_27)行偏移 —— 直线型第二站,冲刺第二实体验收线

> 交给 pi gpt-6-luna max。BASIC_PERSON 因全局状态宽度选择器未闭合(t01k 负结果);census 判定 type 27 = WEATHER@db@@ 为 **straight-line**,且 client_db.dat 有 table_27 —— 这是当前最干净的 t01f 方法复制目标。
> 规则不变:只读输入、不启动游戏/编辑器/IDA、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 已知锚点(直接引用)

- t01h census type-27:RTTI `.?AVWEATHER@db@@`(RTTI 匹配,无候选歧义);type query 返回 27;alloc `mov edx,0x88`(0x88=136B);reader `0x158b970`(straight-line,27 宽度指令,首条 `0x158b9ae: mov r8d,1`,28 次流调用)
- 方法论模板:`scratch/t01/inbox/t01f/REPORT.md` §2;负对照:E20/E21/E24/E26 已证伪清单
- 行框架:client_db.dat 有 `client_db/table_27.dat`(t01i 目录全枚举);框架未知需恢复(参照 t01f:前导标记+定步,或 t01g:变长)
- 4CC 注意(t01k 新发现):**4CC 比较不一定用 ESI** —— person getter 用 `cmp edx,imm32`(81 fa)。扫描 getter 窗口时覆盖 81 f8..ff(全部寄存器)与 3d(eax)
- 码表:master.json `weather.xml#weat` 94 码

## 任务(按序)

1. **行框架**:解压 client_db.dat/table_27.dat,恢复 count、行起公式、stride(定长则行数×stride 封口 payload;变长则给模式)
2. **宽度累加**:沿 reader 0x158b970 的 27 条宽度指令记录顺序/宽度/分支;确认 census 的 straight-line 判定(有无 t01k 那种全局状态宽度选择器——若有,如实报告并处理)
3. **4CC 对齐**:定位 weather getter 窗口(全寄存器 cmp imm32),建 4CC→对象偏移→行偏移三元组
4. **验收线**:**≥10 个字段**行内偏移 L3 + 5 行抽验;或负结果:给出与 comp 模式的差异证据

## 交付

`scratch/t01/inbox/t01l/`:`output.json`(同 t01f 形状)、`REPORT.md` ≤110 行、`verify.py --selftest`(只读,全量行走查+负对照)。

## 纪律

深度优先一条线;45 分钟无进展记录现状换线;勿重做 t01f/g/h/i/j/k 已证部分;候选不写成结论。
