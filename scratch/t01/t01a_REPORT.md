# t01-a: editor.exe 4CC 属性注册块全量扫描报告

产物: `scratch/t01/t01a_editor_sweep.json` (1.28MB; meta / clusters / dispatch_switches / entity_index / hits / aux_hits / residual_code_hits)
复验: `py -V:3.12 -I scratch/t01/verify_4cc.py` → 2954/2954 primary hits、175 簇、357/357 调用目标、254 switch 样本全部对回 exe 原始字节 (ALL CHECKS PASSED)

## 总量
- 扫描 74,807,296 B;主形态命中 2954 (c7_45:1711, c7_44_24:1025, c7_85:190, c7_84_24:28),gap<4096 聚成 **175 簇** (.rdata 118 / .reloc 57);confidence: high 25 / medium 8 / low 142
- **comp 锚点复现**: 0xebf060..0xebf9c7,51 块,步长 {0x30:50},helperA=0x83abf0 / helperB=0x83caf0,匹配 comp.xml#comp cont=0.9412 (high)。注意:这只是 comp 注册函数片段,comp 255 码中仅 48 码在此 (cov=0.19)

## 注册函数 (mov-imm 内联块,每块 `c7 45 f0 <4CC反序>` ... e8 helper,步长 0x30)
- **helper 对 A (0x83abf0/0x83caf0)**: 72 个 dense run,全部在 .rdata。实体→函数 off:
  nnpl 0xdc67a4 | pers 0xde7a42 + 0xdfc1f0 + 0x1199290 + 0x15e7cb0 | awar 0xe490b0 | club 0xe87d74 | ktfl 0xeab22a + 0x11fa3e7 | **comp 0xebf060** | drbr 0xffcc50 | stad 0x1185040 | nati 0x11eff90 | mdso 0x1546900 | inju 0x1580560 | offc 0x1585b59 | weat 0x158cad0 | jour 0x15d8069 | agen 0x1435789
- **helper 对 B (0x6cfff0/0x6d1ef0)**: 44 个 dense run,全部在 .reloc 段 (VA=off+0x16B600)。city 0x3aa7220 (Cnam/Cnti/Clat...)、lang 0x3d55b50 (Lnam/Linf...)、stgn 0x43e4fc0 (SNna...)、player 家族 0x3a72a90 (PCAB/PPAB/PCRP...)、team 0x4390800 — 第二套注册子系统,大小写敏感的另一码形
- 另有微量 helper 对 (0x1069c0/0x834de0)×3、(0x2273d0/0x8330d0)×3 run,未定实体 (low)
- 未匹配簇: low 142 簇几乎全为散点噪声 (单码重复/字符串巧合);c2tm/c3tm/c4tm、alnm 无 mov-imm 注册函数 (见异常 3)

## 每实体码覆盖 (master.json entity_summary,32 实体;命中=任何 imm 上下文 mov/cmp/push)
- 22/32 实体 **100%**: awar CntF drbr inju jour lang mdso offc stgn ktfl weat agen agrm alnm curr dscr regi city cont team lcrg stad
- 部分覆盖: nnpl 128/129, pers 261/271, c2tm/c3tm/c4tm 25/30, prnm 4/8, **comp 143/252, club 239/431, player 93/179, nation 133/346**

## 分发 switch — H2 证实 (`81 f8..ff <4CC反序>` + `0f 84 <rel32>`,cmp 步长 0xC)
- comp: **0xec0095..0xec2d35** (110 cmp,95 comp 码) + **0xecad39..0xecbfc4** (112 cmp,102 comp) — E4 区域定性为 comp 读写 per-field switch
- club 家族: 0xe82b4c (199 cmp) + 0xe89c24 (220 cmp,含 C2*/C3*/C4* 码,即 club b/c/d team 共用) + 0xe57e2c (32)
- person 0xde9ad9 (110) / 0x109a3d5 (141);nnpl 0xdc8276+0xdc9b38;player 0xe247c0;stad 0x1185f5e+0x11892a7;drbr 0xffd1f5+0xffdfd2;全文件共 **103 个 switch 簇**,明细在 JSON dispatch_switches[]

## 异常发现
1. **.reloc 段 45.7MB 且含活代码**: helper 对 B 注册函数与 switch 在此;.code 段 rsize 仅 0x200 (加壳),真码实际在 .rdata (VA=off+0xA00) 与 .reloc (VA=off+0x16B600)
2. **615 个实体码在 74.8MB 内无任何字面字节** (comp 109, club 192, nation 213, player 86, pers 10, c2tm 5;如 RJ12/RP23/PMst/PDld): 疑在 .arch (0x46c4800, 压缩原 .code) 运行时解压侧,或该 build 未注册 — **unknown**,建议 t01-b 解 .arch 验证
3. **c2tm/c3tm/c4tm 无内联注册块**,仅出现在 club 家族 switch → 其注册走通用/表路径,非 c7 块形态
4. 615 码缺失主要集中在大实体;小实体基本齐全 → 大实体的注册可能部分在运行时解压代码中
5. 噪声源: .rdata 头部 0x2173a6 (455 命中) 等为字符串巧合;两簇 3-hit "club" 高置信簇 (0xe850f8/0x11f6fa2) 是弱信号,采信需谨慎

## 方法备注
- 纯 stdlib 字节扫描 (`sweep_4cc.py` + `analyze_4cc.py`),无反汇编器;confidence 规则见 JSON meta.confidence_rule
- hits[] 每条带指令起始 off + imm off;4CC = imm32 字节反序 (如 `6d 61 6e 63`→cnam);主簇仅用指挥官规格的 c7 形态,push/mov_r32/cmp 形态仅作残码定位
