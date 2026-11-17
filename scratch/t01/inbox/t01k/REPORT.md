# t01-k：BASIC_PERSON 变长行字段映射

## 结论

按任务书允许的负结果线验收：**未达到 ≥10 个固定行偏移字段**。类号不能单独决定 reader 游标：对 class-4，`cmp al,4` 之前先经过一个由全局状态选择的 4/8B 读取；class 1/2/3 另有两组 4/8B 互斥分支，且 `object+0x38` helper 的游标增量未闭合。**不把 t01-j 的 1+2+2 局部对齐当成完整 class-4 路径。**

- BASIC_PERSON slot-19 reader：`editor.exe+0x187b3c0: 70 fd e4 40 01 00 00 00` → `+0xe4f370: 41 57 41 56 56 57 55 53 48 83 ec 48`。slot-2 getter 指针 `+0x187b338: d0 0c e5 40 01 00 00 00` → `+0xe502d0`；此 getter 用 EDX 比较 4CC（不要求一定是 ESI）。RTTI、112B 分配及 type query 沿用 t01-j/t01-h 锚点。
- 独立重走 `.dat` 全部 658,011 行：压缩输入 SHA-256 `2ac7da37…d67f48bc`，解压 payload SHA-256 `16709b0b…c9589d35a5`。`payload+0x0: 5b 0a 0a 00`（count 658,011），首行 `payload+5`；长度 1/2/3=83B、4=34B、5=22B；计数 `166064/476158/4757/9839/1193`。每行末 12B 的 ordinal 连续，后两 dword 全量相等；`payload+0x338e402: 00 00 00 00 01 4c bd 54 77` 为 EOF 前 9B。偏移均属解压 payload。5 个样本行原字节在 `output.json`，`verify.py` 全量复验。

## class-4：`1+2+2` 之前存在游标分派

1. reader 先读 class byte：`+0xe4f393: 41 b8 01 00 00 00`，目的 `+0xe4f38b: 48 8d 71 65`。之后 `+0xe4f3c8: ba 20 00 09 00`（mask `0x90020`）、`+0xe4f3cd: 0f a3 ca`；class 4 的 bit 4 清零，`+0xe4f3d0: 0f 83 ff 00 00 00` 跳到 `+0xe4f4d5`。
2. 在 class-4 比较之前，`+0xe4f4dc: 48 8d 53 30` 设定 object+0x30 目的；宽度受两全局状态读取影响：`+0xe4f4f6: 41 b8 08 00 00 00` 或 `+0xe4f4fe: 41 b8 04 00 00 00`，之后 `+0xe4f507: ff d0` 调流方法。选择器位于 `+0xe4f4d5: 80 3d 77 04 d1 00 00`、`+0xe4f4ed: 80 3d 38 fd d0 00 00`；本任务未运行程序取其运行时值。`+0xe4f51c: 0f 86 c5 fe ff ff` 再回到第二类掩码测试。
3. 第二掩码 `+0xe4f3e7: ba 70 01 0d 00` 含 class-4 bit 4，随后才到 `+0xe4f42e: 3c 04`。class-4 路径的两个 2B 读取确实存在：目的 `+0xe4f432: 48 8d 53 52` / 宽度 `+0xe4f43c: 41 b8 02 00 00 00`；目的 `+0xe4f452: 48 8d 53 5a` / 宽度 `+0xe4f468: 41 b8 02 00 00 00`。但它们的行偏移依赖前置宽度 W：分别是 `row+2+W`、`row+4+W`，即 W=4 时 +6/+8，W=8 时 +10/+12，而非仅按 class 比较得到的 +2/+4。
4. class-4 样本 `payload+0x13b29` 原字节以 `11 04 af 00 00 00 21 03 00 00 64 00 6c 07` 开始。它同时含候选跨度 `+2..5`、`+6..9`、`+10..13`，但不能静态决定本次运行选择哪个 W。reader 直接宽度合计 `1+W+2+2`；身份块从 row+22 开始，剩余前身份字节尚未赋名/定位，不能视作 padding。

## 4CC getter 对齐与边界

`person.xml#pers`（master SHA-256 `7d57477e…92776eda`）共 271 码。slot-2 getter 的 10 个 4CC→对象成员链及每条 `cmp/branch/member` 原字节见 `output.json.getter_to_object_member`。其中 9 个是业务码；`duni` 的 getter 访问 object+0x0c，但在此任务未证明其 BASIC_PERSON reader 行内来源，排除出业务计数。

| 4CC / schema | getter 成员（editor.exe offset: bytes） | reader 对齐结论 |
|---|---|---|
| `Ptyp` Person Type | `e50959: 81 fa 70 79 74 50` → `e50965: 0f be 7f 65` | `e4f393: 41 b8 01 00 00 00` 写 object+65；固定 `row+1`，唯一已闭合固定字段 |
| `Pdob` Date Of Birth | `e506a5: 81 fa 62 6f 64 50` → `e51158: 0f b7 7f 5a` | reader 的 object+5a 有 class-4 2B 读取 `e4f468: 41 b8 02 00 00 00`；row offset 为 +8 或 +12，取决于 W |
| `Pnti` Nation / `Pcti` Club / `Pnai` Nation | getter 分别访问 object+30/+20/+28；字节详见 JSON | reader 在 `e4f4f6/e4f4fe`、`e4f542/e4f54a`、`e4f57f/e4f587` 各有互斥 8/4B；行起点依前序宽度变化 |
| `PCJO` Job / `PSJO` Secondary Job / `PNJO` Job / `Piap` International Apps | getter 分别访问 object+5e/+60/+62/+64；字节详见 JSON | 对应 reader 2/2/2/1B 指令，但行游标经过未闭合 helper `e4f5a3: e8 f8 2b 16 00` → `fb21a0: e9 5b 6b e2 02`，不报告固定偏移 |

width census 共 27 个 `mov r8d,N`：reader 本体 23 个，另 4 个在 callee 窗口；不可把互斥宽度指令拼成线性字段序列。reader 本体准确的 2B 槽是 9 个（`e4f5fa..e4f6fa`），不是把范围描述误数成 10 个。

## 验收、负对照和复验

- 固定 L3 行偏移只证明 `Ptyp@row+1`，共 1 个；其余 getter→成员证据保留为条件/未闭合，未宣称达成 10 字段验收。
- 负对照：class-4 `0x90020` bit4 清零、`0xd0170` bit4 置位；8B/4B 两臂由 `e4f4eb: 74 11`、`e4f4f4: 75 08` 分流，不可相加。样本身份块和全量行链由脚本重验；不赋予重复 ID `duni/rdui` 语义。
- 未启动游戏、编辑器或 IDA；无外部输入写入；L4=0。仅输出在本目录。

```powershell
py -V:3.12 -I -B scratch/t01/inbox/t01k/verify.py --help
py -V:3.12 -I -B scratch/t01/inbox/t01k/verify.py --selftest
```
