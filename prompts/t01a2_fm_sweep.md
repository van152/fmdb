# t01-a2 任务书:fm.exe 4CC 注册块/比较式扫描

> 机械扫描任务,纯 Python,只读输入,产物写 `<WORKSPACE>\scratch\t01\inbox\t01a2\`。
> Python 固定 `py -V:3.12 -I`。不 pip install,不启动任何程序,不 git commit。

## 背景(自包含)

FM24 编辑器(editor.exe)里已确认存在字段码体系:字段码是 4 字符 ASCII(如 `ccti`),在代码里以 4 字节立即数出现,字节序为 ASCII **反序**('cnam' 存为 6d 61 6e 63)。editor.exe 的形态:
- mov-imm 注册块:`c7 45 f0 <imm32反序4CC>`,每 0x30 一块,`48 83 c0 38` 步进(实体属性注册)
- cmp 式分发:`81 fe <imm32大端>` + `0f 84`(XML→对象字段 switch)

已知中途结论(前一轮代理,需你复核):**fm.exe 里存在 editor 的字段码,但不成 4096B 密簇**——所以本次要做分布/密度分析,不要假设与 editor.exe 同构。

## 对象

`<OLD_REPO>\input\fm.exe`(只读;先报告文件大小)

## 任务

1. 全文件扫描:
   - mov-imm 式:`c7 45 <disp8> <imm32>`、`c7 44 24 <disp8> <imm32>`、`c7 85 <disp32> <imm32>`,imm 反序后 [A-Za-z0-9]{4}
   - cmp 式:`81 f8`..`81 ff <imm32>`、`81 fa <imm32>`、`3d <imm32>`、`81 fe <imm32>`
2. 锚点自检:editor 的 comp 序列 cnam/cnsm/cl3n/cnti/ccti/cpcm/crep/cext/PLgn/dbty 在 fm.exe 的命中数与样本偏移(每码前 10 个)
3. 密度剖面:1MB 窗口统计 imm-4CC 命中,top20 窗口;判断 fm.exe 是"散布全文件"还是"集中在若干区域"
4. 聚类:相邻 <4096B 归簇,保留 4CC≥3 的簇;每簇记录 mov-imm vs cmp 构成比
5. 实体匹配:读 `<WORKSPACE>\evidence\fm24\reports\editor_schema\master.json` 的 `entity_summary` codes,Jaccard top3;注意 fm.exe 可能按功能模块组织(而非按实体),如实报告
6. 与 editor.exe 对比结论:同体系?同布局?哪些实体码在 fm.exe 缺席(重要负结果)?

## 交付(写到 inbox/t01a2/)

- `fm_sweep.json`:`{meta:{exe,size,forms}, anchor_check:{...}, density_top20:[{window_off,count}], clusters:[{start,end,forms:{mov:n,cmp:n},cc_list[:50]}], entity_match:{...}, editor_compare:{...}}`
- `REPORT.md` ≤50 行
- 脚本放 `<WORKSPACE>\scripts\t01a2_fm_sweep.py`(可复跑,有 --help)

## 验收

- 脚本可复跑;JSON 可 json.load;随机抽 3 个 offset 可在 fm.exe 字节复现
- 大文件注意内存(mmap/分块);offsets 每码只留前 10 个
