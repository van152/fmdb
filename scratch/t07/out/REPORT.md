# t07 全局 4CC 表报告

## 结果

状态：`complete_with_ref_only`。校准集均通过 `verify.py`：**injury 13/13，city 6/6**；26 个实体的全部 240 个槽均在 `naming_result.json` 中保留原始 `row_off/width`。

| 实体/字段 | object_off | size | 关联槽 |
|---|---:|---:|---|
| city `Clat` | `0x48` | 4 | row+1 的 8B 坐标槽前半 |
| city `Clon` | `0x4c` | 4 | row+1 的 8B 坐标槽后半 |
| city `Cnti` | `0x20` | 4 | row+10 |
| city `Cwea` | `0x28` | 4 | row+14 |
| city `Clgi` | `0x30` | 4 | row+21 |
| city `Clri` | `0x38` | 4 | row+25 |

`Clat/Clon` 是两个 4B 读访问，覆盖 reader 的合并 8B 槽。按指令边界重新解码，`file_off=0xe55097` 是 `cmp edx,'Clon'`，其 `je` 目标在 `file_off=0xe55284` 读 `[rdi+0x4c]`；`Clat` 的窄读为 `[rdi+0x48]`。这与 row+1/row+5 的独立纬度/经度数据及 reader 顺序一致；任务书示例把前一个分支标成 Clat，和实际 cmp immediate 不符。4 个引用字段的宽度由 reader 槽和独立引用数据验证确定；全局 getter 链首个访问是同偏移的 qword 引用包装，因此记录为 `kind=ref_only`，未把 qword 指针误报成 8B 字段读。

injury 表 A 的 13 个 (object_off,size) 均复现：`icla 4c/1, iscl 4d/1, Imnd 34/2, Iexd 36/2, Iiar 58/1, Irec 59/1, Iocr 30/4, Imip 50/1, Iagr 51/1, Icms 52/1, Icon 53/1, inSr 54/1, Icdp 56/1`。位打包字段仍按共享偏移处理，不计入上述 13 项。

## 全局扫描规模

- `editor.exe` SHA-256：`b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`
- 可执行段字节搜索后，经正确指令边界与 `cmp` immediate 二次确认：18,031 处 cmp、8,399 个不同的 4CC 候选。
- 输出保留 1,477 个有证据条目的 4CC、共 2,103 条候选：1,473 个窄读/窄写来源 code，另有 city 4 个 `ref_only` 字段来源。
- 每个 code 最多保留 4 条按证据排序且位置/宽度有区分的候选。分数是可复核的启发式排序，不是统计概率。

## 过滤与证据口径

1. 仅扫描 PE 可执行段的 `cmp reg,imm32` 字节编码；命中后从 `pe.f2va(file_off)` 得到的 VA 开始反汇编，必须确认首指令确为 `cmp` 且 immediate 与字节候选一致。跳转目标再用 `va2f` 回到文件偏移。
2. 同时收 `je/jz` 目标 getter 与 `jne/jnz` fall-through；访问候选限定为 0x20..0x400 的 byte/word/dword 窄读或窄写。qword load 不作为字段访问证据，避免把内部引用包装误判为字段宽度。
3. 读写证据与 reader `obj_seq` 的 object offset/width 对齐后加分；字段命名另受实体 schema 代码与字段类型约束。已有独立 assignment 只作为显式的 ref-only 证据或歧义约束。
4. city 的 `Cnti/Cwea/Clgi/Clri` 宽度使用现有 `scratch/t06/out/assignments.json` 的行数据引用验证，并由 reader offset 对齐；候选 why 保留了分发 cmp 与首个包装指针访问的位置。它们没有被伪装成窄读结论。

## 未解析项

`naming_result.json` 汇总为 37 个 `readpair`、8 个 `ref_only`、195 个 `unresolved` 槽。未解析表示当前证据不足，不是空字段结论；主要原因是没有可信 4CC 窄访问、schema 多义、reader 槽为打包/常量字节，或全局同偏移候选无法唯一归属。候选表规模大于可命名字段规模，未把 ASCII 偶合直接当作结论。

## 复跑

```powershell
py -V:3.12 -I -B scratch/t07/out/build.py --help
py -V:3.12 -I -B scratch/t07/out/build.py --selftest
py -V:3.12 -I -B scratch/t07/out/build.py
py -V:3.12 -I -B scratch/t07/out/verify.py --help
py -V:3.12 -I -B scratch/t07/out/verify.py --selftest
py -V:3.12 -I -B scratch/t07/out/verify.py
```
