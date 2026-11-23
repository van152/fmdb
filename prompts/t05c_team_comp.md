# t05c — team(type 24) 行边界 + team/comp 字段级映射

## 角色与硬约束

你是数据逆向工程师。工作区 `D:\tmp2b\fm24-db`,Python 固定 `py -V:3.12 -I -B`。

**只读**:游戏数据目录 `Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\`(含 `client_db.dat`、`server_db.dat`)只读;上游 `D:\tmp2b\fm24\` 全目录只读。**唯一可写 = 本任务 OUTDIR**。不要改 `scratch/t01`、`scratch/t02` 既有文件。

**纪律**:closure 精确算术;允许诚实负结果;第一步先落盘骨架 JSON。

## 任务一(优先):team — type 24,server only,84,507 行

### 已知
- `server_db/table_24.dat`:count = 84,507,payload ≈ 8,819,030 B。上游普查标 `variable_or_nonstandard`,之前一次尝试(fw24)也未闭合。
- **强假设(你要验证或证伪)**:`server_db/table_extra_24.dat` 精确满足 `12 + 82 × 84,507 = 6,929,586`,即 **82 B/row**。若 extra 是主表行的"定长扩展区",则主表行可能是 **82 B 定长标量区 + 行尾若干内联字符串**。
- team schema = **25 个字段、0 个列表**:`unique_id×1, integer×5, string×4, enum×2, database_record_unique_id×9, boolean×1, cash×3`。
  → 4 个 string 若内联(长度前缀)就解释了"变长";若存引用则应为定长 82 B。
  → 25 个字段塞进 82 B 完全可能(9 个 4B 引用=36 + 5 个 4B int=20 + 3 cash=12 → 68,加 enum/bool/duni 需压缩)。

### 判断路线(按顺序试)
1. 取出 table_24 payload,直接验 `14 + 84507*82 + 8 == 8,819,030`?(算一下:84507*82=6,929,574;+22=6,929,596 ≠ 8,819,030 → **不成立**)。所以 82 B 不是全部。
2. 试 `row = 82 + k`,求 k 使整表整除;再验身份槽。
3. 真正路线:**逐行解析**。从 +14 起,先按 82 B 读定长区,再读行尾的字符串结构(常见:`u32 byte_len` + UTF-8,或 `u8 len` + UTF-8);用"下一行 82 B 定长区的首字段/身份槽必须合法"作为行边界约束,正向走满 84,507 行并要求末行结束 == payload_len-8。
4. 反向验证:从 payload 尾部 8 B footer 往前倒推,校验与正向一致。

### 交付(任务一)
- `team.json`:`{"status":"...","type_id":24,"count":84507,"payload_len":...,"row_model":"fixed_plus_strings|fixed|variable","closure":"...","identity":{...},"fields":[{"field":"...","offset":...,"width":...,"evidence":...,"confidence":"..."}],"unresolved":[...]}`
- 25 个字段尽量全命名。命名依据 = schema 顺序 + 类型线宽 + 数据合法性:
  - 引用字段(9 个 `database_record_unique_id`)的值必须落在目标表行数范围(如引用 stadium → <48,413;引用 city → <56,293;引用 comp → <comp count);
  - enum 值必须小于枚举基数;date 必须落在 1800–2100 的合理编码;colour 必须能解释为 RGB。
- 若只能给出部分,如实标注并说明卡点。

## 任务二:comp — type 25,client table_25,255 字段

### 已知
- `client_db/table_25.dat`(competition)。schema 255 字段:44 个子字段 + 15 个 list → **196 个顶层标量**。
- 已解 **18 个字段**:见 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01f\output.json`(`row_offset_map`)与其 `REPORT.md`。
- 上游: `D:\tmp2b\fm24\reports\dbdat_decode\DB_TABLES_BIG.md` 的 `table_25` 段;`D:\tmp2b\fm24\reports\dbdat_decode\client_table_25_competition_samples.json`。

### 要做
1. 先确认 table_25 的行边界模型(定长/变长),给出精确 closure。若既有资料不足,自己解。
2. 在 18 个已知字段基础上**扩展命名**:目标 **≥40 个** schema 字段带偏移。
3. 方法:`mov r8d,N` + `call [rax+0x28]` 宽度序列 + 4CC getter `cmp` 对齐 + 数据合法性验证(club 433 字段那种硬骨头不用碰,这里只要标量)。

## 输入速查

| 用途 | 路径 |
|---|---|
| archive 读取 | `D:\tmp2b\fm24\scripts\modding_read_dbdat.py`(`runpy.run_path` 加载;`list_tables()`、`_resolve_table(tid, ents, 'server_db.dat'|'client_db.dat')`、`_stream_decompress`) |
| schema 字段表 | `D:\tmp2b\fm24\reports\EDITOR_SCHEMA_FIELDS.md`(搜 `### team（记录标识 \`team\`` 与 `### comp（记录标识 \`comp\``) |
| exe | `D:\tmp2b\fm24\input\editor.exe`;reader 入口:team `0x11c1d80`、comp `0xed0a40`(census: `D:\tmp2b\fm24-db\scratch\t01\inbox\t01h\output.json`) |
| 行框架范例 | `D:\tmp2b\fm24-db\scratch\t02\inbox\club_v2\solve.py`(`load_raw()` 解压 + 全表 walker) |
| capstone | 已安装 |

**解压陷阱**:`_resolve_table()` 的 `offset` 不是 zstd 帧起点。从 offset 起向后 64 B 内搜 magic `28 b5 2f fd`,从 magic 起解压。解压后断言 `len == payload_size` 且 `sha256` 与上游普查一致。

**payload 头**:前 8 B `03 01 74 61 64 2e f1 0d`,+10 起 u32 count,行区 **+14** 开始,末尾 **8 B** footer。

## 交付清单

1. `team.json`(见上)
2. `comp.json`:`{"status":"...","type_id":25,"count":...,"payload_len":...,"row_model":...,"closure":"...","named":[{"field","offset","width","evidence","confidence"}],"collections":[...],"unresolved":[...]}`
3. `verify.py` — `--selftest` 通过;默认模式从原始 archive 复算 team 与 comp 的 closure 和字段值分布。
4. `REPORT.md` — 结论 + 表 + 卡点 + 对上游/fw24 旧结论的勘误。

## 验收

- team closure 精确成立,25 字段中 **≥18** 命名(带字节证据)。
- comp 命名字段 **≥40**(在原有 18 基础上净增 ≥22),每个带 `(file offset, bytes)` 证据。
- `verify.py --selftest` 全 true。
- 负结果如实写,不编造。

## 完成后

打印:team 行模型 + closure 等式 + 命名字段数;comp closure + 命名字段数(净增数)。
