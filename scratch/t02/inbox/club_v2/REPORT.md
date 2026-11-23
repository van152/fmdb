# t02-c：club 变体段续解

## 状态

- **行框架封口：84,259/84,259 行**；最后一行结束于解压 member `+0x69c66a`，紧接 8B footer `00 00 00 01 e3 c0 3a 77`，与 member 末尾精确相接。
- **schema/类级解析未完成**：12 项是 L1 结构偏移，不是 4CC→对象槽位的 L3 映射；L3 字段数 **0**。三条紧凑行仅由尾部 identity 锚定，字段语义未解。
- 本次证据与既有“第 69,705 行起第五字段变 4B”的说法不一致：ordinal 69,705 的整行仍通过当前 5B 聚合布局，失败点是尾字节 `0x0c`，不是 identity 错位。此处保留冲突，不把未核实的类归属写成结论。

## 输入与复现

- 只读输入：`Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\client_db.dat` 中的 `client_db/table_3.dat`；member 解压长度 `6,932,082`，SHA-256 `db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f`。以下 offset 均为**解压 member 内偏移**，不是归档压缩块 offset。
- 只使用 `py -V:3.12 -I -B`；未启动游戏、编辑器、IDA，未安装依赖；输出只在本目录。
- 复验：
  ```text
  py -V:3.12 -I -B scratch/t02/inbox/club_v2/solve.py --help
  py -V:3.12 -I -B scratch/t02/inbox/club_v2/solve.py --selftest
  py -V:3.12 -I -B scratch/t02/inbox/club_v2/finalize.py --help
  py -V:3.12 -I -B scratch/t02/inbox/club_v2/finalize.py --selftest
  ```
  输出：`walked_rows=84259/84259`、`footer_exact=True`、两脚本 `selftest OK`。

## 行走查与变体证据

- 标准字段解析：**84,256 行**，第五块按 `row+16..+20` 的 5B 聚合读取；其内部分成一个 4B 值还是 4B+相邻 1B，单凭行字节尚不能定性。序号范围：`0..69705`、`69709..84258`。标准行逐条校验 ordinal 与重复 ID；紧凑 3 行逐条校验 identity 后缀，故 84,259 行 identity 均通过。
- 紧凑、未解 body：**3 行**，ordinal `69706..69708`，各 55B；identity 从 `row+42` 起，之后 1B trailer 分别为 `0c / 0c / 00`。普通 5B 字段解析失败，程序只用 `ordinal|ID|ID` 和 trailer 作行框架，不猜其余字段。
- `0x0c` trailer 共 3 行：69705、69706、69707；其余 84,256 行 trailer 为 `0x00`。因此 `0x0c` 也不能单独充当两类 RTTI 的判据。
- 变长跨度直方图见 `output.json.row_length_distribution`：**87 种跨度，54..156B**，频数合计 84,259。footer 前数据区长度 `0x69c66a`。
- 普通布局的 4B 重试成功数为 **0**（84256 行）。反例：row 69709，member offset `0x570ec7`。5B 解释下 `row+16..20 = 57 db 00 00 00`，`row+21..24 = 00 00 00 00`，`row+25 = 00`，名称长度在 `row+26..29 = 12 00 00 00`（18），对应 `NK Rudar Kamengrad`。若只将第五块当 4B 并维持其余同一布局，长度字落在 `row+25..28 = 00 12 00 00`（4608），与该布局不符。
- 转折样本（全部完整行 bytes 在 `output.json.variants`）：
  - 前段：row 69702 `+0x570cfe`、69703 `+0x570d53`、69704 `+0x570d96`，均可用 5B 聚合布局、trailer `00`。
  - row 69705 `+0x570dd9`：`... 49 10 01 00 31 45 d8 05 31 45 d8 05 0c`；identity 为 `[69705, 98059569, 98059569]`，末字节 `0c`。它仍是 5B 布局的成功解析行。
  - 紧凑行：row 69706 `+0x570e22`、69707 `+0x570e59`、69708 `+0x570e90`；均 `+42` 处开始 identity，span=55B。
  - 后段：row 69709 `+0x570ec7`、69710 `+0x570f16`、69711 `+0x570f6a`，均可用 5B 聚合布局解析。

**变体规则结论（保守）**：当前可证规则是“标准布局按 5B 聚合字段可解析；69706–69708 是 55B 紧凑 body；trailer 0x0c 出现在三行但不等价于类标记”。“CLUB vs LEAGUE_BODY_CLUB 哪些 ordinal 使用第五字段 4B”仍未确定；不以行序、名称或 trailer 猜类。

## `editor.exe` 静态链及边界

使用 `scratch/t01/inbox/t01h/output.json` 中 type_id=3 项；editor SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`：

- RTTI 有 `.?AVCLUB@db@@` 与 `.?AVLEAGUE_BODY_CLUB@db@@` 两个类。CLUB slot19 reader entry `0xe5a7a0`；`editor.exe@0xe5a811: 41 b8 04 00 00 00`，附近 destination setup `@0xe5a807: 49 8d be e0 00 00 00`，证明向 object+`0xe0` 的一项 4B transfer。
- LEAGUE_BODY_CLUB slot19 thunk `0x157cff0` → body `0x43beba0`；`@0x43bebe6: 41 b8 04 00 00 00`，destination `@0x43bebdc: 48 8d 91 70 01 00 00`（object+`0x170`）；另有 `@0x43bec05: 41 b8 01 00 00 00`，destination `@0x43bebfb: 48 8d 93 78 01 00 00`（object+`0x178`）。这些证明 reader 中有不同目的地址的 4B/1B transfer，**没有**证明它们对应行内第五块，也没有把 RTTI 类绑定到具体 row ordinal。
- `output.json.row_offset_map` 记录 12 项 L1 wire 结构。对象偏移、getter 4CC 与 reader sink 未闭合，故未把它们升级为 schema 字段，也未计入 L3 阈值。

## 未闭合

1. RTTI class → row ordinal 的独立判据，以及第五块“4B vs 5B”语义分段；现有行证据反而显示标准解析均为 5B aggregate。
2. row 69706–69708 的 42B prefix 各字段。
3. ≥10 个 getter 4CC → object destination → payload 行偏移的完整 L3 链。本次未完成字段 getter 对齐，**字段数 0**。

## 交付物

- `scratch/t02/inbox/club_v2/output.json`：机器结果、全量跨度分布、原始样本和未闭合事项。
- `scratch/t02/inbox/club_v2/solve.py`：只读逐行 walker；每 1,000 行写一次本目录 checkpoint。
- `scratch/t02/inbox/club_v2/finalize.py`：复核 member footer、集中输出证据与 L1 结构偏移；输出只写本目录。
