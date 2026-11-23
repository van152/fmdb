DONE type=t76c status=complete

# t76c 完成

四张表 × 双档 = 8 个 (archive,table) 全部 `status=closed`,行框 100% 复现 t74 权威,
槽位映射按 L2/L3/candidate/unassigned/unmapped 五级交付。

## 判据达成

| 判据 | 结果 |
|---|---|
| 8 个 (archive,table) 全闭合 | 8/8,footer/count/identity 三项与 `scratch/t74/out/frames.json` 逐项相符 |
| agreement 冒烟先行 | 先做,双档 100B 闭合,产出纯负结果(见下) |
| 独立 verify.py(不 import builder) | `scratch/t76c/out/verify.py`,**197 passed / 0 failed** |
| ≥5 槽位对拍 | 远超:derby 11 槽、weather 每块 4 组 ×4 块、lcrg 5 组、agreement 2 槽,全部逐槽复算 |
| 小表全量 | agreement 6 行、derby 1,567 行、weather 334 行、lcrg 2,488 行 —— 全部全量,无抽样 |
| 不修改 t73 文件 | 未改;`runpy.run_path` 取 `t73_mapper_core.load_payload` 纯函数 |
| t01_anchors.py | **7/7 passed**(未回归) |

## 两条新立结构性 L2

1. **derby 双档 6 字节差 = schema 里恰好 3 个缺 `is_client_field` 的字段**
   (`D1tw/D1td/D1tl`,3×u16,903 行全 null / 664 行全非空 / **0 行部分 null**)。
   结构对齐,不依赖值域猜测。组内顺序仍 candidate。
2. **weather 95B 中段 = 3 + 4×23**
   由「全中段唯一 `{0,100}` 列恰在 `3+23b+22` 且逐行一致」钉死;竞争假设
   `3+4×22+4` 的组闭合率 1519 → 583(满分 4008),已否证并写入 verify 复算。

## 关键校准

引用槽存**稠密序数**而非 UID —— 用与本任务无关的 stadium `Scti@3`→city(100% <56,293)
与 city `Cwea@14`→weather(100% <334) 独立重推。
同时据此拒绝了 `Dfma@20` 的空洞拟合(出席人数上限 82,100 “落在” club 序数域内纯属巧合,
JSON 内标 `"vacuous": true`)。

## 负结果(原文保留)

- **agreement**:一行**恰好只有** 13B 身份三元组,`14+6×13+8=100` 吃满 payload。
  6 个业务字段(`NDBC/FDBC/dbnm/AGna/AGsn/Anti`)在本表 payload 内**不存在**,
  标 `unmapped`,不伪造偏移。
- **lcrg `Llgl`**:非空 712 值,对 language(126) 只命中 537/712 → **不是** language UID 集;
  对 weather(334) 却 100% 命中且顶值 333。紧致但指向错表 → candidate,不写结论。

## 未定项(数据侧边界,非遗漏)

- 组内顺序(`p0..p4`/`w0..w4`/`te..t7`/`Dfg1,Dfg2`/`Dwdr,Dntr`/`D1tw,D1td,D1tl`)
- weather `w{b}dn`:按排除法指派(23B 装 22 字段),但值集仅 `{0,1}`,不符 0..50
- weather `+22` 行级 `{0,100}` 列:20 行全为干旱/热带气候区,weather.xml 无对应字段

`escalate_to_sol` = 0。

## 产物

```
scratch/t76c/out/slots_client_18.json   slots_server_18.json
scratch/t76c/out/slots_client_27.json   slots_server_27.json
scratch/t76c/out/slots_client_47.json   slots_server_47.json
scratch/t76c/out/slots_client_56.json   slots_server_56.json
scratch/t76c/out/verify.py    scratch/t76c/out/REPORT.md   scratch/t76c/out/DONE.md
scripts/t76c_slots.py
```

## 复现

```
py -V:3.12 -I -B scripts/t76c_slots.py --selftest          # 22 checks
py -V:3.12 -I -B scripts/t76c_slots.py --calibrate
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t76c_slots.py --all
py -V:3.12 -I -B scratch/t76c/out/verify.py --selftest
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t76c/out/verify.py
```
