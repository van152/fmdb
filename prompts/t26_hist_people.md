# t26 任务书:未覆盖档案数据侧普查(hist 族 / people_db / 小件)

先读 `AGENTS.md`。这是纯数据侧任务,**不需要分析 exe**。四个子任务相互独立,按 A→B→C→D 优先级做,每个子任务独立落盘;**卡壳立刻把已有进度写成 partial,再做下一个**。输出预算纪律:单次输出 ≤64K token,输入引用 ≤250K token,大结果写文件不要打印。

## 已有基线(t15b 清点,直接复用其脚本手法)

- 容器处理先例:`scratch/t15b/probe.py` / `probe2.py` / `probe3.py`(tad. 外壳 + zstd 解压、tadc v3 串联 zstd、tad. v1 u32 数组)。数据一律用本地镜像 `<WORKSPACE>/scratch/data/`(原始容器文件),**不读写 Z:**。
- `people_db.dat`:tad. + zstd@8,解压后 400,443,970 B;头部 `u32@2 = 658011`(与 basic_people_db 行数完全一致);probe3 已从 pos 6 走通 1193 行 compact 文法:`row_span = 33 + name_len`,全 type 5,key 范围 [656818, 658010],duni 范围 [2002040996, 2002042188],见 `scratch/t15b/out/probe3.json`。
- `non_pl_hist_dt.dat`:27.6MB,tadc v3 + 串联 zstd,容器已进、表层未拆。
- `non_pl_hist_id.dat` / `pl_hist_id.dat`:tad. v1 + u32 数组。
- `summary.dat`:tad. v3569 自有文法(无 zstd);`lang_update_db.dat`:内嵌 fmf. 目录。
- **165,461 悬案**(晨报 E58/t15c):t49 引用行中未命中 person duni 的净差,假设去向是 non_pl_hist 族。现成数组:`scratch/t15/out/_miss.npy`、`t49_duni_missing.npy`、`person_duni_all.npy`、`person_uid_all.npy`(numpy 可读;若口径不清,读 `scratch/t15/out/more.json` 与 t15c 汇总核对,不要凭空重定义)。

## 子任务 A(最高优先):people_db.dat 全文法走查

1. 复用 probe3 的 compact 文法从 pos 6 继续走,**走到文法断裂为止**;记录断裂 offset、前后 64B hexdump、已走行数。
2. 断裂处尝试识别下一段文法(可能换 type/换宽度/换段头);每识别一种新文法就继续走。目标:判定"658,011 条完整 person 库"假设成立与否——key/duni 覆盖率、与 basic_people 的 key 空间关系(重叠?互补?超集?)。
3. 400MB 全走可能慢:用流式读 + 每 10 万行 checkpoint 落盘;走不完就交 partial(已走覆盖率 + 文法清单 + 断裂日志),**不许空转**。
4. 交付 `scratch/t26/out/people_walk.json` + `people_walk.md`:文法变体表、行数/key/duni 统计、断裂点清单、假设裁决(支持/反对/证据不足)。

## 子任务 B:165,461 未命中引用 × non_pl_hist_id 交叉

1. 解 `non_pl_hist_id.dat` 与 `pl_hist_id.dat` 的 u32 数组(去壳后),报长度、值域、排序性、重复率。
2. 把 `_miss.npy` / `t49_duni_missing.npy` 的未命中集分别与两个 ID 数组求交:命中率多少?是否解释 165,461?注意区分 duni 空间与行号空间——先核对数组语义再求交,口径写清楚。
3. 交付 `scratch/t26/out/hit_cross.json` + `.md`:命中率、残差、结论(悬案关闭/部分解释/负结果)。

## 子任务 C:non_pl_hist_dt.dat 表层拆包

1. tadc v3 串联 zstd 逐成员解压(复用 t15b 手法),列出成员数、各自解压尺寸。
2. 每成员头部 census:前 64B hex、u32 候选(行数/尺寸样)、可见 ASCII 标签;**不做深文法**。
3. 交付 `scratch/t26/out/hist_dt_census.json` + `.md`。

## 子任务 D(小件,最后做):summary.dat + lang_update_db.dat

1. summary.dat:按 tad. v3569 自有文法列成员/段清单 + 头部 census。
2. lang_update_db.dat:列内嵌 fmf. 目录成员清单(名字+尺寸),抽 1 个成员确认是否语言文本。
3. 交付 `scratch/t26/out/small_census.json` + `.md`。

## 纪律

- 只读 `scratch/data/` 与仓内证据;只写 `scratch/t26/out/` 与 `scratch/t26/*.py`;不碰 exe、不联网、不启动任何程序。
- 每个子任务一个 status 字段(`complete_*`/`partial_*`/`negative_*`);顶层 `scratch/t26/out/status.json` 汇总四子任务状态——**即使只完成 A 也要写顶层 status**。
- 新脚本 `--help`/`--selftest`,退出码 0/1/2;候选不写成结论;负结果保留。
- 完成后打印交付清单:每个子任务拿到什么、卡在哪。