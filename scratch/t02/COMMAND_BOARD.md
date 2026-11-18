# t02 指挥台账(2026-11-18 16:05 发射)

## 架构

星型:指挥官(我,串行独占分诊/抽验/入账)+ 4 执行者(并行,只写各自 outbox)。
四渠道认证 16:04 全部 `ready`。发射器 `scripts/launch.sh`(后台长跑 + 断流重试 + 增量落盘判成功)。

## 在跑的四路任务

| 任务 | 渠道 | 目标 | outbox | 日志 | 预算 |
|---|---|---|---|---|---|
| t02c-club | gpt-6-luna(稳定) | club 第 69,705→84,259 行变体段 + ≥10 字段 | `inbox/club_v2/` | `pi-logs/t02c-club.log` | 3×25min |
| t02p-pw | gpt-6.2-sol(最强,额度少) | BASIC_PERSON W 选择器静态溯源(全项目最大卡点) | `inbox/pw/` | `pi-logs/t02p-pw.log` | 2×25min |
| t02f-b3 | devseek(便宜,断流) | t7/t9/t22 三张 client 表行框架 | `inbox/batch3/` | `pi-logs/t02f-b3.log` | 6×15min |
| t02g-nati | logfare(1M,曾限流) | nati(t10)变长行边界 + 251 行封口 | `inbox/nati/` | `pi-logs/nati.log` | 5×15min |

发射时间 16:05:39,四进程已确认在跑(ps 可见)。任务书在 `prompts/t02{c,p,f,g}_*.md`。

## 为什么这样分(调度决策)

- **luna 接 club**:稳定长任务,club 是唯一半解的高价值表(433 字段,82.7% 已验),续解边际收益最高。
- **sol 接 person**:额度少→只打最高价值卡点。person 家族 271 字段全卡在 W 选择器;t01-k 因 L4=0 停在 1 字段,本任务放宽为静态溯源(追全局字节写入点 + 数据侧反推),允许负结果。
- **devseek 接批量框架**:断流 2-14min,只配"每张表 5 分钟、先落盘骨架"的极小任务,断流重跑无损。t7/t9/t22 都是 client 未解、模式已知。
- **logfare 接 nati**:1M 上下文适合长推导;曾限流,故只给单表且允许负结果,失败退回指挥官手解。

## 验收队列(按到达顺序,指挥官独占)

每个产物到齐后执行:
1. safety-scan(只读声明、无目录外写入)
2. 模型自检对照(不单信)
3. **指挥官独立抽验**:closure 等式 + 身份块抽样 + file offset 字节级(参考 `scripts/t01m_spotcheck.py` 范式)
4. 锚点回归 `py -V:3.12 -I scripts/t01_anchors.py`(7/7)
5. 入账 LEDGER(E31 起,只追加)+ 更新本台账 + git 提交

## 账本 debt(已知,待补)

- LEDGER.json 停在 E30(11:45);之后已验收入账的 9 张表(regi/curr/city/stgn/inju/lang/drbr/awar/cont)+ fw24 部分,只散在 git commit message 里,**尚未写进 LEDGER**。
- 处理:等四路产物到齐后,一次性补 E31(汇总 t02 已完成 9 表 + 本次四路结果),避免账本与 HEAD 脱节。

## 不变约束

只读游戏库与旧仓;L4=0(不启动程序);claim 带字节证据;负结果保留;候选不写成结论;LEDGER 只追加;sol 额度已耗 2 次(本项目累计),再用需用户批准。
