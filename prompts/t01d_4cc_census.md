# t01-d 任务书:editor.exe 4CC 普查(deepseek 渠道 2)

> 机械扫描任务,纯 Python,只读输入,产物写 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01d\`。
> Python 固定 `py -V:3.12 -I`。不 pip install,不启动任何程序。

## 背景
editor.exe(`D:\tmp2b\fm24\input\editor.exe`,74,807,296 B)里字段码以 4 字节立即数出现,字节序是 ASCII **反序**(字段码 'cnam' 在指令里是 6d 61 6e 63)。已知一个样本:mov-imm 注册块 `c7 45 f0 6d 61 6e 63`(@0xebf093)。另一代理在做注册块的深度解码,你做**全量普查**——哪些字段码以哪种指令形态出现在哪里。两层互补,不要做块解码。

## 任务
1. 全文件扫描以下指令形态,提取 imm32 并**反序**成候选字段码(字符集 [A-Za-z0-9]{4}):
   - `c7 45 <disp8> <imm32>`(mov [rbp+d8], imm)
   - `c7 44 24 <disp8> <imm32>`(mov [rsp+d8], imm)
   - `c7 85 <disp32> <imm32>`(mov [rbp+d32], imm)
   - `b8`..`bf <imm32>`(mov r32, imm)
   - `81 f8`..`ff <imm32>`、`81 fa <imm32>`、`3d <imm32>`(cmp r32, imm)
2. 统计输出:
   - 每形态命中数;每候选码的 (形态 × 次数) 矩阵
   - 与词汇表对照:读 `D:\tmp2b\fm24-db\scratch\t01\inbox\t01c\vocab.json`(若尚不存在,退回读 `D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json` 的 entity_summary codes),报告:
     a. 32 实体的字段码中,哪些在 exe 内**零命中**(这些实体可能走哈希/间接路径——重要负结果)
     b. 命中码按实体的覆盖分布(每实体命中码数/总码数)
   - 密度地图:0x100000 为窗口,每窗口 imm-4CC 命中数 top20
3. 与已知锚点自检:cnam 应在 0xebf093 命中(mov-imm 形态)、ccti 在 0xebf153;对不上说明你的形态表有错,先修再出报告。

## 交付(写到 inbox/t01d/)
- `census.json`:`{meta:{exe_size,forms}, per_form_counts:{}, per_code:{code:{form:count, offsets:[前10个]}}, entity_coverage:{entity:{hit,total,zero_hit_codes:[...]}}, density_top:[{window_off,count}]}`(offsets 全存内存会爆,每码只留前 10 个偏移+总数)
- `REPORT.md` ≤50 行:零命中实体清单、覆盖分布要点、密度热点、与锚点自检结果

## 验收
- 脚本可重跑;JSON 可 json.load;锚点自检通过;census 里每个 offset 抽 3 个能在原文件字节复现
- 注意误报:普通 ASCII 字符串不会命中(它们不是指令 imm),但字符串恰好跟在 c7 后的情况存在——报告里给出你观察到的误报率估计(抽样 20 个人工核对)
