# t35 Cafl/Cvfl 数据侧发现

## 结果

状态：`partial_no_semantic_candidate`。按 t14 的 74 个 RTTI/table type 和 stage2 的 45 条身份记录完成语义扫描；未找到 affiliation/link 类候选。Cafl、Cvfl 仍为 unknown。
未对静态 cursor 做分析，也没有字段晋级 L3。

## 候选扫描

- 正向语义候选：0。扫描词见 `profiles/semantic_candidate_scan.json`。
- t14 类型：74；stage2 记录：45。
- club-related RTTI near-miss：6 项；它们没有 affiliation/link 类名或独立 Cafl/Cvfl join，不作为候选。
- Cafl/Cvfl 的 29/19 个 schema item 字段按 master.json 与 t24 顺序交叉核对；它们仍是 schema 候选，不是数据列名。

## 父表数据画像

`table_type=3` 是 stage2 已解析的 club 父表，只作上下文，不能复制成 Cafl/Cvfl table_type。
- client：状态 `complete_parent_client_row_profile`；count=84259；stride=variable；封口 `14 + 6932060 + 8 = 6932082`；payload SHA-256 `db8ea78cbb8fcc7973525b04f55ca1b2c9dafda1e096dfa15c1affcdcc4fab9f`。
- client 行跨度：54..156 bytes，87 种；标准 5B 聚合行 84,256，identity-only 紧凑行 3。
- server：状态 `partial_payload_only_no_row_walk`；payload bytes=16595312；row_count_header=84259；未做行 walker，不能给 count/stride/封口。
- parent 原始 u32 lane 与 5B aggregate 的逐 bit 统计保存在 `profiles/parent_table3_context.json`；这些统计没有语义列名，不能视作 affiliation item 字段画像。

## 视图假说

结论倾向：`no_data_vote`，当前数据不能支持或反驳‘同一集合的两个视图’。没有找到两张 affiliation-like archive table，也没有提取到可检验的 Cafl/Cvfl item 列。
保留反例/限制：RTTI 无命中不证明子表不存在；它可能嵌在 club 父记录或使用无语义 RTTI。client club 表中 3 条 compact body 仅由 identity 封口，未解 body 不作为视图证据。

## Copy-ready

`cafl_cvfl_discovery.json` 中 `copy_ready` 对 Cafl/Cvfl 分别保留 `candidate_table_type/archive/rtti_class/count/stride=unknown`、空 `item_field_candidates`、schema-only 字段和 blockers。
与 sol 衔接：可复用‘无命中’和 table_type=3 仅为 parent context；下一步仍需沿已知 +0x118/+0x120 collection 找到独立 archive/row 证据，再做 item 列画像。

## 验证与边界

- 输入快照：master SHA-256 已与 evidence/MANIFEST.json 匹配；t14、stage2、t24 part 哈希与 t29 provenance 匹配。
- `fm24_dump.py --archive client --table 3` 原命令因既有 `footer_offset` 十六进制字符串转 int 报错；本任务未改该脚本，使用了独立行 walker复算 client 闭合。
- server table_type 3 只记录唯一 header-compatible frame 的 payload 元信息，没有推断行边界。

验证命令：`py -V:3.12 -I -B scratch/t35/out/verify.py` 与 `py -V:3.12 -I -B scripts/t01_anchors.py`。
