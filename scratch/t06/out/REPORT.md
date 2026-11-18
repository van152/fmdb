# t06 字段命名结果

状态：`complete_city_regi_calibrations_exact_partial`。输入布局逐槽照抄；未把 schema 原始顺序当行内顺序。共 31 个 archive/entity 分组、240 槽；20 个 high（含 server boundary marker），220 个 unresolved。

## 校准集与结论

- city：client/server 均复现 Clat+Clon 合并槽与 `Cnti@10`；还以目标行数/哨兵统计命名 Cwea、Clgi、Clri。Catt/Cinh/Calt 相关槽仍 unresolved，不伪造。
- regi：client 8 个 4B 槽与参考偏移逐一相同；server 同 8 槽并保留 +32 的 1B boundary marker。region 数值槽的语义没有独立锚点，保持 unresolved。
- injury server：用户给定 9 条命名原样保留，偏移/宽度/值域与画像相符；其余槽不扩展猜名。
- 校准差异：0（city Cnti@10、city 经纬度组件、regi 位置闭合、injury 9 条）。

## 画像与解释纪律

t05_profile 画像保存在本目录。引用计数：nation=251、language=126、weather=334；local-region=2488。lcrg 用已闭合 walk_lcrg 分行后仅对前 31B 业务区画像。server table_34 的上游 fixed 规格闭包失败（14+7115*44+8=313082，payload 仅 12B），不造行画像或字段名。

## 逐槽分配

### city — type 2 / server，business_width=30

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile: constant 0 in all 56,293 rows; no matching scalar field can be identified from a constant byte.；原因：constant/padding-like byte; no discriminating value evidence |
| 1 | 1 | 8 | `<Clat+Clon 合并> (`Clat+Clon`)` | high | 56,293 行均为有限 f32 对：row+1 纬度 -54.8127..78.2243，row+5 经度 -179.9813..179.55；与 schema 两个 real 字段吻合，且 city_reference 明确两者。 |
| 2 | 9 | 1 | `unresolved` | unresolved | profile=profile_server2_city.json, rows=56293, byte@9 distinct=21 range=0..20 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0; candidate city codes Catt(integer) / Cinh(enum) both accept a low-cardinality byte, so type alone is ambiguous；原因：no independent field anchor or legal-enum cardinality to separate Catt from Cinh |
| 3 | 10 | 4 | `Cnti` | high | u32 distinct=230，min/max=0..249，0xFFFFFFFF 比率=0；nation 表 251 行且 ref_lt_251=1.0；schema 类型 database_record_unique_id。city_reference 与任务基准均指定 Cnti@10。 |
| 4 | 14 | 4 | `Cwea` | high | u32 distinct=321，min/max=0..333，0xFFFFFFFF 比率=0；weather profile 表 334 行且 ref_lt_334=1.0；符合 4B database_record_unique_id。 |
| 5 | 18 | 3 | `unresolved` | unresolved | profile=profile_server2_city.json, rows=56293, byte@18 distinct=256 range=0..255 ff_ratio=0.0040; u16 distinct=2365 range=0..65533 ff_ratio=0.0000; 3B reader chunk may contain subfields, but its internal field boundaries are not established；原因：no proven split of the 3B read into Calt/Cinh; do not split a fixed reader slot speculatively |
| 6 | 21 | 4 | `Clgi` | high | u32 distinct=61；0xFFFFFFFF 哨兵比率=0.8173；其余 18.27% 全部 < language 表 126 行(ref_lt_126=0.1827)，可作为可空引用。 |
| 7 | 25 | 4 | `Clri` | high | u32 distinct=2330；0xFFFFFFFF 哨兵比率=0.0835；其余 91.65% 全部 < local-region 表 2488 行(ref_lt_2488=0.9165)，可作为可空引用。 |
| 8 | 29 | 1 | `unresolved` | unresolved | profile=profile_server2_city.json, rows=56293, byte@29 distinct=2 range=0..2 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：byte values {0,2} do not uniquely match a schema field; no independent semantic anchor |

### city — type 2 / client，business_width=30

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile: constant 0 in all 56,293 rows; no matching scalar field can be identified from a constant byte.；原因：constant/padding-like byte; no discriminating value evidence |
| 1 | 1 | 8 | `<Clat+Clon 合并> (`Clat+Clon`)` | high | 56,293 行均为有限 f32 对：row+1 纬度 -54.8127..78.2243，row+5 经度 -179.9813..179.55；与 schema 两个 real 字段吻合，且 city_reference 明确两者。 |
| 2 | 9 | 1 | `unresolved` | unresolved | profile=profile_client2_city.json, rows=56293, byte@9 distinct=21 range=0..20 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0; candidate city codes Catt(integer) / Cinh(enum) both accept a low-cardinality byte, so type alone is ambiguous；原因：no independent field anchor or legal-enum cardinality to separate Catt from Cinh |
| 3 | 10 | 4 | `Cnti` | high | u32 distinct=230，min/max=0..249，0xFFFFFFFF 比率=0；nation 表 251 行且 ref_lt_251=1.0；schema 类型 database_record_unique_id。city_reference 与任务基准均指定 Cnti@10。 |
| 4 | 14 | 4 | `Cwea` | high | u32 distinct=321，min/max=0..333，0xFFFFFFFF 比率=0；weather profile 表 334 行且 ref_lt_334=1.0；符合 4B database_record_unique_id。 |
| 5 | 18 | 3 | `unresolved` | unresolved | profile=profile_client2_city.json, rows=56293, byte@18 distinct=256 range=0..255 ff_ratio=0.0040; u16 distinct=2365 range=0..65533 ff_ratio=0.0000; 3B reader chunk may contain subfields, but its internal field boundaries are not established；原因：no proven split of the 3B read into Calt/Cinh; do not split a fixed reader slot speculatively |
| 6 | 21 | 4 | `Clgi` | high | u32 distinct=61；0xFFFFFFFF 哨兵比率=0.8173；其余 18.27% 全部 < language 表 126 行(ref_lt_126=0.1827)，可作为可空引用。 |
| 7 | 25 | 4 | `Clri` | high | u32 distinct=2330；0xFFFFFFFF 哨兵比率=0.0835；其余 91.65% 全部 < local-region 表 2488 行(ref_lt_2488=0.9165)，可作为可空引用。 |
| 8 | 29 | 1 | `unresolved` | unresolved | profile=profile_client2_city.json, rows=56293, byte@29 distinct=2 range=0..2 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：byte values {0,2} do not uniquely match a schema field; no independent semantic anchor |

### inju — type 6 / client，business_width=3

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_client6_inju.json, rows=115, byte@0 distinct=11 range=1..13 ff_ratio=0.0000；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 1 | 1 | 1 | `unresolved` | unresolved | profile=profile_client6_inju.json, rows=115, byte@1 distinct=45 range=1..48 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 2 | 2 | 1 | `unresolved` | unresolved | profile=profile_client6_inju.json, rows=115, byte@2 distinct=2 range=0..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |

### inju — type 6 / server，business_width=27

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `icla` | high | 值域 1–13，11 种; server injury profile n=115, u8 min=1, max=13, distinct=11; calibrated 4CC getter + semantic validation. |
| 1 | 1 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@1 distinct=45 range=1..48 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 2 | 2 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@2 distinct=2 range=0..1 ff_ratio=0.0000；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 3 | 3 | 2 | `Imnd` | high | 值域 1–180，22 种; server injury profile n=115, u16 min=1, max=180, distinct=22; calibrated 4CC getter + semantic validation. |
| 4 | 5 | 2 | `Imio` | high | 值域 3–290，29 种; server injury profile n=115, u16 min=3, max=290, distinct=29; calibrated 4CC getter + semantic validation. |
| 5 | 7 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@7 distinct=11 range=0..100 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 6 | 8 | 1 | `Irec` | high | 严格 {0,1}; server injury profile n=115, u8 min=0, max=1, distinct=2; calibrated 4CC getter + semantic validation. |
| 7 | 9 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@9 distinct=2 range=0..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 8 | 10 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@10 distinct=2 range=0..1 ff_ratio=0.0000；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 9 | 11 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@11 distinct=2 range=0..1 ff_ratio=0.0000；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 10 | 12 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@12 distinct=1 range=0..0 ff_ratio=0.0000；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 11 | 13 | 4 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@13 distinct=8 range=0..205 ff_ratio=0.0000; u16 distinct=8 range=0..55050 ff_ratio=0.0000; u32 distinct=27 range=953267991..1091567616 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0001..9.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 12 | 17 | 1 | `Imip` | high | 值域 0–90，10 种; server injury profile n=115, u8 min=0, max=90, distinct=10; calibrated 4CC getter + semantic validation. |
| 13 | 18 | 2 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@18 distinct=25 range=0..184 ff_ratio=0.0000; u16 distinct=40 range=0..4871 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 14 | 20 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@20 distinct=3 range=0..2 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 15 | 21 | 1 | `Icms` | high | 严格 {0,1,2,3} 四季; server injury profile n=115, u8 min=0, max=3, distinct=4; calibrated 4CC getter + semantic validation. |
| 16 | 22 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@22 distinct=2 range=0..1 ff_ratio=0.0000；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 17 | 23 | 1 | `inSr` | high | 值域 1–5，五级; server injury profile n=115, u8 min=1, max=5, distinct=5; calibrated 4CC getter + semantic validation. |
| 18 | 24 | 1 | `unresolved` | unresolved | profile=profile_server6_inju.json, rows=115, byte@24 distinct=6 range=5..255 ff_ratio=0.8174；原因：not in the nine-field calibrated set; no independent name/semantic anchor for this slot |
| 19 | 25 | 1 | `Icdp` | high | {50,255}；0xFF 为不适用哨兵，ff_ratio=0.9826; server injury profile n=115, u8 min=50, max=255, distinct=2; calibrated 4CC getter + semantic validation. |
| 20 | 26 | 1 | `Icdo` | high | 值域 1–51; server injury profile n=115, u8 min=1, max=51, distinct=15; calibrated 4CC getter + semantic validation. |

### regi — type 19 / client，business_width=32

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@0 distinct=23 range=1..255 ff_ratio=0.1429; u16 distinct=25 range=354..65535 ff_ratio=0.1429; u32 distinct=25 range=11711..4294967295 ff_ratio=0.1429; f32 finite_ratio=0.8571 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@4 distinct=25 range=17..255 ff_ratio=0.1429; u16 distinct=25 range=59..65535 ff_ratio=0.1429; u32 distinct=25 range=6889..4294967295 ff_ratio=0.1429; f32 finite_ratio=0.8571 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@8 distinct=25 range=0..255 ff_ratio=0.1429; u16 distinct=25 range=0..65535 ff_ratio=0.1429; u32 distinct=25 range=0..4294967295 ff_ratio=0.1429; f32 finite_ratio=0.8571 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 3 | 12 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@12 distinct=23 range=0..247 ff_ratio=0.0000; u16 distinct=25 range=0..23902 ff_ratio=0.0000; u32 distinct=25 range=0..23902 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 4 | 16 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@16 distinct=24 range=0..246 ff_ratio=0.0000; u16 distinct=25 range=0..62303 ff_ratio=0.0000; u32 distinct=25 range=0..67333 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 5 | 20 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@20 distinct=22 range=0..250 ff_ratio=0.0000; u16 distinct=24 range=0..32462 ff_ratio=0.0000; u32 distinct=24 range=0..32462 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 6 | 24 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@24 distinct=1 range=255..255 ff_ratio=1.0000; u16 distinct=1 range=65535..65535 ff_ratio=1.0000; u32 distinct=1 range=4294967295..4294967295 ff_ratio=1.0000; reference confirms constant FFFFFFFF at these offsets；原因：both slots are constant 0xFFFFFFFF (28/28); two readonly integer candidates cannot be ordered from data, so retain unresolved |
| 7 | 28 | 4 | `unresolved` | unresolved | profile=profile_client19_regi.json, rows=28, byte@28 distinct=1 range=255..255 ff_ratio=1.0000; u16 distinct=1 range=65535..65535 ff_ratio=1.0000; u32 distinct=1 range=4294967295..4294967295 ff_ratio=1.0000; reference confirms constant FFFFFFFF at these offsets；原因：both slots are constant 0xFFFFFFFF (28/28); two readonly integer candidates cannot be ordered from data, so retain unresolved |

### regi — type 19 / server，business_width=33

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@0 distinct=23 range=1..255 ff_ratio=0.1429; u16 distinct=25 range=354..65535 ff_ratio=0.1429; u32 distinct=25 range=11711..4294967295 ff_ratio=0.1429; f32 finite_ratio=0.8571 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@4 distinct=25 range=17..255 ff_ratio=0.1429; u16 distinct=25 range=59..65535 ff_ratio=0.1429; u32 distinct=25 range=6889..4294967295 ff_ratio=0.1429; f32 finite_ratio=0.8571 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@8 distinct=25 range=0..255 ff_ratio=0.1429; u16 distinct=25 range=0..65535 ff_ratio=0.1429; u32 distinct=25 range=0..4294967295 ff_ratio=0.1429; f32 finite_ratio=0.8571 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 3 | 12 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@12 distinct=23 range=0..247 ff_ratio=0.0000; u16 distinct=25 range=0..23902 ff_ratio=0.0000; u32 distinct=25 range=0..23902 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 4 | 16 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@16 distinct=24 range=0..246 ff_ratio=0.0000; u16 distinct=25 range=0..62303 ff_ratio=0.0000; u32 distinct=25 range=0..67333 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 5 | 20 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@20 distinct=22 range=0..250 ff_ratio=0.0000; u16 distinct=24 range=0..32462 ff_ratio=0.0000; u32 distinct=24 range=0..32462 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：region schema has no unique matching varying scalar here; Rnam is language/string-associated and the row values do not uniquely identify it |
| 6 | 24 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@24 distinct=1 range=255..255 ff_ratio=1.0000; u16 distinct=1 range=65535..65535 ff_ratio=1.0000; u32 distinct=1 range=4294967295..4294967295 ff_ratio=1.0000; reference confirms constant FFFFFFFF at these offsets；原因：both slots are constant 0xFFFFFFFF (28/28); two readonly integer candidates cannot be ordered from data, so retain unresolved |
| 7 | 28 | 4 | `unresolved` | unresolved | profile=profile_server19_regi.json, rows=28, byte@28 distinct=1 range=255..255 ff_ratio=1.0000; u16 distinct=1 range=65535..65535 ff_ratio=1.0000; u32 distinct=1 range=4294967295..4294967295 ff_ratio=1.0000; reference confirms constant FFFFFFFF at these offsets；原因：both slots are constant 0xFFFFFFFF (28/28); two readonly integer candidates cannot be ordered from data, so retain unresolved |
| 8 | 32 | 1 | `boundary_marker` | high | server-only byte at +32; constant 0x04 in 28/28 rows. The task/reference identifies the extra server byte as the boundary marker. |

### stad — type 21 / client，business_width=25

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 2 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@0 distinct=10 range=0..130 ff_ratio=0.0000; u16 distinct=11 range=0..2176 ff_ratio=0.0000；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 1 | 2 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@2 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 2 | 3 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@3 distinct=256 range=0..255 ff_ratio=0.0038; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 3 | 4 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@4 distinct=212 range=0..219 ff_ratio=0.0000；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 4 | 5 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@5 distinct=1 range=0..0 ff_ratio=0.0000；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 5 | 6 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@6 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=0.0862 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 6 | 7 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@7 distinct=256 range=0..255 ff_ratio=0.9142; f32 finite_ratio=0.0862 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 7 | 8 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@8 distinct=162 range=0..255 ff_ratio=0.9138; f32 finite_ratio=1.0000 range=-524287.9688..8589934080.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 8 | 9 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@9 distinct=2 range=0..255 ff_ratio=0.9138; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 9 | 10 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@10 distinct=2 range=0..255 ff_ratio=0.9138; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 10 | 11 | 2 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@11 distinct=7 range=29..200 ff_ratio=0.0000; u16 distinct=7 range=29..200 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 11 | 13 | 2 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@13 distinct=1 range=1..1 ff_ratio=0.0000; u16 distinct=1 range=1..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 12 | 15 | 2 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@15 distinct=1 range=108..108 ff_ratio=0.0000; u16 distinct=1 range=1900..1900 ff_ratio=0.0000；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 13 | 17 | 2 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@17 distinct=256 range=0..255 ff_ratio=0.0024; u16 distinct=24437 range=0..65535 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=-54.8163..71.0288；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 14 | 19 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@19 distinct=256 range=0..255 ff_ratio=0.0019；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 15 | 20 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@20 distinct=16 range=0..194 ff_ratio=0.0000；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 16 | 21 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@21 distinct=256 range=0..255 ff_ratio=0.0026; f32 finite_ratio=1.0000 range=-175.2074..179.1984；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 17 | 22 | 2 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@22 distinct=256 range=0..255 ff_ratio=0.0027; u16 distinct=24218 range=0..65532 ff_ratio=0.0000；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |
| 18 | 24 | 1 | `unresolved` | unresolved | profile=profile_client21_stad.json, rows=48413, byte@24 distinct=19 range=0..195 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：stadium has 40 scalar schema candidates and no ground-truth slot anchor; low-value profile is not a unique name match |

### unknown(type 22) — type 22 / server，business_width=66

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@0 distinct=181 range=0..255 ff_ratio=0.2004; u16 distinct=310 range=86..65535 ff_ratio=0.1960; u32 distinct=311 range=86..4294967295 ff_ratio=0.1960; f32 finite_ratio=0.8040 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@4 distinct=201 range=0..255 ff_ratio=0.0111; u16 distinct=370 range=9..48373 ff_ratio=0.0000; u32 distinct=370 range=9..48373 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@8 distinct=115 range=0..255 ff_ratio=0.6236; u16 distinct=144 range=414..65535 ff_ratio=0.6236; u32 distinct=144 range=414..4294967295 ff_ratio=0.6236; f32 finite_ratio=0.3764 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 12 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@12 distinct=53 range=1..245 ff_ratio=0.0000; u16 distinct=53 range=1..365 ff_ratio=0.0000; u32 distinct=89 range=131072001..133038353 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 16 | 1 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@16 distinct=78 range=1..245 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 5 | 17 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@17 distinct=2 range=0..1 ff_ratio=0.0000; u16 distinct=23 range=57601..60929 ff_ratio=0.0000; u32 distinct=103 range=67627008..4278709761 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 6 | 21 | 1 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@21 distinct=53 range=4..255 ff_ratio=0.8040; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 7 | 22 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@22 distinct=3 range=0..255 ff_ratio=0.8040; u16 distinct=3 range=0..65535 ff_ratio=0.8040; u32 distinct=131 range=16908287..4278583295 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 8 | 26 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@26 distinct=82 range=0..255 ff_ratio=0.5367; u16 distinct=82 range=0..65535 ff_ratio=0.5367; u32 distinct=87 range=0..83886079 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 9 | 30 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@30 distinct=51 range=4..255 ff_ratio=0.8040; u16 distinct=65 range=532..65535 ff_ratio=0.8040; u32 distinct=65 range=532..4294967295 ff_ratio=0.8040; f32 finite_ratio=0.1960 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 10 | 34 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@34 distinct=59 range=0..255 ff_ratio=0.6058; u16 distinct=68 range=0..65535 ff_ratio=0.6058; u32 distinct=68 range=0..4294967295 ff_ratio=0.6058; f32 finite_ratio=0.3942 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 11 | 38 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@38 distinct=29 range=0..255 ff_ratio=0.6949; u16 distinct=32 range=0..65535 ff_ratio=0.6949; u32 distinct=32 range=0..4294967295 ff_ratio=0.6949; f32 finite_ratio=0.3051 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 12 | 42 | 1 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@42 distinct=38 range=0..255 ff_ratio=0.6904; f32 finite_ratio=0.3096 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 13 | 43 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@43 distinct=40 range=0..255 ff_ratio=0.6904; u16 distinct=41 range=0..65535 ff_ratio=0.6904; u32 distinct=79 range=16777215..4294967295 ff_ratio=0.6214；原因：schema entity/name unavailable; emit type profile only |
| 14 | 47 | 1 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@47 distinct=25 range=0..255 ff_ratio=0.8530；原因：schema entity/name unavailable; emit type profile only |
| 15 | 48 | 1 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@48 distinct=2 range=0..255 ff_ratio=0.8530; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 16 | 49 | 1 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@49 distinct=2 range=0..255 ff_ratio=0.8530；原因：schema entity/name unavailable; emit type profile only |
| 17 | 50 | 4 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@50 distinct=40 range=1..242 ff_ratio=0.0000; u16 distinct=41 range=1..366 ff_ratio=0.0000; u32 distinct=75 range=124518401..133038445 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 18 | 54 | 12 | `unresolved` | unresolved | profile=profile_server22_unknown_type22.json, rows=449, byte@54 distinct=14 range=11..255 ff_ratio=0.9065; u16 distinct=27 range=11..65535 ff_ratio=0.8820; u32 distinct=27 range=11..4294967295 ff_ratio=0.8820; f32 finite_ratio=0.1158 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### stgn — type 23 / client，business_width=1

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_client23_stgn.json, rows=278, byte@0 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：type profile alone does not uniquely distinguish a schema field; leave unnamed rather than use schema order |

### stgn — type 23 / server，business_width=1

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_server23_stgn.json, rows=278, byte@0 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：type profile alone does not uniquely distinguish a schema field; leave unnamed rather than use schema order |

### unknown(type 30) — type 30 / server，business_width=21

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@0 distinct=256 range=0..255 ff_ratio=0.0045; u16 distinct=26157 range=2..65532 ff_ratio=0.0000; u32 distinct=32184 range=16..656816 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@4 distinct=115 range=0..114 ff_ratio=0.0000; u16 distinct=115 range=0..114 ff_ratio=0.0000; u32 distinct=115 range=0..114 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@8 distinct=256 range=0..255 ff_ratio=0.0033; u16 distinct=366 range=1..366 ff_ratio=0.0000; u32 distinct=6947 range=124518401..132645219 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 12 | 4 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@12 distinct=256 range=0..255 ff_ratio=0.0026; u16 distinct=366 range=1..366 ff_ratio=0.0000; u32 distinct=6767 range=124518401..132710551 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 16 | 1 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@16 distinct=2 range=0..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 5 | 17 | 1 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@17 distinct=2 range=0..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 6 | 18 | 1 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@18 distinct=31 range=0..30 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 7 | 19 | 1 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@19 distinct=4 range=0..3 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 8 | 20 | 1 | `unresolved` | unresolved | profile=profile_server30_unknown_type30.json, rows=72473, byte@20 distinct=2 range=0..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 31) — type 31 / server，business_width=8

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server31_unknown_type31.json, rows=37283, byte@0 distinct=256 range=0..255 ff_ratio=0.2488; u16 distinct=23689 range=0..65535 ff_ratio=0.2457; u32 distinct=28122 range=0..4294967295 ff_ratio=0.2457; f32 finite_ratio=0.7543 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 2 | `unresolved` | unresolved | profile=profile_server31_unknown_type31.json, rows=37283, byte@4 distinct=174 range=1..200 ff_ratio=0.0000; u16 distinct=174 range=1..200 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 6 | 2 | `unresolved` | unresolved | profile=profile_server31_unknown_type31.json, rows=37283, byte@6 distinct=1 range=0..0 ff_ratio=0.0000; u16 distinct=1 range=0..0 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 34) — type 34 / server，business_width=31

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 2 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 3 | 10 | 2 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 4 | 12 | 4 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 5 | 16 | 4 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 6 | 20 | 1 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 7 | 21 | 1 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 8 | 22 | 4 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 9 | 26 | 1 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |
| 10 | 27 | 4 | `unresolved` | unresolved | no row-level profile: auto parser failed its closure check (14 + 7115*44 + 8 != payload length 12); row grammar unavailable；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 35) — type 35 / client，business_width=2

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_client35_unknown_type35.json, rows=890, byte@0 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 1 | 1 | `unresolved` | unresolved | profile=profile_client35_unknown_type35.json, rows=890, byte@1 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 35) — type 35 / server，business_width=2

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_server35_unknown_type35.json, rows=890, byte@0 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 1 | 1 | `unresolved` | unresolved | profile=profile_server35_unknown_type35.json, rows=890, byte@1 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 37) — type 37 / server，business_width=27

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@0 distinct=256 range=0..255 ff_ratio=0.0028; u16 distinct=2894 range=0..7044 ff_ratio=0.0000; u32 distinct=2894 range=0..7044 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@4 distinct=256 range=0..255 ff_ratio=0.0041; u16 distinct=38504 range=1..65535 ff_ratio=0.0000; u32 distinct=42629 range=51..84481 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@8 distinct=256 range=0..255 ff_ratio=0.9618; u16 distinct=2030 range=135..65535 ff_ratio=0.9616; u32 distinct=2036 range=135..4294967295 ff_ratio=0.9616; f32 finite_ratio=0.0384 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 12 | 2 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@12 distinct=137 range=0..232 ff_ratio=0.0000; u16 distinct=137 range=0..2024 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 4 | 14 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@14 distinct=146 range=0..255 ff_ratio=0.0091；原因：schema entity/name unavailable; emit type profile only |
| 5 | 15 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@15 distinct=70 range=0..255 ff_ratio=0.0141；原因：schema entity/name unavailable; emit type profile only |
| 6 | 16 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@16 distinct=54 range=0..255 ff_ratio=0.0292；原因：schema entity/name unavailable; emit type profile only |
| 7 | 17 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@17 distinct=43 range=0..255 ff_ratio=0.0294; f32 finite_ratio=0.9661 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 8 | 18 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@18 distinct=62 range=0..255 ff_ratio=0.0292；原因：schema entity/name unavailable; emit type profile only |
| 9 | 19 | 2 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@19 distinct=178 range=0..255 ff_ratio=0.0339; u16 distinct=178 range=0..65535 ff_ratio=0.0339; f32 finite_ratio=0.9661 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 10 | 21 | 2 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@21 distinct=227 range=0..255 ff_ratio=0.0339; u16 distinct=235 range=0..65535 ff_ratio=0.0339; f32 finite_ratio=0.9823 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 11 | 23 | 2 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@23 distinct=163 range=0..255 ff_ratio=0.0173; u16 distinct=163 range=0..65535 ff_ratio=0.0173；原因：schema entity/name unavailable; emit type profile only |
| 12 | 25 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@25 distinct=70 range=0..110 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 13 | 26 | 1 | `unresolved` | unresolved | profile=profile_server37_unknown_type37.json, rows=465712, byte@26 distinct=63 range=5..127 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 42) — type 42 / server，business_width=13

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_server42_unknown_type42.json, rows=17721, byte@0 distinct=256 range=0..255 ff_ratio=0.0043；原因：schema entity/name unavailable; emit type profile only |
| 1 | 1 | 4 | `unresolved` | unresolved | profile=profile_server42_unknown_type42.json, rows=17721, byte@1 distinct=256 range=0..255 ff_ratio=0.0030; u16 distinct=6167 range=0..65531 ff_ratio=0.0000; u32 distinct=16756 range=16..4286002827 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 2 | 5 | 4 | `unresolved` | unresolved | profile=profile_server42_unknown_type42.json, rows=17721, byte@5 distinct=256 range=0..255 ff_ratio=0.0030; u16 distinct=6167 range=0..65531 ff_ratio=0.0000; u32 distinct=12284 range=2638..4278557307 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 3 | 9 | 2 | `unresolved` | unresolved | profile=profile_server42_unknown_type42.json, rows=17721, byte@9 distinct=2 range=0..1 ff_ratio=0.0000; u16 distinct=100 range=27648..61184 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 11 | 2 | `unresolved` | unresolved | profile=profile_server42_unknown_type42.json, rows=17721, byte@11 distinct=1 range=7..7 ff_ratio=0.0000; u16 distinct=10 range=7..2567 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..2944.0642；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 43) — type 43 / server，business_width=33

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 8 | `unresolved` | unresolved | profile=profile_server43_unknown_type43.json, rows=535, byte@0 distinct=226 range=0..255 ff_ratio=0.0037; u16 distinct=531 range=37..65448 ff_ratio=0.0000; u32 distinct=533 range=859596..2000310215 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 1 | 8 | 8 | `unresolved` | unresolved | profile=profile_server43_unknown_type43.json, rows=535, byte@8 distinct=103 range=0..255 ff_ratio=0.0019; u16 distinct=122 range=85..64704 ff_ratio=0.0000; u32 distinct=122 range=85..91013388 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 16 | 8 | `unresolved` | unresolved | profile=profile_server43_unknown_type43.json, rows=535, byte@16 distinct=135 range=0..255 ff_ratio=0.0019; u16 distinct=188 range=89..65502 ff_ratio=0.0000; u32 distinct=188 range=89..2000104441 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 3 | 24 | 4 | `unresolved` | unresolved | profile=profile_server43_unknown_type43.json, rows=535, byte@24 distinct=14 range=2..84 ff_ratio=0.0000; u16 distinct=14 range=2..84 ff_ratio=0.0000; u32 distinct=14 range=2..84 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 28 | 4 | `unresolved` | unresolved | profile=profile_server43_unknown_type43.json, rows=535, byte@28 distinct=84 range=2..254 ff_ratio=0.0000; u16 distinct=106 range=1041..62535 ff_ratio=0.0000; u32 distinct=106 range=1041..3861111 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 5 | 32 | 1 | `unresolved` | unresolved | profile=profile_server43_unknown_type43.json, rows=535, byte@32 distinct=3 range=1..12 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 46) — type 46 / server，business_width=12

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server46_unknown_type46.json, rows=7, byte@0 distinct=6 range=63..142 ff_ratio=0.0000; u16 distinct=6 range=1907..63039 ff_ratio=0.0000; u32 distinct=6 range=1907..72052048 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server46_unknown_type46.json, rows=7, byte@4 distinct=7 range=56..161 ff_ratio=0.0000; u16 distinct=7 range=1907..60472 ff_ratio=0.0000; u32 distinct=7 range=1907..72049313 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 1 | `unresolved` | unresolved | profile=profile_server46_unknown_type46.json, rows=7, byte@8 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 9 | 1 | `unresolved` | unresolved | profile=profile_server46_unknown_type46.json, rows=7, byte@9 distinct=2 range=1..2 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 10 | 2 | `unresolved` | unresolved | profile=profile_server46_unknown_type46.json, rows=7, byte@10 distinct=2 range=232..233 ff_ratio=0.0000; u16 distinct=2 range=2024..2025 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### lcrg — type 47 / client，business_width=31

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@0 distinct=164 range=0..242 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 1 | 1 | 2 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@1 distinct=1 range=0..0 ff_ratio=0.0000; u16 distinct=1 range=0..0 ff_ratio=0.0000；原因：no schema entry for lcrg; emit only the measured type profile |
| 2 | 3 | 4 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@3 distinct=1 range=0..0 ff_ratio=0.0000; u16 distinct=256 range=0..65280 ff_ratio=0.0000; u32 distinct=1810 range=0..3930880000 ff_ratio=0.0000；原因：no schema entry for lcrg; emit only the measured type profile |
| 3 | 7 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@7 distinct=4 range=0..4 ff_ratio=0.0000；原因：no schema entry for lcrg; emit only the measured type profile |
| 4 | 8 | 4 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@8 distinct=80 range=0..100 ff_ratio=0.0000; u16 distinct=233 range=0..25600 ff_ratio=0.0000; u32 distinct=328 range=0..1677721600 ff_ratio=0.0000；原因：no schema entry for lcrg; emit only the measured type profile |
| 5 | 12 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@12 distinct=27 range=0..93 ff_ratio=0.0000；原因：no schema entry for lcrg; emit only the measured type profile |
| 6 | 13 | 4 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@13 distinct=29 range=0..99 ff_ratio=0.0000; u16 distinct=40 range=0..25600 ff_ratio=0.0000; u32 distinct=80 range=0..1342178575 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..8591260672.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 7 | 17 | 4 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@17 distinct=29 range=0..54 ff_ratio=0.0000; u16 distinct=80 range=0..25600 ff_ratio=0.0000; u32 distinct=95 range=0..8323072 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 8 | 21 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@21 distinct=2 range=0..1 ff_ratio=0.0000；原因：no schema entry for lcrg; emit only the measured type profile |
| 9 | 22 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@22 distinct=7 range=0..7 ff_ratio=0.0000; f32 finite_ratio=0.5253 range=0.0..0.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 10 | 23 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@23 distinct=1 range=0..0 ff_ratio=0.0000; f32 finite_ratio=0.5253 range=0.0..0.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 11 | 24 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@24 distinct=80 range=0..255 ff_ratio=0.4747; f32 finite_ratio=0.5253 range=0.0..0.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 12 | 25 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@25 distinct=2 range=0..255 ff_ratio=0.4747；原因：no schema entry for lcrg; emit only the measured type profile |
| 13 | 26 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@26 distinct=2 range=0..255 ff_ratio=0.4747；原因：no schema entry for lcrg; emit only the measured type profile |
| 14 | 27 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@27 distinct=2 range=0..255 ff_ratio=0.4747; f32 finite_ratio=0.7359 range=0.0..0.0；原因：no schema entry for lcrg; emit only the measured type profile |
| 15 | 28 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@28 distinct=256 range=0..255 ff_ratio=0.0016；原因：no schema entry for lcrg; emit only the measured type profile |
| 16 | 29 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@29 distinct=84 range=0..255 ff_ratio=0.2641；原因：no schema entry for lcrg; emit only the measured type profile |
| 17 | 30 | 1 | `unresolved` | unresolved | profile=profile_client47_lcrg.json, rows=2488, byte@30 distinct=3 range=0..255 ff_ratio=0.2641；原因：no schema entry for lcrg; emit only the measured type profile |

### unknown(type 49) — type 49 / server，business_width=23

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@0 distinct=256 range=0..255 ff_ratio=0.0011; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 1 | 2 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@1 distinct=2 range=0..1 ff_ratio=0.0000; u16 distinct=240 range=23552..59393 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 2 | 3 | 2 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@3 distinct=1 range=7..7 ff_ratio=0.0000; u16 distinct=256 range=7..65287 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 3 | 5 | 4 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@5 distinct=256 range=0..255 ff_ratio=0.0037; u16 distinct=24802 range=0..65535 ff_ratio=0.0000; u32 distinct=330925 range=0..4286003887 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 4 | 9 | 4 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@9 distinct=256 range=0..255 ff_ratio=0.0080; u16 distinct=5165 range=0..65524 ff_ratio=0.0000; u32 distinct=26665 range=0..4286003872 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 5 | 13 | 4 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@13 distinct=249 range=0..255 ff_ratio=0.0206; u16 distinct=1090 range=0..65535 ff_ratio=0.0114; u32 distinct=20397 range=0..4294967295 ff_ratio=0.0114；原因：schema entity/name unavailable; emit type profile only |
| 6 | 17 | 4 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@17 distinct=256 range=0..255 ff_ratio=0.7911; u16 distinct=4531 range=0..65535 ff_ratio=0.7895; u32 distinct=7763 range=16777215..939524095 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 7 | 21 | 1 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@21 distinct=48 range=0..89 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 8 | 22 | 1 | `unresolved` | unresolved | profile=profile_server49_unknown_type49.json, rows=792149, byte@22 distinct=4 range=0..4 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 50) — type 50 / server，business_width=13

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server50_unknown_type50.json, rows=45, byte@0 distinct=17 range=21..235 ff_ratio=0.0000; u16 distinct=19 range=1903..63039 ff_ratio=0.0000; u32 distinct=19 range=1903..2000153732 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server50_unknown_type50.json, rows=45, byte@4 distinct=17 range=2..235 ff_ratio=0.0000; u16 distinct=19 range=1903..65218 ff_ratio=0.0000; u32 distinct=19 range=1903..2000153732 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 1 | `unresolved` | unresolved | profile=profile_server50_unknown_type50.json, rows=45, byte@8 distinct=1 range=0..0 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 3 | 9 | 4 | `unresolved` | unresolved | profile=profile_server50_unknown_type50.json, rows=45, byte@9 distinct=3 range=1..110 ff_ratio=0.0000; u16 distinct=3 range=1..366 ff_ratio=0.0000; u32 distinct=4 range=124518401..133103981 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 51) — type 51 / server，business_width=10

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server51_unknown_type51.json, rows=59, byte@0 distinct=27 range=2..235 ff_ratio=0.0000; u16 distinct=30 range=1903..65218 ff_ratio=0.0000; u32 distinct=30 range=1903..2000153732 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server51_unknown_type51.json, rows=59, byte@4 distinct=3 range=113..173 ff_ratio=0.0000; u16 distinct=3 range=12973..37489 ff_ratio=0.0000; u32 distinct=3 range=1520812..2241197 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 2 | `unresolved` | unresolved | profile=profile_server51_unknown_type51.json, rows=59, byte@8 distinct=3 range=229..232 ff_ratio=0.0000; u16 distinct=3 range=2021..2024 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 58) — type 58 / server，business_width=32

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@0 distinct=8 range=42..207 ff_ratio=0.0000; u16 distinct=8 range=16591..62282 ff_ratio=0.0000; u32 distinct=8 range=28000463..76042892 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@4 distinct=8 range=42..207 ff_ratio=0.0000; u16 distinct=8 range=16591..62282 ff_ratio=0.0000; u32 distinct=8 range=28000463..76042892 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@8 distinct=7 range=61..222 ff_ratio=0.0000; u16 distinct=8 range=603..1871 ff_ratio=0.0000; u32 distinct=8 range=603..1871 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 12 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@12 distinct=7 range=61..222 ff_ratio=0.0000; u16 distinct=8 range=603..1871 ff_ratio=0.0000; u32 distinct=8 range=603..1871 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 16 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@16 distinct=8 range=59..230 ff_ratio=0.0000; u16 distinct=8 range=658..1733 ff_ratio=0.0000; u32 distinct=8 range=658..1733 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 5 | 20 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@20 distinct=8 range=59..230 ff_ratio=0.0000; u16 distinct=8 range=658..1733 ff_ratio=0.0000; u32 distinct=8 range=658..1733 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 6 | 24 | 2 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@24 distinct=3 range=152..182 ff_ratio=0.0000; u16 distinct=3 range=152..182 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 7 | 26 | 2 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@26 distinct=3 range=232..234 ff_ratio=0.0000; u16 distinct=3 range=2024..2026 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 8 | 28 | 4 | `unresolved` | unresolved | profile=profile_server58_unknown_type58.json, rows=8, byte@28 distinct=8 range=16..244 ff_ratio=0.0000; u16 distinct=8 range=1400..38800 ff_ratio=0.0000; u32 distinct=8 range=1400..38800 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 60) — type 60 / server，business_width=10

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server60_unknown_type60.json, rows=59, byte@0 distinct=27 range=2..235 ff_ratio=0.0000; u16 distinct=30 range=1903..65218 ff_ratio=0.0000; u32 distinct=30 range=1903..2000153732 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server60_unknown_type60.json, rows=59, byte@4 distinct=3 range=2..139 ff_ratio=0.0000; u16 distinct=3 range=14475..41004 ff_ratio=0.0000; u32 distinct=3 range=1220652..2177163 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 2 | `unresolved` | unresolved | profile=profile_server60_unknown_type60.json, rows=59, byte@8 distinct=4 range=203..232 ff_ratio=0.0000; u16 distinct=4 range=203..2024 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 61) — type 61 / server，business_width=7

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server61_unknown_type61.json, rows=16, byte@0 distinct=16 range=75..192 ff_ratio=0.0000; u16 distinct=16 range=1099..64704 ff_ratio=0.0000; u32 distinct=16 range=1099..3800256 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 1 | `unresolved` | unresolved | profile=profile_server61_unknown_type61.json, rows=16, byte@4 distinct=1 range=1..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 5 | 2 | `unresolved` | unresolved | profile=profile_server61_unknown_type61.json, rows=16, byte@5 distinct=1 range=231..231 ff_ratio=0.0000; u16 distinct=1 range=2023..2023 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 62) — type 62 / server，business_width=29

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 1 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@0 distinct=9 range=1..37 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 1 | 4 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@1 distinct=256 range=0..255 ff_ratio=0.0042; u16 distinct=23715 range=0..65535 ff_ratio=0.0000; u32 distinct=25034 range=0..84258 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 5 | 4 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@5 distinct=235 range=1..255 ff_ratio=0.8043; u16 distinct=518 range=15..65535 ff_ratio=0.8041; u32 distinct=518 range=15..4294967295 ff_ratio=0.8041; f32 finite_ratio=0.1959 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 9 | 4 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@9 distinct=256 range=0..255 ff_ratio=0.8154; u16 distinct=4955 range=6..65535 ff_ratio=0.8145; u32 distinct=4955 range=6..4294967295 ff_ratio=0.8145; f32 finite_ratio=0.1855 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 13 | 4 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@13 distinct=63 range=0..253 ff_ratio=0.0000; u16 distinct=66 range=0..1500 ff_ratio=0.0000; u32 distinct=66 range=0..1500 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 5 | 17 | 4 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@17 distinct=32 range=0..250 ff_ratio=0.0000; u16 distinct=33 range=0..3000 ff_ratio=0.0000; u32 distinct=33 range=0..3000 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 6 | 21 | 4 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@21 distinct=26 range=0..250 ff_ratio=0.0000; u16 distinct=26 range=0..300 ff_ratio=0.0000; u32 distinct=26 range=0..300 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 7 | 25 | 1 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@25 distinct=8 range=0..7 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 8 | 26 | 1 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@26 distinct=8 range=0..7 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 9 | 27 | 1 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@27 distinct=4 range=0..6 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 10 | 28 | 1 | `unresolved` | unresolved | profile=profile_server62_unknown_type62.json, rows=37214, byte@28 distinct=7 range=0..255 ff_ratio=0.8883; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 63) — type 63 / server，business_width=7

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server63_unknown_type63.json, rows=2, byte@0 distinct=2 range=125..151 ff_ratio=0.0000; u16 distinct=2 range=1149..2199 ff_ratio=0.0000; u32 distinct=2 range=1149..2199 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 1 | `unresolved` | unresolved | profile=profile_server63_unknown_type63.json, rows=2, byte@4 distinct=1 range=3..3 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 5 | 2 | `unresolved` | unresolved | profile=profile_server63_unknown_type63.json, rows=2, byte@5 distinct=1 range=231..231 ff_ratio=0.0000; u16 distinct=1 range=2023..2023 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 64) — type 64 / server，business_width=8

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server64_unknown_type64.json, rows=6946, byte@0 distinct=254 range=0..255 ff_ratio=0.0027; u16 distinct=752 range=11..65035 ff_ratio=0.0000; u32 distinct=753 range=11..82188 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 2 | `unresolved` | unresolved | profile=profile_server64_unknown_type64.json, rows=6946, byte@4 distinct=67 range=0..255 ff_ratio=0.0007; u16 distinct=68 range=0..262 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 6 | 1 | `unresolved` | unresolved | profile=profile_server64_unknown_type64.json, rows=6946, byte@6 distinct=4 range=0..3 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 3 | 7 | 1 | `unresolved` | unresolved | profile=profile_server64_unknown_type64.json, rows=6946, byte@7 distinct=7 range=0..10 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 66) — type 66 / server，business_width=11

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server66_unknown_type66.json, rows=753, byte@0 distinct=192 range=0..255 ff_ratio=0.0066; u16 distinct=343 range=82..65332 ff_ratio=0.0000; u32 distinct=343 range=82..2000274140 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server66_unknown_type66.json, rows=753, byte@4 distinct=100 range=0..255 ff_ratio=0.0027; u16 distinct=131 range=4..65534 ff_ratio=0.0000; u32 distinct=131 range=5..82082526 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 1 | `unresolved` | unresolved | profile=profile_server66_unknown_type66.json, rows=753, byte@8 distinct=6 range=0..5 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 3 | 9 | 1 | `unresolved` | unresolved | profile=profile_server66_unknown_type66.json, rows=753, byte@9 distinct=16 range=0..32 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 10 | 1 | `unresolved` | unresolved | profile=profile_server66_unknown_type66.json, rows=753, byte@10 distinct=23 range=0..45 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

### unknown(type 70) — type 70 / server，business_width=27

| idx | row_off | width | 分配 | 置信度 | 数据证据 / unresolved 原因 |
|---:|---:|---:|---|---|---|
| 0 | 0 | 4 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@0 distinct=256 range=0..255 ff_ratio=0.5439; u16 distinct=1788 range=16..65535 ff_ratio=0.5423; u32 distinct=1807 range=16..4294967295 ff_ratio=0.5423; f32 finite_ratio=0.4577 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 1 | 4 | 4 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@4 distinct=256 range=0..255 ff_ratio=0.5878; u16 distinct=1893 range=16..65535 ff_ratio=0.5861; u32 distinct=1916 range=16..4294967295 ff_ratio=0.5861; f32 finite_ratio=0.4139 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 2 | 8 | 4 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@8 distinct=88 range=1..255 ff_ratio=0.8969; u16 distinct=105 range=1..65535 ff_ratio=0.8969; u32 distinct=105 range=1..4294967295 ff_ratio=0.8969；原因：schema entity/name unavailable; emit type profile only |
| 3 | 12 | 4 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@12 distinct=80 range=0..255 ff_ratio=0.9174; u16 distinct=100 range=5..65535 ff_ratio=0.9166; u32 distinct=100 range=5..4294967295 ff_ratio=0.9166; f32 finite_ratio=0.0834 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 4 | 16 | 2 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@16 distinct=7 range=0..208 ff_ratio=0.0000; u16 distinct=7 range=0..9000 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 5 | 18 | 2 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@18 distinct=9 range=108..231 ff_ratio=0.0000; u16 distinct=9 range=1900..2023 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 6 | 20 | 2 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@20 distinct=15 range=108..241 ff_ratio=0.0000; u16 distinct=15 range=1900..2033 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 7 | 22 | 1 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@22 distinct=53 range=1..172 ff_ratio=0.0000；原因：schema entity/name unavailable; emit type profile only |
| 8 | 23 | 1 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@23 distinct=20 range=0..255 ff_ratio=0.0040; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 9 | 24 | 1 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@24 distinct=16 range=17..255 ff_ratio=0.9094；原因：schema entity/name unavailable; emit type profile only |
| 10 | 25 | 1 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@25 distinct=1 range=255..255 ff_ratio=1.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |
| 11 | 26 | 1 | `unresolved` | unresolved | profile=profile_server70_unknown_type70.json, rows=10075, byte@26 distinct=2 range=0..1 ff_ratio=0.0000; f32 finite_ratio=1.0000 range=0.0..0.0；原因：schema entity/name unavailable; emit type profile only |

## schema 字段未落槽说明

- city 的 Cnam 是 string/language 关联字段，不据此强塞进 1B/3B 槽；本任务的 3B chunk 内部未证明 Calt/Cinh 的精确切分，故 unresolved。
- regi 的 NDBC/FDBC 都是 schema integer 候选，但 +24/+28 在 28 行均为 FFFFFFFF，数据不能区分两者；Rnam 属语言/字符串路径，不由 schema 次序猜槽。
- stad 与无 schema 实体仅给画像；同类型/近似值域的多对多候选无独立锚点，均 unresolved。
- 所有 unresolved 偏移与宽度仍保留 layouts.json 原值；没有合并或重排布局槽。
