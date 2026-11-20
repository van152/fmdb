# t44 — Cafl/Cvfl 俱乐部附属关系 静态发现(t35 负例攻坚,集合追踪法)

你是受指挥官委派的子代理,负责**最难**的发现任务。t35(luna 数据侧)已诚实负例:**74 类 t14 census + 45 行 stage2 全扫,0 语义 RTTI 候选**(AFFILIAT/CLUB_LINK/FEEDER/FARM/SATELLITE 等全空),Cafl/Cvfl 的 table_type/archive/RTTI/count/stride **全未知**。本任务用 **静态集合追踪**(t39/t41 已证法)从 CLUB 对象分发反查真实表,突破无语义锚点困境。

## 必读
- <WORKSPACE>\AGENTS.md(硬约束)
- scratch/t35/out/cafl_cvfl_discovery.json + REPORT.md(**负例真源,原样保留不删改**;view_hypothesis/unknown_list/near_miss_club_classes)
- scratch/t39/out/REPORT.md + scratch/t41/out/REPORT.md(**集合追踪范例**:Club slot2 `0xe89a00` 按 4CC 精确分发→集合 helper(全局 VA table `+0x80` vector,t39=0x141b60158/t41=0x141b601e8)→entry vptr→factory case→table_type;owner 筛选 outer+0x30)
- scratch/t27/out/replication.md(cursor 方法模板)
- evidence/fm24/reports/editor_schema/master.json(club.xml#club Cafl/Cvfl,冻结 SHA 7d57477e 对照 MANIFEST)
- scratch/t24/out/subtables.part003.json(Cafl idx370-398 / Cvfl idx400-418 nested occurrence)

## 已知锚点
- `Cafl`="Current Affiliations",**29 item 字段**(idx370-398):affl(Affiliated Club,database_record_unique_id→club/t3)、ismc(bool)、stdt/endt(date)、type(enum)、yfee(cash)、fri%(int)、msls/pwgp(int)、+18 bool(frly/golo/fotb/UsSK/plfr/smbo/fnhl/perm/yutr/hlwf/mrrl/scks/cpsd/ualf/lpfs/ustf/yout/rsrv/pfpr/bttr)。
- `Cvfl`="Validated Current Affiliations",**19 item 字段**(idx400-418):Cafl 子集 + `clfr`(Validated?,enum),少 endt/UsSK/ualf/lpfs/ustf/msls/yout/rsrv/pfpr/pwgp/bttr。**强 hypothesis:一集合两视图**(Cvfl=validated 子集),待静态证实/否证。
- parent table_type3(LEAGUE_BODY_CLUB,club.xml#club,84259 行)**仅上下文,不可拷为 Cafl/Cvfl table_type**(t35 data_boundary_note)。
- 多帧/data_base:成员绝对起点=data_base(34)+entry.offset,按 entry.size 选帧(E80);entry.sha256=压缩区 SHA。

## 任务
1. **静态发现 table_type**:CLUB slot2 `0xe89a00`(或实际 club getter)按 4CC `Cafl`/`Cvfl` 精确分发→追集合 helper→全局集合 table→entry vptr→factory rel32 表 case→**确定 table_type/archive/RTTI/count/stride**。保存每跳 bytes+VA+指令分片。若 Cafl/Cvfl 共用一表(两视图)或各自独立表,如实判定。
2. 若发现独立表:两 archive 目录+payload(count/stride/SHA,client 无成员如实记);factory→RTTI/vtable→slot19→真 reader(+identity tail),PE runtime-function extent 建可达 CFG(t21b_control_flow.ReaderCFG),追 thunk。
3. 分支五分类逐条证据+首反例;变长则按 t41 法(wire count 决定 row_len)。
4. walk 逐行闭合 header+Σrow+footer==payload_len;双坐标 legacy14/wire13;identity 后置校验;selector 全表观察。
5. 三重闸门+全表画像:affl ordinal 引用走 club/t3 实际 ordinal 集;stdt/endt packed date;yfee cash i32;type/clfr enum 域;**18+ bool 验是否同字节 bitmask**(t31 法);fri%/msls/pwgp integer 有符号/sentinel。可证实者 L3,域冲突 held 留首反例。
6. 若**无独立表**(附属列表嵌入 parent 记录或 uninformative RTTI):诚实 negative + 静态证据指明列表实际所在(parent 内偏移/集合成员),保留 t35 负例,不强行晋级。
7. 独立 verify.py(不 import builder)+ builder scripts/t44_cafl_cvfl.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 Cafl/Cvfl;不碰已闭 club 子表;发现其它 unknown parent 另案。
- 候选不写结论;t35 negative/held 原样保留;L4=0;不启动游戏/编辑器/IDA,不联网,不读写 Z:。
- 预算内无法发现/闭合则诚实 partial+已绑定子集+剩余+首反例(发现任务允许 negative)。

## 交付 scratch/t44/out/
- discovery_cafl_cvfl.json(table_type 判定+静态链)、cursor_*.json/fields_*.json(若闭合)、instructions.part*.json、branches.part*.json、verify.py、REPORT.md、DONE.md
- scripts/t44_cafl_cvfl.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;只写 scratch/t44/ 与 scripts/t44_*.py;完成跑 verify + t01_anchors.py(7/7)。