# stage2 三向表(table_type ↔ entity ↔ registration_fn)+ 序列化模式

| type | entity | tag | fields | vtable(s) | regfn block off | mode | 来源 |
|---|---|---|---:|---|---|---|---|
| 0 | award.xml#awar | awar | 38 | 0x187ae20 | 0xe490b0 | mixed | t01c/property_map+t01h/E23+t01e/E17 |
| 1 | person.xml#pers | pers | 271 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 2 | city.xml#city | city | 15 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 3 | club.xml#club | club | 433 | 0x187c300, 0x18bf1f0 | 0xe87d74, 0xe87d74 | mixed | t01c/property_map+t01h/E23+t01e/E17 |
| 5 | continent.xml#cont | cont | 16 | - | - | count-loop | t01c/property_map+t01h/E23 |
| 6 | injury.xml#inju | inju | 27 | 0x1881d30 | 0x1580560 | straight-line | t01c/property_map+t01h/E23+t01e/E17 |
| 7 | media source.xml#mdso | mdso | 22 | 0x18bd300 | 0x1546900 | count-loop | t01c/property_map+t01h/E23+t01e/E17 |
| 8 | language.xml#lang | lang | 12 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 9 | nation.xml#nati | nati | 346 | 0x1888ed0, 0x188db40 | 0x11eff90, 0x11eff90 | mixed | t01c/property_map+t01h/E23+t01e/E17 |
| 10 | nation.xml#nati | nati | 346 | 0x1888ed0, 0x188db40 | 0x11eff90, 0x11eff90 | count-loop | E21+t01c/property_map+t01g+t01h/E23 |
| 18 | derby.xml#drbr | drbr | 22 | 0x1886870 | 0xffcc50 | straight-line | t01c/property_map+t01h/E23+t01e/E17 |
| 19 | region.xml#regi | regi | 6 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 21 | stadium.xml#stad | stad | 60 | 0x188d1d0 | 0x1185040 | straight-line | t01c/property_map+t01h/E23+t01e/E17 |
| 23 | stage name.xml#stgn | stgn | 8 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 24 | team.xml#team | team | 25 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 25 | comp.xml#comp | comp | 255 | 0x187d2b0 | 0xebf060 | straight-line | E20+t01c/property_map+t01f+t01h/E23 |
| 27 | weather.xml#weat | weat | 94 | 0x18823e0 | 0x158cad0 | straight-line | t01c/property_map+t01h/E23+t01e/E17 |
| 35 | description.xml#dscr | dscr | 6 | - | - | unclear | t01c/property_map+t01h/E23 |
| 41 | currency.xml#curr | curr | 7 | - | - | straight-line | t01c/property_map+t01h/E23 |
| 47 | local region.xml#lcrg | lcrg | 11 | - | - | mixed | t01c/property_map+t01h/E23 |
| 56 | agreement.xml#agrm | agrm | 8 | - | - | unclear | t01c/property_map+t01h/E23 |

无属性映射的表型(0..58):[4, 11, 12, 13, 14, 15, 16, 17, 20, 22, 26, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58]

t01e 已映射但 property_map 缺的 tag:['agen', 'jour', 'offc']

模式分布(E23,全 74 项):46 straight-line / 7 count-loop / 7 mixed / 14 unclear;11 null-return 型无专属工厂
stage-2 排序:straight-line 已映射实体直接套 t01f 方法(pers 271 字段最高价值);mixed/count-loop 先恢复行边界(club 前缀可先行)