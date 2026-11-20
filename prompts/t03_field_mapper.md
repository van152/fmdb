# t03:通用字段映射器(field_mapper)—— 全库解析的规模化杠杆

## 使命

FM24 `.dat` 字段→行偏移映射的**自动化**。目标不是解某一张表,而是把已走通的人工方法固化成可复跑脚本,让剩余 30+ 实体能批量展开。**只读输入,不启动游戏/编辑器/IDA,不 pip install,`py -V:3.12 -I -B`。**

## 背景:方法已验证,缺的是自动化

E20(t01f)证明:**行偏移不存于 descriptor 槽,而是序列化器 reader 逐字段固定顺序 + 显式宽度即时数累加**。4CC getter 给字段名。这条"宽度累加法"已在 14 个实体、5 种模式上人工验证成功(comp/weat/stad/pers/nati/awar/city/cont/inju/lang/drbr/regi/stgn/curr)。

**死路勿重走**:descriptor 槽/构造器里找行偏移数组(H4)已被 E14 证伪、t01b-r2 构造器 0 命中、helper thunk 进壳区——不要再尝试。

## 输入(全部现成)

- `scratch/t02/field_mapper/fixtures.json`:**7 个归一化回归夹具,173 字段**,覆盖 5 种模式。每个含 type_id/field_count/{code:row_offset}/reader(entry+unwrapped+mode)。
- `scratch/t01/inbox/t01h/output.json`:**74 项 census,63 项有 reader.entry_file_offset**;每项含 factory handler/ctor/RTTI/reader mode。
- `editor.exe`:`<OLD_REPO>/input/editor.exe`(只读,SHA b82ebe8e032f2017)。
- `capstone 5.0.7` / `numpy` / `pefile` 已装,`py -V:3.12 -I -B` 可 import。

## 任务(先落盘,边做边存)

1. **第一步**:在 OUTBOX 创建 `field_mapper.py` 骨架 + `REPORT.md` 一行,之后每完成一个能力就重写。
2. **实现 `analyze(type_id) -> {code: row_offset}`**,三步流水线:
   - **① reader 定位**:从 census 拿 `reader.entry_file_offset`。注意 thunk 链:comp(type25)是 `0xed0a40 → 0x3b3f0d0(设arg8=0) → 0xeb7000(真正读主体)`,census 只展开到中间环;需沿 `e9/e8 rel32` 继续跟进到真正的读主体(找密集 `call [rax+0x28]` 的函数)。
   - **② 宽度累加**:capstone 线性扫读主体,识别 `mov r8d, N`(宽度)+ `call qword ptr [rax+0x28]`(流传输)配对,顺序累加得每个传输点的 `row_offset`。要处理:分支互斥臂(4B/8B 二选一,不能相加)、循环(确定循环可按次数展开,计数循环需单独的边界公式)、helper thunk(宽度在被调用函数里,需跟进一层)。
   - **③ 4CC 对齐**:在实体 getter 窗口扫 `cmp r32, imm32`(`81 f8..ff`,4CC 小端作 imm32),把 4CC → 对象成员偏移 `[rbx+disp]` 对齐到 reader 里写同一 `disp` 的传输点,给出字段名。
3. **回归验证**:脚本跑 7 个夹具,输出每个实体的"复现字段数 / 夹具字段数 / 逐字段偏移吻合率"。目标是**至少 5/7 实体复现 ≥80% 字段偏移**(weat 的 89 字段允许只复现前缀,club mixed 允许部分)。
4. 输出 `OUTBOX/fixtures_result.json` + 更新 `REPORT.md`,报告哪些模式自动化成功、哪些仍需人工、卡点在哪。

## 验收判据(指挥官会独立复跑)

- `py -V:3.12 -I -B OUTBOX/field_mapper.py --selfcheck` 能在夹具上给出吻合率报告。
- 至少 5/7 夹具实体达到 ≥80% 偏移吻合。
- 诚实标注失败模式,不猜、不把未闭合当成功。

## 硬约束

只读 editor.exe 与游戏库;claim 带 file offset + 字节;负结果保留;只写 OUTBOX;脚本要有 `--help` 与 `--selfcheck`,退出码 0/1/2。

## 交付

`OUTBOX/field_mapper.py` + `REPORT.md` + `fixtures_result.json`。打印:7 夹具各自吻合率 + 平均 + 哪些模式通过。
