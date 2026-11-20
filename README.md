# fm24-db — FM24 数据库语义解析工作区

专注一件事:**把 FM24 `.dat` 数据库的 schema 字段映射到行内偏移**。不做解密(容器层已解完)、不做 FMF 生成器、不做存档研究。

## 导航

- 使命与硬约束:[AGENTS.md](AGENTS.md)
- **仓库现状速览(2026-11-21 v11 同步):[docs/REPO_STATUS.md](docs/REPO_STATUS.md)**
- 覆盖率基线 + 增量台账:[docs/BASELINE.md](docs/BASELINE.md) — 冻结快照(2026-11-18)结构层 ~51-68% / 字段语义 ~1.5%;其后 E89–E121 增量见文档内各节
- 外部只读引用:[docs/refs.md](docs/refs.md) — 旧证据库 `D:\tmp2b\fm24` 与游戏库 `Z:`
- 证据快照:[evidence/fm24/](evidence/fm24/)(56 文件,SHA-256 见 [evidence/MANIFEST.json](evidence/MANIFEST.json))
- 公共 schema:`reports/club_nation_subtable_schema.{json,md}`(**v11**,E111–E120 已并入;E110 为 v10 验收点)
- schema v11 拆分件(主 schema 只留指针 + SHA-256):
  - `reports/other_tables_schema.json` — 13 张非主表槽位裁决(t73 4 + t76a 1 + t76c 4 + t74 行框 4)
  - `reports/xml_denominator_coverage.json` — 1,034 occurrence 分母台账(物理覆盖 110/1034 = 10.6%)

## 三阶段(进度)

1. **comp packed 区**:table_25 +0..51/+68..113 ≥10 字段 L3 定位 — **已达标**:comp 主行 49 L3(E99),集合层 7 文法 + 4 引用 lane(E104)
2. **50 张 unknown 表**实体映射 — **进行中**:t41/t19/t5/t9 等经引用闭合,余表未逐一映射
3. **club/nation 批量字段**(433+346,滚动推进,不设"全解"验收) — **进行中**:club 主行 43 L3(+22 经 E111 的 table_extra_3 对象投影)、nation 主行 5 L3、comp 主行 49 L3;三张主表行框均自证闭合。分母口径已量化:club 433 / nation 346 / comp 255 = 1,034 occurrence,物理覆盖 110/1,034 = 10.6%(E116)。

## 当前状态(2026-11-21)

- 分支 `t70-schemav10` 线性链;HEAD 已推进至 t82(E121);LEDGER **121 条**(末 E121)。
- **schema v10→v11(t77)已构建并自检**(E111–E120 增量合并;anchors 7/7、L4=0)。v11 纯增量:22 个 v10 根节 byte 不变,新增 10 个节 + 两个拆分件指针。
- E121(t82,table_extra_3 双对象闭合,35 新 L3)不在 v11 内,归 t87 补丁。
- 未结悬案:EDfx 上游持久化来源;award/language/media 三表槽位(t76b 三面碰壁,转 t83);merge-to-main(评估见 REPO_STATUS,未执行)。
- 车队全部空闲,无后台进程。

## 目录

| 目录 | 用途 |
|---|---|
| `docs/` | 使命基线、覆盖率、现状速览、外部引用 |
| `prompts/` | 各任务(tNN)的 pi 车队 brief |
| `scripts/` | 解码/普查/复算脚本(py 3.12 `-I`) |
| `reports/` | 结论报告 + 机读 JSON(同名成对) |
| `evidence/fm24/` | 旧证据库只读快照(带 SHA-256) |
| `scratch/<任务>/` | 临时实验、pi 日志/会话、IDA 会话产物(不入验收) |
| `.pi/` | pi harness 配置 |

## 命令

```powershell
py -V:3.12 -I scripts/baseline_coverage.py            # 复算基线聚合
py -V:3.12 -I scripts/baseline_coverage.py --check    # 对照 BASELINE.md 数字(快照数字仍 OK)
py -V:3.12 -I -B scripts/t01_anchors.py               # 冻结锚点回归(7/7)
py -V:3.12 -I -B scripts/t77_schema_v11.py --selftest # v11 构建器自检
py -V:3.12 -I -B scripts/t77_schema_v11.py --verify   # 重读全部输入、复算每节计数(只读)
```
