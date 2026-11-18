# 给 t05b(对齐器)的修正与线索 — 指挥官留

任务书里 `club top_level_scalars: 109` **是错的**。正确口径(已机读落盘):

- `club` 声明 433 字段 = **386 个标量 + 47 个列表**,列表子字段 239。
- 请以 `scratch/t05/schema_inventory.json` 的 `entities.club` 为准(含保序字段表与类型)。

另外三条会影响你算法设计的实测结论(详见 `scratch/t05/ALIGNMENT_NOTES.md`):

1. **club 行宽约 82B,却有 386 个标量 → 0.21 字节/标量。** 大量字段必然是位域打包
   或"存在位图 + 稀疏值",不是每个字段都占独立字节。所以你的对齐器必须允许
   `boolean/multiple_enum` 等字段**共享同一字节**(对单字段可视作 0 宽)。
2. **optional 字段可跳过。** award 的 37 个标量按最小线宽硬算,在没数完 15 个 optional
   字段前就已超过 77B 可用区 —— 说明 optional 字段"有值才出现",不是恒占位。
   请把"optional → 允许 0 宽"作为候选加进对齐器,否则夹具一定过不了。
3. **award 的可用区是 0..63**,`rdui u32@64`、`duni@68`(两个相等 u32)、`@76` marker=0
   是身份尾,不参与业务字段累加。校准夹具时请把这段排除。

夹具真值表在 `ALIGNMENT_NOTES.md` 第 4 节(含 lcrg 的 `rdui@len-13` 等本仓已验证锚点)。

若时间不够做完 club,请**优先保证阶段 A**:award / city / stadium / injury 四个定长夹具
的已知锚点全部自动复原 + 总宽吻合。这个结果本身就有价值,我在验收时会先看它。
