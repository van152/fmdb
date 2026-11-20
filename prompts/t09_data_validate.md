# t09 任务书：数据侧证据引擎 —— 给 45 个已命名字段做对抗性验收，给 195 个未解析槽出形状签名

## 一句话目标

**完全不看 exe**，只用 `.dat` 里的真实列数据，回答两个问题：
1. t07 声明的 45 个字段名，**数据侧站得住吗**？（找出错的）
2. 剩下 195 个未解析槽，**数据长什么样**？（给出可用于后续命名的形状签名）

你是**对抗性验证者**，不是配合方。你的价值在于**推翻**，而不在于确认。

## 输入（全部只读）

| 文件 | 用途 |
|---|---|
| `scratch/t07/out/naming_result.json` | 41 个槽的字段名声明（client+server 去重后 45 条），你的验收对象 |
| `scratch/t05/layouts.json` | 26 实体 240 槽的权威 `row_off/width`（**不许改**） |
| `scratch/t05/schema_inventory.json` | FM schema 字段清单（字段名/类型/顺序），取名参考 |
| `scratch/t05/ref_matches.json` | 已有的引用字段候选（值域法产出 25 个，10 实体） |
| `scratch/t06/out/assignments.json` | city 的引用字段人工/数据双证结论 |
| `scripts/fm24_dump.py` | 表导出器（`--archive/--table/--csv/--limit/--list`），46/47 张定长表可 dump |
| `scripts/t05_profile.py` | 列画像器（`--archive --table --width/--auto --refN`），可复用其统计逻辑 |

数据文件在外部只读库（路径见 `docs/refs.md`），**只读**。

## 第一部分：45 个字段的对抗验收

对每条声明，算出数据侧指标并给判决：

- `supported`：数值落在该语义的合理区间，且有**分布特征**支撑（不是"不矛盾"，是"有正向特征"）；
- `weak`：不矛盾但也无特征，或样本太少；
- `contradicted`：数值范围/取值集合与该语义**冲突**（必须给出具体反例值与行号范围）。

### 待验清单（t07 声明，`archive` 标注）

| 实体 | 表 | row_off | w | object_off | 声明字段 | 语义期望（用于判断，非真理） |
|---|---|---:|---:|---:|---|---|
| city | t2 | 1 | 8 | 72 | `Clat+Clon` | 两个 f32：纬 ∈[-90,90]、经 ∈[-180,180] |
| city | t2 | 9 | 1 | 84 | `Catt` | **语义未定**——这是最需要你攻的一个；w1 能是什么？ |
| city | t2 | 10 | 4 | 32 | `Cnti` | u32 引用 type9 nation（251 行） |
| city | t2 | 14 | 4 | 40 | `Cwea` | u32 引用 type27 weather（334 行，fill 0.997） |
| city | t2 | 21 | 4 | 48 | `Clgi` | u32 引用 language（126 行），81.7% 为 0xFFFFFFFF 哨兵 |
| city | t2 | 25 | 4 | 56 | `Clri` | u32 引用 type47 lcrg（2488 行，fill 0.995） |
| inju | t6 | 0 | 1 | 76 | `icla` | 分类枚举，值域 1–13，约 11 个不同值 |
| inju | t6 | 1 | 1 | 77 | `iscl` | 未定，需你判断 |
| inju | t6 | 3 | 2 | 52 | `Imnd` | u16 最小天数，值域 1–180 |
| inju | t6 | 5 | 2 | 54 | `Iexd` | u16，值域 3–290（与 Imnd 的关系是关键证据） |
| inju | t6 | 7 | 1 | 88 | `Iiar` | 未定 |
| inju | t6 | 8 | 1 | 89 | `Irec` | 严格 {0,1} 布尔 |
| inju | t6 | 13 | 4 | 48 | `Iocr` | f32（`movss` 直证），发生率类 |
| inju | t6 | 17 | 1 | 80 | `Imip` | 百分比 0–90 |
| inju | t6 | 18 | 2 | 78 | `Icau` | 未定，w2 |
| inju | t6 | 20 | 1 | 81 | `Iagr` | 未定，w1 |
| inju | t6 | 21 | 1 | 82 | `Icms` | 赛季，值域 0–3 且**恰好等于文件里出现的赛季集合**（强特征） |
| inju | t6 | 22 | 1 | 83 | `Icon` | 未定，w1 |
| inju | t6 | 23 | 1 | 84 | `inSr` | 严重度 1–5 五级 |
| inju | t6 | 24 | 1 | 85 | `Igpr` | 未定，w1 |
| inju | t6 | 25 | 1 | 86 | `Icdp` | 值域 {50, 255}，0xFF 为"未设置"哨兵（强特征） |
| inju | t6 | 26 | 1 | 87 | `Ibin+Ibis+Ibph+Ibsp+Ibpg` | 5 位位打包，同一字节；须验证各 bit 只取 0/1 |
| stad | t21 | 2 | 1 | 157 | `Spty` | 未定 w1（场地类型？需自证） |
| stad | t21 | 3 | 1 | 159 | `Sste` | 未定 |
| stad | t21 | 4 | 1 | 160 | `Senv` | 未定 |
| stad | t21 | 5 | 1 | 155 | `Sdah+Sitg+Sext` | 位打包 3 位 |
| stad | t21 | 6 | 1 | 161 | `Sunt` | 未定 |
| stad | t21 | 7 | 1 | 162 | `Su21` | 未定（U21 队？） |
| stad | t21 | 8 | 1 | 163 | `Su19` | 未定（U19 队？） |
| stad | t21 | 9 | 1 | 164 | `Soty` | 未定 |
| stad | t21 | 11 | 2 | 144 | `Smnl` | u16 场地最小**长**（米，~90–120） |
| stad | t21 | 13 | 2 | 146 | `Smnw` | u16 最小**宽**（~45–90） |
| stad | t21 | 15 | 2 | 148 | `Smxl` | u16 最大长 |
| stad | t21 | 17 | 2 | 150 | `Smxw` | u16 最大宽 |
| stad | t21 | 19 | 1 | 156 | `Sdtr` | 未定 |
| stad | t21 | 21 | 1 | 158 | `Sprr` | 未定 |
| lcrg | t47 | 17 | 4 | 112 | `Lpop` | u32 人口 |

（共 41 行；`client/server` 两档都要各算一遍，**同一槽两档结论不一致本身就是发现**。）

### 必须回答的三个硬问题

1. **`Smnl/Smnw/Smxl/Smxw` 的"长宽"假设成立吗？** 判据：`Smnl <= Smxl`、`Smnw <= Smxw` 是否 100% 成立；数值分布是否落在足球场尺寸区间；若四者其实是两对 (min,max)，那排序关系是铁证。
2. **`Imnd/Iexd` 的"最小/额外天数"假设成立吗？** 判据：`Imnd <= Imnd+Iexd` 平凡，真正判据是 `Iexd` 是否 ≥ `Imnd` 的倍数关系、以及两者是否在长伤类别（`icla` 特定值）下才非零。这是**条件分布**问题，不是范围问题。
3. **`Catt`（city row+9 w1）到底是什么？** t07 只给了 readpair，语义空白。请穷举：值域、distinct、与 `Clat/Clon` 的相关性、是否等价于某 nation/region 的子集、是否 255 哨兵。给出 2–3 个竞争假设及各假设的**可证伪判据**，不要给单一结论。

## 第二部分：195 个未解析槽的形状签名

对 `naming_result.json` 里所有 `confidence=unresolved` 的槽（应 195 个），产出签名：

```json
{"type_id":2,"entity":"city","archive":"server","idx":0,"row_off":0,"width":1,
 "n":56293,"distinct":4,"min":0,"max":3,"top":[{"v":0,"n":51000},...],
 "sentinel_rate":{"0xFF":0.0,"0xFFFFFFFF":null},
 "bool_like":false,"enum_like":true,"ref_candidates":[{"table":12,"count":4,"fill":1.0}],
 "type_guess":"enum8","note":"..."}
```

要求：
- `bool_like`：distinct ≤ 2 且值 ⊆ {0,1}；
- `enum_like`：distinct ≤ 32 且 max < 300；
- `ref_candidates`：w4 槽用值域 ⊆ [0,count) 匹配全部定长表（复用 `t05_ref_match.py` 的逻辑，**但你必须自己重算一遍并给出 fill 与歧义度**——E42 已证明 fill 越接近 1 反而偏向小表，所以同一槽列出所有 fill ≥ 0.98 的候选，不许只报 top1）；
- `type_guess ∈ {bool8, enum8, u8, u16, u32, ref4, f32, bitfield, unknown}`；
- 对 w8 槽单独处理（可能是两个 f32 或一个指针）。

## 交付（写到 `scratch/t09/out/`）

1. `field_validity.json` —— 41 条 × 2 档的判决，每条带 `verdict` + `metrics` + `why`（一句可核对的话，含具体反例值），顶层 `"status"`。
2. `shape_signatures.json` —— 195 个未解析槽的签名。
3. `open_questions.md` —— 上面三个硬问题的完整回答（含反例、竞争假设、可证伪判据）。
4. `verify.py` —— 可复跑，须检查：41 条全覆盖、195 条全覆盖、`sum(width)==business_width`、被判 `contradicted` 的每条都有至少一个具体反例（行号+值）。
5. `REPORT.md` —— 判决统计（supported/weak/contradicted 各几个）、`contradicted` 逐条列出并给**最可能的错因**（读错偏移？槽内子字段错位？同名不同义？）、形状签名对后续命名的可用性评估。

## 验收线

1. 41 条字段 × 2 档全部有判决，**`contradicted` 必须给出反例**（无反例的 contradicted 视为无效）。
2. 195 个未解析槽全部有签名，无一 `null`/占位。
3. 三个硬问题都有明确回答，且 `Smnl/Smnw/Smxl/Smxw` 的排序关系给出**百分比数字**。
4. `verify.py` 全绿。

## 纪律

- `py -V:3.12 -I`；脚本须有 `--help` 与 `--selftest`；退出码 0/1/2。
- **只读**：`scripts/`、`scratch/t05`、`scratch/t06`、`scratch/t07` 一律不许改；只写 `scratch/t09/out/`。
- 不许联网、不许启动游戏/编辑器。
- 全量统计优先（`--limit 0`），样本不足时明确写 `n`，不许用 1000 行样本冒充全量。
- **先落盘骨架**（`"status":"in_progress"`），完成时 `"status":"complete_<限定词>"`。
- 你最重要的产出是**发现错误**。如果 41 条全 supported，请检查是不是自己的判据太松。
