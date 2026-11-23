# t01-m：STADIUM（table_21）行偏移

## 结论

- **验收达成：16 个确定 L3 字段**，另列 2 个有条件 pitch getter backing-slot 候选（`Spln`/`Spwd`，不计入阈值）。包括 server 前缀 12 个确定字段及 common/client tail 4 个字段；字段三元组与逐条字节证据见 `output.json.row_offset_map`。
- client：48,413 行、stride 38；server：48,413 行、stride 181。两式分别为 `14+48,413×38+8=1,839,716`、`14+48,413×181+8=8,762,775`。**全表** `server[143:181] == client[0:38]`（48,413/48,413）。
- t01h 的“77 宽度”不是一行的 wire 长度：它统计 entry 与 7 个 direct-callee 的八个 0x800 扫描窗口，共 77 个 `mov r8d,imm` / 76 个流调用候选。reader 函数首个 `ret` 在 `editor.exe@0x11844dd:c3`；函数体内是 34 个直接宽度点/34 个流调用，宽度立即数相加 74B（其中有条件路径）。不能拿 77 或 74 与 client stride 38 作等式。窗口拆分、每个立即数及负对照在 JSON `reader.t01h_scan_windows`。
- reader 的 `test bpl,bpl`（`editor.exe@0x1183f51:40 84 ed`）后 `je`（`@0x1183f54:0f 84 5c 04 00 00`）跳到 file offset `0x11843b6`，绕过 server 前缀直接进入 common tail。false 路径 direct transfers 共 21B；对象 `+0x34` helper 的调用链为 `@0x1184481:48 8d 4b 34`、`@0x1184488:e8 f3 3a c3 ff` → thunk `@0xdb7f80:e9 2b 04 d9 02` → `@0x39dd7c8:41 b8 04 00 00 00` / `@0x39dd7d4:ff 57 28`（4B）。row flag gate `@0x11843dd:f6 06 10`、条件 helper call `@0x11843ef:e8 1c fd 68 ff`；全量 client rows 均不置 bit 0x10。reader 在 client row+24 后以 `@0x11844dd:c3` 返回，没有把 +25/+29 的 base identity 字节冒称为该虚 reader 的 L3 字段。

## 输入与行框架（payload 偏移均指解压成员）

- 只读 client archive：SHA-256 `5ce7cd91…b9e5b5ecc1`；table_21 压缩数据在 archive file offset `0xb9b0f9`，字节 `28 b5 2f fd 04 60 fc d8 00 1a 12 02 5c 3c 10 10`。member SHA-256 `a817c6eb…d0ac17297`；payload `+0:03 01 74 61 64 2e f1 0d 1d bd 00 00 00 00`，count=`0xbd1d=48,413`；footer `+0x1c125c:00 00 00 01 7e ce 3a 77`。
- 只读 server archive：SHA-256 `99eed00b…b3ca4a662`；table_21 压缩数据在 archive file offset `0xf1c968`，字节 `28 b5 2f fd 04 60 e4 6d 04 2e 7d 06 88 14 3c 10`。member SHA-256 `c1071561…f6a50f62`；payload header 同为 14B/count 48,413，footer `+0x85b58f:00 00 00 01 7e ce 3a 77`。完整 SHA 与 file offset 证据在 `output.json.sources.database`。
- 冻结旧证据只从 `evidence/fm24/` 引用；`DB_TABLES_BIG.md` SHA-256 `453c0f0b…f2e7`，已对照 `evidence/MANIFEST.json`。其 table_21 L1 stride/identity 与本次全量复验相符；快照日期和校验结果见 JSON。

## 4CC → 对象 → 行偏移（L3）

下表 `G` 为 getter 的 `cmp 4CC / 对象读取`，`R` 为 reader 的 `lea destination / mov r8d,width / call [rax+0x28]`；地址均是 `editor.exe` file offset，冒号后为原字节。`server+143+n` 是 common tail 映射。

|字段|wire row+ / object+|G：cmp / object access|R：destination / width / stream call|
|---|---:|---|---|
|`Scpy`|server+0 / +0x6c|`118688c:81 fb 79 70 63 53`; `1186898:8b 77 6c`|`1183f5a:4c 8d 7b 6c`; `1183f65:41 b8 04 00 00 00`; `1183f6e:ff 50 28`|
|`Sscy`|server+4 / +0x70|`1186840:81 fb 79 63 73 53`; `118684c:8b 77 70`|`1183f71:4c 8d 63 70`; `1183f7c:41 b8 04 00 00 00`; `1183f85:ff 50 28`|
|`Secy`|server+8 / +0x7c|`11867f4:81 fb 79 63 65 53`; `1186800:8b 77 7c`|`1183f88:48 8d 53 7c`; `1183f93:41 b8 04 00 00 00`; `1183f99:ff 50 28`|
|`Scas`|server+12 / +0x78|`1186283:81 fb 73 61 63 53`; `1186eca:8b 77 78`|`1183f9c:48 8d 53 78`; `1183fa7:41 b8 04 00 00 00`; `1183fad:ff 50 28`|
|`Sowi`|server+16 / +0x80|`11864e8:81 fb 69 77 6f 53`; `11864f4:48 8b 8f 80 00 00 00`|`1183fb4:48 8d 93 80 00 00 00`; `1183fbe:41 b8 04 00 00 00`; `1183fc7:ff 50 28`|
|`Sdcy`|server+20 / +0x9a|`1186112:81 fb 79 63 64 53`; `1186e42:0f be b7 9a 00 00 00`|`1183fd8:48 8d 93 9a 00 00 00`; `1183fe2:41 b8 01 00 00 00`; `1183feb:ff 50 28`|
|`Spln`*|server+25 / +0x88|`1186307:81 fb 6e 6c 70 53`; fallback `1186f2a:0f b7 87 88 00 00 00`|`1184010:48 8d 93 88 00 00 00`; `118401a:41 b8 02 00 00 00`; `1184023:ff 50 28`|
|`Spwd`*|server+27 / +0x8a|`1186bb2:81 fb 64 77 70 53`; fallback `1187611:0f b7 87 8a 00 00 00`|`1184034:48 8d 93 8a 00 00 00`; `118403e:41 b8 02 00 00 00`; `1184047:ff 50 28`|
|`SlIM`|server+29 / +0x8c|`1186aae:81 fb 4d 49 6c 53`; `1186aba:0f b7 87 8c 00 00 00`|`1184058:48 8d 93 8c 00 00 00`; `1184062:41 b8 02 00 00 00`; `118406b:ff 50 28`|
|`SwIM`|server+31 / +0x8e|`11866cf:81 fb 4d 49 77 53`; `11866db:0f b7 87 8e 00 00 00`|`118407c:48 8d 93 8e 00 00 00`; `1184086:41 b8 02 00 00 00`; `118408f:ff 50 28`|
|`Spty`|server+33 / +0x9d|`1186603:81 fb 79 74 70 53`; `118660f:0f b6 87 9d 00 00 00`|`11840a0:48 8d 93 9d 00 00 00`; `11840aa:41 b8 01 00 00 00`; `11840b3:ff 50 28`|
|`Sste`|server+34 / +0x9f|`1186b0d:81 fb 65 74 73 53`; `11875a4:0f be b7 9f 00 00 00`|`11840c4:48 8d 93 9f 00 00 00`; `11840ce:41 b8 01 00 00 00`; `11840d7:ff 50 28`|
|`Senv`|server+35 / +0xa0|`1186514:81 fb 76 6e 65 53`; `118705b:0f be b7 a0 00 00 00`|`11840e8:48 8d 93 a0 00 00 00`; `11840f2:41 b8 01 00 00 00`; `11840fb:ff 50 28`|
|`Sitg`|server+36 / +0x9b|`1186aa2:81 fb 67 74 69 53`; `1187567:8a 9f 9b 00 00 00`|`118410c:48 8d 93 9b 00 00 00`; `1184116:41 b8 01 00 00 00`; `118411f:ff 50 28`|
|`Scti`|client+3 / server+146 / +0x50|`1186b5d:81 fb 69 74 63 53`; `11875dc:48 8b 4f 50`|`1184427:48 8d 53 50`; `118442e:41 b8 04 00 00 00`; `1184437:ff 50 28`|
|`Sptc`|client+11 / server+154 / +0x98|`11865f7:81 fb 63 74 70 53`; `118710d:0f bf b7 98 00 00 00`|`1184465:48 8d 93 98 00 00 00`; `118446f:41 b8 02 00 00 00`; `1184478:ff 50 28`|
|`Slat`|client+17 / server+160 / +0x60|`1186330:81 fb 74 61 6c 53`; `1186f74:f3 0f 10 77 60`|`1184495:48 8d 53 60`; `118449c:41 b8 04 00 00 00`; `11844a5:ff 50 28`|
|`Slon`|client+21 / server+164 / +0x64|`118633c:81 fb 6e 6f 6c 53`; `1186348:f3 0f 10 77 64`|`11844b2:48 8d 53 64`; `11844b9:41 b8 04 00 00 00`; `11844c2:ff 50 28`|

`* Spln/Spwd` getter先检查 international slot（分别 `obj+8c/+8e`，`SlIM`/`SwIM` 自身也直接读该槽），仅在条件分支才回退 `obj+88/+8a`；因此这两项保持 fallback/backing-slot 候选，不计入 16 个确定字段。full-register getter scan 从 vtable slot 2（`editor.exe@0x188d1e8`）起，对窗口 `0x1185eb0..0x1189250` 扫 `81 f8..ff` 与 `3d`；命中、边界解码及 EAX-only 负对照均在 JSON `getter_scan`。

## 旧锚、抽验与边界

- `Scti@client+3` 经 reader 的 `obj+0x50 / 4B` 链印证；48,413/48,413 引用均小于 table_2 的 56,293 行数。四个冻结 L2 城市锚复现：Anfield row67→1061 Liverpool；Old Trafford row71→1075 Manchester；Bernabéu row430→316 Madrid；Munich Stadium row12048→540 München。
- client row ordinal@+25（旧 L1 标签 `rdui`，E20 勘误：不是 native rdui）、`duni@+29` 与 server row ordinal@+168、`duni@+172` 按 L1 旧锚全量复验：48,413 行 ordinal 全等、repeated-u32 DUNI 全表唯一。reader 在坐标读完后于 `0x11844dd` 返回，故未将 identity suffix 升级成此 virtual reader 的 L3。
- 5 行抽验（row 起点均为解压 member offset）：row0 client `0xe`；Anfield client `0xa00`/server `0x2f6d`；Old Trafford `0xa98`/`0x3241`；Bernabéu `0x3fe2`/`0x13014`；Munich `0x6fc6e`/`0x21465e`。每行完整 client bytes、server prefix bytes及字段样例见 JSON `five_row_samples`。
- 容量候选保留旧反例：Old Trafford `Scpy` 候选 74,031，不等于独立参考 74,140；Bernabéu 81,044、Munich 75,000 / `Sscy` 54,511 与旧锚吻合。此处 L3 结论是槽位，容量语义仍按旧报告的候选口径。
- 负对照：client stride=181、Scti 错移一字节、server suffix 起点错用142均被拒；全表错序/坏引用/身份与拼接不匹配都会使自检失败。L4=0。

复验：`py -V:3.12 -I -B scratch/t01/inbox/t01m/verify.py --help`；`py -V:3.12 -I -B scratch/t01/inbox/t01m/verify.py --selftest`。仅 `--write` 会重建本目录 `output.json`。
