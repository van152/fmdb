# t11 任务书：schema 约束命名 —— 清违规、补引用、攻小表

## 一句话目标

把 `scratch/t05/schema_inventory.json`（FM schema 的字段码清单）作为**名字合法性约束**接入 t08 的链分组命名器，做到三件事：

1. 删掉 9 个违反 schema 的名字（已由指挥官定位，见下）；
2. 补上 ref_ptr 形态，拿回 type22 的 `Sold/Snew/Salt`；
3. 用"名字优先"路线攻那 11 个至今零命名的小表。

## 事实基线（全部已独立复核）

| 项目 | 数值 |
|---|---|
| t08 命名 | **138/240**（chain_unique 81 / chain_ambiguous 12 / readpair 37 / ref_only 8 / unresolved 102）|
| t08 校准与回归 | injury 13/13、city 6/6、t07 的 45 名零回归，均 PASS |
| 命令官独立复核 | 84 条访问记录在其声明 VA 处的真实指令/偏移/宽度**全部吻合**；67 个 cmp 立即数独立复算一致 |

### 已知的 9 个违规命名（你必须自己复现出这 9 个，再消灭它们）

方法：`schema_inventory.json` 的 `entities[*].fields[*].code` 是每个实体的**合法字段码集合**。先剔除 5 个全实体通用码 `duni / rdui / NDBC / FDBC / dbnm`（出现在 ≥10 个实体里，无区分力），再用剩余码做归属判定。

| type_id | 归属实体 | 违规码 | 说明 |
|---:|---|---|---|
| 2 | city | `Icon` / `Igpr` | 这两个码属 injury，不该出现在 city 链里 |
| 21 | stadium | `Snft` / `Wucf` | 不在 stadium 字段表 |
| 47 | local region（归属待你重判） | `DELE` / `Lpop` | `DELE` 明显是英文词截断的伪码；`Lpop` 才是 local region 的真字段 |
| 58 | person | `otht` | 不在 person 字段表 |
| 62 | club | `Todo` / `Ttea` | 不在 club 字段表 |

**注意 t47 的归属陷阱**：t08 的 8 个去重码里有 6 个能在 injury 表里找到（75%），但那 6 个很可能是**跨实体共享码**，真归属是 local region。所以归属判定不能用简单覆盖率，要用**稀有码投票**：对每个码算它在多少个 schema 里出现（`df`），投票权重取 `1/df`（`df=1` 的码最有说服力），得分最高的实体为归属。请自己实现并报告每个 type_id 的投票明细。

## 三条工作线

### A. 清违规（必须做）

在命名器里加硬约束：**候选码必须属于该 type_id 的归属 schema 字段集（通用码除外）**。然后：

- 违规的 9 个槽降级为 `unresolved` 并保留原码到 `rejected` 字段（**不许静默删除**，要留下证据链）；
- 如果同一槽的链里另有合规候选码，改用它并标 `confidence=schema_fixed`；
- 报告：清掉几个、救回几个、仍空几个。

### B. 补 ref_ptr 形态（必须做）

指挥官已实证：`Sold` 与 `Salt` 在二进制里是标准编码，但因 getter 形如
```
mov rcx, qword ptr [rbx + 0x20]   ; obj+0x20 = 32
test rcx, rcx
jne ...
```
被 t07/t08 的"只收窄读"规则**整码丢弃**。判别式为：`mov r64, qword ptr [reg+OFF]` 之后 3 条指令内出现 `test` 且随后的条件跳转是空检查。

规则要点（务必照此，别踩我踩过的坑）：
- `kind=ref_ptr`，**object_off 取该 qword 的偏移**，但**宽度一律取自 reader**（引用字段在行里通常是 4B id，绝不能记成 8）；
- 用 `(object_off)` 做偏移匹配，用 reader 的 `width` 做宽度断言，不要用访问侧的 8B 去比 reader 的 4B；
- 已知锚点（自检用）：`Sold` cmp 在 file `0x1538f2d`（imm `0x536f6c64`），目标块 `[rbx+0x20]` → obj 32 → type22 `row+4/w4`；`Salt` cmp 在 `0x153920a`，`[rbx+0x48]` → obj 72 → `row+17/w4`；`Snew` 在 `0x153905b` 一带 → obj **40**（t07 表里记的 166 是错的实例）。

顺带修一个 t08 的遗留：`chain_ambiguous` 12 个槽，用"合规码唯一"来裁决（同槽多个候选里如果只有一个属于 schema 字段集，就定它）。

### C. 攻 11 个零命名小表（本任务最有价值的部分）

涉及 type_id：`23, 31, 35, 42, 46, 50, 51, 60, 61, 63, 64`，合计约 39 个槽，槽数只有 1–5 个，`object_off` 全在 24–39 之间。

它们拿不到链，是因为 t08 的"精确命中 ≥3"门槛对小表数学上不可达（1 槽表最多命中 1）。**但它们不需要链也能定名**：schema 已经告诉你这张表有哪些字段码，于是问题反转成"已知名字集合，求每个名字的偏移"。

做法：
1. 从 schema 拿到该实体的**字段码全集**（去掉通用码）；
2. 对每个码，在 `scratch/t07/out/4cc_table.json` 与 `scratch/cmd/ref_ptr_codes.json`（已有 244 个 ref 码的偏移）里取候选实例；
3. 只保留 `object_off ∈ 该 reader 的槽偏移集合` 的实例；
4. 在实体内部做**单射分配**（一个码一个槽、一个槽一个码），求可行解数：
   - 唯一解 → `confidence=schema_first`；
   - 多解 → 报 `ambiguous` 并给出解空间大小（这本身是有价值的结论：说明该表槽位过密）；
   - 无解 → 报 `no_instance`。
5. **必须做的证伪**：抽 2 个你判定为唯一解的表，用数据侧核对（`scripts/fm24_dump.py` 导出该表，检查该列的值域是否符合字段名语义），把核对结果写进报告。若数据侧不支持，降级为 `ambiguous`。

小表有个天然优势可以当交叉验证：**同族表（如 t61/t63 槽结构完全相同：`[(0,4,24),(4,1,28),(5,2,30)]`）如果归属不同实体，字段码应当不同；若你给出的答案在两张表里是同一组码，那就是错的。**

## 交付（写到 `scratch/t11/out/`）

1. `schema_map.json` —— type_id → schema 实体 的归属判定，含每个码的 `df` 与投票明细、落选实体及分数。
2. `naming_result.json` —— 与 t08 同构，新增 `confidence` 取值 `schema_fixed` / `schema_first` / `ref_pair`；被否决的码进 `rejected` 数组。**不得修改 row_off/width**。
3. `small_tables.json` —— 11 个零命名实体的逐表结果（解空间大小、分配、证伪结论）。
4. `verify.py` —— 可复跑，必须检查：
   - 9 个违规码**一个都不在** `field` 字段里出现（硬断言，从 schema 现算，不许写死清单）；
   - t07 的 45 名零回归、injury 13/13、city 6/6 仍 PASS；
   - t08 的 84 条访问记录仍能通过"声明 VA 处真实指令 = 声明指令"的复核；
   - `Sold/Snew/Salt` 三个槽已命名且 object_off 分别为 32/40/72；
   - 每个实体 `sum(width)==business_width`。
5. `REPORT.md` —— 三段式：违规清理账（9 个逐条去向）、ref_ptr 收益、11 个小表逐表结论。

## 验收线（缺一即 FAIL）

1. **违规归零**：`field` 里不再出现任何不属于归属 schema 的码（通用码除外）。
2. **总数 ≥ 138**（不许靠删违规把数字做小；删了必须补回来），**目标 ≥ 150**。
3. `Sold/Snew/Salt` 三槽命名成功。
4. 11 个小表逐表给出结论（唯一解/多解/无解），**不允许只写 unresolved**；至少 2 个唯一解表完成数据侧证伪。
5. `verify.py` 全绿。

## 纪律

- `py -V:3.12 -I`；脚本须有 `--help` 与 `--selftest`；退出码 0/1/2。
- **只读**：`scripts/`、`scratch/t05`、`scratch/t07`、`scratch/t08`、`scratch/cmd` 一律不许改；只写 `scratch/t11/out/`。
- 不许联网、不许启动游戏/编辑器。
- 不许把 t08 的 `naming_result.json` 直接改名复制充当交付：必须有 schema 约束与 ref_ptr 的实质改动。
- **先落盘骨架**（`"status":"in_progress"`），完成时 `"status":"complete_<限定词>"`。
- 负结果可接受：若某小表确实无解，把"为什么无解"写成可核对的数字（槽偏移集合 vs 全部候选偏移集合的交集为空）。
