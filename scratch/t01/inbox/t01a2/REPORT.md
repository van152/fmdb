# t01-a2 报告:fm.exe 4CC 注册块/比较式扫描

对象 `D:\tmp2b\fm24\input\fm.exe`,**491,339,776 B**(2025-05-26)。脚本 `scripts/t01a2_fm_sweep.py`(可复跑,`--help`/`--selftest`/`--verify`),机读结果 `fm_sweep.json`。全量扫描 1.7 s。

## 1. 总量与形态

命中 **54,790**(mov 8,021 / cmp 46,769),distinct 4CC **22,348**。按形态:`cmp_r32` 41,477、`cmp_eax` 5,292、`mov_rbp_d8` 3,702、`mov_rsp_d8` 3,450、`mov_rbp_d32` 869。**cmp 式占 85%**——fm.exe 以"XML/属性名→字段"分发为主,注册块是少数。

## 2. 锚点自检(重要修正)

任务书给的 `cnsm`/`cl3n` 是**笔误**:master.json 与两个二进制的实际码是 **`csnm`/`c3ln`**。按原拼写扫得 0(原始 ASCII 也 0 次),按修正拼写全部命中:

| 码 | imm(rev) 命中 | 原始 ASCII(rev) | 码 | imm(rev) | 原始 ASCII(rev) |
|---|---|---|---|---|---|
| cnam | 8 | 431 | crep | 13 | 88 |
| csnm | 6 | 6 | cext | 3 | 11 |
| c3ln | 6 | 6 | PLgn | 7 | 18 |
| cnti | 5 | 36 | dbty | 2 | 6 |
| ccti | 4 | 4 | cpcm | 3 | 3 |

10/10 存在。样本 offset 见 `anchor_check_corrected`(每码前 10 个)。

## 3. 密度剖面:不是"散布全文件",而是"集中在 .sdata"

PE 节区归属(命中/MB):**`.sdata` 50,071 命中 / 89.6 MB = 585.7**;`.arch` 4,634 / 377.8 MB = **12.9**;`.idata` 84 / 13.5 MB = 6.5;`.sxdata` 1。`.arch` 是打包资源区,其 12.9/MB 即**随机噪声底**(x86 立即数偶然凑成 4 个字母数字),`.sdata` 高出 45 倍 = 真实代码。1 MB 窗口:`.sdata` 84 个窗口全部有命中,均值 596、中位 234、最大 2,223;top1% 窗口只占 4.4% 命中(editor 为 12.2%)→ **fm.exe 的 4CC 比 editor 更均匀地铺在代码里,没有 editor 那种 4096 B 密簇**。top20 窗口 19 个在 `.sdata`。

## 4. 聚类(相邻 <4096 B,≥3 命中)

**1,712 簇**(其中 distinct 4CC ≥3 的 1,601)。最大簇 49,337,568–49,413,508(span 75,940,1,328 命中,mov:cmp = 75:1,253)——纯分发 switch。mov 主导的簇(如 19,790,394:471 mov / 391 cmp)才是注册块。

## 5. 实体匹配

Jaccard 绝对值低(person 0.0125 / club 0.0115 / player 0.0079),但**这是分母假象**:fm 的 4CC 全集 20,348 个,含大量与实体无关的比较即时数。改用**覆盖率**(实体码在 fm 中出现的比例)后:中位 **88.3%**,person 93.7%、player 89.9%、club 54.7%、comp 51.4%、nation 33.8%。→ fm.exe 与 editor 共用同一套字段码,只是 fm 侧缺一部分(见 §6)。

## 6. 与 editor.exe 对比:同体系、同代码、不同布局

- **comp 注册块逐码相同**:fm `0x22E8F93`(raw 36,605,107,VA 0x22E96B3)与 editor raw 15,462,499 都是 **63 个码、序列完全一致**:`PLgn cnam csnm c3ln cnti ccti cpcm crep cext cusn culn cmnl cmxl cmnw cmxw cfcl cbcl ctcl clrp ccrp wbcl wbst wben cuae csso Ccre CTty Pcsp…VARd cssp CFcR CFcY Chns CHst CLwR CoII`。**前一轮"fm.exe 里不成 4096B 密簇"的结论应修正为:同一注册块存在,只是被重排到别的偏移**。
- 0x30 步进块:fm 72 个 / editor 58 个,**38 个序列完全相同**(如 fm 34,653,319 ≡ editor 14,444,455,138 码)。fm 独有 34 块(如 34,874,469 的 100 码 person 族、35,661,811 的 `PcPj…Cnam Cnti Clat`),editor 独有 20 块(如 14,580,293 的 101 码 person 族——比 fm 多 1 码)。
- 码表重叠:jaccard(fm_rev, editor_rev) = **0.357**;fm_rev vs master = 0.059,editor_rev vs master = 0.141。
- **缺席(负结果)**:master 2,144 个实体码中 **634 个(29.6%)在 fm.exe 两种读法下都不出现**;但**没有任何实体整体缺席**(32/32 实体至少 1 码命中)。缺席集中在 nation(229/346)、club(196/433)、comp(124/255)——即 editor 侧 UI/编辑专用字段。
- 步进/回归锚点:`48 83 c0 38` 5,716 次(首 452,695)、`48 83 c0 30` 156 次(首 461,966)、`81 fa 63 70 61 63` 2 次(首 77,200,626)。

## 7. 复现

`py -V:3.12 -I scripts/t01a2_fm_sweep.py --selftest` → 0;`--verify fm_sweep.json` 随机 3 offset 回读全部 OK(exit 0);JSON 可 `json.load`(1.37 MB)。
