# t13e 旁路任务：整理"已知实体基数清单"供交叉核对

## 性质说明

这是**旁路资料整理**，不是主线。主线（luna 的 t13）会自己查基数出处；你的清单只作交叉核对用。**你没有产出也不阻塞任何事**，所以尽快交付，不要追求穷尽。

## 任务

从本仓已有工件里收集"实体 → 已知行数基数"，产出一份带出处的清单。

### 必查文件（只读）

| 文件 | 能拿到什么 |
|---|---|
| `scratch/t05/COVERAGE.json` | 79 条表覆盖记录，含 `table_id / archive / count / equation` |
| `scratch/t01/stage2_three_way.json` | 21 个已定表型 → `entity_tag` / `field_count` |
| `scratch/t05/layouts.json` | 26 个实体的布局（业务宽度、档数）|
| `scratch/t01/LEDGER.json` | E30/E42/E47 等条目里有 city 56,293、weather 334、language 126、nation 251、injury 115、lcrg 2,488 等锚点数 |
| `reports/t01f_comp_row_offsets.md` | comp 7,047 行 |

### 输出格式

```json
{"entity":"city", "count":56293, "source":"scratch/t05/COVERAGE.json:table_2", "cross_check":"E42 city 列画像同为 56293", "reliability":"high|mid|low"}
```

同一实体若有多个来源且数字冲突，**两个都保留**并标 `conflict: true`，不要自行选一个。

## 交付（只写 `scratch/t13e/out/`）

1. `baselines.json` —— 清单，顶层 `"status"`。
2. `baselines.md` —— 人读表格，按实体名字排序，标出冲突项。

## 硬约束

- 只写 `scratch/t13e/out/`，其他目录只读。
- `py -V:3.12 -I`；不许联网。
- 数字必须带**具体出处**（文件名 + table_id 或 E 编号），没有出处的不要写进去。
- **你是旁路，卡住就把已有的部分写盘标 `"status":"partial"` 并结束。**
