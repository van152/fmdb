# t05 字段对齐设计笔记(指挥官整理,2026-11-18)

## 1. 精确口径(机读:`scratch/t05/schema_inventory.json`)

32 个数据库实体:**声明 2,144 字段 / 顶层 2,144 / 其中标量 1,968 / 列表 176 / 列表子字段 634**。

| 实体 | code | 声明 | 标量 | 列表 | 行宽(B) | 字节/标量 |
|---|---|---:|---:|---:|---:|---:|
| club | club | 433 | **386** | 47 | ~82(5B block) | **0.21** |
| nation | nati | 346 | 317 | 29 | 50–1199 变长 | — |
| comp | comp | 255 | 240 | 15 | 变长 | — |
| person | pers | 271 | 236 | 35 | 68 载荷 | 0.29 |
| player | play | 179 | 171 | 8 | 68 载荷(共用) | — |
| non player | nnpl | 129 | 126 | 3 | 68 载荷(共用) | — |
| weather | weat | 94 | 94 | 0 | 99B 数值中段 | ~1.05 |
| stadium | stad | 60 | 58 | 2 | 38(client)/181(server) | 0.66 / 3.12 |
| award | awar | 38 | 37 | 1 | 77 | 2.08 |
| injury | inju | 27 | 27 | 0 | 16 | **0.59** |
| team | team | 25 | 25 | 0 | ~104 变长 | — |
| city | city | 15 | 15 | 0 | 43 | 2.87 |
| language | lang | 12 | 12 | 0 | 变长(名+30B) | — |

> **修正**:t05b 任务书里写 club `top_level_scalars: 109` 是错的,正确是 **386**(433 减 47 个列表)。

## 2. 三条结构性结论(会改变对齐器的设计)

### 2.1 字节/标量 < 1 的表,必然有位打包
`injury 0.59`、`stadium client 0.66`、`person 0.29`、`club 0.21` —— 标量数超过可用字节数,
说明这些表的布尔/枚举被压成**位域**,或字段以"存在位图 + 稀疏值"编码。

### 2.2 award 的 37 个标量在 77B 里放不下 → 存在 optional 跳过
按最小线宽硬算:award 37 标量 = duni(8) + rdui(4) + 22 个 4B/3B/2B/1B 混合,
在还没数到 15 个 optional 字段时就已经超过 64B 可用区。
→ **optional 字段不是恒占位**,而是"有值才出现"(或由位图控制)。
这解释了为什么纯"schema 顺序 × 固定宽度累加"必然失败,也解释了 exe reader 里的分支。

### 2.3 列表字段的 0 宽假设成立
176 个列表字段不占行内字节,只有计数/段偏移。行宽公式应写成:
```
row_len = Σ(标量线宽) + Σ(列表段的项数 × 项宽) + 身份尾
```

## 3. 对齐器要吃的约束(给 t05b / 后续轮次的规格)

1. **保序**:schema 字段顺序 = reader 传输顺序(E20 已验)。列表子字段不参与主序列。
2. **线宽候选**:见 `schema_inventory.json` 的 `type_width_candidates`。
3. **optional 可跳过**:每个 optional 字段允许"0 宽"这一候选(表示该行未出现)。
   非 optional 字段必须有宽度。
4. **总宽 == 行宽**(逐行验证,不是全表平均)。
5. **数据合法性**:
   - 引用型值 < 目标表行数(或 == 0xFFFFFFFF);
   - enum 值 < 枚举基数;colour 高位 alpha 常 0 或 0xFF;
   - date 落在 1800–2100 对应编码;real 为有限数且在合理量级。
6. **求解**:DP/回溯在"保序 + 候选宽度 + optional 跳过"下搜索,优先
   `Σ|候选宽度 - 期望宽度|` 最小的解;再用夹具(award/city/stadium/injury/language)校准。

## 4. 已知夹具真值

| 夹具 | 行宽 | 已验锚点 | 校验来源 |
|---|---|---|---|
| award | 77 定长 | `rdui u32@64 == row index`,`duni@68` 两半相等,@76 marker=0 | 上游 b46 + 本仓 dump |
| city | 43 定长 | `Clat f32@1`、`Clon f32@5`、`Cnti u8@10`、`rdui@30`、`duni@34` | 上游 b47 |
| stadium | 38(client)/181(server) | `Scti u32@3`、`Slat f32@17`、`Slon f32@21`、`rdui@25`、`duni@29` | 上游 b47 |
| injury | 16 定长 | `rdui@3`、`duni@7` | 上游 b46 |
| language | 变长(名 + 30B 后缀) | 后缀 `u32@+17` == 0-based 行号 | 上游 b46 |
| lcrg | 41+5k 变长 | `rdui@len-13 == row index`、`duni@len-9/@len-5` 相等、@len-1=0 | **本仓 scripts/t05_lcrg.py 双约束闭合** |
| club | 84,259 行闭合 | `Cccn u32@+8`(L3 字节链 8/8) | 本仓 E36 |

## 5. 边界现状(本仓口径)

- client 20/20 闭合(含 table_47 双约束攻克)
- server:3 闭合 + 36 算术候选(待 t05a 验身份)+ 18 未解
- 可 dump 表:46 定长 + 1 变长(lcrg)= 47(`scripts/fm24_dump.py --list`)

## 6. 工具

- `scripts/t05_schema.py` → `schema_inventory.json`(字段序列 + 类型宽度候选)
- `scripts/fm24_dump.py` → 按边界导出行(JSON/CSV),闭合不符即报错
- `scripts/t05_lcrg.py` → table_47 双约束闭合复现 + `--selftest`
- `scripts/t05_coverage.py` → 全库进度矩阵 `scratch/t05/COVERAGE.md`
