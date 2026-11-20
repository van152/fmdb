# t01-i 任务书:pers 核心行(table_1 / BASIC_PERSON)行偏移 —— t01f 方法第三站

> 交给 pi gpt-6-luna max。t01f(comp,直线型,18 字段)→ t01g(nation,变长型,负结果)→ t01h(全普查,mode 46/7/7/14)。现在做排序后的第一名:**type 1 = BASIC_PERSON,straight-line,reader 有 27 条宽度指令**。
> 规则不变:只读输入、不启动游戏/编辑器/IDA、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 已知锚点(直接引用,勿重复)

- t01h census type-1 项(`scratch/t01/inbox/t01h/output.json`):handler `0xf48d12` → alloc `0x70`(112B,wrapper `mov edx,0x70`)→ 构造类 `BASIC_PERSON@db@@`(RTTI 0x1aac700,vptr 0x187b328);slot7 query 返回 1;reader `0xe4f370`(straight-line,27 宽度指令,首条 `0xe4f393: 41 b8 01 00 00 00`)
- 方法论模板:`scratch/t01/inbox/t01f/REPORT.md` §2(宽度累加 = 行偏移;对象成员由 XML switch 分发对齐)
- .dat 侧框架:client_db.dat/table_25 = 13+i*127 前导标记 + 14+i*127 行起(t01f);table_10 用 _entries/_decompress_entry 取 payload(t01g);table_1 的行框架**未知,你要先恢复**(旧库未解码 table_1)
- 码表:master.json `person.xml#pers` 271 码;`field_codes` 有每码 schema 名
- 已证伪/勿重复:行偏移不在描述符槽(E20);switch 区是实体特异的(E21)—— person 的 getter 区要自己定位(参照 t01g 在 0x1041930..0x1045300 找 nation getter 的办法)

## 任务

1. **行框架恢复**:client_db.dat 中找 table_1 条目(旧库 `_entries`);从 payload 头部+行结构推 stride 与行起(t01f 是标记+定步;若 BASIC_PERSON 定长,行数 × stride 应封口 payload)。行数从 version/framing 读(旧库解码器有先例)。
2. **宽度累加**:沿 reader 0xe4f370 的 27 条宽度指令记录顺序/宽度/分支,得出字段顺序与对象偏移(`[rbx+disp]`/`lea reg,[rbx+disp]`);与 payload 行字节逐字段对照。
3. **4CC 对齐**:person 的 getter 区(先扫,参照 t01g),把 4CC → 对象偏移 → 行偏移三元组建全;27 条宽度指令 ≈ 27 个字段,尽量全对齐。
4. **验证**:duni/rdui 型身份块(参照 comp 12B 与 nation 的模式,不预设);抽 5+ 行对照原始字节;行序号/重复 ID 块模式若有,复现之。

## 验收判据

- table_1 行 **≥10 个字段**的行内偏移映射(L3,访问+流宽度指令字节证据)+ 行框架(行起公式/stride)+ 5 行抽验;
- 或负结果:table_1 并非 BASIC_PERSON 行(如另属其他类),指出真实对应并给已证明部分。

## 交付

`scratch/t01/inbox/t01i/`:`output.json`(同 t01f/t01g 形状)、`REPORT.md` ≤110 行、`verify.py --selftest`(只读,含负对照)。

## 纪律

深度优先一条线;45 分钟无进展记录现状换线;勿重做 t01f/g/h 已证部分(引用即可)。
