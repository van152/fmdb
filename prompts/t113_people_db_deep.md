# t113 — 攻克全库最大文件 `people_db.dat` (67.5 MB)：`PERSON` / `PLAYER` / `NON_PLAYER` / `OFFICIAL` 虚表与 IDA 反编译

> 交付目录：`OUTDIR`（`scratch/t113/out`）
> 脚本路径：`scripts/t113_people_db_ida.py`（Python 3.12 `-I -B`，须含 `--help` 和 `--selftest`，退出码 0/1/2）
> 输入源（只读）：`D:\tmp2b\fm24\input\editor.exe`、`scratch/t95/editor_work.i64`（只读引用或仅在只读方式打开，**注意不要同时与其它 IDA 进程写同一 i64**，建议复制临时份或用 `editor.exe -a-`）、`scratch/data/people_db.dat` (67.5 MB)、`scratch/data/basic_people_db.dat` (12.9 MB)、`scripts/t38_multiframe.py`、`scratch/t95/funcs/140e4fd70.c` (`BASIC_PERSON::slot19`)。
> 不要修改 `reports/` 或 `LEDGER.json`。

## 背景
`people_db.dat` (67.5 MB) 是整个 FM24 数据库体积最大的归档，承载全部球员（`PLAYER`）、教练/职员（`NON_PLAYER`）、裁判（`OFFICIAL`）、记者（`JOURNALIST`）、人物基类（`PERSON`）与球员属性块（`PLAYER_DATA` / `PDxx`）。此前因旧文档限制从未系统逆向！
现在 IDA Pro 9.4 `idalib` + Hex-Rays x64（见 `scripts/t95_ida_vtables.py`）和 Unicorn 均已完全可用！

## 任务目标
1. **RTTI 全量扫描 `PERSON` 继承体系全部虚表**：
   - 在 `editor.exe` 中通过 MSVC x64 RTTI 扫描与 `BASIC_PERSON` / `PERSON` / `PLAYER` / `NON_PLAYER` / `OFFICIAL` / `JOURNALIST` / `HUMAN` / `PLAYER_DATA` / `NON_PLAYER_DATA` / `CONTRACT` / `SPOKESPERSON` 相关的全部 vtable VA 与类名。
   - 核对每个类的 `slot[2]` (`get_prop`)、`slot[3]` (`set_prop`)、`slot[19]` (`read_from_stream`)、`slot[20]`、`slot[21]` (`write`)。
2. **IDA 9.4 `idalib` + Hex-Rays 批量反编译**：
   - 复用 `scripts/t95_ida_vtables.py` 的 thunk 解析 + Hex-Rays 方法（输出目录 `scratch/t113/out/funcs/`，**不要写 `scratch/t95/editor_work.i64` 原文件**，用 `editor.exe -o scratch/t113/ida_tmp.i64 -a-` 或单独拷贝 `i64`），反编译上述全部人物子类的 `slot02`, `slot03`, `slot19`（含 1-hop thin wrapper）。
   - 抽取每个类的 4CC 列表（重点统计 `PLAYER` / `NON_PLAYER` / `PERSON` / `PLAYER_DATA` 各自覆盖了多少个 4CC！）。
3. **解包 `people_db.dat` (67.5 MB) 与 `basic_people_db.dat` (12.9 MB) 结构普查**：
   - 使用 `t38_multiframe.py` 列出这两个归档内的全部成员、压缩/解压大小、13B 头版本、行数与首 64 字节样本，并对照 `sub_140F49530` `case 1`（`sub_1410992C0(a2)` 按 `person_type` 字节分发子类构造！）验证 `people_db.dat` 每行首字节的 `person_type` 分布！

## 交付物（写入 `OUTDIR = scratch/t113/out`）
1. `people_vtables.json`：含 `"status": "complete"`，全部人物体系 RTTI 类名、vtable VA、核心虚函数 VA、反编译结果与 4CC 列表。
2. `people_archives_inventory.json`：`people_db.dat` 与 `basic_people_db.dat` 全成员清单 + `sub_1410992C0` 子类分发映射 + 真实行首字节类型分布。
3. `funcs/*.c`：全部人物子类的 Hex-Rays 反编译 C 源码。
4. `REPORT.md`：清晰架构图（人物类继承树、每类 4CC 数、`people_db.dat` 成员布局）。
5. `DONE.md`：含 `DONE type=t113` 与核心统计数字。
