# t112 — FM24 只读多表数据库解析库（`scripts/t112_fm24_reader.py`）

**纯 Python（标准库 + vendored `zstandard`），无 IDA / 无 Unicorn 依赖，全表 100% footer 闭合校验。**

- 最终状态：**66 张表全部 `footer_closed == true`**（server 49 + client 17），共解码 **1,942,341 行，6.4 s**，0 字节误差。
- `--selftest` 退出 0（12 项 PASS）；`--verify-all` 退出 0。
- 字段名直接绑定 t110 L3 4CC（全库共 **390 个命名列**）；无 4CC 处诚实命名 `col_<row0_off>`；每行尾部 12B 解出 `identity = {ordinal, uid, dbid}`。

---

## 1. 使用说明

### CLI

```bash
# 列出全部已支持表及校验状态
py -V:3.12 -I -B scripts/t112_fm24_reader.py --list

# 样例行 JSON（--limit 控制，默认 5）
py -V:3.12 -I -B scripts/t112_fm24_reader.py --dump server 45 --limit 5
py -V:3.12 -I -B scripts/t112_fm24_reader.py --dump client 10 --limit 3

# 全表 footer 闭合校验（写 scratch/t112/out/reader_verify.json）
py -V:3.12 -I -B scripts/t112_fm24_reader.py --verify-all

# 自检（合成 t8 行闭合 + 负例越界 + 注册表组成 + 5 张活表抽查 + t45 500 行）
py -V:3.12 -I -B scripts/t112_fm24_reader.py --selftest
```

退出码：`0` 成功 / `1` 校验失败 / `2` 用法或致命错误。

### 作为库导入

```python
import sys; sys.path.insert(0, "scripts")
import t112_fm24_reader as R

arc = R.Archive("server")                 # scratch/data/server_db.dat 只读句柄
pay = arc.payload(45)                     # table_45 的解压 payload
spec = R.build_registry(R.load_traces())  # 表注册表（fixed/variable/empty）
reader = R.TableReader(spec, l3)          # l3 = t110 master JSON
res = reader.verify(pay, sample_limit=3)  # 全行解码 + footer 闭合校验
```

### 数据模型

- **容器层**：FMF 归档 = `data_base` + zstd 压缩目录树 + 成员区。成员边界 = zstd 帧边界，
  以「解压长度 == 目录 `size`」选帧；帧选择失败按 t38 策略扩到下一成员起点重试一次（P2）。
- **payload 层**：13 字节头（magic 6B + version u16 `0xdf1` + row_count u32 + 保留 1B）
  → 每行 `[1B flag + 行体]` → 末尾 9 字节闭合窗 = 末行 identity 终止符 `0x00` + 8B 文件 footer。
  闭合判据：**全部行解完后 `pos == len(payload) - 9`**。
- **行层两类解码器**：
  - `fixed`：t96c 实测 row0 读序列满足 `13 + nrows*(1+rowlen) == footer_off` 且首行读宽和
    == rowlen、末读为 12B identity 时，泛化为全行定长布局。`struct.Struct` 一次解一行
    （84,477 行的 t45 只要 1.6 s），仅样例行物化 dict。
  - `variable`：从 t95/funcs slot19 反编译手写的行程序（VM op：`u` 定宽 / `s` u32 前缀
    字符串 / `id` identity / `v` 向量 / `rep` 固定重复；向量计数 u8/u16/u32，`a7` 服务器门
    已编进程序结构）。逐行解释执行，读上界 `footer_off` 防越界进 footer。
- **命名层**：t110 L3 4CC 按 `wire_off_row0 + in_slot_off` 绑定字段名（direct_field 优先，
  DELE 最后，重名 `#N` 去重）；identity 无 4CC，按结构解出 `{ordinal, uid, dbid}`。

---

## 2. 全表闭合矩阵（`--verify-all`，status: complete）

计数：66 支持 / 66 闭合 / 0 失败 / 13 跳过；fixed 46 + variable 18 + empty 2；总行数 1,942,341。

| 表 | 类 | 行数 | 耗时 | 命名列 | | 表 | 类 | 行数 | 耗时 | 命名列 |
|---|---|---:|---:|---:|---|---|---|---:|---:|---:|
| server/2 | CITY | 56,293 | 52.9ms | 8 | | client/2 | CITY | 56,293 | 66.4ms | 8 |
| server/5 | CONTINENT | 7 | 0.1ms | 1 | | client/5 | CONTINENT | 7 | 0.1ms | 1 |
| server/6 | INJURY | 115 | 0.2ms | 16 | | client/6 | INJURY | 115 | 0.2ms | 2 |
| server/7 | MEDIA_SOURCE | 208 | 8.4ms | 8 | | client/7 | MEDIA_SOURCE | 208 | 7.6ms | 5 |
| server/8 | LANGUAGE | 126 | 1.2ms | 7 | | client/8 | LANGUAGE | 126 | 2.1ms | 7 |
| server/10 | NATION ★ | 251 | 109.1ms | 13 | | client/10 | NATION ★ | 251 | 7.9ms | 8 |
| server/12 | (sub) | 28,597 | 827.3ms | 24 | | client/18 | (sub) | 1,567 | 40.5ms | 11 |
| server/18 | (sub) | 1,567 | 33.9ms | 14 | | client/19 | REGION | 28 | 0.1ms | 0 |
| server/19 | REGION | 28 | 0.1ms | 0 | | client/21 | STADIUM | 48,413 | 63.2ms | 6 |
| server/21 | STADIUM | 48,413 | 100.6ms | 37 | | client/23 | STAGE_NAME | 278 | 0.3ms | 1 |
| server/22 | STADIUM_CHANGE | 449 | 0.7ms | 21 | | client/25 | COMP ★ | 7,047 | 16.3ms | 21 |
| server/23 | STAGE_NAME | 278 | 0.3ms | 1 | | client/27 | WEATHER | 334 | 27.2ms | 4 |
| server/26 | (sub) | 90,128 | 113.5ms | 14 | | client/35 | PLAYER_TYPE | 890 | 0.7ms | 0 |
| server/27 | WEATHER | 334 | 25.7ms | 4 | | client/41 | CURRENCY_RECORD | 173 | 27.8ms | 1 |
| server/30 | STARTING_INJURY | 72,473 | 72.0ms | 8 | | client/47 | (sub) | 2,488 | 38.7ms | 3 |
| server/31 | STARTING_CONFIDENCE | 37,283 | 32.9ms | 0 | | client/56 | AGREEMENT | 6 | 0.0ms | 0 |
| server/33 | STARTING_CLUB_DEBT | 32,409 | 41.9ms | 15 | | | | | | |
| server/34 | STARTING_TEAM_CUP_HISTORY | 7,115 | 7.1ms | 9 | | | | | | |
| server/35 | PLAYER_TYPE | 890 | 0.7ms | 0 | | | | | | |
| server/37 | STARTING_TEAM_LEAGUE_HISTORY | 465,712 | 554.9ms | 12 | | | | | | |
| server/38 | STARTING_BAN | 5,241 | 5.1ms | 7 | | | | | | |
| server/39 | STARTING_AVERAGE_POINTS | 117 | 0.3ms | 1 | | | | | | |
| server/41 | CURRENCY_RECORD | 173 | 27.2ms | 2 | | | | | | |
| server/42 | STARTING_RETIREMENT | 17,721 | 19.8ms | 2 | | | | | | |
| server/43 | STARTING_MONTHLY_INSTALLMENT | 535 | 0.7ms | 5 | | | | | | |
| server/45 | STARTING_RECORD ★ | **84,477** | 1,623.0ms | 16 | | | | | | |
| server/46 | STARTING_DRAFT_TRANSFER | 7 | 0.1ms | 0 | | | | | | |
| server/47 | (sub) | 2,488 | 50.9ms | 3 | | | | | | |
| server/48 | STARTING_RECORD ★ | 5,210 | 109.2ms | 16 | | | | | | |
| server/49 | (sub) | **792,149** | 666.1ms | 2 | | | | | | |
| server/50 | (sub) | 45 | 0.1ms | 0 | | | | | | |
| server/51 | (sub) | 59 | 0.1ms | 0 | | | | | | |
| server/52 | (empty) | 0 | 0.0ms | – | | | | | | |
| server/56 | AGREEMENT | 6 | 0.0ms | 0 | | | | | | |
| server/57 | (empty) | 0 | 0.0ms | – | | | | | | |
| server/58 | (sub) | 8 | 0.0ms | 4 | | | | | | |
| server/59 | (sub) | 9,079 | 49.7ms | 0 | | | | | | |
| server/60 | (sub) | 59 | 0.1ms | 2 | | | | | | |
| server/61 | (sub) | 16 | 0.0ms | 0 | | | | | | |
| server/62 | (sub) | 37,214 | 39.5ms | 10 | | | | | | |
| server/63 | (sub) | 2 | 0.1ms | 0 | | | | | | |
| server/64 | (sub) | 6,946 | 7.0ms | 0 | | | | | | |
| server/65 | (sub) | 1,417 | 1.8ms | 4 | | | | | | |
| server/66 | (sub) | 753 | 0.9ms | 4 | | | | | | |
| server/67 | (sub) | 6,826 | 8.3ms | 4 | | | | | | |
| server/68 | (sub) | 138 | 0.2ms | 4 | | | | | | |
| server/69 | (sub) | 230 | 0.3ms | 4 | | | | | | |
| server/70 | (sub) | 10,075 | 9.1ms | 10 | | | | | | |
| server/73 | (sub) | 1 | 0.1ms | 0 | | | | | | |

★ = 提示书点名的核心大表/加分表。server/12、server/59 等为 prompt 之外顺带闭合的子表。

### 跳过的 13 张（诚实原因，见 reader_verify.json `skipped_tables`）

- 无闭合方程、无手写程序：server/0 AWARD、server/3 CLUB、server/9 NATIONAL_TEAM_CONTAINER、
  server/24 NATIONAL_TEAM、server/25 COMP(server)、server/32 STARTING_FUTURE_TRANSFER、
  server/36 STARTING_MANAGER_HOF_RECORD、server/71 STARTING_PAST_TRANSFER、
  server/72 STARTING_PAST_TRADE、client/0、client/3、client/9。
- slot19 C 不完整：server/29 STARTING_LOAN（sub_1445195D0 调用链缺 .c）。
- 注：client/25 COMP 已接入（7,047 行闭合）——prompt 的加分项「table_25 COMP (client)」达成。

---

## 3. 真实样本（节选自 reader_verify.json `sample_rows`）

**client/10 NATION**（row 0，本国 = England，identity uid=dbid=5）：

```json
{"Ngct": 1, "Ncti": 0, "Nrgi": 7, "NcpR": 1187, "Ncur": 1, "Nsod": 2, "Necf": 13,
 "col_19": 0, "Nygn": 7, "col_25": 100, "col_29": 9, "col_30": 50, "col_34": 78,
 "col_35": 10, "col_39": {"ordinal": 0, "uid": 5, "dbid": 5}}
```

**server/6 INJURY**（row 0）：`icla=12, iscl=48, Imnd=1, Iexd=3, Iiar=50, Iocr=1.5(f32),
Iagr=2, Icms=3, Icon=1, inSr=5, Ibin=9`

**server/8 LANGUAGE**（前两行）：

```json
{"col_0": "Albanian", "Linf": 0, "Ldff": 15, "Lfam": 44, "Lgro": 1, "Lsub": 20, "Lnat": 126, "dbnm": 1}
{"col_0": "Arabic",   "Linf": 12, "Ldff": 18, "Lfam": 1,  "Lgro": 18, "Lsub": 5,  "Lnat": 78,  "dbnm": 2}
```

**server/5 CONTINENT**：`Crgs=1062836634(f32 0.72…), col_10=30472, col_12=8744`（row 0）

**server/22 STADIUM_CHANGE**（row 0）：`Smot=86, Sold=1129, Snew=39316, Slea=132645076,
Ssta=132907220, Styp=1, Scpm=4, Snxa=40000, Slhm=52`

**server/33 STARTING_CLUB_DEBT**（row 0）：`col_0=51(club), Ctbu=239, stdt/endt=124518401,
Ccfa=3, comp=4294967295`

**server/37 STARTING_TEAM_LEAGUE_HISTORY**（row 0）：`divi=6330, year=2005, posi=5,
play=22, wins=10, draw=6, lost=6, gfor=34, gaga=24, poin=36, mxtm=12`

**server/45 STARTING_RECORD（84,477 行全解，rowlen == 80 + namelen，18 列）**：

```json
{"col_0": 71, "stid": 8325867, "stnm": "Markelian Xhai", "stdt": 124518401,
 "endt": 124518401, "stdb": 124518401, "apps": 65535, "gols": 65535,
 "rati": 100, "info": 79, "rrea": 0, "etin": 0, "identity": {"ordinal": 0, "uid": 1, "dbid": 1}}
{"col_0": 72, "stid": 8326023, "stnm": "Elvin Beqiri", "rati": 75, "rrea": 1, ...}
{"col_0": 75, "stid": 2000010224, "stnm": "Ndunguidi Daniel", "rati": 100, "etin": 1, ...}
```

**DATE 线格式**（本次逆向确证）：u32 = `[day-of-year u16][year u16]`（LE），
`01 00 6c 07` = 1900 年第 1 天（占位默认），`98 00 e7 07` = 2022 年第 152 天。

---

## 4. t10 NATION：三个缺失反编译的元素解析器的实证求解

t10 的 slot19 解析器 `sub_1410404C0`（server/client 同函数，按 `a7` 分块）在
scratch/t95/funcs 有完整 C，但其中三个向量元素函数 **没有 .c 文件**：
`sub_1415CFD70`、`sub_141072F60`、`sub_1415CFEA0`（14104F0B0 是 143EE0430 的 thunk，
二者都只是「读 u32 计数 + 循环调 sub_141072F60」的包装）。求解过程
（探针：`scratch/t112/solve_t10.py`）：

1. **结构锁定**：Unicorn row0 全读序列（server 202 条 / client 20 条）+ C 逐行对照，
   得到 a7=1/0 两条流程的完整骨架（server 10 组向量 + a7 尾块 10×u32+u16+u8；client
   短头部 + 3 组向量）。row0 中所有未知向量计数恰为 0，元素大小不可见。
2. **字节记账穷举**：全表 251 行按候选元素宽度做纯字节记账行走，
   以「行尾 identity 序号 == 行号」为锚、`pos == footer_off` 为闭合判据。
   - **client 先解**：唯一未知 s_CFEA0，0..48 穷举 → **唯一解 28**（7×u32，slot5/6 为
     DATE 型值），251 行全闭合，且顺带独立证实 `sub_1410605B0` 元素 = [u32, DATE, DATE]（12B）。
   - **server**：row 52 首个非零 143EE0430 计数（=1）暴露 s_72F60 → 行内 identity 锚定唯一解
     **14**（[_P1,_P4,_P4,_P1,_P1,_P2,_P1]，13 行非零样本字节全一致）。
   - row 162 的 v127 计数 = 7 时所有定宽候选全灭 → 手解发现 **元素含字符串**：
     `sub_1415CFD70` 元素 = **[u8, str, str, 7×u32]**（例如 `01 | "Bruno" | "de Carvalho" |
     0 | 0 | DATE(1978,d39) | 1509 | 788 | -1 | uid`——主教练姓名记录）。
     字符串元素进入 VM 程序后全表闭合。
3. **结果**：server/10 与 client/10 均 251 行 100% `footer_closed == true`（109ms / 8ms）。

副产物：DATE 线格式确证为 `[day-of-year u16][year u16]`；NATION 头部 u16 计数向量
（v128）与 u32 计数向量（v126）在两个库全部 251 行中计数恒 0（结构仍按 C 保留）。

---

## 5. 交付物与验收

| 项 | 结果 |
|---|---|
| `scripts/t112_fm24_reader.py` | 66 表（fixed 46 + variable 18 + empty 2），CLI 4 模式，退出码 0/1/2 |
| `scratch/t112/out/reader_verify.json` | `"status": "complete"`，66/66 `footer_closed=true`，1,942,341 行，每表 `rows_decoded/elapsed_ms/footer_closed/l3_named_fields/sample_rows(前3行真实数据)` |
| `scratch/t112/out/REPORT.md` | 本文档 |
| `scratch/t112/out/DONE.md` | `DONE type=t112` + 核心统计 |
| 验收 1：`py -V:3.12 -I -B scripts/t112_fm24_reader.py --selftest` | 退出 0（12 项 PASS） |
| 验收 2：≥25 张表 100% footer_closed | **66 张**（超出 2.6 倍） |

约束遵守：所有输入只读（scratch/data、t96c/t110 产物、t95/funcs）；未修改 `reports/` 与 `LEDGER.json`。
探针脚本 `scratch/t112/solve_t10.py`、`trace_funcs.py`、`extract_prog.py`、`ctrees/*.txt`
为本任务的过程工具，不影响交付。
