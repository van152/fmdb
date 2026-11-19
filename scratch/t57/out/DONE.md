# t57 交付

状态：**双档行框 / 已观测外层站点闭合；字段命名 partial。**

- Client / server 各 84,259/84,259 行；identity 非零、严格递增、唯一。12 B 是真正的 identity transfer；旧 13 B 尾把下一条 selector 当作自身末字节，首反例 ordinal 69705。
- 34 个逻辑位置；client 每行 14 个事件，server 普通 32、derived 31。433 个顶层 occurrence：18 项槽位对齐，72 对 XML 顺序倒置，13 L3 / 11 held / 10 独立成员父项跳过 / 399 unmapped。新增 L3：`Cext`、`Cedp`、`Cncl`、`CIns`、`Ctsi`。L4=0。
- 留项：`Cnam/Csnm/PLgn/Cprs/Cdof` 的投影或域限制；未证成的 `Csti`、Club 经纬度、成立年、直接 competition 及 reputation 主行槽；未出现的 tag-1 / 旧版路径。保留所有相关旧负例和本轮首反例。
- Python 3.12 隔离运行：builder、独立 verifier（3,443 条指令 / 407 条条件）、两者 `--help` / `--selftest` 均退出 0；`t01_anchors.py` **7/7**。Liverpool、Bernabéu、成立年等用于回归，不误报成 Club 主行直接字段。未修改 t39/t44/v6 等既有产物。

## 清单

- `scratch/t57/out/field_slots.json`
- `scratch/t57/out/field_map.json`
- `scratch/t57/out/instructions.part001.json` … `instructions.part009.json`
- `scratch/t57/out/branches.part001.json` … `branches.part003.json`
- `scratch/t57/out/verify.py`
- `scratch/t57/out/REPORT.md`
- `scratch/t57/out/DONE.md`
- `scripts/t57_clubmain_fields.py`
