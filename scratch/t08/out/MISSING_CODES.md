# MISSING_CODES — Sold / Salt 与 Snew

## 结论

`Sold` / `Salt` **不是比较指令编码漏扫**。在 t22 getter 的局部 dispatch 区域内，两者都是普通 `cmp r32, imm32`，原始字节和 immediate 可直接复核：

| code | file_off | 指令 bytes | 解码指令 | 条件目标 | 目标块首个对象成员访问 |
|---|---:|---|---|---|---|
| Sold | `0x1538f2d` | `81 fa 64 6c 6f 53` | `cmp edx,0x536f6c64` | `0x141539da6` (`file_off=0x15393a6`) | `mov rcx,qword ptr [rbx+0x20]` |
| Salt | `0x153920a` | `81 fa 74 6c 61 53` | `cmp edx,0x53616c74` | `0x14153a10d` (`file_off=0x153970d`) | `mov rcx,qword ptr [rbx+0x48]` |

同一 Salt dispatch 的 setter 分支也操作 qword wrapper（`[rsi+0x48]`）。上述比较码不是 `cmp r8d,imm32`、`cmp r/m32,imm8`、寄存器间接比较或跳转表编码；本次检查直接见到的是正常 `81 /7 imm32`（`cmp edx,imm32`）。

## 为什么不在 `4cc_table.json`

`4cc_table.json` 是 t07 的**窄读/窄写候选证据表**，不是扫描到的所有 cmp immediate 的清单。t07 的扫描/指令边界确认阶段能识别这种常规 immediate；但候选生成阶段要求找到 1/2/4 字节对象成员访问。Sold/Salt 的 getter 分支先取 qword 成员 wrapper（偏移 `+0x20`、`+0x48`），后续通过间接调用处理；该路径没有被窄访问提取器记录为对应的 4-byte 字段访问。因此它们虽有有效 4CC 比较，却没有窄访问证据条目，最终被 `4cc_table.codes` 的证据过滤遗漏。

**漏因分类：扫描后候选证据过滤（qword/间接 wrapper 路径），不是 4CC immediate 编码覆盖缺失。** 这也解释了为何检查 `41 81 F8`、`83 /7`、寄存器间接 cmp 或 perfect-hash/switch 不是这两个码的必要路径；本地链上的标准 cmp 与直接条件边已经提供反证。

## Snew 错实例纠正

t07 全局候选把 `Snew` 记录为 `object_off=166`（cmp 记录在 `file_off=0x11860aa`），但 t08 在 t22 局部 dispatch 链重新解码到：

- getter cmp：`file_off=0x153905b`，`81 fa 77 65 6e 53`，`cmp edx,0x536e6577`；目标 `0x141539e87` 首先取 `mov rcx,qword ptr [rbx+0x28]`（`+40`）；
- setter cmp：`file_off=0x153869b`，目标块访问 `[rsi+0x28]`（`+40`），同样是 qword wrapper。

这证实 `166` 是错实例，链内找到的是 `+40` 路径；但访问宽度是 8，而 reader 槽是 `(40,4)`。按任务要求的精确 `(off,width)` 配对，t08 不把它提升成 `chain_unique` 字段名。对 Sold/Salt 也同理：不把 qword wrapper 冒充成 reader 的 4-byte 字段访问。t05 的字段名只在报告阶段做事后交叉校验，未参与生成。

## 受影响数量上界

t07 表内统计为 8,399 个经指令验证的不同 4CC cmp code，1,477 个 code 有窄访问或 ref-only 证据。因此，当前全局表中没有证据条目的 code 值上界是：

`8,399 - 1,477 = 6,922`

其中至少 2 个（Sold、Salt）已证实是 qword/间接 wrapper 路径；6,922 是“可能缺失/无候选证据的 code 值”的保守上界，不是 6,922 个有效业务字段的断言。其余还可能是非字段比较、不可达代码、没有对象访问的分支或其他提取器不覆盖的形式。单凭全局计数不能把 qword-wrapper 这一子类精确计数。
