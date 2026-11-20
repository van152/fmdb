# t06 任务书：用已证布局做批量半自动字段命名

## 背景（必读，全部是已验证事实）

本仓已完成两件事，它们是本任务的地基，**不得推翻、不得重算**：

1. **行边界全覆盖**：client 20/20、server 58/59 精确闭合（见 `scratch/t05/COVERAGE.md`、`scratch/t05/server_bounds/boundaries.json`）。
2. **字段布局机械化产出**：`scratch/t05/layouts.json` 给出 **26 个实体、240 条**行内字段槽，
   每槽有确定的 `row_off` 与 `width`。这些值由 `editor.exe` 里 reader 的
   `lea rdx,[obj+OFF]` + `mov r8d,W` + `call [rax+0x28]` 指令流累加得出，
   并用 `sum(widths) == 业务区宽度 == stride - 13` 做硬闭包断言。

三条已证校验（**务必用它们自查，不许绕过**）：

- **regi(type19)**：自动布局偏移 `0,4,8,12,16,20,24,28` 与 `scratch/t02/regi_reference.json` 里人工解的 9 字段**逐一精确吻合**（server 多出的 `+1B@32` 是 boundary marker）。
- **city(type2)**：自动布局偏移 `0,1,9,10,14,18,21,25,29` 与 `scratch/t02/city_reference.json` 的 12 个业务字段**逐一吻合**（唯一差异：reader 用一次 `mov r8d,8` 合并写 Clat+Clon 两个相邻 f32，故 9 槽 vs 10 字段）。
- **injury(type6)**：21 槽已用 4CC getter 命名 11 个，且**每个都通过了数据语义验证**（见下"校准集"）。

## 你的任务

对**没有 4CC 分发链**的实体，用"**数据类型 + 列统计 + schema 类型约束**"把
`layouts.json` 里的槽位分配给 `schema_inventory.json` 里的具体字段名。

**硬性约束（违反即失败）**：

1. **不得修改任何 `row_off` 或 `width`**。它们已由 exe 指令流确定并有闭包背书。
   你只输出「槽 idx → 字段代码」的分配。
2. **不得使用 schema 的原始顺序作为行内顺序**。E38 已证伪该假设
   （injury 的 7 个 0/1 列位置是 `2,6,8,9,10,11,22`，而 schema 保序推导是 `9,10,17,18,19,20,21`，完全不符）。
   行内顺序由 reader 决定，而 layouts.json 已给出该顺序。你要做的是**多对多分配**（带类型约束的二分匹配），不是对齐。
3. **每个分配必须给出数据证据**（值域/是否 0-1/是否 f32 有限/是否引用型/是否哨兵值 0xFF）。
4. **不确定就标 `unresolved`**，禁止硬凑。宁可少命名，不许错命名。

## 校准集（必须原样保留，作为你的正确性基准）

injury(type6) server 已证命名（4CC getter 直证 + 数据验证双背书）：

| row_off | width | 字段 | 语义 | 数据实测 |
|---:|---:|---|---|---|
| 0 | 1 | `icla` | Classification | 值域 1–13，11 种 |
| 3 | 2 | `Imnd` | Minimum Days | 值域 1–180，22 种 |
| 5 | 2 | `Imio` | (文档无，exe 有) | 值域 3–290，29 种 |
| 8 | 1 | `Irec` | Recurring | 严格 {0,1} |
| 17 | 1 | `Imip` | Match Injury Percentage | 值域 0–90，10 种 |
| 21 | 1 | `Icms` | Season | **恰为 {0,1,2,3} 四季** |
| 23 | 1 | `inSr` | Seriousness | 1–5 五级 |
| 25 | 1 | `Icdp` | Central Defender Percentage | {50,255}，0xFF=不适用 |
| 26 | 1 | `Icdo` | (文档无，exe 有) | 1–51 |

city/regi 的已解字段（`scratch/t02/*_reference.json`）同样是校准集。

## 优先目标（按价值排序）

| 优先 | 实体 | 槽数 | 业务区 | 可用 schema | 备注 |
|---:|---|---:|---:|---|---|
| 1 | city (type2) | 9 | 30B / 43B 行 | 13 个标量 | 有 12 已解字段可当 ground truth，**必须先做到 100% 复现** |
| 2 | regi (type19) | 8/9 | 32/33B | 9 个标量 | 已有 9 已解字段，同上 |
| 3 | stad (type21) | 19 | 25B | 40 个标量 | 无 ground truth，低值域多 |
| 4 | lcrg (type47) | 18 | 31B | 无 schema | 只能出类型画像，不出名 |
| 5 | 其余 19 个未命名实体 | — | — | 多数无 schema | 只做类型画像即可 |

## 可用输入（都在仓内，只读）

- `scratch/t05/layouts.json` —— 240 条槽（`archives.{client,server}.fields[]`，含 `row_off`/`width`）
- `scratch/t05/schema_inventory.json` —— 32 实体、1968 标量，含字段代码/类型/原始顺序
- `scratch/t05/profile_*.json` —— award/city/stadium/injury 的逐偏移列统计
- `scripts/t05_profile.py` —— **列画像器，你应该用它为更多表生成画像**（见下方命令）
- `scripts/fm24_dump.py` —— 权威取数器（`load_payload(codec, archive, tid)` + `fixed_specs()`）
- `scratch/t05/server_bounds/boundaries.json` —— 变长表的行文法
- `scratch/t05/COVERAGE.json` —— 每表 count/stride/闭合状态

生成新画像的命令（照抄，别自己写解压）：

```
py -V:3.12 -I -B scripts/t05_profile.py --archive server --table 6 --auto --json scratch/t05/profile_srv6_injury.json
py -V:3.12 -I -B scripts/t05_profile.py --archive client --table 2 --auto --json scratch/t05/profile_city.json
```

## 类型判据（用数据裁决，不靠猜）

| schema 类型 | 数据侧必须满足 |
|---|---|
| `boolean` | 该列严格只取 {0,1}（或高比例 0xFF 时考虑 0xFF=true 变体） |
| `enum` / `multiple_enum` | distinct 小（≤ 字段的合法值数），近似连续，无 f32 解释 |
| `real` | 4 字节 f32 全部有限，量级合理；**单字节列不可能是 real** |
| `integer` 类 | 1/2/4 字节整数；百分比类值域 0–100 或含 0xFF/0xFFFF 哨兵 |
| `string` / `picture` | 通常 4B 引用（`ref_lt_N` 高）；也可能整个不占行内（见 injury：`Inam`/`Isnm` 不占槽，名称经 `duni` 关联 lang 表） |
| `database_record_unique_id` | u32 且 `ref_lt_N ≥ 0.8` |

**重要**：schema 声明的字段数常常多于槽数，说明部分字段不占行内空间（走引用/外部表）。
不要为了凑数把一个字段硬塞进多个槽。

## 交付物

写到 `scratch/t06/out/`：

1. `assignments.json`
   ```json
   {"entity": "city", "type_id": 2, "archive": "client",
    "business_width": 30,
    "slots": [{"idx":0,"row_off":0,"width":1,"code":"NDBC","confidence":"high",
               "evidence":"值域 {0,1,2}，distinct=3；schema 类型 integer"},
              {"idx":1,"row_off":1,"width":8,"code":"<Clat+Clon 合并>","confidence":"high",
               "evidence":"f32 双精度对，值域 -32.16..54.98 / -174.35..179.99"}]}
   ```
2. `REPORT.md` —— 每个实体的分配表 + 未解析槽及原因 + 与校准集的差异（必须为 0）
3. `verify.py` —— 可复跑自检：
   - 校准集 100% 复现（city 的 Cnti@10、regi 全部、injury 的 9 条表）
   - 每个 high 置信分配的类型判据通过
   - 不得修改 row_off/width（与 layouts.json 逐槽比对）

## 验收门槛

- city 与 regi 的已解字段 **100% 复现**（错一个即整体 FAIL）
- injury 的 9 条已证命名 **原样保留不改**
- `verify.py --selftest` 退出码 0
- REPORT 里明确列出哪些槽 unresolved 及原因

## 纪律

- **第一步就落盘骨架**（`assignments.json` 先写 `{"status":"in_progress"}`，边做边覆盖），
  防止超时丢失。完成时把 status 改成 `complete_<限定词>`（如 `complete_city_regi_exact`）。
- 只读输入，只写 `scratch/t06/out/`。
- 不猜：任何没有数据支撑的分配一律 `unresolved` 并写明缺什么证据。
- 不许调用网络。不许改本仓既有文件。
