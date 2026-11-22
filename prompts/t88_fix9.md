# t88-fix9 — 数据侧终局:per-rec_type tag 序列→117 码 wire 映射(纯向量化,禁碰 exe)

你是受指挥官委派的子代理,**全新会话**。E137 指挥官终判已冻结,**禁碰 exe、禁 4CC 猎寻**:

- 4CC 码在两个 exe 中零存在;club 记录族读取=(rec_type, tag 序号) 位置路由
- u8@4=rec_type(37 值);**fix5 `scratch/t88/out3/recget_tagmap.json` 的 8 组(apps/cash/cnst/endt/fsgt/gams/info/otht)即静态 tag→字段映射**
- 冻结三列(E132):u32@0=club-uid、u32@5=person-uid、identity uid=行自键
- 行框(out2/row_frame.json):pre 37B + [u32 len][utf8 name]@37 + tail 26B + identity 13B@row_end-13
- `scratch/t88/out3/slots.json`:117 码(34 已 L3、83 待映射)

## 任务(纯数据侧;全部写 `scratch/t88/out3/` 新文件;每步落盘)

1. **10 分钟内**:写 `out3/tag_wire.json` 骨架
2. **行体 tag 序列逆向**(核心):取 rec_type 8(3,391 行,样本足)若干行,从 name 尾到 identity 头解析 body:试 [u8 tag][len][value] / [u16 tag]... 等文法;与 recget_tagmap 的字段组对齐——tag 序号即字段序,每 rec_type 一张 tag→offset 表。产出 `out3/tag_layout_{rt}.json`(每 rec_type 一文件或并档)
3. **117 码映射**:tagmap 8 组的码集 ∪ slots.json 的 117 码,逐码给 (rec_type 组, tag 序号, wire_off, width, grade=L2 数据侧);tail_cols/tail_prof/tail_sig(fix6 产物)交叉验证;`0xffffffff`/合法 0 分列;wrong-club 控制(@0 非成员行)同报
4. `out3/verify.py`(独立,≥6 项:闭包不变式 13+Σbody+12×N+9=载荷、tag 文法覆盖率≥95%、抽样值域、三列不变式、117 覆盖、wrong-club)+ 更新 `REPORT.md` + `DONE.md`(complete/partial)
5. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 out3/ 新文件与 `scripts/t88_*.py`;**editor.exe/fm.exe 本棒一律不读**(已无需);不碰 reports/、LEDGER、scratch/cmd/
2. 每完成一个 rec_type 立即落盘;>20KB 不进会话;print ≤30 行;单次写 ≤120 行
3. 文法 2 轮试不出→该 rec_type 标 held+首反例跳下一个;候选不写成结论;时间不够→partial DONE 列剩余
4. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`;zstd vendored `D:/tmp2b/fm24/tools/python`

## 交付 scratch/t88/out3/

`tag_wire.json`、`tag_layout_*.json`、`slots.json`(更新)、`verify.py`、`REPORT.md`(更新)、`DONE.md`。
