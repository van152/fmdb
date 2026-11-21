# t84 — name_table 六成员解包 + name 槽 join(闭 Cnam/Csnm/Nnam/Nsnm/N3ln/cnam/csnm/c3ln)(deepseek)

你是受指挥官委派的子代理。t78 分母账本(E116)里 8 个 name 槽 4CC 全部 `bucket=held`;nation 三条(Nnam/Nsnm/N3ln)注记 **getter 已证但主行 sink 未落**——值不在主行,而在独立成员 `name_table_*` 里。本任务解包这些成员并证明 join。

## 已冻结地基(直接用,不重做)

- **成员位置**:FMF 目录条目 `client_db/name_table_{0,1,2}.dat`、`client_db/name_table_extra_{0,1,2}.dat` 及 `server_db/` 同名六条(t71 chain.json `name_table` 节原文列了全部路径);另存在第三档案 `lang_update_db.dat`(t38 multiframe_report.json 有其目录),name 池是否也在其中=你要查证
- **成员寻址**:E80 口径——member start = data_base(34)+entry.offset,frame 由 `len==size` 选出;zstd 解压载荷;`scripts/fm24_dump.py` 的 load_payload 模式可 runpy 复用(不得修改)
- **槽位挂账**:`scratch/t78/out/buckets.json` occurrences 里 `Cnam/Csnm`(club.xml#club/006/007,E97 r1 held)、`Nnam/Nsnm/N3ln`(nation.xml#nati/007/008/011,getter_proven_but_no_main_row_sink)、`cnam/csnm/c3ln`(comp.xml, E99 held)
- **行框**:`scratch/t71/out/rows_extra3.json` club 行框+fixture(Liverpool ordinal 460/UID 676);nation/comp 行框见 fm24_dump FIELDS 与 reports/club_nation_subtable_schema.json 各 main_row 节
- **锚点真值**:已知俱乐部/国家/竞赛名(Liverpool、England、Premier Division 等)可从 t71 fixture 与 fm24_dump 现有解码行拿

## 任务

1. **解包六成员**(client+server 双档;lang_update 有则三档):逐成员 header/count/行语法/字符串池结构 profiling,产出 `scratch/t84/out/members_profile.json`;每成员给行数、字符串编码、索引→字符串映射示例(≥5 行真名,不得编造)
2. **join 证明**:对 8 个 name 槽,从主行槽值(索引/偏移)→ name_table 成员 → 字符串,验证 ≥50 个对象真名(club/nation/comp 各抽已知名);**wrong-UID 控制同报**(错索引命中率);extra_* 与主池的分工(0/1/2 三池分别装什么、extra 是变体名/多语言?)要给数据判据
3. **闭槽**:join 成立 → 8 条 held 升 L2/candidate(注 provenance:t71/t57/t99 原条目引用);join 不成立 → held 原样保留+首反例
4. **lang_update 档案**若含 name 池,给 client/server/lang_update 三档字符串一致性对拍
5. `verify.py`(独立重抽)+ `--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7

## 避坑纪律

1. 只写 `scratch/t84/` 和 `scripts/t84_*.py`;不碰 reports/、LEDGER、t71/t63/t57/t75 文件
2. 单次文件写 ≤120 行,先骨架后追加;大 JSON 由 builder 生成
3. 负结果原样保留;候选不写成结论;字符串编码不确定时按原始字节呈现,不猜码页
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t84/out/

`members_profile.json`、`joins.json`(8 槽逐条:槽位→池→字符串→命中/反例)、`lang_update_check.json`(若适用)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t84 status=complete`)。
