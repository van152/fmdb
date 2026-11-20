# t68 — Club table_3 数据侧交叉验证(t50 范式迁移;L2)

**指挥官注记**:worker 两次被环境 SIGTERM(07:22、08:09,rc=143,非超时、非额度);核心交付(crosswalk.json / sensitivity.json / verify.py)在第二次中断前已完整落盘,`verify.py --check` 独立复核 PASS。按 E88 先例由指挥官补写本报告与 DONE;以下数字全部取自 worker 已落盘交付物,未做内容改写。

## 结论(status: complete_data_side_crosswalk;L2 目标,L3=0,L4=0)

- **双档封口复现**:rows 字节 client 6,932,060 / server 16,595,290,+13 header+9 footer = 6,932,082 / 16,595,312 —— 与 t57(E97)reader 侧封口**逐字节一致**。
- **DP 单路**:标准约束(ordinal 0..84,258、UID 非零严格递增、identity triple UID lane 重复)下四对齐扫描+分层非重叠全铺各得一路;两侧 31 项敏感性对照全落 sensitivity.json。
- **identity 跨档同值**:UID 集 SHA-256 client==server(84,259 个),identity bytes 相等,footer e3c03a77 相等。
- **selector 平铺**:双档直方图 `{0: 84,256, 12: 3}` —— 与 t57 CLUB identity selector_counts **完全一致**(12 是 COMP 风格 selector 在 club 的罕见出现,t57 已记 3 例)。
- **行宽**:client 54–156 B、server 81–2,618 B,server−client 全部为正(84,259 行)。
- **夹具**:Liverpool ordinal 460/UID 676/nation 139/city 1061;Bernabéu stadium 430/UID 1056/81,044(引自 t57 regression 记录复核)。
- execution_templates client 2/server 多模板,序列与 t57 field_slots 对照记录在 crosswalk.json。

## 边界

- 只 table_3;不改 reports/、不碰 t57 交付物;negative/对照留在 sensitivity.json,不晋升。
- 未启动游戏/编辑器/IDA,未联网,未读写 Z:。

## 复现

```text
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scripts/t68_club_data_crosswalk.py --build
FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data py -V:3.12 -I -B scratch/t68/out/verify.py --check
py -V:3.12 -I -B scripts/t01_anchors.py
```
