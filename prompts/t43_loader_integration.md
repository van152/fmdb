# t43 — 把 t38 data_base 修复集成进 fm24_dump.load_payload(最小改动 + 全回归)

你是受指挥官委派的子代理。t38 已证实(E80):`fm24_dump.load_payload` 漏加 FMF `data_base`(=34),致 119 条目误读前一成员 stub(含 server34 取 12B)。本任务把 **最小修复集成进共享加载器**,严格回归,不破坏已接受任务。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- scripts/fm24_dump.py(**待修目标,仅 load_payload 函数**;现 line 86-96)
- scripts/t38_multiframe.py(load_payload_mf 参考实现,member_bounds/decode_frames)+ scratch/t38/out/REPORT.md §7(最小修复点)
- <OLD_REPO>\scripts\modding_read_dbdat.py(codec:`_archive_layout(data)`→{data_base,...}、`_read_archive`、`_entry_summary`、`list_tables`、`_resolve_table`;entry.offset **相对 data_base**)

## 已知事实(E80,460/460 实证)
- 成员绝对起点 = `data_base + entry["offset"]`;边界 = `packed_size`;**460 条目全单帧**,唯一帧 len==entry["size"]。
- `entry["sha256"]` = 压缩区 SHA(非解压 payload SHA)。
- data_base 三 archive 均 34,但**须从 codec `_archive_layout(db)["data_base"]` 动态取,不硬编码**。
- 旧法从 entry.offset 扫 64B 首 MAGIC:前一成员 packed_size<34 时误中其 stub;≥34 时首帧恰正确(缺陷被掩盖)。

## 任务
1. 修 `load_payload(codec, archive, tid)`:用 `codec["_archive_layout"](db)["data_base"]` 取 base;成员区 `db[base+off : base+off+packed_size]`;在区内找 MAGIC 解压,**以 len==entry["size"] 选帧**(单帧即唯一);无匹配 raise RuntimeError(不回落首帧、不静默截断)。保持函数签名/返回 bytes 不变。
2. 不动 fm24_dump.py 其它函数(walk_*/dump/selftest/OVERRIDE/FIELDS 等);不引入对 t38 脚本的 import 依赖(独立实现,可参考逻辑)。
3. **全回归**(必须全绿才算完成):
   - `py -V:3.12 -I -B scripts/fm24_dump.py --selftest`:server34 由 SKIP→PASS,定长 PASS 数不减(原 49/0/1SKIP→预期 50/0/0SKIP 或更多),无新 FAIL。
   - `scripts/t01_anchors.py` 7/7。
   - `scripts/t38_multiframe.py --selftest` 25/0(参考加载器不受影响)。
   - 单帧回归:对 ≥20 表(含 t33 七表 + server34/66/43 + client0/2/3)比对修复后 load_payload 与 load_payload_mf 字节全等。
   - 已接受任务 spot 复跑不回归:scratch/cmd/t39_spot.py(26/26)、t34_spot.py、t36_spot.py(若用 load_payload 则验仍 PASS;用自有 pick_frame 者注明不受影响)。
4. 修前后对 119 受影响条目抽样(含 lang_update)验证修复后 len==size、SHA 正确;保留修复前负例(12B stub)作对照,不删。

## 边界
- 只改 scripts/fm24_dump.py 的 load_payload + 写 scratch/t43/;不碰其它 scripts/任务产物。
- data_base=34 结构含义仍候选(未 L3 exe 确认),集成是操作性修复,不写结构结论;L4=0。
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 回归任一不绿→诚实 partial + 首反例,不强行宣布完成。

## 交付 scratch/t43/out/
- integration_report.json(修前后对照/119 抽样/回归矩阵)、verify.py(独立不 import fm24_dump,从 archive 复算修复后 load_payload 应得 payload)、REPORT.md、DONE.md
- Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑上述全回归 + t01_anchors.py(7/7)。