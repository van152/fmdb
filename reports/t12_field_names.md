# FM24 字段槽位命名台账 (t12 版)

**132/240** 槽已命名字段(占 55.0%),**schema 违规 0**。

本表把 `editor.exe` 的 4CC 属性派发链与 `.dat` 行读取器的槽偏移连起来,得到「字段名 → 行内偏移」的映射。
名字来自 exe 的分发码,偏移来自 reader 指令流,两者必须同偏移才成立。

## 口径与证据等级

| confidence | 槽数 | 含义 |
|---|---:|---|
| `unresolved` | 108 | 未解析 |
| `chain_unique` | 68 | L3 链内唯一(分发链内该偏移只有这一个码) |
| `readpair` | 37 | L3 双侧指令直证(4CC getter 与 reader 槽同偏移) |
| `chain_ambiguous` | 9 |  |
| `ref_only` | 8 | L3 引用字段(值域与行数据双证) |
| `full_shape_unique` | 5 | L3 形态完整唯一(五类形态穷举后唯一) |
| `ref_pair` | 3 | L3 引用字段(取指针+空检查, 宽度取 reader) |
| `schema_fixed` | 2 | L3+约束(链内多码, 由 schema 字段集合定为唯一合法者) |

`unresolved` 不等于空字段,只表示当前证据不足(无 4CC 窄访问 / schema 多义 / 槽为打包字节)。

### 已复核撤回的命名

| type | 档 | 槽 | 撤回字段 | 理由 |
|---:|---|---:|---|---|
| 23 | client | 0 | `SNsn` | t23 row+0 在 278 行里全为 0; SNsn 的 schema 类型是 string, 而 reader 槽仅 1 字节; t11 已据数据侧证否并降级, t12 的单射唯一性不足以推翻数据 |
| 23 | server | 0 | `SNsn` | 同上(client/server 同槽): 278 行全 0, 字符串型字段不可能落在 1 字节槽 |


## 逐实体覆盖

| type | schema 实体 | 槽数 | 已命名 | 覆盖 |
|---:|---|---:|---:|---:|
| 2 | city | 18 | 12 | 67% |
| 6 | injury | 24 | 18 | 75% |
| 19 | club | 17 | 12 | 71% |
| 21 | stadium | 19 | 16 | 84% |
| 22 | club | 19 | 17 | 89% |
| 23 | stage name | 2 | 0 | 0% |
| 30 | player | 9 | 6 | 67% |
| 31 | club | 3 | 0 | 0% |
| 34 | club | 11 | 5 | 45% |
| 35 | club | 4 | 0 | 0% |
| 37 | club | 14 | 11 | 79% |
| 42 | club | 5 | 0 | 0% |
| 43 | club | 6 | 3 | 50% |
| 46 | club | 5 | 0 | 0% |
| 47 | local region | 18 | 2 | 11% |
| 49 | person | 9 | 7 | 78% |
| 50 | club | 4 | 0 | 0% |
| 51 | nation | 3 | 0 | 0% |
| 58 | person | 9 | 4 | 44% |
| 60 | nation | 3 | 0 | 0% |
| 61 | None | 3 | 0 | 0% |
| 62 | club | 11 | 7 | 64% |
| 63 | None | 3 | 0 | 0% |
| 64 | team kit | 4 | 0 | 0% |
| 66 | club | 5 | 3 | 60% |
| 70 | club | 12 | 9 | 75% |

## 已命名字段全表

| type | 实体 | 档 | row_off | w | field | 证据 |
|---:|---|---|---:|---:|---|---|
| 2 | city | client | 1 | 8 | `Clat+Clon` | readpair 0xe55152 |
| 2 | city | client | 9 | 1 | `Catt` | readpair 0xe55219 |
| 2 | city | client | 10 | 4 | `Cnti` | ref_only 0xe55187 |
| 2 | city | client | 14 | 4 | `Cwea` | ref_only 0xe55193 |
| 2 | city | client | 21 | 4 | `Clgi` | ref_only 0xe5515e |
| 2 | city | client | 25 | 4 | `Clri` | ref_only 0xe550a3 |
| 2 | city | server | 1 | 8 | `Clat+Clon` | readpair 0xe55152 |
| 2 | city | server | 9 | 1 | `Catt` | readpair 0xe55219 |
| 2 | city | server | 10 | 4 | `Cnti` | ref_only 0xe55187 |
| 2 | city | server | 14 | 4 | `Cwea` | ref_only 0xe55193 |
| 2 | city | server | 21 | 4 | `Clgi` | ref_only 0xe5515e |
| 2 | city | server | 25 | 4 | `Clri` | ref_only 0xe550a3 |
| 6 | injury | client | 0 | 1 | `icla` | readpair 0x158101b |
| 6 | injury | client | 1 | 1 | `iscl` | readpair 0x1581033 |
| 6 | injury | server | 0 | 1 | `icla` | readpair 0x158101b |
| 6 | injury | server | 1 | 1 | `iscl` | readpair 0x1581033 |
| 6 | injury | server | 3 | 2 | `Imnd` | readpair 0x1580f01 |
| 6 | injury | server | 5 | 2 | `Iexd` | readpair 0x1580c93 |
| 6 | injury | server | 7 | 1 | `Iiar` | readpair 0x1580cab |
| 6 | injury | server | 8 | 1 | `Irec` | readpair 0x1580dc9 |
| 6 | injury | server | 13 | 4 | `Iocr` | readpair 0x1580dbd |
| 6 | injury | server | 17 | 1 | `Imip` | readpair 0x1580ef5 |
| 6 | injury | server | 18 | 2 | `Icau` | readpair 0x1580d46 |
| 6 | injury | server | 20 | 1 | `Iagr` | readpair 0x15810aa |
| 6 | injury | server | 21 | 1 | `Icms` | readpair 0x1580fa4 |
| 6 | injury | server | 22 | 1 | `Icon` | readpair 0x1580fb0 |
| 6 | injury | server | 23 | 1 | `inSr` | readpair 0x1581027 |
| 6 | injury | server | 24 | 1 | `Igpr` | readpair 0x1580c9f |
| 6 | injury | server | 25 | 1 | `Icdp` | readpair 0x1580f98 |
| 6 | injury | server | 26 | 1 | `Ibin+Ibis+Ibph+Ibsp+Ibpg` | readpair 0x1580e6c |
| 19 | club | client | 8 | 4 | `Slea` | chain_unique 0x15386ff |
| 19 | club | client | 12 | 4 | `Ssta` | chain_unique 0x153873f |
| 19 | club | client | 16 | 4 | `Slmd` | chain_unique 0x15387cb |
| 19 | club | client | 20 | 4 | `Scap` | chain_unique 0x153865b |
| 19 | club | client | 24 | 4 | `Sscp` | chain_unique 0x15385f7 |
| 19 | club | client | 28 | 4 | `Sceb` | chain_unique 0x1538813 |
| 19 | club | server | 8 | 4 | `Slea` | chain_unique 0x15386ff |
| 19 | club | server | 12 | 4 | `Ssta` | chain_unique 0x153873f |
| 19 | club | server | 16 | 4 | `Slmd` | chain_unique 0x15387cb |
| 19 | club | server | 20 | 4 | `Scap` | chain_unique 0x153865b |
| 19 | club | server | 24 | 4 | `Sscp` | chain_unique 0x15385f7 |
| 19 | club | server | 28 | 4 | `Sceb` | chain_unique 0x1538813 |
| 21 | stadium | client | 0 | 2 | `Spwd|SwIM` | chain_ambiguous 0x11866cf |
| 21 | stadium | client | 2 | 1 | `Spty` | readpair 0x1186603 |
| 21 | stadium | client | 3 | 1 | `Sste` | readpair 0x1186b0d |
| 21 | stadium | client | 4 | 1 | `Senv` | readpair 0x1186514 |
| 21 | stadium | client | 5 | 1 | `Sdah+Sitg+Sext` | readpair 0x118971a |
| 21 | stadium | client | 6 | 1 | `Sunt` | readpair 0x118698a |
| 21 | stadium | client | 7 | 1 | `Su21` | readpair 0x118638c |
| 21 | stadium | client | 8 | 1 | `Su19` | readpair 0x1186b19 |
| 21 | stadium | client | 9 | 1 | `Soty` | readpair 0x118679c |
| 21 | stadium | client | 11 | 2 | `Smnl` | readpair 0x118691c |
| 21 | stadium | client | 13 | 2 | `Smnw` | readpair 0x1186928 |
| 21 | stadium | client | 15 | 2 | `Smxl` | readpair 0x1186655 |
| 21 | stadium | client | 17 | 2 | `Smxw` | readpair 0x1186661 |
| 21 | stadium | client | 19 | 1 | `Sdtr` | readpair 0x11867e8 |
| 21 | stadium | client | 21 | 1 | `Sprr` | readpair 0x11868d8 |
| 21 | stadium | client | 22 | 2 | `Scov` | schema_fixed 0x118628f |
| 22 | club | server | 4 | 4 | `Sold` | ref_pair 0x1538f2d |
| 22 | club | server | 8 | 4 | `Snew` | ref_pair 0x153905b |
| 22 | club | server | 12 | 4 | `Scap` | chain_unique 0x1538fdc |
| 22 | club | server | 16 | 1 | `Styp` | chain_unique 0x1539196 |
| 22 | club | server | 17 | 4 | `Salt` | ref_pair 0x153920a |
| 22 | club | server | 21 | 1 | `Scpm` | chain_unique 0x15390f2 |
| 22 | club | server | 22 | 4 | `Sscp` | chain_unique 0x1538f39 |
| 22 | club | server | 26 | 4 | `Snxa` | chain_unique 0x1538f21 |
| 22 | club | server | 30 | 4 | `Snmn` | chain_unique 0x1539067 |
| 22 | club | server | 34 | 4 | `Snmx` | chain_unique 0x1539073 |
| 22 | club | server | 38 | 4 | `Stks` | chain_unique 0x153918a |
| 22 | club | server | 42 | 1 | `Slhm` | chain_unique 0x153910a |
| 22 | club | server | 43 | 4 | `Scam` | chain_unique 0x1538fd0 |
| 22 | club | server | 47 | 1 | `Scns` | chain_unique 0x15392cb |
| 22 | club | server | 48 | 1 | `ScTL` | chain_unique 0x1539216 |
| 22 | club | server | 49 | 1 | `ScYL` | chain_unique 0x1538fc4 |
| 22 | club | server | 50 | 4 | `Sceb` | chain_unique 0x15392bf |
| 30 | player | server | 4 | 4 | `inju` | full_shape_unique 0x1197d6f |
| 30 | player | server | 16 | 1 | `futu` | chain_unique 0x1197c81 |
| 30 | player | server | 17 | 1 | `perm` | chain_unique 0x1197d7b |
| 30 | player | server | 18 | 1 | `seve` | chain_unique 0x1197d04 |
| 30 | player | server | 19 | 1 | `side` | chain_unique 0x1197de6 |
| 30 | player | server | 20 | 1 | `pret` | chain_unique 0x1197cf8 |
| 34 | club | server | 8 | 2 | `mstn|styr` | chain_ambiguous 0x156f87d |
| 34 | club | server | 10 | 2 | `edyr` | chain_unique 0x156f941 |
| 34 | club | server | 21 | 1 | `dbrt` | chain_unique 0x156f8d2 |
| 34 | club | server | 26 | 1 | `posi` | chain_unique 0x156f913 |
| 34 | club | server | 27 | 4 | `tcop` | full_shape_unique 0x156f889 |
| 37 | club | server | 12 | 2 | `year` | chain_unique 0x119ea09 |
| 37 | club | server | 14 | 1 | `posi` | chain_unique 0x119e9f1 |
| 37 | club | server | 15 | 1 | `play` | chain_unique 0x119e8e5 |
| 37 | club | server | 16 | 1 | `wins` | chain_unique 0x119e9fd |
| 37 | club | server | 17 | 1 | `draw` | chain_unique 0x119e84d |
| 37 | club | server | 18 | 1 | `lost` | chain_unique 0x119e971 |
| 37 | club | server | 19 | 2 | `gfor` | chain_unique 0x119e965 |
| 37 | club | server | 21 | 2 | `gaga` | chain_unique 0x119e859 |
| 37 | club | server | 23 | 2 | `poin` | chain_unique 0x119e8f1 |
| 37 | club | server | 25 | 1 | `orde` | chain_unique 0x119e8d9 |
| 37 | club | server | 26 | 1 | `mxtm` | chain_unique 0x119e97d |
| 43 | club | server | 24 | 4 | `mths` | chain_unique 0x153c9ec |
| 43 | club | server | 28 | 4 | `cash|play` | chain_ambiguous 0x153c9b0 |
| 43 | club | server | 32 | 1 | `pyiv` | chain_unique 0x153c9f8 |
| 47 | local region | client | 8 | 4 | `Lwea` | full_shape_unique 0x14590e9 |
| 47 | local region | client | 17 | 4 | `Lpop` | readpair 0x1458fcd |
| 49 | person | server | 1 | 2 | `date|year` | chain_ambiguous 0x1456087 |
| 49 | person | server | 3 | 2 | `date|year` | chain_ambiguous 0x1456087 |
| 49 | person | server | 5 | 4 | `divi` | full_shape_unique 0x119e841 |
| 49 | person | server | 13 | 4 | `comp` | chain_unique 0x1456124 |
| 49 | person | server | 17 | 4 | `otea` | chain_unique 0x14561f1 |
| 49 | person | server | 21 | 1 | `plac` | chain_unique 0x145616b |
| 49 | person | server | 22 | 1 | `ajob` | chain_unique 0x1456118 |
| 58 | person | server | 0 | 4 | `divi` | full_shape_unique 0x119e841 |
| 58 | person | server | 8 | 4 | `team` | chain_unique 0x1543ebe |
| 58 | person | server | 12 | 4 | `team` | chain_unique 0x1543ebe |
| 58 | person | server | 28 | 4 | `comp` | chain_unique 0x1543cf7 |
| 62 | club | server | 0 | 1 | `Ttyp` | schema_fixed 0x119c881 |
| 62 | club | server | 13 | 4 | `Catd` | chain_unique 0x119c72a |
| 62 | club | server | 17 | 4 | `Cmxa` | chain_unique 0x119c80b |
| 62 | club | server | 21 | 4 | `Cmna` | chain_unique 0x119c7ff |
| 62 | club | server | 25 | 1 | `Twhm` | chain_unique 0x119c88d |
| 62 | club | server | 26 | 1 | `Tmhm` | chain_unique 0x119c777 |
| 62 | club | server | 27 | 1 | `tmno|tmnv` | chain_ambiguous 0x119ca0c |
| 66 | club | server | 8 | 1 | `maxa|nati|rati` | chain_ambiguous 0xea6787 |
| 66 | club | server | 9 | 1 | `maxa|mina|rati` | chain_ambiguous 0xea6787 |
| 66 | club | server | 10 | 1 | `maxa|rati` | chain_ambiguous 0xea6787 |
| 70 | club | server | 8 | 4 | `comp` | chain_unique 0x1454f8f |
| 70 | club | server | 16 | 2 | `wrcl` | chain_unique 0x1454efc |
| 70 | club | server | 18 | 2 | `styr` | chain_unique 0x1454ef0 |
| 70 | club | server | 20 | 2 | `enyr` | chain_unique 0x1454f9b |
| 70 | club | server | 22 | 1 | `type` | chain_unique 0x1454f08 |
| 70 | club | server | 23 | 1 | `levl` | chain_unique 0x1454e51 |
| 70 | club | server | 24 | 1 | `mage` | chain_unique 0x1454e5d |
| 70 | club | server | 25 | 1 | `mlen` | chain_unique 0x145501c |
| 70 | club | server | 26 | 1 | `isog` | chain_unique 0x1454e45 |

## 已知边界(必读)

- **11 张小表(约 39 槽)在 4CC 路线上不可达**: 其 object 偏移 24/28 上没有任何 4CC 候选,t61/t63 的槽偏移集合与全体候选交集为空。这不是门槛问题,是这些表不走 4CC 派发。
- **club(433 字段)未解**: 575 个码里 386 存在于 exe,190 个拿到偏移或下沉路径;但 185 个 offset 只落在 73 个不同偏移上且重度撞车(0x30 有 12 个码),并混入 `levl/venu/perc` 这类跨表同名码 —— 全局「码→偏移」对 club 无效,必须按类作用域抽取。
- **引用字段宽度取自 reader,不是访问指令**: `mov r64,[reg+OFF]` 是取指针,行里存 4B id。早期版本把这类码整批丢弃,导致 `Sold/Salt/Snew` 缺失。

## 复跑

```
py -V:3.12 -I -B scripts/t12_catalog.py
py -V:3.12 -I scratch/t12/out/verify.py
```
