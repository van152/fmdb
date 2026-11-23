# t01-b：字段描述符链静态复核

## 结论

- `editor.exe` 中的 comp/stadium 注册代码都以 `0x38`（56 B）步进描述符指针；但没有安全识别出原始描述符的任何成员，更未得到 `.dat` 行偏移。helperA 返回后的 vtable 访问对象已被改写，不能算作描述符成员证据。
- helperA 将 `{描述符指针, 4CC}` 复制到注册记录前缀，再把记录指针追加到容器。字节显示容器 slot 是 **8 B 指针**，不是 32 B 元素；`0x20` 是一处初始容器缓冲分配大小。
- ccti/cnti delegate setter 将两个 dword 转发给通用引用处理器；通用处理器中出现的 `helperB()+0x48` 仍是未解释的描述符/临时对象定位，不能当作行偏移。
- 两处字段 switch 都暴露运行时对象偏移（ccti `+0x58`、cnti `+0x60`、cpcm `+0x68`），但没有接到 table_25 行槽。新增 comp L3 行槽为 0。

## 来源与只读检查

- 分析对象：`D:/tmp2b/fm24/input/editor.exe`，74,807,296 B，SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`；哈希与只读来源登记 `evidence/fm24/reports/qa/IDA_PROVENANCE.md` 快照一致（该快照 SHA-256 `14e55d3c61c2ff7871eb943d6e0c7df6507cc597e0977829e526b80d12e7a789`，均与 `evidence/MANIFEST.json` 相符）。
- `.rdata` 地址换算沿用 `file offset + 0xA00 = RVA`，VA 再加 image base `0x140000000`。未启动游戏、编辑器或 IDA；未修改任何输入。

## 1. helperA 与 56 B 描述符

### helperA 参数及注册项

- comp ccti 注册点：off `0xebf150` bytes `c7 45 f0 69 74 63 63` 写入 ccti 4CC；off `0xebf157` `48 89 45 e8` 写入描述符指针；off `0xebf15b` `48 8d 7d e8` 取 pair 地址；off `0xebf15f` `48 89 f1 48 89 fa` 设 RCX/RDX；off `0xebf165` `e8 86 ba 97 ff` 调到 helperA file off `0x83abf0`（VA `0x14083b5f0`）。
- helperA 入口 off `0x83ac0d` `49 89 d6`（RDX→r14）、`0x83ac10` `49 89 cf`（RCX→r15）；off `0x83ac13` `48 8b 39`、`0x83ac16` `48 39 79 10` 检查容器 begin/capacity。故 RCX 是容器，RDX 是源 pair `{descriptor*, 4CC}`。
- off `0x83ad52` `49 8b 06`、`0x83ad55` `49 8b 4e 08` 读取 pair 两个 qword；off `0x83ad59` `48 89 4b 08`、`0x83ad5d` `48 89 03` 将它们复制到记录前缀 `[rbx+8]`、`[rbx]`。4CC 是第二 qword 的低 32 位；高 32 位语义未定。随后 off `0x83ad65` `48 83 c0 08`、`0x83ad71` `49 89 06` 将源 pair[0] 改写为 helperB()+8，pair[1] 清零（off `0x83ad69` `49 c7 46 08 00 00 00 00`）。
- 修正 helperA 容器元素解释：off `0x83ad7e` `48 89 1f` 写入记录指针，`0x83ad81` `49 83 47 08 08` 将 end 加 8；增长路径 off `0x83adca` `4a 8d 14 e5 00 00 00 00` 按 slot 数乘 8 计算容量，off `0x83adda` `48 89 1c 30` 复制指针 slot。off `0x83ac2b` `ba 20 00 00 00` 是 0x20 字节缓冲分配参数，不证明 vector 元素为 32 B。

### 56 B 步进与成员可见度

- comp：off `0xebf057` `e8 94 da 97 ff` 调 helperB；off `0xebf05c` `48 83 c0 38` 步进 56 B。helperA 之后，调用者在 off `0xebf1fa` `48 8b 4d e8`、`0xebf1fe` `48 8b 01`、`0xebf204` `ff 50 10` 对局部指针取 vtable；但 helperA 已在 off `0x83ad71` 将 pair[0] 改写，因此不能把该 vtable 访问归到原始 `+0x38` 描述符。
- 独立 stadium 验证：off `0x1185037` `e8 b4 7a 6b ff` 调 helperB；off `0x118503c` `48 83 c0 38`；off `0x1185040` `c7 45 f0 6d 61 6e 53` 注册 Snam；off `0x1185055` `e8 96 5b 6b ff` 调同一 helperA。紧随的 Scti 项在 off `0x118506c` 再次 `48 83 c0 38`。
- 描述符数组只确认了 `0x38` 迭代步长，没有直接确认原始描述符内任何成员。调用者的 vtable 间接访问属于 helperA 改写后的临时指针；原始描述符 `[+0..+0x37]` 仍未知。4CC 在独立 pair/注册记录中，不冒充描述符成员。

### 构造器路线及边界

- 对直接 E8/E9 rel32 目标 `0xebf040`（comp 注册函数）做全文件扫描：没有直接调用命中。找到一个静态 qword 地址引用：off `0x187d2e0` bytes `40 fa eb 40 01 00 00 00`，值为 VA `0x140ebfa40`；它仅是候选间接函数指针，不足以定位数组构造器。
- helperB file off `0x83caf0` 起始 bytes `e9 7b 0e f4 02` 跳入 `.reloc` 区域；不继续解壳。当前没有据此声称描述符数组分配/初始化函数已找到。

## 2. delegate setter 复核

- ccti caller：off `0xec3792` `49 8b 4c 24 58`，`0xec3797` `4c 89 f2`，`0xec379a` `e8 c1 36 12 00` 调 RVA `0xfe7860`（file off `0xfe6e60`）。setter off `0xfe6e6c` `8b 41 0c`、`0xfe6e6f` `8b 49 10` 读取输入对象 `+0x0c/+0x10`；空值分支 off `0xfe6e79` / `0xfe6e7e` 各写 `0xffffffff`；off `0xfe6e90` `ba 74 6e 6f 63` 传类型 tag `cont`，off `0xfe6e95` `e8 16 fa ff ff` 调共同处理器 RVA `0xfe72b0`。
- cnti caller：off `0xec3780` `49 8b 4c 24 60`、`0xec3785` `4c 89 f2`、`0xec3788` `e8 83 7f 10 00` 调 RVA `0xfcc110`（file off `0xfcb710`）。setter off `0xfcb71c` `8b 41 0c`、`0xfcb71f` `8b 49 10`；off `0xfcb740` `ba 74 61 6e 4e` 传 tag `Nnat`；off `0xfcb745` `e8 66 b1 01 00` 调同一共同处理器。
- 共同处理器 RVA `0xfe72b0`（file off `0xfe68b0`）将两个 dword 合成 64-bit 值：off `0xfe68e4` `8b 43 04`、`0xfe68e7` `48 c1 e0 20`、`0xfe68eb` `48 63 1b`。随后 off `0xfe68f1` `e8 fa 61 85 ff` 调 helperB、off `0xfe68f6` `48 83 c0 48` 加 0x48，并把结果放入临时 pair（off `0xfe68fe` `48 89 45 e8`）。该 +0x48 尚无 `.dat` 行语义。
- 这些 setter 没有显示 `mov [row+N]` 或可映射到 table_25 行的直接存储。`+0x0c/+0x10` 是输入包装对象成员，`helperB()+0x48` 是共同处理器中的未解释临时定位，均不升级为行偏移。

## 3. switch 与 `.dat` 桥

- XML/对象分发样本：off `0xec2007` `81 fe 69 74 63 63` 比较 ccti，相关 handler off `0xec3792` 取 `[r12+0x58]` 并调用 setter；cnti 比较 off `0xec1fea` `81 fe 69 74 6e 63`，handler off `0xec3780` 取 `[r12+0x60]`。这些是运行时对象链。
- 另一个 4CC switch 样本：off `0xecb63e` `81 fb 69 74 63 63` 比较 ccti，handler off `0xecb64a` `48 83 c7 58` 后在 `0xecb654` `e8 87 be 11 00` 调 setter；cnti handler off `0xecc621` `48 8d 4f 60`、`0xecc628` `e8 f3 ac 11 00`；cpcm handler off `0xecc3ee` `48 83 c7 68`、`0xecc3f8` `e8 63 fb 0f 00`。说明对象字段操作分别用 `+0x58/+0x60/+0x68`，不等同于 row slots。
- cpcm 的 XML 分发样本 off `0xec0aa9` `49 8b 4c 24 68`、off `0xec0ab1` `e8 ea 60 12 00` 也只显示对象成员 `+0x68` 的 delegate。
- table_25 的 L2 已知行槽来自快照 `evidence/fm24/reports/dbdat_decode/DB_TABLES_BIG.md`（SHA-256 `453c0f0be8326dcb966b15632b56194a0982dbdfa9d5e169c9fdb2a2def572e7`，与 manifest 相符）：ccti `+52`、cnti `+56`、cpcm `+64`、rdui `+114`、duni `+118`。本轮没有找到把上述运行时偏移桥接到这些行偏移的 L3 链；也未产生新槽位。

## 交付边界

- `output.json` 保留已证据化的 helperA、helperA 改写后的临时指针 vtable 调用、setter 结果、运行时偏移与未解项；`comp_new_slots` 为空。
- 尚缺：descriptor 构造器/完整成员布局、setter 运行时数据到 `.dat` 行的转换、编辑器数据库读入或写回/pack 链。以上均保持 open questions，不作推断。
