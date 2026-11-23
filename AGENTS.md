# AGENTS.md — fm24-db

## 项目地图

| 路径 | 作用 |
|---|---|
| `AGENTS.md` | 本文件，工作区入口 |
| `README.md` | 导航与命令速查 |
| `docs/REPO_STATUS.md` | 仓库现状速览 |
| `docs/BASELINE.md` | 覆盖率基线 + 增量台账 |
| `docs/refs.md` | 外部只读引用与路径 |
| `prompts/` | 各任务（tNN）的 pi 车队 brief |
| `scripts/` | 解码/普查/复算脚本（Python 3.12 `-I`） |
| `reports/` | 结论报告 + 同名机读 JSON |
| `reports/club_nation_subtable_schema.json/.md` | 公共 schema（v11.1） |
| `evidence/fm24/` + `evidence/MANIFEST.json` | 旧证据库只读快照（带 SHA-256） |
| `scratch/<任务>/` | 临时实验、会话与 IDA 产物（不入验收） |
| `.pi/` | pi harness 配置 |

外部只读引用：游戏库 `Z:\SteamLibrary\...`、旧证据库 `D:\tmp2b\fm24`。不启动游戏本体与 FM Editor；IDA 静态分析允许。

## 目标



| 阶段 | 目标 | 状态 |
|---|---|---|
| 一 | comp 表 packed 区（table_25 +0..51 / +68..113）≥10 字段 L3 定位 | 已达标：comp 主行 49 L3，集合层 7 文法 + 4 引用 lane |
| 二 | 50 张 unknown 数值表的表号→实体映射 | 进行中：部分经引用闭合，余表未逐一映射 |
| 三 | club/nation 批量字段映射（433+346，滚动推进） | 进行中：club 主行 43 L3、nation 5 L3、comp 49 L3；物理覆盖 110/1,034 = 10.6% |

person 属性块（PDxx）不在范围内，需用户明示才启动。
