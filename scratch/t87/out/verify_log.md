# t87 verify log — schema v11 → v11.1 (E121 / t82)

日期 2026-11-21;分支 `t75-wirexref`(工作区当前分支);L4 = 0(未启动游戏/编辑器/IDA,未读 `Z:`,未联网)。

## 1. 输入锚定(构建前,实测)

| 对象 | SHA-256 | 字节 |
|---|---|---:|
| `reports/club_nation_subtable_schema.json`(v11,t77) | `8733497cbd42b33eed7e19a702034dbbc9dc08bb2800d2a30695ef8d2f7cf555` | 29,884,088 |
| `reports/club_nation_subtable_schema.md`(v11) | `3f47bf1661c865635442b0fdc01f76aacc69cc122d5df4ac66cb2817250d582f` | 87,373 |
| `scratch/t82/out/field_map.json` | `2a31c0250c905d45b1528c4196e20da9b492225ccaed17bed976d9060041ddae` | 260,540 |
| `scratch/t82/out/xref_extra3.json` | `944eea8683fcbb1a6a0a8431c4c0f79ba60402fea646de9638eb8cd6479a15ef` | 43,678 |
| `scratch/t82/out/domain_stats.json` | `d61111dc4bfb1734e7083ecbbdf5bddc2f971121dcbd394d2efbde33b43fd7ff` | 42,425 |
| `scratch/t82/out/REPORT.md` | `dd809207499b898125311b79478e76e2aeeaeeceed2f3178b39185e9c3bec343` | 16,996 |
| `scratch/t82/out/DONE.md` | `ee919a9992624c6b39c6d962785ac3911c3ea10c6cb5bb88216859fc96baff0c` | 2,694 |
| `scratch/t82/out/verify.py` | `7a01d870385160a0876aaab0f6647c03b037403d69449a64aac57065a41df1cc` | 33,395 |

LEDGER `E121`:kind=`acceptance` / level=`L3` / date=`2026-11-21`;claim canonical SHA-256 = `714e3331e7a02f6d…`(由 `--verify` 实时复算比对)。

## 2. 产物(构建后,实测)

| 对象 | SHA-256 | 字节 |
|---|---|---:|
| `reports/club_nation_subtable_schema.json`(v11.1) | `f811a216a8d1f72ea98dd86995924a3f55e952bc52b2b23466005dd7a7d4efed` | 29,893,769 |
| `reports/club_nation_subtable_schema.md`(v11 + t87 附录) | `a95a150edee2608ab36aa701d63e4bc045f9208693bb83c95517822c6182db03` | 89,265 |
| `scratch/t87/out/v11_section_digests.json` | 见文件 | 逐节护栏(32 节摘要) |

JSON 增量 +9,681 B;Markdown 增量 +1,892 B(= 附录长度)。

## 3. 三档结果

| 档位 | 结果 | 说明 |
|---|---|---|
| `--selftest` | **9/9** | digest/规范序列化稳定、`adder_guard` 正负用例、`group_l3` 全覆盖、`split_t82` 计数护栏 |
| `--build` | **27/27** | v11 pin 校验、6 个 t82 产物重算哈希、32 个非 mutable 根节 `==` 比对、计数 35/39/131、coverage 43→78 |
| `--verify` | **59/59** | 重读 v11.1 + t82 全量复算;逐节摘要比对;E121 claim 措辞与条目数交叉校验 |

回归:`scripts/t01_anchors.py` **7/7**;`scripts/baseline_coverage.py --check` **CHECK OK**(BASELINE.md 冻结数字不变)。

## 4. 只增不改的自证

`v11_section_digests.json` 记录 v11 的 32 个非 mutable 根节摘要,`--verify` 逐节重算比对 —— 全部一致。

独立旁证(构建时一次性脚本,未入库):用与 `t77_common.json_bytes` 相同的序列化参数重排 v11 基线,可**逐字节复现** 29,884,088 B 的 v11 文件;同一序列化器重排 v11.1 亦可逐字节复现 29,893,769 B。在此前提下按节取原文切片比对,32 个非 mutable 节的**原文字节切片完全一致**,漂移列表为空。

改动面仅:根键 `schema_version`(11→"11.1")、`generated_by`(t77→t87)、`coverage`(只追加键 + `club_main_row_L3` 43→78)、`incremental_provenance`(追加 E121 行 + t87 快照),以及新增根节 `club_extra3_l3_e121`。根键 36 → 37。

## 5. t77 验证器现状(记录性)

`scripts/t77_schema_v11.py --verify` 现为 **59/63**,4 个失败全部是把**已发布文件钉在 v11** 的终态断言,已被 v11.1 超集取代,与本补丁无关:

- `published schema_version is 11`
- `published generated_by is t77`
- `root keys are exactly v10 + the new sections`
- `coverage club_main_row_L3 = 43 (21 + 22)`

t87 的 `--verify` 把该差异做成显式断言(`t77 verifier regressions are limited to the superseded pins`),一旦 t77 侧出现**其它**回归即失败。t77 自身的构建器(纯函数重算 63 项)不受影响。

## 6. 负结果与边界(原样保留)

- t82 的 39 held 与 131 负证**只并入计数与 4CC 列表**,首反例原文仍只在 `scratch/t82/out/field_map.json`;本补丁不复制、不改写、不翻案。
- `reports/xml_denominator_coverage.json` **未改**:117 项 carve-out 仅以 `coverage.club_denominator_note_E121` 注记,桶重发归后续任务。
- `reports/other_tables_schema.json` 未改。
- 未改 LEDGER、未改其它 reports/docs。
