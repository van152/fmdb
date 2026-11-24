# 仓库现状速览（2026-11-24 更新）

本文件是新接手者的入口快照。**结论性证据以 `docs/BASELINE.md`、`reports/`、`scratch/t01/LEDGER.json` 为准**；`WAVE14_MORNING_REPORT.md` 是叙事性总结，不是验收依据。

## 一、身份与拓扑

| 项 | 值 |
|---|---|
| 使命 | FM24 `.dat` 数据库 → 行内偏移语义映射；已完成 13 个档案零误差解码与双向回写（详见 `AGENTS.md`） |
| 当前分支 | `main`，HEAD `2b11ee9` |
| 提交数 | 292 |
| 本地任务分支 | 36 条 `tNN-短名` 历史分支，全部保留 |
| 验收台账 | `scratch/t01/LEDGER.json` 142 条，末条 E142 |
| 远端 | `origin` = `github.com/van152/fmdb.git`；`origin/main` 与本地 HEAD 一致（merge 已完成，无待推送差异） |
| 公共 schema | `reports/club_nation_subtable_schema.json` **v11.3**（`generated_by=t92`，21.4 MB）/ `.md` 89 KB |
| 磁盘 | `.git` 211 MB、`scratch` 4.4 GB、`reports` 22 MB、`evidence` 17 MB |

### schema 拆分件

| 文件 | 内容 | 体积 |
|---|---|---|
| `reports/club_nation_subtable_schema.json` | 三主表 + 子表 + 4CC/L3 映射，43 个根节 | 21.4 MB |
| `reports/other_tables_schema.json` | 13 张非主表槽位裁决 | 280 KB |
| `reports/xml_denominator_coverage.json` | 1,034 occurrence 分母台账（E139 重桶后版本） | 338 KB |

主 schema 的 `pointer_artifacts` 节记录另外两件的路径与 SHA-256。

## 二、方法与硬约束

- **证据分级**：L1 自检 / L2 独立事实对照 / L3 exe 静态或机器码仿真证据（注明二进制、VA、来源）/ L4 完整真机加载（当前 schema 中仍记为 0）。候选不写成结论，负结果原文保留。
- **外部数据只读**：游戏库与旧证据库一律只读；引用旧证据须经 `evidence/fm24/` 快照 + `MANIFEST.json` SHA-256。
- **工具链**：Python 3.12；核心脚本提供 `--help` / `--selftest`，退出码 0/1/2。
- **落地位置**：临时实验进 `scratch/<任务>/`，结论进 `reports/`，机读结果与报告同名成对；`scratch/` 下大部分中间产物不入版本库。
- **口径提醒**：`WAVE14_MORNING_REPORT.md` 里的 editor.exe 验证是 Unicorn 机器码仿真（L3 扩展），不等同于 L4 完整游戏加载；两个说法不矛盾，但不要混用。

## 三、已达成的主要成果

| 任务 | 成果 |
|---|---|
| t106/t112/t119/t133 | 79/79 编号表 + 13 特殊成员 + summary.dat 纯 Python 零误差解码 |
| t120/t123/t138 | `people_db` / `basic_people_db` 658,011 行零误差解码，54/54 球员属性 GET==SET |
| t127/t128/t143 | 772.8 万条履历链、704 个语言包成员（22 语种）零误差闭合 |
| t135/t137d | 21 位球星 54 项属性、20 位名帅 34 项属性原盘直读 |
| t139/t140 | 191.7 MB SQLite 数仓；79/79 位级双向回写 + editor.exe 机器码回读 |
| t141/t142 | `fm.exe` ≡ `editor.exe` 数据库层同源证明；84 表外键图谱与 764 处官方悬空引用检出 |

字段语义净覆盖：`568/663 = 85.7%`（按 1,034 总 occurrence 的毛覆盖为 `568/1034 = 54.9%`，余 95 个缺口）。

## 四、环境与可复现

- Python 3.12（`py -V:3.12`）；`zstandard` 使用 vendor 版。
- 路径由 `scripts/fm24_config.py` 统一解析，可用环境变量覆盖：

| 环境变量 | 默认值 | 用途 |
|---|---|---|
| `FM24_ROOT` | 脚本所在仓库根目录 | 仓库根 |
| `FM24_LEGACY_DIR` | `D:\tmp2b\fm24` | 旧证据库 / 二进制输入 |
| `FM24_GAME_DIR` | `Z:\SteamLibrary\steamapps\common\Football Manager 2024` | 游戏安装目录 |
| `FM24_DATA_DIR` | `<ROOT>/scratch/data` | `.dat` 输入数据（被 git 忽略，需自行准备） |
| `FM24_VENDOR_DIR` | `<FM24_LEGACY_DIR>/tools/python` | vendor 依赖 |

- `scratch/data` 不入库；没有原始 `.dat` 数据时，只能跑 `--selftest` 中纯常量断言，无法复跑全量解码。
- `scratch/` 下除 `t01/LEDGER.json` 外全部停止跟踪；全量回归依赖的机读产物需要先运行对应 `--build` / `--selftest` 生成（本地已存在则直接使用）。

## 五、回归与验证

```bash
# 真实重跑 24 项核心自检 + 当前 schema 守卫（约 3 分钟）
py -V:3.12 -B scripts/t145_final_regression.py --selftest

# 只读快检：直接读取上一次的 regression_matrix.json，不重跑测试
py -V:3.12 -B scripts/t145_final_regression.py --cached

# 历史 v11 schema 校验器（冻结输入在 scratch/t77/frozen/）
py -V:3.12 -B scripts/t77_schema_v11.py --verify
```

`--selftest` 会把产物清单中缺失的文件判为失败；`reports/` 与 `scratch/t01/LEDGER.json` 受保护，任何测试不得改动。当前 schema v11.3 的内部一致性由 `t92_schema_v113.py --selftest` 覆盖。

## 六、仍开事项

1. EDfx 上游持久化来源未闭合。
2. 大三主表剩余 95 个语义缺口；优先看分母台账中 `unresolved_wire_slot` 分桶。
3. comp 集合层业务语义（物理文法已闭合）。
4. 历史一次性脚本（`scripts/tNN_*`）中仍有绝对路径，新增代码必须使用 `fm24_config.py`。

## 七、文档权威性

`README.md` → 本文件 → `docs/BASELINE.md` → `AGENTS.md` 是当前状态的权威入口。`WAVE14_MORNING_REPORT.md` 记录 2026-11-23 的叙事与战果清单，其中数字反映当时快照；与台账冲突时以台账为准。
