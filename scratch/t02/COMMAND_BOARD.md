# t02 指挥台账(2026-11-18 16:05 发射)

## 架构

星型:指挥官(我,串行独占分诊/抽验/入账)+ 4 执行者(并行,只写各自 outbox)。
四渠道认证 16:04 全部 `ready`。发射器 `scripts/launch.sh`(后台长跑 + 断流重试 + 增量落盘判成功)。

## 在跑的四路任务

| 任务 | 渠道 | 目标 | outbox | 日志 | 预算 |
|---|---|---|---|---|---|
| t02c-club | gpt-6-luna(稳定) | ~~club 变体段~~ ✅ **框架全解入账 E33**(84,259 行封口;字段 L3=0 未做) | `inbox/club_v2/` | `pi-logs/t02c-club.log` | 实耗 20min(冗余轮已 kill) |
| t02p-pw | gpt-6.2-sol(最强,额度少) | ~~BASIC_PERSON W 选择器~~ ✅ **已交付入账 E32** | `inbox/pw/` | `pi-logs/t02p-pw.log` | 实耗 23min |
| t02f-b3 | devseek(便宜,断流) | ~~t7/t9/t22 批量框架~~ ⚠️ **2/3 入账 E33**(fw7/fw22 ✓,fw9 仍骨架) | `inbox/batch3/` | `pi-logs/t02f-b3.log` | 2 轮超时 |
| t02g-nati | logfare→**转派 luna** | logfare 5 次限流失败(负结果入 E33)→ luna 接手在跑 | `inbox/nati/` | `pi-logs/t02g{,-natir}.log` | t02g2 2×25min |

发射时间 16:05:39,四进程已确认在跑(ps 可见)。任务书在 `prompts/t02{c,p,f,g}_*.md`。

## 为什么这样分(调度决策)

- **luna 接 club**:稳定长任务,club 是唯一半解的高价值表(433 字段,82.7% 已验),续解边际收益最高。
- **sol 接 person**:额度少→只打最高价值卡点。person 家族 271 字段全卡在 W 选择器;t01-k 因 L4=0 停在 1 字段,本任务放宽为静态溯源(追全局字节写入点 + 数据侧反推),允许负结果。
- **devseek 接批量框架**:断流 2-14min,只配"每张表 5 分钟、先落盘骨架"的极小任务,断流重跑无损。t7/t9/t22 都是 client 未解、模式已知。
- **logfare 接 nati**:1M 上下文适合长推导;曾限流,故只给单表且允许负结果,失败退回指挥官手解。

## 验收记录

- **调度轮全部收口 → E33 已入账(16:4x)**:
  - club(luna):84,259/84,259 行全走通、footer 0x69c66a 精确封口;solve.py --selftest 独立复跑 PASS;**推翻旧"4B 变体"结论**(实为 84,256 标准+3 特殊空记录)。字段级 L3=0,诚实标注未闭合。
  - devseek:fw7(208 变长)/fw22(449×13)complete,旧库 header 独立核对一致;fw9 超时仅骨架(2/3)。
  - logfare:5 次全 throttling 限流负结果;落盘 nati payload bin(SHA 与 E21 吻合),已转派 luna。
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
