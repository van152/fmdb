# t138 — 纯 Python 全量解码 people_db.dat（658,011 人 / 400,443,970 B 零依赖闭合）

**结果：全量闭合达成 — `diff == 0`。** 纯 Python（stdlib + vendored `zstandard`，运行时零 Unicorn / 零 IDA）
流式解析器按真实 C 文法走完 decompressed payload 的**每一个字节**：

| 指标 | 值 |
|---|---|
| rows_decoded | **658,011**（= 头部 count，= 任务给定直方图总和） |
| total_bytes | **400,443,970**（zstd 解压后，内存中，无磁盘 dump） |
| end_offset | **400,443,970 = EOF**（`footer_closed: true`） |
| **diff** | **0** |
| oracle（前 3,000 行 vs `scratch/t126/out/_walk.json`） | **0 mismatches**（含 end_offset 1,216,813 的 limit 模式复验） |
| 直方图 | `{1: 166064, 2: 476158, 3: 4757, 4: 9839, 5: 1193}`（与任务给定**逐型完全一致**） |
| BranchError | **0**（全量 walk 中所有受保护未知分支均未触发） |
| selftest | **PASS**（5 类合成行全部 `exact: true` + 2 个 14141E220 定向用例） |
| 耗时 | 解压 0.5s + walk ~16s（`py -V:3.12`，单线程纯 Python） |

## 交付物

- `scripts/t138_people_pure_py.py` — 解析器本体（`--verify-full` / `--limit N` / `--selftest` / `--out`）。
  ~60 个文法函数逐一镜像 `scratch/t138/out/ida/<funcva>.c`（idalib 仅用于 `scratch/t95/editor_work.i64`，
  `editor_merge_v2.i64` 全程只读未碰）。每个 C 分支诚实映射；不可判定分支 `BranchError` 带行号/偏移停机，
  **全量 walk 中一次都没有触发**。
- `scratch/t138/out/people_pure_py_verify.json` — 全量 walk 结果（本 REPORT 的全部数字来源）。
- `scratch/t138/out/people_pure_py_selftest.json` — selftest PASS 记录。
- `scratch/t138/out/ida/` — 247 个函数的 Hex-Rays 反编译（`t138_ida_callees.py` 生成，含 4 轮探测）。
- `scratch/t138/out/_row1331_trace.json` — 行 1331 的 293-read Unicorn 地面真值（修 14144AD70 时生成）。

## 文法要点（全部 C 级验证，无启发式跳过）

- **行结构** `[u32 ordinal][u8 ptype][body]`，ptype→slot19 多态读取链：
  1=NON_PLAYER(0x140DC1D30)、2=PLAYER(0x140E06EC0)、3=双读取器（a3=0 只跳过各子读取器的尾链，
  分发器自身跑一次 DD8520→DFB5C0→PERSON base）、4=OFFICIAL(0x1415856B0)、5=RETIRED。
- 缓冲流语义：每个 `slot40(dst,len)` = 一次 wire 读；被调者序言的排队读会移动调用者归属但**不改变 wire
  次序/总量** — 本解析器按 wire 次序消费，与 t120 trace 逐 read 对齐。
- 本次会话修正的两处分歧（均由行 1331 run-away + t120 全 trace 定位）：
  - `sub_14141E220` 元素：version≥0xDCD 时 `[1][2][1][1 b]; b==1?[4]:[8]`（14432a580.c L1-138）。
  - `sub_14144AD70`（PLAYER f3 对象）：**55B 固定**（两次无条件 `sub_140DB8980` [4] 读；先前 53B 是
    摘要算术错误，+2B 错位曾导致行 1331 后 400MB run-away）。
- **自测builder同步**：`_build_player_body` 的 f3 对象 53→55B（与上一条同步，否则 selftest 过读）。

## Footer 闭合（28 字节）— 本次会话的 C 级攻坚

行循环结束后 payload 剩 28 字节（400,443,942..400,443,969）。四步钉死：

1. **Loader 只读前 8 字节**（C：`sub_140F64530` case 3 读两个 `[4]` = case-3 表 pass1/pass2 count；
   且用 t120 在真实字节上仿真真 stage machine 复证：恰好 8 字节后 stage→4→5 清理，无更多读）。
   本档两 count 均为 0 → 无元素读。解析器对非零诚实地 `BranchError`（元素读会跟随，不可跳过）。
2. **同族尾包文法**（`sub_140F2FE70` 尾 → `sub_140FFAFD0`）：`[u32 n] + n×(u64 uid + u32 idx)` 索引
   + `[u8 flags]` + `[u32 value]`。在 **basic_people_db.dat**（同 "tad." 族、同 envelope、同 zstd 单帧、
   count 同为 658,011）上实证：其末 9 字节 = `[4]=0 [1]=01 [4]=末行 uid(0x7754bd4c)`，与 t92 table_9
   footer `00 00 00 00 01 ec 7a e4 04` 同形 —— 族尾包实证闭合。
3. **people_db 的 28 字节布局**（机器逐字节核验，01 字节在 footer 偏移 **9 与 23**——手工求和两次出错
   后改为一律机器核验）：`[4]=0 [4]=0`（loader 两 count）+ `00 01 00 00 00×9`（11B commit 残留，
   首个 u32 = 0x100）+ 偏移 19 处族尾包 `[4] n=0 [1]=01 [4]=0`（该 9 字节形状在全 28 字节内**只有**
   偏移 19 一个对齐能容纳两个 01 的位置）。
4. **20 字节"writer-only"证明**（无任何读取方消费）：(a) stage machine 恰 8 字节后返回 true；
   (b) 族尾包文法与 basic 实证吻合；(c) `people_db.dat` zstd 帧后无多余字节（unused_data=0），
   即 20 字节确在 payload 内、由保存侧 commit 层写入；(d) 所有 loader 调用方（0x140035880/0x140049bb0/
   0x14004af40）在 stage machine 后零 stream 读。解析器对这 20 字节做**逐字节精确断言**
   （`decode_footer`），任何偏差即 `BranchError` —— 是闭合校验，不是行级跳过。

旁证：同族其余文件（client_db/server_db/lang_update_db）是嵌套 `"fmf."` 容器（`02 01 "fmf." 08 00 00`），
people_db/basic_people_db 是单 blob 直压 —— 与上述"单段+writer 尾包"结构自洽。

## 统计产出

- body 长度（按 ptype）min/max：`{1: 292/2149, 2: 457/2037, 3: 582/1765, 4: 115/181, 5: 28/67}`。
- **Top-20 球员按 CA**（ptype 2/3，`body+6` u16），姓名经三路 name-id 读取（`sub_143B934A0` 的三个
  `[i32 id][u8 flag]`，flag≠0 时行内注册新名字 `sub_1410B9440`）解析到 `scratch/t106/out/
  payload_server_name_table_extra_{0,1,2}.bin`（12B 头 + `[u32 uid][u32 len][utf8]`，t106 闭合验证）。
  common 名优先，否则 `first second`（t135 约定）：

| # | CA | 姓名 | uid | 行号 |
|---|---:|---|---:|---:|
| 1 | 190 | Kevin De Bruyne | 18004457 | 474633 |
| 2 | 188 | Kylian Mbappé | 85139014 | 387095 |
| 3 | 188 | Erling Haaland | 29179241 | 251231 |
| 4 | 185 | Lionel Messi | 7458500 | 63517 |
| 5 | 184 | Harry Kane | 28049320 | 413499 |
| 6 | 184 | Vinícius Júnior | 19302146 | 38111 |
| 7 | 181 | Mohamed Salah | 98028755 | 647489 |
| 8 | 181 | Thibaut Courtois | 18026122 | 474634 |
| 9 | 180 | Rodri | 67217524 | 156364 |
| 10 | 180 | Ederson | 55057659 | 38112 |
| 11 | 178 | Virgil van Dijk | 37024025 | 266447 |
| 12 | 178 | Robert Lewandowski | 719601 | 243057 |
| 13 | 178 | Bernardo Silva | 55041632 | 214364 |
| 14 | 177 | Jude Bellingham | 29232937 | 413501 |
| 15 | 176 | Declan Rice | 28106491 | 413502 |
| 16 | 176 | Alisson | 19058734 | 38113 |
| 17 | 175 | Marc-André ter Stegen | 35017428 | 369879 |
| 18 | 175 | Neymar | 19024412 | 38114 |
| 19 | 174 | Bukayo Saka | 28122642 | 413503 |
| 20 | 174 | Joshua Kimmich | 92039023 | 369880 |

**交叉验证**：#1–#18 的姓名/CA/uid 与 t135（Unicorn 引擎逐卡验证）完全一致；#19–#20 为其表的顺位
延伸。每张卡还带 54 个 `PDxx` 属性（`body[44:98]`）存于 verify JSON 的 `pdxx_hex`。

名字解析顺带修出一个真 bug：Top-20 的末行 identity 此前把**下一行 5 字节行头**裹进 body 末尾，
`(ordinal, dbid, uid)` 三元组右移 5 字节读错 —— Top-20 重解码断言（`rr.p != nxt` 即 raise）把它暴露
并修正（`nxt = body_off[i+1] - 5`）。

## 约束遵守

- 只写 `scripts/t138_people_pure_py.py`、既定工具 `scripts/t138_ida_callees.py`/`t138_caller_probe.py`、
  `scratch/t138/out/**`；未触碰 `reports/`、`scratch/t01/LEDGER.json`、任何其他 `scratch/tNN/`。
- `people_db.dat`/`editor_merge_v2.i64` 只读；400MB 解压全程在内存；无磁盘 dump。
- idalib 仅打开 `scratch/t95/editor_work.i64`；反编译只落 `scratch/t138/out/ida/`。
- 最终解析器运行时零 Unicorn / 零 IDA（Unicorn 仅作调试 oracle）。

## 复算

```bash
py -V:3.12 -B scripts/t138_people_pure_py.py --verify-full   # diff 0, footer_closed true, oracle 0/3000
py -V:3.12 -B scripts/t138_people_pure_py.py --selftest      # PASS (5 cases + 2 targeted)
```
