# t01 交接文档(指挥官 GLM 额度 2026-11-18 09:00 过期,给下一班)

## 30 秒上手

```powershell
cd D:\tmp2b\fm24-db
py -V:3.12 -I scripts/t01_anchors.py     # 7/7 PASS = 仓库事实未被破坏
git log --oneline | head -12             # 全部进度已提交(t01-exe-slot-map 分支)
```

然后读 `scratch/t01/MORNING_REPORT.md`(结论)+ `scratch/t01/LEDGER.json`(E1-E15 证据)。

## 不受额度影响、正在跑的东西(pi = 用户账号侧进程)

| 进程 | 看护方式 | 产出位置 |
|---|---|---|
| t01k(luna max,BASIC_PERSON ≥10 字段行偏移 = 第二实体验收线) | `scratch/t01/pi-logs/t01k.log` | `inbox/t01k/` |

验收判据:任一类(83B/34B)≥10 字段行偏移 L3 + 5 行抽验 → E26;协议 = safety-scan → 自检 → 指挥官独立字节抽验(参考 `scripts/t01j_dat_spotcheck.py` 可直接复用其行走查)→ 锚点 7/7 → 账本 → 提交。

**不需要任何人守着;产物落盘即完成。** gpt-6.2-sol 探测状态(2026-11-18 02:0x):账号侧尚不支持("not supported when using Codex with a ChatGPT account"),守哨会自动重试至上线,共 40 次/10 小时。

## 受额度影响、会在 09:00 终止的

- glm53 后台子代理(t01-e 虚表枚举):若 09:00 前完成,产物在 `scratch/t01/t01e_vtables.json` + `t01e_REPORT.md`;若中途死掉,半成品 JSON 仍可读——**验收协议:抽 3 张虚表手工核对 slot6 字节(参考 E11 锚点 0x187d2b0 slot6=0x140ebfa40),通过则记 E16**。

## 下一班的验收队列(按到达顺序)

1. **t01-e**(若已产出):对照 E11 锚点抽验 → E17 已入账(12/32 实体映射,H3 半证实) → 若 H3 成立,把"实体↔注册函数全映射"与 `property_map.json`(table_type↔entity)合流,输出三向表 `table_type ↔ entity ↔ registration_fn`(阶段二核心工件)
2. **luna r2**:验收点 = 槽成员是否给出 +0 vtable 之外的新成员(带字节证据)、类型标签清单('cont' 之外)→ E17
3. ~~t01f(sol 杀手锏)~~ **已验收(E20,2026-11-18 04:35)**:18 字段行偏移 + 序列化器方法论 + 3 项修正(helperB 非墙 / slot 计数勘误 / rdui=行序号);指挥官四路独立验收全过;sol 额度已耗 1 次,默认不再用
4. 用户上轮留下的决策:阶段一验收线"≥10 字段行偏移 L3"是否分两档

## 交接后的优先级

1. .dat 行偏移之桥(若 t01f 未解决):luna r2 的类型标签 ↔ `evidence/fm24/reports/editor_gen/replicate/codec_tables.json`(420 条)对齐
2. comp 槽位清单推进验收线
3. 阶段二:50 张 unknown 表实体映射(依赖 t01-e/t01f 产物)

## 硬约束提醒(不变)

只读游戏数据与 `D:\tmp2b\fm24` 旧仓;候选不写成结论;负结果保留;claim 带字节证据;新任务书进 `prompts/`;所有结论进 LEDGER(只追加)。

## 状态更新(2026-11-18 06:4x,夜班封盘终版)

- **E20-E25 全部入账**(E25 = person 行仓库框架解码:basic_people_db.dat 658,011 条类变长记录全量封口),HEAD 见 git log;详见 [MORNING_REPORT.md](MORNING_REPORT.md) v5
- t01e 的 nati 标签已按 E23 COL 字节勘误(NATIONAL_TEAM_CONTAINER/TEAM_CONTAINER,均非 NATION)
- t01k(BASIC_PERSON 字段映射)运行中,验收判据见上表
- stage-2 排序就绪:pers(框架已就绪)→ club(433,mixed 前缀先行)→ weat(94)/stad(60)(直线);变长型先恢复行边界
