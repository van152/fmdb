# b41 — people_db 位置向量与 PDxx 属性族研究（PEOPLE_ATTRS）

## 摘要与验收状态

**位置向量：variant 2/3 的 14 槽结构已确立，但完整字段顺序仍是候选；只有部分字段码获得独立位置锚。PDxx 属性：明确负结果，逐字段 byte index 数为 0。** 本任务走“明确负结果报告”分支，不宣称属性解码完成。

- 当前 basic ordinal→PID 对照重建 people_db **658,011** 行；旧 `tmp_b36` 行缓存与当前 basic 原件失配，不作统计来源。
- v2/v3 位置候选位于 row+34、row+36..+48，共14个 byte；row+35 恒为1。480,915/480,915 行各槽都在0..20。
- 8个可独立复核的 FM Scout `Natural 20` 对照吻合4个字段码（Pdmc、Pmce、Pamr、Pace）；Pgoa/Pdce另有较低置信度角色候选。其余位置码未独立定级。
- row+49..+102 的54 B属性窗仅为范围候选；40个核心 PDxx 和其他14个 player_attribute 字段的 byte index 均留空。属性 L2 样本数为0。
- `PEOPLE_FIELDS.md` 中 CA/PA 仍为 medium（值候选）/weak（字段名）；没有第三个独立精确来源。`L4=0`，未启动游戏或编辑器。

交付：`scripts/modding_people_attrs.py`、`people_attr_map.json`、`people_attr_verify.json`。`--verify` 的 PASS 只代表当前行链、结构和列明的位置锚检查成功；**不代表完整位置码顺序或 PDxx 语义已解出**。

## 1. 数据源与行链

- 输入（只读）：`archive/people_bins/people_db_streamed_b22.bin` 400,443,970 B；`basic_people_db.uncompressed.bin` 54,060,043 B。
- 由当前 basic ordinal→PID 与 people 行尾 `<u32 ordinal><u32 PID><u32 PID>` 重建：658,011 个唯一行，覆盖 offset 6..400,443,942，尾余28 B。行 variant：v1=166,064、v2=476,158、v3=4,757、v4=9,839、v5=1,193。
- 旧 `<OLD_REPO>\tmp_b36\rows.pkl` / `basic_walk.npy` 的 ordinal 0→PID 为50,331,648，当前 basic 原件为PID 3；旧索引有4,312个 ordinal-0 假命中且首行从trailer offset45起算。脚本不读写这些缓存。

## 2. Variant 2/3 位置向量

### 2.1 L1 结构

- v2/v3 共480,915行；row+34、row+36..+48 的14个位置槽均在0..20，逐variant全量符合。
- row+35 在v2 476,158/476,158、v3 4,757/4,757行恒为1，是标记/分隔候选；确切用途未解。
- 20个具名 v2/v3 行的候选常用位置槽均至少有一个值≥10。此宽口径存在性检查只是候选布局的合理性辅助，不能替代精确位置码锚定。

### 2.2 独立 L2 锚点与候选顺序

以下8个 FM Scout FM24 `rev=24.0` 页面给出UID匹配的 `Natural 20` 标签；本地PID对应槽值均为20。该网页版本与本地24.3.0不保证同一补丁，因此只作独立位置码锚点，不外推为整库等值。

| Schema码 | 位置 | people_db偏移 | 独立 Natural-20 样本 | 本地值 |
|---|---|---:|---|---:|
| Pdmc | DM | +39 | [Busquets](https://www.fmscout.com/player/1510566/sergio-busquets.html?rev=24.0)、[Kimmich](https://www.fmscout.com/player/92039023/joshua-kimmich.html?rev=24.0) | 20 |
| Pmce | MC | +41 | [Bellingham](https://www.fmscout.com/player/29232937/jude-bellingham.html?rev=24.0)、[Valverde](https://www.fmscout.com/player/78074594/federico-valverde.html?rev=24.0) | 20 |
| Pamr | AMR | +45 | [Messi](https://www.fmscout.com/player/7458500/lionel-messi.html?rev=24.0) | 20 |
| Pace | ST | +46 | [Mbappé](https://www.fmscout.com/player/85139014/kylian-mbapp%C3%A9.html?rev=24.0)、[Haaland](https://www.fmscout.com/player/29179241/erling-haaland.html?rev=24.0)、[Kane](https://www.fmscout.com/player/28049320/harry-kane.html?rev=24.0) | 20 |

8/8单点检查覆盖4个字段码。Pgoa@+34 有 Neuer/De Gea/Courtois 的公开 GK 角色及本地高值支持，Pdce@+37 有 Sergio Ramos 中后卫角色及本地值支持；两者为较低置信候选，不计入上述精确 Natural-20 检查。追加实时检索未能独立确认其他位置页，未核实字段不计为L2。

机读 map 保留一个 schema-driven 候选顺序：Pgoa@34、Pdls@36、Pdce@37、Pdrs@38、Pdmc@39、Pmls@40、Pmce@41、Pmrs@42、Paml@43、Pamc@44、Pamr@45、Pace@46、Pwbl@47、Pwbr@48。只有 Pdmc/Pmce/Pamr/Pace 有精确 Natural-20 锚；Pgoa/Pdce 是较低置信角色候选。余下8码无独立精确锚，候选顺序**不作为完整L2映射**。0表示“无胜任力”还是“缺失/默认”也未解。

## 3. Variant 2/3：54 B 属性候选与负结果

### 3.1 全量分层统计（L1）

候选窗口是 row+49..+102（54 B）。`player.xml` schema 有54个 `player_attribute` 字段：core40=mental17、physical9、technical14；其他14项为 PDvt、GK专属11项、脚偏2项。长度相等、值域相似不能证明窗口边界或字段顺序。

| variant | 行数 | 54 B全窗≤20 | 比例 | 零cell比例 | >20 byte计数 |
|---|---:|---:|---:|---:|---|
| v2 | 476,158 | 471,802 | 99.0852% | 79.7347% | 252=67、253=2,760、254=7,245、255=2,968 |
| v3 | 4,757 | 4,727 | 99.3694% | 67.9809% | 253=4、254=46、255=48 |
| **合计** | **480,915** | **476,529** | **99.0880%** | **79.6184%** | **252=67、253=2,764、254=7,291、255=3,016** |

共20,676,436/25,969,410 cells为0。**54个 player_attribute 字段中可交付 byte index 为0；40个核心字段 L2 样本数也为0。** 不能将 raw window byte 指派为 PDag、PDpc 等，也没有证据可将候选窗拆成 core40 与 additional14。`--person` 输出的是L1原始候选值，不是属性解码。

### 3.2 Variant 1 单独布局

- row+5..+120 的 u8[54] 范围扫描最高候选为 row+21：161,970/166,064 行全窗≤20（97.5347%），但54×v1 cells中91.2962%为0。
- row+22 的 u16[14] 候选：132,431/166,064行全窗≤20（79.7470%），零cell比例86.1803%。两者都保留为稀疏/混合候选，不认定为属性或位置数组；v2/v3偏移不套用到v1。
- 没有原始属性参照，无法判断0是合法属性值还是未设置哨兵。GK位置槽的0值不能解释PDxx候选窗的零值。

## 4. 排除路径、公开参照缺口与剩余候选

1. **旧缓存**：旧 `rows.pkl/basic_walk.npy` 与当前basic源失配，不作任何全量偏移统计来源。
2. **滑窗与范围扫描**：row+49..+102范围很像属性族，但零值占79.62%、存在252..255越界值，不能定语义/边界。v1的+21 u8[54]、+22 u16[14]也保留为候选。
3. **schema猜码**：schema列字段名和40/14分组，不提供people_db序列化顺序；按schema顺序填byte index属于猜测，已排除。
4. **公开属性数据**：FM Scout rev=24.0提供位置Natural-20标签，不提供40个原始属性；EFEM 24.3.0提供0–100归一化属性组/位置分，不是1–20原值（如[Leão页](https://efem.club/players/83111483-Rafael-Le%C3%A3o)）。GitHub `MadsMarius/FM24` CSV仅38行Sandnes Ulf样本，无目标球员且无版本固定证明。没有找到可逐值核对至少10人的公开原始1..20属性表。
5. **本地表/CA-PA**：已解码的client_db小表不是PDxx真值表；未找到第三个独立精确CA/PA来源，5×u16仍为medium（值候选）/weak（字段名）。
6. **L3/L4边界**：本阶段不访问b42独占IDA库；未用exe静态结果支持PDxx顺序。未启动游戏/编辑器，L4仍为0。

剩余候选为 v2/v3 row+49..+102 54 B、v1 row+21 u8[54]/+22 u16[14]，以及其他变长字段流。缺少同版原始属性真值表，不能满足属性字段逐码核验线；因此本报告明确走负结果分支，不虚报验证通过。

## 5. 机读映射与重跑

`people_attr_map.json`列候选位置顺序、逐variant直方图、6个部分支持码位（4个精确Natural-20码）、54 B属性候选分布；全部PDxx `byte_index`为null。`people_attr_verify.json`包含20个具名v2/v3向量、8/8可复核Natural-20对照、候选宽口径角色检查，并注明 `full_task_acceptance: false`。

```powershell
py -V:3.12 -I scripts/modding_people_attrs.py --help
py -V:3.12 -I scripts/modding_people_attrs.py --selftest
py -V:3.12 -I scripts/modding_people_attrs.py --verify
py -V:3.12 -I scripts/modding_people_attrs.py --map
py -V:3.12 -I scripts/modding_people_attrs.py --person 7458500
```

`--selftest` 12/12 PASS只代表当前链、候选槽顺序形状、指定位置锚及候选窗统计符合预期；不代表14码全量定级或PDxx语义完成。