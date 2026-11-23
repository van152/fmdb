# t88-fix8 — PE 寻址基建先行:复核 E121 cmp 位点 + CBW 族真路由(指挥官更正后重定位)

你是受指挥官委派的子代理,**全新会话**。E136 指挥官更正两笔必须先消化:

1. **fix6 的负结果存疑**:slots.json 里 CBW*/CBD* 族的 held 理由「4CC 字节缺席」与 **E121 矛盾**——`scratch/t82/out/xref_extra3.json` 的 `negative_proof_starting_record` 明确记录:**CBDa cmp @0x11f0ca7、CBWa cmp @0x11f0cb6 → hub 0x11f2a76 → 0x11e8af0 → TC_RECORD_GET(0x3ebad50)**,且全局表 `DATABASE_TABLE<STARTING_RECORD>*` 在 VA 0x141b60190(type 0x2d=45)
2. **t89_disasm 的节表硬编码不覆盖全部区**(0x3ebad50 报"不在已收录节内"),且 fo↔VA 换算曾把指挥官引到函数桩区——**第一步必须从 exe 真 PE 头解析节表**(只读 `D:/tmp2b/fm24/input/editor.exe`,SHA b82ebe8e...),建立全节 fo↔VA 映射并落盘 `out3/pe_sections.json`,后续一切寻址走它

## 任务(顺序;每步落盘;全部写 `scratch/t88/out3/` 新文件)

1. **10 分钟内**:真 PE 头解析 → `out3/pe_sections.json`(全部节的 name/rva/fo/size)+ 用它把 0x11f0ca7/0x11f0cb6/0x3ebad50/0x1543ca0/0x141b60190 五个地址全部换算落盘(fixed_addresses.json 可并入)
2. **复核 cmp 位点**:换算正确后反汇编 0x11f0ca7 前后窗口,确认 `cmp` 立即数(试 0x61444243=CBDa LE / 0x61426243=CBWa LE 等 4 种字节序),抄录 case 体(读哪个 [reg+X])
3. **CBW 族真路由**:从 cmp case → hub 0x11f2a76 → 0x11e8af0 → TC_RECORD_GET,解出该族 rec_type 与 reader_off;更新 `out3/slots.json` 的 80 条 held(CBW 族逐码更新,其余保持)
4. **verify.py**(独立,≥6 项:PE 节表自洽、五地址换算、CBDa/CBWa cmp 字节、抽样值域、E132 三列不变式、117 覆盖)+ 更新 `REPORT.md` + `DONE.md`(complete/partial)
5. `scripts/t01_anchors.py`(7/7)

## 避坑纪律

1. 只写 out3/ 新文件与 `scripts/t88_*.py`;**exe 只读**;不碰 reports/、LEDGER、scratch/cmd/、scratch/t82/
2. 每步立即落盘;>20KB 不进会话;print ≤30 行;单次写 ≤120 行
3. PE 解析用 stdlib(struct)即可,勿引第三方;反汇编可用 vendored capstone(`D:/tmp2b/fm24/tools/python`,t89_disasm.py 可读参考但**新建自己的** scripts/t88_*.py 入口,以真 PE 头为准)
4. 两轮定不出→held+首反例;候选不写成结论;时间不够→partial DONE
5. `py -V:3.12 -I -B`;`FM24_DB_DIR=D:/tmp2b/fm24-db/scratch/data`

## 交付 scratch/t88/out3/

`pe_sections.json`、`slots.json`(更新)、`verify.py`、`REPORT.md`(更新)、`DONE.md`。
