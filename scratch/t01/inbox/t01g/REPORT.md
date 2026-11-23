# t01-g：nation 序列化器侦察

## 结论与验收

按 `scratch/t01/inbox/t01f/REPORT.md` 复刻“虚表入口 → 固定宽度指令 → 累加游标 → 4CC 成员访问”方法，但 nation **未达到 COMP 式直线序列化的 ≥10 字段/三行验证**。已满足任务书的负结果分支：nation reader 存在参数分支、计数驱动集合循环和不同字段处理；不能把 COMP 的固定顺序布局直接套给全部 nation 模式。当前仅有 7 个带 4CC 的前缀字段 L3 映射；不冒称完整解码。证据与字节逐项见同目录 `output.json`。

## 类、工厂与虚表（editor.exe file offsets）

- RTTI `.?AVNATION@db@@\0`：`0x1aacac0`；vptr `0x18889b8`，其 `[-8]` 指向 COL `0x1888bb0`。COL 的 type RVA 字段在 `0x1888bbc`（`b0 da aa 01`），回指 TypeDescriptor `0x1aacab0`。各处原字节、VA 和 PE SHA-256 已记录在 JSON；外部二进制只读。
- type-10 工厂表：基址由 `0xf48b45` 得到 `0xf49d38`；type-10 项 `0xf49d60: ef f1 ff ff` → handler `0xf48f27`。此处 `b9 d8 01 00 00` 请求分配 `0x1d8` 字节，`0xf48f37: e8 b4 5c 0f 00` 调构造器 `0x103ebf0`。构造器 `0x103ec17: 48 8d 05 9a 9d 84 00`、`0x103ec1e: 48 89 01` 写入 `0x18889b8`。slot 7 查询函数 `0x104e4b0: b8 0a 00 00 00 c3` 返回 10。`0xf49d9c` 的 type-25 项另落到 `0xf49129`，作为负对照。
- 0-based slot 19：vtable `0x1888a50` → reader `0x103fac0`；slot 21：`0x1888a60` → writer `0x1041460`。入口指针字节、VA 与入口指令均在 JSON。

## 可证明的前缀映射

以下 `row+` 是该 reader 普通路径的**body 游标**，不是已恢复的所有 251 行边界。每项都由 reader 的 `[r15+disp]`、`mov r8d,N`、stream slot `+0x28` 三处指令累加；4CC getter 再将成员连回 schema。文件偏移均为 editor.exe file offset，精确字节在 JSON 的 `serializer` / `field_getter_link`。

| 4CC / schema 名 | body row+ / 宽度 | 对象 + | reader dest / width / call | getter cmp / member |
|---|---:|---:|---|---|
| `Ngct` Gain Nationality Type | 0 / 1 | `0x1cb` | `0x10405b4 / 0x10405be / 0x10405c7` | `0x1042385 / 0x1042a47` |
| `Ncti` Continent | 1 / 4 | `0xf0` | `0x10405d8 / 0x10405e2 / 0x10405eb` | `0x104218a / 0x1042ed7` |
| `Nrgi` Region | 5 / 4 | `0xf8` | `0x10405fc / 0x1040606 / 0x104060f` | `0x10424e5 / 0x10424f1`（`jne` 默认边，等值走 fallthrough） |
| `Ncur` Currency | 13 / 4 | `0x100` | `0x1040644 / 0x104064e / 0x1040657` | `0x1042196 / 0x1042c7d` |
| `Nsod` State Of Development | 17 / 1 | `0x1cc` | `0x1040668 / 0x1040672 / 0x104067b` | `0x1042268 / 0x1042e6f` |
| `Necf` Economic Factor | 18 / 1 | `0x1d0` | `0x104068c / 0x1040696 / 0x104069f` | `0x10421a2 / 0x10421ae`（`jne` 默认边，等值走 fallthrough） |
| `Nygn` Years To Gain Nationality | 23 / 1 | `0x1cd` | `0x10406d4 / 0x10406de / 0x10406e7` | `0x1042078 / 0x1042aaf` |

普通 reader 路径前 25B 的传输宽度为 `1,4,4,4,4,1,1,4,1,1`。对象 `+0xe8`（row+9）、`+0x1b4`（row+19）和 row+24 的栈暂存 byte 保留为未命名；没有猜语义。解压 payload `+0x0e` 的 25B 为 `01 00 00 00 00 07 00 00 00 a3 04 00 00 01 00 00 00 02 0d 00 00 00 00 07 03`，与此**候选首 body 前缀**逐宽度吻合；记录边界/索引尚未独立恢复。

## 负结果与 switch 覆盖边界

- slot-19 reader 在 `0x103fadc` 载入参数并于 `0x103fae6: 0f 84 c4 0a 00 00` 分支到普通路径 `0x10405b0`。该普通路径前缀的 row+24 暂存 byte 在 payload `0x26` 为 `03`；代码 `0x1040728` 取此计数、`0x1040736/0x104073b` 检查空列表，随后以 `inc/cmp/jl`（`0x1040773/0x1040775/0x1040779`）循环。其后还有 4B count（`0x10407a7/0x10407b0`）与循环（`0x1040841/0x1040843/0x1040847`）。另一个参数分支读 2B 计数（`0x103fb2e: 41 b8 02 00 00 00`、调用 `0x103fb37`），循环内重复读 4B（`0x103fcb1: 41 b8 04 00 00 00`、调用 `0x103fcbd`），并有 `inc/cmp/jge`（`0x103fc90/0x103fc98/0x103fc9b`）。这些指令证明存在计数驱动集合路径；不把参数分支擅自命名为 client/server。
- writer slot 21 有独立 1B prelude（`0x1041478`, `0x1041485`, `0x104148e`），随后普通 body 从 `0x1041832` 的对象 `+0x1cb` 开始。prelude 与表 payload 的 14B framing 不被误算成固定 nation stride。
- t01b 的 COMP 专用 `0xec0000..0xec6000` / `0xeca000..0xecc000` 区间不直接代表 nation getter。nation slot-2 getter 实现在另一段（入口文件偏移 `0x1041f30`，扫描窗 `0x1041930..0x1045300`）；此窗找到 19 个精确 `cmp esi,imm32` 的 nation schema 码，包括上述 7 个。346 码未全映射；19 是该窗的扫描结果，不表示其余码在整个 exe 中不存在。
- 冻结 locator 的 SHA-256 与 `evidence/MANIFEST.json` 一致。table_10 解压成员 SHA-256 为 `7e9d…f6c34`，251 行、版本 3569。`payload@0x1046: 6e 00 00 00 6e 00 00 00` 复现 `duni=472446402670`；其前一 dword `37 00 00 00` 保持未赋义。快照明确说该处不是已验证 row index。未做 3+ 行字段值核对。

## 边界与复验

目前没有完整变长行解析、所有 251 个 row start、三行字段值核验或 346 个字段映射；L4=0。输入 archive、editor.exe、旧库快照均只读；未启动游戏/editor/IDA，未安装依赖。冻结快照 SHA-256 在 `output.json`。

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01g/verify.py --help
py -V:3.12 -I -B scratch/t01/inbox/t01g/verify.py --selftest
```

`--selftest` 重建证据并检查错 type-25、错误提升 opaque 槽、声称三行已验证三个负对照。仅 `--write` 写同目录 `output.json`。
