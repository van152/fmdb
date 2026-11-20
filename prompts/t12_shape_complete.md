# t12 任务书：形态完整的 4CC 抽取 —— 让 club 从 302 走到 420+

## 一句话目标

现有 4CC 抽取器只认"窄读"一种形态，导致 club 的 483 个存在于二进制里的字段码中有 181 个**取不到偏移**（覆盖率 302/483 = 63%）。本任务把抽取器做成**形态完整**的五类，并把 club 的 `名字 → 偏移/路径` 覆盖率推到 **≥420/483**。

这是阶段三（club 433 / nation 346 字段）的解锁条件，不是锦上添花。

## 事实基线（指挥官已独立验证，可直接引用）

| 项目 | 数值 | 来源 |
|---|---|---|
| **平表命名基线（以此为准）** | **129/240**（chain_unique 68 / ambiguous 11 / readpair 37 / ref_only 8 / ref_pair 3 / schema_fixed 2 / unresolved 111），schema 违规 **0** | `scratch/t11/out/naming_result.json`（`status=complete_schema_constrained_ref_ptr`）|
| t08 的 138 为何作废 | 其中 14 个是错名：9 个违反 schema，另 5 个是 **injury 的字段漏进 lcrg**（t47 被配到 injury 的 chain_0162，icla/iscl/Iocr/Imip/Iagr/Icdp 全是 injury 的码）| E47 + t11 的 `rejected` 字段 |
| club 字段码 | 声明 433 字段 / 含子字段 672 条 / **575 个去重码** | `scratch/t05/schema_inventory.json` |
| club 码字节存在性 | 483 存在（按立即数**反序**搜）、92 不存�� | E48 |
| club 码偏移覆盖 | **302 已解析 / 181 在但未解析** | E48 |
| club 链形态 | **无主链**：226 条链里覆盖 club 码最多的一条只有 20 个 | E48 |

### 已实证的 5 类形态（照此实现，别自己发明）

| # | 形态 | 判别式 | 取什么 | 实例 |
|---|---|---|---|---|
| 1 | `read` | `movzx/movsx/movsxd/movss` 或 `mov dword/word/byte ptr [reg+OFF], reg` | `OFF` + 宽度 | injury/city/stad 全部 |
| 2 | `ref_ptr` | `mov r64, qword ptr [reg+OFF]` 后 3 条内 `test` + 空检查跳转 | `OFF`，**宽度取 reader（通常 4）** | `Sold`@0x1538f2d→obj32；`Salt`@0x153920a→obj72 |
| 3 | `write` | 分支块内 `mov <sz> ptr [reg+OFF], reg` | `OFF` + 宽度 | injury 的 setter 路径 |
| 4 | `path_descend` | `add rdi, IMM` / `lea rdi,[rdi+IMM]` 后接 `jmp` 或 `call` | `IMM` 作为**下沉量** | `Cccn`@0xe846d0→`add rdi,0xf0`+`jmp`；`Cnam`@0xe550af→`add rdi,0x18`+`call` |
| 5 | `remote` | `je` 目标距离 > 0x1000 且本地块无访问 | 只记 target VA，**不许猜偏移** | `Csnm`@0xe83e03→`je 0x140e85db1` |

### 两个必须避开的坑（都已在别处炸过）

1. **分支极性**：`je/jz` → 取**目标块**；`jne/jnz` → 取 **fall-through**；但 `jle/jl/jg/jae/ja/jb/jbe` 是**边界比较**，它的目标与 fall-through 都**不属于本条码**（属于前一个码的路径）。t08 曾在 `ScYK` 上踩过：`ScYK` 是前一条 `jle` 的边界比较，其后的访问被误挂到 `ScYL`。你必须有一条自检专门覆盖这个陷阱。
2. **比较寄存器不固定**：实测有 `edx / ebx / eax / r8d` 四种（`81 FA / 81 FB / 81 F8 / 41 81 F8`）。不要写死前缀列表——按 **imm32 反序字节**（4CC 在机器码里是 `code[::-1]`）全段搜索，再回验该处能否解码成 `cmp` 且立即数等于该码。

## 工作项

### A. 抽取器 `t12_extract.py`

- 输入：`editor.exe`（只读，路径见 `docs/refs.md`，SHA-256 应为 `b82ebe8e…adab4`）。
- 输出 `scratch/t12/out/codes_full.json`：
```json
{"<4CC>": [{"shape":"read|ref_ptr|write|path_descend|remote",
            "object_off": 32, "size": 4, "descend": null,
            "file_off": "0x1538f2d", "access_va": "0x14153992d",
            "instruction": "mov rcx, qword ptr [rbx + 0x20]",
            "branch": "jne", "route": "je_target|fallthrough|target_remote",
            "why": "一句可核对的话"}]}
```
- 每个码保留 1–6 条实例；`path_descend` 与 `remote` 允许 `object_off=null`，但**必须**填 `descend` 或 `target_va`。
- 规模自检：全段应有 ~14,000 处可打印 4CC 分支（指挥官实测 14,171）。

### B. club 路径表 `club_paths.json`

对 575 个 club 字段码逐个给出：

```json
{"<code>": {"kind":"offset|path|remote|absent",
            "object_off": 240, "descend": [240], "instances": 2, "confidence":"high|mid|low"}}
```

- `offset`：顶层字段，单点偏移；
- `path`：`path_descend` 形态，`descend` 是从父对象到该字段的**下沉量序列**（当前只拿到第一段就写一段，并在 `why` 里注明"路径不完整"）；
- `remote`：目标远跳，暂不可解；
- `absent`：二进制里确实没有该码的字节。

**必须给出的数字**：575 个码里 `offset` / `path` / `remote` / `absent` 各多少，以及"有偏移信息（offset+path+remote 合计）"占比。

### C. 重跑平表命名（防回归 + 顺手提分）

用 `codes_full.json` 重新命名 26 实体（沿用 t08 的链分组与配对逻辑即可，不必重做），并接入 schema 约束（见 E47）：

- 候选名必须属于该 type_id 归属 schema 的字段码集（5 个通用码 `duni/rdui/NDBC/FDBC/dbnm` 除外）；
- 归属判定用**稀有码加权投票**（权重 `1/df`），不要用覆盖率——覆盖率会被通用码污染（t47 曾被误判成 injury，导致 6 个 injury 字段漏进 lcrg）；
- **小表加一条硬约束**：11 个零命名实体的槽数只有 1–5 个，归属候选必须满足"该 schema 的非通用字段数 ∈ [槽数, 槽数×3]"。t11 把 t31/t35（3 槽、2 槽）映射到 `club`（570 个字段），这在搜索空间上等于没约束，是它小表分析失败的直接原因。

## 交付（写到 `scratch/t12/out/`）

1. `codes_full.json`、`club_paths.json`、`naming_result.json`（三份都要，顶层带 `"status"`）。
2. `extract.py`（或 `build.py`）+ `verify.py`，均有 `--help` 与 `--selftest`。
3. `REPORT.md`：逐形态计数（read/ref_ptr/write/path_descend/remote 各多少码）、club 四分类数字、平表命名前后对比、剩余缺口归因。

## 验收线（缺一即 FAIL）

1. **club 覆盖 ≥420/483**（从 302 起）。若达不到，必须给出逐码归因表，说明剩下的码属于哪类、为什么抽不到——**不许只报一个总数**。
2. **平表命名 ≥ 129（不许低于 t11）**，且**违规归零**（沿用 t11 的 schema 约束，`schema-illegal` 必须仍为 0）。目标 ≥150：多出来的部分应当来自本次新增的 `ref_ptr / write / path_descend` 形态，而不是放宽判据。**如果你发现某些槽是"靠放宽阈值"补回来的，宁可不要。**
3. `Sold / Snew / Salt` 三槽命名成功，`object_off` 分别为 **32 / 40 / 72**。
4. injury 13/13、city 6/6、t07 的 45 名零回归，全部仍 PASS。
5. `verify.py` 必须包含**指挥官口径的独立复核**：
   - 每条实例的 `access_va` 处反汇编出的指令文本，与其 `instruction` 字段**逐字相同**；
   - 每个 `file_off` 处确实是 `cmp` 且立即数反序解码后等于该码；
   - 分支极性规则（`jle/jl/jg` 不得挂访问）有专门用例。
6. `ScYK` 陷阱用例通过（证明边界比较没被误挂）。

## 纪律

- `py -V:3.12 -I`；退出码 0/1/2。
- **只读**：`scripts/`、`scratch/t05`、`scratch/t06`、`scratch/t07`、`scratch/t08`、`scratch/t11`、`scratch/cmd` 一律不许改；只写 `scratch/t12/out/`。
- 不许联网、不许启动游戏/编辑器。
- 不许把 t08/t11 的 `naming_result.json` 复制改名当交付；`codes_full.json` 必须是新抽取的产物，且 `path_descend` 形态的实例数必须 > 0（否则说明第 4 类没实现）。
- **先落盘骨架**（`"status":"in_progress"`），完成时 `"status":"complete_<限定词>"`。
- 负结果可接受，但必须带数字：例如"某形态在 575 个 club 码里只命中 3 个，原因是……"。
