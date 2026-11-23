DONE type=t112

- Deliverable: `scripts/t112_fm24_reader.py` — FM24 `.dat` 纯 Python（stdlib + vendored zstandard）高速只读多表解析库；`scratch/t112/out/reader_verify.json`、`REPORT.md`、本文件。
- 支持 66 张表（fixed 46 + variable 18 + empty 2；server 49 + client 17），全量解码 1,942,341 行 6.4s，**66/66 `footer_closed == true`（0 字节误差）**，0 失败；13 张跳过（诚实原因记录在 verify JSON）。
- 验收：`py -V:3.12 -I -B scripts/t112_fm24_reader.py --selftest` 退出 0（12 项 PASS）；`--verify-all` 退出 0；≥25 张表要求超额达成（66 张）。
- 输入只读消费：scratch/data/{server,client}_db.dat、scratch/t96c/out/wire_traces_master.json、scratch/t110/out/master_67tables_l3.json（1,036 条 L3 映射 → 全库 390 个命名列）、scratch/t95/funcs/*.c；未修改 reports/ 与 LEDGER.json。
- 覆盖提示书点名表：CONTINENT/INJURY/MEDIA_SOURCE/LANGUAGE/NATION★/REGION/STADIUM_CHANGE/STAGE_NAME/WEATHER/PLAYER_TYPE/CURRENCY_RECORD/AGREEMENT/CITY/STADIUM/STARTING_RECORD★(84,477 行 + 5,210 行)/COMP(client)★ 及 29~73 中除 29/32/36/71/72 外的全部子表。
- t10 NATION 加分项达成：slot19 C (1410404C0) 手写 server/client 两套程序；三个缺 .c 的元素解析器（1415CFD70/141072F60/1415CFEA0）用「全表字节记账 + identity 序号锚定」穷举实证求解（CFD70=[u8,str,str,7×u32] 含人名、72F60=14B、CFEA0=7×u32=28B），两库各 251 行 100% 闭合；DATE 线格式确证 [day-of-year u16][year u16]。
- 过程工具：scratch/t112/{solve_t10.py, trace_funcs.py, extract_prog.py, ctrees/}。
