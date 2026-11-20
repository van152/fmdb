# t21b 任务书:club reader helper/control-flow follow-up

先读 `AGENTS.md`。这是 t21 的接力任务，不能覆盖或改写已有 `scratch/t21/out/audit.json`、`REPORT.md`、`verify.py`；只能新增 `scratch/t21/out/control_flow.json`、`control_flow.md`，以及必要时新增 `scripts/t21_*.py`。

## 已确认基线

- `scratch/t21/out/audit.json`：本地 `client_db.dat` table 3 全量 84,259 行走通，84,256 standard + compact ordinal 69706..69708，row end/footer `0x69c66a` 精确相等。
- 两个 RTTI reader 的静态引用字节已独立复核：`CLUB` entry `0xe5a7a0`，`LEAGUE_BODY_CLUB` thunk `0x157cff0` -> body `0x43beba0`；对应 t01h trace 的 width/stream/branch 引用全部通过。
- `row+0 == row+8` 只在 55,868/84,259 行成立；不能把 `Cccn@row+8` 晋级。ordinal 69705 附近不能未经证据当作 RTTI class selector。
- t19 已确认 club 行框架，但完整 41-call mixed reader 与 row cursor 未闭合。

## 唯一目标

只做静态控制流取证，回答：

1. `CLUB` reader `0xe5a7a0` 的 41 个 stream transfer 中，哪些在主线，哪些在条件块、循环或 direct helper 返回后；记录每个 transfer 的 file offset、width、RDX/object sink（若可追）、前置/后置分支和 helper target。
2. `LEAGUE_BODY_CLUB` reader `0x43beba0` 的 count-loop / helper 路径：定位循环计数来源、back-edge、每个 stream transfer 的实际执行路径；不要把 bulk/helper 的未知宽度猜成字段。
3. 查找是否存在能把 RTTI class 绑定到 `.dat` row ordinal / row bytes 的独立 discriminator。若没有，明确输出 negative，不能使用连续 ordinal split、marker、名称或相等 ID 猜 class。
4. 对 `Cccn` 做反证整理：现有 direct object_off、path_descend、row data 三者是否能闭合；不能闭合就保持 unpromoted。

## 方法和纪律

- 只读 `<OLD_REPO>\input\editor.exe`、`scratch/t21/out/audit.json`、t01h/t05/t12/t19 等证据；本地数据路径用 `FM24_DB_DIR=<WORKSPACE>/scratch/data`。
- PE file offset/RVA/VA 必须使用 `scripts/t05_pe.py`，不能套固定 delta。
- 指令必须保存原始 bytes、file offset、VA、反汇编文本；helper target 用 PE 映射后再分析。
- 控制流分析优先 CFG/basic-block 路径；线性扫描只能标为候选，不能冒充 executed cursor。
- 不启动游戏、编辑器、IDA，不联网，不读写 Z:；不碰旧 t02 未提交日志。
- 输出状态用 `partial_control_flow_*` 或 `negative_*`；没有新行坐标就明确写 0。
- 单次输出 ≤400 行；大列表 JSON 分片或 compact records。
- 新脚本必须支持 `--help`、`--selftest`，退出码 0/1/2。

## 交付

1. `scratch/t21/out/control_flow.json`：两个 class 的 CFG/transfer/helper/branch 证据和负结果。
2. `scratch/t21/out/control_flow.md`：结论、证据等级、未闭合项、反证记录。
3. 必要的 `scripts/t21_*.py`。

完成后先运行新脚本 `--help`、`--selftest`，再运行 `py -V:3.12 -I scratch/t21/out/verify.py --selftest` 与默认验收；不要宣称 t21 complete，除非完整 cursor 和 row class discriminator 都被独立闭合。
