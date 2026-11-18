# t02 指挥台账(2026-11-18 16:05 发射)

## 架构

星型:指挥官(我,串行独占分诊/抽验/入账)+ 4 执行者(并行,只写各自 outbox)。
四渠道认证 16:04 全部 `ready`。发射器 `scripts/launch.sh`(后台长跑 + 断流重试 + 增量落盘判成功)。

## 在跑的四路任务

| 任务 | 渠道 | 目标 | outbox | 日志 | 预算 |
|---|---|---|---|---|---|
| t02c-club | gpt-6-luna(稳定) | club 第 69,705→84,259 行变体段 + ≥10 字段 | `inbox/club_v2/` | `pi-logs/t02c-club.log` | 3×25min |
| t02p-pw | gpt-6.2-sol(最强,额度少) | ~~BASIC_PERSON W 选择器静态溯源~~ ✅ **已交付入账 E32** | `inbox/pw/` | `pi-logs/t02p-pw.log` | ~~2×25min~~ 实耗 23min |
| t02f-b3 | devseek(便宜,断流) | t7/t9/t22 三张 client 表行框架 | `inbox/batch3/` | `pi-logs/t02f-b3.log` | 6×15min |
| t02g-nati | logfare(1M,曾限流) | nati(t10)变长行边界 + 251 行封口 | `inbox/nati/` | `pi-logs/nati.log` | 5×15min |

发射时间 16:05:39,四进程已确认在跑(ps 可见)。任务书在 `prompts/t02{c,p,f,g}_*.md`。

## 为什么这样分(调度决策)

- **luna 接 club**:稳定长任务,club 是唯一半解的高价值表(433 字段,82.7% 已验),续解边际收益最高。
- **sol 接 person**:额度少→只打最高价值卡点。person 家族 271 字段全卡在 W 选择器;t01-k 因 L4=0 停在 1 字段,本任务放宽为静态溯源(追全局字节写入点 + 数据侧反推),允许负结果。
- **devseek 接批量框架**:断流 2-14min,只配"每张表 5 分钟、先落盘骨架"的极小任务,断流重跑无损。t7/t9/t22 都是 client 未解、模式已知。
- **logfare 接 nati**:1M 上下文适合长推导;曾限流,故只给单表且允许负结果,失败退回指挥官手解。

## 验收记录

- **t02f-b3(devseek)fw7/fw22 部分验收(16:3x,待 fw9)**:旧库 reader 独立核对 header_count/size 与 devseek 完全一致(T7=208/36824、T22=449/5859),closure 算术自洽、identity 全量(T22 449/449、T7 208/208)。待 fw9 落盘后一并入 LEDGER E33。fw9 旧库 header_count=251,devseek 仍在解。
- **t02p-pw(sol)→ E32 已入账(16:3x)**:后台 exit 1 是**发射器判据 bug**,非模型失败——sol 首轮即交付 W=8 + 15 字段,但把 status 写成 `complete_file_layout_runtime_selector_open`(带限定词的诚实标注),launch.sh 只认精确 `complete/partial` 故误判。已修判据(放宽为 `complete*|partial*` + ≥2 实质文件)。指挥官独立验收:字节 11/11、658,011 行独立走查全封口、锚点 7/7。

## 验收队列(按到达顺序,指挥官独占)

每个产物到齐后执行:
1. safety-scan(只读声明、无目录外写入)
2. 模型自检对照(不单信)
3. **指挥官独立抽验**:closure 等式 + 身份块抽样 + file offset 字节级(参考 `scripts/t01m_spotcheck.py` 范式)
4. 锚点回归 `py -V:3.12 -I scripts/t01_anchors.py`(7/7)
5. 入账 LEDGER(E31 起,只追加)+ 更新本台账 + git 提交

## 账本 debt(已清零 16:12)

- ~~LEDGER.json 停在 E30(11:45),9 张表未入账~~ → **E31 已补(commit 92b0f1a)**:regi/curr/city/stgn/inju/lang/drbr/awar/cont 共 68 字段/行框架汇总入账,LEDGER 与 HEAD 对齐(31 条)。
- 本次四路结果到齐后另记 E32+。

## 不变约束

只读游戏库与旧仓;L4=0(不启动程序);claim 带字节证据;负结果保留;候选不写成结论;LEDGER 只追加;sol 额度已耗 2 次(本项目累计),再用需用户批准。
