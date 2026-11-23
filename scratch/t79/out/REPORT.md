# t79 — stadium(21) + team(24) + extra_24 静态 L3 收割 + CLUB+0x18 转发链

## 0. 摘要与证据口径

- **静态二进制(只读)**:`D:/tmp2b/fm24/input/editor.exe`(SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`),全部静态地址采用 t57 约定(PE **file offset**,机读台账同时附 VA、指令字节与反汇编)。
- **冻结证据校核(`evidence/MANIFEST.json`)**:
  - `evidence/fm24/reports/editor_schema/master.json`:SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda` 校验通过。
  - `evidence/fm24/reports/dbdat_decode/db_tables_big.json`:SHA-256 `c57b2b6837a3dcca106bf4363da105eca7665df407b738483839d1b7b6de3ddf` 校验通过。
  - `evidence/fm24/reports/dbdat_decode/extra_tables_verdict.json`:SHA-256 `4916b1a26fc3ceaa9c464fbe68fdd2af1cdb07fcb6335a9051877a824f24ab91` 校验通过。
- **L2 指纹来源说明**:`scratch/t76a/out/` 为空目录,按任务约定由本任务直接在 `client_db.dat` / `server_db.dat` 帧上完成向量化全档槽位 profiling 与值域验证。
- **证据等级**:静态链达 **L3**,数据面为 L1/L2 全档向量化校验;**L4=0**(未启动游戏/编辑器/IDA,未读写 `Z:`,未联网)。

### 总收获一览

| 目标 | 总字段 / 槽位 | L3 | held | 非 wire / 计算 / 转发 / 子表 / 未实现 | 说明 |
|---|---:|---:|---:|---:|---|
| **`stadium.xml` (`table_21`)** | 60 | **41** | **4** | 15 | 9 常见双档 + 31 server 独有 + 1 `duni`;另 7 个内部/不透明 wire 槽使 181B/38B 100% 闭合 |
| **`team.xml` (`table_24`)** | 25 | **11** | **2** | 12 | server-only 84,507 行(251 `NATIONAL_TEAM` + 84,256 `TEAM`);另含 `Tldi@+0x60` 等内部槽 |
| **`table_extra_24.dat`** | 82B 全闭合 | **2 (+1 内部)** | 0 | 74B 静态成员未接 4CC | 绑定至 **`TEAM+0xa0`**(`0x11a15fa`);`Twhm@10`/`Tmhm@11` L3 + `Tpvr@21` L3 内部 |
| **`club.xml` 经 `CLUB+0x18` 转发** | 6 (t63 held) | **6** | 0 | 0 | `Crep/Cdvi/Cldi/Cndi/Codi/Csti` 全部由 `held` 升 **L3**(标注 **经 +0x18 转发的投影**),getter+setter 均已入账 |

---

## 1. 工厂、Vtable / RTTI 与全局 `db+offset` 绑定

工厂函数 `0xf48b30` 的 rel32 跳转表位于 `0xf49d38`:

| 表号 | 入口 (`rel32`) | 类 / RTTI | Vtable VA (fo) | slot 2 (get) | slot 3 (set) | slot 19 (read) | slot 20 (fixup) | slot 21 (write) |
|---:|---|---|---|---|---|---|---|---|
| 21 | `0xf49078` | `.?AVSTADIUM@db@@` | `0x14188dbd8` (`0x188d1d8`) | `0x1185eb0` | `0x1189260` | `0x1183f30` | `0x1184920` (`0x3e44580`) | `0x1184a50` |
| 24 (`bl==0xb`) | `0xf490f9` | `.?AVNATIONAL_TEAM@db@@` | `0x141889618` (`0x1888c18`) | `0x1056a90` (`0x3d7d6c0`) | `0x11b4c30` | `0x1052c80` | `0x1053120` (`0x3d7b710`) | `0x10531b0` |
| 24 (`bl!=0xb`) | `0xf490f9` | `.?AVTEAM@db@@` | `0x14188e2d8` (`0x188d8d8`) | `0x11af7b0` | `0x11b4c30` | `0x11a0880` | `0x11a0c40` | `0x11a10e0` |
| 24 (基类) | — | `.?AVTEAM_BASE@db@@` | `0x141882c78` (`0x1882278`) | `0x11c2600` | `0x11c23f0` (`0x3e98660`) | `0x11c1d80` (`0x3e94390`) | `0x11c1f40` | `0x11c1f90` |

`0xf026c0` 中的全局 `DATABASE` 上下文表注册(用于所有 fixup 引用目标确认):
- `[db+0x8]` (`0xf02957`):table 2 (`CITY`)
- `[db+0x10]` (`0xf02a93`):table 3 (`CLUB`)
- `[db+0x18]` (`0xf02bcf`):table 25 (`COMP`)
- `[db+0x60]` (`0xf036eb`):table 9 (`NATION`)
- `[db+0x80]` (`0xf03f06`):table 21 (`STADIUM`)
- `[db+0x98]` (`0xf042c3`):table 24 (`TEAM`)

---

## 2. `stadium` (`table_21.dat`, 48,413 行)静态 L3 与双档差异解释

### 2.1 行框与 Client 38B vs Server 181B 静态根因

- **原生行框**(13B 头 `03 01 tad. f1 0d` + u32 `48413` + `00`,每行首字节为 selector=`0x00`,尾 9B footer `00000000017ece3a77`):
  - Client:`13 + 48,413 × 38 + 9 = 1,839,716 B` = `1B sel` + `25B common (c+0..24)` + `12B identity (c+25..36)`。
  - Server:`13 + 48,413 × 181 + 9 = 8,762,775 B` = `1B sel` + `143B server prefix (s+0..142)` + `25B common (s+143..167)` + `12B identity (s+168..179)`。
  - **双档逐字节对照**:全部 48,413 行 × 37B (`common 25B + identity 12B`)在 `client_db` 与 `server_db` 间 **100% 逐字节相等**。
  - **与 b47/t74 口径对账**:b47 (`db_tables_big.json`) 与 t74 采用 `14 + 48413×stride + 8`,将第 0 行首字节 selector `0x00` 计入 header,并将每行之后下一行的 selector `0x00` 计为尾字节 `+37/+180`(末行借用 footer 首字节 `0x00`)。按去掉首字节 selector 后的行体坐标(body offset),client 锚点完全复洽:**`Scti@3`**, **`Slat@17`**, **`Slon@21`**, **`ordinal@25`**(b47 标注为 `rdui@25`), **`duni@29..32`** + 重复 `rdui_raw@33..36`。
- **143B 差额的静态证明**:`STADIUM::read` (`0x1183f30..0x1184519`, 370 条指令, 0 间接跳转) 在 `0x1183f49..0x1183f54` 检测模式字节 `[rsp+0xd0]` (`test bpl, bpl; je 0x11843b6`)。client(`mode=0`)直接跳过 `0x1183f5a..0x11843b3` 的全部 143B server-only 成员读入(`Scpy..Sscl`,含 `STADIUM+0x18` 66B 侧翼子对象),落入 `0x11843b6` 读取 25B 公共尾段与 `0x3c600f0` 12B identity。

### 2.2 `stadium.xml` L3 字段(41 项)

- **Identity (1,双档)**:`duni` (`c+29 / s+172`, `+0x0c`, `DATABASE_RECORD_GET 0xfe3912`, 48,413 唯一且全行 `u1==u2`)。
- **公共 25B 尾段(9 项,client+server 双档逐字节一致)**:
  - `Scov` (`c+0/s+143 bit 0`, `+0xa6 b0`, get `0x118628f`, set `0x1189636`, 73 置位;注:getter 在全局 `0x86640()!=0` 且 `Srrf(b6)=1` 时返回 `true`,覆盖 48 行,setter 仅写 bit 0)
  - `Sush` (`c+0/s+143 bit 1`, `+0xa6 b1`, get `0x1186996`, set `0x1189382`, 1,040 置位)
  - `Srrf` (`c+0/s+143 bit 6`, `+0xa6 b6`, get `0x1186222`, set `0x11894c3`, 55 置位)
  - `Nucf` (`c+0/s+143 bit 7`, `+0xa6 b7`, get `0x11863ec`, set `0x11893df`, 1,651 置位)
  - `Scti` (`c+3/s+146`, `+0x50`, i32→t2 via `[db+0x8]`, get `0x1186b5d`, set `0x118951f`, 48,413 live / 0 miss;错配 UID 对照 43,056 miss)
  - `Snbs` (`c+7/s+150`, `+0x58`, i32→t21 via `[db+0x80]`, get `0x1185f74`, set `0x118979a`, 4,173 live / 44,240 `-1` / 0 miss;错配 UID 对照 3,732 miss)
  - `Sptc` (`c+11/s+154`, `+0x98`, i16, get `0x11865f7`, set `0x11892a5`, `[29, 200] ⊂ [0, 200]`)
  - `Slat` (`c+17/s+160`, `+0x60`, f32, get `0x1186330`, set `0x11896bd`, 全有限 `[-54.8163, 71.0288]`)
  - `Slon` (`c+21/s+164`, `+0x64`, f32, get `0x118633c`, set `0x118957a`, 全有限 `[-175.2074, 179.1984]`)
- **Server 独有 143B 前缀(31 项,server-only)**:
  - 容量与归属:`Scpy` (`s+0`, `+0x6c`, `[0,115109]`), `Sscy` (`s+4`, `+0x70`, `[0,114000]`), `Secy` (`s+8`, `+0x7c`, `[0,150000]`), `Scas` (`s+12`, `+0x78`, getter 抑制 `<=0`, 5,290 live `[1,107601]`), `Sowi` (`s+16`, `+0x80`, i32→t3 via `[db+0x10]`, 13,576 live / 34,837 `-1` / 0 miss;错配 UID 12,388 miss), `Sdcy` (`s+20`, `+0x9a`, 全 5), `Sucy` (`s+21`, `+0x74`, getter 抑制 `<=0`, 7,489 live `[1,100000] ⊂ [1,200000]`)。
  - 球场尺寸(`i16 / 10.0`,读后经 `0x3e42e30` 钳位):`Spln` (`s+25`, `+0x88`), `Spwd` (`s+27`, `+0x8a`), `SlIM` (`s+29`, `+0x8c`, 450 live `[90,110]m`), `SwIM` (`s+31`, `+0x8e`, 450 live `[55,75]m`), `Smnl` (`s+54`, `+0x90`, 全 `90.0m`), `Smnw` (`s+56`, `+0x92`, 全 `55.0m`), `Smxl` (`s+58`, `+0x94`, 3,934 live `[9,120]m`), `Smxw` (`s+60`, `+0x96`, 3,941 live `[5.8,90]m`)。
  - 枚举与状态:`Spty` (`s+33`, `+0x9d`, getter `0x1186603` `cmovae` 将 `<2` 钳位至 `1`,原值 `{0:1901,1:35768,2..8}`→有效值全落 `enums['Spty']={1..8}`), `Sste` (`s+34`, `+0x9f`, `{1..5}`), `Senv` (`s+35`, `+0xa0`, `{0..4}`), `Sunt` (`s+49`, `+0xa1`, `ubnt`), `Su21` (`s+50`, `+0xa2`, `ubnt`), `Su19` (`s+51`, `+0xa3`, `ubnt`), `Soty` (`s+52`, `+0xa4`, getter `0x118679c` 抑制 0, 31,356 live 全落 `{1..5}`), `Sprr` (`s+130`, `+0x9e`, `[0,20]`)。
  - 标志与日期与颜色:`Sext` (`s+36 b0`, `+0x9b b0`, 824), `Sitg` (`s+36 b2`, `+0x9b b2`, 5,167), `Sdah` (`s+36 b6`, `+0x9b b6`, 519), `Sbld` (`s+37`, `+0x28`, `1807..2029`), `Srbd` (`s+41`, `+0x2c`, `1900..2028`), `Doco` (`s+45`, `+0x30`, `1859..2028`), `Sprl` (`s+135`, `+0x24`, `1900..2031`), `Sscl` (`s+139`, `+0x68`, `0x3e43f90` 逆序读 `+3,+2,+1,+0`, `0x3e448a0` 回退 club/`0xff7f7f7f`, 31,306 非零)。

### 2.3 `stadium.xml` `held`(4 项)与非 wire / 未实现(15 项)

1. **`rdui` (`held`)**:`DATABASE_RECORD_GET` `0xfe38a2` 在 `[+0x0c]==[+0x10]` 时抑制输出,48,413/48,413 全被抑制(0 live)。
2. **`Sdtr` (`held`)**:`STADIUM_GET 0x11867e8 → 0x11872fe` 直接 `movsx [rdi+0x9c]` 无钳位无抑制,但 **29,983 / 48,413** 行原值为 `0`(首反例:row 0, UID 600, raw=0),越出 `enums['Sdtr']={1:Slow, 2:Medium, 3:Fast}`。
3. **`Splr` (`held`,大小写错配)**:`stadium.xml[29]` 写小写 `Splr`,而 `STADIUM_GET 0x1186313` (`cmp ebx, 'Splr'; je 0x1185f0a`)直接空操作返回 1 且 `STADIUM_SET` 无此分支;实际 `s+131` (`+0x20`, 48,413 合法日期 `1900..2024`)由大写 **`SplR`** 分发(get `0x1186a4c` / set `0x1189678`)。
4. **`Ssds` (`held`)**:`s+63` 存在标志(全 1) + `s+64..129` (`0x4401010` 读 8 侧 × 8B + 2B 全 0)。`STAD_side_get` (`0x15e6650`) 全部 12 子字段(`indx, capc, sage, cond, exis, seat, iuse, tunn, roof, rofs, tclo, reno`)静态闭合且 11/12 域验证 0 违例,但 `sage` (`+4` i16, wire `+5..6`, `0x15e6740` 直接 `movsx`)在全档 387,304 侧中出现 **20,425 个负值**(`-1..-7173`,含 10,291 个 `exis=True` 侧,首反例 row 80 side 0 UID 689 raw=`-4`,伯纳乌 `-7173`),违背 XML `min_value=0`,依规 `held`。
- **非 wire / 派生 / 子表 / 未实现(15 项)**:`Snam`(inline 标志 `+0xa6 b4` 全 0, 名称在语言层)、`dbnm`(虚拟名)、`Snti`(`(*(STADIUM+0x50))+0x20` 经 City 转发)、`Scpc`(扫描全局 `table_22 STADIUM_CHANGE`)、`Shts..Shtl`(8 项仅在 slot 5 `0x1185020` 注册,get/set 均无处理)、`Shcc`(`.text` 0 命中)、`NDBC/FDBC`(编辑器变更计数)。
- **其余内部/不透明 wire 槽(实现 181B/38B 100% 字节闭合)**:`Sovl@s+36b5` (1,940)、`Snft@s+53` (全 0)、`SplR@s+131`、`Wucf@c+0b11` (116)、`+0xa8@c+2` (全 0)、`+0x34@c+13` (全 `1900-01-01`)、`ordinal@c+25`。

---

## 3. `team` (`table_24.dat`, 84,507 行, server-only)静态 L3

- **行框与 t74 对账**:`client_db.dat` 无 `table_24.dat`。`server_db/table_24.dat` 原生行框为 13B 头 + 84,507 变长行(行宽 `86..666 B`) + 9B footer (`0000000001e3c03a77`) = `8,819,030 B` 精确闭合。
  - 首字节 selector 分布:**`11` (`NATIONAL_TEAM`, 49B 前缀 = 48B 标量 + i8 cnt 全 0) 共 251 行** + **`10` (`TEAM`) 共 84,256 行** = 84,507 行,与 `Tisn==1` (251 行) **100% 一致**。t74 记录 `{10:84256, 11:250, 0:1}` 系将第 0 行首字节 `11` 计入 14B header 并把末行外 footer 首字节 `00` 计入行尾所致。
- **`team.xml` L3 字段(11 项)**:
  - `duni` (identity `-8..-5`, `+0x0c`, 84,507 唯一, 与 t66 一致)
  - `Trep` (`TEAM+2..3`, `+0xa8`, i16, get `0x11aff60`, set `0x11b4c85`, 原值 `[0,9400]`, 读后 `0x11a090d` 将 `<=0` 钳位至 1, 共 18,338 行)
  - `Tdvi` (`TEAM+4..7`, `+0x50`, i32→t25, get `0x11b064f`, set `0x11b4cd3`, 54,518 live / 29,989 null / 0 miss;错配 UID 53,989 miss)
  - `Tndi` (`TEAM+12..15`, `+0x58`, i32→t25, get `0x11afe92`, set `0x11b4ed6`, 2,269 live / 82,238 null / 0 miss;错配 UID 2,179 miss)
  - `Tsti` (`TEAM+16..19`, `+0x78`, i32→t21, get `0x11afbe0`, set `0x11b4e54`, 56,845 live / 27,662 null / 0 miss;错配 UID 54,903 miss)
  - `Todo` (`TEAM+29..32`, `+0x68`, i32→t25, get `0x11b00b6`, set `0x11b4d27`, 1,740 live / 82,767 null / 0 miss;错配 UID 1,740 miss)
  - `Tnod` (`TEAM+48+4*vec38`, `+0x70`, i32→t25, get `0x11afe9e`, set `0x11b4ee2`, 1 live / 84,506 null / 0 miss;错配 UID 1 miss)
  - `Ttyp` (`TEAM_BASE+0`, `+0x28`, i8 enum `tmty`, get `0x11c338a`, set `0x3e98747`, 12 个观测值全落 `enums['tmty']`, 0 违例)
  - `Tisn` (`TEAM_BASE+1`, `+0x2f`, u8 bool, get `0x11c31e4`, `{0:84256, 1:251}`, 与 `selector==11` 完全等价)
  - `Tlna` (`TEAM_BASE+10`, `+0x18`, `u32 len + utf8`, get `0x11c2b8e`, set `0x3e986ce`, 1,741 行内嵌有效 UTF-8 / 0 错,空串回退 `0xdbe020`)
  - `Tsna` (`TEAM_BASE` 紧随 `Tlna+1B`, `+0x20`, `u32 len + utf8`, get `0x11c2c46`, set `0x3e9873f`, 1,741 行内嵌有效 UTF-8 / 0 错)
- **`held`(2 项)**:`rdui` (84,507/84,507 抑制)、`PLgn` (`TEAM_BASE_GET 0x11c277d` 转发 `(*(TEAM+0x30))+0xb9` 且无作用域枚举定义,沿用 t57/t59 口径)。
- **非 wire / 转发 / 计算(12 项)**:`Tmtd` (`0x11afa23` 读主队 `Tdvi`)、`Ccti` (`0x11c2a69 → 0x11c33f5` 转发 owner)、`Ccba` (`0x11c2a51 → 0xe89a00` / set `0x3e98681 → 0xe82aa0`)、`Ctbu`/`Crmb` (`TEAM` slot 10 `0x11ba5c5`/`0x11ba5ad` 返回 owner `CLUB*`)、`Crkt` (`TEAM_BASE_SET 0x3e986c6` 仅写转发至 `CLUB_SET`)、`Clri`/`Cnti` (TEAM 上无 getter)、`dbnm`/`dAPw` (`DATABASE_RECORD_GET` 虚拟名)、`NDBC`/`FDBC`。
- **内部 wire 槽**:`Tldi` (`TEAM+8..11`, `+0x60`, 41,712 live→t25, 0 miss;即 `CLUB.Cldi` 转发目标)、`owner@+0x30`(84,256→t3 club + 251→t9 nation, 0 miss)、`squad_vec38@+0x38`(max 145)。t59/t75 的 `WpBn`/`dbty` 邻接结论仅引用不重判。

---

## 4. `table_extra_24.dat` 静态绑定(`TEAM+0xa0`)与 82B 行框自证

- **静态绑定链**:
  1. `0xf5167e..0xf51694`(受 `r13b` server 标志门控,故 client 缺失)取 `[db+0x98]` (`DATABASE_TABLE<TEAM>`)调用 `0xf55340 → 0x3bb9b00`。
  2. `0x3bb9b37..43` 调 `0x3cefbe0(..., extra=1, old_save=0)` + `.dat` 拼出 **`table_extra_24.dat`**。
  3. 循环读取 `u32 count` (`84,507`)与每行 `u32 ordinal` (`0x3bb9bf9`),在 `context+0x80` 查既有 `TEAM*` 后调 `0x11a1580(team, stream, 1)`。
  4. `0x11a15ad..0x11a15fa` 分配 `0x118` B 对象(`0x3e67f80`)并写入 **`TEAM+0xa0`**(与 t71 `table_extra_3.dat → CLUB+0x100` 完全同构)。
- **82B 定长行框自证(数据 + 静态双闭合)**:
  - **任意对齐全链搜索**(`start ∈ [0..199], stride ∈ [4..500]`)仅得 **唯一解 `(start=12, stride=82, footer=0)`**,`12 + 84,507 × 82 + 0 = 6,929,586 B` 精确至 EOF。
  - **头/尾灵敏度**(`h ∈ [0..20], f ∈ [0..16]`):13 组整除组合中仅 `(h=12, f=0, stride=82)` 获得 `84,507 / 84,507` 序号匹配(其余 12 组 `<= 1`)。
  - **文法闭合**:`0x11a160c..0x11a1b2a` 逐字节覆盖 `@0..81`;其中 6 个可变段(`h80@49, h68@53, ha0@62, hd0@64, ha8@65, h98@66`)在全档 84,507 行均为 0,尾段 `h10e@70` 长度恒为 8,静态解释为何在当前库中退化为严格 82B 定长。
  - **与既有边界相容**:保留 t66 "只取 ordinal" 的旧任务范围边界不动;与 `extra_tables_verdict.json` L1 观察(仅 `@10/@11/@81` 三个字节变化)完全一致。
- **已绑定字段槽位**:
  1. **`Twhm` (L3)**:`extra+0x109` (`@10`, 1B i8, `day_of_week`, `club.xml[59]`),`TEAM_GET 0x11b0406` (抑制 0)/`TEAM_SET 0x11b4e6c`,并由 `CLUB_GET 0xe8bf39 → 0xe8eb48` / `CLUB_SET 0xe83056 → 0xe8489b` 经 `CLUB+0x18` 转发;73,732 为 0(抑制),10,775 live 全落 `1..7` (周六=6,451/周日=3,848 主导,0 违例)。
  2. **`Tmhm` (L3)**:`extra+0x10a` (`@11`, 1B i8, `day_of_week`, `club.xml[60]`),`TEAM_GET 0x11afa0b` (抑制 0)/`TEAM_SET 0x11b4d75`,由 `CLUB_GET 0xe8c68a` / `CLUB_SET 0xe83c56` 经 `CLUB+0x18` 转发;77,610 为 0(抑制),6,897 live 全落 `1..7` (周三=3,786/周二=2,669 主导,0 违例)。
  3. **`Tpvr` (L3 内部 4CC,不在 `field_codes`)**:`extra+0xf8` (`@21..22`, 2B i16),`TEAM_GET 0x11afb1f` / `TEAM_SET 0x11b4c79` (`Trpc 0x11aff6c` 计算 `Trep - Tpvr`),全档恒为 `1`。
  - 注:尾段 `@74..81` (`+0x10e` 8B) 中 `@81` 取值 `{0:79890, 2:4616, 99:1}`,但无 getter/setter 4CC 命中,记为未命名静态成员。

---

## 5. `CLUB+0x18` 转发链与六个 held `club.xml` 字段升 L3

### 5.1 装载与 Fixup 静态链

- `CLUB` 基类 reader `0x11d0d30` 调 `0x11d10e0` 在 `server_db/table_3.dat` 读入 `base18` (`u8 count` × `i32` ordinal) 至 `[CLUB+0x18 .. CLUB+0x20]`。
- `CLUB` slot 20 fixup `0xe5c550` 调 `0x11d2580` (`0xe5c979`),在 `0x11d25a8..0x11d2619` 通过 `[db+0x98]` (`DATABASE_TABLE<TEAM>`) 调 `0xf7e440 → 0x3bf3460` 将每个 ordinal 解析为 `TEAM*`。
- 全档 84,259 家俱乐部验证:`82,515` 家拥有 `>=1` 支球队,`1,744` 家为 0 支;`0 / 82,515` 家首队 `Ttyp ∈ {0x16, 0x2c}`(即直取 index 0 与 `0x11f41d0/0x11f6cf0` 跳过 `0x16/0x2c` 的首个非跳过队 100% 重合);`82,515 / 82,515` 首队满足 `team.owner(+0x30) == club_ordinal` 且 `Tisn == 0`。

### 5.2 六个 `club.xml` 发生位完整链路(均升 L3,标注 **经 +0x18 转发的投影**)

| `club.xml` 字段 | 目标 `TEAM` 4CC / 偏移 | Getter 链 (`editor.exe` fo) | Setter 链 (`editor.exe` fo) | 全档值域验证 (82,515 有队 + 1,744 无队) |
|---|---|---|---|---|
| **`Crep`** `[31]` | `Trep` (`+0xa8`, t24 `TEAM+2`) | `0xe8be31 → 0xe8ea2e` (直取 `**(CLUB+0x18)`,空则 1500) | `0xe84049 → 0xe851bf → 0x3c951a0` (钳位 `1..10000`) | `[0,9400]` 原值 (`[1,9400]` 读后钳位) `⊂ [0,10000]`, 0 违例 |
| **`Cdvi`** `[125]` | `Tdvi` (`+0x50`, t24 `TEAM+4`) | `0xe8b939 → 0xe8b945` (直取首队 `[+0x50]`) | `0xe83f65 → 0xe84fdf` (`0xe8501f` 写 `[+0x50]`) | 52,900 live / 29,615 null → t25 0 miss (错配 UID 52,372 miss) |
| **`Cldi`** `[126]` | `Tldi` (`+0x60`, t24 `TEAM+8`) | `0xe89f6d → 0xe8d14d → 0x11f41d0 → 0x11afe0d` | `0xe842ed → 0xe842f9 → 0x11f6cf0 → 0x11b4cdf` | 40,617 live / 41,898 null → t25 0 miss (错配 UID 40,158 miss) |
| **`Cndi`** `[128]` | `Tndi` (`+0x58`, t24 `TEAM+12`) | `0xe8ab0d → 0xe8ab19 → 0x11f41d0 → 0x11afe92` | `0xe82d8d → 0xe82d99 → 0x11f6cf0 → 0x11b4ed6` | 2,167 live / 80,348 null → t25 0 miss (错配 UID 2,078 miss) |
| **`Codi`** `[130]` | `Todo` (`+0x68`, t24 `TEAM+29`) | `0xe8b7d8 → 0xe8e3f5 → 0x11f41d0 → 0x11b00b6` | `0xe83ad2 → 0xe854ac → 0x11f6cf0 → 0x11b4d27` | 1,723 live / 80,792 null → t25 0 miss (错配 UID 1,723 miss) |
| **`Csti`** `[57]` | `Tsti` (`+0x78`, t24 `TEAM+16`) | rel32 `0xe8a03f` `0xe91d8c[8]` → `0xe8cf2f → 0x11f41d0 → 0x11afbe0` | rel32 `0xe82ce9` `0xe86b38[6]` → `0xe84537 → 0x11f6cf0 → 0x11b4e54` | 55,498 live / 27,017 null → t21 0 miss (错配 UID 53,665 miss) |

---

## 6. 锚点对照与既有负结果保留

### 6.1 球场与俱乐部经 `+0x18` 实测锚点

- **Anfield** (t21 row 67, UID 676):`Scpy=50,109`, `Scti=1061` (Liverpool UID 100047), `Slat=53.430820, Slon=-2.960832`, `Sowi=460` (Liverpool);反向 **Liverpool** (club 460, UID 676) → `base18[0]=team 586 (UID 676)` → `Crep=8700`, `Cdvi=7` (comp UID 11), `Csti=67`。
- **Old Trafford** (t21 row 71, UID 680):`Scpy=74,031` (保留 b47 旧负结果:不等于公开 74,140), `Slat=53.463058, Slon=-2.291336`;**Man Utd** (club 464, UID 680) → `team 590` → `Crep=8550`, `Csti=71`。
- **Santiago Bernabéu** (t21 row 430, UID 1056):`Scpy=81,044`, `Slat=40.453022, Slon=-3.688375`;**Real Madrid** (club 1297, UID 1736) → `team 1495` → `Crep=9150`, `Cdvi=51` (comp UID 67), `Csti=430`。
- **Allianz Arena** (t21 row 12048, UID 8700726):`Scpy=75,000, Sscy=54,511`, `Slat=48.218803, Slon=11.624716`;**FC Bayern** (club 623, UID 915) → `team 800` → `Crep=8800`, `Cdvi=16` (comp UID 22), `Csti=12048`。
- **Arsenal** (club 387 → team 513 → `Csti=7718`, `Scpy=60,704`)、**Chelsea** (club 415 → team 541 → `Csti=27`, `Scpy=41,837`)。

### 6.2 保留的既有负结果与边界

1. `db_tables_big.json` table 21 全部原始 `negative_results` 原文保留于 `xref_stad_team.json`(含 Old Trafford `74031 != 74140` 差异、以及 L4=0 声明)。
2. `extra_tables_verdict.json` 对 `table_extra_24.dat` 的全部 L1 否定模型(offset table / length table / index_string 伪证)原文保留。
3. t66 对 `table_extra_24.dat` "只取 ordinal" 的任务边界保持不变;t59/t75 的 `WpBn`/`dbty` 邻接结论仅引用不重判。
4. `t01_anchors.py` 7/7 回归通过;独立校验脚本 `scratch/t79/out/verify.py` (不 import builder/`t05_pe`/`ReaderCFG`/`fm24_dump`) 12/12 全通过。
