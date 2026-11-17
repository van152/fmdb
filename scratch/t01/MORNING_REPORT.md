# t01 晨报 v5 终版(2026-11-18 06:1x —— 夜班全程封盘)

## 一句话

**一夜四连发全部验收入账(E20-E23):杀手锏命中解决行偏移桥并收口阶段一;方法论边界已探明;stage-2 排序就绪;下一个最高价值目标(pers 核心行)已在跑。**

## 时间线(全部已验收,HEAD = 3da4f4b)

| 时间 | 事件 | 结果 |
|---|---|---|
| 03:35 | gpt-6.2-sol 上线,sol_watch 自动发射 t01f | **18 字段行偏移,阶段一收口(E20)** |
| 04:35 | 指挥官四路独立验收 t01f | 静态 49/49、.dat 独立解压 ALL PASS、锚点 7/7 |
| 04:38-05:08 | t01g(luna)nation 方法论复制 | **负结果:nation=计数循环变长型;7 前缀字段+类全链+duni 锚点复现(E21)** |
| 05:17-05:55 | t01h(luna)factory 跳表全普查 | **74 项全 census:46 直线/7 循环/7 混合/14 不明;裁决 type9=NATIONAL_TEAM_CONTAINER(E23)** |
| 06:10-06:11 | t01i(luna)pers 核心行 | **负结果:主 archive 无 table_1**;新规律:工厂跳表 ≈ archive 表 ID 分发(E24) |
| 06:15-06:32 | t01j(luna)basic_people_db.dat 侦察 | **正面突破:person 行仓库框架解码** —— 658,011 条类变长记录(83/34/22B),身份块+尾全封口;BASIC_PERSON class-4 分支与行字节精确对齐(E25) |
| 06:37- | t01k(luna)BASIC_PERSON 字段映射 | 运行中 → `inbox/t01k/`(第二实体验收线 ≥10 字段冲刺) |

## 项目结构认知(夜班后终版)

```
.dat 行 ←—— 序列化器(直线型:固定顺序+显式宽度,静态可推导)| (变长型:计数驱动循环)——→ 运行时记录类(63 个!)
         factory 跳表 74 项(type-id→handler→ctor→RTTI)—— 11 项无专属工厂
         32 editor 实体 ⊂ 63 记录类;275 个 db@@ 类名全清单在手
```

- **阶段一(comp ≥10 字段行偏移)达成**:18 字段 + 5 锚点一致 + 四路独立验收
- **方法论边界**:直线型(46 个)可直接套 t01f 宽度累加法;变长型(7 循环+7 混合)需先恢复行边界;**type 1 pers(271 字段)= straight-line,最高价值目标,t01i 在做**
- **三向表建成**(E22+E23):`scratch/t01/stage2_three_way.{json,md}` —— table_type↔entity↔registration_fn+mode
- **勘误三则**:0x187d2b0 是 RTTI 指针(注册函数=0-based slot5);旧库 rdui@+114/+30 实为行序号(系统性);t01e 的 nati 双虚表实为 NATIONAL_TEAM_CONTAINER/TEAM_CONTAINER

## 验收纪律执行情况

每个 pi 交付都走了完整验收:safety-scan → 自检 → 指挥官独立字节抽验(不单信模型自检)→ 锚点回归 7/7 → 账本 → 提交。我方脚本初跑的 FAIL 均为我方笔误(VA/offset 混淆、抄写错位),逐条修正后全过,无实质不符——全部记录在案(E20/E21/E23 evidence 字段)。

## 下一班上手顺序

1. `py -V:3.12 -I scripts/t01_anchors.py`(7/7)→ 读本报告 → LEDGER E20-E24
2. **t01j 已验收(E25)**:person 行仓库框架解码(658,011 行全量封口,指挥官独立走查复现);**t01k 运行中**(BASIC_PERSON ≥10 字段 → E26),验收协议同前
3. stage-2 主攻:三向表排序——**pers(框架已就绪,t01k 字段映射)→ club(433,mixed,前缀先行)→ weat(94,直线)→ stad(60,直线)**;变长型(cont/mdso/nati)先恢复行边界
4. sol 额度:已耗 1 次,**默认退役,再用需用户批准**
5. luna 会话可续(t01b/g/h/i/j 各 session 独立在盘上);deepseek 渠道不稳,用前先探

## 不变约束

旧仓与游戏只读;L4=0(全程未启动游戏/编辑器/IDA);无 pip install;claim 带字节证据;LEDGER 只追加(E1-E23)。
