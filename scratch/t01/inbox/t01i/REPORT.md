# t01-i：pers / BASIC_PERSON 行偏移侦察

## 结论

**目标输入不存在：安装版 `client_db.dat` 的 FMF 目录没有 `client_db/table_1.dat`。** 因此无法从指定 payload 恢复 count、行起、stride，也不能把 `BASIC_PERSON` reader 的宽度序列映射到行偏移。任务书所列 27 条指令数不是 27 个已命名字段。验收未通过：命名行字段 0，五行抽验未做；这不是负载/偏移结论。

同一安装库的 `server_db.dat` 也没有数值 table 1；这是额外排除，不可替代 client 输入。`basic_people_db.dat` 确实是独立的 `tad.` + Zstd 文件，但本任务未证明它与该 reader 对应，故只记为待验证候选，不作真实映射结论。

## 证据

- 只读解析原始 `client_db.dat`（SHA-256 `5ce7cd91da1031436a55ad47dac04bac446cb0cad807e9c9b24f4885d9b5ecc1`）：外层 `file+0x0: 03 01 74 61 64 2e f1 0d`；FMF 目录帧在 `file+0xc81799: 02 01 66 6d 66 2e 08 00 00 28 b5 2f fd`，完整解压目录 1,954 B/31 项，20 个严格命名数值表，ID 列见 `output.json`，不含 1。不存在项由完整目录枚举证明，不伪造一段“缺失字节”。正对照 `table_25.dat` 压缩成员在 archive `file+0x4bc277: 28 b5 2f fd`。原始 `server_db.dat`（SHA-256 `99eed00bd26582648c0d3ff51b5c8e37a35b68c296a074e8fb476d1b3ca4a662`）TOC 在 `file+0x36d7c94`（同样以 `02 01 66 6d 66 2e 08 00 00 28 b5 2f fd` 开头），解析 77 项/59 张数值表，亦无 1；其 table25 压缩成员位于 `file+0x7f27b9: 28 b5 2f fd`。
- 对冻结快照 `evidence/fm24/reports/dbdat_decode/client_db_directory.json` 的 SHA-256 `90182a76d76674b52d06b79f15df0d6949ac1d4cd6a482170369fc3995a5e48b` 与 `evidence/MANIFEST.json` 相符；快照同样没有 table 1。快照只作交叉核对，主判断来自当前原始只读 archive。
- 误判负对照：严格 `_table_id` 不把 `name_table_1.dat` 当 numeric table 1；client `table_25.dat` 解压正对照头为 `03 01 74 61 64 2e f1 0d`、count=7,047、payload=894,991 B，且不会被当作 table 1。合成精确名 `table_1.dat` 可被目录检测器识别。
- 静态一侧直接复用 t01h 已核查锚点，并由本交付脚本复核关键字节：type-1 跳表项 `editor.exe+0xf49d3c: da ef ff ff`；112 B 分配 wrapper `+0x3bcd6fc: ba 70 00 00 00`；RTTI `.?AVBASIC_PERSON@db@@` 在 `+0x1aac700`；slot-19 reader 指针 `+0x187b3c0: 70 fd e4 40 01 00 00 00`，入口 `+0xe4f370`。首条宽度指令 `+0xe4f393: 41 b8 01 00 00 00`。exe SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。

## 结论边界 / 后续

factory type-id 1 与 numeric table ID 1 未被证明相等；RTTI 和 reader 存在只说明程序有此记录类，不说明它来自此编号表。虽有独立文件 `basic_people_db.dat`（12,934,775 B；头 `03 01 74 61 64 2e f1 0d 28 b5`），本次未恢复其记录框架，也未做字段或身份 join，所以不称它为已证明的 BASIC_PERSON 行来源。没有获得可提供的 row 偏移、getter 三元组或 5 行验证。

未启动游戏、编辑器或 IDA；未安装依赖；输入只读；L4=0。`verify.py` 不写文件，`--selftest` 验证 raw archive 目录、冻结快照哈希、静态锚点和正/负对照：

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01i/verify.py --help
py -V:3.12 -I -B scratch/t01/inbox/t01i/verify.py --selftest
```
