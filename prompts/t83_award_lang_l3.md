# t83 — award(0)/language(8)/weather(27)/derby(18)/media(7) 五表 L3 升级 + t76b 遗产吸收(neon 攻坚 #3)

你是受指挥官委派的攻坚车道(neon xhigh,agy CLI)。E115(t74)已把这五张表双档行框闭合;E118(t76c)已把 weather/derby 槽位做到 L2(含 derby 6B 差=3 个非 client 字段 D1tw/D1td/D1tl、weather 95B=3+4×23 两条结构判定);t76b(award/language/media L2 扫表)三连墙零落盘已弃——**其表并入本任务**。目标:五表槽位语义升 L3(exe 静态三重闸门),award/language 先补 L2 profiling。

## 已冻结地基(直接用,不重做)

- `scratch/t74/out/frames.json`:award 77B 定长×3,545(双档逐字节同构);language [u32 len][UTF-8 名][17B 后缀][13B identity];weather [u32 len][名][95B=3+4×23][13B];derby k∈{2,4} lstr 名+(const−4k) 数字段 const=65/71;media identity DP 唯一铺法、server 每行 +7B(插在 identity 前)。header 14/footer 8,identity 13B 行尾
- `scratch/t76c/out/slots_{client,server}_{18,27}.json`:weather/derby 逐列 L2 槽位与锚点(含 `1wcf/1wcl` 族 FK 域)
- `scratch/t79/out/field_map.json`:getter+setter 双链范式与 4CC gate 记法(t83 输出沿此格式)
- 静态:只读 `D:/tmp2b/fm24/input/editor.exe`(SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`);helper 区 0x151d2e0/0x151d710/0x15211a0/0x4339e80/0x433bbc0/0x4342940 已证可复用
- schema:`evidence/fm24/reports/editor_schema/master.json` 的 entities(award/weather/derby/media/language 相关 .xml 键)+ enums + field_codes;XML 端分母见 `reports/xml_denominator_coverage.json`(若已由 t77 落盘;否则用 master.json 自数)
- fm24_dump FIELDS 既有锚点:award `rdui@64/duni@68`、language `rdui_suffix@17`;t76c 冻结锚点不得冲突

## 任务

1. **award/language 先补 L2**(数据侧):award 77B 逐列 profiling(双档 3,545 行向量化,0xffffffff 与合法 0 分列)、language 17B 后缀 + 13B identity 逐列;master 字段按 type 宽度×值域×FK(t30 伤病、t10 nation、t25 comp、t3 club ordinal/UID 域,wrong-UID 控制同报)给候选
2. **weather/derby 升 L3**:对 t76c 的 L2 槽位逐个走三重闸门(frozen 唯一 occurrence → getter 4CC gate → 同位移 sink + 全档域);derby 的 D1tw/D1td/D1tl 三 u16 与 server +6B 段优先
3. **media(7)攻坚**:中段嵌套 count/list 结构(t74 记载未解;client fitcount {1:105,0:57,2:46},server 无简单拟合)→ 静态链先定结构,再数据侧闭合;identity 前 5B 16 种取值给解释或 held
4. **三重闸门照旧**:过闸 L3(注明二进制/VA/来源);不过闸 held+首反例;t63/t57 negative 不翻案(除非新链证据明确推翻并引用原条目);业务名不发明
5. **独立 verify.py**(不 import builder/fm24_dump)+ builder `scripts/t83_*.py`;`--help`/`--selftest`;退出码 0/1/2;t01 anchors 7/7

## 边界

- 只做这五张表;不碰 stadium/team(t79)、lcrg/agreement(t76c 已收)、club/nation/comp 主行
- **防冲突**:只写 `scratch/t83/` 和 `scripts/t83_*.py`;不碰 reports/ 与 LEDGER
- 不启动游戏/编辑器/IDA,不联网,不读写 Z:;全档验证向量化,不得抽样代替

## 交付 scratch/t83/out/

`field_map.json`(增量 grades,引用 t63/t74/t76c 既有 id)、`xref_{award,language,weather,derby,media}.json`(静态链+成员台账)、`domain_stats.json`(全档域)、`verify.py`、`REPORT.md`、`DONE.md`(首行 `DONE type=t83 status=complete`)。

Python `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`。
