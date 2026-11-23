# t143 — FM24 本地化归档与实体名称

| 归档 | 字节精确闭合 | 记录 | 非空字符串 | person_names 记录 / 字符串 |
|---|---:|---:|---:|---:|
| `lang_db_2400.dat` | 352/352 | 5,296,880 | 10,028,256 | 800,000 / 1,796,024 |
| `lang_update_db.dat` | 352/352 | 111,255 | 262,470 | 15,732 / 37,799 |

合计 **10,290,726** 个非空字符串；计入实体固定槽、变体字符串和 `person_names` 的非空字段。同文、同记录在不同槽或归档中分别计数；空字符串和 NULL 另计。

## 语言分布

每个 ID 在每个归档中均有 15 张实体表和 1 个 `person_names` 成员。语言名从 t133 `client/8` 的内部 ID 与 UID/DBID 三重相等取得。

| ID | `client/8` 原名 | 2400 记录 | 2400 字符串 | 2430 记录 | 2430 字符串 |
|---:|---|---:|---:|---:|---:|
| 6 | Czech | 204,402 | 368,493 | 4,013 | 9,311 |
| 7 | Dutch | 204,825 | 367,656 | 4,249 | 9,792 |
| 8 | English | 204,378 | 406,464 | 4,406 | 12,132 |
| 10 | French | 204,406 | 367,205 | 4,868 | 11,144 |
| 11 | German | 204,406 | 371,003 | 4,816 | 11,330 |
| 12 | Greek | 226,846 | 448,009 | 4,739 | 12,273 |
| 15 | Italian | 204,406 | 367,209 | 4,879 | 10,992 |
| 16 | Japanese | 204,402 | 365,148 | 4,481 | 10,771 |
| 17 | Korean | 210,912 | 394,100 | 4,554 | 10,647 |
| 18 | Polish | 204,406 | 367,884 | 4,372 | 9,941 |
| 19 | Portuguese | 204,410 | 367,451 | 4,533 | 10,510 |
| 21 | Russian | 204,405 | 371,912 | 4,281 | 9,870 |
| 22 | Norwegian | 204,406 | 369,707 | 4,376 | 10,049 |
| 24 | Spanish | 204,411 | 369,310 | 5,131 | 11,111 |
| 25 | Turkish | 204,406 | 365,379 | 4,271 | 9,826 |
| 30 | Swedish | 204,408 | 368,844 | 4,362 | 10,061 |
| 32 | Danish | 204,406 | 369,369 | 4,322 | 9,939 |
| 1000000 | Latin American | 204,411 | 369,303 | 4,555 | 10,273 |
| 1000001 | Brazilian | 204,402 | 366,679 | 3,022 | 6,922 |
| 1000002 | Chinese Simple | 903,340 | 1,927,976 | 15,724 | 36,568 |
| 1000003 | Chinese Traditional | 276,082 | 552,661 | 6,901 | 16,888 |
| 1000004 | Usa | 204,404 | 406,494 | 4,400 | 12,120 |

## 字节文法

- 每个归档是 8B `tad.` 外壳 + FMF；目录路径、Zstd frame 偏移、压缩/解压字节数见 JSON。单帧恰好消耗目录给出的整个成员区间。
- 每个解压成员头：`03 01 74 61 64 2e` + LE `u16` 版本（2400=`0x0def`，更新=`0x0df1`）。
- 数字表：`+8 u32 n`，`+12` 开始 `n` 行，每行 `u32 DBID` 后接下表槽位，无独立记录长度、UID、表号或文件尾。表号来自文件名。
- `S` = `u32` 字节长度 + 严格 UTF-8；`0` 是空串，`0xffffffff` 是 NULL。简繁中文也是 UTF-8；无 UTF-16LE 分支。
- `B` = `u8` 原始标量，字符串旁通常是语法分类；`H` = `u16`；`V` = `u8` 数量 + 对应数量的 `S, u16 field_type, u8 form`。`form` 依语言与字段而定，不是全局位掩码。
- 法语 t9/type 1 `algérien / algérienne / algériens / algériennes` 对应 `1/2/3/4`（阳单、阴单、阳复、阴复）；意大利语该槽顺序不同。希腊语另有格变；法语 t35 的 `field_type 3/4` 分别选择阳性/阴性位置术语。
- `person_names`：从 `+8` 开始，无行数；每行是 `S S S S + u32 qualifier_id + u16 qualifier + u8 form`。下一条首串长度为零即读到 4B 终止符，之后必须是 EOF；不是数字表的 UID 索引。
- 验证不靠扫描名称锚点：逐成员按槽位解析，正文游标与 EOF/终止符边界之差 `diff=0`，并用已解析值重编码整个成员进行逐字节比较。未证实的标量语义保留原值。

| 本地化表 | t133 实体 | 键之后的槽位 |
|---:|---|---|
| 0 | AWARD | `SBSBV` |
| 2 | CITY | `SBV` |
| 3 | CLUB | `SBSBSSSBSVH` |
| 5 | CONTINENT | `SBSSSBSBV` |
| 6 | INJURY | `SBSBV` |
| 7 | MEDIA_SOURCE | `SB` |
| 9 | NATION | `SBSBSSV` |
| 18 | DERBY | `SSSSBBBBV` |
| 19 | REGION | `SV` |
| 21 | STADIUM | `SSBBV` |
| 23 | STAGE_NAME | `SBSBSBV` |
| 25 | COMP | `SBSBSV` |
| 35 | PLAYER_TYPE | `BBV` |
| 47 | LOCAL_REGION | `SBSBV` |
| 56 | AGREEMENT | `SBSBB` |

## 英文／简体／繁体 UID 联接

行键按实体表匹配 t133 的 DBID，再读该行实际 UID。国家名本地化表 **9 → server/10**；独立复核 server/9（国家队容器）与 server/10 的 251 个 `(DBID, UID, ordinal)` 全等。球场与俱乐部等不同表可以共享 UID；`--lookup` 分表列出。

| 实体 | t133 表 | 2400 命中 / 记录 | 2430 命中 / 记录 |
|---|---:|---:|---:|
| COMP | 25 | 154,770 / 154,770 | 876 / 876 |
| NATION | 10 | 5,522 / 5,522 | 519 / 519 |
| CLUB | 3 | 1,843,116 / 1,844,414 | 72,264 / 72,264 |
| AWARD | 0 | 77,440 / 77,440 | 1,643 / 1,643 |
| STADIUM | 21 | 1,059,168 / 1,059,476 | 11,840 / 11,840 |
| CITY | 2 | 1,232,286 / 1,232,396 | 7,054 / 7,054 |

`t3` 行末 `H`：`lang_db_2400` 非空有效国家序号中 1,804,110/1,805,364 与当前 t133 `CLUB_HEAD` 的 t57 `Cnti`（缺失时 `Cbni`）一致；另有 37,752 个 `0xffff`。

`t3` 行末 `H`：`lang_update_db` 非空有效国家序号中 71,178/71,178 与当前 t133 `CLUB_HEAD` 的 t57 `Cnti`（缺失时 `Cbni`）一致；另有 1,086 个 `0xffff`。

以下 **76** 行均命中英文、简中和繁中语言成员；其中 **39** 行的简繁名称均含汉字。繁中成员对不少国外实体保存英文原文，本表如实列出。每种语言独立以整行 update 覆盖 base；† 表示来自更新层。表中保留原始名称、简写和大小写；每行的 core 和语言层字节偏移可在 JSON 复查。

| 实体 | UID | English | 简体中文 | 繁體中文 |
|---|---:|---|---|---|
| COMP | 11 | English Premier Division | 英格兰超级联赛 | English Premier Division |
| COMP | 1301394 | UEFA Champions League | 欧洲冠军联赛 | UEFA Champions League |
| COMP | 1301396 | UEFA Europa League | 欧足联欧洲联赛 | UEFA Europa League |
| COMP | 31051584 | UEFA Europa Conference League | 欧足联欧洲协会联赛 | UEFA Europa Conference League |
| COMP | 1301385 | World Cup | 国际足联世界杯足球赛 | 國際足協世界盃足球賽 |
| COMP | 22 | Bundesliga | 德国足球甲级联赛 | Bundesliga |
| COMP | 32 | Italian Serie A | 意大利足球甲级联赛 | Italian Serie A |
| COMP | 16 | Ligue 1 Uber Eats | “Uber Eats”法国足球甲级联赛 | Ligue 1 Uber Eats |
| COMP | 130026 | Clearer Water Irish Cup† | 塞缪尔盖尔斯顿威士忌爱尔兰杯 | Clearer Water Irish Cup† |
| COMP | 95 | European Championship Qualifying Playoff | 欧洲杯预选赛附加赛 | 歐洲國家盃外圍賽附加賽 |
| COMP | 5624449 | Hong Kong Premier League | 中国香港超级联赛 | 香港超級足球聯賽 |
| COMP | 5624451 | Hong Kong FA Cup | 中国香港足总杯 | 香港足總盃 |
| COMP | 23397138 | Chinese Taipei Football Premier League | 中国台湾超级联赛 | 中華臺北超級聯賽 |
| NATION | 765 | England | 英格兰† | 英格蘭 |
| NATION | 796 | Spain | 西班牙† | 西班牙 |
| NATION | 771 | Germany | 德国† | 德國 |
| NATION | 769 | France | 法国† | 法國 |
| NATION | 776 | Italy | 意大利† | 義大利 |
| NATION | 1651 | Brazil | 巴西† | 巴西 |
| NATION | 1649 | Argentina | 阿根廷† | 阿根廷 |
| NATION | 110 | China PR | 中华人民共和国† | 中華人民共和國 |
| NATION | 116 | Japan | 日本† | 日本 |
| NATION | 111 | Hong Kong (China PR) | 中国香港† | 中國香港 |
| NATION | 124 | Macau (China PR) | 中国澳门† | 中國澳門 |
| NATION | 138 | Chinese Taipei (China PR) | 中国台湾† | 中國臺灣 |
| CLUB | 679 | Manchester City | 曼彻斯特城足球俱乐部 | Manchester City |
| CLUB | 680 | Manchester UFC | 曼彻斯特红 | Manchester UFC |
| CLUB | 1736 | R. Madrid | 皇家马德里 | R. Madrid |
| CLUB | 602 | Arsenal | 阿森纳 | Arsenal |
| CLUB | 915 | FC Bayern München | 拜仁慕尼黑足球俱乐部 | FC Bayern München |
| CLUB | 676 | Liverpool | 利物浦 | Liverpool |
| CLUB | 630 | Chelsea | 切尔西 | Chelsea |
| CLUB | 1708 | Barcelona | 巴塞罗那 | Barcelona |
| CLUB | 868 | Paris Saint-Germain | 巴黎圣日耳曼足球俱乐部 | Paris Saint-Germain |
| CLUB | 907 | Borussia Dortmund | 多特蒙德普足球俱乐部 | Borussia Dortmund |
| CLUB | 992 | AFC Ajax | 阿贾克斯足球俱乐部 | AFC Ajax |
| CLUB | 1135 | FC Internazionale Milano | 国际米兰足球俱乐部 | FC Internazionale Milano |
| CLUB | 1139 | Juventus | 尤文图斯足球俱乐部 | Juventus |
| CLUB | 406 | Beijing Guo'an | 北京国安足球俱乐部 | 北京中赫國安 |
| CLUB | 409 | Guangzhou FC | 广州队足球俱乐部 | 廣州足球俱樂部 |
| CLUB | 414 | Shanghai Shenhua | 上海绿地申花足球俱乐部 | 上海綠地申花 |
| CLUB | 23366052 | Shanghai Jiading Huilong | 上海嘉定汇龙足球俱乐部 | 上海嘉定匯龍足球俱樂部† |
| AWARD | 102406 | World Golden Ball | 国际足联金球奖 | 國際足協金球獎 |
| AWARD | 109375 | World Cup Golden Boot | 世界杯金靴奖 | 世界盃金靴獎 |
| AWARD | 150936 | UEFA Champions League Golden Boot | 欧洲冠军联赛金靴奖 | UEFA Champions League 金靴獎 |
| AWARD | 150967 | European Golden Shoe | 欧洲金靴奖 | 歐洲金靴獎 |
| AWARD | 136386 | Chinese Super League Golden Boot | 中国足球联赛金靴奖 | 中國超級聯賽金靴獎 |
| AWARD | 106965 | MLS Golden Boot | 美国大联盟神射手 | MLS 金靴獎 |
| AWARD | 23397143 | Chinese Taipei Football Premier League Golden Boot | 中国台湾超级联赛最佳射手 | 中華臺北企業甲級足球聯賽金靴獎 |
| STADIUM | 102969 | Wembley | 温布利大球场 | Wembley |
| STADIUM | 676 | Anfield | 安菲尔德球场 | Anfield |
| STADIUM | 680 | Old Trafford | 老特拉福德球场 | Old Trafford |
| STADIUM | 5114325 | Etihad Stadium | 伊蒂哈德球场 | Etihad Stadium |
| STADIUM | 5114336 | Emirates Stadium | 酋长球场† | Emirates Stadium |
| STADIUM | 1056 | Santiago Bernabéu | 圣地亚哥·伯纳乌球场 | Santiago Bernabéu |
| STADIUM | 1040 | Camp Nou | 诺坎普球场 | Camp Nou |
| STADIUM | 977 | Parc des Princes | 王子公园球场† | Parc des Princes |
| STADIUM | 28096287 | The Tottenham Hotspur Stadium | 托特纳姆热刺体育场† | The Tottenham Hotspur Stadium |
| STADIUM | 624 | The Cledara Abbey Stadium† | 艾比体育场 | The Cledara Abbey Stadium† |
| STADIUM | 103239 | Hong Kong Stadium | 香港大球场 | 香港大球場 |
| STADIUM | 135465 | Hong Kong Football Club Stadium | 港会足球场 | 港會足球場 |
| STADIUM | 131131 | Beijing Sport University Stadium | 北京体育学院体育场 | 北京體育學院體育場 |
| STADIUM | 23148989 | Shenzhen Bay Sports Centre | 深圳湾体育中心 | 深圳灣體育中心 |
| CITY | 100023 | London | 伦敦 | London |
| CITY | 100062 | Manchester | 曼彻斯特 | Manchester |
| CITY | 341 | Madrid | 马德里 | Madrid |
| CITY | 270 | Paris | 巴黎 | Paris |
| CITY | 370 | Barcelona | 巴塞罗那 | Barcelona |
| CITY | 553 | Rome | 罗马 | Rome |
| CITY | 103194 | Beijing | 北京 | 北京 |
| CITY | 128046 | Shanghai | 上海 | 上海 |
| CITY | 103195 | Hong Kong | 香港(中国香港) | 香港(中國) |
| CITY | 103225 | Taipei | 台北(中国台湾) | 臺北 |
| CITY | 128037 | Wuhan | 武汉 | 武漢 |
| CITY | 128042 | Shenzhen | 深圳 | 深圳 |
| CITY | 128055 | Guangzhou | 广州 | 廣州 |

## 复算

```powershell
py -V:3.12 -B scripts/t143_lang_db.py
py -V:3.12 -B scripts/t143_lang_db.py --selftest
py -V:3.12 -B scripts/t143_lang_db.py --lookup 676
```

输入 `.dat` 只读，解压和重编码均只在内存进行；`--lookup` 和 `--selftest` 不写输出。
