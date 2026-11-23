# t74 — 9 表行框(行边界 + 行长)双档闭合

日期 2026-11-20 · 分支 `t74-row-frames9` · 只读数据侧,未启动游戏/编辑器

## 1. 结论

**17/17 个 (archive, table) 行框闭合**,`header + Σrow_len + footer == payload_len` 逐字节成立,
每表 identity 宽度**独立自证为 13B**(不跨表照抄),`bad_identity = 0`。

| 表 | 实体 | 归档 | payload | header | count | 行长 | 模型 |
|---|---|---|---|---|---|---|---|
| 56 | agreement | client+server | 100 | 14 | 6 | 13 定长 | fixed |
| 0 | award | client+server | 272,987 | 14 | 3,545 | 77 定长 | fixed |
| 21 | stadium | client | 1,839,716 | 14 | 48,413 | 38 定长 | fixed |
| 21 | stadium | server | 8,762,775 | 14 | 48,413 | 181 定长 | fixed |
| 8 | language | client+server | 5,248 | 14 | 126 | 37..53 | 顺序语法 |
| 27 | weather | client+server | 43,345 | 14 | 334 | 117..156 | 顺序语法 |
| 18 | derby | client | 139,891 | 14 | 1,567 | 69..195 | 顺序语法 |
| 18 | derby | server | 149,293 | 14 | 1,567 | 75..201 | 顺序语法 |
| 7 | media | client | 36,824 | 14 | 208 | 80..715 | identity DP |
| 7 | media | server | 38,280 | 14 | 208 | 87..722 | identity DP |
| 47 | local_region | client+server | 109,505 | **14** | 2,488 | 41..76 | identity DP |
| 24 | team | **server only** | 8,819,030 | 14 | 84,507 | 86..666 | identity DP |

footer 一律 8B。t24 在 client 档无该表条目(声明 `status: absent`),非解析失败。

## 2. identity 三元组与宽度自证

每行尾 13B:`[ordinal u32][UID u32][UID u32][尾字节]`。
`ordinal == 行下标`(即 fm24_dump 的 `rdui`),两处 UID 相等(即 `duni`)。

宽度**不靠引用** club 12B / nation 13B,改用两条独立判据(见 `identity_width_proof.json`):

**判据 A — 对齐自证。** 行框先用与 identity 无关的方法独立确定(fixed stride / 顺序语法 / 唯一 DP),
然后统计行尾 `-11..-16` 六个偏移中"能构成 (ordinal==i ∧ UID 对相等)"的行数:

| 偏移 | -11 | -12 | **-13** | -14 | -15 | -16 |
|---|---|---|---|---|---|---|
| 17/17 档命中 | 0 | 0 | **全部行** | ≤1 | ≤1 | ≤1 |

只有 `-13` 对**每一行**成立,其余偏移最多偶然命中 1 行(prefix 字节巧合)。故宽度 = 13。

**判据 B — footer 唯一性。** 固定 W=13,footer 扫 5..12,只有 footer=8 有非零铺法;
16/17 档为唯一 1 路,t27 为 3 路(见 §4.1)。

**尾字节语义。** 16 档中 15 档尾字节恒为 0(marker);t24 为 selector:`{10: 84,256, 11: 250, 0: 1}`,
故 t24 的判据 A 用"UID 对相等"而非"尾字节为 0"。

## 3. 行语法(逐表)

- **56 agreement** `13 定长`。`14 + 6×13 + 8 = 100`。
- **0 award** `77 定长`。`14 + 3545×77 + 8 = 272,987`。
- **21 stadium** `client 38 / server 181 定长`。双档 `48413` 行同数,行长差 143B 来自 server 独有字段段。
- **8 language** `[u32 len][UTF-8 名][17B][13B identity]`。双档 payload 逐字节相同。
  名字后缀恒 30B,`u32@suffix+17 == ordinal` 126/126(即 `rdui_suffix@17`)。
- **27 weather** `[u32 len][UTF-8 名][95B 数值中段][13B identity]`。双档逐字节相同。
- **18 derby** `k 个 lstr 名 + (const-4k) 数字段 + 13B identity`;
  `k∈{2,4}`(1446 行 k=2,121 行 k=4);`const = 65`(client) / `71`(server),即 server 每行 +6B。
- **47 local_region** `41 + 5k`(k≥0),行长集 `{41,46,51,56,61,71,76}`,2488 行全满足 `(len-41)%5==0`。
- **7 media** identity DP 唯一铺法;server 每行比 client 长 7B(208/208 行),插在 identity 前。
- **24 team** identity DP 唯一铺法;84,507 行,行长 86..666(均值 104.358),server 独有。

## 4. 与上游的冲突与负结果(保留原文)

### 4.1 t27 的 DP 多解
固定 95B 中段的顺序语法闭合 334/334,但纯 identity DP 在 (W13/f8) 下给出 **3 路**。
三路差异落在 opaque 中段内部,不影响行边界。已用"行长 == 4+name_len+95+13"这一独立约束收敛到唯一语法;
DP 的 3 路作为负结果保留,不删。

### 4.2 t47 header 25 → 14(推翻上游 OVERRIDE)
上游 OVERRIDE 记 `25 + 2488*44 + 8`。实测 **H=25 时首行 35B**,违反全表 `(len-41)%5==0`;
**H=14 时 2488/2488 行满足**。DP 在 H=14 与 H=25 下都唯一(两者只是把同一段字节切成 35+41… 或 41+41…),
但只有 H=14 与行长规则自洽,故取 14。t47 的 `rdui@-13/duni@-9` 锚点在 H=14 下 2488/2488 命中。

### 4.3 t24 上游 82B 均值不成立
上游记 E37 82B 定长、均值 104.36B。实测变长 86..666,均值 104.358,唯一铺法闭合。

### 4.4 未解语法(不阻塞行框)
- t7 media 中段的嵌套 count/list 结构未定(客户端 fitcount `{1:105, 0:57, 2:46}`,server 无简单拟合)。
- t7 identity 前 5B 有 16 种取值;server 的 +7B 插入为数据侧观测,未给语义。
- t18 server 的 +6B 插入同理。

## 5. 锚点回归(全部通过)

| 表 | 锚点 | 结果 |
|---|---|---|
| 21 stadium | `Scti@3 / Slat@17 / Slon@21` | 48,413/48,413 |
| 21 stadium | `rdui@25 / duni@29` | 48,413/48,413 |
| 0 award | `rdui@64 / duni@68` | 3,545/3,545 |
| 56 agreement | `rdui@0 / duni@4` | 6/6 |
| 47 lcrg | `rdui@-13 / duni@-9` | 2,488/2,488 |
| 8 language | `rdui_suffix@17`(后缀内偏移) | 126/126 |

`Slat@17` / `Slon@21` 按 f32 读,5000/5000 落在 `[-180,180]`,值域 `[-42.97,70.20]` / `[-175.21,178.45]`。

**口径纠正(负结果保留):** 任务简报把 media 锚点 `rdui@3/duni@7` 归到 **t7**;
`fm24_dump.FIELDS` 中该条目实际是 **`("client", 6)`**(行 16B 定长,115 行),t7 在 FIELDS 里**没有条目**。
t6 的 `rdui@3/duni@7` 实测 115/115 命中。t7 的 identity 内部一致性(`-13`/`-9`)208/208 通过。

## 6. 复现

```
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -3.12 -I -B scripts/t74_row_frames9.py      # 17/17 闭合
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -3.12 -I -B scratch/t74/out/verify.py       # 95/95
```

`verify.py` 不 import builder,自行重载 payload 与重建行框(独立实现),用于对拍。

## 7. 证据等级

- 行框闭合、行长分布、identity 对齐自证:**L1**(自家解码自检,可复现)。
- 锚点命中:**L2**(与既有 `fm24_dump` 字段表独立事实对照)。
- 未做 exe 静态证据(L3)、未做真机加载(L4)。
