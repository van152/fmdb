# b51 handoff — summary.dat / history structures

日期：2026-11-17　分支：`work/b51-summary-hist`

## 交付与验收

### 1) `summary.dat`：结构完成，语义负结果

- `scripts/b51_summary_fields.py` 可独立重跑；`--selftest` 5/5 true。`reports/dbdat_decode/summary_field_map.json` 对 2430 文件精确记账 1,648,018 B，描述 54,087 个 delimiter occurrence、54,086 个候选 body、53,742 个 17B body、344 个非 17B body、117 个 extended candidate。
- 标准 body 11 个可复现 raw 槽位均有 offset/width/encoding/profile；b0..b5、三列 u16、id 语义均未独立命名。L2 named field=0；ID/DBID/历史 ID 交叉不足以构成 entity join。变长候选及 head/升序 ID 列表/63 组 `(u32,float32)` 也保留为 unresolved。详见 `reports/dbdat_decode/SUMMARY_SEMANTICS.md`。
- L3 已到 editor.exe writer 链：`sub_140FF3840`、调用者 `sub_140035F10`（call xref `0x140036b0b`）、日志函数 `sub_14004AF40`、nested vector writer `sub_140FF4420`；给出源对象成员偏移及告警条件，但无法逐字节对齐到每个 raw body 槽位。L3 不是 L2，也不是运行时加载证据。
- 按任务书允许的验收分支，交付的是**逐槽穷尽负结果 + L3 函数证据路径**，不是“字段语义已验证”。L4=0。

### 2) non-player 历史索引：L1 结构闭合

- `non_pl_hist_index` 754,688 项：673,317 个唯一 key、81,371 个重复 key 额外项、8,145 个 `0xffffffff` sentinel；有效 ordinal 恰为 `0..746542` 的完整置换。
- `non_pl_hist_id` 746,543 个 inclusive 范围；全部 start≤end、24B 对齐；相邻 746,542 个范围 gap 全为 24B。
- `non_pl_hist_dt` 3,212,443×24B = 77,098,632 B，含 2,465,900 工作行 + 746,543 终止符；所有 next 链/terminator 检查通过，尾部余数 0。key 不唯一且有 sentinel，不能直接当唯一职员主键，也不能推出当前职员人数。
- 报告 `NONPL_HIST_INDEX.md`、JSON `nonpl_hist_index.json`；脚本 `b51_nonpl_hist_index.py`；selftest 5/5，分析检查 10/10。

### 3) `pl_hist` 稀见 row_type：明确负结果

- `scripts/b51_rare_hist.py` 全量拆分 4,515,803 物理行（4,000,222 career + 515,581 terminator），验证范围/链 0 违例；解释此前含 terminator 与不含 terminator 的统计差值。
- ≥3 的 14 个码均列于 `HIST_RARE_TYPES_B51.md` 和 `rare_hist_types_b51.json`。本机姓名/球队 join 只算 L1；没有独立事实源或消费者 enum 能把任何稀见码定为 L2：0/14 定级。type 4/16/24/20 等样本提供上下文，不强行命名。selftest 4/4。

## 修改文件

- `scripts/b51_summary_fields.py`、`scripts/b51_nonpl_hist_index.py`、`scripts/b51_rare_hist.py`
- `reports/dbdat_decode/SUMMARY_SEMANTICS.md`、`NONPL_HIST_INDEX.md`、`HIST_RARE_TYPES_B51.md`
- 对应机读文件 `summary_field_map.json`、`nonpl_hist_index.json`、`rare_hist_types_b51.json`
- `reports/DBDAT_FORMAT.md` 更新 non-player / summary / rare-history 状态；`tmp_b51/PROGRESS.md` 记录过程。

## 验证

- 三个脚本 `--help` 可用；全部 `--selftest --json` 通过；三种真实 `--json` 输出均由 Python JSON parser 成功读取。
- 全量回归：**12 PASS / 0 FAIL / 0 SKIP**，含 12 个用户 DBC payload/整文件、官方 DBC、AFE repack、8 份 save 共 8,977 个成员、语言/Schema、3,861 个安装数据文件/1,092 个存档成员与官方自检。
- 为严格保持主树只读，未在 `<OLD_REPO>` 原地运行会覆盖其 baseline 的脚本；把当前主树 runner 临时复制到 `tmp_b51`，使 ROOT/output 落在本 worktree。三个临时 junction（`dbc_decoded`、`decrypted`、save samples）只用作只读输入，所有输出落在 worktree；随后逐个 `rmdir` 删除 junction 并验证目标目录仍存在。回归的生成 tracked QA/index 文件已恢复；主树未作为 runner 的输出根。

## 安全与证据边界

- 未启动游戏/Editor、未 attach。主树及 `Z:` 输入按只读处理；工作区临时 IDB 与 runner/junction 已清理。
- IDA 无符号运行时，PDB provider 曾尝试 `%LOCALAPPDATA%\\Temp\\ida\\editor.pdb\\...` 并报告 “Could not find PDB file”；没有加载 PDB 符号。是否创建过空临时目录无法确认；依只读边界未检查或清理用户目录，也未再运行 IDA。此情况已记入 `tmp_b51/PROGRESS.md`。
- L1 是结构/字节证据，L2 为独立语义锚点，L3 为 exe 静态路径，L4 为真机加载；本任务没有 L4 结论。

## 后续建议

1. summary：继续从 `sub_140FF4390`、`sub_140FF47B0` 及 `unk_14157FD30` 解 helper，再用独立聚合统计/俱乐部历史对齐标准槽；目前不具备安全命名依据。
2. rare row_type：寻找 `fm.exe` 消费端 enum/switch，或可引用的历史履历数据源，优先验证 type 4/16/24；现有 L1 模式不够定级。
3. non-player：role 2,817 最常见但 176 种枚举仍未定名；key→people duni 关系仍未做；不要用 range 数量冒称当前 staff 人数。
4. 不要把 summary 的 0 个 L2 字段、rare code 的 0/14 L2 或 L4=0 改写为“验证通过”。
