# t11：schema 约束命名

状态：`complete_with_explicit_acceptance_gaps`（本轮产物已生成；硬约束检查通过，但任务书的命名数量与小表数据侧验收线未达到）。输入 `scratch/t05`、`scratch/t07`、`scratch/t08`、`scratch/cmd`、`scripts/` 均未修改；只读调用了 `scripts/fm24_dump.py`。

## 一、违规清理账

`t08` 基线为 138/240。`schema_map.json` 对 26 个 type 使用 `df(code)=包含该码的 schema 实体数`，每个非通用码向所属实体投 `1/df`；逐码的 df、权重、落选实体及得分均落在该文件。

| type | 码 / 槽 | 去向 |
|---:|---|---|
| 2 | `Icon`、`Igpr` | city schema 不含这两个 injury 码；client/server 共 4 个槽均降为 unresolved，原码与访问证据保存在 `rejected`。 |
| 21 | `Snft` | stadium schema 不含；槽降为 unresolved，原码保留在 `rejected`。 |
| 21 | `Wucf` | stadium schema 不含；同槽唯一合规码 `Scov` 接替，`confidence=schema_fixed`，原 `Wucf` 留在 `rejected`。 |
| 47 | `DELE` | 不是 local region 字段码；拒绝并保留原码。 |
| 47 | `Lpop` | 是 local region 合法码，保留。 |
| 58 | `otht` | person schema 不含；两个槽降为 unresolved，原码保留。 |
| 62 | `Todo`、`Ttea` | club schema 不含；同槽合法码 `Ttyp` 接替，`confidence=schema_fixed`，两个原码均保留。 |

**复现时发现与任务书基线存在冲突，未作静默处理。** 上表将 `Lpop` 列在“9 个违规名”中，但按 `schema_inventory.json` 的 local region 字段表它是合法码；上表其余只有 8 个不同的非法码。相反，type47 的字段候选还含 `Icdp/Iocr/Imip/Iagr/icla/iscl` 六个 injury-only 码。选定 local region 后，硬 allow-list 必须拒绝这六码（`Imip` 两个槽），否则验收项“所有 field 均属于 schema”无法成立。最终 rejected 中共 18 个码实例、14 种不同码；14 个槽被清空，2 个槽由唯一合规候选救回。`field` 中 schema 非法码为 0。

type47 的原始稀有度票数如实记录在 `schema_map.json`：`Iagr/Icdp/Imip/Iocr/icla/iscl` 的 schema `df` 均为 1，各给 injury 1 分；`Lpop` 的 `df=1`，给 local region 1 分；原始分数为 **injury 6 : local region 1**，并非 75% 覆盖率结论。因 row+17 的 `Lpop` 是 local region 唯一字段锚点，且原 layout 标记 `lcrg`，本次以该独立字段锚点将 type47 定为 local region，并拒绝链串入的 injury 码。此处不能声称 `1/df` 投票本身选出了 local region。

`t08` 的 12 个歧义槽按合法码筛选：stadium 的 `Scov|Wucf` 与 club 的 `Todo|Ttea|Ttyp` 各有一个唯一合法码，已分别修复；其余多码仍保留歧义。t07 原有 45 个名字 45/45 原样保留。

## 二、ref_ptr 收益

通过 cmp → getter 分支目标静态反汇编确认 `mov r64, qword ptr [reg+OFF]` 后紧跟 `test reg,reg` 与空检查跳转；`object_off` 取 qword 的 OFF，`size` 则按 reader 取 4B：

| 码 | cmp file offset | getter 指令 / object_off | reader 槽 |
|---|---:|---|---|
| `Sold` | `0x1538f2d` | `[rbx+0x20]` / 32 | type22 row+4 / w4 |
| `Snew` | `0x153905b` | `[rbx+0x28]` / 40 | type22 row+8 / w4 |
| `Salt` | `0x153920a` | `[rbx+0x48]` / 72 | type22 row+17 / w4 |

3/3 槽已以 `confidence=ref_pair` 命名。输出 access 的 `size` 是 reader 的 4，不是 getter qword 的 8；`row_off/width` 未改。

## 三、11 个零命名小表

单射分配按 schema 字段码与 `4cc_table.json` / `ref_ptr_codes.json` 的 `object_off` 候选计算；ref_ptr 候选宽度使用 reader 宽度。`small_tables.json` 同时列出每个槽候选、完整/最大部分解空间、数值偏移交集，以及对所有 32 个 schema 实体的完整唯一解搜索结果。

| type | schema 候选 | 结论 | 解空间（完整；最大部分） | 备注 |
|---:|---|---|---:|---|
| 23 | stage name | ambiguous（数据侧降级） | 1；1 | 唯一候选 `SNsn` 的 schema 类型是 string，但 reader 槽仅 1B；`fm24_dump.py` 导出 server 278 行，row+0 的 278 个值全为 0，不能支持短名字符串引用。全 schema 搜索还出现 `language:Linf`、`non player:NDsp` 两个不同实体假设。 |
| 31 | club（投票首选） | ambiguous | 0；68（2/3 槽） | object 24 无候选；object 32/34 有多码。数据侧诊断导出 512 行：row+4 取值如 200、125、180，row+6 样本恒 0；候选分配不唯一，不据此命名。 |
| 35 | club | ambiguous | 26；26（2/2） | 两槽均有候选，但单射解有 26 个。 |
| 42 | club（投票首选） | ambiguous | 0；68（2/5 槽） | object 24、28、39 无候选；32/34 多码。 |
| 46 | club | ambiguous | 0；196（3/5 槽） | object 24、28 无候选；其余候选多解。 |
| 50 | club | ambiguous | 0；82（2/4 槽） | object 24、28 无候选；其余候选多解。 |
| 51 | nation（投票首选） | ambiguous | 0；9（1/3 槽） | object 24、28 无候选；object 32 多码。 |
| 60 | nation（投票首选） | ambiguous | 0；9（1/3 槽） | object 24、28 无候选；object 32 多码。 |
| 61 | schema 未定 | no_instance | 0；0 | reader offsets `{24,28,30}` 与全体候选 offsets 的交集为空。 |
| 63 | schema 未定 | no_instance | 0；0 | reader offsets `{24,28,30}` 与全体候选 offsets 的交集为空；与 type61 槽结构相同。 |
| 64 | team kit（投票首选） | ambiguous | 0；8（3/4 槽） | object 24 无候选；其余槽仍多解。 |

本轮没有得到两个同时通过数据侧核对的唯一解：所有 32 个 schema 的穷举中，只有 type23 出现完整唯一分配候选，但其数据值域不支持该命名并已降级；其他 10 表无完整唯一解。type31 的导出仅作为歧义诊断，不伪称唯一解验证。因此“小表至少两个唯一解 + 数据侧支持”未通过。

## 验证与验收状态

运行方式：

```powershell
py -V:3.12 -I scratch/t11/out/build.py --help
py -V:3.12 -I scratch/t11/out/build.py --selftest
py -V:3.12 -I scratch/t11/out/build.py
py -V:3.12 -I scratch/t11/out/verify.py --help
py -V:3.12 -I scratch/t11/out/verify.py --selftest
py -V:3.12 -I scratch/t11/out/verify.py
```

验证器通过：schema 非法 field 码为 0、t07 45/45、injury 13/13、city 6/6、原 t08 84 条 chain_unique 访问在声明 VA 反汇编指令 84/84、`Sold/Snew/Salt` 3/3、全部布局 `sum(width)==business_width`。**验收仍 FAIL**：命名总数 129/240（低于 138，且 t47 的额外六码必须拒绝）；支持数据侧的唯一小表 0/2。`verify.py` 对这两项按退出码 1 明确报 FAIL，没有将未达线包装成 PASS。
