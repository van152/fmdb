# t15e 任务书:t15d 抽查收尾(现场已有半成品)

先读 [AGENTS.md](../AGENTS.md)。t15d 两轮都倒在最终汇总,但数据在 `scratch/t15d/out/`(fk_hits.json、measure.json、prof/、grid/、idset/、clubwords.npy 等)。你只做汇总,不重跑。

## 任务

1. 读 `scratch/t15d/out/` 现有 json/目录,按 t15d 原判据(prompts/t15d_dspot.md:类名语义 ↔ ID 空间/金额/日期列,给 `plausible | implausible | silent`)汇总:
   - `scratch/t15d/out/dspot.json`:逐表 `{"table_type","rtti_class","verdict","evidence"}` + 顶层 `{"status":"complete_spot_check"}`(部分表数据缺失就标 silent)
   - `scratch/t15d/out/dspot.md`:人读表
2. 原判据参照对象:person 658,011 / club 84,259 / team 84,507 / comp 7,047 / injury 115。
3. 缺哪张表的数据就标 `silent` + "缺 dump",不许重跑补数据。

## 纪律

只写上述两个文件;10 分钟;输出预算单次 ≤300 行;`py -V:3.12 -I`。
