# t38 — 多帧感知 payload 加载器

**任务书**:建独立加载器解 E66(`server table_34` 返回 12B 空 stub)。
**交付**:`scripts/t38_multiframe.py`(`load_payload_mf`)+ `scripts/t38_build.py` + `scratch/t38/out/*`。
**未改** `scripts/fm24_dump.py` 及其他既有脚本。

---

## 0. 结论摘要(先说结论)

| 项 | 结果 |
|---|---|
| 加载器落地 | `load_payload_mf(codec, archive, tid) -> bytes` ✅ |
| 五个锚点 | server34=313082 / client3=6932082 / server73=45 / server66=18094 / server43=24632 全中 ✅ |
| 单帧回归 | t33 七表 + t29 十三表 = 20 表，20/20 payload size+SHA 与已落盘证据一致 ✅ |
| `--selftest` | **25 PASS / 0 FAIL** |
| `out/verify.py` | **34/34 PASS**（独立复算，不 import 加载器） |
| `t01_anchors.py` | **7/7** |

### ⚠ 任务书前提需要修正（证据见 §3）

任务书与 E77 认为「成员含多帧：空 stub 首帧 + 真实 payload 第二帧」。**实测不是这样**：

* 三个归档 **460 个条目,全部是单帧成员**，首帧（也是唯一帧）解压长度恒等于 `entry["size"]`。
* `server table_34` 的真实成因是 **`load_payload` 少加 FMF `data_base`（=34）**，起点整体前移 34B，落进前一个成员的尾部；恰好前一成员是 25B 的 `tad.` 空 stub（解压 12B），于是「首帧」取到别人的 12B。
* 一旦前移后的窗口里扫到的首帧 MAGIC 属于**前一个成员**，就取到**别人的 payload**——不是「同一成员的 stub 帧」。

E77 报的 `BOUNDED frame2=287410 eof=False / UNBOUNDED frame2=313082 eof=True` 我**完整复现了**（见 §4），但它是同一坐标 bug 的连带现象，不是 `packed_size` 语义问题。

---

## 1. 权威字段语义（实测）

来自 `codec["list_tables"]` / `codec["_resolve_table"]`：

| 字段 | 实测语义 | 本次用法 |
|---|---|---|
| `offset` | **相对 `data_base`** 的成员起点，不是文件绝对偏移 | 成员起点 = `data_base + offset` |
| `packed_size` | 成员压缩区**总字节数**（含全部帧 + 成员内的 `tad.` 前缀） | 帧枚举硬上界 |
| `size` | 真实解压 payload 字节数 | **唯一选帧判据**：`len(frame) == size` |
| `sha256` | **压缩区** SHA-256（**不是** payload SHA） | 成员边界自证（460/460 命中） |
| `payload_version` / `record_count_header` | 取自 payload +6..8 / +8..12 | 多帧同长时消歧（本次未触发） |

> 关键点：`sha256` 是 packed SHA。任务书说「先查 sha256 是否为 payload SHA」——**不是**。实测 5 个锚点 `sha256(archive[start:start+packed_size]) == entry["sha256"]` 全 True，`sha256(payload) == entry["sha256"]` 全 False。该字段因此成为**成员定界的最强自证**，比 `size` 更早可用。

`data_base` 实测：`server_db.dat` = 34，`client_db.dat` = 34，`lang_update_db.dat` = 34（`03017461642ef10d` + `0201666d662e080000` = 8+9+… 共 34B 头）。

---

## 2. 选帧判据与实现

```python
start = data_base + entry["offset"]          # 成员绝对起点（旧法漏了 data_base）
end   = start + entry["packed_size"]         # 成员硬边界
frames = 逐帧 decompressobj(unused_data 推进) # 绝不读 end 之外
return 该 frame where len(frame) == entry["size"]  # 唯一命中
# 无命中 / 同长多帧消歧失败 → raise FrameError（不回落首帧）
```

两阶段边界策略（`inspect_entry`）：

1. **P1 `packed_size`**：严格区间。实测 460/460 条目在此阶段即选出正确帧，`leftover == 0`。
2. **P2 `next_member_start`**：仅当 P1 帧被截断（`eof=False`）或无 `size` 命中时，扩到**下一成员起点**重试，仍不跨成员。是否升级全部落盘（`escalated` / `surface` 字段）。

P2 存在的理由：任务书/E77 担心「packed_size 只覆盖真实帧、不覆盖整成员」。**实测该情形不存在**（P1 全部成功），但 P2 让加载器在该假设成立时仍能正确工作，且不会越过成员边界——两条要求同时满足,不靠选边站。

---

## 3. 多帧成员清单

**结论：0 个多帧成员。**

```
server      entries= 77  单帧=77   多帧=0  非吻合=0
client      entries= 31  单帧=31   多帧=0  非吻合=0
lang_update entries=352  单帧=352  多帧=0  非吻合=0
合计        entries=460  单帧=460  多帧=0  非吻合=0
```

每个条目的 `frame_count`、`frame_lengths`、`leftover_bytes`、`conforms_single_frame_size` 见 `multiframe_report.json` → `members[]`。故「首帧 stub 长度 / 真实帧相对偏移」两列在多帧语境下**为空**（无此现象）；下表给出任务书点名的五表在**正确坐标系**下的实况：

| archive | table | entry.offset | data_base | 成员起点 | packed_size | size | 帧数 | 帧长 | 唯一帧成员内偏移 | leftover |
|---|---|---|---|---|---|---|---|---|---|---|
| server | 34 | 38972269 | 34 | 38972303 | 89082 | 313082 | 1 | [313082] | +0 | 0 |
| client | 3 | 1117295 | 34 | 1117329 | 2058628 | 6932082 | 1 | [6932082] | +0 | 0 |
| server | 73 | 38661537 | 34 | 38661571 | 53 | 45 | 1 | [45] | +0 | 0 |
| server | 66 | 24307967 | 34 | 24308001 | 5834 | 18094 | 1 | [18094] | +0 | 0 |
| server | 43 | 24766564 | 34 | 24766598 | 8796 | 24632 | 1 | [24632] | +0 | 0 |

对比 t33 profile 里 `packed_offset` 记的值（如 server73=38661571）：**它已经等于 `data_base+offset`**——即 t33 用的是正确坐标，`fm24_dump` 用的是错的。

---

## 4. E77 复现与归因（可执行证据）

`e77_repro()` 在 `--selftest` 中执行，产物在 `multiframe_report.json` → `e77_investigation`。

E77 的坐标是 `entry.offset + 9`（server34 首 MAGIC 相对 `entry.offset` 的偏移 = 9）。但那个 9 是**绝对坐标**下的偏移，正确成员起点是 `data_base + offset`：

```
E77 起点      = 38972269 + 9 = 38972278   ← 在 12B stub 成员内部
正确成员起点  = 34 + 38972269 = 38972303   ← 差 -25B
E77 终点      = 38972269 + 89082 = 39061351  ← 也是绝对坐标
```

复现结果（三个坐标系同表对比）：

| 坐标系 | 区间字节 | 帧 (len, eof) | leftover |
|---|---|---|---|
| E77 bounded `[off+9, off+packed_size)` | 89073 | **(12, True), (287410, False)** | — |
| E77 unbounded `[off+9, EOF)` | — | (12,T), **(313082,T)**, (18628502,T) | — |
| **正确** bounded `[base+off, base+off+packed_size)` | **89082** | **(313082, True)** | **0** |

`287410 eof=False` 与 `313082` 是**末 34 字节被切掉**所致,不是 `packed_size` 太短:

* E77 终点 `off + packed_size = 39061351`,正确成员终点 `34 + off + packed_size = 39061385`,**短 34B**;那 34B 就是 `data_base`。
* E77 区间 89073B,真实帧从区间内 +25 处起算,可用 `89073 - 25 = 89048B`,而帧需 `89082B` —— **恰好少 34B**,与上面一致。
* 起点多出的 25B 是前一成员的尾部(12B stub 帧 + 13B 残留),因此区间总长只差 9B(`89082 - 89073`)看起来像是「差 9 字节」,但那 9B 是 25B 误入与 34B 被切的**净差**,不是截断量。

判定：`packed_size_is_whole_member = True`（正确坐标下单帧、`len==size`、`leftover==0`）。

---

## 5. 单帧回归结果

20 表（t33 七表 + t29 十三表）逐表对照：

| 项 | 结果 |
|---|---|
| `mf` payload size+SHA 与已落盘证据一致 | **20/20** |
| `mf` 与 `load_payload` 完全相同 | 19/20 |
| 差异 | 1 表：`server#34`（`legacy=12B` vs `mf=313082B`） |
| 无法用「旧法漏 data_base」解释的差异 | **0** |

### 5.1 旧法缺陷判定式（100% 可验证）

```
predict(load_payload 取错帧) ≡ [该条目的前一成员 packed_size < data_base]
```

在 server / client / lang_update 三归档 **460 条目**上：预测集合 == 实测错帧集合，`symmetric_diff = 0`。命中 **119** 个条目（server 2 + lang_update 117 + client 0）。

机制：`load_payload` 从 `entry["offset"]`（绝对）起扫 64B。若前一成员 `packed_size < 34`，则 `offset` 落在**前一成员**内，扫到的首个 MAGIC 属于前一成员 → 返回前一成员的 payload。若前一成员 `≥34`，窗口内的首帧恰是正确帧，**不报错**，缺陷被掩盖（119 vs 460 的分布即由此而来）。

注意：受害面 **不限 `table_34`**。`lang_update_db.dat` 有 117 个条目落入此模式，之前从未暴露，因为没人按 table 语义验证过它们。

### 5.2 与 `load_payload` 差异表

| archive#table | `load_payload` | `load_payload_mf` | 根因 |
|---|---|---|---|
| server#34 | 12 B（前成员 `non_player_bans` 的 payload） | 313082 B ✅ | 前成员 packed=25 < 34 |
| 其余 19 表 | 正确 | 相同 ✅ | 前成员 packed ≥ 34 |
| lang_update 117 条目 | **错**（未在回归集，普查中发现） | 正确 | 前成员 packed=25 < 34 |

---

## 6. 诚实失败（负结果保留）

| 场景 | 行为 | selftest |
|---|---|---|
| `size` 无任何帧匹配 | `raise FrameError`，不返回首帧 | `negative no-match raises` |
| `packed_size` 被截断且有下一成员 | 升级到下一成员起点重试，取到正确帧 | `truncated packed_size escalates` |
| `packed_size` 被截断且是**末成员**（无升级目标） | `raise FrameError` | `truncated last member raises` |
| 帧在区间内 `eof=False` | P1 记录截断；不静默补零 | `phase1.error` 落盘 |
| 同长多帧消歧后仍 >1 | `raise FrameError` | 代码路径就绪，本次数据未触发 |

`iter_frames`（严格）与 `decode_frames`（可观测截断）分离：前者供边界自证，后者供诊断，避免「用报错掩盖诊断信息」。

---

## 7. 对后续任务的影响

* **E66 解除**：用 `load_payload_mf(codec, "server", 34)` 即可拿到 313082B。不需要等 sol 静态闭合。
* **集成建议（待指挥官决定）**：`fm24_dump.load_payload` 的最小修复是
  `hit = next(...)` 改为在 `db[data_base+off : data_base+off+packed_size]` 内扫描，并以 `size` 选帧。本次**未改**该文件。
* **`lang_update` 117 条目**是新发现的风险面，任何基于 `load_payload` 的 lang_update 分析结论都需复核。
* **`t33` profile 的 `packed_offset` 值正确**（= `data_base+offset`），与本次坐标一致，可继续沿用；`fm24_dump` 用绝对 `offset` 才是异常方。

---

## 8. 复现命令

```bash
py -V:3.12 -I -B scripts/t38_multiframe.py --help
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t38_multiframe.py --selftest
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t38_multiframe.py --scan
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t38_multiframe.py --dump server 34
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t38_build.py --build
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t38/out/verify.py --selftest
py -V:3.12 -I -B scripts/t01_anchors.py
```

## 9. 证据等级

| 证据 | 等级 | 说明 |
|---|---|---|
| 460 条目单帧 + `len==size` + `leftover==0` | **L1** 自家解码自检 | 从归档字节直接复算 |
| `sha256(packed region) == entry.sha256` 460/460 | **L1** | 成员定界自证 |
| 五锚点 payload size+SHA 匹配 t29/t33/t35 已落盘值 | **L2** 独立事实对照 | 与既有证据交叉 |
| 旧法缺陷判定式 0 反例 | **L1** | 预测 == 实测，460 条目 |
| E77 截断复现（287410 / 313082） | **L1** | 三坐标系同表 |
| `data_base`=34 的含义 | 候选 | 未做 L3 exe 静态确认；仅作「必须加到 offset 上」的操作性事实使用 |
