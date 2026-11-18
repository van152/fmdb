# t01 晨报 v6 终版(2026-11-18 08:4x —— 夜班全程封盘,额度线前)

## 一句话

**一夜八连发全部验收入账(E20-E28):杀手锏命中收口阶段一;方法论四场景验证;三个实体验收线达成(comp 18 / weat 89 / stad 16 = 123 个 L3 行偏移字段);首次 L1↔L3 双源互证;全部独立验收,零单信模型自检。**

## 时间线(全部已验收,HEAD = 3da4f4b)

| 时间 | 事件 | 结果 |
|---|---|---|
| 03:35 | gpt-6.2-sol 上线,sol_watch 自动发射 t01f | **18 字段行偏移,阶段一收口(E20)** |
| 04:35 | 指挥官四路独立验收 t01f | 静态 49/49、.dat 独立解压 ALL PASS、锚点 7/7 |
| 04:38-05:08 | t01g(luna)nation 方法论复制 | **负结果:nation=计数循环变长型;7 前缀字段+类全链+duni 锚点复现(E21)** |
| 05:17-05:55 | t01h(luna)factory 跳表全普查 | **74 项全 census:46 直线/7 循环/7 混合/14 不明;裁决 type9=NATIONAL_TEAM_CONTAINER(E23)** |
| 06:10-06:11 | t01i(luna)pers 核心行 | **负结果:主 archive 无 table_1**;新规律:工厂跳表 ≈ archive 表 ID 分发(E24) |
| 06:15-06:32 | t01j(luna)basic_people_db.dat 侦察 | **正面突破:person 行仓库框架解码** —— 658,011 条类变长记录(83/34/22B),身份块+尾全封口;BASIC_PERSON class-4 分支与行字节精确对齐(E25) |
| 06:37-06:59 | t01k(luna)BASIC_PERSON 字段映射 | 负结果:全局状态宽度选择器致 W 条件行偏移,仅 Ptyp@row+1 固定;新知:getter 用 cmp edx(全寄存器扫描)、class 字节=Ptyp 值(E26) |
| 07:02-07:47 | t01l(luna)weat/table_27 行偏移 | **第二实体验收线达成:89 字段 L3**(88 季节+wnam);334 行全量封口;census"直线"修正为固定四季循环(E27) |
| 07:51-08:29 | t01m(luna)stad/table_21 行偏移 | **第三实体验收线达成:16 确定字段 + 首次 L1↔L3 双源互证**(stride 38/181、server≡client 48,413/48,413、四城市锚全复现;2 条件候选诚实排除)(E28) |

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

每个 pi 交付都走了完整验收:safety-scan → 自检 → 指挥官独立字节抽验(不单信模型自检)→ 锚点回归 7/7 → 账本 → 提交。指挥官抽验脚本已沉淀 6 份(f/g/k/l/m_spotcheck + dat_spotcheck),初跑 FAIL 均为我方笔误(VA/offset 混淆、抄写错位、marker 计数),修正后全过——全部记录在案。

## 下一班上手顺序

1. `py -V:3.12 -I scripts/t01_anchors.py`(7/7)→ 读本报告 → LEDGER E20-E28
2. stage-2 主攻(方法论已四场景验证,照方抓药):**club(433,mixed,前缀先行)→ 剩余 43 个直线型逐个复制 → 变长型先恢复行边界 → pers(需 W 解析或 L4)**
3. 三向表持续回填:`scripts/t01_stage2_three_way.py`(t01h census 已并入)
4. sol 额度:已耗 1 次,**默认退役,再用需用户批准**
5. luna 会话可续(t01b/g/h/i/j/k/l/m 各 session 独立在盘上);deepseek 渠道不稳,用前先探

## 不变约束

旧仓与游戏只读;L4=0(全程未启动游戏/编辑器/IDA);无 pip install;claim 带字节证据;LEDGER 只追加(E1-E23)。
