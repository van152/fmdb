# t07 任务书：全局 4CC 表 —— 让 city/regi/stad 等也能命名

## 一句话目标

把 `scratch/t05/4cc_global.json` 做成**可信的全局 4CC → 字段偏移表**，验收标准是能复现下面两组已知答案（缺一即 FAIL）。

## 为什么需要这个任务（背景，全是已验证事实）

本仓已打通三段链（见 `scratch/t01/LEDGER.json` 的 E39/E40/E41/E42）：

1. **reader 指令流 → 行内偏移**：`lea rdx,[obj+OFF]` + `mov r8d,W` + `call [rax+0x28]` 累加，闭包 `sum(W)==stride-13`。已产出 `scratch/t05/layouts.json`（26 实体 / 240 槽 / 覆盖 151 万行）。
2. **4CC 分发链 → 字段名**：`cmp edx,'<4CC>'; je <getter>` 或 `cmp edx,'<4CC>'; jne <skip>; ... mov [rsi+OFF],reg`。
3. **getter 成员访问 → 同一 OFF**，把 1 和 2 连起来。

**当前卡点**：`scripts/t05_name_fields.py` 只在 **reader body 之后 0x6000 字节**内找 4CC 链，因此只有 injury(type6) 和 type22 成功。
但已实证 city(type2) 的 4CC 链存在，只是**远在别处**：

```
0xe55098  cli / outsb / insb ...        ← 前面若干字节不是指令边界，从这里开始反汇编才对齐
0xe5509c  je      0xe55284              ← 属于 Clat
0xe550a3  cmp     edx, 0x436c7269       ← 'Clri'
0xe550a9  je      0xe552e6              ← Clri 的 getter
0xe550af  cmp     edx, 0x436e616d       ← 'Cnam'
0xe550b5  jne     0xe5545d              ← Cnam 走 setter(fall-through)
0xe55284  movss   xmm6, dword ptr [rdi + 0x4c]   ← Clat 的 getter 体
```

city 的 reader body 在 `0x3aa5550`，与上面相距约 0x2C 万字节 —— **"dispatch 链紧邻 reader" 只对手写优化的实体成立**，必须改用全局扫描。

## 现状（你接手的地方）

`scripts/t05_4cc_global.py` 已写出并跑通框架：

- 用 `cmp reg,imm32` 的机器码（`81 FA/FB/F9/F8/FE/FF/FD/FC`、`3D`）做**字节搜索**定位 4CC，比 capstone 全扫快百倍；
- 在 70.1MB 可执行段里找到 **18,837 处** `cmp` 候选、**8,954 个不同 4CC**；
- 已修 `base_va`：disasm 的 base 必须传 **VA**（`pe.f2va(off)`），否则 `je` 目标会是 file-offset 形式却被当成 VA 换算。

**已知缺陷（你要修的）**：

1. **`size` 判错**：Clri 目前得到 `off=0x38 size=8`，但按 city 的布局它应是 4 字节引用。原因是"跟随 je 目标后取第一条 mem access"会抓到 `mov rax,[rdi+0x38]` 这类**对象内部指针取用**，不是字段读取。
   正确做法：只接受 `movzx/movsx/movss`（窄读）或 `mov dword/byte/word ptr [reg+OFF], reg`（窄写）作为字段访问证据；`mov r64, qword ptr` 大概率是取内部指针，应跳过。
2. **单选歧义**：同一 4CC 常出现 3-4 处（不同属性系统/不同版本）。需要**按证据强度打分**而不是取第一个。
3. **误报率高**：8,954 个 code 里大量是巧合的 ASCII。可用 `--code` 逐个查，但要建全表必须过滤。

## 两个校准集（必须在你的输出里 100% 复现）

### A. injury(type6) —— 已有 4CC getter 直证 + 数据验证双背书

| 4CC | object_off | size | 已验证的 row_off |
|---|---:|---:|---:|
| `icla` | 0x4c | 1 | 0 |
| `iscl` | 0x4d | 1 | 1 |
| `Imnd` | 0x34 | 2 | 3 |
| `Iexd` | 0x36 | 2 | 5 |
| `Iiar` | 0x58 | 1 | 7 |
| `Irec` | 0x59 | 1 | 8 |
| `Iocr` | 0x30 | 4 | 13 |
| `Imip` | 0x50 | 1 | 17 |
| `Iagr` | 0x51 | 1 | 20 |
| `Icms` | 0x52 | 1 | 21 |
| `Icon` | 0x53 | 1 | 22 |
| `inSr` | 0x54 | 1 | 23 |
| `Icdp` | 0x56 | 1 | 25 |

（`Ibph/Ibsp/Ibin/Ibis/Ibpg` 五个共享 `0x57`，那是位打包，不算失败。）

现有 `scripts/t05_name_fields.py` 在 injury 上已能做到 13/13，**你的新工具必须不劣于此**。

### B. city(type2) —— 偏移由独立人工/数据双证，但 4CC 归属待定

city 的 9 个槽（`scratch/t05/layouts.json`，业务区 30B）：

```
row+0  w=1    row+1  w=8(Clat+Clon 合并)   row+9  w=1
row+10 w=4    row+14 w=4                  row+18 w=3
row+21 w=4    row+25 w=4                  row+29 w=1
```

已知语义（E30 人工解 + E42 引用验证）：

| row_off | width | 字段 | 证据 |
|---:|---:|---|---|
| 1,5 | 4+4 | `Clat` / `Clon` | f32 对，纬 -54.81..78.22 / 经 -179..179 |
| 10 | 4 | `Cnti` | u32 值域 0..249，type9 nation 251 行 |
| 14 | 4 | `Cwea` | u32 max=333，type27 weather 334 行（fill 0.997） |
| 21 | 4 | `Clgi` | 81.73% 为 0xFFFFFFFF 哨兵，非哨兵 max=112，language 126 行 |
| 25 | 4 | `Clri` | 非哨兵 max=2476，type47 lcrg 2488 行（fill 0.995） |
| 0,9,18,29 | 1/1/3/1 | 未定 | — |

**你的验收**：把 `Clat/Clon/Cnti/Cwea/Clgi/Clri` 这 6 个 4CC 的 `object_off` 全部正确解出（并与 city 的 reader obj_seq 对齐），且 `size` 全部为 4（Clat+Clon 段可为 4 或 8）。

提示：已知 `Clri` 的 cmp 在 file offset `0xe550a3`、`je` 目标 `0xe552e6`；`Cnam`/`Clon`/`Clat` 在 `0xe55098–0xe550c0` 同一段内。可用这些做自检锚点。

## 你要交付什么

写到 `scratch/t07/out/`：

1. `4cc_table.json`
   ```json
   {"codes": {"<4CC>": [{"file_off":"0xe550a3","object_off":76,"size":4,
                          "kind":"read","access_va":"0x...","score":0.95,
                          "why":"je 目标块内 movzx byte ptr [rdi+0x4c]"}]}}
   ```
   每个 4CC 保留 1-4 条候选，带 `score` 与 `why`（一句可核对的证据）。
2. `naming_result.json` —— 对 `layouts.json` 里 26 个实体逐槽命名（用 `object_off` 连接），
   并标 `confidence`（`readpair` / `ref_only` / `unresolved`）。**不得修改 row_off/width。**
3. `verify.py` —— 可复跑自检，必须覆盖：
   - injury 13/13 复现（表 A）
   - city 6/6 复现（表 B）
   - 所有命名槽的 `size` 与 `layouts.json` 的 `width` 一致（Clat+Clon 合并槽除外）
   - 逐槽比对 `row_off/width` 与 layouts.json **完全未变**
4. `REPORT.md` —— 全局表规模、city/injury 复现情况、误报过滤策略、未解析原因

## 技术要点（别踩的坑）

- **disasm 的 base 必须传 VA**：`md.disasm(raw[file_off:...], pe.f2va(file_off))`。传 file_offset 会让 `je` 目标算成 file-offset 形式，再经 `va2f` 就错位（这个 bug 已在本仓出现过一次）。
- **cmp 位置不是指令边界**：用字节搜索到的 `81 FA` 位置需先反汇编确认 `mnemonic == "cmp"` 才可用。
- **两条链**：`je` 目标（getter 读）与 fall-through（setter 写，紧接 `jne skip` 之后）都要收。
- **窄读才算字段**：`movzx/movsx/movss` 与 `mov byte/word/dword ptr [reg+OFF], reg` 是字段访问；`mov r64, qword ptr [reg+OFF]` 多为内部指针，跳过。
- 偏移合理区间 `0x20 <= OFF <= 0x400`。
- 不许联网、不许改本仓既有文件、只写 `scratch/t07/out/`。

## 纪律

- **先落盘骨架**（`4cc_table.json` 先写 `{"status":"in_progress"}`，边做边覆盖）。
- 完成时 `status` 写 `complete_<限定词>`。
- 复现不了就如实报负结果，**禁止把校准集硬编码进程序**（verify 里可以硬编码期望值，生成逻辑里不行）。
