# t01-k 任务书:BASIC_PERSON 类变长行字段映射 —— 第二实体验收线冲刺

> 交给 pi gpt-6-luna max。t01j 已解码 person 行仓库框架(658,011 行,类变长 83/34/22B,身份块+9B 尾全封口);你的任务是给 BASIC_PERSON 行做出 **≥10 个字段的行内偏移映射**,达成第二实体验收线(与 t01f comp 同级)。
> 规则不变:只读输入、不启动游戏/编辑器/IDA、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 已知锚点(直接引用,勿重复)

- 行框架(t01j/E25):payload 头 u32 count@0;行头 `0x11|class_id`;类长 1/2/3=83B、4=34B、5=22B;类计数 1:166064/2:476158/3:4757/4:9839/5:1193;全行末 12B = ordinal|ID|ID;9B 尾。样本身份块(t01j REPORT §行框架)
- 静态(reader `0xe4f370`,t01h/t01i/t01j 已核):`0xe4f42e: 3c 04`(cmp al,4)、`0xe4f430: 75 4c`;宽度指令 27 条(luna Capstone 清单:0xe4f393:1、0xe4f43c:2、0xe4f468:2、0xe4f4f6:8、0xe4f4fe:4、0xe4f542:8、0xe4f54a:4、0xe4f57f:8、0xe4f587:4、0xe4f5ba:4、0xe4f5da:4、0xe4f5fa..0xe4f6fa 十条 2B、0xe4f71a/3a/5a:1、helper 3dc0241:8、3dc027b:12、3c6e121:8、3c6e129:4)
- 对象侧:alloc 0x70(112B,小类!);RTTI BASIC_PERSON@db@@ @0x1aac700;vptr 0x187b328;type query 返回 1
- 码表:master.json `person.xml#pers` 271 码;person getter 区要自己定位(参照 t01g nation getter 窗口法)
- 方法论:t01f REPORT §2(宽度累加=行偏移);负对照 E20/E21/E24 已证伪清单勿重复

## 任务(按序)

1. **class-4(34B)先行**:9,839 行,结构最短。reader class-4 分支已闭合 1+2+2B;把该分支全部指令走完,得 class-4 行字段顺序与偏移;对照 payload 类 4 样本逐字节验证。
2. **class-1/2/3(83B)主体**:476,158+166,064+4,757 行。走 reader 非 4 分支(83-12-2=69B 业务区),同样指令级累加;与样本行逐字节对照。
3. **4CC 对齐**:定位 person getter 区(扫 `cmp esi,imm32` 窗口,imm 逆向 = master person 码),建 4CC→对象偏移→行偏移三元组;对象小(0x70),getter 成员访问 `[rbx+disp]` 应密集。
4. **验收线**:≥10 个字段(任一类)行内偏移 L3 + 5 行抽验;或负结果:reader 与行的对应在类分支外还有分派变体,给出已闭合部分与差异证据。

## 交付

`scratch/t01/inbox/t01k/`:`output.json`(同 t01f 形状,row_offset_map 按类分)、`REPORT.md` ≤110 行、`verify.py --selftest`(只读,全量行走查+负对照)。

## 纪律

深度优先;45 分钟无进展记录现状换线;候选不写成结论;勿重做 t01j 框架部分(引用即可)。
