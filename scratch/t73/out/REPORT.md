# t73 — 通用扫表工具 `t73_table_slot_mapper` + city/continent/region/currency 四表双档闭环

**8/8 (archive, table) 行框全部闭合,L2 槽位 17 个,L3 冻结锚点 14 个全部复核通过、零冲突。** city/continent/region 走定长 DP,currency 走变长 trailer walk;`verify.py` 44/44 独立通过;`t01_anchors.py` 7/7。L4=0,未启动游戏/编辑器/IDA。

## 1. 方法:从 t57/t59 抽成通用工具

三个纯函数层,`scripts/t73_mapper_core.py` 承载方法,`scripts/t73_table_slot_mapper.py` 只做 CLI 表面:

| 层 | 做什么 | 关键判据 |
|---|---|---|
| **行框闭合** `frame_closure` | 枚举 (H, F, S, p) 全组合 | 只接受**逐行**成立 `u32(ordinal)==row_index` **且** `u32(uid)==u32(uid)!=0`;算术闭合单独不算证据 |
| **别名规范化** `canonical_frame` | 把同 stride、同绝对 identity 位点的 (H,F) 归为一个 alias group | 组内 `(13,9)`/`(14,8)`/`(15,7)` 数据侧**不可区分**——这是结论,不是缺陷 |
| **槽位对齐** `align` | 类型宽度 × 值域 × 外键命中 | 不按 XML 顺序、不按"值长得像" |

### 1.1 关键否定结果(原文保留)

- **city `13 + 56293×43 + 9 = 2,420,621` 也成立,`14 + 43n + 8` 也成立,`15 + 43n + 7` 也成立。** 三者是同一 alias group,identity 位点分别是 row+31 / +30 / +29。**数据侧不能定 header 原点。**
- 定原点的判据不是算术,是 footer 的 flag 字节:只有 F=8 时 payload 末 8 B 读作 `[BE 1][u32 value]`。
  ```
  city   F=8  flag_be1=True  tail_le=2000341156
         F=9  flag_be1=False
         F=7  flag_be1=False
  continent / region 三档同样:仅 F=8 为 True
  ```
- `resolve_frame` 里的 `footer_last_eq_max_uid` 判据**只对 city(56,293 行)与 region(28 行)成立,对 continent(7 行)不成立**(`0x333e4 != 0x7`)。因此该判据**不写入**主判据集,只作为辅助观察记录在 `frames.json` 的 `footer` 字段里。这是本轮主动放弃的一条伪通用规则。
- `frames.json` 的 `header_origin_data_unique` 在 6 个定长归档上**全为 `false`**——数据侧从不唯一确定 header。canonical 取 `H=14` 的理由是:F=8 的 footer flag 判据 + 冻结锚点 `city Clat@1` 只有在 row base 14 时才是合法 f32 纬度。

## 2. 行框结果(8/8 closed)

| 表 | 档 | 封口 | 行宽 | identity 位点 | payload SHA-256 前缀 |
|---|---|---|---|---|---|
| city 2 | client | `14 + 56293×43 + 8 = 2,420,621` | 43 | row+30 | `66f8cc27cba587a0…` |
| city 2 | server | 同上 | 43 | row+30 | `66f8cc27cba587a0…` |
| continent 5 | client | `14 + 7×34 + 8 = 260` | 34 | row+21 | `8f888154ccd5a833…` |
| continent 5 | server | `14 + 7×48 + 8 = 358` | 48 | row+35 | `91ea610d3b96b6d0…` |
| region 19 | client | `14 + 28×45 + 8 = 1,282` | 45 | row+32 | `c6a5ac4aa4199a67…` |
| region 19 | server | `14 + 28×46 + 8 = 1,310` | 46 | row+33 | `05b73738dd216e51…` |
| currency 41 | client | `14 + Σrow + 8 = 74,352` (173 行) | 变长 | 行尾 −13 | `9963118f3d379291…` |
| currency 41 | server | 同上 | 变长 | 行尾 −13 | `9963118f3d379291…` |

**city 双档 payload 逐字节相同**(`raw_c == raw_s` 为 `True`),因此 city 的槽位结论对双档同时成立,不需要二次推导。continent/region/currency 双档 SHA 不同。

### 2.1 双档行宽差异:是发现,不是错误

- **continent**:server 行 `0:21` 与 client 行 `0:21` **逐字节相同**(7/7 行);server 行 `21:35` **全 `00`**(7/7 行);剩余尾段与 client 尾段相同。即 **server = client 业务字节 + 14 B 全零槽位**。`14 + 7×48 + 8 = 358` 成立。这 14 B 零列是 server 独有的零填充字段块,不是 stride 误判。
- **region**:server 比 client **每行多 1 B**,位于 row+32(client)/row+33(server)之前。server 在该位点常量为 `04`(28/28 行),client 对应字节取 `0xff` 或业务值。client 业务字节 `[1:32]` 与 server `[1:32]` 逐行相同。
- region 存在 `0xffffffff` 哨兵(如 row0 `0:12` 全 `ff`)——与合法 0 **分开记**,`classify_column` 的 `n_ff` 字段单列。

## 3. 槽位对齐结果

### 3.1 L2(本轮数据侧闭合,17 个)

| 表 | 字段 | 偏移 | 判据 |
|---|---|---|---|
| city | rdui | 30 | 列 == 行号,56,293/56,293 |
| city | duni | 34 | UID 对相等且非零,56,293/56,293 |
| continent s | rdui / duni | 35 / 39 | 同上,7/7 |
| region s | rdui / duni | 33 / 37 | 同上,28/28 |
| currency | Cnam | 行首 | 173/173 行解出可打印 UTF-8 币名 |
| currency | Cexr | 行首+34 | 字符串块后 f32,值域符合对 GBP 汇率 |
| currency | rdui / duni | 行尾 −13 / −9 | 173/173 行 trailer 自证 |

### 3.2 L3(冻结静态锚点,14 个复核全过)

`scripts/fm24_dump.py:FIELDS` + `scratch/t05/layouts.json` 的 city 全套在**本轮 payload 上重新验证**,`frozen_check` 记录 `checked=9, ok=9`:

```
city  Clat@1  Clon@5  Catt@9  Cnti@10  Cwea@14  Clgi@21  Clri@25  rdui@30  duni@34
continent  rdui@21  duni@25        region  rdui@32  duni@36
currency   rdui=-13  duni=-9
```

**零冲突。** city 的 `Clat@1` 独立佐证:该列 f32 值域 `[-54.813, 78.224]` 全落在 `[-90,90]`,而 `H=13` 或 `H=15` 时同一偏移读出 `4.8e7` 量级——这是 F=8 判据的第二个独立支撑。

### 3.3 unmapped(不硬凑)

| 表 | unmapped 字段 | 原因 |
|---|---|---|
| city | `NDBC` `FDBC` `Calt` | 幸存 u32 列值域不可区分 |
| city | `Cinh` | 3 个 byte 列都是 `Cinh` 枚举(16 值)域子集 |
| continent | `NDBC` `FDBC` | 同上 |
| continent | `Crgs` | 17 个 f32 列幸存 |
| continent | `DBvw` | 0 个 byte 列是枚举域子集(其枚举 4 值全为空名,不可判别) |
| region | `NDBC` `FDBC` | 同上 |
| currency | `NDBC` `FDBC` | 同上 |

`dbnm`/`Cnam`/`Rnam`/`C3ln` 等 string 字段统一进 `held`:`string/list 字段在独立长度前缀区,不是定宽槽`,不当作 unmapped 计入分母。

### 3.4 关键负结果:FK 一条也没命中

`Cnti`/`Clgi`/`Clri`/`Cwea` 的 FK 判定**全部落入 unmapped**,原因写实:

```
no u32 column hits nation (table_10) UID domain at rate 1.0
```

根因是本工具的 `reference_uids` 只对**定长表**能自证 identity;`nation(10)`/`language(8)`/`weather(27)`/`local_region(47)` 都是变长表,`canonical_frame` 返回 `resolved=False`,于是 FK 域为空、无法判命中。**这不是"这些字段没有槽",而是"本工具的 FK 判据在这四张目标表上无能力"。** 这四条已由 L3 冻结锚点给出偏移(`Cnti@10` 等),因此最终结论不受影响,但工具的这一能力缺口必须如实记账——不是用 L3 结果回头把 L2 说成"命中"。

## 4. 工具的已知边界(交第 2 波用)

1. **只对定长表能自证 identity。** 变长表(t10/t8/t27/t47…)`canonical_frame` 必然 `resolved=False`,必须走 `walk_var` 式专用文法。第 2 波扫 9 张表时,变长表要么补文法,要么直接 `escalate_to_sol`。
2. **enum 判定需要 scoped enum 有非空值名。** `continent DBvw` 的 4 个枚举值全为空名,`align` 无法把它当判据,只能 unmapped。这是 master.json 的数据缺陷,不是工具 bug。
3. **`footer_last_eq_max_uid` 不是通用判据。** 7 行表不成立。已从主判据集移除,仅作记录。
4. **city 34 秒 / 表(双档各一次)。** 耗时来自 `frame_closure` 对每个算术候选逐字节扫全表,56,293 行 × 1,355 个算术候选。第 2 波扫大表(city 规模)要预留时间,或先用 `EXTRA_FIXED` 先验收窄候选集。
5. **`--table` 只覆盖 2/5/19/41。** 其余表号走 `build` 的 `xml is None` 分支,返回 `slots="escalate_to_sol"`,不猜实体。

## 5. 交付与复跑

```text
FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t73_table_slot_mapper.py --selftest
py -V:3.12 -I -B scripts/t73_table_slot_mapper.py --table 2 --archive client --json scratch/t73/out/slots_client_2.json
py -V:3.12 -I -B scratch/t73/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```

| 交付物 | 内容 |
|---|---|
| `scripts/t73_mapper_core.py` | 方法层:载荷解码复用、行框 DP、alias 规范化、变长 walker、列 profiling、字段对齐、冻结锚点复核、双档差分 |
| `scripts/t73_table_slot_mapper.py` | CLI 壳:`--table/--archive/--json/--selftest`,退出码 0/1/2 |
| `scratch/t73/out/frames.json` | 8 个 (archive,table) 行框 + alias group + footer 敏感性 + 双档 SHA |
| `scratch/t73/out/slots_{client,server}_{2,5,19,41}.json` | 8 份槽位表(槽位→字段候选+等级+证据+unmapped+held+逐列 profiling) |
| `scratch/t73/out/verify.py` | 独立复核,不 import builder,44/44 |
| `scratch/t73/out/REPORT.md` / `DONE.md` | 本报告 |

## 6. 复跑结果

- `--selftest`:`selftest ok`,exit 0(合成表验证行框、alias、变长 walker、schema 装载)
- `verify.py`:**44/44 checks passed**,exit 0
- `t01_anchors.py`:**7/7 checks passed**,exit 0
- 8 个 `build()` 全部 `status=closed`,exit 0

L4=0。未启动游戏/编辑器/IDA,未访问 `Z:`。
