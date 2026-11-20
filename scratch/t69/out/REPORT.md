# t69｜t57/t59 skipped / static-untriggered 尾账审计

本轮 **L2**：已交付台账交叉引用，加双档 COMP 四处定点原字节复核。仅在 `scratch/t69/out/` 落盘；未重新找槽、重跑行框 DP、复判枚举、追 PE/IDA 或重做任何普查。没有启动游戏/编辑器/IDA、联网或读写 `Z:`。**新增 L3=0，L4=0**；下文的旧 L3 只按原适用范围引用。

## 1. Club：十个跳过项逐项对账

`t57 = scratch/t57/out/field_map.json`；`S8 = scratch/t60/out/club_nation_subtable_schema.v8.json`；`S9 = reports/club_nation_subtable_schema.json`。`#` 后为零基 JSON Pointer。已实比 S8/S9 的整个 `/tables`、`/club_auxiliary_sources`，两者逐值相等；分别提供条目级承接和一条已接受的子项见证。

| t57 跳过 occurrence | 承接成员 / server 行数 | S8/S9 承接条目及见证 | 已承接任务 |
|---|---|---|---|
| `CNtp` `/fields/45` | `table_66.dat`，753 | `/tables/4`；`/tables/4/fields/0` `nati` | t34 |
| `CSrs` `/fields/83` | `table_62.dat`，37,214 | `/tables/2`；`/tables/2/fields/0` `Ttyp` | t31 |
| `Cstc` `/fields/84` | `table_22.dat`，449 | `/tables/0`；`/tables/0/fields/0` `Slea` | t27 |
| `Csme` `/fields/105` | `table_59.dat`，9,079 | `/tables/7`；`/tables/7/fields/0` `Melf`，有项才存在 | t41 / E82 |
| `Cdbt` `/fields/117` | `table_33.dat`，32,409 | `/tables/5`；`/tables/5/fields/0` `cash` | t36 |
| `Cmti` `/fields/122` | `table_43.dat`，535 | `/tables/3`；`/tables/3/fields/0` `play` | t32 |
| `Cafl` `/fields/209` | `server_db/club_links.dat`，9,261（视图 0） | `/club_auxiliary_sources/0/views/0`；其 `/occurrences/0` `affl` | t44 / E84；t48 / E88 折入 |
| `Cvfl` `/fields/210` | **同一个** `server_db/club_links.dat`，9,261（视图 1） | `/club_auxiliary_sources/0/views/1`；其 `/occurrences/0` `affl` | t44 / E84；t48 / E88 折入 |
| `Clhs` `/fields/329` | `table_37.dat`，465,712 | `/tables/1`；`/tables/1/fields/0` `divi` | t30 |
| `Tchl` `/fields/331` | `table_34.dat`，7,115 | `/tables/6`；`/tables/6/fields/0` `tchc` | t39 / E78 |

**10/10 承接，0 悬案。** 8 个编号成员的 server 封口取各条 `/server_payload/closure_formula`；上述编号成员中只有 `Cstc` 的 `client_observation.present=true`。封口不等于全部子项已命名或升级。`Tchl` 是共享 helper；7,084 个非空 owner 全指 t24 selector 11 `NATIONAL_TEAM`，另 31 个 null（S9 `/tables/6/supplemental_evidence/shared_dispatch_and_owner_scope`）。`Csme` 的 owner 指 t24（selector 10/11：8,941 / 138），不算 club 独占（S9 `/tables/7/owner_scope`）。

`CLUB_LINK` 只有一个 server 来源，`12 + 9261×47 + 0 = 435279`；client 无成员，无数字 `table_type`。t44 `fields_cafl_cvfl.json#/occurrences/Cafl/0`、`/occurrences/Cvfl/0` 对照相同 `affl` wire 字段的两个 occurrence；两视图各自的 held/运行期条目不升级。t57 的 `+0x118/+0x120` 是对象 vector，不是 t3 wire 槽。

**t68 已交付**：`crosswalk.json#/claims/3` 复核 t57 selector/template；`/scope` 明确只读 t3、不读 `CLUB_LINK`。它支撑主行边界，不是独立成员承接证据。t57 强制 13 B identity 且 marker=0 在 ordinal 69705 的反例，仍见 t68 `sensitivity.json#/sensitivity_notes/identity_13`；不复算，也不把替代 lookahead 写作原生布局。

## 2. COMP：静态可选边与双档实字节

静态摘自 t59 已交付分片；原二进制为 `D:/tmp2b/fm24/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。地址栏为 **PE file offset**，各条 VA 和原指令字节保留在 ledger `comp_static_predicates`；未重新打开二进制。

| 闸门 | 谓词及分支 | 确切出处（t59 `out/`） |
|---|---|---|
| 外层 mode | `0xeb739d test r13b,r13b`；`0xeb73a0 je`。0 → `0xeb7a21`，跳过整个扩展；非 0 → `0xeb73a6`。 | `branches.part01.json#/30`；`instructions.part01.json#/445`、`/446`。 |
| `+0xa8` | `0xeb7532` 读 1 B；在成功读分支上 `0xeb753f cmp byte ptr [rsp+0x5f],0`，`0xeb7544 je`。0 → `0xeb75d7`；非 0 → `0xeb754a`，后续 payload call `0xeb75ca → 0x9f9ab0`。 | `branches.part01.json#/43`；`instructions.part01.json#/539`、`/542`、`/543`、`/563`。 |
| `+0xe0` | `0xeb76c0` 读 1 B；在成功读分支上 `0xeb76cd cmp byte ptr [rsp+0x5e],0`，`0xeb76d2 je`。0 → `0xeb770b`；非 0 → `0xeb76d4`，后续 payload call `0xeb76fb → 0x838a80`。 | `branches.part01.json#/54`；`instructions.part02.json#/21`、`/24`、`/25`、`/35`。 |

| 槽 / t59 `field_slots.json` | Client（7,047 行） | Server（7,047 行；`@` 是解压成员坐标） | 已交付 t66 `collections.json` 判定 |
|---|---|---|---|
| `+0xa8` `/slots/44` presence、`/45` payload | mode 跳过，0 次 presence 读取，0 payload | `{0:7047}`，首 row 0 `@133:00`，0 payload、无 payload 坐标 | `/collections/+0xa8` held；非零分支未见证 |
| `+0xe0` `/slots/51` presence、`/52` payload | mode 跳过，0 次 presence 读取，0 payload | `{0:7047}`，首 row 0 `@142:00`，0 payload、无 payload 坐标 | `/collections/+0xe0` held；非零分支未见证 |
| `vec30` `/slots/43` | mode 跳过，0 次 count 读取 | u32 `{0:7047}`，首 row 0 `@129:00000000`，0 item | `/collections/vec30` held：静态 `u32 N + 2N`，没有非空项 |
| `+0x100` `/slots/65` (`vec100`) | mode 跳过，0 次 count 或 item 读取 | i16 `{0:6918,1:62,2:56,3:9,5:1,6:1}`；首非空 row 47 `@17364:0100`，129 行非空，212×5 B | `/collections/+0x100` **旧 L3 仅物理文法**：`i16 N + N×(1+2+2)`，无 item tag；不命名业务字段或引用域 |

`+0x100` item 三个 wire lane 的完整 LE 无符号直方图见 ledger `entries` 对应 `data.server.item_histograms_unsigned_LE`。按 `item.+0/+1/+3` 分别为 0–9、0–2024、0–2023（范围，不代表所有整数都出现）；数值本身不证明业务含义。

**双档“全 0”的边界**：实档双侧均零触发，不是两侧都读到零。依 t50 §4/§6 区分档位跳过、读到零、无载荷及坐标证据不完整；不把 mode 0 的缺测写成 `{0:7047}`，不把未触发写成死边。t59/t66 的反 mode 原始反例保持：client `vec30: row 0 @129: invalid count 16777216`；server `row 0 @128: identity (255, 4294901760, 131071)`。

**复核方法**：只选两档 `table_25.dat`。TOC 用 `data_base + offset` 界定 member，按 declared size 选唯一帧，核对压缩/解压 SHA。沿 t66 已交付 `census.json#/sides/{client,server}/rows` 校验原字节 identity、边界与 t59 摘要；双档公共前 71 B（含 selector）与末 56 B 逐行同值。四处目标使用 t66 坐标直接读值，以 t59 模板、坐标/内容摘要及 t66 发布的直方图对照；不重跑 reader，不消费其他集合或展开其他归档成员。

## 3. Nation：引用 t61，不重新判定

`t61 已交付`。下列为其 `enum_inventory.json` 判词和已交付诊断；两档均各 251 行。保留 t55 首反例，不自拟哨兵或标签。

| 字段 | t55 → t61 条目 | t61 判定 / 诊断 |
|---|---|---|
| `Necf` | `/fields/26` → `/occurrences/6` | `held / no_enum_source`；冻结界 [1,20] 下每档 `0`×28。首 row 121：client `@8628:00` / server `@99394:00`。 |
| `Nygn` | `/fields/28` → `/occurrences/7` | `held / no_enum_source`；冻结界 [0,100] 下每档 `-1`×26。首 row 29：client `@2102:ff` / server `@17005:ff`。 |
| `Ngct` | `/fields/32` → `/occurrences/8` | `held / no_enum_source`；每档 `{1:122,2:129}`。现有 getter 不补足枚举来源。 |
| `Nsod` | `/fields/33` → `/occurrences/9` | `held / no_enum_source`；每档 `{0:21,1:54,2:100,3:76}`。现有 getter 不补足枚举来源。 |

此处“四项”只指 t61 的 nation `main` 四条已定位记录；不并入 `EDsc` 等 `main_other`，也不把 t57/t59 的其他 held 列重抄进本任务。

## 4. 折叠与验收

[SUMMARY.md](SUMMARY.md) 是三表晨报总表；[tail_ledger.json](tail_ledger.json) 逐项提供 `id/table/kind/evidence_refs/grade/承接`。L2 表示本轮交叉核验，`held` 原样保留，旧 L3 只在原作用域引用。不折叠 COMP 三条无 live 见证的开放边，不把 `+0x100` 物理文法折成业务名；这些未决事项未获后续任务号，不写成承诺。

```bash
export FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data
py -V:3.12 -I -B scratch/t69/out/verify.py --help
py -V:3.12 -I -B scratch/t69/out/verify.py --selftest
py -V:3.12 -I -B scratch/t69/out/verify.py --check
```

退出码：0 通过，1 证据/台账不一致，2 用法或致命错误。`--selftest` 不读档；`--check` 对当前已交付的 v8/v9 与 t61/t66/t68 产物及两档原字节复验，不运行上游 verifier。
