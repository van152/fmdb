# t05b2 — 字段对齐器(重发):以 fixtures_truth.json 为硬约束

## 为什么重发

上一轮(t05b)交付 0/5 夹具,理由写的是"city 的 `Cnti` 锚点与 schema 顺序冲突、u8 宽度与 reader 的 u32 证据不符"。

**这个冲突不存在,是读取错误。** 指挥官已逐字节验证:

| 城市 | row | off10 | rdui@30 | duni@34 |
|---|---:|---:|---:|---:|
| Liverpool | 1061 | **139** ✓ | 1061 ✓ | 100047 ✓ |
| Manchester | 1075 | **139** ✓ | 1075 ✓ | 100062 ✓ |
| Madrid | 316 | **170** ✓ | 316 ✓ | 341 ✓ |
| München | 540 | **145** ✓ | 540 ✓ | 592 ✓ |

`u8@10` 与 `u32@10` 不矛盾:因为 off11/12/13 在全部 56,293 行恒为 0,所以 `u32@10 == u8@10`。
**不要再把这条当成阻塞项。**

## 硬约束

- 工作区 `<WORKSPACE>`,Python `py -V:3.12 -I -B`。
- 游戏数据与 `<OLD_REPO>\` 全只读;唯一可写 = OUTDIR。不要改 `scratch/t01`、`scratch/t02`。
- **不要写 `status: in_progress`**;结论必须定格为 `complete*` / `partial*` / `negative`。

## 直接可用的输入

| 用途 | 路径 |
|---|---|
| **夹具真值(硬约束,先读)** | `scratch/t05/fixtures_truth.json` — 每夹具的 closure 等式、锚点偏移/宽度、3 条样例行 hex、四城市 named_rows(全 MATCH)、身份验证率(100%) |
| schema 机读 | `scratch/t05/schema_inventory.json`(`entities.<name>.fields` 保序 + `type_width_candidates`) |
| 字节列画像 | `scratch/t05/profile_{award,city,stadium,injury}.json` — 每偏移的 constant/zero%/distinct/min/max/monotonic/ref_lt_N |
| 设计笔记 | `scratch/t05/ALIGNMENT_NOTES.md`(必读,尤其"字节/标量密度"与"optional 跳过"两节) |
| club 行框架 | `scratch/t02/inbox/club_v2/output.json`(84,259 行闭合) |
| club 已验字段 | `scratch/t02/inbox/club_fields/output.json`(Cccn@+8,字节链 8/8) |
| exe | `<OLD_REPO>\input\editor.exe` |
| 导出器(取行) | `scripts/fm24_dump.py`(`_reader()` / `load_payload()` / `fixed_specs()` / `walk_fixed()`) |

## 必须先接受的四条结构事实(指挥官已实测)

1. **身份尾 13B 恒定**:`row_end-13` 起是 `u32 rdui(==行号) | u32 duni | u32 duni(同值) | u8 marker`。
   **业务区 = row_len - 13**。可用字节:
   - award 77 → 业务 64B(35 个业务字段)
   - city 43 → 业务 30B(13 个)
   - stadium client 38 → 业务 25B(56 个!)
   - injury client 16 → 业务 **3B**(24 个)
2. **字节/标量 < 1 必然位打包**。injury 实测:off0 只用低 4 位(11 种取值)、off1 只用低 6 位(45 种)、off2 只用 bit0 → 这是 `4-bit enum + 6-bit enum + 1 bit bool`,不是三个独立字节的标量。
3. **optional 字段有值才出现**(或由位图控制),不是恒占位。award 的 35 个业务字段按最小宽度硬算必然超过 64B。
4. **client 与 server 同名表行宽不同 = 服务端附加字段**:injury 16 vs 40、stadium 38 vs 181、table_22 13 vs 79、table_5 34 vs 48。字段名要以 **server 版**(更宽)为主战场,client 版只做子集验证。

## 算法(按这个思路写,不要再用"游标追踪")

这是**保序约束下的线宽分配搜索**,不是控制流追踪。

### 步骤
1. 解析 schema → 该实体的**保序标量序列**(排除列表字段),共 `K` 个,其中身份字段 `duni/rdui` 已知在尾部。
2. 每个字段按其类型取候选线宽集合 `W(type)`(见 `type_width_candidates`);`optional` 字段额外允许 `0`。
3. 约束:`Σ width == 业务区字节数`。
4. 打分(越大越好):
   - **类型-统计匹配**:对字段类型与实际列统计打分
     - `boolean` ↔ 该字节/位只取 0/1 → +3;否则 −5
     - `enum` ↔ distinct 数量接近某枚举基数且值域连续 → +2
     - `database_record_unique_id` ↔ 值 `< N_target` 或 `==0xFFFFFFFF` → +3
     - `real` ↔ float32 全有限且量级合理(0.01–1e6)→ +2
     - `date` ↔ 2B 解释落在 1800–2100 → +2
     - `integer` ↔ 值域与 declared 约束一致 → +1
   - **锚点命中**:若某字段落在 `fixtures_truth.json` 的锚点上,`+10`;宽度不符 `−10`。
   - **结构合理性**:业务区末尾应紧接身份尾(不留空洞)→ +1。
5. 用 DP(按字段顺序 × 当前偏移)求最优解;对同一夹具可保留 top-3 解并输出。
6. **验证**:每个候选解都要用全部行重算"每行的业务区+身份尾 == row_len",并输出该解在锚点上的命中情况。

### 阶段 A 验收(必须先过)
对 award / city / stadium / injury 四个夹具:
- 自动搜索出的最优解**必须命中 `fixtures_truth.json` 里的全部锚点偏移**(不能把这些偏移写死在代码里当输入;可以作为打分项)。
- 输出每个夹具的解:字段→偏移表、总宽、锚点命中数、总分。
- 允许"部分字段判为 unresolved(0 宽)",但已命名字段的偏移必须正确。

### 阶段 B(有余力再做)
把同一算法套到 **club(client,业务区 ≈ 69B,386 个标量)**:
- 已知 `Cccn u32@+8`,身份尾 13B。
- 目标 ≥15 个字段有 medium 以上置信 + 给出列表段的计数/项宽推断。
- club 极紧(0.21 B/标量),允许大量字段判 0 宽(位域共享),**不要硬凑**。

## 交付

1. `align.py` — `--selftest`(跑四夹具并打印命中)、`--entity <name>`、`--json`。搜索逻辑与锚点校验必须分离(锚点只用于打分与验收)。
2. `fixtures_result.json` — `{"status":"PASS|FAIL","fixtures":[{"name","anchors_hit","anchors_total","total_width","closure_ok","assignment":[...]}]}`
3. `club_fields.json` — 阶段 B 的结论(若做了)。
4. `REPORT.md` — 算法、打分表、四夹具结果、club 结果、未解与负结果、与上一轮(t05b)的差异说明。

## 验收标准

- 四夹具:**锚点 100% 命中**(award 3 锚点、city 6 个、stadium 6 个、injury 3 个,以 `fixtures_truth.json` 为准),且 `Σ width == 业务区`。
- 不得把锚点偏移硬编码进搜索;若被我发现搜索里直接写了 `30`/`64`/`25` 这类常量作为字段偏移,即判定不合格(锚点可作为打分项)。
- `align.py --selftest` 退出码 0。
- 结论 `status` 不得为 `in_progress`。

## 完成后

一行打印:四夹具 anchors_hit/anchors_total + club 命名字段数。
