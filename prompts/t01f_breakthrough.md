# t01-f 突破任务书:描述符槽布局 + .dat 行偏移之桥(杀手锏,单发)

> 交给 pi gpt-6.2-sol max。额度有限:**这是一次性投入,请在本会话内尽力推进到最深处**,产物完整落盘。
> 规则不变:只读输入、不启动游戏本体/FM 编辑器(IDA 静态分析允许)、不 pip install、Python `py -V:3.12 -I`、每个 claim 带 file offset + 字节证据。

## 你要解决的核心问题(项目当前唯一主线缺口)

FM24 编辑器(editor.exe)的运行时对象与游戏数据库 .dat 行之间的**字段偏移桥**:

- 已知:运行时属性槽步进 0x38(56B),槽 +0 = vtable;XML→对象 switch 已提取(121 case / 67 comp 码)
- 已知:.dat comp 行 127B,行内偏移 ccti@+52 / cnti@+56 / cpcm@+64 / rdui@+114 / duni@+118(L2 锚点)
- **未知:行偏移存放在哪里、如何被读写链消费。两侧搜索(editor.exe / fm.exe)都证明行解析器无硬编码偏移 → 架构是 schema 驱动的,行偏移就在描述符槽(或其构造器写入的结构)里**
- 验收判据:给出 comp 行 ≥10 个字段的行内偏移映射,且与上述 5 个已知锚点一致;或证伪"行偏移在槽内"假设并给出行偏移的真实存放处

## 全部既有证据(先读账本与工件,不要重复扫描)

必读(按序):
1. `D:\tmp2b\fm24-db\scratch\t01\LEDGER.json` —— E1-E15 全部条目,含关键偏移与已证伪清单
2. `D:\tmp2b\fm24-db\scratch\t01\t01a_editor_sweep.json` —— editor.exe 全景:175 簇、103 switch、2954 hit、逐实体码覆盖(.reloc 区映射 VA=off+0x16B600)
3. `D:\tmp2b\fm24-db\scratch\t01\t01b_switch_cases.json` —— comp switch 121 case 清单
4. `D:\tmp2b\fm24-db\scratch\t01\inbox\t01b\output.json` + `REPORT.md` —— luna 第一轮:helperA=registry 插入、descriptor+0=vtable、'cont' 类型标签、ccti setter→0xfe72b0
5. `D:\tmp2b\fm24-db\scratch\t01\inbox\t01a2\fm_sweep.json` —— fm.exe(491MB)全景:50,071 命中在 .sdata,comp 注册块与 editor 逐字节相同(fm off 36605107 ≡ editor off 15462499)
6. `D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json` —— 32 实体/2144 码
7. `D:\tmp2b\fm24-db\evidence\fm24\reports\dbdat_decode\DB_TABLES_BIG.md` —— table_25 行结构与锚点
8. `D:\tmp2b\fm24-db\scratch\t01\t01e_vtables.json` —— 虚表↔实体映射 12/32(H3 半证实,槽位数随实体变 43/68/89/243)
9. `D:\tmp2b\fm24-db\scratch\t01\inbox\t01b\round2\output.json` —— luna r2:0xfe72b0 标签普查(17 标签,122 引用口径)
10. `D:\tmp2b\fm24-db\scratch\t01\t01f_tag_codec_alignment.json` —— 标签↔codec 对齐:实体标签主轴贯通 .dat/XML 两侧(DBC 记录→工厂→对象→schema 分发;'cont' 为字段类型标签)

关键锚点速查:
- 注册函数:off 0xebf040(RVA 0xebfa40),序言 `call helperB; add rax,0x38`,slot1=PLgn→slot9=cext
- helperA:off 0x83abf0(vector<32B>::push_back 变体,容器 {begin,end,cap});helperB:off 0x83caf0 = thunk jmp 0x377e370(**墙,在 .reloc 加壳区**)
- 44 项虚表:off 0x187d2b0(RVA 0x187dcb0),slot6 = 注册函数 VA 0x140ebfa40(实体定义类接口假设 H3)
- 注册容器消费端未找;PE:.rdata VA=off+0xA00;.reloc VA=off+0x16B600(t01-a 证实其中有明文 dense code,44 个 dense run,city/lang/stgn/player 家族注册在此)
- fm.exe:.sdata = VA=off+0xA00(raw 0x600..0x557e400);.arch 为压缩壳

## 建议攻击面(按价值排序,自由判断)

1. **.reloc 明文区**(45.7MB,VA=off+0x16B600):t01-a 找到 44 个 dense run 和第二套注册 helper 对(0x6cfff0/0x6d1ef0)。helperB thunk 目标 0x377e370 也在加壳区——若壳是轻量压缩/XOR,dense run 附近可能有解压后代码或跳板表。目标:helperB 语义 + 描述符数组构造器。
2. **注册容器消费端**:push 进容器的 {descriptor, 4CC} 记录被谁读?找到读取者即找到 schema 驱动读写链的入口(helperA 容器指针来自全局/单例,xref 它)。
3. **DBC 保存链**:editor 保存 FMF/DBC 时把字段值按 wire type 编码(`evidence/fm24/reports/editor_fmf/DBC_FORMAT.md`、`reports/editor_gen/replicate/codec_tables.json` 已有 420 条 XML ID↔码映射)。DBC 写入器的类型表 ↔ switch 'cont' 等标签 ↔ .dat 行编码,三者对齐即桥。
4. **fm.exe 的 DBC 应用链**:游戏启动读 .dat + DBC 补丁行。行偏移在 fm.exe 的 schema 结构里(.sdata 46k cmp-switch)。fm 的 comp 注册块与 editor 相同但重排——fm 侧 schema 结构若带行偏移,可直接命中。
5. **旧库伪代码**:`D:\tmp2b\fm24\reports\reverse_engineering\decompiled\` 86 份(function_14242c670.c 提到 database_table_type),`ida/editor_merge_v2.i64` 可只读打开做静态分析;也可参考 `reports/qa/IDA_PROVENANCE.md` 的既有地址。

## 交付(写 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01f\`)

- `output.json`:{slot_layout(更新), constructor, helperB_semantics, row_offset_map(comp ≥10 字段), type_tags, open_questions, falsified}
- `REPORT.md` ≤150 行,每步证据
- **时间与额度纪律:宁可深处做完一条线,不要浅尝全部五条**。若某条线 45 分钟无进展,记录现状换下一条。

## 已证伪/勿重复
- 行解析器无硬编码偏移(两侧已证,勿再扫 magic offset)
- 4CC 不在描述符槽内(E14)
- summary.dat 逐槽语义(b51 负结果);DBC 生成器可靠性问题(与本题无关)
