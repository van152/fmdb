# t01-b 任务书:editor.exe 字段描述符链(串行深链,长会话)

> 交给 pi gpt-6-luna max。你是一个长会话逆向代理,这是本项目当前最重要的单点任务。
> 全部工作只读,不启动游戏本体/FM 编辑器(IDA 静态分析允许),不 pip install。Python 固定 `py -V:3.12 -I`。

## ⚡ 指挥官夜间进展(2026-11-18,先读这段,避免重复劳动)

你接手时以下工作**已完成**,见 `scratch/t01/LEDGER.json` E5/E6/E7 与 `scratch/t01/t01b_switch_cases.json`:

1. ✅ helperA(RVA 0x83b5f0)已解码 = `std::vector<32B>::push_back`;注册块语义 = 把 {属性对象*, 4CC} 推入全局注册表;`add rax,0x38` 遍历实体属性描述符数组。
2. ✅ XML→对象字段分发 switch 已定位并粗提取(0xec0000..0xec6000,105 case,54 个 comp 匹配;direct 模式偏移:cext→obj+24,dbty/crep→+40,cmnl/cmxl→+104 等)。
3. ✅ PE 换算:RVA = fileoff + 0xA00(.rdata 内);VA = 0x140000000 + RVA。
4. ⚠️ helperB(RVA 0x83d4f0)是 thunk(jmp 进 .reloc 加壳区)——静态墙,别浪费会话去解壳。

**你的任务相应修订**(原第 1-3 步作废,按此执行):

### 新第 1 步:属性描述符数组构造器(最高优先)
0x38 步进数组里有每个字段的 {类型, 行内偏移?, 序列化器?}。找它的构造/初始化函数:xref 注册函数的调用者;或在 .rdata 搜 0x38 步进数组的基址分配。产出 56B 布局表(带字节证据)。

### 新第 2 步:setter 内部偏移
switch 的 delegate 型 case 把偏移藏在 setter 里(已知:ccti→0xfe7860、cnti→0xfcc110,switch JSON 里有完整 setter 清单)。反汇编这些 setter,找 `add rax,N` / `mov [rax+N]` 形态,提取字段→运行时偏移。已知 direct 案例(cext→+24 等)用于交叉验证 setter 结果。

### 新第 3 步:运行时偏移 → .dat 行偏移的桥
运行时布局 ≠ 行布局(例证:cext 运行时 +24,但行内旧候选被证伪)。找 .dat 行加载/写回链:编辑器打开数据库时把行读进对象(找与 switch 同区域 0xec0xxx-0xecbxxx 的读侧 switch),或找 save/pack 路径。判据:能解释 comp 行 +52=ccti/+56=cnti/+64=cpcm/+114=rdui/+118=duni 的已知锚点。

### 交叉验证锚点(不变)
六大洲 ccti∈0..5、cnti England=139/China PR=55、cpcm parent row=352;client comp 行 127B;详见 DB_TABLES_BIG.md table_25 节。


## 背景(自包含,无外部上下文)

FM24《Football Manager 2024》的安装数据库是 `.dat` 文件(自定义容器+Zstd,无加密),外层已完全解通。剩余瓶颈:**字段语义**——把编辑器 schema 的字段代码(4 字符 ASCII,如 `ccti`=continent reference)映射到数据库行内的字节偏移。

已确认 editor.exe 内存在字段码体系(指挥官探针,证据等级 L3-static):

1. **comp 实体属性注册函数**(文件偏移 0xebf060..0xebf200):
   ```asm
   c7 45 f0 <imm32>        ; imm32 = 字段码 ASCII 反序(如 'cnam'→6d 61 6e 63)
   48 89 45 e8             ; mov [rbp-0x18], rax
   48 8d 7d e8             ; lea rdi, [rbp-0x18]
   48 89 f1                ; mov rcx, rsi
   48 89 fa                ; mov rdx, rdi
   e8 -> 0x83abf0          ; helperA(文件偏移,VA=0x14083b5f0)
   48 8b 4d e8             ; mov rcx, [rbp-0x18]
   48 8b 01                ; mov rax, [rcx]        ; 取 vtable
   48 89 fa                ; mov rdx, rdi
   ff 50 10                ; call qword [rax+0x10] ; 虚调用
   e8 -> 0x83caf0          ; helperB(VA=0x14083d4f0)
   48 83 c0 38             ; add rax, 0x38         ; 属性对象步进 56 字节
   ```
   已见字段序列:PLgn→cnam→cnsm→cl3n→cnti→ccti→cpcm→crep→cext(与 comp.xml schema 字段顺序一致)。
2. **第二簇**:0xec0000..0xecb000 散布 ccti/cpcm/cext/dbty/cnam 命中,形态不同,疑似序列化/分发 switch。
3. **PE 换算**:image_base=0x140000000;.rdata 段内 `VA = fileoff + 0xA00`。二进制疑似加壳(.code 段 raw 仅 0x200),但上述区域字节解码为一致 x86-64 代码。

**主假设 H1**:注册函数按 schema 顺序把每个字段登记为 56 字节属性对象;对象内含类型/序列化槽位/行内偏移。**解码对象布局 = 解开全部 32 实体的字段→偏移映射**。若证伪,如实报告并转向第二簇。

## 你的任务(按序推进,每步先留证再前进)

### 第 1 步:解码 helperA(0x14083b5f0 / off 0x83abf0)
读 editor.exe off 0x83abf0 起约 0x200 字节,手工解码 x86-64(可用 capstone,若 `py -V:3.12 -I -c "import capstone"` 可用;不行就手工,本区域指令形态简单)。回答:
- 参数(rcx=属性对象指针?rdx=&4CC?)如何被使用;
- 4CC 被写到属性对象哪个偏移;
- 函数是否还读/写对象其它成员(记录每个 `[reg+disp]` 访问)。

### 第 2 步:属性对象 56B 布局
- 找属性对象**构造器**:向上找对注册函数的调用者(xref:在 .rdata 全文件搜 `e8` rel32 目标=注册函数 off;也搜 VA 形式的 4 字节相对引用),或找 `48 83 c0 38` 数组起点分配处(搜对象数组基址的 lea);
- 输出布局表:每成员 {偏移, 宽度, 推断用途, 证据字节};至少定位 4CC 成员和"类型/偏移/序列化器"候选成员;
- 用第二实体交叉验证:任选另一实体的注册函数(如 stadium/city),其对象步进与成员访问偏移应一致。

### 第 3 步:连接 .dat 行序列化
- 解码第二簇(0xec0000..0xecb000)中的 1-2 个样本点(如 ccti@0xec2009 前后 0x80 字节):判断是 cmp-4CC switch(读侧)还是静态表;
- 若是 switch:记录每个 case 对象+offset 的计算式(`mov eax,[obj+X]` / `add` / `lea`),这就是**字段→行内偏移**的直接证据;
- 对照:comp 的 packed 区(数据库 client 行 127B,+0..51 与 +68..113 未分配)——若 case 给出 `ccti@+52`、`cnti@+56`、`cpcm@+64`(已知 L2 锚点),则方法自证;继续列出新字段槽位。

### 第 4 步:写回
- 产出 `output.json`(结构见下)与 `REPORT.md`(≤150 行,含每步证据);
- 已知 L2 锚点用于交叉验证:六大洲 ccti∈0..5、cnti England=139/China PR=55、cpcm parent row=352、rdui@+114、duni@+118(来自 D:\tmp2b\fm24-db\evidence\fm24\reports\dbdat_decode\DB_TABLES_BIG.md 的 table_25 节)。

## 输入路径(全部只读)
- `D:\tmp2b\fm24\input\editor.exe`(二进制)
- `D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json`(3009 字段码、32 实体)
- `D:\tmp2b\fm24-db\evidence\fm24\reports\DBDAT_FORMAT.md`(表格式)
- `D:\tmp2b\fm24-db\evidence\fm24\reports\dbdat_decode\DB_TABLES_BIG.md`(table_25 已知锚点)
- `D:\tmp2b\fm24-db\evidence\fm24\reports\editor_gen\PROPERTY_MAP.md`(database_table_type↔entity 先例)
- `D:\tmp2b\fm24-db\scratch\t01\LEDGER.json`(指挥官账本,追加你的发现时沿用其格式)
- `D:\tmp2b\fm24-db\scratch\t01\probe_pe.py`(PE 换算,只读运行)

## 输出契约(写到 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01b\`)
- `output.json`:
  ```json
  {
    "helperA": {"va": "...", "role": "...", "arg_layout": "...", "evidence": ["off 0x...: bytes ..."]},
    "prop_object_layout": {"stride": 56, "members": [{"offset": 0, "width": 8, "role": "...", "evidence": "..."}]},
    "serialization_link": {"region": "0xec...", "kind": "switch|table", "field_slots": [{"code": "ccti", "row_offset": 52, "evidence": "off 0x..."}]},
    "comp_new_slots": [{"code": "...", "row_offset": null, "level": "L3", "evidence": "..."}],
    "open_questions": ["..."],
    "falsified": [{"claim": "...", "evidence": "..."}]
  }
  ```
- `REPORT.md`:步骤叙事+证据,≤150 行
- **每个 claim 必须带 file offset + 原始字节**;没有字节证据的写进 open_questions,不进结论。

## 验收线(本轮)
- helperA 角色与参数布局(带证据)= 必达;
- 属性对象布局(至少 4CC 成员 + 2 个候选成员)= 必达;
- 序列化连接 = 尽力,失败则明确记录走到哪一步、卡在哪个字节。

## 禁止
- 修改任何输入文件;启动游戏/编辑器/IDA;pip install;把推测写成结论;删除或改写 LEDGER 已有条目(只追加)。
