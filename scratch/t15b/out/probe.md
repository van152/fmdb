# t15b — 未覆盖档案清点报告

**状态:ok(9/9 档案容器层全部进入)**
生成:2026-11-18 · 只读 · 数据源 `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`(**未读 Z: 盘**)
机读结果:`scratch/t15b/out/probe.json` · 脚本:`probe.py` / `probe2.py` / `probe3.py` / `finalize.py`
一键重跑:`bash scratch/t15b/run_all.sh`(只读,全部产出在 `scratch/t15b/out/`)
基线对照:`scratch/t13e/out/baselines.json`

---

## 0. 一句话结论

9 个档案的**容器层 100% 进入,0 个未知外壳**;真正值得开专项的只有 **`people_db.dat`** ——
它和已解析的 `basic_people_db.dat` 是同一个 658,011 人宇宙,但 `basic_people_db` 只是定长 stub
(连姓名都没有),`people_db` 才是带姓名 + 出生日期的全量库,且本任务已找到一条 **1,193 行逐字节对齐的跨档案锚点**。
其余 8 个档案(id/dt/index/summary/lang_update)**容器与链条已闭合,缺的只是行内字段语义**,不构成新专项。

---

## 1. 容器层普查(9/9 通过)

| 档案 | 大小 | tag | ver | Zstd@8 | FMF@8 | 判定 |
|---|---:|---|---:|:-:|:-:|---|
| people_db.dat | 67,502,767 | `tad.` | 3569 | ✔ | ✘ | `tad.` + offset 8 单个 Zstd 流 |
| pl_hist_dt.dat | 56,996,116 | `tadc` | 3 | ✔ | ✘ | `tadc` + **串联 Zstd 帧** |
| pl_hist_id.dat | 4,124,656 | `tad.` | 1 | ✘ | ✘ | v1 裸 u32 数组 |
| pl_hist_index.dat | 3,081,975 | `tad.` | 3569 | ✔ | ✘ | `tad.` + Zstd |
| non_pl_hist_dt.dat | 27,607,915 | `tadc` | 3 | ✔ | ✘ | `tadc` + 串联 Zstd 帧 |
| non_pl_hist_id.dat | 5,972,352 | `tad.` | 1 | ✘ | ✘ | v1 裸 u32 数组 |
| non_pl_hist_index.dat | 4,153,253 | `tad.` | 3569 | ✔ | ✘ | `tad.` + Zstd |
| summary.dat | 1,648,018 | `tad.` | 3569 | ✘ | ✘ | `tad.` 自有文法(无 Zstd 无 FMF) |
| lang_update_db.dat | 2,317,274 | `tad.` | 3569 | ✘ | ✔ | `tad.` + **内嵌 fmf. 目录** |

`list_tables()`(fm24_dump 的 runpy 链)结果:

* **只有 `lang_update_db.dat` 可列** → 352 个成员,**`table_entries = 0`**(全是 auxiliary)。
* 其余 8 个档案全部抛 `ValueError: no supported embedded resource-FMF signature` —— **它们不是 FMF 档案,
  不能按 `client_db`/`server_db` 的表目录思路处理**。这是负结果,已保留。

### 1.1 lang_update_db.dat 成员构成

| 项 | 值 |
|---|---:|
| 成员总数 | 352 |
| `<lang>_<table>.dat` 命名 | 330 = **22 语言 × 15 表号** |
| `<lang>person_names.dat` | 22 |
| 表号全集 | 0,2,3,5,6,7,9,18,19,21,23,25,35,47,56 |
| 解压总长 | 7,390,959 B |

**行文法未闭合(负结果,如实登记)**:每个成员头是 `tad.` + `f1 0d` + `u32 count` + `u32 aux`,
随后是 `(u32 len, utf8, 0xff)` 序列;但走 3–6 个字符串后就遇到非该文法的字节
(例 `8_3.dat` 在 offset 76 撞到 `u32 = 1258291456`),说明**记录内还有子结构**。
235 个带 `tad.` 头的成员中,**0 个**能被单层文法走到 EOF。
→ 三语列示(`Atl�tico Petr�leos de Luanda` / `Petro Luanda` / `APL` / `PL`)是真实内容,
但"每行几条字符串"不能声称已解。

---

## 2. `people_db.dat` —— 唯一建议开专项的档案

### 2.1 基本事实

| 项 | 值 |
|---|---|
| 压缩 / 解压 | 67,502,767 B → **400,443,970 B**(5.93×) |
| 解压 SHA-256 | `21686a98…0f2fbd`(**与旧仓 `PEOPLE_DB.md` 记录逐字节一致**) |
| 非 FMF | `list_tables()` 抛 FMF 签名错 |
| **payload + 2 的 u32** | **658,011** ← 与 `basic_people_db.dat` payload + 0 的 count **完全相同** |

### 2.2 已闭合的跨档案锚点(本任务新增,旧仓没有)

offset 6 起的**紧凑段**:

```
u32 key | u32 type(=5) | u8 unk | u32 name_len | name(utf8) | 8×00 | u32 key2(==key) | u32 duni | u32 duni(==上一列)
行跨度 = 33 + name_len
```

实测 **1,193 / 1,193 行全走通,end_pos = 55,750,零剩余**:

* `key` 集合 **恰为 656818..658010 连续全覆盖**(无缺、无重)
* `duni` 值域 2,002,040,996 – 2,002,042,188
* 与 `basic_people_db.dat` 逐 ordinal 对照:**1193/1193 行 (key, duni) 完全相等**,且这 1193 行在
  basic 侧**全部是 class 5**
* 首行 `Zarko Serafimovski`、末行 `Polo Carrera`,1 行空名

这是本任务最强的证据:**`people_db` 的 key 列就是 `basic_people_db` 的行序号**,两者同一 person 宇宙。
等级:**L1(两份档案字节对齐)+ L2(跨文件同值锚点)**。

### 2.3 段之后的版图

| 区间 | 内容 |
|---|---|
| 0 – 55,750 | 紧凑段 1,193 行(已闭合,见 2.2) |
| 55,750 – 56,126 | **376 B 未解小间隙**(含 `ff ff ff ff 07 06` 等) |
| 56,126 – EOF | **姓名 + 出生日期锚点流** |

锚点文法:`FF FF FF FF 00 | u32 name_len | utf8 name | u32 dob`,其中 `dob = (year<<16) | day_of_year`。

全量扫描结果:

* `FF FF FF FF` marker:10,143,298 次
* `FF FF FF FF 00` marker:**2,260,437** 次
* 通过"合法 UTF-8 + 可打印 + 年份 1850–2015 + doy 1–366"四重判据的锚点:**186,082** 个
  (旧仓 `PEOPLE_DB.md` 报 186,084,差 2 —— 阈值 1850/2015 vs 旧仓更窄,不构成矛盾)
抽样 3 个真实姓名:`Esteban Ariel Saveljich`(off 74,870)、`Stefan Mugoša`(88,392)、`Vladan Giljen`(143,880)。

**注意:186,082 是"姓名+生日锚点"计数,不是 658,011 行解析。** 主体（约 400 MB）里
还有未定性的属性块,这正是专项要解的东西。

### 2.4 与 `basic_people_db.dat` 的关系(直接回答任务书第 4 问)

| | basic_people_db | people_db |
|---|---:|---:|
| 解压长度 | 54,060,043 B | 400,443,970 B(7.41×) |
| 行数声明 | 658,011 | 658,011(同值) |
| 行结构 | 定长:class1/2/3=83B,class4=34B,class5=22B | 变长,带姓名/生日 |
| class 5 段 | **连姓名都没有**(`11 05 00×8 ...`) | 有姓名 + duni |
| 用途 | 索引/骨架 | 真身 |

结论:**不是父子表,是同一次装载的两个 face**。`basic_people_db` 用于快速遍历身份，
`people_db` 才是带人名的全量数据。

---

## 3. `pl_hist_*` / `non_pl_hist_*` —— 已解,不建议开专项

三件套形成 **id → dt → index** 的完整三角,本任务抽样复现 + 与旧仓 L1 结论一致:

| 档案 | 解压长度 | 关键量 | 复现结果 |
|---|---:|---|---|
| pl_hist_dt.dat | 198,695,332 | 44 B/行,4,515,803 数据行;**48,510 帧** | 抽样 6,000 行 next 链 **0 违例**(4,982 中间行 + 1,018 终结行) |
| pl_hist_id.dat | — | 1,031,162 u32 = **515,581 对** | 前 200 对 **200/200** 24B/44B 对齐、步长连续 |
| pl_hist_index.dat | 4,124,652 | count = **515,581** | count == id 对数 ✔;key 严格升序 ✔;ordinal 是 0..n-1 完整置换 ✔ |
| non_pl_hist_dt.dat | 77,098,632 | 24 B/行,3,212,443 行;**18,823 帧** | 抽样 6,000 行 next 链 **0 违例**(5,968 为终结行,与"大量单行块"一致) |
| non_pl_hist_id.dat | — | 1,493,086 u32 = **746,543 对** | 前 200 对 **200/200** 24B 对齐 |
| non_pl_hist_index.dat | 6,037,508 | count = **754,688** | = 746,543 有效 + **8,145 个 0xFFFFFFFF sentinel** |

闭合校验:`id` 末对 `end + stride == dt 解压长度`,**pl 与 non_pl 双双成立**。

### 3.1 与已知基数的关系(任务书第 4 问)

| 量 | 值 | 对照 | 差 |
|---|---:|---|---:|
| pl_hist 人物数 | 515,581 | class2 PLAYER 476,158 | **+39,423** |
| non_pl_hist 人物数 | 746,543 | class1 NON_PLAYER 166,064 | **+580,479** |
| non_pl_hist 人物数 | 746,543 | server t49 履历 792,149 | **−45,606** |
| 两者之和 | 1,262,124 | basic 总 658,011 | +604,113 |

**结论:对不上,而且不该对得上。** 履职历史(person × 赛季/职位)与 person 行数不是同一层;
`t49` 是 server 侧列式履历,`non_pl_hist` 是独立的历史档案,两者差 45,606 属于正常口径差。
**不得用行数互推实体同一性。**

另外:index 的 key 列值域很宽(pl 最大 2,002,040,995;其中 183,593 个 ≥ 2e9),说明 key 不全是
`basic_people` 的 0..658,010 序号 —— 这一点**保留为开放问题**,不在本任务裁决。

---

## 4. `summary.dat` —— 容器已清,字段语义保持 0

| 项 | 值 |
|---|---:|
| 大小 | 1,648,018 B |
| 外层 | `tad.` v3569,**无 Zstd、无 FMF** |
| `ff ff ff ff 03` 分隔符 | 54,087 次 → **body 54,086 个** |
| body 长度分布 | **17 B × 53,742**;28 B × 92;41 B × 7;1019 B × 7 |
| block1 @8 | `7, 1,2,3,4,5,6,7` |
| block2 @40 | `251, 3, 1280, 156928, 256` |
| 首个分隔符 | offset 73 |

字节总账与旧仓 `SUMMARY_SEMANTICS.md` 逐项一致(54,086 body / 17 B 标准体 53,742)。
**字段语义 L2 = 0**,旧仓已穷尽候选(L1 槽位 11 个全部 raw/unresolved),本任务不重复投入。

---

## 5. 建议

| 档案 | 开专项? | 理由 |
|---|:-:|---|
| **people_db.dat** | **是(P1)** | 唯一带完整姓名/生日/属性块的档案;658,011 同一宇宙已证;1,193 行双向锚点可直接反推主体行首标记 |
| pl_hist_* / non_pl_hist_* | 否 | 容器、范围、链条全闭合;缺的只是行内字段语义,属"履历"不属 schema |
| summary.dat | 否 | 54,086 body 账已平;旧仓 L2=0,无新锚点前不重复 |
| lang_update_db.dat | 否 | 352 成员可列可解压;行文法未闭合(见 §1.1),但它是本地化覆盖层,不影响 schema 映射 |

### 若开 people_db 专项,建议的下一步(仅供决策,未执行)

1. 用 1,193 行紧凑段做**样例集**(key/duni 双向已知),反推主体每个 person 记录的边界标记语义;
2. 用 186,082 个姓名+生日锚点做**覆盖度回归**,而不是当行数;
3. 先回答一个问题:主体里 658,011 − 1,193 = 656,818 个 person 的记录起点用什么字节模式标记?

---

## 6. 负结果登记(必须保留原文)

1. `people_db.dat` / `summary.dat` / `*_hist_*.dat` 对 `list_tables()` 全部抛
   `no supported embedded resource-FMF signature` —— 它们不是 FMF 档案。
2. `lang_update_db.dat` 352 成员全部 `table_id = None`,不存在 `table_N.dat`,
   不能与 client/server 表号互比。
3. `lang_update_db.dat` 的 `(u32 len, utf8, 0xff)` 单层文法**未闭合**:235 个带 `tad.` 头的成员中 0 个走到 EOF。
4. `non_pl_hist_index` 的 count 754,688 **≠** 746,543 有效范围,差 8,145 个 `0xFFFFFFFF` sentinel。
5. `people_db` 紧凑段 1,193 行的 **key 与行序不同序**(首行 key=657,483,集合覆盖 656818..658010),
   不能把段内行号当 key。
6. 186,082 个姓名+生日锚点**不等于** 186,082 个 person 行,也**不等于** 658,011。
