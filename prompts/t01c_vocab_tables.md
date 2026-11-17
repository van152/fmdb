# t01-c 任务书:schema 词汇表机读化(deepseek 渠道 1)

> 机械转换任务,纯 Python,只读输入,产物写 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01c\`。
> Python 固定 `py -V:3.12 -I`。不 pip install,不启动任何程序。

## 背景
FM24 数据库语义解析项目需要一张"字段码词汇表":每个实体有哪些 4 字符字段码、哪些是客户端字段、每张数据库表对应哪个实体。其它并行任务(t01-a 扫描、t01-b 深挖)要用你的产物做匹配。

## 输入(全部只读)
1. `D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json`
   - 顶层 `entities`(32 个实体定义)、`entity_summary`(每实体 field_count + codes 列表)、`field_codes`(3009 个字段码)、`enums`(304 张枚举表)、`auxiliary`
2. `D:\tmp2b\fm24-db\evidence\fm24\reports\editor_gen\PROPERTY_MAP.md`
   - 里面有 database_table_type ↔ entity XML 的映射行(如 table_25→comp.xml#comp),把表格转录为机读

## 任务
1. **vocab.json**:
   ```json
   {
     "entities": {"comp.xml#comp": {"field_count": 255, "codes": ["ccti", "..."], "client_codes": [...], "readonly_codes": [...]}, ...},
     "field_codes": {"ccti": {"entity": "comp.xml#comp", "type": "...", "is_client_field": true|false|null, "enum_ref": "..."} },
     "code_conflicts": {"<code>": ["出现在多个实体的清单"]}
   }
   ```
   - 以 master.json 内实际字段为准:先检查 entities 内每个字段的实际属性名(可能有 type/enum/is_client_field 等),忠实转录,**不发明不存在的属性**
   - 4 字符码(全 [A-Za-z0-9]{4})与其它长度的码分开统计
2. **property_map.json**:转录 PROPERTY_MAP.md 的全部映射行,字段:`table_type`(int)、`entity`、`property`、`source`(md 里的原文行)
3. **REPORT.md** ≤40 行:实体数、4 字符码数量、码冲突清单、property_map 行数、任何 JSON 结构与预期不符的地方(如属性名不同)

## 验收
- `py -V:3.12 -I` 脚本重跑可复现;JSON 可被 json.load 无错读取
- vocab.json 的 codes 总数 = master.json field_codes 的码数(对不上要解释差在哪)
- comp.xml#comp 应含 ccti/cnti/cpcm/cnam/cnsm/cl3n/PLgn/crep/cext(指挥官已知锚点,用于自检)
