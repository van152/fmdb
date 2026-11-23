# t01-g 任务书:序列化器方法论复制到 nation(t01f 方法论的第一站)

> 交给 pi gpt-6-luna max。t01f(gpt-6.2-sol)已解决 comp 行偏移桥并固化方法论;你的任务是把该方法论**完整复制到 nation**,产出同形状工件。
> 规则不变:只读输入、不启动游戏本体/FM 编辑器(IDA 静态分析允许)、不 pip install、Python `py -V:3.12 -I -B`、每个 claim 带 file offset + 字节证据。

## 背景:阶段一已收口(E20)

t01f 结论(必读 `scratch/t01/inbox/t01f/REPORT.md` —— 这是你的方法论模板):

- 行偏移**不在**描述符槽内;`helperB()+0x38` 是 `RAW_TYPED_TRAITS<unsigned int>`(共享类型 traits)
- 真实机制:COMP 序列化器(slot19 读主体 off 0xeb7000 / slot21 写主体 off 0xeb8920)按**固定指令顺序**逐字段传输,`mov r8d,N`(41 b8 N..)/`lea reg,[rbx+disp]` 等即时数给出宽度与对象偏移,静态累加即得行偏移
- 4CC→对象成员的分发 switch 在 0xEC0000..0xEC6000 + 0xECA000..0xECC000(`cmp esi/r32,<4CC 大端>` + `je handler`),成员访问指令模式:`mov/movsx [r12+disp]` 或 `lea reg,[rbx+disp]`
- 身份块:12B 读入 COMP+8/+0xc/+0x10;+114 = 行序号(旧"rdui"标签勿沿用);+118 = 8B 重复 ID

## 你的任务:nation(旧库 table_10,251 行,强候选实体)

1. **找类**:在 editor.exe 搜 nation 记录类 RTTI(`.?AVNATION@db@@` 之类;若命名不同,从 `db::DATABASE_TABLE<?>` 家族或 type-id 工厂跳表反查——COMP 的 type query 返回 25,nation 应返回 10)。拿到 RTTI、构造器、vptr、sizeof。
2. **找读写主体**:vtable 内 slot19/slot21(参照 COMP:0x187d350/0x187d360 的位置模式),追 e9/e8 链到读/写主体函数。
3. **走宽度累加**:逐指令记录顺序、目标寄存器、分支、宽度;与 client_db.dat table_10 行字节对照验证。
4. **对齐 4CC**:用 master.json 的 nation 346 码,在 switch 区域提取 nation case(t01b_switch_extract.py 可参数化复用,REGIONS 已含两段);把 4CC → 对象偏移 → 行偏移三元组建全。
5. **锚点验证**:旧库 table_10 锚点(见 `evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md`:251 行,duni 样例 472446402670,rdui-行序号模式);每个字段值抽 3+ 行对照原始字节。nation.xml 的语义字段名(如 `nfil/nsho/nshof` 等,以 master.json 为准)只作命名参考,不猜值。

## 验收判据

- nation 客户端行 **≥10 个字段**的行内偏移映射(L3,每条带访问指令 + 流宽度指令字节证据),且与 duni/身份块锚点一致;
- 或给出负结果:该实体序列化模式与 COMP 不同,指出差异点(如分支表驱动而非直线累加)并给出你实际能证明的部分。
- 交付 `scratch/t01/inbox/t01g/`:`output.json`(同 t01f 形状)、`REPORT.md` ≤120 行、`verify.py --selftest`(只读自检,含负对照)。

## 纪律

- 深度优先:一条线走穿,不浅尝;45 分钟无进展记录现状换线。
- 勿重复 t01f 已证部分(直接引用其工件);勿沿用已证伪假设(E20 falsified 清单,含"4CC 在槽内""helperB 是墙""rdui@+114")。
- nation 若 45 分钟内找不到 RTTI,先记录检索过程,再试从 table_10 的工厂跳表项(参照 COMP:0xf49d9c type-25 项 → 0xf49129)反查 type-10 项。
