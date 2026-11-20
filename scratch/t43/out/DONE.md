# DONE — t43 把 t38 `data_base` 修复集成进 `fm24_dump.load_payload`

**状态**: 完成(全回归全绿)。`fm24_dump --selftest` **50/0/0**,独立 `verify.py` **19/0**,`t01_anchors` **7/7**。

---

## 交付清单

| 文件 | 说明 |
|---|---|
| `scripts/fm24_dump.py` | **唯一被改文件**:仅 `load_payload` 函数(+40/−5;AST 逐节点确认其余函数/常量零变化) |
| `scratch/t43/out/integration_report.json` | 修前后对照(25 表)/ 119 条目抽样(逐条入档)/ 回归矩阵 / t38 计数受控实验 / 证据等级 |
| `scratch/t43/out/verify.py` | 独立复算:不 import `fm24_dump`(子进程调用),自解析 FMF 头+目录,19 检查项 |
| `scratch/t43/out/verify_result.json` | `verify.py --json` 明细(含 119 条逐条记录 + 42 条 12B 巧合条目) |
| `scratch/t43/out/REPORT.md` | 结论 / 最小修复点 / 修前后对照 / 119 分析 / 回归矩阵 / 方法论发现 |
| `scratch/t43/out/DONE.md` | 本文件 |
| `scratch/t43/build.py` | 证据生成器(允许 import fm24_dump / t38 做对照;产品代码无此依赖) |
| `scratch/t43/build.log` | 最后一次 `--build` 的完整输出 |

---

## 验收对照

| 任务书要求 | 结果 |
|---|---|
| 用 `codec["_archive_layout"](db)["data_base"]` 动态取 base | ✅ `verify.py` 用 AST 检查 `load_payload` 代码体无 `\b34\b` 字面量 |
| 成员区 `db[base+off : base+off+packed_size]` | ✅ 区内逐帧解压,`not eof`/无进展即停,不越界 |
| 以 `len == entry["size"]` 选帧 | ✅ 单帧即唯一;25 表与 `load_payload_mf` 逐字节全等 |
| 无匹配 → `RuntimeError`(不回落首帧/不静默截断) | ✅ 错误消息带成员区间与期望长度 |
| 签名/返回类型不变 | ✅ `load_payload(codec, archive: str, tid: int) -> bytes` |
| 不动其它函数、不 import t38 | ✅ AST 比对:changed 集合 = `['load_payload']` |
| `fm24_dump --selftest` 49/0/1SKIP → 50/0/0SKIP | ✅ **50 PASS / 0 FAIL / 0 SKIP**,server34 SKIP→PASS,无新 FAIL |
| `t01_anchors.py` 7/7 | ✅ 7/7 |
| `t38 --selftest` 不回归 | ✅ 0 FAIL(HEAD 版 24 PASS,见下);25→24 是 **DIFF 提示行消失**的正向证据 |
| 单帧回归 ≥20 表 vs `load_payload_mf` | ✅ **25 表 25/25 字节全等**(含 t33 七表、server34/66/43、client0/2/3) |
| `t39_spot` 26/26 | ✅ 26/26(自有 `pick_frame`,不受影响) |
| `t34_spot` / `t36_spot` 不回归 | ✅ 13/13 · 9/9(均用 `load_payload`,server#66 / #33) |
| 119 条目抽样 len==size / SHA 正确 | ✅ 119/119 `len==size`、单帧、`leftover==0`、packed 区 SHA 自证 |
| 保留修复前负例(12B stub) | ✅ `negative server#34 legacy = 12B (delta −25B)` 固定为检查项,不删 |
| 只写 `scratch/t43/` + 只改 `load_payload` | ✅ `git status` 中本任务只涉及这两个路径 |

---

## 关键数字

```
server#34   修复前 12 B (600175712b2f…, 前一成员 25B stub, −25B)
            修复后 313082 B (a07b2bb76fb8796b…)  == t38/t29 已落盘值

fm24_dump --selftest   49 PASS/0 FAIL/1 SKIP  →  50 PASS/0 FAIL/0 SKIP
单帧 25 表 vs mf        25 byte-identical / 0 divergent / 0 raised
119 受影响条目          server 2 + client 0 + lang_update 117 = 119
                        修复后 119/119 len==size,单帧,leftover==0,packed-SHA 自证
                        旧法坐标 119/119 错(−25B);旧法字节 77/119 不同
t01_anchors 7/7 · t39 26/26 · t34 13/13 · t36 9/9 · t43 verify 19/0
```

---

## 方法论发现(需传递给后续任务)

**42 个 `lang_update` 条目上,"取错成员"在字节层面不可见。**
这 42 个条目自身 `size == 12`,而前一成员的 stub payload 恰好是同一个 12B 模板(`600175712b2f…`),
所以修复前后 payload 长度与 SHA **完全一致**。

⇒ 任何以「payload 长度」或「payload SHA」做自检的加载器,在这些条目上都是**假阳**。
唯一可靠的自证是**成员边界**:起点必须 `data_base + offset`,且
`sha256(db[start:start+packed_size]) == entry["sha256"]`(该字段是压缩区 SHA,不是 payload SHA)。

---

## 诚实记录

1. **t38 计数 25 → 24**:不是回归。`run_selftest` 计分是 `len(lines)-len(fails)`,信息行也算一行;
   修复前有 1 条 `DIFF[EXPECTED(E66-family)] server#34: legacy=12B vs mf=313082B`,修复后消失。
   `build.py` 用**同一份 HEAD 版 t38 脚本**做了受控实验:旧实现 → 25 PASS/1 DIFF;新实现 → 24 PASS/0 DIFF;FAIL 恒 0。
2. **工作区外部改动**:本任务执行期间 `scripts/t38_multiframe.py` 被另一会话追加了 145 行
   (无界选帧对照 check #10/#11),现场因此跑出 32 PASS。该文件不在本任务改动范围,本次未触碰;
   `integration_report.json` 同时记录 HEAD 版与工作区版结果,不择一粉饰。
3. **`data_base`=34 的结构含义仍是候选**:未做 L3 exe 静态确认,本次仅作操作性偏移使用,不写结构结论。**L4 = 0**。

---

## 复现

```bash
export FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/fm24_dump.py --selftest          # 50 PASS / 0 FAIL / 0 SKIP
py -V:3.12 -I -B scripts/t01_anchors.py                   # 7/7
py -V:3.12 -I -B scripts/t38_multiframe.py --selftest     # 0 FAIL
py -V:3.12 -I -B scratch/cmd/t39_spot.py                  # 26/26
py -V:3.12 -I -B scratch/cmd/t34_spot.py                  # 13/13
py -V:3.12 -I -B scratch/cmd/t36_spot.py                  # 9/9
py -V:3.12 -I -B scratch/t43/out/verify.py --selftest     # 19 PASS / 0 FAIL
py -V:3.12 -I -B scratch/t43/build.py --build             # 重建 integration_report.json
```
