# t50 — t9 NATIONAL_TEAM_CONTAINER 数据侧独立画像

状态:`partial_data_profile_t9`。证据等级 **L1**(本仓重算)+ **L2**(双档/跨表对照);**L3 = 0,L4 = 0**。

本任务只做数据侧:t50 未读 `editor.exe`、未读 IDA、未追 reader/VA、未命名任何语义字段、未做 target ordinal join。
所有 framing 规则都标为**候选**,并附敏感性表说明哪些参数由数据钉死、哪些不由数据决定。

## 1. 归档与成员锚点(4 成员全部独立解码)

成员绝对起点 = `data_base(34) + entry.offset`;按 `entry.size` 选帧;`packed_sha256` 由本仓在压缩区重算。
两档目录条目数 client 31 / server 77,`data_base` 均 34,与 E80 一致。

| 成员 | entry.offset | packed_size | declared size | member_start | payload SHA-256 (前 16) | padded SHA (前 16) | count@8 |
|---|---|---|---|---|---|---|---|
| client `table_9.dat` | 5133549 | 10752 | 31956 | 5133583 | `784810f0946a25d2` | `4e85f79f11196cf0` | 251 |
| client `table_extra_9.dat` | 5144301 | 17352 | 83927 | 5144335 | `2717052d63a4cba9` | `91d149897032833f` | 251 |
| server `table_9.dat` | 8726725 | 82354 | 307564 | 8726759 | `6c2d8a0606de2665` | `57ea2e312e8bbd59` | 251 |
| server `table_extra_9.dat` | 8809079 | 28845 | 105228 | 8809113 | `a56715372b33bd48` | `e4931778250325da` | 251 |

- 4 成员均为 **单帧** zstd,帧长 == declared size,**无游离字节**。
- tad shell `03017461642ef10d` + `u32 count@8 == 251`:4/4 成立。
- `table_extra_10.dat` 两档均**缺失**(负结果保留)。
- 上表 anchors 与 `scratch/t47/out/discovery_nation_unknown.json` 的 archive 记录**逐字节一致**
  (offset/packed_size/size/member_start/packed SHA/payload SHA/count 七项全等),但 t50 未取用其任何静态结论。

## 2. `table_9.dat` — 行边界可由 identity tail 唯一闭合(L1)

`t9` 的行尾结构 = **13 字节 `ordinal | row_id | row_id | 0x00`**(与 t10/t46 同形)。用它做游标:

| 档 | 方程 | 闭合 |
|---|---|---|
| client | `13 + Σ(row_lens=31935) + 8 = 31956` | 精确 |
| server | `13 + Σ(row_lens=307543) + 8 = 307564` | 精确 |

- 两档均 **251 行**,行边界连续无洞无叠(verify 逐行验证 `offset` 递推 == `Σlen`)。
- 闭合唯一性(**不是简单首解**,而是对全部候选分区做 DP 计数):在"row_id 非 0 且严格递增"规则下
  **client = 1 条完整铺法,server = 1 条**。

### 2.1 framing 敏感性(哪些参数由数据钉死)

| 变体 | client 完整铺法 | server 完整铺法 | 读法 |
|---|---|---|---|
| footer=7 | 0 | 0 | 钉死 |
| **footer=8(交付)** | **1** | **1** | 唯一能闭合的切分 |
| footer=9 / 10 / 12 | 0 | 0 | 钉死 |
| header=11..15 | 1 | 1 | **不由数据决定**:11..15 窗口内不落任何 identity,故 header/selector 切分数据无法区分 |
| 忽略 marker 必须为 0x00 | 1 | 1 | marker 不是载荷承重项 |
| 允许 row_id = 0 | 1 | **362** | **承重**:行体内的 `ordinal|0|0|0` 诱饵会炸开解空间 |
| 放弃 row_id 递增 | **6** | **24** | **承重** |
| 允许 0 + 放弃递增 | 50331648 | 295302623920128 | 完全失控 |

**结论(诚实边界)**:footer=8 与"row_id 非零 + 递增"这两条由数据独立钉死;header 的 13 字节切分**不能由数据自证**
(候选,不写结论)。server 的 362 条宽解全部只出现在 **row 0**(同一段连续 0 值 `ordinal=0` 诱饵族),
一旦要求 row_id 非零即收敛为 1 —— 这不是"强行挑首解",而是规则敏感性可复核。

### 2.2 identity census

| 项 | client | server |
|---|---|---|
| ordinal 序列 == 0..250 | 是 | 是 |
| repeated lane 相等(row_id == repeated_id) | 251/251 | 251/251 |
| marker 全 0x00 | 251/251 | 251/251 |
| row_id 唯一 | 是 | 是 |
| row_id 严格递增 | 是 | 是 |
| row_id 取值域 | 5 .. 82082540 | 5 .. 82082540 |
| 选中尾中 row_id == 0 | 0 行 | 0 行 |
| 末行 row_id == footer u32@-4 | 是(82082540) | 是(82082540) |
| 逐 ordinal 候选数直方图 | `{1:225, 2:25, 54:1}` | `{1:112, 2:53, 3:21, 4:19, 5:9, 6:8, 7:3, 8:2, 10:3, 12:1, 13:1, 14:1, 18:1, 20:3, 22:2, 23:1, 25:1, 26:1, 27:1, 32:1, 69:1, 88:1, 107:1, 232:1, 264:1, 290:1, 53072:1}` |

server 的候选密度远高于 client(row 0 有 53072 个候选),这是 server 行体更长的直接后果;唯一性来自
**递增 + 非零 + 全区闭合**三条联合约束,不来自任何外部锚点。

### 2.3 行长度分布

| 档 | 直方图 bin 数 | min | max | mean | 最多见长度 |
|---|---|---|---|---|---|
| client | 92 | 58 | 461 | 127.231 | 58×53, 76×13, 94×11, 107×9, 98×8 |
| server | 211 | 383 | 36514 | 1225.271 | 383×23, 415×3, 475×3, 431×2, 435×2 |

server 最长行 36514 B 是 client 最长行(461 B)的 79 倍 —— 双档行体不可互换。

## 3. `table_extra_9.dat` — 只能定位块首,块内文法未解(诚实 partial)

结构:**block 起始 = `u32 ordinal | u32 name_len | name bytes`**(候选形,由 record 0 锚定)。

| 档 | 方程 | 完整铺法 | 最终位置 | 块内歧义 |
|---|---|---|---|---|
| client | `12 + Σ(block_spans=83915) = 83927` | **1** | 唯一 | 0 块 |
| server | `12 + Σ(block_spans=105216) = 105228` | **4** | 4 条解都落在同一末块起点 105048 | 2 块(row 2、row 82) |

- 251 块全部定位,首块起点 12,末块起点 client 83769 / server 105048,**块连续铺到载荷末尾**。
- `block_span`:client 23..850,server 45..944;无名字块(block 内 `name_len==0`)client 52 / server 54。
- server 的 4 条解**只在块内部分歧**(row 2 候选 867/875、row 82 候选 39439/39533),不影响块首;
  交付取最早候选,并原样记下 4 解与 2 处歧义,不外推。
- **块内文法(除 ordinal+name 前缀外的字节)未解**,记为 `unknown`;本任务不猜。
- **末尾无独立 footer**:与 `table_9` 不同,末块一直跑到载荷末字节;client 末 9 字节为
  `01fffafafaff2f55b5`、server 末 9 字节全 0,均不构成可分离的计数/标志尾。记 `footer_separable=false`。

### 3.1 identity 结构不存在(负结果原样保留)

把 t9 的 13 字节 identity 判定式**原封不动**套到 `table_extra_9`:

| header | footer | client 完整铺法 | server 完整铺法 | 死在哪行 |
|---|---|---|---|---|
| 12 | 0 | 0 | 0 | row 1 |
| 12 | 8 | 0 | 0 | row 1 |
| 13 | 0 | 0 | 0 | row 1 |
| 13 | 8 | 0 | 0 | row 1 |

判定式在 **row 1 就死**,4 变体全 0。首反例:`row 0` 前 13 字节 = `000000000b0000004c65732046`,
即 `ordinal=0 | name_len=11 | "Les F…"`,**不是** `ordinal|id|id|00` 尾。

另有 client 0 / server 22 个块的末 13 字节"看起来像" identity 尾(重复 u32 + 0x00),但那是块内容的巧合重复,
用它当边界无法闭合 —— 计数原样保留,但**不当作证据**。

## 4. 双档对比(`grammar_diff_t9.json`)

### 4.1 `table_9`:计数与 identity 相同,行体不同

- count 251 == 251;**ordinal 序列逐行相同**;**row_id 序列逐行完全相同**(首差异 = 无)。
- 但**零行字节相同**(`identical_row_count = 0`),行长分布不可比(client 58..461 vs server 383..36514)。
- 判定:**row body grammar 不同构**;相同的只是 identity 阶梯(ordinal + row_id ladder),行体本身不同。
- 同偏移探针(row 0,+0/+1/+2/+4/+8/.../+64)全部记在 `same_offset_probe_row0`,**一律标注为
  "positional probe only; no field is assigned"**,不赋任何语义。

### 4.2 `table_extra_9`:结构本身不同

- 无 identity 尾(见 3.1),改用块首 `ordinal + name_len + name` 标记。
- 块数相同(251)但块跨度分布不同(client min 23 / server min 45),块间不能按长度对齐。

### 4.3 跨表对照(t9 vs t10,纯数据侧)

| 项 | client | server |
|---|---|---|
| t10 用同一 identity 判定式的完整铺法 | 1 | 1 |
| t10 精确闭合 | 是 | 是 |
| t9 row_id 阶梯 == t10 row_id 阶梯 | **是** | **是** |
| t9 行跨度 != t10 行跨度 | 是 | 是 |

t9 与 t10 各自独立解码,却给出**完全相同的 251 条 row_id 序列**,而行跨度不同。
这在数据侧说明:两表共享**同一个 row_id/ordinal 阶梯**,不共享行体。此为数据侧跨表一致,**不是** ordinal join,
也未命名任何字段。

## 5. 样本与探针

- `profiles/table_{client,server}_9.rows.jsonl`:每行 `row / offset / body_offset / len / identity{ordinal,row_id,repeated_id,marker,tail_offset_in_row,basis} / prefix_probe_i32le / raw_hex`。
- `profiles/table_{client,server}_extra_9.rows.jsonl`:每块 `row / offset / body_offset / len / marker{ordinal,name_len,name_ascii,name_hex,basis} / prefix_probe_i32le / raw_hex`。
- 每成员 6 个样本(首/次/末/最短/最长/按长排序)存在 `profile_t9.json` 的 `row_samples` / `block_samples`。
- `prefix_probe` 偏移:t9 记 +0/+1/+4/+8/+12/+16/+20/+24/+32/+40;extra_9 记 +0/+4/+8/+12/+16/+20/+24。
  每个探针都带 `"meaning": "unassigned positional probe; not asserted as a count or a field"` —— **没有任何探针被写成结论**。

## 6. 明确的负结果与未解项(不得删改)

1. `table_9` 的 **header 13 字节切分不能由数据自证**:header 11..15 都能同样闭合(候选)。
2. `table_9` 的 8 vs 9 字节 footer 切分**不能由数据区分**:末行 marker 字节正好是 9 字节读法的 `count0` 首字节
   (同一字节);但 9 字节读法铺法为 0,故交付 8。此点如实记录,不当作"已解"。
3. 允许 row_id 取 0 时 server 有 **362** 条宽解;全部集中在 row 0 的 0 值诱饵族。放宽递增则 client 6 / server 24 条。
4. `table_extra_9` **块内文法未解**(仅定位 ordinal+name 前缀);server 有 2 处块内歧义(4 条解)。
5. `table_extra_9` **无独立 footer**,末块直达载荷末尾。
6. `table_extra_9` **不适用** t9 identity 判定式(4 变体全 0,row 1 即死)。
7. `table_extra_10.dat` 两档均缺失。

## 7. 边界与合规

- 未读 `editor.exe` / IDA / `fm.i64`;未追 reader、未记 VA;未命名语义字段;未做 target ordinal join;未晋 L3。
- 未启动游戏/编辑器/IDA;未联网;未读写 `Z:`(脚本对 `Z:` 有硬拒绝路径)。
- 未改 `scratch/t49/`、`scratch/t37/`、`scratch/t47/` 任何文件;t47 只被读取并用其 archive 记录做 anchors 对照。
- 只写 `scratch/t50/` 与 `scripts/t50_*.py`。

## 8. 复现

```
py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --help
py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --selftest        # 合成 payload,无归档访问
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --build
py -V:3.12 -I -B scratch/t50/out/verify.py --selftest
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t50/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py                              # 7/7
```

`verify.py` **不 import** 任何 builder、也不 import t49;它自行重解归档、重算闭合、重跑 identity 判定式,
并与交付 JSON 逐项对比(15 组检查)。
