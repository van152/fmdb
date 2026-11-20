# t17c 任务书:全量回归套件(独立前置,不等台账)

先读 [AGENTS.md](../AGENTS.md)。这是今晚所有产物的总验收,独立于 t16 引擎状态。

## 一句话目标

把仓库全部历史锚点 + 今晚新增锚点跑成一次机器回归,`regression.json` 逐项 pass/fail,**失败项原文保留**——这是晨裁的底座。

## 回归清单(一项不漏)

**A. 历史锚点(L2/L3)**
1. 六大洲 0..5(comp 表)、England=139 / China PR=55、parent row 352
2. E51 city 坐标 100% 复现(工具链:`scripts/fm24_dump.py --archive client --table 2`,FM24_DB_DIR 已设)
3. E27 weather 334 行封口:payload 43,345B、行跨度 = 112 + name_len、33 种跨度(工件 `scratch/t01/inbox/t01l/output.json` 有 E27 的 89 字段基线,先读它)
4. E20 comp 行偏移 18 个 L3(工件 `scratch/t01/inbox/t01f/output.json`)
5. E25/E32 basic_people_db 658,011 双重封口;class 分布 166064/476158/4757/9839/1193

**B. t13 A 类锚(exe 反汇编)**
6. 12→award AHp1 `[rdi+0x80]`、33→club CMWE `[rbx+0x44]`、45/48→person gols `[rdi+0x56]`(工件 `scratch/t13/out/verify.py` 可直接复跑;**复跑并把它的 PASS 原文贴进你的 regression**)

**C. t14 RTTI D 锚**
7. `scratch/t14/out/verify.py` 复跑(74/74、67 链、fm.exe 67/67、8 实体零矛盾)——原文入档
8. 抽 5 条 D 链(0/2/27/26/38)自己独立重解码一遍:跳表 rel32 → handler → vtable → COL → TD 字符串

**D. t15 C 类佐证**
9. t30 @4 值域 0..114 distinct 115;t38 @0 全表 <658,011;t49 @4 distinct 279,109 ∩ person duni 213,513(工件 `scratch/t15/out/fk.json`;抽样复算其中数字,数据在本地 FM24_DB_DIR)

**E. t15c people_diff**
10. 165,461 − 31,323 = 134,138 数字链复算

## 纪律

- 只写 `scratch/t17/out/`;py -V:3.12 -I;脚本 --help/--selftest,退出码 0/1/2。
- 任何 fail:**原文保留 + 不要试图修**——你是验收员不是维修工。
- 输出预算:单次写盘 ≤400 行;regression.json 超 50KB 就分项拆文件。
- 35 分钟做不完就落盘 partial。

## 交付(scratch/t17/out/)

1. `regression.json` —— `[{"id":"A3","claim":"...","method":"...","result":"pass|fail","actual":"...","source":"..."}]`,顶层 `{"status":"complete_regression"}`(哪怕有 fail 也算 complete——诚实报告即完成)
2. `REPORT.md` —— 一页纸:通过率、fail 清单、晨裁建议
