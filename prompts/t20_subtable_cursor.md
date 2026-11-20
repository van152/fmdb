# t20 任务书:club 子表 cursor 重建(t22 等小表)—— 收官补刀

先读 [AGENTS.md](../AGENTS.md)。t19 已证明 club 主行是 `50 + N + M` 名字优先框架(672 字段放不下主行,E39/E40 的"二级派发+子对象下沉"结论再次成立)。club 的业务字段在**子表**里。本任务拿最小、证据最全的子表开刀。

## 主目标:t22(club 球场/迁建属性集,449 行,定长 stride=79)

- 证据链最全的子表:E56 A 级(df=1 唯一码)裁定 club 属性;`scratch/t13d/out/t22.csv` 全量 449 行已有;`scratch/t15/out/fk.json` 有 c0 362 值 ⊂ club ID 域 [86,82403] 的旁证。
- 方法(照抄 t18/t19 已验证的):factory 跳表 t22 块是 callee 构造 → 深追找到序列化器 → 按 cursor 步骤累加宽度 → 与 stride 79 封口 → codes_full.json 里 club 4CC 的 object_off 实例互验 → 行坐标字段台账。
- t13d audit 已给的列画像可直接用(col0 distinct 311 min 86、col3/col4 值 ~131-133M 像打包日期等)。

## 次目标(时间允许才做,按序):t64(club staff job status,6,946 行)、t66(club transfer preference,753 行)

## 纪律

- 只写 `scratch/t20/out/` + 新增 `scripts/t20_*.py`;其他只读;不联网;FM24_DB_DIR 已设。
- 结构优先于命名;unnamed 合法;stride 封口是硬门。
- 输出预算单次 ≤400 行;40 分钟做不完落盘 partial。
- status:`complete_cursor_<限定词>` / `partial_<限定词>`。

## 交付(scratch/t20/out/)

1. `cursor_t22.json` —— 序列化器定位 + 步骤序列 + stride 封口
2. `fields_t22.json` —— 行坐标字段台账(449 行表的字段不多,应当能命名过半;做不到就如实)
3. `verify.py`(--help/--selftest)+ `REPORT.md`
