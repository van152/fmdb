# t34 交付 — CNtp / table 66

- **Cursor 闭合**：server 753 × 24 B；client 目录无成员。`13 + 753 × 24 + 9 = 18094`，reader + identity tail 静态路径可复验。
- **字段**：`nati`、`rati` 晋级 L3。`mina`、`maxa` 已绑定静态 sink，但因 required 年龄域的零值冲突仍 held；首个原始顺序反例是 row 57 `(18,0)`。L4=0。
- **复验**：builder、独立 verifier、两者 `--help` 与 `--selftest` 均 PASS；`t01_anchors.py` 7/7 PASS。

交付清单（本目录除特别标出外）：

- `cursor_cntp.json`、`fields_cntp.json`
- `instructions.part001.json` – `instructions.part005.json`
- `branches.part001.json`、`branches.part002.json`
- `verify.py`、`REPORT.md`、`DONE.md`
- `scripts/t34_cntp_cursor.py`（仓库根相对路径）
