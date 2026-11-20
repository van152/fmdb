# t18 任务书:行↔对象偏移桥 —— 命名桥 G1 失败的根因攻坚

先读 [AGENTS.md](../AGENTS.md)。这是今晚的收官任务:G1 只有 5.06%(12/237)一致率,这个数字本身就是诊断——**两个坐标系被直接比对了**。

## 核心假设(先验证,再修)

`t16b` 的 walk 给出的是 **C++ 对象内偏移**(vtable 之后);而 E55/E27/E20 基线是 **.dat 行内偏移**。仓里早有路标:

> E36(t04):club 只闭合的 1 个字段 `Cccn@row+8` = **对象成员 +0xf0** ——行偏移与对象偏移差一个映射,不是同一个数。

## 求证路线(按顺序,每步留证据)

1. **序列化序 = 行布局序**:E20 方法论——行偏移 = 序列化器逐字段固定指令顺序 + 显式宽度即时数**累加**,不是对象内偏移。对 golden 三实体,把 t16b 的 walk(entity_trace_*.json 里有指令顺序)按 walk 序累加宽度,得到"行侧候选偏移",与基线比:
   - comp(E20 基线 18 个):`scratch/t01/inbox/t01f/output.json`
   - weather(E27 基线 89 个,行框架 = u32 name_len + UTF-8 名 + 3B + 字段):`scratch/t01/inbox/t01l/output.json`
   - city(E55 已命名槽):`reports/t12_field_names.json`
2. **reader 槽佐证**:`scratch/t05/reader_widths.json` 是行侧槽布局(t05 用 reader 宽度累加做的),它的槽序应与 walk 序一致——对齐两者可互验。
3. **步长封口**:`scratch/t05/COVERAGE.json` 每表有 stride;行侧累加结果 + 行前缀长度应等于 stride(对定长表)。这是硬校验。
4. **对象偏移与行偏移的映射**:对每实体拟合 `object_off = row_off + Δ` 的 Δ(club 的 0xf0-8 就是一个样本);若 Δ 恒定,记入台账作旁证;不恒定就只用行侧。

## 交付

1. 过了 ≥95% 行侧一致率后,**重生成全部实体台账**到 `scratch/t18/out/fields_<tag>.json`(ROW 偏移,字段结构同 t16b,grade 沿用 L3_instruction/L3_inherited/unnamed;grade 换 L3_row_instruction 以示区别)。
2. `bridge.json`:每实体 `{"entity","row_base","stride_check":"pass|fail","delta_obj_minus_row":"...","g1_row_consistency":x}` + 顶层 status。
3. `verify.py`(--help/--selftest):golden 三实体行侧比对 + stride 封口复算。
4. `REPORT.md`:假设验证过程原文(包括证伪尝试)、Δ 拟合结果、club 672 字段命名率变化。

## 纪律

- 只写 `scratch/t18/out/` + 新增 `scripts/t18_*.py`;scratch/t16b、t05..t17 只读;不联网。
- 输出预算:单次写盘 ≤400 行;大 JSON 分片。
- 50 分钟做不完分批落盘 partial。**若假设被证伪**(行侧一致率仍 <50%),如实落盘 `"status":"complete_hypothesis_falsified"` + 证据——证伪也是合格交付,不许硬凑。

## 优先级

club(672 字段)> nation(441)> comp(294)> 其余。golden 三实体是门,过了才放量。
