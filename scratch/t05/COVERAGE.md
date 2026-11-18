# 全库解析覆盖矩阵

生成:2026-11-18 19:13

## 总览

| 指标 | 数值 |
|---|---|
| client 表边界闭合 | **20/20** |
| server 表边界闭合 | **58/59**(另有 0 张算术候选、1 张未解) |
| 已描述行内偏移(按实体去重) | **102** |
| 其中有 schema 字段码 | 43 |
| 数据库实体数 | 32(全文档 112) |
| 实体声明字段总数 | 2144 |
| 实体顶层列表字段 | 176 |
| **实体顶层标量(真正可落偏移)** | **1968** |
| 已映射实体标量预算合计 | 2190 |
| 字段映射进度(粗) | 102/1968 = 5.2% |

> 注:字段映射按实体(tid)计,client/server 同名表的行内布局可能不同;
> 表中 client/server 两栏的偏移数是同一实体结论的复用,不是两套独立成果。

## client 20 表

| tid | entity | mode | count | 边界 | 上游 | 偏移 | 命名字段 | 标量预算 | 等式 |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| 0 | award | mixed | 3545 | closed | closed | 9 | 0 | 37 | 14+3545*77+8=272987 |
| 2 | city | straight-line | ? | closed | closed | 12 | 0 | 15 | 14+56293*43+8=2420621 |
| 3 | club | mixed | ? | closed | closed | 19 | 14 | 386 | 84,259 行全封口(5B block + 3 特例行) |
| 5 | continent | count-loop | 7 | closed | closed | 9 | 0 | 15 | 14+7*34+8=260 |
| 6 | injury | straight-line | 115 | closed | closed | 5 | 0 | 27 | 14+115*16+8=1862 |
| 7 | media source | count-loop | 208 | closed | closed | 0 | 0 | 16 | 208 行变长全封口 |
| 8 | language | straight-line | 126 | closed | closed | 5 | 0 | 12 | 126 行语言名全封口 |
| 9 | nation (name/key companion) | mixed | 251 | closed | closed | 0 | 0 | - | 251 行 sentinel+duni 尾锚全封口 |
| 10 | nation | count-loop | 251 | closed | open | 7 | 7 | 317 | 14+24710+8=24732 (4 段计数循环) |
| 18 | city-associated secondary-name data | straight-line | 1567 | closed | closed | 10 | 0 | - | 1567 行双字符串全封口 |
| 19 | regi | straight-line | 28 | closed | closed | 9 | 7 | - | 14+28*45+8=1282 |
| 21 | stadium | straight-line | ? | closed | closed | 0 | 0 | 58 | 14+48413*38+8=1839716 |
| 22 | ? | straight-line | 449 | closed | closed | 0 | 0 | - | 14+449*13+8=5859 |
| 23 | stgn | straight-line | 278 | closed | closed | 3 | 0 | - | 14+278*14+8=3914 |
| 25 | competition | straight-line | ? | closed | closed | 0 | 0 | 240 | comp 行边界 |
| 27 | weather profile | straight-line | 334 | closed | closed | 0 | 0 | - | 334 行变长全封口 |
| 35 | ? | unclear | 890 | closed | closed | 0 | 0 | - | 14+890*15+8=13372 |
| 41 | currency | straight-line | 173 | closed | closed | 6 | 0 | 7 | 173 行变长全封口 |
| 47 | lcrg | mixed | 2488 | closed | closed | 8 | 0 | - | 14+Σ(41+5k)+8=109505 (2488行, rdui/duni |
| 56 | agrm | unclear | 6 | closed | closed | 0 | 0 | - | 14+6*13+8=100 |

## server 59 表

| tid | entity | model | count | 边界 | 上游 | 偏移 | 命名字段 | 标量预算 |
|---:|---|---|---:|---|---|---:|---:|---:|
| 0 | ? | mixed | 3545 | closed | closed | 9 | 0 | - |
| 2 | city | straight-line | 56293 | closed | closed | 12 | 0 | 15 |
| 3 | club | mixed | 84259 | closed | closed | 19 | 14 | 386 |
| 5 | ? | count-loop | 7 | closed | closed | 9 | 0 | - |
| 6 | ? | straight-line | 115 | closed | closed | 5 | 0 | - |
| 7 | media_source | count-loop | 208 | closed | closed | 0 | 0 | - |
| 8 | language | straight-line | 126 | closed | closed | 5 | 0 | 12 |
| 9 | ? | mixed | 251 | closed | closed | 0 | 0 | - |
| 10 | nation | count-loop | 251 | closed | closed | 7 | 7 | 317 |
| 12 | ? | straight-line | 28597 | closed | closed | 0 | 0 | - |
| 18 | ? | straight-line | 1567 | closed | closed | 10 | 0 | - |
| 19 | ? | straight-line | 28 | closed | closed | 9 | 7 | - |
| 21 | stadium | straight-line | 48413 | closed | closed | 0 | 0 | 58 |
| 22 | ? | straight-line | 449 | closed | closed | 0 | 0 | - |
| 23 | ? | straight-line | 278 | closed | closed | 3 | 0 | - |
| 24 | team | mixed | 84507 | open | open | 0 | 0 | 25 |
| 25 | competition | straight-line | 7047 | closed | closed | 0 | 0 | 240 |
| 26 | ? | straight-line | 90128 | closed | closed | 0 | 0 | - |
| 27 | ? | straight-line | 334 | closed | closed | 0 | 0 | - |
| 29 | ? | straight-line | 13278 | closed | closed | 0 | 0 | - |
| 30 | ? | straight-line | 72473 | closed | closed | 0 | 0 | - |
| 31 | ? | straight-line | 37283 | closed | closed | 0 | 0 | - |
| 32 | ? | count-loop | 315 | closed | closed | 0 | 0 | - |
| 33 | ? | straight-line | 32409 | closed | closed | 0 | 0 | - |
| 34 | ? | straight-line | 7115 | closed | closed | 0 | 0 | - |
| 35 | ? | unclear | 890 | closed | closed | 0 | 0 | - |
| 36 | ? | count-loop | 6535 | closed | closed | 0 | 0 | - |
| 37 | ? | straight-line | 465712 | closed | closed | 0 | 0 | - |
| 38 | ? | straight-line | 5241 | closed | closed | 0 | 0 | - |
| 39 | ? | mixed | 117 | closed | closed | 0 | 0 | - |
| 41 | currency | straight-line | 173 | closed | closed | 6 | 0 | 7 |
| 42 | ? | straight-line | 17721 | closed | closed | 0 | 0 | - |
| 43 | ? | straight-line | 535 | closed | closed | 0 | 0 | - |
| 45 | ? | straight-line | 84477 | closed | closed | 0 | 0 | - |
| 46 | ? | straight-line | 7 | closed | closed | 0 | 0 | - |
| 47 | ? | mixed | 2488 | closed | closed | 8 | 0 | - |
| 48 | ? | straight-line | 5210 | closed | closed | 0 | 0 | - |
| 49 | ? | straight-line | 792149 | closed | closed | 0 | 0 | - |
| 50 | ? | straight-line | 45 | closed | closed | 0 | 0 | - |
| 51 | ? | straight-line | 59 | closed | closed | 0 | 0 | - |
| 52 | ? | straight-line | ? | closed | closed | 0 | 0 | - |
| 56 | ? | unclear | 6 | closed | closed | 0 | 0 | - |
| 57 | ? | straight-line | ? | closed | closed | 0 | 0 | - |
| 58 | ? | straight-line | 8 | closed | closed | 0 | 0 | - |
| 59 | ? | count-loop | 9079 | closed | closed | 0 | 0 | - |
| 60 | ? | straight-line | 59 | closed | closed | 0 | 0 | - |
| 61 | ? | straight-line | 16 | closed | closed | 0 | 0 | - |
| 62 | ? | straight-line | 37214 | closed | closed | 0 | 0 | - |
| 63 | ? | straight-line | 2 | closed | closed | 0 | 0 | - |
| 64 | ? | straight-line | 6946 | closed | closed | 0 | 0 | - |
| 65 | ? | straight-line | 1417 | closed | closed | 0 | 0 | - |
| 66 | ? | straight-line | 753 | closed | closed | 0 | 0 | - |
| 67 | ? | straight-line | 6826 | closed | closed | 0 | 0 | - |
| 68 | ? | straight-line | 138 | closed | closed | 0 | 0 | - |
| 69 | ? | straight-line | 230 | closed | closed | 0 | 0 | - |
| 70 | ? | straight-line | 10075 | closed | closed | 0 | 0 | - |
| 71 | ? | mixed | 616665 | closed | closed | 0 | 0 | - |
| 72 | ? | count-loop | 138 | closed | closed | 0 | 0 | - |
| 73 | ? | straight-line | 1 | closed | closed | 0 | 0 | - |

## 未闭合清单

- server table_24: **open**(上游 open) 未建立；无法给出最后一行结束位置 + 8 == payload 长度的精确等式。
