# t15b 任务书:未覆盖档案清点 —— people_db / pl_hist / non_pl_hist / summary

先读 [AGENTS.md](../AGENTS.md)。你是旁路探路组,不依赖 t14/t16,独立交付。

## 环境变化(重要)

数据库已本地化:`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`(环境变量已设,`scripts/fm24_dump.py` 已支持)。**不许读 Z: 盘。**

## 一句话目标

主仓至今只解析了 client_db.dat(20 数值表)+ server_db.dat(59 表)+ basic_people_db.dat(BASIC_PERSON 658,011)。本地还有 5 个从未清点的档案:给你一次只读清点,判断里面有什么、值不值得开专项。

## 清点对象

| 档案 | 大小 |
|---|---|
| people_db.dat | 67.5 MB |
| pl_hist_dt.dat / pl_hist_id.dat / pl_hist_index.dat | 57.0 / 4.1 / 3.1 MB |
| non_pl_hist_dt.dat / non_pl_hist_id.dat / non_pl_hist_index.dat | 27.6 / 6.0 / 4.2 MB |
| summary.dat | 1.6 MB |
| lang_update_db.dat | 2.3 MB |

## 做法

1. 先做容器层确认:文件头是否 `tad.` 外壳(4CC `tada`/`tad.` 系列,MAGIC Zstd `28 b5 2f fd`)。容器结构判断可参考 `scratch/t01/inbox/t01k/verify.py` 与 `D:\tmp2b\fm24\scripts\modding_read_dbdat.py`(只读)。
2. 用 fm24_dump 的 runpy 链(`fm24_dump.py` 的 `_reader()`/`codec`)尝试 `list_tables(路径, 文件名)`;能列出就报表数/表型/行数。
3. 列不出就报:外壳形态、Zstd 流数、可辨识的 4CC 表名(扫前 64KB + 抽样 8 个窗口)、与已知 archive 的结构差异。
4. 对照已知基数(见 `scratch/t13e/out/baselines.json`):people_db 67.5MB 与 basic_people_db 13MB(658,011 行)是何关系?pl_hist 与 person 658,011 / t49 履历 792,149 是否对得上?
5. **只清点不解析字段**——那是后续专项的事。

## 规则

- 只写 `scratch/t15b/out/`;py -V:3.12 -I;不联网。
- 解不开就如实报"容器层都进不去",不要硬猜。
- 15 分钟做不完就落盘标 `"status":"partial"`。

## 交付(scratch/t15b/out/)

1. `probe.json` —— 逐档案:container_ok / tables(或 null)/ 关键 4CC / 与已知基数关系 / 建议(值得开专项吗)+ 顶层 status。
2. `probe.md` —— 人读版。
