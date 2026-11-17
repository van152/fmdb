# b41 交接：people_db 位置向量与 PDxx 属性

## 交付状态

分支：`work/b41-attrblock`。本任务按“位置结构部分解码 + PDxx 明确负结果”交付；**未完成完整位置码顺序或属性字段解码**，不满足完整属性验收线。

本分支关键提交：

| Commit | 内容 |
|---|---|
| `cf2ecf1f3e3b88ddd38145d92917cb975ba94257` | 当前源严格行链修正、people 属性/位置探针及机器可读结果、字段报告更新 |
| `a1d1f50b2f5662254d786cd107f07b38a8c72f58` | 将位置结论限定到可独立复核的锚点，纠正过度映射表述 |

在交接文件提交前，HEAD 为 `a1d1f50b2f5662254d786cd107f07b38a8c72f58`；本 HANDOFF 与进度记录随后作为独立文档提交入本分支。

## 交付文件

- `scripts/modding_people_attrs.py`：只读 current-source 探针，提供 `--selftest`、`--verify`、`--map`、`--person`。不读写旧 `tmp_b36` 缓存，不写 archive。
- `reports/dbdat_decode/PEOPLE_ATTRS.md`：位置向量部分证据、PDxx 负结果、参照缺口及重跑命令。
- `reports/dbdat_decode/people_attr_map.json`、`people_attr_verify.json`：候选字段映射、逐 variant 统计、样本和验收边界；均标明 `full_task_acceptance: false`。
- `scripts/modding_people_fields.py` 与 `PEOPLE_FIELDS.md`、`people_field_map.json`、`people_field_verify.json`：修正 basic ordinal→PID 数据源和 strict row-chain；旧 full-pop Pcti/Pcjd 计数已撤回，不可沿用。
- `tmp_b41/PROGRESS.md`：阶段记录与验证结果。

## 核心结果与证据等级

### 当前数据源链（L1）

使用当前 basic 原件 ordinal→PID 对照重建 **658,011** 行；people_db 连续覆盖 offset **6..400,443,942**，尾余28 B。variant 分布 v1=166,064、v2=476,158、v3=4,757、v4=9,839、v5=1,193。旧 `D:\tmp2b\fm24\tmp_b36\rows.pkl`/`basic_walk.npy` 与当前 basic 不匹配，保留只读且不作统计来源。

### 位置向量（L1 结构 + 部分 L2）

- v2/v3 共480,915行；row+34、row+36..+48 共14个 byte 槽全在0..20，row+35恒为1。后者仅称 marker/delimiter 候选。
- FM Scout `rev=24.0` 的 **8/8** 可复核 `Natural 20` 单点核对成功，覆盖四个字段码：Pdmc@+39、Pmce@+41、Pamr@+45、Pace@+46。版本与本地24.3.0有差异，不宣称整库逐版相同。
- Pgoa@+34（公开 GK 角色/高行值）和 Pdce@+37（Sergio Ramos中后卫角色/本地值）只保留较低置信候选，不计为精确 Natural-20 锚。
- 14码候选排列保留在 machine map；其余8码没有独立精确锚，**完整字段顺序仍未确认**。0值是无胜任力、缺失还是默认值也未区分。
- `--verify` 抽样20个具名v2/v3行，20/20能定位；宽口径常用位置存在性检查20/20。该类别检查不是逐字段解码证据。

### PDxx 属性（L1 候选统计；无属性 L2）

- v2/v3 row+49..+102 的54 B候选窗：476,529/480,915行全窗≤20（99.0880%）；零值20,676,436/25,969,410 cells（79.6184%）；越界byte 252=67、253=2,764、254=7,291、255=3,016。
- 没有任何 PDxx `byte_index` 可交付（0/40核心字段）；54个player_attribute字段顺序、边界及0值语义未解。该普查只说明窗口值域现象，不是属性解码器。
- v1另有 row+21 u8[54] 与 row+22 u16[14] 范围候选，但零值比例更高，未确认其字段语义；v2/v3布局不套用到v1。
- 未找到可逐值核对的同版原始1..20属性真值表；属性 L2 样本数为0，full task acceptance为false。

### 既有字段（L1/L2 边界）

- `modding_people_fields.py --verify` 当前行链22/22身高、体重、DOB样本均解出；身高与公开值精确16/22、体重15/22，`|Δ|≤2 cm` 身高22/22、`|Δ|≤6 kg` 体重22/22。C. Ronaldo 使用 PID 735216 加唯一公开 packed-DOB 候选定位，不等同常规姓名锚。
- Pcex：签名命中448,255/658,011；真实日期249,701、1900-01-01 null哨兵198,554、整块缺席209,756。
- CA/PA 5×u16仍为 medium（值候选）/weak（字段名）；未找到第三个独立精确源。Pcti/Pcjd旧全量统计已撤回，必须等待严格当前链重跑后才能恢复。

## 验证与边界

- `py -V:3.12 -I scripts/modding_people_attrs.py --selftest`：12/12 PASS；`--verify`：20/20样本、8/8 Natural-20检查；仅表示当前结构/候选和指定锚检查成功。
- `py -V:3.12 -I scripts/modding_people_fields.py --verify`：命令退出码0；当前链22/22身高体重/DOB样本成功。
- `py -V:3.12 -I scripts/run_regression.py`：12/12 PASS，0 FAIL，0 SKIP（177.4s）。
- **L4=0**。未启动游戏/编辑器、未写游戏或用户目录、未访问 b42 独占 IDA 库。

## 下一步

1. 如继续位置研究，优先补齐8个未定码位和完整14码顺序的独立精确位置锚，并查明0值语义。
2. 如继续属性研究，先寻找同版原始1..20属性真值或等价独立参照；否则不填PDxx byte index。可再考虑 exe 静态 L3，但不得将静态猜测表述为L4。
3. 对当前 basic 严格链重跑 Pcti/Pcjd 全量统计；在重跑前沿用“旧计数撤回”的报告状态。
4. CA/PA 名称维持 medium/weak，除非找到第三个独立精确来源。
