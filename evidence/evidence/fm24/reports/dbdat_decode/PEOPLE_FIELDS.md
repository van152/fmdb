# b36/b41 — people_db 人物业务字段（PEOPLE_FIELDS）

任务书：`prompts/b36_people_fields.txt`。本报告保留 b36 的已解字段结论，并登记 b41 对当前数据源、行链及全量统计的纠偏。只读研究：不启动游戏/编辑器，不写游戏目录、用户目录或 `archive/people_bins/`。

## 证据等级

- **L1**：安装盘字节结构/自洽解码；不得单独写成“独立验证通过”。
- **L2**：与独立公开事实或 `pl_hist_dt` 预言机交叉一致。
- **L3**：exe 静态证据。
- **L4**：游戏/编辑器真实加载；本工作区仍为 **0 项**，未尝试。

当前工具：`scripts/modding_people_fields.py`；人物字段机读映射 `people_field_map.json`、验证报告 `people_field_verify.json`。位置/属性族专项研究见 `scripts/modding_people_attrs.py`、`people_attr_map.json`、`PEOPLE_ATTRS.md`（v2/v3 位置字段 L2 对照完成，PDxx 仍为负结果）。

## b41 数据源纠偏（重要）

- 当前 `archive/people_bins/people_db_streamed_b22.bin` 为 400,443,970 B；`basic_people_db.uncompressed.bin` 为 54,060,043 B。当前 basic 原件按 ordinal→PID 与 people 行尾 `<u32 ordinal><u32 PID><u32 PID>` 严格重建，得到 **658,011** 个唯一行，连续覆盖 people_db offset **6..400,443,942**，文件尾余 **28 B**。
- 当前行 variant：v1=166,064、v2=476,158、v3=4,757、v4=9,839、v5=1,193。完整链与当前 basic 的 ordinal/PID 一一对应。
- **撤回旧缓存统计**：`<OLD_REPO>\tmp_b36\rows.pkl` / `basic_walk.npy` 与当前 basic 原件不匹配；旧缓存把 ordinal 0 映射成 PID 50,331,648（当前 ordinal 0→PID 3），并制造 4,312 个重复 ordinal-0 假命中；旧行链从 trailer offset 45 起算，而当前 payload 起点为 6。旧 662,324 行口径不再使用。缓存保留只读。
- 已修正 `scripts/modding_people_fields.py`：默认从 current basic 原件解析，不再在只读 `archive/people_bins/` 下创建 pickle；people 行链按当前 ordinal/PID 与行头重建。`people_field_verify.json` 已由该链重跑。
- 因旧行索引不匹配，旧全量 `Pcti` / `Pcjd` 计数（如 208,600、100,821）撤回；字段候选与已知人样本事实仍保留，完整人群统计待当前链重跑。身高/体重与 Pcex 数字已在当前链上重算。

## 1. 验收项状态

| 项目 | 当前结果 | 证据/边界 |
|---|---|---|
| 身高+体重 | 22/22 解出；精确匹配：身高 16/22、体重 15/22；`|Δ|≤2 cm` 身高 22/22、`|Δ|≤6 kg` 体重 22/22 | L2 公开样本。C. Ronaldo 无顶层姓名锚，使用 basic PID 735216 定位行，并在该行唯一匹配公开 packed DOB 字节；此特殊路径已在 JSON 记录，不等同于常规姓名锚解码。公开体重来源间可能有口径差异。 |
| DOB | 21 个常规姓名/DOB 锚 + C. Ronaldo PID 行内唯一 packed-date 候选；报告为 22/22 与公开生日相符 | L2；CR7 路径须保留上述限定。 |
| CA/PA 候选 | 行首 +5 的 5×u16 范围 0..200；CA≤PA 样本比例约 98.3%；字段名未坐实 | L1 + 弱 L2（值域、排序、人名合理性）；不能声称官方 CA/PA 字段已验证。 |
| 当前俱乐部 Pcti | v2 行首 +30 候选；已知人样本与公开俱乐部/`pl_hist_dt` 相符 | L2；旧全量计数撤回，当前链完整人群计数待重跑。 |
| 加盟日 Pcjd | v2 行首 +108 / DOB 相对 +108 候选；Messi 等已知样本与历史加盟日相符 | L1/L2；旧全量 100,821 计数撤回。 |
| 合同到期 Pcex | 当前严格行链：签名 448,255/658,011；真实日期 249,701、1900-01-01 null 198,554、无签名 209,756 | 结构统计 L1；Messi/Busquets、Mbappé、Haaland 等公开日期吻合为 L2。真实日期占当前全行 37.95%。 |
| 位置族 / PDxx 属性族 | v2/v3 14 个位置码完成 L2 对照；PDxx 仍为明确负结果 | 22/22 Natural-20 槽值核对覆盖 14 个位置码、20 个 UID；row+49..+102 仅为 54 B 属性候选，0 个 PDxx byte index 达到 L2。v1 另布局未解，详见 `PEOPLE_ATTRS.md`。 |

## 2. 数据布局

### 2.1 `basic_people_db.uncompressed.bin`

- 54,060,043 B；`<u32 count=658,011><u8 flag>` 后为 658,011 条变长记录，消费到 offset 54,060,034，余 9 B。
- 记录：`<u8 0x11><u8 class>` + class fields + `<u32 ordinal><u32 PID><u32 PID>`；ordinal 0..658,010 连续，PID 双写。
- 当前 class/variant 分布：class1=166,064、class2=476,158、class3=4,757、class4=9,839、class5=1,193；长度分别 83、83、83、34、22 B。类名字符串来自此前 `fm.exe` 静态发现（L3），记录形态/数量为 L1。
- 83 B 摘要记录中 `+42..+51` 是 5×u16 ability/reputation 候选；它为 CA/PA 字段名提供不了独立真值表。

### 2.2 `people_db_streamed_b22.bin`

- 当前 payload 行链从 offset 6 开始；每行以 `<u32 ordinal><u32 PID><u32 PID>` 结束。严格链 658,011 行，长度 33..2,154 B，尾余 28 B。
- 行首 `<u32 ordinal><u8 variant>`。姓名/DOB 锚格式仍为 `FF FF FF FF 00 | u32 byte_length | UTF-8 name | u32 packed DOB`；变长字段偏移随 variant/布局漂移。
- 当前链严格 trailer 候选总数 660,606；链选择 658,011 个，其余 2,595 个是落在有效链之外的额外字节候选，不能当作新行。

## 3. 已有业务字段候选

| 字段/候选 | 偏移 | 当前状态 | 证据 |
|---|---:|---|---|
| row ordinal / variant | +0 / +4 | 结构字段 | 当前链全量 ordinal/PID/行头交叉，L1 |
| 声誉/能力 5×u16 | +5 | 值域和顺序候选；CA/PA 名称未定 | medium（值）/low（名称） |
| Pcti 当前俱乐部 | v2 +30 | 已知样本通过；全量统计待当前链重跑 | L2 样本 |
| 身高/体重 R1 | v2 +126 | `53 ff 00 00 01 | u16 weight_kg | u16 height_cm` | 22 人公开对照，L2 |
| 身高/体重 R2 | v1 变长位置约 +99/+102/+105 | `01 00 6c 07 00 ff | flag | 00 | u8 weight | u8 height` | 10 名 v1 样本，L2 |
| Pcjd 加盟日 | v2 +108；DOB 相对 +108 | 样本候选 | L1/L2 |
| Pcti v1 | +136 候选 | v1 子布局未穷尽 | low/medium |
| Pcjd v1 | +148 候选 | 883 hit 的旧口径未复核 | low/medium；全量计数撤回 |
| Pcex 合同到期 | DOB 相对 +579 | `ff×7 | u32 packed date | 01 00 6c 07 | u16 Pces` | 当前链 L1 普查；公开日期 L2 |
| Pdob 出生日期 | DOB 相对 +797 | `(year<<16)|1-based day_of_year`；1900-01-01 为 null | 22 人事实样本；CR7 使用 PID 行候选，L2 有限定 |

packed date：`(year << 16) | 1-based day_of_year`；`0x076c0001` 为 1900-01-01 null 哨兵。

### 3.1 身高/体重当前链普查

- R1：v2 20,661 行、v3 512 行，共 21,173。
- R2：v1 52,330 行、v3 2,586 行，共 54,916。
- 合计 **76,089/658,011（11.56%）**；v1=52,330/166,064，v2=20,661/476,158，v3 混合命中 3,098/4,757，v4/v5=0。
- L2 样本：22/22 解出；当前脚本输入事实下精确身高 16/22、精确体重 15/22；身高差≤2 cm 为 22/22，体重差≤6 kg 为 22/22。b34 旧负结果的原因已定位：身高/体重在姓名/DOB 锚前的行头区，b34 只向锚后搜 512 B。

### 3.2 合同到期 Pcex 当前链普查

- 签名 hit 448,255；其中有效真实日期 249,701、1900-01-01 null 198,554；无签名行 209,756。
- 真实日期 249,701/658,011 = 37.95%。到期年（null 除外）top：2024=134,914、2023=53,017、2025=31,897、2026=12,503。
- Pces top：3=447,826、0=428、183=1（签名 hit 范围）。外部样本：Messi/Busquets 2025-12-31、Mbappé 2024-06-30、Haaland 2027-06-30。

## 4. 复跑

```powershell
py -V:3.12 -I scripts/modding_people_fields.py --selftest
py -V:3.12 -I scripts/modding_people_fields.py --map --out reports/dbdat_decode/people_field_map.json
py -V:3.12 -I scripts/modding_people_fields.py --verify --out reports/dbdat_decode/people_field_verify.json
py -V:3.12 -I scripts/modding_people_attrs.py --selftest
py -V:3.12 -I scripts/modding_people_attrs.py --verify
py -V:3.12 -I scripts/run_regression.py
```

Python 3.12 环境需含项目 numpy/zstandard 依赖。所有输出仅写当前工作区；不使用旧 `tmp_b36` 行缓存作统计依据。

## 5. 未解与负结果

1. **位置向量**：v2/v3 14 槽 row+34、row+36..+48 已按 `Pgoa,Pdls,Pdce,Pdrs,Pdmc,Pmls,Pmce,Pmrs,Paml,Pamc,Pamr,Pace,Pwbl,Pwbr` 完整映射；row+35 恒为 1。22 个 FM Scout `Natural 20` 字段对照覆盖全部 14 码、20 个 UID；来源 rev=24.0 与本地 24.3.0 存在版本差异，详见专项报告。
2. **PDxx 属性**：v2/v3 row+49..+102 的 54 B 窗口仅为 L1 候选（全窗≤20：v2 471,802/476,158、v3 4,727/4,757；合计 476,529/480,915；79.62% cells 为 0）。无逐码映射、无独立原始 1..20 表；v1 +21 u8[54]/+22 u16[14] 仍是稀疏/混合候选，0 值语义未定。负结果和排除路径见 `PEOPLE_ATTRS.md`。
3. **CA/PA 字段名**未坐实。当前证据上限 medium/弱；未找到第三个独立精确 CA/PA 数据源。
4. **Pcti/Pcjd 全量统计**：旧缓存口径撤回；已知样本语义仍保留，完整计数待当前严格链重跑。
5. **Pcwg 工资 / Pmsq / Psnu / Pnti 第二国籍排序**仍未完全定型；variant 1 子布局未穷尽。
6. **L4=0**：没有启动游戏或编辑器，也没有真实加载验收。
