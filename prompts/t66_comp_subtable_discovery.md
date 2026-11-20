# t66 — Comp 子集合/子表发现(t59 opaque 集合的母行普查,sol;复刻 t46/t51 方法)

你是受指挥官委派的子代理。t59(E99)在 comp table_25 主行内发现 server 独有 opaque 集合:`vec30`(u32 count+2N,本档全 0)、`vec18`(i32 count+逐 item tag 8/9B,32 行非空)、`+0xe8`(149 行,per-item 10/11/12B)、`+0xc0`(366 行,外 count+内 count×12)、`+0xc8`(121 行,25B)、`+0xd0/+0xd8`(各 51 行,15B)、`+0x100`(i16 count×5)、`+0xa8/+0xe0`(presence 全 0,静态分支无实档坐标)。本任务按 t46(nation 母行)/t51(unknown parent)方法做 **comp 子集合发现与文法闭合**,不贴语义名。

## 必读
- AGENTS.md(候选不写结论;negative 原样;L4=0)
- scratch/t59/out/REPORT.md + field_slots.json + field_map.json(**集合坐标与行框唯一来源**;identity 12B+footer 9B 口径)
- scratch/t46/out/REPORT.md(母行普查法:双档 count/消费逐行一致、identity census)
- scratch/t51/out/REPORT.md + t51_spot(unknown parent 收口法)
- reports/club_nation_subtable_schema.json(v8;club 8 子表/CLUB_LINK 已闭,**不要重做**; nation_t9_wire 参考)
- scratch/t53/out/REPORT.md(TCrs 先例:main reader 与 getter 后缀两个层级的裁决口径)

## 任务
1. **集合盘点**:按 t59 坐标逐集合建立双档母行台账:哪些行非空、count 分布、per-item 字节文法、绝对 offset 界;`vec30` 全 0 与 `+0xa8/+0xe0` presence 全 0 如实记(候选:静态可选,不强行赋语义)。
2. **文法闭合**:每个非空集合给出 item 文法(字段宽/tag/引用),判据:双档逐 item 消费一致 + 母行边界闭合 + 值域自洽;过闸 → L3;否则 held 留首反例。集合若指向独立 subtable 成员(table_XX.dat),按 t46/t51 收口(不猜测成员名,须 entry 实证)。
3. **引用核验**:item 内引用(nation/club/comp 自引/stadium/city)走目标实表 ordinal 集;wrong-UID 控制例照 t59 口径。
4. **双档差异如实**(server-only 集合的 client 对应物:确认 client 真无或未触发,给静态/数据双侧证据)。
5. 独立 verify.py(不 import builder/ReaderCFG/fm24_dump)+ builder scripts/t66_comp_subtable_discovery.py;--help/--selftest;退出码 0/1/2。

## 边界
- 只 comp 派生集合;不碰 club/nation 已闭层、不碰 t59 主行已闭 L3(其坐标可引用);opaque 不贴业务名;vec30 全 0 不赋语义。
- 预算内无法全闭则诚实 partial:优先级 vec18(32 行)→ +0xe8(149)→ +0xc0(366)→ +0xc8(121)→ +0xd0/+0xd8(51)→ +0x100 → 其余。

## 交付 scratch/t66/out/
- collections.json(逐集合台账+文法+grade)、census.json、verify.py、REPORT.md、DONE.md;scripts/t66_comp_subtable_discovery.py

Python `py -V:3.12 -I -B`;FM24_DB_DIR=<WORKSPACE>/scratch/data;完成跑 verify + scripts/t01_anchors.py(7/7)。
