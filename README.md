# fm24-db — FM24 数据库语义解析工作区

专注一件事:**把 FM24 `.dat` 数据库的 schema 字段映射到行内偏移**。不做解密(容器层已解完)、不做 FMF 生成器、不做存档研究。

- 使命与规则:[AGENTS.md](AGENTS.md)
- 覆盖率基线(2026-11-18):[docs/BASELINE.md](docs/BASELINE.md) — 结构层 ~51-68%,字段语义 ~1.5%
- 外部只读引用:[docs/refs.md](docs/refs.md) — 旧证据库 `D:\tmp2b\fm24` 与游戏库 `Z:`
- 证据快照:[evidence/fm24/](evidence/fm24/)(56 文件,SHA-256 见 [evidence/MANIFEST.json](evidence/MANIFEST.json))

## 三阶段

1. **comp packed 区**:table_25 +0..51/+68..113 ≥10 字段 L3 定位(服务赛事闭环)
2. **50 张 unknown 表**实体映射(复用通用映射结构)
3. **club/nation 批量字段**(433+346,滚动推进,不设"全解"验收)

## 当前任务

- `t01`:editor.exe 字段槽位映射侦察(未开始)

## 命令

```powershell
py -V:3.12 -I scripts/baseline_coverage.py            # 复算基线聚合
py -V:3.12 -I scripts/baseline_coverage.py --check    # 对照 BASELINE.md 数字
```
