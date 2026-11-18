# t20 — club 子表 t22 cursor 重建（partial）

## 结论

- `status=partial_cursor_t22_branch_paths_unreconciled`。
- E56 的 A 级 4CC 证据裁定 table 22 是 **club 球场/迁建属性集**；RTTI 名 `STADIUM_CHANGE` 是运行时类名，不等同于 stadium 主表实体。`scratch/t14/out/census.json` 的类名与 `reports/stage2_table_identity.json` 的实体归属分别记录，未混为一谈。
- 行封口已确认：449 × 79 B，行起点 14，payload 方程 `14 + 449*79 + 8 = 35493`。静态 reader 的候选业务宽度和为 66，`66 + 13 = 79` 只封住**字节预算**；它还不是已证实的逐字段 cursor。
- 关键证伪：t16 的 slot-19 线性 walk 有 23 个分支；reader width scan 的候选线性窗跨越分支屏障。直接累加所得偏移与数据侧日期分布矛盾，因此**不把候选偏移升级为行坐标**。

## 静态定位与候选序列

- Factory handler：file offset `0xF49092`；RTTI 类 `STADIUM_CHANGE`，vtable VA `0x1418BD5A8`。
- slot-19 reader：VA `0x141538200` / file offset `0x1537800`。t16 in-memory walk 在同一函数得到 18 个带 object sink 的传输，分支数 23。
- `scratch/t05/reader_widths.json` 的 40-call scan 中，开头 19-call 窗口宽度为：`4,4,4,4,1,4,1,4,4,4,4,4,1,4,1,1,1,4,12`，和为 66。前 18 项与 t16 事件宽度/object_off 一致；第 19 项 12 B 的宽度指令为 file offset `0x1537AA8` / VA `0x1415384A8`，call 为 `0x1537AB4` / `0x1415384B4`，object sink 未解析。
- 这仅给出 `row_offset_candidate`。`cursor_t22.json.steps[].row_offset` 与 `fields_t22.json.fields[].row_offset` 均为 `null`；候选线性偏移单独保存，未伪装成结论。

## 数据侧冲突与保留项

- `scratch/t13d/out/audit.json` 对 +12、+16、+50 给出稳定的 packed day/year 画像（年份范围分别为 2000–2030、2017–2030、1900–2030）。候选线性配对却会把 +12 叫作 `Scap`（New Capacity）、把 +16 起始字节叫作 `Styp`（Type）、把 +50 叫作 `Sceb`（Future Stadium Development Fund）；这些不是可接受的独立互验。候选 `Salt@+17` 还落在 +16 日期内部。故 cursor 路径保持 partial。
- 可保留的代码/字段名候选共 15 个，均未获得 row offset 晋级；`Sold`、`Snew` 在 club.Cstc 中各有多个 schema occurrence，仅保留 code-only；slot 0 和 12-byte bulk 未命名。台账为 0 个已确认行坐标字段，不以候选名计入命名率。
- E56 四个唯一码（`Salt`、`Scam`、`Scpm`、`Slhm`）只确认 club 字段身份，不提供 row offset。当前工作区版本的 `scratch/t15/out/fk.json` 未发现 table_type=22 项；本报告的 FK 兼容旁证取自 t13d 审计及 CSV：+0 有 361 个非 `0xFFFFFFFF` 行值、310 distinct，live 范围 `[86,82403]`。它说明 club-ID 域兼容，不独立证明表身份。任务书提及的 362 值计数与当前 CSV 审计口径未合并，保留为计数口径差异。

## 交付与验证

- `cursor_t22.json`：RTTI/factory/slot-19 定位、19 个宽度候选、stride 字节预算与未闭合原因。
- `fields_t22.json`：449 行字段候选台账；所有未证实坐标为空，重复 4CC 与数据画像冲突保留。
- `verify.py`：`--help`、`--selftest` 均可用；默认检查通过（状态仍为 partial）。
- `scripts/t20_build.py`：仅读现有证据与 editor.exe；只写 `scratch/t20/out/`。`--help`、`--selftest` 已运行通过。
- t64、t66 未启动：主目标的 row cursor 仍需分支路径解决，避免用未闭合方法扩散。

## 主要来源

`scratch/t14/out/census.json`、`scratch/t05/reader_widths.json`、`scratch/t12/out/codes_full.json`、`scratch/t13d/out/{t22.csv,audit.json,quick_audit.md}`、`reports/stage2_table_identity.json`、只读 `D:\tmp2b\fm24\input\editor.exe`（SHA-256 见 `cursor_t22.json`）。
