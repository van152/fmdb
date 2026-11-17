# t01-c REPORT:schema 词汇表机读化

- 输入: master.json(editor_schema, 24.4.2, parse_errors=[]) + PROPERTY_MAP.md
- 产物: 本目录 vocab.json / property_map.json / REPORT.md;脚本 scripts/t01c_build_vocab.py 可复跑

## 对账
- 实体数 32(32 个 xml 均单 record 组,key=<file>#<id>;field_count 与字段数逐一核对一致)
- vocab.field_codes = 3009 = master.field_codes ✓(键与 master 完全一致)
- 码长分布:4 字符码 2343,其它 666
- 属于 32 实体的码 2057(含嵌套 list_item_fields);非实体来源 952(rule_group/format/extractor)→ entity=null
- 实体顶层码合计 2144(= sum field_count),顶层并集 1697;codes 列表按 master 原样保留重复(如 comp 的 duni 出现 2 次)
- code_conflicts:324 个码出现在 >1 实体(机读全清单在 vocab.json);最大:dbnm 出现于 21 实体

## 锚点自检(comp.xml#comp)
- 通过 7/9:ccti/cnti/cpcm/cnam/PLgn/crep/cext
- cnsm:master 全库(3009 码,大小写不敏感)无此码;comp 的是 csnm(Short Name)与 c3ln(Three Letter Name)
- cl3n:无此码;club.xml 有 Cl3n,comp.xml#comp 有 c3ln
- → 两个锚码与证据不符(疑拼写偏差),解析经 3 重核对(entities/summary/field_codes)无误

## 结构与预期不符(如实记录)
- 属性名:枚举引用为 enum_ref(非 enum);只读为 is_read_only(174 处)+ 1 处非标 read_only(MYpc,已计入 readonly_codes)
- master field_codes[].locations 对 52 个实体码漏记 database 位置(如 PLgn/Cnti 只记 rule_group)→ vocab 的 entity 以 entities 树全量遍历为准
- is_client_field 顶层 true=192 / false=3(CSrs/Cfvp/CRtm);另有 2 个嵌套 list_item_field 为 true,不计入 client_codes(与 codes 同为顶层范围)
- 一码多枚举:enum_ref 冲突 Ttyp、PFjo → vocab 用 list;75 个码有多个 type 变体,type 按 master 原文转录
- vocab.field_codes 的 entity 字段:单实体→str,多实体→list,非实体→null(is_client_field/enum_ref 同理)

## property_map.json(21 行)
- 转录 §3「database_table_type 数值 → 实体」全部映射行;property=该行 dbts 枚举名(表 10 无 → null);投票/一致/备注保留在 source 原文行
- entity 已归一化为 <file>#<id>(md 的 derby name → derby.xml#drbr,唯一子串匹配);dbts 枚举名与 master#enums.dbts 交叉验证:一致
- §4 字段映射行未转录:其表号列含多值(如 10,9)不满足 table_type(int),内容已由 vocab.json 承载
