# 阶段二：表身份总清单

合并 E22 三向表、E56 十二表裁决、t13 空白表锚点。共 **45** 张已归纳表，resolved 29 / candidate 3 / negative 11 / empty 2。

## 已定表

| type | 实体 | 状态 | 等级 | 来源 | 角色/证据摘要 |
|---:|---|---|---|---|---|
| 0 | `awar` | resolved | A | E22三向表 | award.xml#awar |
| 1 | `pers` | resolved | A | E22三向表 | person.xml#pers |
| 2 | `city` | resolved | A | E22三向表 | city.xml#city |
| 3 | `club` | resolved | A | E22三向表 | club.xml#club |
| 5 | `cont` | resolved | A | E22三向表 | continent.xml#cont |
| 6 | `inju` | resolved | A | E22三向表 | injury.xml#inju |
| 7 | `mdso` | resolved | A | E22三向表 | media source.xml#mdso |
| 8 | `lang` | resolved | A | E22三向表 | language.xml#lang |
| 9 | `nati` | resolved | A | E22三向表 | nation.xml#nati |
| 10 | `nati` | resolved | A | E22三向表 | nation.xml#nati |
| 12 | `awar` | resolved | A | t13锚点 | type 12 reader 的 object_off=128 与 award 专属字段 AHp1 对齐；chain_0106 的读取指令直接访问该成员，AHp1 在 sche |
| 18 | `drbr` | resolved | A | E22三向表 | derby.xml#drbr |
| 19 | `regi` | resolved | A | E22三向表 | region.xml#regi |
| 21 | `stad` | resolved | A | E22三向表 | stadium.xml#stad |
| 22 | `club` | resolved | A | E56裁决 | club 的球场/迁建属性集 |
| 23 | `stgn` | resolved | A | E22三向表 | stage name.xml#stgn |
| 24 | `team` | resolved | A | E22三向表 | team.xml#team |
| 25 | `comp` | resolved | A | E22三向表 | comp.xml#comp |
| 26 | `None` | negative | - | t13锚点 | 负结果：scratch/t05/reader_widths.json 中 type 26 的 seq=[12]、obj_seq=[null]，没有可关联到 schema 字段的 |
| 27 | `weat` | resolved | A | E22三向表 | weather.xml#weat |
| 29 | `None` | negative | - | t13锚点 | 负结果：type 29 的 reader_widths 只有一个 12-byte call 且无 object_off；邻近 player 码簇仅是位置候选，不能按邻近投票定案 |
| 30 | `player` | resolved | A | E56裁决 | 球员伤病/未来状态记录 |
| 31 | `None` | negative | negative | E56裁决 | 零字段表 |
| 32 | `None` | negative | - | t13锚点 | 负结果：type 32 为变长 count-loop 行，reader_widths 的 obj_seq=[null]；邻近链中没有能与本 reader 直接关联的唯一 df= |
| 33 | `club` | resolved | A | t13锚点 | type 33 reader 的 object_off=68 与 schema 中仅属于 club 的 CMWE（Maximum Wage Allowed）成员对齐；reade |
| 34 | `club` | candidate | B | E56裁决 | 俱乐部赛事历史(起止年/对手/结果) |
| 35 | `dscr` | resolved | A | E22三向表 | description.xml#dscr |
| 36 | `None` | negative | - | t13锚点 | 负结果：type 36 的行边界已闭合，但 reader_widths 只有 object_off 24、64 两个无语义的 4-byte 访问；周边 injury/playe |
| 37 | `club` | resolved | A | E56裁决 | 俱乐部战绩/积分榜记录 |
| 38 | `None` | negative | - | t13锚点 | 负结果：type 38 的 7 个 reader object_off 只能给出结构位置；最近链候选码经 schema_inventory 去重后均不是唯一实体码，值域也未形成 |
| 39 | `None` | negative | - | t13锚点 | 负结果：117 行与 injury 的 115 行接近但不相等；type 39 的混合 reader 有 null object_off，邻近链接的代码簇未建立到本表的唯一 s |
| 41 | `curr` | resolved | A | E22三向表 | currency.xml#curr |
| 42 | `None` | negative | negative | E56裁决 | 零字段表 |
| 43 | `club` | candidate | B | E56裁决 | 转会付款分期 |
| 45 | `pers` | resolved | A | t13锚点 | type 45 reader 的 object_off=86 与 person 专属 schema 字段 gols（Goals）对齐；chain_0153 的读取指令访问 [r |
| 46 | `None` | negative | negative | E56裁决 | 零字段表 |
| 47 | `lcrg` | resolved | A | E22三向表 | local region.xml#lcrg |
| 48 | `pers` | resolved | A | t13锚点 | type 48 reader 序列也明确含 object_off=86；其链内 gols 读取指令映射到 schema 中 df=1 的 person 字段。该结论逐表核验，不 |
| 49 | `person` | resolved | A | E56裁决 | 人员任职/对阵履历 |
| 50 | `None` | negative | negative | E56裁决 | 零字段表 |
| 51 | `None` | negative | negative | E56裁决 | 零字段表 |
| 52 | `None` | empty | - | t13锚点 |  |
| 56 | `agrm` | resolved | A | E22三向表 | agreement.xml#agrm |
| 57 | `None` | empty | - | t13锚点 |  |
| 58 | `None` | candidate | candidate | E56裁决 | 零决定性字段表 |

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
