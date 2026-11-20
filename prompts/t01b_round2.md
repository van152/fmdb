# t01-b 第二轮任务书(续会话)

> 继续第一轮的成果(`scratch/t01/inbox/t01b/output.json`)。本轮产物写到 `scratch/t01/inbox/t01b/round2/`。
> 同样规则:只读、不启动程序、不 pip install、`py -V:3.12 -I`、claim 带字节证据。

## 第一轮验收结论(指挥官,三项抽验全过)

helperA 角色、注册块字节、setter→0xfe72b0 调用、证据 SHA-256 全部确认。你的"证伪 4CC 在描述符槽内"已入账(E14),E5 措辞已收窄。

## 本轮三个目标(按优先级)

### 1. 56B 描述符槽的剩余成员(第一轮 open_question)
槽 +0 是 vtable(已证)。用**跨实体对比**推进:非 comp 的注册函数已在全景扫描里(`scratch/t01/t01a_editor_sweep.json`,175 簇,如 club 家族 0xe82b4c/0xe89c24)。对比 comp 与另一实体的 switch handler(`add rax,N` 的 N 值集合)和注册块,推断槽内布局:vtable 之后是什么(类型?名字缓存?值区?)。可用 direct 型 case 的 N 分布(24/40/104)与槽步进 56 的关系做约束。

### 2. 描述符数组构造器
新线索(LEDGER E11):
- comp 注册函数起点 off **0xebf040**(RVA 0xebfa40),序言 `call helperB; add rax,0x38` → 槽基址来自 helperB
- .rdata(RVA 0x187dcb0 / off 0x187d2b0)有一张 **44 项虚表**,slot 6 = comp 注册函数 VA 0x140ebfa40 —— 实体定义类接口
- 墙:helperB(0x14083d4f0)是 thunk(jmp 0x377e370,进 .reloc 加壳区);虚表的 lea 引用在明文区未命中
思路:绕开 helperB,从**注册容器的消费端**反推——push 进容器的 {descriptor, 4CC} 记录最终被谁读取(helperA 的容器在全局,找持有它的单例与读取者);或找 0x187dcb0 虚表在 .reloc 区的引用(t01-a 证实 .reloc 有明文 dense code,映射 VA=off+0x16B600)。

### 3. 0xfe72b0 公共 helper 的语义(新增线索)
ccti setter 带 'cont'(container/reference?)类型标签转发 0xfe72b0。枚举 switch JSON(`scratch/t01/t01b_switch_cases.json`)里所有 setter,统计转发的类型标签集合('cont' 之外还有什么:整数/字符串/日期标签?),反推标签↔schema wire type 映射。这对后面 .dat 行编码直接有用。

## 交付
- `round2/output.json`:成员布局(更新版)、构造器线索、类型标签清单
- `round2/REPORT.md` ≤80 行
- 完成后打印交付清单。不确定的写 open_questions,不猜。
