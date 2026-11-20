# t08 任务书：分发链分组 —— 把 240 槽命名从 45 推到 150+

## 一句话目标

建**分发链索引**（把散落的 `cmp reg,'XXXX'` 点按"同一条 dispatch 链"聚成组），用"整条链的偏移集合 vs reader 偏移集合"做实体配对，从而把 t07 丢掉的 type22（以及另外 14 个零命名实体）重新连上。

## 事实基线（全部已独立复算，可当场验证）

| 项目 | 数值 | 来源 |
|---|---|---|
| 实体/槽总数 | 26 实体 / **240 槽**（client+server 两档） | `scratch/t05/layouts.json` |
| t07 命名成果 | **45/240**（injury 18/24、stad 14/19、city 12/18、lcrg 1/18，其余 22 实体 0） | `scratch/t07/out/naming_result.json`，`confidence` 分布 = readpair 37 / ref_only 8 / unresolved 195 |
| t05 命名成果 | 28（type22 **17**/19、injury 11/24） | `scratch/t05/named_fields.json` |
| t07 校准 | injury 13/13、city 6/6 双 PASS | `py -V:3.12 -I scratch/t07/out/verify.py` |

**关键负结果（本次任务的存在理由）**：把 t05 与 t07 逐槽比对，交集只有 type22，且 t07 在 type22 上是 **0/19**；`AGREE 0 / CONFLICT 0 / only05 17`。t07 没有推翻 t05，是**根本没连上**。

## 根因（我已定位，你直接从这一步开始，不要重查）

t07 用 `object_off` 做全局匹配，但全局表里有 1,477 个 4CC，**同偏移被多个码占用**是常态。type22 的实证：

```
reader obj_off = [24,32,40,60,100,72,101,64,80,84,88,92,102,96,105,103,104,68]
全局表里偏移落在该集合内的 S 码：
  off 40  -> Sbdy, Sbld            (2 码撞车)
  off 96  -> Scam, Slat, Smnk      (3 码撞车)
  off 100 -> Slon, Styp            (2 码撞车)
  off 101 -> Scpl, Scpm            (2 码撞车)
  off 64  -> Shwn, Sscp            (2 码撞车)
  off 32  -> SplR
  ...
```

单看偏移无法裁决，所以 t07 全判 unresolved。而 t05 能用窗口法拿到 17 个，是因为它**在一条链内部**做匹配：同一条链里的 20 个码是一个封闭集合，集合级对齐全链就能定死每个槽。

**另外实证一处 t07 表本身有错**：全局表把 `Snew` 记成 `object_off=166`，而 t05 的链内结果与新读数都是 **40**（`Snew` 在 row+8/w4），166 是抓错了实例。所以链分组不只是"多连线"，还是**纠错手段**。

## 方法（按此实现，遇到更优解可换但要说明）

### 1. 链分组

- 从 `scratch/t07/out/4cc_table.json` 的 2,103 条候选（1,473 个码）出发，**不要重新全库扫描**（太慢）。
- 分组依据用 `file_off`：同一 dispatch 函数的 cmp 点是**代码上连续的一段**（type22 的整段落在 `0x1538f39–0x1539xxx`，city 的落在 `0xe55098–0xe550c0` 一带）。
- 具体做法：按 `file_off` 排序后，以"相邻 cmp 间距 ≤ 512 字节"做单链聚合；再用 `je` 目标做连通性校验（同链的 target 块应落在同一函数的可达范围内）。跨链接缝处会因间距突增自然断开。
- 每链产出：`chain_id`、`file_off_range`、`codes[]`、`targets[]`、`n_codes`。要求每链 `n_codes >= 5` 才保留（少于 5 的对不齐）。

### 2. 链 ↔ reader 配对

- 对每条链 C（码 → 候选偏移集合）与每个 reader R（`layouts.json` 的 obj_seq 偏移集合 + 宽度），算
  `score = |{(off,width) ∈ C} ∩ {(off,width) ∈ R}|`，要求 **≥3 个精确命中** 才视为候选配对。
- 输出**配对矩阵**（26 reader × 所有链），含 top-3 候选与命中明细。这张矩阵是本任务最有价值的产物——它同时证明"哪些实体确实没有 4CC 链"。
- 一条链允许配多个 reader（client/server 双档），但**一个 reader 只能有一条主链**；冲突时按 score 与宽度一致率裁决并记录落选者。

### 3. 链内定槽

- 配对确立后，在该链的码集合内做 `off → code` 唯一化：
  - 同 `(off,width)` 只有 1 个码 → `confidence=chain_unique`；
  - 有 2 个及以上 → 用 `je` 目标块的**指令形态**（读/写、`movzx` vs `movsx` vs `movss`）与 reader 的字段类型约束排歧；仍不唯一则记 `ambiguous` 并**两个码都列出来**，不许瞎选。
- t05 的 17 个 type22 命名是**交叉校验集，不是输入**：禁止直接搬运 `named_fields.json`。要求链分组法独立复现，报告"17 个里复现几个、几个名字不同、为什么"。

### 4. 顺带修一个洞：`Sold` / `Salt`

这两个码**完全不在** `4cc_table.json` 里（不信可自验）。它们是 t22 里已确认存在的字段，说明字节扫描漏了一种编码。排查方向：`cmp r8d,imm32`（`41 81 F8`）、`cmp r/m32,imm8`（`83 /7`，小值符号扩展——但 4CC 都是大值，可能性低）、寄存器间接比较（先把 imm 装进寄存器再 `cmp reg,reg`）、以及**跳转表/二分派发**（若 t22 链是 perfect-hash/switch，那 `Sold` 走的是另一条路径）。查明并给出：漏因分类 + 受影响码数量的上界估计。**若确认是跳转表机制，只需写清机理与证据，不要求把码全捞回来。**

## 交付（写到 `scratch/t08/out/`）

1. `chains.json` —— 链索引（`chain_id / file_off_range / codes / targets / n_codes`），顶层 `"status"`。
2. `pairing.json` —— 26 reader × 链的配对矩阵（含 top-3、score、命中明细、裁决理由）。
3. `naming_result.json` —— **与 t07 同构**（字段名对齐 `type_id/entity/archives/*/fields[]` 的 `idx,row_off,width,object_off,field,codes,confidence,why`），`confidence ∈ {chain_unique, chain_ambiguous, readpair, ref_only, unresolved}`。**不得修改 row_off/width**。
4. `MISSING_CODES.md` —— `Sold/Salt` 漏因分析。
5. `verify.py` —— 可复跑，必须检查：
   - t07 的 45 个命名槽**一个不少、名字一字不变**（防回归，这是硬门槛）；
   - injury 13/13、city 6/6 仍 PASS；
   - `sum(width) == business_width` 每实体成立；
   - 所有 `chain_unique` 槽的 `(off,width)` 在配对链内确实唯一（反向自检，防止自欺）。
6. `REPORT.md` —— 前后对比表（逐实体 45→N）、配对矩阵结论、仍然零命名的实体及其原因分类。

## 验收线（缺一即 FAIL）

1. **零回归**：t07 的 45 个命名槽全部保留原名（`verify.py` 强制执行）。
2. **type22 ≥ 14/19**（t05 的 17 是上限参照；低于 14 说明链分组没做对）。
3. **总数 ≥ 62/240**（45 + 17 的下界，实际应更高）。
4. 对仍然 0 命名的实体，给出**原因分类**（无 4CC 链 / 链太短 / 配对分数不足 / 码表缺失），不许只写 "unresolved"。

## 纪律

- `py -V:3.12 -I`；脚本须有 `--help` 与 `--selftest`；退出码 0/1/2。
- 只写 `scratch/t08/out/`，**不改本仓既有文件**（`scripts/`、`scratch/t05`、`scratch/t07` 一律只读）。
- 不许联网、不许启动游戏/编辑器。
- **先落盘骨架**（`"status":"in_progress"`），边做边覆盖；完成时 `"status":"complete_<限定词>"`。
- 拿不到就报负结果，禁止把期望值硬编码进生成逻辑（verify 里可以硬编码期望值）。
