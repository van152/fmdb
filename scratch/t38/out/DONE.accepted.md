# DONE — t38 多帧感知 payload 加载器

**状态**: 完成,`--selftest` 25/25 PASS,`verify.py` 34/34 PASS,`t01_anchors.py` 7/7。

## 交付清单

| 文件 | 说明 |
|---|---|
| `scripts/t38_multiframe.py` | 加载器主体:`load_payload_mf` / `inspect_entry` / `e77_repro` / `--selftest` / `--scan` / `--dump` |
| `scripts/t38_build.py` | 生成 `multiframe_report.json` 的机读证据 |
| `scratch/t38/out/multiframe_report.json` | 460 条目帧结构全集 + 五锚点选帧证据 + 回归表 + E77 归因 |
| `scratch/t38/out/REPORT.md` | 结论、判据、差异表、E77 复现 |
| `scratch/t38/out/verify.py` | 独立复算(不 import 加载器) |
| `scratch/t38/out/DONE.md` | 本文件 |

## 验收对照

| 任务书要求 | 结果 |
|---|---|
| `load_payload_mf(codec, archive, tid)` | ✅ |
| `--selftest`: server34→313082 / client3→6932082 / server73→45 / server66→18094 / server43→24632 | ✅ 5/5,含 SHA |
| 单帧回归 t33 七表 + t29 若干 | ✅ 20/20 payload size+SHA |
| `--help`;退出码 0/1/2 | ✅ (无参数=2,校验失败=1) |
| 打印 ≤400 行 | ✅ selftest 输出 25 行 |
| 独立 verify.py,从 archive 复算 | ✅ 34/34,不 import 加载器 |
| 不改 `fm24_dump.py` | ✅ `git status` 无该文件改动 |
| 只写 `scratch/t38/out/` 与 `scripts/t38_*.py` | ✅ |

## 对任务书前提的修正(重要)

任务书/E77 假设「成员含多帧:空 stub 首帧 + 真实 payload 第二帧」。**460 个条目实测全部单帧**,唯一帧长度恒等于 `entry["size"]`。

真实成因:`fm24_dump.load_payload` **少加 FMF `data_base`(=34)**。E66 的 12B 是**前一个成员**(`non_player_bans.dat`,25B `tad.` 空 stub)的 payload,不是同一成员的 stub 帧。

判定式 `[前一成员 packed_size < data_base]` 在 460 条目上预测 == 实测,`symmetric_diff = 0`,命中 119 个条目(含 `lang_update` 117 个此前未暴露的)。

E77 报的 `BOUNDED 287410 eof=False` / `UNBOUNDED 313082` 已**完整复现**,但归因为坐标系差 34B(见 REPORT §4),非 `packed_size` 语义问题。

## 实现要点

* 成员起点 = `data_base + offset`;边界 = `packed_size`;选帧 = `len(frame) == size` 唯一命中。
* 两阶段边界:P1 `packed_size`(实测 460/460 足够)→ P2 `next_member_start`(仅在 P1 截断时),均不跨成员。
* `entry.sha256` 经 460/460 证实为**压缩区** SHA,用作成员定界自证。
* 无匹配帧 / 末成员截断 → `raise FrameError`,不回落首帧。

## 未做 / 边界

* 未改 `fm24_dump.py`(集成由指挥官决定;REPORT §7 给出最小修复点)。
* `data_base`=34 的结构含义**未做 L3 exe 静态确认**,仅作操作性事实使用(候选,不写结论)。
* 未启动游戏/编辑器/IDA,未联网,未读写 Z:。
