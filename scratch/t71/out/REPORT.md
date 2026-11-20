# t71 — CLUB+0x100：定位 `table_extra_3.dat`，24 项转正 L3

**22 个 `cnst`、`Cebd`、`Cyfn` 全部转正。** `cnst` / `Cebd` 是 **server wire**，client 没有相应字节；`Cyfn` 在两档均有 wire。L4=0。不修改 t57/t63、公共 schema 或 LEDGER。

## 成员绑定：同一 CLUB 容器，两条读路

证据来自只读 `<OLD_REPO>/input/editor.exe`，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。下文地址均为 **PE file offset**；`chain.json` 记录对应 VA、原字节、分支和虚表格。Schema 和旧夹具均按 `evidence/MANIFEST.json` 核验；精确 4CC gate→helper→`movsx` 沿用 t63(E106)，未用 XML 顺序推 lane。

- **上下文自证**：`0xf0296b` 传 type `3`，`0xf02973 → 0xff9910 → 0x3ceb7d0` 的 `0x3ceb8e2` 保存到 context `+0x54`。`0xf02978/7f` 安装 vptr，其 COL/RTTI 命名为 `DATABASE_TABLE<CLUB>`；`0xf02a93` 把该 context 安装到数据库 `+0x10`。
- **主对象**：`0xf4d4db → 0xf4d519` 对该 context 选普通 `table_` 名；`0xf4d57f → 0xf2b350` 读主表。`0xf2b583` 调 `0xf48b30`，case 3 的 `0xf49d44` 格指向 `0xf48daf`；普通和 selector 12 均调 `0xe59a40` 构造 CLUB。`0x3aad1a9` 将 `CLUB+0x100` 置空。主读器调用 `0xf2b5b1` 使用 vtable slot 19，普通 CLUB 为 `0xe5a7a0..0xe5bfca`；slot 2 为 `0xe89a00`（getter）。
- **辅助成员**：`0xf5164c/58 → 0xf54f00 → 0x3bb8b70` 取同一个数据库 `+0x10`。`0x3bb8bb2/bb5/bb8` 传 `extra=1, old_save=0` 给名称格式器 `0xffa3b0 → 0x3cefbe0`。`0x3cefca4/cb2` 的立即数拼成 `table_extra_`；`0x3cefc62` 取 context `+0x54`，整数转十进制，再由 `0x3cefd4e` 拼接；`0x3bb8b90` 取 `.dat`，`0x3bb8bf6` 开流。因此名称是 `table_extra_3.dat`，不是从成立年凑出的候选。两档 FMF 目录均有该精确条目，按声明压缩范围和解压长度唯一选帧。
- **既有对象 join**：`0x3bb8c28` 读 count u32，`0x3bb8c68` 每轮只读 **4 B ordinal**；快路 `0x3bb8cf8..d02` 取 context `+0x80` 的向量项，另有 context `+0x20` 的 remap 慢路及找不到目标时的 scratch 对象路径。`0x3bb8d0c → 0xe5d210` 将记录喂给既有 CLUB；`0xe5d250..29d` 缺额外对象才分配 `0x130` B、构造并存入 `CLUB+0x100`。组合流另有 `0xf2926d → 0x3b92ca0 → 0xe5d210`（mode 1），不是 split 名称的依据。
- **排除对照**：`club_links.dat` 由 `0xf2a395/3af → 0x1529210` 读到 `context+0x680`，t44 已证是 `CLUB+0x118/+0x120` 的 POD 向量；8 个普通编号子表是 `22/37/62/43/66/33/34/59`（Cstc/Clhs/CSrs/Cmti/CNtp/Cdbt/Tchl/Csme），走普通 `table_<type>` 命名与工厂分配，不是 existing-CLUB 辅助流。目录里 `name_table_{0,1,2}` 和 `name_table_extra_{0,1,2}` 有各自独立前缀，不能由此格式器产生。未重解这些成员。

## 行框：从前缀 ordinal 自证，不引入伪 UID

| 档 | 封口：header + rows + footer | 行数 | 单行宽度 | 首行范围 | 末行起点 |
|---|---|---:|---:|---|---:|
| client | `12 + 13,053,896 + 0 = 13,053,908` | 84,259 | 25–1,861 | `[12,307)` | 13,053,883 |
| server | `12 + 35,009,236 + 0 = 35,009,248` | 84,259 | 238–4,827 | `[12,602)` | 35,009,010 |

数据侧在四种对齐上枚举 ordinal，按 `0..84258` 分层做非重叠 DP；前缀签名不使用任何目标字段值、不按主表 UID 或跨档年份拣行。client 对照 `+6..9=ff ff ff ff`，再加 `+11/+13/+14/+15=0`，把 **5,280** 条弱路径收敛到 **1**；server 对照 `+6..9=00 00 00 01`，再检 `+19/+43=1`，强签名只有 ordinal 0 有多候选（6 个）；头锚 `@12` 留 **1** 路。即使最小非重叠宽度只取 identity 的 4 B，两档仍各 1 路。加入最短行约束后，header 11/13/14 均无路径；footer `1/2/4/7/8/9/10/12` 均在末 ordinal 84258 断开，footer 0 唯一。独立 verifier 用反向 DP 重建边界；正向 reader replay 不找下一 ordinal 修游标，逐行与 DP 边界和 EOF 一致。

`table_extra_3` 的 identity 只有 `ordinal:u32le`，不是 `ordinal|UID|UID`。把前缀 12 B 强当主表 triple 两档分别 **84,259/84,259** 不符；首条 `@12` 期待 UID 57，client dwords `(0,4294903707,65535)`／server `(0,1795,256)`，再附 1/2 B 也不能恢复 UID。真实 `table_3` triple 仅用作已冻结的 ordinal→UID 字典，双档 84,259 对齐、无重号或缺键。旧 b47/b50 的贪婪短跳、模板误命中和 20 个年份未命中的记录原文仍在快照；不把它们的边界猜测用作本轮证据。

## 游标与全档域

`0xe5d2b7/ba` 决定外部模式：0 跳过 server 扩展，直接到 `0xe5d338`；1 走扩展，最终 `0xe5ec24/2b` 汇回 `0xe5d342/388`，同样读 `extra+0xd8`。强制交换两档模式或使用旧版本短尾臂均无法封口，首反例在 `rows_extra3.json`。公开的 `0x3511e/0x352cd` split caller 均传 1；client 的 mode 0 是**档数据与静态分支的闭合结论**，不是声称观察到编辑器实际走了 mode 0。

设 `r` 为 extra 成员内的行首绝对偏移。server 现代闭合前缀中，扩展 `+0x18` count 全 0、第二组日期 flag 全 1、`+0xf8/+0x10c` 版本均 3。`E=u8[r+83]` 是 election 存在位（0/1），出现则多 19 B。A/B 定位如下：

- `A = r+132+19E`：`0xe5de44 → 0x151d2e0 → 0x4339e80` 到 `extra+0xe0`。84,259 个 tag 2，随后 7 个逐字节 transfer；旧 tag ≤1 只读 +1..+6 并把 +1 复制到 +0。旧臂未见，不计现代样本。
- `B = r+140+19E`：`0xe5dea5 → 0x151d710 → 0x433bbc0` 到 `extra+0xe7`。84,259 个 tag 3，随后 15 个逐字节 transfer；旧 tag <2 读 12 字节并复制 +8→+12、+4→+13（+14 无 wire），tag 2 读 14 并复制 +4→+14。精确 B lane 顺序以 t63 `object_path` 为准，不能按任务列表或 comp 顺序配位。
- `Cebd`（E106/048）：`0xe5dc38` 检 flag，`0xe5dc73` 保存 `extra+0x78` 的 election 指针，`0xe5dcc4 → 0x15211a0 → 0x4342940` 读取 19 B；`0x4342989` 的第二次 4 B transfer 落在 election `+8`，与 getter `0xe8a39d → 0xe8c679 → 0xe97023 → 0xe9717c` 相同。坐标 `r+88`，仅当 `E=1`。11,963 条有日期，72,296 缺对象；年 1900–2027、日 1–365，逐行 Gregorian 校验 0 违规，10,643 条 `(1900,1)` 保留原值；首例 `@100:01006c07`。
- `Cyfn`（E97/026）：`0xe5d388` 读 2 B 至 `extra+0xd8`，`0xe8b977 → 0xe8e6a9/e8e6b1` 取 `u16`、零时抑制。client 坐标 `r+4`。server 全档等价坐标：`a28=r+180+19E; f48=a28+2+22*u8[a28]; a68=f48+8+66*u8[f48]; Cyfn=a68+5+11*u16le[a68]`。66 B 来自已观测的 `+0x48` 子对象内版本 1、10 个 4 B item；此简式仅用于当前两档的实测分支，完整顺读和 EOF 另查。UID 配对 **84,259/84,259 同值**；30,661 个可选零、53,598 个非零（1857–2024，在 schema 1800–2100 内）。

| 块及 lane | 4CC（按 lane 顺序） | server 各字段域 | client |
|---|---|---|---|
| A+0..6 | `Ccsp Ccsk Ccsf Ccsr Ccsb Ccsh Ccsy` | 合计观察集 `{0,1,2,4,6}` | 无 wire |
| B+0..14 | `Ccjm Ccja Ccjc Ccjy Ccji Ccjg Ccjp Ccjs Ccjd Ccda Ccdr Ccss Ccjt Ccjh Ccpc` | 合计观察集 `{0,1,2,4,6}` | 无 wire |

逐行封口还重放了状态块后的全部载荷，但没有给旁路字节命名：现代 server 扩展在 B 后依次消费 `4+8+5+8` B、`i8 count ×22`、`u8 count ×10`、四类条件/计数段（`+48/+30/+38/+70`）、`u32 count` 的 `+50`、`u16 count` 的 `+68`（实测 item 为 tag 2 + 10 B）、`+40` 条件段与 `+dc` 的 2 B。`+30/+38/+70/+50/+40` 本档 count/flag 全零，未见分支不作发布。公共尾从 `+d8:u16/+cc:u32` 进入 `0xe5d5a6 → 0x11d3200`：已冻结主行 `CLUB+0xba=0`，故跳过可选 `+90` 字符串；顺读 `+ac:2`、`+98:u32len+bytes`、`u8 count` 的 `+78`（tag 1 + 26 B）、8 B scalar。server 再读 `i16 count ×20`、`i8 count ×6`、16 B scalar、`u16 count` 的 8 种 base 虚分派项，以及可选 `+48` 版本/向量；各 tag 的 rel32 格与 vtable reader 在 `chain.json`。两档终点后均无 footer。

22 个字段逐列扫描 84,259 个 server `i8`，对冻结 `cnst={0,1,2,3,4,6}`，**1,853,698 个 byte / 0 越界**。枚举 `3` 合法但未出现；`Ccpc` 全是 6，仍有唯一 4CC 与明确 sink，不凭变化值命名。按 UID 检查了全部 84,259 对；client 的 **wire 交集为 0**，另列 server 与新建 extra 对象默认 6（构造 `0x3aabb18..30`）的对照及首个不同 UID。比如 `Ccsp` 有 683 个 server 值不同于该默认，443 个合法 0。没有把默认值当成 client 持久化值。邻接但未命名的 `+0xcc` 两档各 **84,259 个 `0xffffffff`、0 个 `0`**，与合法枚举 0、年份可选 0、缺 station 分列；枚举 wire `0xff`/signed −1 未见。Comp 只对照 t59/E99 转正并由 t64/E107 保留的观测子集 `{0,1,2,4,6}`，不引入 comp 坐标或解释。

## 回归与复跑

Liverpool：双档 ordinal 460 / UID 676，city ordinal 1061 / UID 100047；Bernabéu 容量和座位各 81,044。14 条冻结 client extra_3 年份夹具的**原坐标**全部复洽；Liverpool 1892，Manchester City 仍为 wire 1894 / 外部起源 1880。Old Trafford `74,031 != 74,140`、原 `Cccn` 及冻结 Club/Stadium 负结果原样保留。未启动游戏/编辑器/IDA，未联网，未访问 Z:。

独立 `verify.py` 不 import builder、ReaderCFG 或 fm24_dump；独立解目录、反向 DP、逐行有界重放、重验 PE 原字节及每字段全档域。两脚本 `--help` / `--selftest`、全量 build/verify、t01 anchors **7/7** 均通过。退出码 0/1/2。

```bash
export FM24_DB_DIR=<WORKSPACE>/scratch/data
py -V:3.12 -I -B scripts/t71_club100_cnst.py --build
py -V:3.12 -I -B scratch/t71/out/verify.py
py -V:3.12 -I -B scripts/t01_anchors.py
```
