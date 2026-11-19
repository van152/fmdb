# t61 — Held 字段 scoped `enum_ref` 批量复核

**73 条 held 台账记录全部保持 held；新增 L3=0，L4=0。** 开工时公共 schema 为 v8/E98；交付前 t60 已生成 **v9**，以 `reports/` 实际 v9 重建、独立复验（SHA-256 `8a3d959597dbd3477c819e73902fd5612b6f3bbe25668087211d15ddeec05d25`）。v9 的 10 条 COMP held 与 E99/t59 原记录逐条一致。冻结 `master.json` SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`，与 `evidence/MANIFEST.json` 匹配。

| 侧 | 层 | 核对 | `no_enum_source` | 有定义、无 wire 样本 | 枚举冲突 | 新 L3 |
|---|---|---:|---:|---:|---:|---:|
| nation | table_10 主行，已定位的 4 项 | 4 | 4 | 0 | 0 | 0 |
| nation | 主行补充：`Nftb` 父、`EDsc`、无活动 XML 的 `Npop` | 3 | 3 | 0 | 0 | 0 |
| nation | 子项层（含 `TCrs` 的两份物理向量） | 24 | 20 | 3 | 1 | 0 |
| club | table_3 主行 | 11 | 11 | 0 | 0 | 0 |
| club | 编号子表（不含共享 `Tchl`） | 14 | 14 | 0 | 0 | 0 |
| club/nation 共享 | `Tchl`，按 v8 club 侧台账计一次；两个 XML 路径分别核过 | 2 | 2 | 0 | 0 | 0 |
| club | `CLUB_LINK` 辅助源（两视图 5 occurrence / 3 物理 lane） | 5 | 5 | 0 | 0 | 0 |
| comp | table_25 主行 | 10 | 8 | 1 | 1 | 0 |

## 有显式引用的 6 条 held

| Occurrence | 冻结定义 | 全档复核 |
|---|---|---|
| comp `dbty` | `cdbt`，39 个数值/标签对 | Client 跳过。Server 7,047 个 i8，严格原值枚举闸门 178 miss：`-1`×163、`30`×15。首原值 miss row 155 `@44057:ff`。t59 getter 抑制的 `-1` 另有既有证据，不将其改写为枚举项；排除这些 `-1`，仍有 15 个业务值越界，首 row 394 `@102218:1e`（原反例保留）。 |
| comp `VARt` | `VART`，1–5 | 两档各 7,047 行，但 t59 getter 进入规则/context，未证同一 COMP wire 槽，不能把其他整数列作为样本。 |
| nation `TCrs/PUnJ` | `ftjn`，32 个数值/标签对 | Client 两成员均跳过。Server 原生 t9：2,219 项、425 miss，首 row 1/item 7 `@1827:6400` (=100)。Server getter `table_extra_9.dat`：76 项、2 miss（`0` 与 `109`），首 row 129/item 5 `@55950:6d00` (=109)。即使另看既有 getter-missing `0`，`109` 仍冲突。两向量不混为一个槽。 |
| nation `NTRv/repu`、`NWGv/repu`、`NSps/repu` | `crrp`，20 个范围，`enum` 为 1、11、…、191，`enum_id` 为 0–19 | 三条 occurrence 均声明引用，但 getter 生成 UI 索引，无独立持久化字段；不可拿邻接的 `valu` 或 UI 索引补出 wire 直方图。 |

`EDfx/stadium_rules` 和 `EDsc/stadium_rules` 有字符串 token 型 `nstr`，在清单中单列为未列级的子项排除项，不计入 73 条：没有该子项的 held wire 记录，也不重啃 UI 路径。`Cafl/Cvfl.type` 的 `CAfT` 是既有同名对照，并非这两条 occurrence 的显式引用；继续保留旧 `21`×609（首 server row 12 `@580:15`），不把 CAfT 当成 scoped 来源。

## 无显式引用的重点

- **Nation**：`Ngct` 两档各 `{1:122, 2:129}`，`Nsod` 各 `{0:21, 1:54, 2:100, 3:76}`；精确 getter 不补足枚举出处。冻结整数界诊断原样复现：`Necf` 各 28 个 `0`（首 client/server row 121 `@8628:00` / `@99394:00`），`Nygn` 各 26 个 `-1`（首 row 29 `@2102:ff` / `@17005:ff`）。不自拟哨兵。
- **Club**：`Csti` 是可选 stadium 引用，不是显式枚举；无主行绑定，不拿 `Ctsi` 或 Liverpool 探针代填。`PLgn` 两档 84,259 个 `0`，无标签。`Csnm` 每档仍有 537 条超 25 Unicode code points；首 row 1428，client `@107960`、server `@859028`，长度 27。`CLat/CLon` 保留同对象反例；`Cyfn` 保留 `extra+0xd8` 证据，仅先例、非 t3 主行。
- **COMP**：`CTty` 两档各 7,047 个值，实际 0–11，首 client `@32:05`，无 scoped 引用。`PLgn` client 跳过，server 7,047 个 `0`（首 `@141:00`），仍无来源。`CpRp`、`rdui` 的原始画像不等于 getter 输出；`cnam/csnm/c3ln/HKEt` 不从邻近 bytes 补槽。

## 复跑与边界

每档先以 FMF 目录的 `data_base+offset` 限定成员，按声明尺寸唯一选帧。主行复用 t55/t57/t59 的全档游标和 slot/lane；子项复用已验条目/固定跨度。行号零基，绝对偏移相对于**解压后的成员**。`scanned`、档位跳过、无条目、成员缺失、未绑槽、person 边界分别标记；空直方图不是域通过。余留候选槽的直方图标为诊断，冻结 `min/max/max_length` 诊断与枚举判定分开。

独立 `verify.py` 自解两档目录，复用旧独立数据侧 replay（不 import builder、不做 PE/IDA 静态重追），逐 occurrence 重算直方图与首反例、复核枚举出处和晋级条件。`prior_first_counterexample` 保留原见证，`first_counterexample` 优先指向本轮枚举或冻结界首反例；原源台账、negative、公共 schema 与既有 L3 均未改。不读取 person 目标数据或 PDxx；不启动游戏、编辑器、IDA；不联网、不读写 Z:。

```bash
export FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data
py -V:3.12 -I -B scripts/t61_enum_ref_sweep.py --build
py -V:3.12 -I -B scratch/t61/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py
```

两脚本 `--help` / `--selftest` 支持；退出码 0 成功、1 检查未过、2 用法或致命错误。

## fix1

根因：t60 v9 构建/落账竞态使 t61 采样到中间态，且守卫错误钉了 `reports/` 全文件 SHA。
修复：守卫与 builder 改为仅钉 t61 实际引用的 E94/E97/E98/E99 的 `id`、`kind/level` 与 canonical claim SHA；旧全文件 SHA 仅作历史记录、不参与断言。
