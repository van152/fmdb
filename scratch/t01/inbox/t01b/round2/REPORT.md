# t01-b 第二轮报告

## 结论

- 跨 comp/club/stadium 注册代码确认均以 `0x38` 步进；比较两组 switch 的 `call helperB; add rax,N` 后，N 是运行时对象偏移，不是 56B 描述符内成员。未推断出 vtable 后的类型、名字缓存或值区；+0 沿用 E11/E14 基线。
- comp/club/stadium 的实体接口表均在 slot 6 放置对应注册函数。对构造器/容器消费端的只读扫描没有定位到具体实现。
- switch setter 可见标签为 `cont`、`Nnat`、`city`；另有未被 je-only JSON 收录的 cpcm fall-through 路径使用 `comp`。这些与 schema 的数据库引用表类型吻合，不是整数/字符串/日期 wire-type 证据。

## 1. 56B 描述符：跨实体约束

- comp 注册：off `0xebf057` `e8 94 da 97 ff`，`0xebf05c` `48 83 c0 38`；club 注册：off `0xe87d6b` `e8 80 4d 9b ff`，`0xe87d70` `48 83 c0 38`，`0xe87d74` `c7 45 f8 6d 61 6e 43`（Cnam）；stadium：off `0x1185037` `e8 b4 7a 6b ff`，`0x118503c` `48 83 c0 38`。
- comp direct 样本：cext off `0xec3631` `e8 ba 94 97 ff` → `0xec3636` `48 83 c0 18`；crep off `0xec3811` `e8 da 92 97 ff` → `0xec3816` `48 83 c0 28`；cmnl off `0xec33cf` `e8 1c 97 97 ff` → `0xec33d4` `48 83 c0 68`。本轮扫描得到 N 分布 `0x18:2, 0x28:18, 0x68:3`。
- club 两组 switch 样本：C4mn off `0xe84ea4` `e8 47 7c 9b ff` → `0xe84ea9` `48 83 c0 08`；C2g3 off `0xe8cd4e` `e8 9d fd 9a ff` → `0xe8cd53` `48 83 c0 18`；`name` off `0xe8d7de` `e8 0d f3 9a ff` → `0xe8d7e3` `48 83 c0 38`；CLat off `0xe8dc78` `e8 73 ee 9a ff` → `0xe8dc7d` `48 83 c0 68`。两簇合计 N 分布 `0x08:2, 0x18:30, 0x28:57, 0x38:1, 0x68:1`。
- comp 与 club 共用 `0x18/0x28/0x68`；`0x68 > 0x38`。这些样本都从 helperB 返回值加 N，不能据此给 56B 描述符分配字段；+0 之后仍无新成员证据。

## 2. 注册接口表与构造器路线

- comp 表：file off `0x187d2b0`，slot 6 在 `0x187d2e0` bytes `40 fa eb 40 01 00 00 00` → VA `0x140ebfa40`（注册函数 raw `0xebf040`）。
- club 表：file off `0x187c300`，slot 6 `0x187c330` bytes `50 87 e8 40 01 00 00 00` → VA `0x140e88750`（raw `0xe87d50`）；另一个同目标表在 `0x18bf1f0/0x18bf220`。
- stadium 表：file off `0x188d1d0`，slot 6 `0x188d200` bytes `20 5a 18 41 01 00 00 00` → VA `0x141185a20`（raw `0x1185020`）。三类表均把注册方法置于 `+0x30`。
- 直接 E8/E9 xref 按各 PE section 的 raw→RVA 映射扫描，指向 comp 注册起点的命中为 0。全文件未找到 vtable base VA `0x14187dcb0` 的绝对 qword 引用；`.reloc` 中对其 `0x160` 字节范围的常见 RIP-relative MOV/LEA 扫描也无命中。`.reloc` 有通用 `call [rax+0x30]`（例如 off `0x1b9d96c` `ff 50 30`），但无法关联到这张表。
- 结论：三实体 slot-6 对照锁定了同一注册接口；数组构造器和 helperA 容器消费端仍未定位，不能把通用虚调用当作消费端证据。

## 3. `0xfe72b0` 标签

- 当前 `t01b_switch_cases.json` 中 `setter_rva` 项为 0；从原始 handler 重提：ccti 调 `0xfe7860`（off `0xec379a` `e8 c1 36 12 00`），setter off `0xfe6e90` `ba 74 6e 6f 63` / `0xfe6e95` `e8 16 fa ff ff` → `cont`；cnti 调 `0xfcc110`（off `0xec3788` `e8 83 7f 10 00`），setter off `0xfcb740` `ba 74 61 6e 4e` / `0xfcb745` `e8 66 b1 01 00` → `Nnat`；csou 调 `0xfe76a0`（off `0xec39ff` `e8 9c 32 12 00`），setter off `0xfe6cd0` `ba 79 74 69 63` / `0xfe6cd5` `e8 d6 fb ff ff` → `city`。
- cpcm 的第一 switch 用 `cmp` 后 `jne default`、相等时 fall-through：off `0xec0a9d` `81 fe 6d 63 70 63`、`0xec0aa3` `0f 85 55 3d 00 00`；handler off `0xec0ab1` `e8 ea 60 12 00` 调 `0xfe75a0`。setter off `0xfe6bd0` `ba 70 6d 6f 63`、`0xfe6bd5` `e8 d6 fc ff ff` → `comp`。该路径被当前 je-only 提取器漏掉。
- 按各 PE section raw→RVA 映射扫描 `BA imm32; E8` 到 helper file off `0xfe68b0`：122 个 direct call refs 中，21 个紧邻 `mov edx,imm32`，得到 17 个不同字面标签：`Ttea, Nnat, comp, awrd, lang, Cclu, city, curr, injr, MedS, stad, wthr, regi, cont, lcrg, stgn, agrm`。`output.json` 为每个标签列出原始 file offset、指令 bytes 与 call bytes。
- comp schema 快照中 ccti/cnti/cpcm/csou 均为 `database_record_unique_id`，对应表分别是 continent/nation/competition/city（`master.json` SHA-256 与 MANIFEST 一致）。因此 switch 中观测的标签是引用目标类别，不支持整数/字符串/日期 wire-type 映射。122 个 call 中其余非相邻/动态参数路径仍未全部分类。

## 未解与交付

- 未找到描述符 +0 之后的成员布局、数组构造器或注册容器消费端；不推断行偏移。
- 类型标签结论限定于已命中的静态直接标签；不是完整 wire-type 清单。
- 交付：`round2/output.json`、`round2/REPORT.md`。
