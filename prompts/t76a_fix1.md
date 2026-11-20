# t76a-fix1 — stadium(21) 单表 L2 扫表(分块交付,deepseek;全新会话)

你是受指挥官委派的子代理。前一轮 t76a 三次撞墙零落盘(每次 resume 重读上下文烧窗)。本会话全新开始,**只做一张表:stadium(21) 双档**,方法如下,先落盘后完善。

## 已有资产(直接用,不重做)

- 行框真源:`scratch/t74/out/frames.json` 的 `tables['21']`(client 38B/server 181B 定长 ×48,413,header 14,footer 8,identity 13B 在行尾)——**行框不许重闭**,直接用
- 逐列 profiling 参考实现:runpy 载入 `scripts/t73_mapper_core.py`(只读,不得修改)的列 profiling 函数;或按 t73 slots JSON 的输出格式自己写简版
- schema:`evidence/fm24/reports/editor_schema/master.json` 的 `entities['stadium.xml']` 字段清单(field/name/type)+ `enums` + `field_codes`
- 冻结锚点(结论不得冲突):client `Scti@3/Slat@17/Slon@21/rdui@25/duni@29`(fm24_dump FIELDS);t59 证 t21 48,413;server 行长差 143B(t74 已证是 server 独有字段段)

## 任务(按顺序,每步落盘)

1. **第一步(5 分钟内)**:写 `scratch/t76a/out/slots_client_21.json` 骨架:行框引用 + identity 三元组 + 逐列原始 profiling(u8..u32/f32 值域、distinct、all_zero、全一占比)。38B×48,413 向量化,几分钟内完成。
2. **第二步**:`slots_server_21.json`(181B 同法;server 独有 143B 段单独标 `server_only_segment`,不猜语义)。
3. **第三步**:字段对齐:stadium.xml 字段按 type 宽度 × 值域 × FK(t2 city 56,293 / t3 club 84,259 / t10 nation 251 / t19 region 28 / t25 comp 7,047 ordinal 集,wrong-UID 控制同报)给候选;数据侧=L2/candidate;锚点冲突=回查。
4. **第四步**:`REPORT.md` + `DONE.md`(首行 `DONE type=t76a status=complete`)+ `verify.py`(重抽锚点+≥5 槽对拍)。
5. team(24)/extra_24 **不在本会话范围**(t79 neon 在做静态收割);字符串槽不猜;跨对象/分发 → `escalate_to_sol`。

## 避坑纪律

1. 只写 `scratch/t76a/` 和 `scripts/t76a_*.py`;**任何文件写单次 ≤120 行**,先骨架后追加。
2. `0xffffffff` 与合法 0 分列;负结果原样保留。
3. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;载荷用 fm24_dump.load_payload 模式(可 runpy,不得修改)。
