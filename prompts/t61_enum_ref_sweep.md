# t61 — Held 字段 scoped enum_ref 批量专项(nation/club/comp,sol)

你是受指挥官委派的子代理。三张主表普查(t55/t57/t59,E94/E97/E99)留下 held 字段,其中一批的 XML schema 声明了 `enum_ref` 但当年域检验缺 scoped 枚举集或域冲突。本任务**只做枚举域批量复核**:从冻结 editor_schema 提取 scoped 枚举集,对每个 held occurrence 走既有全档域管线,**过闸门 L3 晋级,不过闸保持 held 并更新首反例**。候选不写结论,negative 原样保留,L4=0。

## 必读
- AGENTS.md;reports/club_nation_subtable_schema.json(**v8**,E98;若指挥官已并 v9 则以 v9 为基线,先读 reports/ 实际版本)
- scratch/t55/out/field_map.json + REPORT.md(nation held:主行 4——Necf/Nygn 域冲突、Ngct/Nsod 无 scoped enum_ref;子表层 held 见 schema)
- scratch/t57/out/field_map.json + REPORT.md(club 主行 held 11:Csnm 537 越界、CLat/CLon、Csti、Cyfn=extra+0xd8 等)
- scratch/t59/out/field_map.json + REPORT.md(comp held 10:dbty、CTty、PLgn、CpRp、rdui、cnam/csnm/c3ln、VARt/HKEt)
- evidence/fm24/reports/editor_schema/master.json(冻结 SHA 7d57477e;enum_ref/min/max 唯一来源)
- scratch/t01/LEDGER.json(E84–E99)

## 任务
1. **枚举集提取**:对每个 held occurrence 的 XML 路径,提取 scoped `enum_ref` 的值集(含数值与字符串对);无 enum_ref 或引用不存在的 → 记 no_enum_source,保持 held。
2. **域批量检验**:按各表既有坐标(t55/t57/t59 field_map 的 slot/lane/legacy_body_offset 等)全档取值(client/server 各自全部行),直方图 vs 枚举集;越界=首反例(行号+绝对 offset+原始字节)。引用字段类 held 若属枚举问题同样处理。
3. **晋级口径**:全部档位值 ∈ 枚举集 且 4CC/getter 链为既有 L3 同级证据(不重做静态链,引用 t55/t57/t59 的 getter 记录)→ L3;否则 held(记录枚举集+实际值域+首反例)。**Club/comp/nation 三侧分开计数**,不混层。
4. **边界**:不改 scratch/t55/t57/t59;不碰已闭 L3;不碰 person/PDxx;不启动游戏本体/FM 编辑器(IDA 静态分析允许),不联网,不读写 Z:。bit 投影类(如 cext)不在本任务(已 L3)。
5. 独立 verify.py(不 import worker/builder)+ builder scripts/t61_enum_ref_sweep.py;--help/--selftest;退出码 0/1/2。

## 交付 scratch/t61/out/
- enum_inventory.json(逐 held:表/4CC/XML 路径/enum_ref 源/枚举集/双档直方图/判定/首反例)
- promoted.json(晋级清单+证据引用)、verify.py、REPORT.md、DONE.md;scripts/t61_enum_ref_sweep.py

优先级:有 enum_ref 的先做;预期重点 nation Ngct/Nsod、club Csti、comp CTty/PLgn。Python `py -V:3.12 -I -B`;FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
