# t158 — L4 真机加载验证预备包与自动化预检套件（`scripts/t158_l4_prep_kit.py`）

## 重要工程约束（避免单次输出超限）
- 本模型单次输出上限约 8K tokens，**单次 `write`/`edit` 严格控制在 150 行以内**，分步构建并测试。
- 直接 `import` 复用 `fm24_config`、`t140_fm24_roundtrip`、`t155_history_roundtrip` 等已有引擎。

## 背景与目标
目前项目已通过 L3（Unicorn 仿真 `editor.exe` 机器码回读），但尚未在真实 FM24 游戏本体内做最终 L4 真机加载验收（见 `AGENTS.md` 阶段四）。
你的目标是编写 `scripts/t158_l4_prep_kit.py`，在 `${OUTDIR}/l4_staging/` 下自动构建一套**可安全用于真机加载验证的最小化外科手术补丁包**（绝对不改动原游戏目录或 `scratch/data`）：
1. 生成修改后的 `server_db.dat` / `client_db.dat`（复用 `t140` 变长改名/实体修改）与 `pl_hist_*`（复用 `t155` 履历微调），给出清晰、肉眼可辨的 3–5 处 UI 核对锚点（原值 vs 改后值）；
2. 自动执行全套 L3 预检（容器校验、纯 Python 全表无损回读、SHA-256 差异清单、字节偏移对照）；
3. 生成 `${OUTDIR}/L4_CHECKLIST.md`，列出用户真机启动 FM24 / FM24 Editor 加载测试的精确步骤、核对项与一键回滚方案（明确标注当前仍为 `L4=0` 预备态，不虚报已过 L4）。

## 纪律与边界
- 严禁启动游戏/编辑器进程，严禁修改 `Z:\`、原 `scratch/data`、`reports/`、`scratch/t01/LEDGER.json`。
- 路径统一使用 `import fm24_config`，通过 `check_repo.py`。

## 交付物
1. `scripts/t158_l4_prep_kit.py`（`--help`、`--build`、`--selftest` 全过）
2. `${OUTDIR}/l4_prep_manifest.json`（含 `"status": "complete"`、`"L4": 0`、文件 SHA-256 清单、锚点对照表、预检结果）
3. `${OUTDIR}/L4_CHECKLIST.md`、`${OUTDIR}/REPORT.md`、`${OUTDIR}/DONE.md`（首行含 `DONE type=l4_prep_kit`）
