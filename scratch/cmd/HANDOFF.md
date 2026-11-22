# HANDOFF — 指挥官收尾交接(2026-11-22,E140 终态)

本文件记录收尾时的完整状态与下一 session 恢复指令。已接受工作全部提交。

## LEDGER / 分支
- **LEDGER 140 条,末 E140**(`scratch/t01/LEDGER.json`,append-only;E129–E139 为 Wave 12 十一条,E140 外部语料+锚交叉验证)。
- 分支 `t75-wirex`,工作树收尾时仅余 t93 车道半程产物(随本次交接入库)。
- 本轮末次提交:`1919182`(E140)、`5842fce`(t92 日志)、`33024b1`(E139 v11.3 定稿)。

## Wave 12 + E140 核心成果(E129–E140;细则以 LEDGER 为准)
- **E132/E138 table_45 结构定论**:uniform 行分解(rowlen=80+namelen 普适)、三列冻结(club-uid@0 / rec_type@4=37 值 / person-uid@5)、**117 码=访问器视图**(family→rt:CFG→24/CHA→13/CHS→25/CLA→26)。
- **E130 [NATION+0x108]=NATION_T9 L3 定论**(getter 0x1410668f0 / setter 0x141063f30 双路由闭环)。
- **E133 table_9 文法闭**:client 31,956 精确;server **307,564**(纠 E127 九字节);ordinal/sentinel lane 251/251。
- **E135–E137 CBW 终判**:CBDa/CBWa/CBWo/CHSo 在 editor.exe+fm.exe 零存在(全量扫);E121 cmp 位点引用降级。
- **E129/E139 schema v11.2→v11.3**(43 根节),分母 1034 行守恒+117 条改路由注记。
- **E140 外部语料侦察**:三仓入 scratch/ext/(fmsave@755fe9c 纯 Python zstd 存档解析 1,417 字段字典;fm-editor@ba605f4 FM24 内存布局;FMLibreEditor@fb76023 FM27 recon)。"几乎通用"三轴成立。**UID 锚满贯 4/4**:Harry Kane person=28049320+club=728(Tottenham)三元收敛;Ronaldo 735216、Bayern 915、Antalyaspor 1865 全命中(`scratch/cmd/t93_ext_probe.json`)。

## t93 车道状态(收尾时 in-flight!)
- **attempt 2 运行中**(attempt 1 rc=1 节流重试),交付目录 **`scratch/t93/outbox.md/`(车道把 outbox 参数当目录写,quirk 保留)**。
- 已落 6/9:`README.md`、`save_grammar.json`、`field_dictionary.json`、`fm24_fields.json`、`fm24_memory_layout.json`、`fm27_recon_digest.json`。
- **缺 3+1**:`crosswalk.json`、`verify.py`、`REPORT.md`、`DONE.md`。
- 车道脚本 `scripts/t93_{fields,fm24,recon}.py`(767 行)已入库。
- **恢复指令**:若关机杀死 → 新会话名重发(避免 stale outbox 误报):`bash scripts/launch.sh t93b devseek deepseek-v4.1-flash-free prompts/t93_ext_mining.md scratch/t93/outbox2.md 3 2400`,brief 里注明只补缺的 4 件;若 `DONE.md` 已存在 → 直接验收(程序:lane verify + 根 diff 抽查 + E141 入账)。

## 下一 session 待办(优先级)
1. **t93 验收**(或重发,见上)——验收后字典喂 suffix→列钉死(83 码)。
2. **t94:t14 handler 全量反编译**(新最短路径):`scratch/t14/out/census.json` 已冻结 **74 表入口(63 dedicated handler_off)**——逐表反编译 handler 本体,字段读取序=wire 列序,预计一棒吃 10–20 表;静态已授权无需 t02。
3. **t95 三小件**:社区 custom DB(editor data)差分挖矿;lang_update_db 全解(官方字段显示名);11 张 default handler 表一次收。
4. **待用户决策(不变)**:Phase 3 **t02 定向编辑器授权**——时间线最大压缩杠杆(估省 3–5 波);之后 t86 统一只读库。merge-to-main 评估备于 `docs/REPO_STATUS.md` §六。
5. 进度口径(实测):74 表分母,已透 6 表(8% 按表数 / ~25% 按难度加权);只读全解包估 12–14 波,t86 可用约 8–9 波。

## 关键锚点 / 约束(不变)
- editor.exe SHA `b82ebe8e032f2017...`(只读 D:/tmp2b/fm24/input);frozen master `7d57477e...`;t37 baseline REPORT `5656568e...`/inventory `8af89c72...`(原样保留)。
- **E80**:成员绝对起点=`data_base(34)+entry.offset`,按 `entry.size` 选帧;`entry.sha256`=压缩区 SHA(非 payload SHA)。
- **E138**:table_45 wire 三列+行框冻结(`scratch/t88/out2/row_frame.json`;`_p_server_45.bin` 84,477 行)。
- **E140 纪律**:外源仓(scratch/ext/,gitignored)零执行、标签仅假设源、provenance=ext/<repo>@<hash>。
- 硬约束(AGENTS.md):只读 Z:/D:\tmp2b\fm24;不启动游戏/编辑器/IDA 除非用户显式授权;L4=0;负结果原样保留不删改;候选不写结论;Python `py -V:3.12 -I -B`,新脚本 --help/--selftest,退出 0/1/2;大数据/二进制不入 repo;车道只写 scratch/<task>/ 与 scripts/tNN_*.py。
- 验证:`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;anchors `scripts/t01_anchors.py`(**7/7 绿**);zstandard vendored 于 `D:/tmp2b/fm24/tools/python`(`-I` 下须 sys.path.insert);GBK 终端先 `sys.stdout.reconfigure(encoding='utf-8',errors='replace')`。
- 车道运营教训(E128 meta+本轮):launch.sh DONE 判定续作车道误报(stale outbox)→ 续作一律独立 outbox;devseek rc=124→微交付(每小节覆写落盘、≤120 行分块、先骨架);outbox 参数可能被车道当目录(outbox.md/ quirk)→验收时查两处。
