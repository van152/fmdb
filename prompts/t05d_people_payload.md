# t05d — 人员行 68 字节载荷全量字段映射(basic_people_db, class 1/2/3)

## 角色与硬约束

你是数据逆向工程师。工作区 `D:\tmp2b\fm24-db`,Python 固定 `py -V:3.12 -I -B`。

**只读**:`Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\basic_people_db.dat` 只读;上游 `D:\tmp2b\fm24\` 全目录只读。**唯一可写 = 本任务 OUTDIR**。不要改 `scratch/t01`、`scratch/t02` 既有文件。

**纪律**:每个偏移必须有数据侧统计支撑;允许诚实负结果;第一步先落盘骨架。

## 已知结构(已由前序工作证明,可直接信任但要自己复现一遍)

- `basic_people_db.dat`:文件前 8 B 后是 zstd 帧。解压 payload 头 `5b 0a 0a 00` + u32 count = **658,011**,行区从 **+5** 起,末尾 9 B 尾。
- 行 = `u8 tag(0x11)` + `u8 class` + 载荷 + `u32 ordinal` + `u32 duni` + `u32 duni` + `u8 0x00`。
- 类长度:**class 1/2/3 = 83 B**(含 tag+class),**class 4 = 34 B**,**class 5 = 22 B**。类计数:1→166,064 / 2→476,158 / 3→4,757 / 4→9,839 / 5→1,193。全表封口已独立验证。
- class 名:`1=ACTUAL_NON_PLAYER`、`2=ACTUAL_PLAYER`、`3=ACTUAL_PLAYER_AND_NON_PLAYER`、`4=OFFICIAL`、`5=RETIRED_PERSON_NAME_STRINGS`。
- 已闭合字段(前序任务,见 `scratch/t02/inbox/pw/output.json`,15 个):含 `Pnti`(nation, row+2)、`Pdob` 年份(row+12)等。

**算一下载荷空间(你要用这个当硬约束)**:83 - 1(tag) - 1(class) - 4(ordinal) - 8(duni) - 1(marker) = **68 字节**可分配。class4:34-1-1-4-8-1 = **20 B**。class5:22-1-1-4-8-1 = **8 B**。

## 输入

| 用途 | 路径 |
|---|---|
| **上游人员字段映射(重要起点)** | `D:\tmp2b\fm24\reports\dbdat_decode\people_field_map.json`(含 basic_people_db 的 record_layout 与 fields 列表:offset/type/semantic/confidence) |
| **上游位置向量映射(已确认锚点)** | `D:\tmp2b\fm24\reports\dbdat_decode\people_attr_map.json`(`schema_inventory.position_fields`:如 `Pgoa` confirmed@34、`Pdce`@37、`Pdmc`@39 等;还有 `variant_2_3_attribute_window_candidate`、`ca_pa`) |
| 上游校验件 | `D:\tmp2b\fm24\reports\dbdat_decode\people_attr_verify.json`、`people_field_verify.json` |
| 上游说明 | `D:\tmp2b\fm24\reports\dbdat_decode\PEOPLE_FIELDS.md`、`PEOPLE_ATTRS.md`、`PEOPLE_DB.md` |
| 已解 15 字段(前序) | `D:\tmp2b\fm24-db\scratch\t02\inbox\pw\output.json` + `REPORT.md` + `verify.py`(`--selftest` 需 `-I -B`) |
| schema(权威) | `D:\tmp2b\fm24\reports\EDITOR_SCHEMA_FIELDS.md`:`### person（记录标识 \`pers\`，271 个字段）`、`### player（记录标识 \`play\`，179 个字段）`、`### non player（记录标识 \`nnpl\`，129 个字段）` |
| exe | `D:\tmp2b\fm24\input\editor.exe` |
| capstone | 已安装 |

## 目标

把 **68 字节载荷**尽可能完整地映射成 schema 字段。分三块:

### A. 核心标量(已有 15 个,补齐剩余)
用数据统计法:
- 对 68 个偏移逐字节/逐 u16/逐 u32 统计值域、唯一值数、与已解字段的相关性;
- 引用型字段(`database_record_unique_id`)的值必须落在目标表行数范围内(如 nation → <251、city → <56,293、club → <84,259);
- `date` 字段常见 2 字节编码(年/日),用分布验证;
- `boolean` 往往是位域:找"只有 0/1 值的位"或"只用到低 n 位的字节"。

### B. 位置向量块(上游有确认锚点,先复现再扩展)
上游 `position_fields` 给了 `Pgoa@34`、`Pdce@37`、`Pdmc@39` 等 confirmed 偏移。你要:
1. 用你自己的数据统计**独立复现**这些偏移(不能只是抄);
2. 把 person schema 里全部位置字段(约 20 个:GK/DL/DC/DR/DM/WBL/WBR/ML/MC/MR/AML/AMC/AMR/ST 等)排成有序序列,对齐到 34..52 这块窗口;
3. 用"位置值分布(football 位置熟练度 0–20 或有/无)"验证。

### C. 球员属性块(player 54 个 `player_attribute` 字段)
schema 里 `player` 实体有 **54 个 `player_attribute` 类型字段**(Tackling/Passing/Finishing…,值域通常 1–20 或 0–100)。
- 先判断它在不在 68 B 载荷内:68 B 装 54 个属性(1 B/个)只剩 14 B 给核心字段,**很紧但可能**;若装不下,说明属性在 `people_db.dat`,如实写负结果并给出判定依据。
- 若在:找**连续 54 字节、取值全部落在 [0,100](或 [1,20])的窗口**——这是强特征,`numpy` 一把扫出来。然后用 schema 里 54 个属性的**声明顺序**对齐(顺序即偏移顺序,这是本项目的核心方法论)。
- 注意 class 1(non-player)同一位置可能是 111 个 `integer`(非球员属性),class 2 才是 player 属性。**分 class 统计**,不要混。

### D. class 4(20 B)/ class 5(8 B)
- class 4 = OFFICIAL,8,839... 实际 9,839 行;20 B 载荷,对应 schema 里 `official`(16 字段)的标量子集。
- class 5 = RETIRED_PERSON_NAME_STRINGS,1,193 行;8 B 载荷,可能只是字符串引用(名字表 id)。
- 给出你能证明的部分,其余标 unresolved。

## 交付

1. `attrs.json`:
```json
{"status":"complete_partial","file":"basic_people_db.dat","count":658011,
 "class_payload_budget":{"1":68,"2":68,"3":68,"4":20,"5":8},
 "class_fields":{
   "2":[{"field":"Pgoa","offset":34,"width":1,"evidence":"...","confidence":"high"}],
   "1":[...], "4":[...], "5":[...]},
 "unresolved":[{"offset":..,"why":"..."}],
 "negative_results":["..."]}
```
2. `verify.py` — `--selftest` 通过;默认模式从 `basic_people_db.dat` 重新解压走查 658,011 行,并统计每个命名偏移的值域/唯一值数,断言与 `attrs.json` 的声明一致。
3. `REPORT.md` — 分块结论表 + 复现的上游锚点 + 未解/负结果 + 与 E32(15 字段)的差异说明。

## 验收

- class 1/2/3 的 68 B 载荷里,**≥35 个偏移**有命名(含 E32 已有的 15 个),其中 high 置信 ≥20。
- 位置向量 20 个字段**至少 12 个**有偏移确认。
- 球员属性块:若在载荷内,给出 54 个属性的偏移表;若不在,给出"不在"的三条以上证据。
- 每个命名都要有数据侧统计证据(值域/唯一值/引用合法性),不能只有"schema 顺序推的"。
- `verify.py --selftest` 全 true。

## 完成后

打印:class2 命名字段数(high/medium)、位置向量确认数、属性块结论(在/不在 + 偏移数)、未解偏移数。
