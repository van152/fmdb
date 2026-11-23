# t01-j：`basic_people_db.dat` 侦察

## 结论

- **文件与主 archive 不同构。** `basic_people_db.dat` 不是 FMF archive：外层 `file+0x0: 03 01 74 61 64 2e f1 0d`，直接 Zstd 从 `file+0x8: 28 b5 2f fd` 开始；FMF 主头 `02 01 66 6d 66 2e 08 00 00` 与目录帧签名 `02 01 66 6d 66 2e 08 00 00 28 b5 2f fd` 全文件均无命中。因此没有可枚举的 FMF 条目/数值表 ID（JSON 的空数组表示“不适用”，不是空目录）。
- 完整单帧解压为 54,060,043 B，SHA-256 `16709b0b…c9589d35a5`。发现 658,011 条按 class 变长记录，行数、行边界、身份尾块及 9 B 尾部均封口通过。
- **BASIC_PERSON 是强候选，但仅获得部分 L3 呼应。** editor.exe `BASIC_PERSON` reader 的 class-4 分支 1/2/2 B 与实际 class-4 行精确对齐；不把 27 条静态宽度指令当成一条无分支序列，其他字段/全行静态映射未闭合。

## FMF 对照

- 主 archive 的外层同为 `file+0x0: 03 01 74 61 64 2e f1 0d`，但 FMF 主头在 `file+0x8`，数据基址 `0x22`；basic_people 在 `file+0x8` 已是 Zstd 魔数。
- client：TOC `file+0xc81799`，帧头 `02 01 66 6d 66 2e 08 00 00 28 b5 2f fd`，解压目录 1,954 B、31 项、20 张数值表。ID 顺序见 `output.json`。
- server：TOC `file+0x36d7c94`，同帧头，目录 4,784 B、77 项、59 张数值表。ID 顺序见 `output.json`。
- 两主 archive 逐字段目录元数据（path、offset、packed/decoded size、time fields）均写入 `output.json`；basic_people 没有对应 FMF 字段。来源 archive SHA-256 与 t01i 当前输入一致。外部输入均只读。

## 行框架与身份块

- payload `offset 0: 5b 0a 0a 00` = u32 count 658,011；`offset 4: 00`；首行从 `offset 5` 开始。
- 行头为 `u8 0x11 | u8 class_id`。class 1/2/3 行长 83 B，class 4 为 34 B，class 5 为 22 B；起点公式 `start[0]=5; start[n+1]=start[n]+length(class[n])`，不是固定 stride。
- class 数量：1=166,064；2=476,158；3=4,757；4=9,839；5=1,193。总行字节 54,060,029；`5 + 行字节 = end 54,060,034`；余下 9 B：`payload+0x338e402: 00 00 00 00 01 4c bd 54 77`，EOF `0x338e40b`。
- 658,011/658,011 行尾 `row_end-12` 都是 `u32 ordinal | u32 ID | 重复 u32 ID`；ordinal 连续 `0..658010`，两个 ID dword 全量相同。这里仅称重复 ID 候选，不擅自命名 DUNI/RDUI。
- 五类抽样（payload offset；长度；身份块原字节）：`ord0/class1 @5 (11 01)/83; +0x4c: 00 00 00 00 03 00 00 00 03 00 00 00`；`ord89/class2 @7392 (11 02)/83; +0x1d27: 59 00 00 00 e4 01 00 00 e4 01 00 00`；`ord1155/class3 @94939 (11 03)/83; +0x17322: 83 04 00 00 86 1c 00 00 86 1c 00 00`；`ord972/class4 @80681 (11 04)/34; +0x13b3f: cc 03 00 00 d2 14 00 00 d2 14 00 00`；`ord656818/class5 @54033788 (11 05)/22; +0x3387d86: b2 05 0a 00 a4 b8 54 77 a4 b8 54 77`。偏移均为解压 payload offset。

## BASIC_PERSON reader 对照 / 边界

- 静态证据（editor.exe SHA-256 `b82ebe8e…adadab4`）：type-1 跳表 `+0xf49d3c: da ef ff ff` → handler `0xf48d12`；RTTI `+0x1aac700: .?AVBASIC_PERSON@db@@\0`；slot-19 `+0x187b3c0: 70 fd e4 40 01 00 00 00` → reader `+0xe4f370`。
- reader census 的 27 个 `mov r8d,N`（文件偏移:宽度）由脚本按 Capstone 从入口及两个直接 helper 复核：`e4f393:1, e4f43c:2, e4f468:2, e4f4f6:8, e4f4fe:4, e4f542:8, e4f54a:4, e4f57f:8, e4f587:4, e4f5ba:4, e4f5da:4, e4f5fa:2, e4f61a:2, e4f63a:2, e4f65a:2, e4f67a:2, e4f69a:2, e4f6ba:2, e4f6da:2, e4f6fa:2, e4f71a:1, e4f73a:1, e4f75a:1, 3dc0241:8, 3dc027b:12, 3c6e121:8, 3c6e129:4`。所有指令原字节均在 JSON。
- 可闭合的一段：reader `+0xe4f42e: 3c 04` 比较 class 4，`+0xe4f430: 75 4c` 非 4 跳过；样本行头 payload `+80681: 11 04 af 00 00 00`；其中 `+80682: 04`、`+80683: af 00`、`+80685: 00 00`，恰与 reader `+0xe4f393` 的 1 B、`+0xe4f43c` 的 2 B、`+0xe4f468` 的 2 B 调用吻合。
- 其余 8/4 B 分支是互斥宽度选择，且 reader 含条件路径/helper。没有把静态宽度清单求和冒充实际行布局；未命名业务字段、未证明完整 27 条序列对应所有 row variant，也未赋予重复 ID 的 DUNI/RDUI 语义。

## 复验与交付

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01j/verify.py --help
py -V:3.12 -I -B scratch/t01/inbox/t01j/verify.py --selftest
```

`--selftest` 只读重建并核对 JSON、输入 SHA、目录、全量行链、静态字节和合成正/负对照；`--write` 仅写同目录 `output.json`。旧证据仅使用冻结快照 `PEOPLE_DB.md` / `PEOPLE_FIELDS.md`，SHA-256 均与 `evidence/MANIFEST.json` 核对；本次行统计另由安装原件全量重算。未启动游戏/编辑器/IDA，未安装依赖，L4=0。
