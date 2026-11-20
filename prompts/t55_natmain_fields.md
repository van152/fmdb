# t55 — Nation table_10 主行字段槽位普查(reader CFG 批量法,sol)

你是受指挥官委派的子代理,负责**最难**的批量字段映射任务。阶段三核心:nation 346 个 schema 字段目前 **0 命名**(BASELINE);但方法基建已经成熟——t47/t49/t51/t53 已把 t10 行框(cursor + identity tail)、slot19 reader extent(`0x103fac0..0x1040be4`,992 可达指令)、mode 分叉(client 0/server 1)、identity/footer 全部闭合验收;Ntxr/t9 各 parent 的"reader 4CC 分发→对象位移→wire sink"三重闸门范式已多次复用。本任务把它推广到**主行内部**:从 t10 主 reader 的可达 CFG 出发,枚举主行 wire 的**字段槽位序列**(按读取顺序的 4CC/类型/位移),再用实档域检验批量晋级。

## 必读
- D:\tmp2b\fm24-db\AGENTS.md(硬约束;候选不写结论;negative 原样保留;L4=0)
- scratch/t47/out/cursor_nation_tax.json + REPORT.md(**t10 双档行界已闭**:server 251 行 13+422323+9、client 13+24710+9;legacy14 借位;identity (0,5,5) 起;footer 00000000|01|ec7ae404)
- scratch/t47/out/REPORT.md 的 Ntxr 三重闸门表(**范式**:frozen 唯一 scoped occurrence→getter 4CC 精确分发→reader sink 同位移→全档域检验)
- scratch/t49/out/REPORT.md(pers→people_db ordinal walk、side/perm 同 byte bitmask、held 口径)
- scratch/t53/out/REPORT.md(逐项三重闸门最新范例+枚举 held 口径)
- evidence/fm24/reports/editor_schema/master.json(nation.xml#nation 346 字段,冻结 SHA 7d57477e)
- scratch/t46/out/REPORT.md(A_B_C_D 内部文法 open 的原始负例——本任务的目标正是把它闭合,但 **t46 负例原文不改**)
- scratch/t22_nation_capital 证据(reports/t22_nation_capital.json——已映射字段的回归夹具)

## 任务
1. **reader CFG 字段序列普查(核心交付)**:从 slot19 主 reader `0x103fac0` 起建完整可达 CFG(t21b_control_flow.ReaderCFG 法,PE exception extent),按**实档执行顺序**枚举每个 wire 消费站点:类型(i8/u8/i16/u16/i32/u32/f32/长度前缀字符串/packed date/内嵌集合)、目的对象 displacement、对应的 getter 4CC(若该站点后接精确分发)。产出 `field_slots.json`:**有序槽位表**(position→type→displacement→candidate 4CC→XML 字段候选)。变长/条件站点(如 presence 闸、版本分叉、Ntxr/Nftb/TCrs 等已闭集合)按已闭口径标注并跳过内部,不重复命名。
2. **XML 对齐**:把槽位表与 frozen nation.xml 346 字段对齐(字段顺序 vs reader 顺序;debug_only/编辑器-only 字段如实标注"无 wire 槽");对齐率与逐字段映射表入 `field_map.json`。**顺序对不上的字段记 mismatch+首反例,不硬凑**。
3. **实档域批量检验**:对每个候选映射,在 server 251 行(双档 client 同步)抽全档值域:i32/i16/i8/u8/f32 域 vs XML min/max/enum_ref;字符串长度分布;packed date 解码(t53 NbPd 法);引用字段(nati 内自引用/club/comp/城市等)走**目标实表实际 ordinal 集**(t49/t53 法),记 hit/miss+首反例。域过+闸门过→**L3**;域冲突/无 enum 域/哨兵歧义→**held** 留首反例。
4. **t46 A_B_C_D 闭合检验**:用槽位表解释 t46 的 A/B/C/D 分段命名(哪些段对应哪些字段簇),把"open"推进为"已解释"(t46 原文不改,新文件记 closure 证据);解释不了的分段如实保留。
5. **回归**:已映射锚点(nation capital、Eng=139/China=55 域、parent 352、Ntxr 7 L3、t53 TCrs 4 held)必须全部复洽——任何冲突=你的映射有错,先自查再报。
6. 独立 verify.py(不 import builder/ReaderCFG/fm24_dump)+ builder scripts/t55_natmain_fields.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 t10 主行;不碰 t9/t25/club 侧;已闭集合(Ntxr/Nftb/TCrs/identity/footer)按已验口径引用不重做。
- 候选不写结论;negative/held 原样保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 预算内无法全闭则诚实 partial:槽位普查完成度+已晋级子集+剩余+首反例。**优先级:槽位普查(1)→XML 对齐(2)→域检验(3)高值字段(引用/现金/日期/布尔簇)→其余。**

## 交付 scratch/t55/out/
- field_slots.json(有序槽位表)、field_map.json(逐字段映射+grades)、instructions.part*.json、branches.part*.json、abc_closure.json(t46 分段解释)、verify.py、REPORT.md、DONE.md
- scripts/t55_natmain_fields.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;只写 scratch/t55/ 与 scripts/t55_*.py;完成跑 verify + t01_anchors.py(7/7)。
