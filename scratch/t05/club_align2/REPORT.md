# t05b2 字段对齐器报告

输出目录：`scratch/t05/club_align2/`

## 结论

- 阶段 A：**PASS**。award 3/3、city 6/6、stadium 6/6、injury 3/3 锚点命中；各业务区宽度分别为 64/30/25/3 B。
- 已用 `fm24_dump.py` 对四张表的 **108,366 行**逐行重检：定长闭合、`rdui == 行号`、`duni` 两个 u32 重复；带 marker 的表也逐行检查 marker=0。city 另逐行验证 `Cnti@10` 后三字节为零，并核验四个 named_rows 的 `rdui/Cnti/duni_lo`。
- 阶段 B：**partial**。只在 `club_fields.json` 汇总已提供的 `Cccn u32@+8`；不声称达到 15 字段目标，列表项宽未推断。
- 最终命名计数：club 1 个（`Cccn`，既有 L3 证据；本轮未新增）。

## 算法

1. 从 `schema_inventory.json` 读取顶层非列表标量及原始保序、类型宽度候选。`duni/rdui` 按已验证的身份尾结构移出业务 DP；列表不参与线宽分配。
2. 业务区大小按 `stride - 13` 得出。DP 的状态为“已处理字段 × 已消费业务字节数”，对每个宽度候选累加统计得分；只允许一个字段占用连续字节。保留前三个完整宽度解。
3. 宽度 0 表示“此字段尚未定位/可能共享存储”，不表示证明了字段缺失。所有非锚点字段在主 assignment 中保持 unresolved；DP 的非锚点命名仅作为 `top_solutions` 中的**未验证假设**，不当作结论。
4. 锚点从 `fixtures_truth.json` 读取，遍历候选位置并按精确命中加分；锚点解以命中数优先、得分次之。搜索函数与 `validate_fixture()` 分开；验证器独立核对偏移、宽度、样例值、闭合及全行身份。
5. 非锚点 DP 字段保序。经真值锚定的字段单独占用已验证字节窗口，故可能打断 schema 顺序；这不是把锚点写死进程序，也不会将未锚定字段错误命名。`order_violations` 记录 DP 假设中的该现象。

### 评分表

| 条件 | 得分 |
|---|---:|
| boolean：u8 仅取 0/1 | +3 |
| boolean：不符 | -5 |
| enum/day_of_week/multiple_enum：1B 值域较小且近似连续 | +2 |
| enum 类：1B 统计不符 / 2或4B | -1 / +0.2 |
| database_record_unique_id：u32 `ref_lt_N >= 0.8` / 缺该统计 / 低于阈值 | +3 / 0 / -2 |
| real：f32 全有限、量级合理且非全零 | +2；否则 -2 |
| date：u16 统计可用的保守代理 | +0.5 |
| integer/cash/short_distance/player_attribute：1/2/其他B | +1 / +0.7 / +0.2 |
| string/picture 4B；colour 3或4B | +0.15；+0.1 |
| unresolved 0B | -0.08 |
| 锚点精确命中；业务区闭合 | +10/锚点；+1 |

`date` 的画像不含足以识别具体日期纪元的数据，因此这里只使用保守代理分，不能视为日期语义验证。统计得分只用于排序候选，不构成独立字段证据。

## 阶段 A 结果

| 夹具 | 业务区 | anchors_hit | 闭合 | 全行验证 | DP 最优分 |
|---|---:|---:|---|---|---:|
| award | 64 B | 3/3 | PASS | 3545/3545 | 63.64 |
| city | 30 B | 6/6 | PASS | 56293/56293 | 69.84 |
| stadium | 25 B | 6/6 | PASS | 48413/48413 | 76.80 |
| injury | 3 B | 3/3 | PASS | 115/115 | 34.24 |

主 assignment 只命名已锚定字段；其余字段为宽度 0，剩余字节列入 `unresolved_wire`。这使每个夹具业务区的 assignment 宽度和恰为业务区大小，同时不把仅由列画像产生的低置信候选冒充已验证偏移。每夹具前三个统计 DP 假设保存在 `fixtures_result.json` 的 `top_solutions`，并明确标记 `candidate_only`。

city 的主 assignment 命中 `Clat@1/4`、`Clon@5/4`、`Cnti@10/1`。此次没有把 `Cnti` 与 schema 声明的 u32 reader 宽度冲突化：全 56,293 行 `off11..13` 均为 0，故从 `off10` 读取 u8 或 u32 得到相同值。Liverpool、Manchester、Madrid、München 的真值行也都匹配。`Cnti` 的业务锚点宽度按 truth 记录为 1；这不否定 reader 可能执行 u32 读取。

award/stadium/injury 的 `rdui/duni` 身份字段在 assignment 中按 13B 身份尾表示；`duni` 为两个相等 u32。identity anchors 不计入业务区 `total_width`。

## 阶段 B / 未解

`club_fields.json` 状态为 `partial`：携带用户指定的既有证据 `Cccn u32@+8`（L3），不把它计作本轮新发现。其余 385 个 scalar 字段未映射，list 计数/项宽推断未开展。club 的 0.21 B/scalar 不能支持固定宽度逐字段分配，故不硬凑。

上一轮 t05b 因 `Cnti` 锚点与 schema 顺序、u8 与 u32 reader 宽度的误读而报 0/5。本次以 `fixtures_truth.json` 为硬约束输入，并对 city 的零填充与 named_rows 做了全量核验；该所谓宽度冲突不再是阻塞项。schema 顺序只用于非锚点字段 DP，并把锚定字段的顺序例外显式报告。

## 交付文件

- `align.py`：`--selftest`、`--entity <name>`、`--json`；selftest 全行验证并写 `fixtures_result.json`。
- `fixtures_result.json`：PASS、四夹具锚点与业务宽度、assignment、前三个 DP 候选和验证信息。
- `club_fields.json`：阶段 B partial 结论。
- `REPORT.md`：本报告。
