# 阶段二：表身份总清单

合并 E22 三向表、E56 十二表裁决、t13 空白表锚点。共 **45** 张已归纳表，resolved 29 / candidate 3 / negative 11 / empty 2。

## 已定表

| type | 实体 | 状态 | 等级 | 来源 | 角色/证据摘要 |
|---:|---|---|---|---|---|
| 0 | `awar` | resolved | A | E22三向表 | award.xml#awar / t01c/property_map |
| 1 | `pers` | resolved | A | E22三向表 | person.xml#pers / t01c/property_map |
| 2 | `city` | resolved | A | E22三向表 | city.xml#city / t01c/property_map |
| 3 | `club` | resolved | A | E22三向表 | club.xml#club / t01c/property_map |
| 5 | `cont` | resolved | A | E22三向表 | continent.xml#cont / t01c/property_map |
| 6 | `inju` | resolved | A | E22三向表 | injury.xml#inju / t01c/property_map |
| 7 | `mdso` | resolved | A | E22三向表 | media source.xml#mdso / t01c/property_map |
| 8 | `lang` | resolved | A | E22三向表 | language.xml#lang / t01c/property_map |
| 9 | `nati` | resolved | A | E22三向表 | nation.xml#nati / t01c/property_map |
| 10 | `nati` | resolved | A | E22三向表 | nation.xml#nati / E21 |
| 12 | `awar` | resolved | A | t13锚点 | type 12 reader 的 object_off=128 与 award 专属字段 AHp1 对齐；chain_0106 的读取指令直接访问该成员，AHp1 在 sche |
| 18 | `drbr` | resolved | A | E22三向表 | derby.xml#drbr / t01c/property_map |
| 19 | `regi` | resolved | A | E22三向表 | region.xml#regi / t01c/property_map |
| 21 | `stad` | resolved | A | E22三向表 | stadium.xml#stad / t01c/property_map |
| 22 | `club` | resolved | A | E56裁决 | club 的球场/迁建属性集 / Salt=Alternative Stadium(df=1,club) / 449 行, 不是 stadium 主表(48413); 字段语义 |
| 23 | `stgn` | resolved | A | E22三向表 | stage name.xml#stgn / t01c/property_map |
| 24 | `team` | resolved | A | E22三向表 | team.xml#team / t01c/property_map |
| 25 | `comp` | resolved | A | E22三向表 | comp.xml#comp / E20 |
| 26 | `None` | negative | - | t13锚点 | 负结果：scratch/t05/reader_widths.json 中 type 26 的 seq=[12]、obj_seq=[null]，没有可关联到 schema 字段的 |
| 27 | `weat` | resolved | A | E22三向表 | weather.xml#weat / t01c/property_map |
| 29 | `None` | negative | - | t13锚点 | 负结果：type 29 的 reader_widths 只有一个 12-byte call 且无 object_off；邻近 player 码簇仅是位置候选，不能按邻近投票定案 |
| 30 | `player` | resolved | A | E56裁决 | 球员伤病/未来状态记录 / futu=Future(df=1,player) / 72473 行 >> injury 主表 115, 故是 player 侧的伤病实例/状态表而 |
| 31 | `None` | negative | negative | E56裁决 | 零字段表 / t11 投给 club 但无任何命名字段、无 A 类证据; 37283 行与 club 主表 84259 不符, 不认可 |
| 32 | `None` | negative | - | t13锚点 | 负结果：type 32 为变长 count-loop 行，reader_widths 的 obj_seq=[null]；邻近链中没有能与本 reader 直接关联的唯一 df= |
| 33 | `club` | resolved | A | t13锚点 | type 33 reader 的 object_off=68 与 schema 中仅属于 club 的 CMWE（Maximum Wage Allowed）成员对齐；reade |
| 34 | `club` | candidate | B | E56裁决 | 俱乐部赛事历史(起止年/对手/结果) / tcop=Opposition(df=2,club+nation) / 6 个码全部 club+nation 共有, 无 df=1 码 |
| 35 | `dscr` | resolved | A | E22三向表 | description.xml#dscr / t01c/property_map |
| 36 | `None` | negative | - | t13锚点 | 负结果：type 36 的行边界已闭合，但 reader_widths 只有 object_off 24、64 两个无语义的 4-byte 访问；周边 injury/playe |
| 37 | `club` | resolved | A | E56裁决 | 俱乐部战绩/积分榜记录 / draw=Games Drawn(df=1,club) / 465712 行 = 俱乐部×赛季/赛事条目; 不是 club 主表(84259) |
| 38 | `None` | negative | - | t13锚点 | 负结果：type 38 的 7 个 reader object_off 只能给出结构位置；最近链候选码经 schema_inventory 去重后均不是唯一实体码，值域也未形成 |
| 39 | `None` | negative | - | t13锚点 | 负结果：117 行与 injury 的 115 行接近但不相等；type 39 的混合 reader 有 null object_off，邻近链接的代码簇未建立到本表的唯一 s |
| 41 | `curr` | resolved | A | E22三向表 | currency.xml#curr / t01c/property_map |
| 42 | `None` | negative | negative | E56裁决 | 零字段表 / t11 投给 club 但零字段; 17721 行无独立锚点, 不认可 |
| 43 | `club` | candidate | B | E56裁决 | 转会付款分期 / mths=Number Months(df=1,club) / 535 行; 两个唯一码均为财务分期语义, 但与 club 主表的连接仅有码证据, 无行数独立 |
| 45 | `pers` | resolved | A | t13锚点 | type 45 reader 的 object_off=86 与 person 专属 schema 字段 gols（Goals）对齐；chain_0153 的读取指令访问 [r |
| 46 | `None` | negative | negative | E56裁决 | 零字段表 / 7 行与 continent(7) 相同但无字段码; 行数吻合只是候选, 不足以定案 |
| 47 | `lcrg` | resolved | A | E22三向表 | local region.xml#lcrg / t01c/property_map |
| 48 | `pers` | resolved | A | t13锚点 | type 48 reader 序列也明确含 object_off=86；其链内 gols 读取指令映射到 schema 中 df=1 的 person 字段。该结论逐表核验，不 |
| 49 | `person` | resolved | A | E56裁决 | 人员任职/对阵履历 / ajob=Job(df=1,person) / 792149 行; 3 个唯一码全属 person, 是典型履历子表; t11 投给 club 系投票污 |
| 50 | `None` | negative | negative | E56裁决 | 零字段表 / 45 行, 零字段; t11 投 club 无证据 |
| 51 | `None` | negative | negative | E56裁决 | 零字段表 / 59 行, 零字段; t11 投 nation 无证据 |
| 52 | `None` | empty | - | t13锚点 |  |
| 56 | `agrm` | resolved | A | E22三向表 | agreement.xml#agrm / t01c/property_map |
| 57 | `None` | empty | - | t13锚点 |  |
| 58 | `None` | candidate | candidate | E56裁决 | 零决定性字段表 / 8 行; 只有 comp/divi/team 三个跨表码(df>=2), 无唯一码; person/club 皆可能, 不定案 |

## 不在 .dat archive 的表

以下 **14** 张 table_type 属于工厂专属 / null-return（E24 负结果），存档里无对应表，保留原始负结果，不改写为“未解”：

`4`, `11`, `13`, `14`, `15`, `16`, `17`, `20`, `28`, `40`, `44`, `53`, `54`, `55`

## 指挥官独立复核

- 静态锚反汇编：4 个 A 锚的 file_off 指令逐条反汇编 + 4 个 cmp 站点立即数 big-endian 解码, 8/8 全一致
- schema df：AHp1=award/CMWE=club/gols=person, 全 df=1
- 簇级证据补强：t[45, 48] obj84=apps/gams, obj86=gols, obj88=fsgs/fsgt/ogls 三连续槽全为person进球统计,w=2自洽; t33 chain_0145 混合(club47:person10), 但C前缀专属码簇(CMWE/Ctbu/Crmb/Csry/Ctrl/Cpll/Csrp/Ctbt/Ccfa)占reader 9/18偏移, A级维持

### 保留的边界

- t12 的 28,597 行与已知 award 表 3,545 行差 706%, 类身份有A锚但行集不同, resolved仅指实体类别
- t45/t48 共用 reader 0x1543730, chain_0153 同时被 t08 配给 t58(score5); 属共用getter区, 不构成冲突但需标注
- t13 报的 4 resolved 全是静态L3; 6 negative 保留原样不硬凑
