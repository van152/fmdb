# t18 行↔对象偏移桥报告

## 结论

- 黄金行侧布局一致：113/113 = 100.00%；comp、weather、city 均通过。此分数只表示三个黄金基线的行侧布局校验，不把未覆盖实体冒充为通过。
- t16b 原始 G1：12/237 = 5.06%；该旧数仍保留为旧口径，新的黄金布局校验不能反向改写它。
- 主假设方向成立：对象成员偏移与 `.dat` 行内偏移不是可直接比较的坐标。Δ 样本不恒定；不得用单一平移量修补全实体。
- club 命名率：14/672 = 2.08%；本任务没有把候选升级为新命名字段，因此变化为 0 个字段、0 个百分点。

## 假设验证过程（按顺序）

1. **序列化顺序**：city 的 t16 serializer widths 按指令顺序累加为 42B，名字段落在 Clat/Clon@1/5、Catt@9、Cnti@10、Cwea@14、Clgi@21、Clri@25；与 E55 7 个唯一命名字段一致。
2. **comp 反例与修正**：直接把 t16 的 9 个稀疏 walk 事件当成完整行序累加，比较 E20 对象↔行锚点仅 2/8 命中；不能还原条件分支省略的字段，原始 naive walk 不作为结论。采用 E20 `cursor_layout` 的 46 个序列化步骤逐宽度累加，业务 18 字段全部与 E20 row map 相符，游标到 +126，含一字节 framing 后 stride=127。
3. **reader 槽佐证**：city 的 t05 reader 10 槽宽度序列与 t16 walk 逐项相同（总计 42B）；其中前 9 槽 30B business，末槽 12B identity。weather reader 前缀三字节 + 季节 loop（2+21×1=23B）与 E27 四季 92B 行侧字段一致。
4. **stride 封口**：city 30B business + 12B identity + 1B marker = stride 43；comp 126B row body + 1B framing = 127；weather 是变长行，公式 `row_start + 7 + name_byte_length + 92 + 12 + 1` = `row_start + 112 + name_byte_length`，与 E27 recurrence 一致。
5. **Δ 拟合**：comp/city/club object-row 差值样本不恒定；weather 的对象成员与行偏移差为 `25+season-name_byte_length`，受变长名称影响。E36 任务书给出的 club 样本 `Cccn row+8 / object+0xf0` 对应 Δ=232，只是单字段样本；此处仅按任务书引述，未独立复核其快照来源。

## 假设及证伪尝试原文记录

> 核心假设：`t16b` 的 walk 给出的是 C++ 对象内偏移（vtable 之后）；E55/E27/E20 基线是 `.dat` 行内偏移。

> 证伪尝试：将 t16 comp walk 按报告中的静态事件顺序直接累加，检查是否直接封口至业务字段 row offset。结果失败：该 walk 是稀疏/条件路径事件，9 个事件漏过颜色、统计块和若干引用字段；不能把这些事件简单当作完整 serializer 顺序。

> 修正检验：使用 E20 明确列出的逐字段 cursor steps（包含显式版本字节及条件块）累计，18/18 row map 对齐且 stride 封口；city 的 walk 与 reader 宽度序列互验；weather 由 reader loop 与 E27 变长 row 公式互验。故证伪的是“直接累加稀疏 t16 walk 足够”，而不是“对象偏移等于行偏移”。

## 结果

| entity | 行侧一致 | stride | row_base |
|---|---:|---|---|
| comp | 18/18 | pass | 0 |
| weat | 88/88 | pass | `row_start+7+name_byte_length` |
| city | 7/7 | pass | 0 |

字段台账已按行坐标重生成；其余实体 stride/一致率标记为未验证，不将缺少独立行布局证据写成通过。机读细节见 `bridge.json` 与 `fields_<tag>.json`（大表使用分片）。
