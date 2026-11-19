# t41 交接 — Csme / table 59

- **Cursor 完成**：server 9,079/9,079 行；`13 + 6567×22 + 2512×32 + 9 = 224880`；client 目录无成员。属性 vector 的 u32 count 决定变长，caller mode 0/1 都闭合。
- **字段 1/2 晋级**：`Melf` 的条件坐标 L3；`Msid` 的双 lane sink 静态绑定，但没有任何 live 引用，held。Club 独占 L3=0；L4=0。
- **保留首反例**：t33 row 0 的 `19 B` 假尾及 row 1 的 `25 B` 补偿；真实是 `22+22`。Club 独占：row 0 owner → Team ordinal 0 / selector 11。原 t33 产物未改。

## 交付清单

- `scratch/t41/out/cursor_csme.json`
- `scratch/t41/out/fields_csme.json`
- `scratch/t41/out/instructions.part001.json` … `instructions.part008.json`
- `scratch/t41/out/branches.part001.json` … `branches.part002.json`
- `scratch/t41/out/verify.py`
- `scratch/t41/out/REPORT.md`
- `scratch/t41/out/DONE.md`
- `scripts/t41_csme_cursor.py`

## 复验

环境 `FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`：

```text
py -V:3.12 -I -B scripts/t41_csme_cursor.py
py -V:3.12 -I -B scratch/t41/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```

Builder、独立 verifier、两者 `--help` / `--selftest` 均 PASS；anchors **7/7 PASS**。未启动游戏、编辑器或 IDA，未联网或访问 Z:。未修改公共 loader、其他任务产物或全局台账。
