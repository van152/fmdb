# t108 — Hex-Rays 4CC ↔ 内存偏移 v2（helper 内联 + Cnti 修复 + 1,034 分母闭环）

> 只读输入：`scratch/t95/vtable_index.json`、`scratch/t95/funcs/*.c`（1,173 份 Hex-Rays C，
> 含 t107 补反编译的 500+ helper）、`scratch/t107/out/helpers_index.json`、
> `scratch/t97/out/*`（基线）、`reports/xml_denominator_coverage.json`、
> `reports/club_nation_subtable_schema.json`。
> **本任务不修改 `reports/`、`LEDGER.json`、`scripts/t97_extract_4cc_mem.py`。**

## 0. 交付物

| 文件 | 内容 |
|---|---|
| `fourcc_mem_map_v2.json` | 67 张表的 v2 映射（`helper_chain` 溯源 + 精确 C 行号） |
| `xml_triage_v2.json` | 1,034 条分母 v2 分诊 + `t97 -> t108` 提升对比矩阵 |
| `static_read_join_v2.json` | 4CC ↔ `mem_off` ↔ slot19/slot20 交叉表（含 delta） |
| `REPORT.md` / `DONE.md` | 本报告 / 完成标记（`DONE type=t108b`） |

## 1. t97 → t108 总览

| 指标 | t97 | t108 | 变化 |
|---|---|---|---|
| 表×4CC 分支记录 | 6219 | 8046 | +1827 |
| 有 `this`/子对象字节偏移 | 1808 | 3720 | +1912 |
| `direct_field` | 1255 | 1836 | +581 |
| `bitfield` | 125 | 84 | -41 |
| `subobj_deref` | 89 | 441 | +352 |
| `resolved_via_helper` | 0 | 2084 | +2084 |
| `helper_computed` | 2525 | 956 | -1569 |
| `delegated_or_empty` | 2225 | 1798 | -427 |
| `confirmed_computed_or_ui` | 0 | 847 | +847 |
| 子表 handler 内定位（`offset_space=child_table`） | 0 | 725 | +725 |
| slot19/slot20 交叉命中（至少一侧） | 802 | 1471 | +669 |

解析器（helper 追踪）内部计数：

```
arg0_not_this                    2728
member_resolved                  1517
dispatch_resolved                805
file_missing                     367
computed_vtable_dispatch_through_global 81
hop2_dead                        33
hop2_resolved                    5
computed_constant_or_arith_only  4
```

回填（`attach_v2_extras`）：12010/12010 个候选（含 `alt`）已挂上 v2 字段，其中 `offset_space=child_table` 798 个、带 `helper_chain` 2248 个。

## 2. helper_computed 的处置

t97 遗留 `helper_computed` **2525** 条，t108 后剩 **956** 条；新增 `resolved_via_helper` **2084** 条、`confirmed_computed_or_ui` **847** 条。

三类判定的判据（全部静态、可复现）：

1. **`resolved_via_helper`（偏移落地）**：helper 的 arg0 就是 `this`（或 `this` 别名、
   `this + K` 内部指针），且 helper 体内对 `arg0 + K` 有真实读/写 → 把 `K` 提升为字段偏移；
   若传入的是 `*(this + K)`（子对象指针），则记录二级偏移 `0xK -> 0xM`。
2. **`offset_space=child_table`（次级分派器）**：helper 把 4CC 字面量/分派码转发给另一个函数，
   而那个函数本身是某张表的 `slot02/slot03` handler → 在该 handler 内定位该 4CC 的精确 `mem_off`，
   `helper_chain` 记录完整链路（例：`CLUB CBDa → sub_1411E9540(type=9) → STARTING_RECORD::set_prop('otht') → +0x28`）。
3. **`confirmed_computed_or_ui`（明确非持久化字段）**：helper 只碰全局/注册表/out-param/纯算术，
   不读写对象自身字段。`computed_reason` 给出理由（`global_or_registry_lookup` /
   `arg0_is_out_param_local_or_global` / `constant_or_arith_only` / `vtable_dispatch_through_global`）。

### 2.1 高频 helper 的处置结果

| helper VA | 出现分支数（t97） | t108 判定 | 说明 |
|---|---|---|---|
| `0x1411e9540` | 644 | `child_table` | 按 (obj_id, type) 查注册表 → `STARTING_RECORD::set_prop(code)` |
| `0x1407c9510` | 366 | `computed` | `a1[0..2] = 0`：out-param 构造，arg0 非 `this` |
| `0x140fe2700` | 359 | `protocol` | 共享对象协议 handler（`BaCP/COPY/DELE`），无字段语义 |
| `0x1411f4bd0` | 141 | `computed` | 内置 vector 扫描 + vtable `+16` 转发，值在子对象 |
| `0x143ca2e60` | 73 | `child_table` | 同 `0x1411E9540`，转发给 `STARTING_RECORD::get_prop` |
| `0x140fead00` | 120 | `computed` | variant 组装（`sub_14083D4F0(...)+40` 粘合） |
| `0x140e75ff0` | 60 | `computed` | 内置 vector 扫描（`this+280/288`）返回子对象指针 |
| `0x140e63b10` | 5 | `resolved` | 读 `this+72/80` 的 16 字节记录数组，匹配 tag/字段 |
| `0x140e759f0` | 5 | `resolved` | 同上（`this+72/80`），递归取 vtable 结果 |

## 3. `Cnti` 回归修复（`mismatch == 0`）

CLUB `slot03_set_prop`（`funcs/140e834a0.c`，分支 2028–2067 行）同一分支里既写外层子对象指针
`*(_QWORD *)(a1 + 216)`，也在条件里读附属标志字节 `*(_BYTE *)(a1 + 185)`：

```c
2033  v32 = *(_QWORD *)(a1 + 216);            // 外层：子对象指针（写入前先读旧值）
2042  if ( *(_BYTE *)(a1 + 185) != 0 )          // 内层：附属标志（仅条件判断）
2065  *(_QWORD *)(a1 + 216) = v200;             // 真正的写入目标
```

t97 按「分支内最小偏移」取 185 → `mismatch`。t108 给每个偏移标注**角色**
（`test` = 条件表达式内、`write` = `=` 左侧、`read` = 其它），并让**外层子对象指针**
优先于**仅出现在条件里的附属标量**，因此 `Cnti → 0xd8 = 216`，与已验收 L3 一致。

角色标注同时让 `Cedp`/`Cncl` 从 `no_static_hit` 变为可定位：它们的 helper
（`sub_140E63B10` / `sub_140E759F0`）直接读 `this + 72` / `this + 80`（内嵌记录数组），
内联后给出 `+0x48`，正落在已验收位移 72 上。

**回归结果：checked=18 / exact=15 / within_slot=3 / no_static_hit=0 / mismatch=0**

| section | code | 已验收 disp | 宽度 | t108 off | kind | offset_space | 判定 |
|---|---|---|---|---|---|---|---|
| club | `duni` | 8 | 12 | 12 | `direct_field` | this | within_slot |
| club | `Cext` | 216 | 4 | 216 | `subobj_deref` | this | exact |
| club | `Cedp` | 72 | 1 | 72 | `resolved_via_helper` | this | exact |
| club | `Cnti` | 216 | 4 | 216 | `subobj_deref` | this | exact |
| club | `Cbni` | 232 | 4 | 232 | `direct_field` | this | exact |
| club | `Cccn` | 240 | 4 | 240 | `direct_field` | this | exact |
| club | `Cncl` | 72 | 1 | 72 | `resolved_via_helper` | this | exact |
| club | `Ccty` | 248 | 4 | 248 | `direct_field` | this | exact |
| club | `CIns` | 352 | 6 | 352 | `subobj_deref` | this | exact |
| club | `CASt` | 352 | 6 | 353 | `subobj_deref` | this | within_slot |
| club | `Csot` | 352 | 6 | 352 | `direct_field` | this | exact |
| club | `Ctsi` | 320 | 4 | 320 | `direct_field` | this | exact |
| club | `CnCV` | 352 | 6 | 355 | `subobj_deref` | this | within_slot |
| nation | `Nnsi` | 280 | None | 280 | `direct_field` | this | exact |
| nation | `Ncti` | 240 | None | 240 | `direct_field` | this | exact |
| nation | `Nrgi` | 248 | None | 248 | `direct_field` | this | exact |
| nation | `Ncur` | 256 | None | 256 | `direct_field` | this | exact |
| nation | `Nndn` | 456 | None | 456 | `direct_field` | this | exact |

## 4. 新解锁的核心字段（CLUB / COMP / NATION）

### CLUB（tt=3）：`resolved_via_helper` 305 条

| 4CC | 槽 | 偏移 | offset_space | helper 链 | 证据行 |
|---|---|---|---|---|---|
| `1sbc` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2814` |
| `1scl` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2828` |
| `1tbc` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2840` |
| `1tcl` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2881` |
| `2sbc` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2732` |
| `2scl` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2700` |
| `2tbc` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2714` |
| `2tcl` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2760` |
| `3sbc` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2908` |
| `3scl` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2932` |
| `3tbc` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2967` |
| `3tcl` | `slot02_get_prop` | `0x118` | `this` | `0x140e75ff0` | `funcs/140e8a400.c:2982` |
| `C2hs` | `slot02_get_prop` | `0x18` | `this` | `0x140e69670` | `funcs/140e8a400.c:3247` |
| `C2na` | `slot02_get_prop` | `0x18` | `this` | `0x140e98410` | `funcs/140e8a400.c:3198` |
| `C2nd` | `slot02_get_prop` | `0x18` | `this` | `0x1411f4bd0` | `funcs/140e8a400.c:3219` |
| `C2nm` | `slot02_get_prop` | `0x18` | `this` | `0x1411f4bd0` | `funcs/140e8a400.c:3223` |
| `C2nt` | `slot02_get_prop` | `0x18` | `this` | `0x1411f4bd0` | `funcs/140e8a400.c:3227` |
| `C2od` | `slot02_get_prop` | `0x18` | `this` | `0x1411f4bd0` | `funcs/140e8a400.c:3290` |
| `C2sj` | `slot03_set_prop` | `0x18` | `this` | `0x1411f4f70` | `funcs/140e834a0.c:1255` |
| `C2sk` | `slot03_set_prop` | `0x18` | `this` | `0x1411f4f70` | `funcs/140e834a0.c:1256` |
| `C2sl` | `slot03_set_prop` | `0x18` | `this` | `0x1411f4f70` | `funcs/140e834a0.c:1257` |
| `C2sm` | `slot03_set_prop` | `0x18` | `this` | `0x1411f4f70` | `funcs/140e834a0.c:1258` |
| `C2sn` | `slot02_get_prop` | `0x18` | `this` | `0x1411f4bd0` | `funcs/140e8a400.c:3127` |
| `C2so` | `slot03_set_prop` | `0x18` | `this` | `0x1411f4f70` | `funcs/140e834a0.c:1259` |

### COMP（tt=25）：`resolved_via_helper` 202 条

| 4CC | 槽 | 偏移 | offset_space | helper 链 | 证据行 |
|---|---|---|---|---|---|
| `Accl` | `slot02_get_prop` | `0x60` | `this` | `0x140ebc8f0` | `funcs/140ec0a60.c:936` |
| `CBWa` | `slot02_get_prop` | `0x58` | `child_table` | `0x143ca2e60` → `0x1415446a0`(ogls) | `funcs/140ec0a60.c:883` |
| `CBWb` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:888` |
| `CBWd` | `slot02_get_prop` | `0x40` | `child_table` | `0x143ca2e60` → `0x1415446a0`(stdt) | `funcs/140ec0a60.c:903` |
| `CBWe` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:889` |
| `CBWf` | `slot02_get_prop` | `0x56` | `child_table` | `0x143ca2e60` → `0x1415446a0`(gols) | `funcs/140ec0a60.c:908` |
| `CBWg` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:890` |
| `CBWh` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:891` |
| `CBWi` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:892` |
| `CBWj` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:893` |
| `CBWk` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:894` |
| `CBWl` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:895` |
| `CBWm` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:896` |
| `CBWn` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:897` |
| `CBWo` | `slot02_get_prop` | `0x28` | `child_table` | `0x143ca2e60` → `0x1415446a0`(otht) | `funcs/140ec0a60.c:913` |
| `CFGd` | `slot02_get_prop` | `0x40` | `child_table` | `0x143ca2e60` → `0x1415446a0`(stdt) | `funcs/140ec0a60.c:773` |
| `CFGe` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:778` |
| `CFGf` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:779` |
| `CFGg` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:780` |
| `CFGh` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:781` |
| `CFGi` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:782` |
| `CFGj` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:783` |
| `CFGk` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:784` |
| `CFGl` | `slot02_get_prop` | `0x8` | `this` | `0x140fe3f20` | `funcs/140ec0a60.c:785` |

### NATION（tt=10）：`resolved_via_helper` 132 条

| 4CC | 槽 | 偏移 | offset_space | helper 链 | 证据行 |
|---|---|---|---|---|---|
| `AwLi` | `slot02_get_prop` | `0xc` | `this` | `0x1411f1090` | `funcs/1410668f0.c:879` |
| `CBDa` | `slot03_set_prop` | `0x58` | `child_table` | `0x1411e9540` → `0x141545680`(ogls) | `funcs/1411f4f70.c:281` |
| `CBDb` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:285` |
| `CBDc` | `slot03_set_prop` | `0x30` | `child_table` | `0x1411e9540` → `0x141545680`(comp) | `funcs/1411f4f70.c:296` |
| `CBDd` | `slot03_set_prop` | `0x40` | `child_table` | `0x1411e9540` → `0x141545680`(stdt) | `funcs/1411f4f70.c:300` |
| `CBDe` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:286` |
| `CBDf` | `slot03_set_prop` | `0x56` | `child_table` | `0x1411e9540` → `0x141545680`(gols) | `funcs/1411f4f70.c:304` |
| `CBDg` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:287` |
| `CBDh` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:288` |
| `CBDi` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:289` |
| `CBDj` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:290` |
| `CBDk` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:291` |
| `CBDl` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:292` |
| `CBDm` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:293` |
| `CBDn` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:294` |
| `CBWa` | `slot03_set_prop` | `0x58` | `child_table` | `0x1411e9540` → `0x141545680`(ogls) | `funcs/1411f4f70.c:314` |
| `CBWb` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:318` |
| `CBWc` | `slot03_set_prop` | `0x30` | `child_table` | `0x1411e9540` → `0x141545680`(comp) | `funcs/1411f4f70.c:329` |
| `CBWd` | `slot03_set_prop` | `0x40` | `child_table` | `0x1411e9540` → `0x141545680`(stdt) | `funcs/1411f4f70.c:333` |
| `CBWe` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:319` |
| `CBWf` | `slot03_set_prop` | `0x56` | `child_table` | `0x1411e9540` → `0x141545680`(gols) | `funcs/1411f4f70.c:337` |
| `CBWg` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:320` |
| `CBWh` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:321` |
| `CBWi` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:322` |

### TEAM_CONTAINER（tt=3）：`resolved_via_helper` 108 条

| 4CC | 槽 | 偏移 | offset_space | helper 链 | 证据行 |
|---|---|---|---|---|---|
| `CBDa` | `slot03_set_prop` | `0x58` | `child_table` | `0x1411e9540` → `0x141545680`(ogls) | `funcs/1411f4f70.c:281` |
| `CBDb` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:285` |
| `CBDc` | `slot03_set_prop` | `0x30` | `child_table` | `0x1411e9540` → `0x141545680`(comp) | `funcs/1411f4f70.c:296` |
| `CBDd` | `slot03_set_prop` | `0x40` | `child_table` | `0x1411e9540` → `0x141545680`(stdt) | `funcs/1411f4f70.c:300` |
| `CBDe` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:286` |
| `CBDf` | `slot03_set_prop` | `0x56` | `child_table` | `0x1411e9540` → `0x141545680`(gols) | `funcs/1411f4f70.c:304` |
| `CBDg` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:287` |
| `CBDh` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:288` |
| `CBDi` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:289` |
| `CBDj` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:290` |
| `CBDk` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:291` |
| `CBDl` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:292` |
| `CBDm` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:293` |
| `CBDn` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:294` |
| `CBWa` | `slot03_set_prop` | `0x58` | `child_table` | `0x1411e9540` → `0x141545680`(ogls) | `funcs/1411f4f70.c:314` |
| `CBWb` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:318` |
| `CBWc` | `slot03_set_prop` | `0x30` | `child_table` | `0x1411e9540` → `0x141545680`(comp) | `funcs/1411f4f70.c:329` |
| `CBWd` | `slot03_set_prop` | `0x40` | `child_table` | `0x1411e9540` → `0x141545680`(stdt) | `funcs/1411f4f70.c:333` |
| `CBWe` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:319` |
| `CBWf` | `slot03_set_prop` | `0x56` | `child_table` | `0x1411e9540` → `0x141545680`(gols) | `funcs/1411f4f70.c:337` |
| `CBWg` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:320` |
| `CBWh` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:321` |
| `CBWi` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:322` |
| `CBWj` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:323` |

### NATIONAL_TEAM_CONTAINER（tt=9）：`resolved_via_helper` 132 条

| 4CC | 槽 | 偏移 | offset_space | helper 链 | 证据行 |
|---|---|---|---|---|---|
| `AwLi` | `slot02_get_prop` | `0xc` | `this` | `0x1411f1090` | `funcs/1410668f0.c:879` |
| `CBDa` | `slot03_set_prop` | `0x58` | `child_table` | `0x1411e9540` → `0x141545680`(ogls) | `funcs/1411f4f70.c:281` |
| `CBDb` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:285` |
| `CBDc` | `slot03_set_prop` | `0x30` | `child_table` | `0x1411e9540` → `0x141545680`(comp) | `funcs/1411f4f70.c:296` |
| `CBDd` | `slot03_set_prop` | `0x40` | `child_table` | `0x1411e9540` → `0x141545680`(stdt) | `funcs/1411f4f70.c:300` |
| `CBDe` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:286` |
| `CBDf` | `slot03_set_prop` | `0x56` | `child_table` | `0x1411e9540` → `0x141545680`(gols) | `funcs/1411f4f70.c:304` |
| `CBDg` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:287` |
| `CBDh` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:288` |
| `CBDi` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:289` |
| `CBDj` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:290` |
| `CBDk` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:291` |
| `CBDl` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:292` |
| `CBDm` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:293` |
| `CBDn` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:294` |
| `CBWa` | `slot03_set_prop` | `0x58` | `child_table` | `0x1411e9540` → `0x141545680`(ogls) | `funcs/1411f4f70.c:314` |
| `CBWb` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:318` |
| `CBWc` | `slot03_set_prop` | `0x30` | `child_table` | `0x1411e9540` → `0x141545680`(comp) | `funcs/1411f4f70.c:329` |
| `CBWd` | `slot03_set_prop` | `0x40` | `child_table` | `0x1411e9540` → `0x141545680`(stdt) | `funcs/1411f4f70.c:333` |
| `CBWe` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:319` |
| `CBWf` | `slot03_set_prop` | `0x56` | `child_table` | `0x1411e9540` → `0x141545680`(gols) | `funcs/1411f4f70.c:337` |
| `CBWg` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:320` |
| `CBWh` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:321` |
| `CBWi` | `slot03_set_prop` | `0x8` | `this` | `0x140fe2700` | `funcs/1411f4f70.c:322` |

## 5. 1,034 分母 v2 分诊

分母 **1034** 条（club 433 / nation 346 / comp 255）。

| 原桶 | 总数 | t108: 直接 mem_off | helper 内联(this) | helper 内联(子对象) | 子表 handler | subobj_deref | 仍 helper_computed | 全 67 表皆无 |
|---|---|---|---|---|---|---|---|---|
| `held` | 59 | 29 | 6 | 0 | 0 | 3 | 4 | 1 |
| `independent_member` | 11 | 2 | 0 | 0 | 0 | 1 | 1 | 0 |
| `mapped_l3` | 99 | 41 | 2 | 0 | 0 | 11 | 0 | 33 |
| `no_wire_evidence` | 564 | 53 | 1 | 0 | 147 | 0 | 55 | 260 |
| `re_routed_table_45` | 117 | 0 | 0 | 0 | 91 | 0 | 26 | 0 |
| `ui_or_derived` | 24 | 0 | 0 | 0 | 0 | 0 | 1 | 10 |
| `unresolved_wire_slot` | 160 | 51 | 18 | 0 | 1 | 5 | 28 | 8 |

### 5.1 三个关键桶的 t97 → t108 变化

| 桶 | 总数 | t97 直接 mem_off | t108 直接 mem_off | t97 helper_computed | t108 helper_computed | t97→t108 新落地偏移 |
|---|---|---|---|---|---|---|
| `unresolved_wire_slot` | 160 | 41 | 51 | 85 | 28 | 26 |
| `held` | 59 | 24 | 29 | 20 | 4 | 6 |
| `no_wire_evidence` | 564 | 46 | 53 | 217 | 55 | 5 |

分母行级别的 `access_kind` 迁移（t97 -> t108，仅列变化）：

| 迁移 | 行数 |
|---|---|
| `helper_computed->resolved_via_helper` | 266 |
| `helper_computed->confirmed_computed_or_ui` | 58 |
| `helper_computed->direct_field` | 26 |
| `bitfield->subobj_deref` | 6 |
| `delegated_or_empty->direct_field` | 6 |
| `none->confirmed_computed_or_ui` | 6 |
| `delegated_or_empty->confirmed_computed_or_ui` | 5 |
| `direct_field->subobj_deref` | 4 |
| `subobj_deref->direct_field` | 3 |
| `none->direct_field` | 1 |
| `none->helper_computed` | 1 |

全表 6,000+ 表×4CC 分支的 `access_kind` 迁移（仅列前 12）：

| 迁移 | 条数 |
|---|---|
| `helper_computed->resolved_via_helper` | 872 |
| `delegated_or_empty->resolved_via_helper` | 675 |
| `helper_computed->confirmed_computed_or_ui` | 602 |
| `absent_then->resolved_via_helper` | 537 |
| `helper_computed->direct_field` | 371 |
| `absent_then->direct_field` | 333 |
| `absent_then->delegated_or_empty` | 310 |
| `absent_then->helper_computed` | 270 |
| `absent_then->confirmed_computed_or_ui` | 217 |
| `direct_field->subobj_deref` | 165 |
| `absent_then->subobj_deref` | 137 |
| `bitfield->subobj_deref` | 64 |

### 5.2 分实体

| entity | 直接 mem_off | helper(this) | helper(子对象) | 子表 handler | subobj_deref | 仍 helper_computed | 全表皆无 |
|---|---|---|---|---|---|---|---|
| club | 76 | 26 | 0 | 91 | 15 | 47 | 115 |
| comp | 28 | 0 | 0 | 73 | 4 | 38 | 78 |
| nation | 72 | 1 | 0 | 75 | 1 | 30 | 119 |

## 6. slot19/slot20 静态交叉（802 → 1471）

- slot02/03 有 `this` 相对偏移的分支：**3720**（t97: 1808, +1912）
- 与 `slot19_read_server` 偏移集合相交：**1285**（t97: 724, +561）
- 与 `slot20_read_client` 偏移集合相交：**482**（t97: 250, +232）
- 至少命中一侧：**1471**（t97: 802, +669）

| tt | class | 有 off | slot19 命中 | slot20 命中 | 至少一侧 |
|---|---|---|---|---|---|
| 3 | LEAGUE_BODY_CLUB | 394 | 250 | 2 | 252 |
| 21 | STADIUM | 294 | 152 | 13 | 152 |
| 24 | TEAM | 576 | 49 | 113 | 141 |
| 27 | WEATHER | 90 | 90 | 0 | 90 |
| 9 | NATIONAL_TEAM_CONTAINER | 184 | 69 | 28 | 72 |
| 24 | NATIONAL_TEAM | 576 | 18 | 52 | 70 |
| 3 | TEAM_CONTAINER | 80 | 61 | 59 | 61 |
| 9 | TEAM_CONTAINER | 80 | 61 | 59 | 61 |
| 12 | STARTING_AWARD_HISTORY | 53 | 53 | 6 | 53 |
| 0 | AWARD | 48 | 43 | 5 | 43 |
| 10 | NATION | 184 | 13 | 30 | 40 |
| 25 | COMP | 170 | 38 | 8 | 38 |
| 1 | BASIC_PERSON | 54 | 37 | 11 | 37 |
| 18 | DERBY | 35 | 35 | 9 | 35 |
| 3 | CLUB | 394 | 29 | 8 | 29 |

## 7. 方法与已知限制

1. **分支定位与字节换算**沿用 t97（`case`/`if`/guard 三型；按 base 变量声明元素宽度换算；
   `this` 别名做逐行 reaching-definition 判定）。
2. **新增角色标注**：每个偏移出现点被标为 `test`（if/while 条件内）、`write`（`=` 左侧）或 `read`；
   选择 `primary_off` 时先排除「只在条件里出现」的偏移，再让子对象指针优先于内层标量。
3. **helper 内联**最多 2 跳，仅当分支自身没有直接偏移、且 helper 的 arg0 是 `this`/`this` 派生时
   才把 helper 内的 `arg0 + K` 作为该 4CC 的偏移；arg0 是 out-param / 局部变量 / 全局的一律不内联。
4. **`child_table` 偏移不与 `this` 偏移混用**：`offset_space` 显式区分，
   交叉表与 L3 回归只使用 `this` / 子对象相对偏移，避免把子表字段当成 `this` 字段。
5. **置信度**：仍无法定位的分支保留 `helper_computed`（helper 无反编译文件），
   或以 `confirmed_computed_or_ui` + `computed_reason` 明确标注为全局/注册表/out-param/纯算术。

## 8. 复现

```
py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --selftest   # 断言含 Cnti==216、18/18 mismatch==0
py -V:3.12 -I -B scripts/t108_extract_4cc_v2.py --run        # 写 5 个交付物到 scratch/t108/out
```

