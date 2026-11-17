# t01 晨报 v4(2026-11-18 04:4x —— 杀手锏命中版,替代 v3)

## 一句话

**gpt-6.2-sol 杀手锏命中:行偏移桥已解决,comp 行新增 18 个 L3 字段偏移(验收线 ≥10),阶段一收口;四路独立验收全过,账本 E1-E20,已提交。**

## 杀手锏结果(t01f,03:35-04:26,gpt-6.2-sol max)

- **交付**:18 个 comp 客户端行 L3 字段(4CC → 行偏移/宽度 → 对象偏移),如 `cmnl@+76/2`、`cnor@+84/4`、`wbst@+103/4`;5 个既有锚点(ccti@+52 等)全部一致
- **架构结论(修正)**:行偏移**不在** 56B 描述符槽内 —— `helperB()+0x38` 是共享的 `RAW_TYPED_TRAITS<unsigned int>`;真实机制 = COMP 序列化器按固定指令顺序逐字段传输,宽度即时数直接可读(静态累加即得偏移)。**方法论已固化,可复制到其他实体**
- **helperB 不是墙**:thunk → VA 0x14377e370(.reloc 明文区),TYPED_TRAITS_MANAGER 单例 —— E11/E14/E18 的"墙"结论仅对此 thunk 解除
- **两个勘误**(字节事实不变,标签修正):
  1. 0x187d2b0 是 RTTI 指针,真 vptr = 0x187d2b8,注册函数 = 0-based slot5(原"slot6"计数含 RTTI 指针)
  2. 旧库 `rdui@+114` 实为**行序号**(我独立复验:60/60 行 +114 == row_index);原生 rdui = +122;旧库 table_21 的 `rdui@+30==row_index` 同属此系统性误标
- **验收四路全过**:
  1. 指挥官独立静态抽验 49/49(editor.exe 原始字节,`scripts/t01f_spotcheck.py`)
  2. 指挥官独立解压 .dat 抽验 ALL PASS(row7/250/639 + 行序号扫描,`scripts/t01f_dat_spotcheck.py`)
  3. 锚点回归 7/7
  4. sol 自检 PASS(7047 行 + server join + 负对照)

## 验收台账(E1-E20)

| 任务 | 渠道 | 核心产出 |
|---|---|---|
| t01-a / t01a2 | glm53 / pi hiyo | editor+fm 全景;fm≡editor 同代码异布局 |
| t01-c | glm53 | 32 实体/2343 码词汇表 |
| t01-b r1+r2 | pi luna max | helperA 精化;0xfe72b0 工厂 17 标签 |
| t01-e | glm53 | 12/32 实体虚表↔注册函数映射 |
| 指挥官 | — | switch 121 case、E19 标签主轴、锚点护栏、t01f 四路验收 |
| **t01f** | **pi gpt-6.2-sol max** | **18 字段行偏移 + 序列化器方法论 + 3 项修正;阶段一收口** |
| t01g | pi luna max | 负结果分支:nation 是计数驱动变长序列化(非直线);类全链 + 7 前缀字段 L3 + duni 锚点复现(E21) |

## 结构认知(终版)

```
.dat 行 ←—— 序列化器逐字段(固定顺序+显式宽度,静态可推导)——→ 运行时对象(db::COMP, sizeof 0x1b0)
              ↑ slot19=读主体 0xeb7000 / slot21=写主体 0xeb8920
              XML/DBC 4CC → switch → 对象成员(已提取 121 case)
```

## 下一班顺序(09:00 后新会话)

1. `py -V:3.12 -I scripts/t01_anchors.py`(7/7)→ 读本报告 + LEDGER E20/E21
2. **t01g 已验收(E21,负结果分支)**:nation 是计数驱动**变长**序列化(非 COMP 直线型),7 前缀字段 L3 + 类全链 + duni 锚点复现;nation getter 窗口 0x1041930..0x1045300(**switch 区是实体特异的**,t01b 区间不代表全部实体)
3. 阶段二攻击顺序(E21 结论):**先直线型实体**(从 factory 跳表 32 项逐一判定,套 t01f 方法),后变长型(nation 类:先恢复行边界);三向表 `table_type ↔ entity ↔ registration_fn` 合流(t01e + property_map)
4. server 扩展全解析(t01f 已给出 join 方法与众数 71B 起点)
5. comp 剩余字段(2 组版本化 byte 数组、内联名称模式)可续 sol 会话 —— **但 sol 额度已耗 1 次,默认不再用,除非用户批准**

## 不变约束

旧仓与游戏只读;L4=0(全程未启动游戏/编辑器/IDA);无 pip install;claim 带字节证据。
