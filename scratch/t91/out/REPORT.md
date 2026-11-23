# t91 — 外源仓库 nottatdat/fm-data 对照报告

**外源**:`github.com/nottatdat/fm-data`,克隆于 `scratch/ext/fm-data/`,只读,
commit `d7a7150`(2026-11-11)。全程 `provenance=ext/fm-data@d7a7150`。
**本仓**:FM24 24.4.2,`evidence/fm24/reports/editor_schema/master.json` +
`reports/club_nation_subtable_schema.json`(v11.1)。
**等级纪律**:外源只是**假设源**。本轮**没有**产生任何新 L1/L2/L3 分级,
**没有**写入 `reports/` 或 `scratch/t01/LEDGER.json`,**没有**改动任何既有判定。

---

## 0. 交付物

| 文件 | 内容 |
|---|---|
| `scratch/t91/out/code_coverage.json` | §2 码表对拍(三清单+计数+逐码台账) |
| `scratch/t91/out/nulldate_probe.json` | §3 空日期探针(逐表逐槽位命中率+对照常量+文法校验) |
| `scratch/t91/out/hypotheses.md` | §4 八条文法印证(H1–H8) |
| `scratch/t91/out/verify.py` | 独立复算 §2/§3 全部计数(45 项,全过) |
| `scripts/t91_codes.py` | §2 生成器(`--help` / `--selftest`) |
| `scripts/t91_nulldate.py` | §3 生成器(`--help` / `--selftest`) |

`scripts/t01_anchors.py`:**7/7 PASS**(未受影响)。

---

## 1. 关键前提:外源 `field_dict.csv` 不在克隆内

agentA §3 明确 `field_dict.csv`(2103 条,739 条 `pers`)位于他们 `work/agentA_re/`,
**不在克隆内**。因此可恢复的外源码只有:

- `agentA-native-re.md` §3 表格:**16 条** `pers,*`(带 label);
- `briefing.md` §Key files 行内补充:**+2 条**(`PCJO`、`PSJO`);
- 合计 **18 条**,占其 2103 条的 **0.86%**。

`fm26/offline/*.py` 内**没有**内嵌码表(只有 person 名/DOB 扫描逻辑),
所以任务书给的备用提取路径同样产出为空。**这一点如实记为范围限制**,不掩盖。

---

## 2. 码表对拍结果(`code_coverage.json`)

| 项 | 我们 | 外源 | 说明 |
|---|---|---|---|
| distinct field codes | **3009** | 2103 | 版本漂移,差值不构成覆盖缺口 |
| `pers` 域码数 | **271** | 739 | 同上 |
| distinct 表标签 | **395** | 12(声明) | 我们的粒度细得多(含 `acmp.helpers.*` 等子域) |
| 无 name 的码 | 60 | 未知 | 我们侧已记录 |

### 清单① 我们有、他们没有

**无法逐条枚举**(缺外源全表)。只能给规模陈述:3009 vs 2103,`pers` 271 vs 739。
⚠ 差值 **不是**覆盖缺口的证据——FM26 与 FM24 的 editor schema 本就分属不同版本。
`pers` 我们更少(271 < 739)反过来说明外源把更多字段归进 `pers` 域(见清单③表域漂移)。

### 清单② 他们有、我们没有

**空**。18 个可恢复外源码**全部命中**我们码表(0 缺失)。

### 清单③ 双方都有但标签/表域冲突(7 条)

**标签漂移(4 条,规范化后仍不同)**

| 码 | 我们 label | 外源 label |
|---|---|---|
| `PnRV` | Full Name | name |
| `Pnti` | *(无 name)* | nation |
| `PCJO` | Job | club primary job |
| `PSJO` | Secondary Job | club secondary job |

**表域漂移(3 条)**

| 码 | 我们表标签 | 外源表标签 |
|---|---|---|
| `Ncra` | `nnpl`(non player) | `pers` |
| `Npta` | `nnpl` | `pers` |
| `Ppsr` | `play`(player) | `pers` |

**判读**:外源把 `Ncra`/`Npta`/`Ppsr` 归到 `pers` 更像**宽松的"人相关"归类**,
而我们按 editor XML 的真实宿主表(`non player.xml` / `player.xml`)分域。
**冲突列不改判**——两边口径不同,不是任一方错。要裁决需外源 `field_dict.csv` 原件。

### 表标签:`natc` 在我们侧完全不存在

外源声称 12 个表标签含 `natc`;我们 `natc` = **0 码**,nation 容器我们记作
**`nati`(339 码)+ `nation.xml`**。这是**命名域冲突**,不是覆盖缺口。
其余 11 个标签我们全部有(pers 271 / club 423 / comp 249 / stad 60 / team 23 /
weat 94 / awar 38 / inju 27 / nati 339 / city 14 / agrm 8)。

---

## 3. 空日期探针结果(`nulldate_probe.json`)

常量 `01 00 6c 07` = `0x076c0001` = `(u16 doy=1, u16 year=1900)`。

### 3.1 命中槽位(全部 15 个已闭合行框的表 × 双档)

| 表 | 行数 | 命中率 100% 槽位 | 次高命中 |
|---|---|---|---|
| `client table_21` | 48,413 | **row+13** | — |
| `server table_21` | 48,413 | **row+156** | +135 99.62% / +131 96.12% / +45 94.73% / +41 92.70% / +37 78.93% |
| `client/server table_0` | 3,545 | — | +19 92.86% / +60 89.45% |
| `table_56 / 7 / 8 / 24 / 27` | 6 / 208 / 126 / 84,507 / 334 | **0 个** | 均 < 0.1% |

`server table_21` 的六个槽位与既有 L3 记录**逐一对齐**:
`Splr`(body 131, held)、`Sprl`(135, L3)、`Sbld`(37, L3)、`Srbd`(41, L3)、
`Doco`(45, L3)、body 156(held 区)。**这是独立复算,不是新判据**。

### 3.2 随机与"任意常量"对照

- 同表其它槽位平均命中率基线:`client_21` 2.86% / `server_21` 3.16% / `table_0` 2.46%。
  命中槽位是基线的 **25–35 倍**。
- **对照常量**:`0x076c0002` 全槽位最高 **0 命中**;`0x076c0000` 最高 0.06%;
  `0x01000001` 最高 0.51%。→ 命中的是**这个特定值**。
- 字节级期望随机 = `len/2^32` ≈ 0.0004–0.002;实测超出 10⁵ 量级。

### 3.3 非 sentinel 行的 `(doy, year)` 文法校验(**本轮最有价值的独立印证**)

| 槽位 | 非 sentinel 行 | 文法通过 | 通过率 | year | doy |
|---|---|---|---|---|---|
| `table_0` +19 | 253 | 253 | **100%** | 2003–2024 | 1–365 |
| `table_0` +60 | 374 | 374 | **100%** | 2008–2024 | 7–366 |
| `server_21` +131 | 1,880 | 1,880 | **100%** | 1957–2024 | 1–366 |
| `server_21` +41 | 3,534 | 3,533 | 99.97% | 1919–2028 | 1–366 |
| `server_21` +45 | 2,549 | 2,529 | 99.22% | 1859–2028 | 1–366 |
| `server_21` +37 | 10,202 | 10,094 | 98.94% | 1807–2029 | 1–366 |
| `server_21` +135 | 182 | 174 | 95.60% | 2009–2031 | 1–365 |

同一 4 字节槽位:**等于常量时是 null date,不等于常量时几乎全部解成合理日期**。
两条互不重叠的证据共同支撑 `(u16 doy, u16 year)` 编码。
**但仍不构成 L3**:缺 exe 侧 getter/setter 的宽度与解码指令;
`row+37` 的 108 行(1.06%)反例**原样保留**,未解释。

### 3.4 与既有 date4 sentinel 分列口径的关系

**只增证据,不推翻**。既有口径按"表/字段"记 sentinel 恒等;本轮补"槽位级命中率 +
非 sentinel 解码通过率"这一维。语义命名差异如实记录:外源称 *null date*(未设置),
我们既有记录多写作 *default/sentinel*(常量)。**命名不改判**;既有 `t83` 已有
"getter suppresses 1900-01-01" 的先例,可作 t92 的对照起点。

### 3.5 people 家族(外源主战场)

| 文件 | 头部 | 扫描量 | `0x076c0001` 次数 | 随机期望 |
|---|---|---|---|---|
| `people_db.dat` | `03017461642ef10d` + zstd@8 | 37.7 MB | **708,262**(18,762/MB) | 0.0088 |
| `basic_people_db.dat` | 同上 | 37.7 MB | **7** | 0.0088 |
| `summary.dat` | 未压缩,`zstd_at=-1` | 1.65 MB | **0** | 0.0004 |

- `people_db.dat` 的 run 长度直方图:`{1: 356066, 2: 100735, 3: 46082, 5: 2496}`
  ——大量 1–3 连,与外源 agentB §2.2 "3 连前缀"描述**同族**。
- `basic_people_db.dat` 几乎无该常量 → 与外源 agentC"basic 表是纯数值 84B 记录"一致。
- `summary.dat` **零**命中 → 与外源 agentC"summary.dat 里没有 DOB"**双向负结果吻合**。

---

## 4. 文法印证(`hypotheses.md`,H1–H8)

| # | 主题 | 一致性 |
|---|---|---|
| H1 | `[u32 len][utf8]` 内联串 | **同族(独立印证)**,我们另有行框闭合 |
| H2 | `01 00 6c 07` null date + `(doy, year)` | **同族**,我们新增槽位级证据 |
| H3 | `[uid][uid]` 双写 | **同族,我们约束更强**(ordinal + 严格递增 + DP 唯一铺法) |
| H4 | CA u16 / age u8 / pos u32 掩码 | **不可比**(people/summary 域,不在本工作区范围) |
| H5 | people 按 `nation_ref` 分组 | **部分同族**(我们只有"行序≠XML序"的负向结论) |
| H6 | 12 字节容器头 | **部分同族 + 确定差异**:外源 6 字节 `a0 0f 90 0e 07 00` 我们档内不存在 |
| H7 | `summary.dat` 未压缩 | **同族**(含双向负结果吻合) |
| H8 | 码表码空间 2103 vs 3009 | **同族 + 7 条漂移** |

### H6 是唯一的**确定差异**(负结果,原文保留)

- 外源:`03 01` + `"tad."` + `a0 0f 90 0e 07 00`(6B)+ zstd@**12**
- 我们:`03017461642ef10d`(8B)+ zstd@**8**
- version 与 magic 完全一致;中间 6 字节常量我们侧**不存在**(我们是 `f1 0d` 两字节)。
- 判读:**版本/产品线差异**(FM24 24.4.2 vs FM26 26.2.0),不是任一方解错。
  我们的 8 字节头在 t71 已按 SHA-256 钉死并逐档验证。
- **不得**把外源 12 字节头套到我们档上。

---

## 5. 复算与回归

```
$ FM24_DB_DIR=... py -V:3.12 -I -B scratch/t91/out/verify.py
== §2 code table ==  (16 项 OK)
== §3 nulldate probe ==  (29 项 OK)
ALL CHECKS PASSED          # 45 项

$ py -V:3.12 -I -B scripts/t01_anchors.py
7/7 checks passed
```

`verify.py` 的独立性:统计与判据全部重写(逐槽位用字节切片而非 `struct.unpack`、
标签规范化独立实现、码提取直接扫 markdown 正则)。容器目录解析复用
`scripts/fm24_dump.load_payload`(t38/E80 已修复口径),**不复用** t91 生成器的统计代码。

---

## 6. 净结论与未解项

**净结论(候选,非结论)**:外源与我们在 H1/H2/H3/H7 上**独立收敛**到同一批文法。
这提升了我们对这几条文法**描述**的信心,但:

- **不产生**任何新的 L3 槽位定位;
- **不改变**任何既有分级(club 78 L3 / comp 49 L3 / nation 30 L3 均不受影响);
- **不写入** `reports/` 或 LEDGER。

**未解项(如实列出,未静默放弃)**:

1. 外源 `field_dict.csv`(2103 条)不在克隆内 → 清单①无法逐条枚举,清单③只能覆盖 18 条。
2. `natc` ↔ `nati` 是否同一实体,需外源原件才能裁决。
3. H1 的 `ff ff ff ff 00` 五字节前缀在 `row+37` 前 5 字节是否出现 —— 未做(row+32..36 未逐行统计)。
4. H4/H5 的复用路径(people 域 / club 表按 nation 分组)属新假设,未启动。
5. `server_21` row+37 的 108 行文法反例(1.06%)未解释,原样保留。
