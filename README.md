# fm24-db — FM24 数据库语义解析工作区

专注一件事:**把 FM24 `.dat` 数据库的 schema 字段映射到行内偏移**。不做解密(容器层已解完)、不做 FMF 生成器、不做存档研究。

## 导航

- 使命与硬约束:[AGENTS.md](AGENTS.md)
- **仓库现状速览(2026-11-20):[docs/REPO_STATUS.md](docs/REPO_STATUS.md)**
- 覆盖率基线 + 增量台账:[docs/BASELINE.md](docs/BASELINE.md) — 冻结快照(2026-11-18)结构层 ~51-68% / 字段语义 ~1.5%;其后 E89–E109 增量见文档内各节
- 外部只读引用:[docs/refs.md](docs/refs.md) — 旧证据库 `D:\tmp2b\fm24` 与游戏库 `Z:`
- 证据快照:[evidence/fm24/](evidence/fm24/)(56 文件,SHA-256 见 [evidence/MANIFEST.json](evidence/MANIFEST.json))
- 公共 schema:`reports/club_nation_subtable_schema.{json,md}`(**v10**,E110 已验收提交)

## 三阶段(进度)

1. **comp packed 区**:table_25 +0..51/+68..113 ≥10 字段 L3 定位 — **已达标**:comp 主行 49 L3(E99),集合层 7 文法 + 4 引用 lane(E104)
2. **50 张 unknown 表**实体映射 — **进行中**:t41/t19/t5/t9 等经引用闭合,余表未逐一映射
3. **club/nation 批量字段**(433+346,滚动推进,不设"全解"验收) — **进行中**:club 主行 21 L3、nation 主行 5 L3、comp 主行 49 L3;三张主表行框均自证闭合

## 当前状态(2026-11-20)

- 分支 `t70-schemav10`;LEDGER **110 条**(末 E110)。
- **schema v9→v10(t70)已验收并提交**(E110;指挥官独立 spot 123 项 0 FAIL、anchors 7/7、L4=0)。
- 未结悬案:EDfx 上游持久化来源;club 350 / comp 196 / nation 318 未映射主行字段;comp 集合业务语义;merge-to-main(按 HANDOFF 搁置)。
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
```
