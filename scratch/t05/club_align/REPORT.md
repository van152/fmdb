# t05b — schema↔reader 宽度序列对齐器 + club 字段级映射

## 结论

本次实现可调用的约束 DP，并保留 fixtures 的真实负结果：完整 reader 宽度序列尚未提供；已知物理行锚点中 city 的 Cnti/Clat 顺序与 schema order 相反。没有把预填锚点冒充 DP 复原。club 仅保留一项既有 L3 reader 候选，因缺少安全的 class→reader 分区数据验证而降为 low。

- Fixtures：0/5 PASS；5 FAIL；DP synthetic unit PASS。
- Club：1 命名（high 0, medium 0, low 1）；闭合列表段 0。
- Schema：433 顶层字段 = 386 标量 + 47 列表；list item 子字段 239。采用 `scratch/t05/schema_inventory.json` 并与权威 Markdown 保序交叉核对。

## 对齐器

`align_fields(schema_fields, reader_widths, row_width, anchors, samples, prefix_width=0, suffix_width=0)` 使用 memoized DP `(schema_index, transfer_index, offset)`，按 schema inventory 的候选宽度、reader transfer 顺序、锚点和精确宽度求解；optional 字段可取 0，boolean 可打包为 0 宽，list/database_record_list 固定按 0 宽从 scalar 序列排除。`prefix_width/suffix_width` 保留边界/身份帧，不把 `rdui/duni` 身份尾当业务字段。引用域、enum、date、colour 样本作合法性评分。

## Fixture 结果

五份输入均可机械复算 row closure。现有 hand-decoded reference 只给部分偏移/宽度，不是完整 `mov r8d,N` 序列；故 fixture 不能据此宣称完整 DP 复原。身份尾作为独立 frame 检查；award/city/stadium/injury 的 `rdui@row_width-13`、`duni@+4`、marker 位置一致。city 的业务 anchors `Cnti` 与 `Clat/Clon` 仍直接逆序：

| fixture | 字段数 | 行宽 | anchors | frame anchors verified | closure | 业务序列顺序 | 结果 |
|---|---:|---:|---:|---:|---|---|---|
| award | 38 | 77 | 2 | 2/2 | PASS | 可行 | FAIL |
| city | 15 | 43 | 5 | 2/2 | PASS | 矛盾 | FAIL |
| stadium | 60 | 38 | 5 | 2/2 | PASS | 可行 | FAIL |
| injury | 27 | 16 | 2 | 2/2 | PASS | 可行 | FAIL |
| language | 12 | variable | 1 | 1/1 | PASS | 可行 | FAIL |

纠错：任务描述把 `city.Cnti` 写作 u8；`scratch/t02/city_reference.json` 的 row0 sample 在 +10 为 `83 00 00 00`，并记录 reader `mov r8d,4`，故本次按 u32/4B 处理。城市业务 anchors 仍为 `Cnti` 在 schema index 6、`Clat/Clon` 在 index 11/12，但物理 offset 分别 +10 与 +1/+5；这是对“schema 与 reader 保序”前提的真实冲突，不通过跳字段消除。其他定长夹具的身份字段均在 row frame 尾部，已从业务 DP 序列排除。language 后缀 ordinal 是相对 17B suffix 的动态锚点。详见 `fixtures_result.json` 与 `CORRECTION.md`。

## Club 映射

### 仅保留的字段

| 字段 | 偏移/宽度 | 置信度 | L3 字节证据 |
|---|---:|---|---|
| `Cccn` | +8 / 4B | low | reader `0xe5a864` `49 8d be f0 00 00 00`; width `0xe5a86e` `41 b8 04 00 00 00`; getter cmp `0xe8b7bf` `81 fb 6e 63 63 43` |

该项仅保留既有 Cccn getter→sink 局部 cursor 证据；没有将它与 substrate 的 `[0,4,8,12,16]` 前缀或 `LEAGUE_BODY_CLUB` 的循环传输合并。全表 framing/footer 已闭合，但连续 class split 没有每行 class byte；row 69709 的物理 `row+8` 还是与 `row+0` 重复的 identity，不可将该样本拿来验证 Cccn。故不做全体引用域分布结论，置信度降到 low。

### 未闭合

- 其余 432 个 top-level schema 项均不作偏移猜测；既有 `Cdof`、`Cprs`、`Ctsi` 三个 reader/getter 候选原样保留在 JSON，未升格。
- 47 个 list/database_record_list 字段有 239 个 schema 子字段；count_offset/item_width 均为空，闭合段数 0。
- CLUB reader 在 `0xe5a801` 出现分支游标分裂；首个动态 helper `0xe5a952` 后宽度/游标未闭合。LEAGUE_BODY_CLUB `0x43beba0` 的 33 个 transfer events/count-loop 保持单独建模。
- 行框架为 84,259/84,259 且 footer 精确；其中 3 行仅 identity-framed，class split 未由行内标记独立确认。不要把 framing closure 误称字段语义 closure。

## 对旧 field_mapper 结论的勘误

旧 `field_mapper` 的 39.7% 是其旧 fixtures 的字段偏移吻合率，旧 CFG 游标在分支/循环处失效；不可据此断言所有类型或字段映射不可解。本轮确认需要先拆 system identity frame、optional/位打包字段、变长语言后缀和两套 club reader。Cccn getter/sink 证据、substrate `[0,4,8,12,16]` 和 LEAGUE_BODY_CLUB loop 是三条独立 track，不得互相补游标。city anchors 还与 inventory 声称的保序关系不一致，必须先定清楚该 anchor/reader 对应关系，再把剩余序列送入 DP。未修改任何 t02 输入/旧脚本。

## 复跑

```powershell
py -V:3.12 -I -B scratch/t05/club_align/align.py --selftest --json
py -V:3.12 -I -B scratch/t05/club_align/align.py --entity club --json
```

## 来源

- schema 快照 SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`，与 `evidence/MANIFEST.json` 一致；inventory 文件由 t05 提供。
- correction/设计：`scratch/t05/club_align/CORRECTION.md`、`scratch/t05/ALIGNMENT_NOTES.md`；上游证据只读引用。
- 本次没有启动游戏/editor/IDA，也没有写入外部数据；本目录为本任务唯一写入位置。
