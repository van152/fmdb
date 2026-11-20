# t76a-fix1 — stadium(21) 双档 slot 扫表(数据侧 L2/candidate)

**结论**:`table_21` client 38B / server 181B 双档行框全部闭合,48,413 行 identity 100% 自证;
client 38B 与 server 181B 均 **0 未覆盖字节**;server 的 143B 差额经**逐字节对照**证明为
server 独有前缀段,其后 38B 与 client 行体在 48,413/48,413 行上**逐字节相同**。

本次交付是**数据侧**成果(`L2` / `L2_structural` / `candidate`)。静态 L3 归 t79(见 §5),
本任务只**引用**不重导,并显式标注 `t79 cited`,两档证据从不混记。

---

## 1. 行框(引用,未重闭)

行框真源 `scratch/t74/out/frames.json` → `tables['21']`,本任务**直接取用**,只做闭合断言:

| 档 | header | stride | count | footer | 闭合 | identity |
|---|---:|---:|---:|---:|---|---|
| client | 14 | 38 | 48,413 | 8 | `14 + 48,413×38 + 8 = 1,839,716` ✅ | `ord@25 uid@29 uid@33 marker@37` |
| server | 14 | 181 | 48,413 | 8 | `14 + 48,413×181 + 8 = 8,762,775` ✅ | `ord@168 uid@172 uid@176 marker@180` |

两档 `identity_rows_ok = 48,413 / 48,413`(ordinal == 行下标、UID 对相等且非零、marker 全 0)。

---

## 2. 锚点复核(5/5 client,4/4 server)

| 锚点 | client 实测 | server 实测 | 判定 |
|---|---|---|---|
| `Scti` | @3,`max 56,290 / 56,293 = 0.9999`,100% 落在 city ordinal 域 | @146 同值 | ✅ |
| `Slat` | @17,f32 有限,[-54.816, 71.029] | @160 同值 | ✅ |
| `Slon` | @21,f32 有限,[-175.207, 179.198] | @164 同值 | ✅ |
| `rdui` | @25,**48,413/48,413 等于行下标** | @168 同 | ✅ 见 §4 |
| `duni` | @29,u32@29==u32@33,48,413 distinct | @172 同 | ✅ |

---

## 3. client 38B 槽位表(12 槽,0 未覆盖)

| off | w | 字段 | 档 | 数据侧判据 |
|---|---:|---|---|---|
| 0 | 2 | (flags) | candidate | u16 位字;仅 bit 0/1/6/7/11 曾置位,11 位恒 0 → **字内字段顺序数据不可判** |
| 2 | 1 | (opaque) | unassigned | 全 0 常量 |
| 3 | 4 | **Scti** | **L2** | city ordinal 域 100% + city UID 编码被否(见 §6) |
| 7 | 4 | **Snbs** | **L2** | 44,240 null;存活值 100% < 48,413 且顶到 48,175(0.9951 紧贴);自表 UID 控制被否 |
| 11 | 2 | Sptc | candidate | u16 域 [29, 200] 落在 schema 0..200 内 |
| 13 | 4 | (opaque) | unassigned | 全行 1900-01-01 默认打包日期 |
| 17 | 4 | **Slat** | **L3** | 冻结 FIELDS 锚点,本 payload 复核 |
| 21 | 4 | **Slon** | **L3** | 同上 |
| 25 | 4 | **rdui(实为行序数)** | **L2** | 等于行下标 48,413/48,413 |
| 29 | 4 | **duni** | **L2** | UID 对 |
| 33 | 4 | **rdui_raw** | **L2** | == duni@29,exe 恒抑制该 arm |
| 37 | 1 | (marker) | unassigned | 恒 0,identity 三元组终止符 |

覆盖率:**38/38 字节有槽**,L2/L3 占 28B = **73.7%**。

---

## 4. 锚点冲突回查:`rdui@25` 的真实语义

任务给的冻结锚点写作 `rdui@25`。数据侧独立复核发现:**@25 在 48,413/48,413 行上等于行下标**,
即它是**行序数**,不是 Random ID。三条互相独立的证据:

1. `@25 == arange(48,413)` 全中,`distinct = 48,413`,`min=0 max=48,412`;
2. `@29 == @33` 全中(UID 对),且与 `@25` **不相等**;
3. t79 静态(引用):该列是成员 `+0x08`;真正的 rdui arm 在 `[+0x0c]==[+0x10]` 时抑制输出,
   而本表 48,413 行**恒等**,故 0 次存活输出。

→ **锚点不冲突,标签有歧义**。`rdui@25` 的偏移正确、名字错位;本任务按数据把 @25 记为
`row_ordinal`、@33 记为 `rdui_raw`,并保留原锚点原文于 `anchors.items`。t79 的 DONE 与
REPORT 已用同一结论("reconciles b47 'rdui@25' label"),两侧独立同结论。

---

## 5. server 181B:143B 独有段 + 38B 共享尾

**逐字节证明**:`server[143:181] == client[0:38]` 在 **48,413 / 48,413** 行上成立。
因此 143B 差额 = server 独有前缀段,`server_only_segment = {offset: 0, length: 143}`;
共享尾 `shared_tail = {offset: 143, length: 38, byte_identical: true}`。

server 共 47 槽,**181/181 字节有槽**。分档统计:

| 档 | 数量 | 字段 |
|---|---:|---|
| L2 | 5 | row_ordinal@168, duni@172, rdui_raw@176, Scti@146, Snbs@150 |
| L2_structural | 4 | Scpy@0, Sscy@4, Secy@8, Scas@12 |
| L3 | 2 | Slat@160, Slon@164 |
| candidate | 31 | Sowi, Sdcy, Sucy, 8×pitch i16, 5×enum, 5×date, 3×ubnt, flags@143, flags@36, Ssds, @63, Sprr, Sscl |
| unassigned | 5 | marker@180, @145, @156, @53, @128 |

**`L2_structural` 是本任务新增的中间档**,只用于一种情况:业务嵌套不变式在数据上成立但
**非绝对**。四个容量槽满足 `Scas@12 <= Sscy@4 <= Scpy@0 <= Secy@8`,在四值全非零的
**5,065 行上成立 98.70%**。该序恰是 schema 语义序,故"族归属"由数据决定;但 66 行反例
原样保留,故**不升 L2**。

---

## 6. wrong-UID 控制(逐列同报)

| 槽 | 参照表 | 域 | 命中 | 结论 |
|---|---|---:|---:|---|
| client Scti@3 | city t2 | 56,293 | 5,357 / 48,413 = **0.1107** | ✅ UID 编码被否 → ordinal |
| client Snbs@7 | stadium t21(自表,取 duni@29) | 48,413 | 441 / 4,173 = **0.1057** | ✅ UID 被否 → ordinal |
| server Snbs@150 | 同上 | 48,413 | 同 client(共享尾) | ✅ |
| server Sowi@16 | club t3 | 84,259 | **不可用**:t3 frame 未解析 | ⚠ 控制缺失 |

**Sowi 因此降为 candidate**:`club(84,259)` 与 `team(84,507)` 的 ordinal 域**同时** 100% 容纳
其存活值(顶值 84,242),而 club UID 集不可取 → 无法否掉 UID 编码、也无法在 club/team 间裁决。
其字段身份仅来自 t79 静态 getter `0x11864e8` → `+0x80`,fixup `0x3e44580` → table_3(引用)。

---

## 7. 负结果与不可判项(原样保留)

1. **u16 位字(flags@0 / @143)字内顺序不可判**:11 位恒 0,数据无法把 `Scov/Sush/Srrf/Nucf`
   分配到具体位。t79 静态给了位号,本任务不据此升档。
2. **8 个 pitch i16 槽(@25/27/29/31/54/56/58/60)域重叠**:解码后均为合理米制区间,
   数据**不能**在 8 个 `short_distance` 字段间裁决;仅 t79 静态定序。
3. **5 个打包日期槽(@37/41/45/131/135)**形状全部 100% 合法。尝试用业务序
   `Sbld <= Srbd <= Doco` 做数据判别:成立率仅 **77.1%**(年份单调 84.3%),**不足以定序**,
   故 5 槽全留 candidate。
4. **`Ssds` 侧翼子对象**:8×8B 记录,`capc@+0 / flags@+4 / sage@+5 / cond@+7`。
   t79 静态接通 11/12 子字段,但 `sage` 在 20,425 个值上违反 `min_value=0`,
   **不升档**,按整块 candidate 报告。
5. **`Sdtr@62`**:29,983/48,413 行原始值为 0,而 `enums['Sdtr']={1,2,3}`,getter 不钳不抑 →
   held(t79 同判)。
6. **`Splr@131` 4CC 大小写错配**:xml 是小写 `Splr`(no-op arm),实际打包日期由大写 `SplR`
   分发(t79 同判)。
7. **字符串/列表/子表/非 wire 字段不猜**:`Snam`(语言层)、`dbnm`(虚拟解析)、`Snti`
   (经 City 转发)、`Scpc`(table_22 子表)、`NDBC/FDBC`(编辑器元数据)、8×`Sh**` 站位
   (注册但无 getter)、`Shcc`(无 getter)——全部进 `held`,不进槽表。

---

## 8. 与 t79 的关系(边界声明)

`scripts/t79_stad_team_harvest.py` 是**同工作区兄弟任务**,做的是**静态二进制收割**
(`editor.exe` SHA-256 `b82ebe…dadab4`,L3)。本任务做的是**数据侧扫表**,两者**正交**:

- 本任务**未修改、未重跑** t79 任何产物;
- 引用处一律标 `t79 cited` 并在 `evidence` 里给出 `getter_fo` / `member_off`;
- 凡"数据不能决定、只有静态能定"的项,本任务**主动降档**为 candidate 而非借用 L3;
- 两侧独立得到同一锚点结论(`rdui@25` 实为行序数)。

因此本任务在 server 侧只产出 **11 个 L2/L2_structural + 2 L3(冻结锚点)**,而不是照抄 t79 的
41 L3。这是**证据分级的诚实结果**,不是覆盖不足。

---

## 9. 复现

```
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t76a_stadium_slots.py --selftest
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t76a_stadium_slots.py --all --check
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t76a/out/verify.py --json scratch/t76a/out/verify.json
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t01_anchors.py
```

结果:builder selftest 21/21;`--all --check` 双档 `closed`;verify **49/49**;
t01 anchors **7/7**。L4 = 0(未启动游戏/编辑器,未读 `Z:`,未联网)。
