# t04 — club 字段级 L3 行偏移（部分交付）

## 结论

- club schema **433** 个字段中，本次闭合 **1 个 L3 字段**：`Cccn @ row+8, width=4`。
- 另外 3 个 getter 与 reader sink 的成员偏移相同，但行游标未闭合，保留为候选，不计数：`Cdof`、`Cprs`、`Ctsi`。
- 目标 ≥30 未达成。当前可证明数是 1；这不是对整个 reader 可解字段数的理论上限判断。**卡点**是 CLUB reader 在首 20B 后分支游标分裂，随后 helper 产生动态宽度；`LEAGUE_BODY_CLUB` reader 还有未展开循环，且 RTTI 到实际行类的 partition 未证实。
- 机器结果：`output.json`。未改写任何输入/旧底稿；未启动游戏、编辑器、IDA，也未安装依赖。

## 已闭合字段

| 字段 | row 偏移/宽度 | 对象成员 | 证据链 |
|---|---:|---:|---|
| `Cccn` (Continental Cup Nation) | **+8 / 4B** | `+0xf0` | getter `editor.exe@0xe8b7bf: 81 fb 6e 63 63 43`（cmp 4CC）→ `@0xe8b7cb: 49 8b 8c 24 f0 00 00 00`（读 `[this+0xf0]`）；CLUB slot19 reader `@0xe5a864: 49 8d be f0 00 00 00`、`@0xe5a86e: 41 b8 04 00 00 00`、`@0xe5a877: ff 50 28`。transfer 唯一游标候选为 `[8]`，无该事件路径不确定标志。 |

行数据抽验（解压 member 内偏移）：row 69709 起点 `0x570ec7`，row+8 的 `0x570ecf` 为 `85 00 00 00`。它与 row+0 的样本值相同；记录该现象但不据此推断引用目标或属性值语义。member 全量 SHA-256 `db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f`，84,259 行。

## 候选与未闭合段

- `Cdof`：getter `@0xe8b17c: 81 fb 66 6f 64 43`，读成员 `+0x148`；reader sink `@0xe5aa69: 49 8d be 48 01 00 00`，width `@0xe5aa73: 41 b8 02 00 00 00`，call `@0xe5aa7c: ff 50 28`。游标候选 `[0,1,20,21]`，无法择一。
- `Cprs`：getter `@0xe8c48d: 81 fb 73 72 70 43`，字段读取 `@0xe8d46f: 41 0f be b4 24 6a 01 00 00`（成员 `+0x16a`）；reader sink `@0xe5a9c0: 49 8d be 6a 01 00 00`、call `@0xe5a9ea: ff 50 28`。游标候选 `[0,20]`，宽度动态/未闭合。
- `Ctsi`：getter `@0xe8c57d: 81 fb 69 73 74 43`，读成员 `+0x140`；reader sink `@0xe5bbef: 49 8d b6 40 01 00 00`，call `@0xe5bc1f: ff 50 28`。宽度候选 `[1,2]`，没有确定行游标。
- CLUB reader 前五项的 wire 游标 `[0,4,8,12,16]` 与既有底稿一致；只有 `+8` 找到上述 4CC 闭合。它们前面的分支 `@0xe5a801: 0f 84 c9 00 00 00` 跳至 `0xe5a8d0`，使下一 6B transfer `@0xe5a921: 41 b8 06 00 00 00` / `@0xe5a92a: ff 50 28` 保留 `[0,20]` 两候选。
- 首个游标失效点：`@0xe5a952: e8 b9 97 9b ff` helper；之后 `@0xe5a95d: 4c 8b 45 18` 从栈槽取动态宽度，`@0xe5a976: ff 50 28`。下游候选不升级为结论。
- `LEAGUE_BODY_CLUB` reader body `0x43beba0` 有 33 个 transfer events，count-loop 未展开；当前也没有把 RTTI 独立绑定到具体 row ordinal 的证据。

Getter scan 以两 RTTI vtable 的 slot2 解析至同一入口 `0xe89a00`，对 4CC schema code 的 `cmp r32, imm32`（全寄存器，不限 `81 f8`）做线性窗口扫描：431 个四字符 code 中观察到 150 个不同比较值；与本次 reader 目的成员直接相同的只有上述 4 个字段候选，只有 `Cccn` 的 row cursor 单值闭合。剩余 **432** 个 schema 项均列入 `output.json.unclosed`，不按字段顺序或数值猜测。

## 来源与复核

- `editor.exe` 只读，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`。
- `evidence/fm24/reports/editor_schema/master.json` 使用快照；SHA-256 `7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda`，已与 `evidence/MANIFEST.json` 对照相符。
- 数据由现有 `scratch/t02/inbox/club_v2/solve.py` 的只读 loader 在内存读取，未运行会写 checkpoint 的主程序。Python 命令遵守 `py -V:3.12 -I -B`，未 pip install。
- 既有 `scratch/t02/field_mapper/out/REPORT.md` 中 t02c fixture 的 `0/11` 负结果保持原样；它以语义描述字段作 fixture，不能替代本次 4CC 对齐。

## 交付清单

- `scratch/t02/inbox/club_fields/output.json`
- `scratch/t02/inbox/club_fields/REPORT.md`
