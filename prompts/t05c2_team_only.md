# t05c2 — team(type 24) 行边界 + 25 字段映射【只做 team,comp 另开】

## 为什么要重发

上一次(t05c)在 20 分钟超时前只完成了载荷提取(留下了 `_t24.bin`),没有做出结论。
**本次只做 team 一张表**,预算 45 分钟。`comp` 已从本任务范围移除。

## 硬约束

- 工作区 `<WORKSPACE>`,Python 固定 `py -V:3.12 -I -B`。
- 游戏数据目录与 `<OLD_REPO>\` **全部只读**。唯一可写 = OUTDIR。
- 不要改 `scratch/t01`、`scratch/t02` 既有文件;不要动 `_t24.bin`。
- closure 必须精确算术;允许诚实负结果;**不要写 `status: in_progress`**,结论无论好坏都要定格成
  `complete*` / `partial*` / `negative`。

## 已经替你准备好的输入(直接用,别再解压)

| 内容 | 路径 |
|---|---|
| **table_24 已解压载荷** | `scratch/t05/team_comp/_t24.bin`(8,819,030 B) |
| 解压器(备用) | `<OLD_REPO>\scripts\modding_read_dbdat.py` |
| 本仓 loader 参考 | `scratch/t05/team_comp/loader.py`(上次留下,含正确的 zstd magic 扫描) |
| schema | `<OLD_REPO>\reports\EDITOR_SCHEMA_FIELDS.md` 搜 `### team（记录标识 \`team\`，25 个字段）` |
| 机读 schema(推荐) | `scratch/t05/schema_inventory.json` 的 `entities.team`(保序字段表 + 类型) |
| 上游普查 | `<OLD_REPO>\reports\dbdat_decode\server_tables_census.json` 里 `table_id == 24` |
| exe | `<OLD_REPO>\input\editor.exe`,reader 入口 `0x11c1d80` |

## 已知事实与强假设

- `server_db/table_24.dat`:count = **84,507**,payload = **8,819,030 B**。
- `14 + 84507 × T + 8 = 8,819,030` → T = **104.36**,非整数 ⇒ **不是定长**。
- `server_db/table_extra_24.dat` 精确满足 `12 + 82 × 84,507 = 6,929,586` ⇒ 存在 **82 B/行** 的定长扩展区。
- team schema = **25 字段、0 列表**:`unique_id×1, integer×5, string×4, enum×2, database_record_unique_id×9, boolean×1, cash×3`。
- **强假设**:主表行 = **82 B 定长标量区 + 行尾 4 个内联字符串**(长度前缀 + UTF-8)。
  平均 (8,819,030-22)/84,507 ≈ 104.4 B,即字符串区平均约 22 B,与 4 个短名/缩写相符。

## 做法(按顺序,每步落盘)

1. **先验 82 B 标量区**:从 offset 14 起每 82 B 读一个"候选定长区",检查其内部是否有稳定身份槽
   (找 `u32 == row_index` 的偏移,或 `重复 u32` 的 8B 槽)。若 25 字段里有 `unique_id`,它很可能是
   `u32 + u32` 相等的一对,或独立 u64。
2. **再解行尾字符串**:在 82 B 之后读 `u8/u16/u32 长度 + UTF-8`。用"下一行 82 B 区首字段必须合法"
   作为边界约束,正向走满 84,507 行,要求末行结束 == payload_len − 8。
3. **反证**:若第 1 步找不到身份槽,改试 `row = 82 + 4×(1+len)` 等其它组合;仍不行就如实写负结果,
   给出你验证过的所有失败组合与原因。
4. **字段命名**:用 schema 顺序 + 类型线宽 + 数据合法性:
   - 9 个 `database_record_unique_id` 的值必须落在目标表行数范围内(stadium<48,413、city<56,293、
     comp<table_25 count、nation<251、region<region count);空值应为 `0xFFFFFFFF`;
   - 2 个 enum 值 < 枚举基数;3 个 cash 为 int32(可正可负,量级合理);
   - 4 个 string 若在行内 = 长度前缀 + UTF-8,先确认它们的位置再谈字段名。
5. 只要能证明**行边界**,即使字段只命名一部分也算成功;字段全命名是加分。

## 交付

1. `team.json` — **必须把 `status` 定格**:
```json
{"status":"complete | complete_partial | negative",
 "type_id":24,"archive":"server","count":84507,"payload_len":8819030,
 "row_model":"fixed82_plus_strings | fixed | variable | unresolved",
 "closure":"14 + 84507*(82+...) + 8 = 8819030",
 "identity":{"offset":..,"kind":"rdui|repeated_u32|none","verified_rows":"84507/84507"},
 "fields":[{"field":"T...","offset":..,"width":..,"evidence":"..","confidence":"high|medium|low"}],
 "string_layout":{"offset":82,"count":4,"encoding":"u8len+utf8"},
 "unresolved":["..."]}
```
2. `verify.py` — `--selftest` 通过;默认模式从 `_t24.bin` 重走全表并断言 closure 与身份计数。
3. `REPORT.md` — 结论 + 表 + 失败过的组合 + 未解项。

## 验收

- team closure 精确成立(84,507 行 + 8B footer == 8,819,030)。
- 身份槽 `verified_rows` 达到 84,507/84,507(或明确说明是哪一类身份、覆盖率多少)。
- 25 字段中 **≥18** 有偏移 + 证据。
- `verify.py --selftest` 全 true;**`status` 不得是 `in_progress`**。

## 完成后

一行打印:row_model / closure 等式 / 命名字段数 / 身份覆盖率。
