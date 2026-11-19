# t39 完成

- **Cursor 闭合**：server table 34，`13 + 7115×44 + 9 = 313082`；client 无该表。Mode 1 通过，mode 0 全表反证。E66 的 12 B 首 magic 帧已定位到前一目录项 `non_player_bans.dat`；按 `entry.size` 选出真正 table 34 帧。
- **字段部分晋级**：7/9 表级 L3（`tchc/mstn/sstn/dbrt/posi/cquf/tcop`），`styr/edyr` 因必填年份零值与冻结 XML 域冲突 held，首反例已留。Club/nation 共用编辑分发；7,084 非空 owner 全指 table 24 `NATIONAL_TEAM` selector，无 club 独占 L3，L4=0。
- **复验**：builder、独立 verifier 及两者 `--help` / `--selftest` 均通过；`t01_anchors.py` 7/7。消费 t29 profile/rows，并比较 t37 profile；指定 t33 table34 文件在本 checkout 不存在。

## 交付清单

- `scratch/t39/out/cursor_tchl.json`
- `scratch/t39/out/fields_tchl.json`
- `scratch/t39/out/instructions.part001.json`–`instructions.part008.json`
- `scratch/t39/out/branches.part001.json`–`branches.part002.json`
- `scratch/t39/out/verify.py`
- `scratch/t39/out/REPORT.md`
- `scratch/t39/out/DONE.md`
- `scripts/t39_tchl_cursor.py`
