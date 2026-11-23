# t88-fix7 — tag 表路由解析 + reader→wire 派生 + verify(E135 收尾棒)

你是受指挥官委派的子代理,**全新会话**。前棒已把 117 码分两类(E135 冻结,禁重做):

- **34 L3**:4CC/rt 链已锚(rec_type + reader_off + exe 三件套,见 `scratch/t88/out3/slots.json`)
- **83 held(CBW*/CBD* 主族)**:**4CC 字节在 exe 分发缺席,走 tag 表(lea 地址引用)路由**——原 t88 台账 `scratch/t88/TC_GET2_4cc.json` 的 lea 组(CBDa/CBwa/CFGd/CGMc/CHAa/CHSa/CLAa/COPc/COSc/CYPc/CYSc...)即证据

## 任务(≤1 attempt 装配量;每步落盘;全部写 `scratch/t88/out3/` 新文件)

1. **10 分钟内**:写 `out3/tag_route.json` 骨架
2. **tag 表路由解析**(核心):TC_GET2 的 lea 引用表(数据区,非 cmp 立即数)→ 找表结构(表基 VA、条目宽度、tag 索引如何进);对 CBW*/CBD* 族:码在表中位置 → 内层 tag/序号 → case 体读 [rec+X] → reader_off。`scratch/t88/out3/recget_tagmap.json` 的 tag 组(apps/cash/cnst/endt/fsgt/gams/info/otht)与 `record_get_tagmap.json` 可交叉。产出并入 `out3/slots.json`(更新 83 held 条目:tag_route 字段)
3. **reader→wire 派生**:对 34 L3:reader_off 是 C++ 结构偏移,用行框(pre 37B 固定区+name 变长+tail)推 wire 位置;**数据侧核验**:抽该 rec_type 行核对值域;已锚 3 列不变式(club@0/person@5/type@4)作对照
4. `out3/verify.py`(独立重抽,≥6 项:117 覆盖、34 L3 抽样值域、tag 表结构自洽、E132 三列不变式、行框不变式、wrong-club 控制)+ 更新 `out3/REPORT.md` + `DONE.md`(complete 或 partial)
5. `scripts/t01_anchors.py`(7/7)

## 避坑纪律(同前棒)

1. 只写 out3/ 新文件与 scripts/t88_*.py;不修改既有文件;不碰 reports/、LEDGER、scratch/cmd/
2. 每完成一码组立即覆写 slots.json;>20KB 不进会话;print ≤30 行;单次写 ≤120 行
3. 两轮定不出→held+首反例,跳下一个;候选不写成结论;时间不够→partial DONE 列剩余
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored;editor.exe 只读(SHA b82ebe8e...)

## 交付 scratch/t88/out3/

`tag_route.json`、`slots.json`(更新)、`verify.py`、`REPORT.md`(更新)、`DONE.md`。
