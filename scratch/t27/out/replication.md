# t27 → luna：复用 club 子表 cursor 的方法

## 1. 定位、分叉、再解释

1. **先查两个 archive 的目录与有效载荷。** 记录 `table_id`、成员名、版本、行数、解压后 SHA。绝不因表号相同就搬用偏移。t22 在两边都存在：server 每行有属性块，client 只有 identity；两边均为 449 行。同一个 slot 19 兼容两种路径。
2. **串起 factory → RTTI/vtable → slot 19；用 PE runtime-function extent 建可达 CFG。** 用 `t05_pe.PE` 往返换算 VA/file offset，保存原指令 bytes。对直接调用追 thunk 到真正的 consumer。t22 的 `0xdb7f80` → `0x39dd7b0` 把 caller 的对象成员指针从 RCX 传到 RDX，`0x39dd7d4` 才执行 `read(4)`，不是 cursor 透明分支。另检查 writer / fixup；引用通常写的是目标记录 ordinal，而 getter 取的是修复后的指针。
3. **按谓词来源分支，而不是按 `jcc` 方向分类。** CAPSTONE 出图用 `t21b_control_flow.ReaderCFG`；手工确认 call summary 和谓词来源，不把线性扫出的指令顺序当执行路径。

| 分支类型 | t22 例子（PE file offset） | 可复制的判定方法 |
|---|---|---|
| 流数据 | loader selector `0xf2ba0e` → factory；reader `0x1537acc` 比较刚读的 identity 首 u32 | 先消费，再把值送到后续条件；记录边与值域，不用行号预测读入值 |
| 外部模式 | `0x153781b` 检查 caller 栈参数；server 走属性块，client 跳过 | 追寄存器/栈参数来源；若入口值未知，fork 后分别跑全表，要求失败路径有明确反例。记录为数据反推的运行时参数，而非一字节 selector |
| 外部 I/O 结果 | t20 窗内 18 次 stream status + 3 次 helper AL | 按有效输入的成功返回建模；短读、非零状态进入失败，不能被解释为另一种正常字段布局 |
| 外部上下文 / 生命周期 | `0x153780a` context、`0x1537a9b`/`0x1537aed` stream、`0x1537ad9` callback、`0x1537af3` refcount | 标明条件来源、caller 约束和仍 opaque 的调用。观测到的 0 次不是一般意义死边 |
| 有效域不可达／死代码 | 日期 helper `0x39dd7bc` 的空 stream 边跳过 read 后仍解引用空指针 | 凭代码证明不属于有效读路径；不凭当前数据缺席就删 CFG 边 |

## 2. Walk 模板

```text
read_header(): version, count, table_flags
p = first selector  # 不预先用候选字段划界
for i in range(count):
    selector = read(site=loader_selector, width=1)
    pc, state = entry_for(table_id, selector), archive_context
    while not exit(pc):
        if transfer(pc):
            v = read(pc, evaluated_width); cursor += width
            state[sink] = v           # helper 和 bulk 都需要明确 sink
        if condition(pc):
            pc = choose(state, branch_proof[pc])  # 未知外部值可 fork
        else:
            pc = unique_successor(pc)
    assert success and identity_relation(state, i)  # 行号仅作后置校验
read_footer_from_current_cursor(); assert cursor == len(payload)
```

- 一个实际路径一份 transfer/branch 模板，逐行保存 selector/body 边界、模板编号、identity 和 body hash；有可变长段则逐行保存长度变量。不对齐时先保留 CFG 与首个反例，不补 padding 凑 stride。
- 双坐标同时记录：t22 legacy 起点 14，业务坐标仍从行体首字节算；真实 wire 起点 13（selector 在前），末行之后是 9 B footer。对照 CSV 时 t22 的 legacy `+78` 借了下条 selector，末条借 footer 首字节。
- 三重闸门：**唯一 scoped schema occurrence → 同类 getter 的 4CC 分发及对象成员 → 实际路径的 wire sink**，再用所有行检验独立画像。日期查 packed day/year（不要只看“值像日期”）；引用走实际目标表的 ordinal 域，同时可报告 parent club 域兼容性；enum/掩码/界值/哨兵单独记账。UI 可见性不改 wire 宽度；出现 schema/raw 差异，不擅自做重编码或货币单位换算。重复 occurrence 不计命名。用独立 verifier 从 archive 复算并保存早期反例。

## 3. 下一批侦察（非映射验收）

`scout.json` 覆盖 t24 的全部 38 个 nested parent；未证实的 table/RTTI/reader/stride 为 `null`（unknown）。下表只列有具体线索的条目。`~` 表示目录元数据只满足算术，未 walk；其他非 t22 stride 来源为 t13d 或 t06 profile。表号与 parent 的配对除 Cstc 外仍为候选，包括名称相近的项。

| Parent | table_id | RTTI | reader VA | schema 字段数 | stride B |
|---|---:|---|---|---:|---|
| Cstc | 22 | STADIUM_CHANGE | `0x141538200` | 28 | server 79 / client 13 |
| Cafl | unknown | unknown | unknown | 29 | unknown |
| Cvfl | unknown | unknown | unknown | 19 | unknown |
| Cdbt | 33 | STARTING_CLUB_DEBT | `0x141535af0` | 5 | ~79 |
| Tchl | 34 | STARTING_TEAM_CUP_HISTORY | `0x14156f9d0` | 9 | 44；club/nation 未排他，见 t13d 的伪帧反例 |
| Clhs | 37 | STARTING_TEAM_LEAGUE_HISTORY | `0x14119e7f0` | 12 | 40 |
| Cmti | 43 | STARTING_MONTHLY_INSTALLMENT | `0x14153d0a0` | 6 | 46 |
| Csme | 59 | STARTING_MEDIA_EXPECTATIONS | `0x141583ba0` | 2 | unknown |
| CSrs | 62 | STARTING_RESERVE_TEAM | `0x14119c960` | 10 | ~42 |
| CNtp | 66 | STARTING_CLUB_TRANSFER_PREFERENCE | `0x141530120` | 4 | 24 |
| unknown | 64 | STARTING_CLUB_STAFF_JOB_STATUS | `0x141584350` | unknown | 21 |
| unknown | 65/67/68/69 | STARTING_NEWGEN_PARAMETER | `0x1415307e0` | unknown | ~31（同 reader 不证明同 parent） |

**Cafl/Cvfl 优先切口。** `Cafl` 的 code compare `0xe8b4db` 进入 `0xe8f13d` 的 `0x141532ab0` thunk，R8D=0；目标函数在 `0x436385d`/`0x4363864` 取 `+0x118/+0x120`。`Cvfl` 的 compare `0xe8c1e8` 后直接比较 club 的相同偏移，且 `0xe8c217` 调 `0x141532c60`（R8B=1），callee 也访问这对成员。先验证是否为同一 club-owned collection 的不同视图，沿对象写入点找 server reader/子 reader，再查独立 archive member；不要因为两个 schema parent 就假定两个独立表。
