# t43 — 把 t38 `data_base` 修复集成进 `fm24_dump.load_payload`

**任务**:E80 已证实 `load_payload` 漏加 FMF `data_base`,致 119 条目误读前一成员。本任务把修复**最小化**地集成进共享加载器,并做全回归。
**改动范围**:`scripts/fm24_dump.py` 的 `load_payload` **一个函数**(+40/−5 行;AST 逐节点比对确认其余函数/常量零变化)。
**交付**:`scratch/t43/out/{integration_report.json, verify.py, verify_result.json, REPORT.md, DONE.md}` + `scratch/t43/build.py`。

---

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 修复落地 | `load_payload(codec, archive, tid) -> bytes`,签名/返回类型不变 ✅ |
| server34 | 12B stub → **313082B**(SHA `a07b2bb7…`,与 t38/t29 已落盘值一致) ✅ |
| `fm24_dump --selftest` | 49/0/**1 SKIP** → **50 PASS / 0 FAIL / 0 SKIP** ✅ |
| 单帧回归 vs `load_payload_mf` | **25 表逐字节全等**(t33 七 + 锚点三 + client0/2/3 + t29 其余 + client25/47) ✅ |
| 119 受影响条目 | 全部 `len == entry["size"]`、单帧、`leftover == 0`、`sha256(packed 区) == entry.sha256` ✅ |
| `t01_anchors.py` | 7/7 ✅ |
| `t38 --selftest` | HEAD 版本 **24 PASS / 0 FAIL**(见 §4:25→24 是**正向**证据) |
| `t39_spot` / `t34_spot` / `t36_spot` | 26/26 · 13/13 · 9/9 ✅ |
| 独立 `verify.py` | **19 PASS / 0 FAIL**(不 import `fm24_dump`,子进程调用;FMF 头/目录自解析) ✅ |
| data_base=34 结构含义 | **仍为候选**(未做 L3 exe 静态确认);本次仅作操作性偏移使用。L4=0 |

**一句话**:修复后 `load_payload` 与已接受的参考加载器 `load_payload_mf` 在全部 25 张对照表上字节全等,缺陷家族 119 条目全部闭合,无任何回归。

---

## 1. 修复内容(最小改动)

```python
base  = int(codec["_archive_layout"](db)["data_base"])   # 动态取,不硬编码 34
start = base + int(e["offset"])                          # 成员绝对起点(= 旧法漏掉的那一步)
end   = start + int(e["packed_size"])                    # 成员硬边界
size  = int(e["size"])                                   # 唯一选帧判据
# 成员区内逐帧解压(zstd decompressobj + unused_data 推进),绝不读 end 之外:
#   len(frame) == size  → 返回
#   无吻合帧            → raise RuntimeError(不回落首帧、不静默截断)
```

要点:

1. **`data_base` 从 codec 动态取**。`verify.py` 用 AST 检查 `load_payload` 的**代码体**(剔除 docstring)不含 `\b34\b` 字面量 —— 硬编码会被直接判 FAIL。
2. **帧枚举严格限制在成员区内**。旧法 `db[hit:]` 无上界,新法 `db[pos:end]`;`consumed <= 0` 或 `not obj.eof` 时停止循环而不是猜下一帧。
3. **失败即报错**。无 `len == size` 的帧 → `RuntimeError`,错误消息带成员区间与期望长度。
4. **不引入对 `t38_multiframe.py` 的任何 import**。实现独立(仅复用 codec 的 `_archive_layout` / `_zstd_module` 两个上游原语),`verify.py` 亦不 import `fm24_dump`。

**AST 逐节点核对**(`scratch/t43/build.py` 内逻辑 + 手工确认):`_reader`、`fixed_specs`、`walk_fixed`、`walk_lcrg`、`walk_club_block`、`dump`、`main`、`OVERRIDE`、`FIELDS`、`EXTRA_FIXED` 全部**字节未变**;唯一变化是 `load_payload`。

---

## 2. 修前后对照

### 2.1 关键表

| archive#table | 修复前 `load_payload` | 修复后 `load_payload` | `load_payload_mf` | 字节相等 |
|---|---|---|---|---|
| **server#34** | **12 B**(前一成员 `non_player_bans` 的 stub,$-$25B) | **313082 B** `a07b2bb7…` | 313082 B | ✅ |
| server#66 | 18094 B(碰巧正确) | 18094 B | 18094 B | ✅ |
| server#43 | 24632 B(碰巧正确) | 24632 B | 24632 B | ✅ |
| client#3 | 6932082 B | 6932082 B | 6932082 B | ✅ |
| 其余 21 表 | 正确 | 不变 | 不变 | ✅ 25/25 |

### 2.2 修复后 `load_payload` vs `load_payload_mf`:25 表逐字节全等

`integration_report.json` → `single_frame_regression_vs_load_payload_mf`:

```
targets = 25   byte_identical = 25   divergent = 0   raised = 0
```

表集:t33 七表(server 12/39/45/48/58/59/73)+ 锚点三表(server 34/66/43)+ client 0/2/3 + t29 其余八表(server 33/37/50/51/60/61/62/63/64/70)+ client 25/47。
> 注:client#47 是覆盖表(`variable/lcrg_tail`,109505 B),也要一并通过 —— 它证明修复对**变长文法表**同样无副作用。

---

## 3. 119 个受影响条目(含 lang_update)

### 3.1 判定式与分布

修复前缺陷判定式(E80):`前一成员 packed_size < data_base` ⇒ 旧法必错帧。

| archive | 受影响条目 |
|---|---|
| server | 2(`manager_player_preferences.dat`, `table_34.dat`) |
| client | 0 |
| **lang_update** | **117** |
| 合计 | **119** |

`verify.py` 独立重算该集合 = **119**(`per-archive={'server': 2, 'client': 0, 'lang_update': 117}`),与 t38 记录一致。

### 3.2 修复后逐条验证(119/119 全绿)

| 判据 | 结果 |
|---|---|
| `len(payload) == entry["size"]` | **119/119** |
| 成员内单帧、`leftover == 0`、无截断错误 | **119/119** |
| `sha256(packed region) == entry["sha256"]`(成员定界自证) | **119/119** |
| 旧法命中点相对正确成员起点偏移 | **119/119 = −25 B**(全部落在前一成员内) |

### 3.3 一个必须保留的负结果:42 个 `lang_update` 条目旧法**字节巧合相同**

旧法的 119 次命中全部偏移 −25B(落在前一成员的 25B `tad.` 空 stub 内)。其中:

* **77 条**旧法返回的字节与正确 payload 不同(被修复改变);
* **42 条**旧法返回**恰好相同的 12B stub 字节**(`600175712b2f…`)。

原因:这 42 个条目本身 `entry["size"] == 12`,而前一成员的 stub payload 也是同一个 12B 模板 —— 于是"取错成员"在**字节层面**不可见。

> **这是本次最重要的方法论发现**:在这些条目上,**长度校验和 payload SHA 自检都会通过**,只有「成员边界」判据(`sha256(packed region) == entry.sha256` + 起点 = `data_base+offset`)才能识别错误。任何以 `len` 或 `payload sha` 做自检的加载器,在这里都是**假阳**。`verify.py` 因此把「legacy 坐标错误 119/119」和「legacy 字节不同 77/119」分成两个独立检查项,不合并。

`integration_report.json` → `affected_entries_119.legacy_identical_12B_stub` 完整保留这 42 条记录。

### 3.4 修复前负例(不删)

```
server#34   legacy = 12 B   sha=600175712b2f553a…   hit_delta=-25B
server#34   fixed  = 313082 B sha=a07b2bb76fb8796b…  (a07b2bb7 与 t38/t29 已接受证据一致)
```

`verify.py` 中以 `negative server#34 legacy = 12B stub (preserved)` / `negative server#34 fixed = 313082` 两个检查项固定,不随修复消失。

---

## 4. 回归矩阵(全绿)

| # | 回归项 | 命令 | 结果 | 判据 |
|---|---|---|---|---|
| 1 | `fm24_dump --selftest` | `py -V:3.12 -I -B scripts/fm24_dump.py --selftest` | **50 PASS / 0 FAIL / 0 SKIP** | 修前 49/0/1SKIP;server34 SKIP→PASS,定长 PASS 不减,无新 FAIL ✅ |
| 2 | `t01_anchors` | `py -V:3.12 -I -B scripts/t01_anchors.py` | **7/7** | 要求 7/7 ✅ |
| 3 | `t38 --selftest` | `py -V:3.12 -I -B scripts/t38_multiframe.py --selftest` | **0 FAIL**(HEAD 版 24 PASS;工作区版 32 PASS,见 §4.1/§4.2) | 无新增 FAIL,参考加载器语义未变 ✅ |
| 4 | 单帧 25 表 vs `load_payload_mf` | `scratch/t43/build.py --build` | **25/25 字节全等** | 要求 ≥20 表 ✅ |
| 5 | `t39_spot` | `py -V:3.12 -I -B scratch/cmd/t39_spot.py` | **26/26** | 要求 26/26 ✅(自有 `pick_frame`,不受影响) |
| 6 | `t34_spot` | `py -V:3.12 -I -B scratch/cmd/t34_spot.py` | **13/13** | 用 `load_payload`(server#66)→ 仍 PASS ✅ |
| 7 | `t36_spot` | `py -V:3.12 -I -B scratch/cmd/t36_spot.py` | **9/9** | 用 `load_payload`(server#33)→ 仍 PASS ✅ |
| 8 | `t43 verify` | `py -V:3.12 -I -B scratch/t43/out/verify.py --selftest` | **19 PASS / 0 FAIL** | 独立复算 ✅ |

### 4.1 `t38` 为什么从 25 PASS 变成 24 PASS —— 这是正向证据,不是回归

`t38_multiframe.run_selftest` 的计分是 `len(lines) - len(fails)`,而**提示行也算一行**。修复前的输出里有一行信息:

```
DIFF[EXPECTED(E66-family)] server#34: legacy=12B vs mf=313082B
```

修复后 `legacy` 不再取错帧(现在也返回 313082B),这行差异提示**消失** → 少 1 行 → PASS 25→24,`FAIL` 仍为 **0**,全部检查项(锚点/选帧/成员边界/单帧回归/普查/负结果)逐条 PASS。

`build.py` 的 `t38_selftest_accounting` 段落把这件事钉成一个**受控实验**:取**同一份** `git show HEAD:scripts/t38_multiframe.py`(t38 已接受验收的版本),只切换 `fm24_dump.load_payload` 一个变量:

| 变量状态 | t38 HEAD 版 selftest | 差异提示行 |
|---|---|---|
| `load_payload` = **修复前**(临时 monkeypatch 回旧实现) | **25 PASS / 0 FAIL** (rc=0) | 1 条 `DIFF[EXPECTED(E66-family)] server#34` |
| `load_payload` = **修复后**(当前工作区) | **24 PASS / 0 FAIL** (rc=0) | 0 条 |

结论:少掉的那 1 条 **就是 server#34 的 legacy-vs-mf 差异行本身**,即修复生效的正向证据;`FAIL` 始终为 0,参考加载器逻辑未被本任务改动。

### 4.2 工作区被外部改动(诚实记录)

本任务执行期间,`scripts/t38_multiframe.py` 被**另一会话**追加了 145 行(新增 check #10/#11:无界选帧对照 `decode_frames_unbounded` / `boundary_spanning_proof`,用于记录无界 size-only 选帧在 `client#23` 上的歧义)。

* 该文件**不属于本任务改动范围**,本次未触碰(本任务只改 `fm24_dump.load_payload`)。
* 它也**没有**任何对修复的依赖或反向依赖:两版均 0 FAIL。
* 现场跑新版本会得到 **32 PASS / 0 FAIL**;HEAD 版本(与 t38 已接受验收一致)在修复后得到 **24 PASS / 0 FAIL**。
* `integration_report.json` 同时记录 `head_version_run` 与 `working_tree_run`,并注明外部改动来源,不做择一粉饰。

---

## 5. 独立验证(`verify.py`,不 import `fm24_dump`)

独立性设计:

| 环节 | 做法 |
|---|---|
| FMF 头 | 自解析:`base = start+9+u64(start+17)`,不调用上游 codec |
| FMF 目录 | 自写 `DirReader`(等价 `_DirectoryReader`),得 `offset/packed_size/size` |
| 帧枚举/选帧 | 自写,`len(frame)==size` 唯一命中 |
| 被验对象 | `subprocess` 调 `py -I -B -c "import fm24_dump; ..."`,本进程不持有其引用 |
| 对照基准 | 仓内已落盘证据(t33 profiles / t29 inventory) |

19 个检查项(全 PASS):

1. 三归档 FMF 自解析成功(`server/client/lang_update` data_base 均 = 34,动态取)
2. `load_payload` 源码使用 `_archive_layout`;代码体无 `\b34\b` 硬编码;无"回落首帧"路径
3. 20 表:`独立复算 == 已落盘证据(size)`、`== 证据(sha256)`、`load_payload == 独立复算(逐字节 SHA)`
4. 受影响条目集合 = 119;修复后 119/119 `len==size`、单帧、`leftover==0`;119/119 成员边界自证
5. 旧法坐标 119/119 错在 −25B;旧法字节 77/119 不同(其余 42 条为 12B stub 巧合,单独列示)
6. 负例固定:server#34 legacy=12B / fixed=313082(a07b2bb7…)
7. `lang_update` 抽样经 `load_payload`(路径形式)调用 == 独立复算
8. 五锚点独立复算(server34=313082 / client3=6932082 / server73=45 / server66=18094 / server43=24632)

---

## 6. 证据等级

| 证据 | 等级 | 说明 |
|---|---|---|
| 修复后 460 条目单帧 + `len==size` + `leftover==0` | **L1** | 归档字节直接复算(t38 普查 + 本次 119 抽样) |
| `sha256(packed region) == entry.sha256` 119/119 | **L1** | 成员定界自证 |
| 25 表逐字节 == `load_payload_mf` | **L1** | 两个独立实现互证 |
| 五锚点 payload size+SHA == t29/t33 已落盘 | **L2** | 独立事实对照 |
| `t01_anchors` 7/7、三个 spot 全 PASS | **L2** | 与已接受任务产物交叉 |
| `data_base`=34 的**结构含义** | **候选** | 未做 L3 exe 静态确认;仅作"必须加到 offset 上"的操作性事实。本次不写结构结论 |
| L4(真机加载) | **0** | 未启动游戏/编辑器 |

---

## 7. 复现命令

```bash
export FM24_DB_DIR=<WORKSPACE>/scratch/data

# 修复自检
py -V:3.12 -I -B scripts/fm24_dump.py --selftest          # 50 PASS / 0 FAIL / 0 SKIP

# 全回归
py -V:3.12 -I -B scripts/t01_anchors.py                   # 7/7
py -V:3.12 -I -B scripts/t38_multiframe.py --selftest     # 0 FAIL
py -V:3.12 -I -B scratch/cmd/t39_spot.py                  # 26/26
py -V:3.12 -I -B scratch/cmd/t34_spot.py                  # 13/13
py -V:3.12 -I -B scratch/cmd/t36_spot.py                  # 9/9

# 独立验证 + 证据重建
py -V:3.12 -I -B scratch/t43/out/verify.py --selftest     # 19 PASS / 0 FAIL
py -V:3.12 -I -B scratch/t43/build.py --build             # 写 integration_report.json
```

---

## 8. 未做 / 边界

* `data_base`=34 的结构含义**未做 L3 exe 静态确认** —— 本次是操作性修复,不写结构结论。
* 未启动游戏/编辑器/IDA,未联网,未读写 `Z:`;`<OLD_REPO>` 与 `scratch/data` 全部只读。
* 未改 `scripts/t38_multiframe.py`、`scripts/t01_anchors.py`、`scratch/cmd/*` 或任何其它任务产物。
* 未对 `lang_update` 的 117 个条目做业务语义解读(它们不是 `table_N.dat`,无表号);仅验证其 payload 边界与长度。
