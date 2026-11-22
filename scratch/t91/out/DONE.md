DONE type=t91 status=complete

# t91 — 外源仓库 nottatdat/fm-data 对照(假设源,不升等级)

## 完成的三节

| 节 | 交付 | 状态 |
|---|---|---|
| §2 码表对拍 | `out/code_coverage.json` | complete |
| §3 空日期探针 | `out/nulldate_probe.json` | complete |
| §4 文法印证 | `out/hypotheses.md`(H1–H8) | complete |

## 交付清单

- `scratch/t91/out/code_coverage.json` — 三清单 + 计数 + 18 码逐条台账 + 表标签对照
- `scratch/t91/out/nulldate_probe.json` — 15 表×双档逐槽位命中率、对照常量、`(doy,year)` 文法校验、people 家族扫描
- `scratch/t91/out/hypotheses.md` — 8 条(外源主张/我们现状/一致性/需补验证)
- `scratch/t91/out/verify.py` — 独立复算 45 项,ALL PASSED
- `scratch/t91/out/REPORT.md`
- `scripts/t91_codes.py` — §2 生成器(`--help`/`--selftest`,rc 0)
- `scripts/t91_nulldate.py` — §3 生成器(`--help`/`--selftest`,rc 0)

## 核心数字

- 码表:我们 3009 码 / 395 标签 / pers 271;外源可恢复 18 码(其 2103 的 0.86%)
  → ①无法逐条枚举 ②**0 缺失** ③**7 条冲突**(4 标签 + 3 表域),`natc` 在我们侧不存在
- 空日期 `0x076c0001`:命中槽位 `client_21+13` / `server_21+156` = **100%**;
  对照常量 `0x076c0002` = **0 命中**;非 sentinel 行 `(doy,year)` 文法通过率 95.6%–100%
- 唯一确定差异:**容器头**——外源 12B(`a0 0f 90 0e 07 00` + zstd@12)vs 我们 8B(zstd@8)

## 纪律遵守

- 外源代码**零执行**(只读 md/py 源码与 JSON)
- 只写 `scratch/t91/out/` 与 `scripts/t91_*.py`;未碰 `scratch/ext/`、`reports/`、LEDGER、其他 tNN
- 全部外源标签标 `provenance=ext/fm-data@d7a7150`
- **零新增分级**,既有 club 78 / comp 49 / nation 30 L3 全部未动
- `scripts/t01_anchors.py` 7/7 PASS

## 未解项(未静默放弃)

1. 外源 `field_dict.csv` 不在克隆内 → 清单①无法逐条枚举
2. `natc` ↔ `nati` 同一性需外源原件裁决
3. H1 的 `ff ff ff ff 00` 五字节前缀在 row+37 前 5 字节未验证
4. H4/H5 复用路径(people 域 / club 按 nation 分组)属新假设,未启动
5. `server_21` row+37 的 108 行(1.06%)文法反例未解释,原样保留
