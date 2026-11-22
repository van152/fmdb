# t89c — table_9 文法 + held 回填(部分交付,指挥官验收补记)

车道 t89c attempt 3 于 40 分钟墙(rc=124)被截断;发射器启发式把盘上部分产出判为 DONE。
指挥官验收:实质内容达 partial 验收线,REPORT/verify/DONE 由指挥官补写(E88 先例)。

## 已交付(全部经指挥官独立重抽验证)

### Phase 2 条目网格(实质完成)
- **载荷头部解码**:13B = `03 01 "tad." f1 0d` + **u32 record_count @+8**(client=251,server=251)——与 table_45 的 u32@+8=84,477 同构(row_frame.json 交叉印证)
- **client 闭包**:13 + 28,922 + 12×251 + 9 = 31,956 精确(tiling 行走精确到达 payload_end-9)
- **server 闭包**:13 + 304,530 + 12×251 + 9 = **307,564**(载荷实测 307,564)
- **纠错**:**E127 的 server 307,555 系 9 字节误差,真值 307,564**(本 verify V1 钉死);schema v11.2 `table9_closure_e127` 同步待 v11.3 修正
- client body 46..449(92 种长度,与 E127 held 数字对账)、server body 371..36,502(211 种)
- ordinal lane:body[12] == ordinal & 0xff,**251/251**
- sentinel head:body[0:5] = `00 ff ff ff ff`,**251/251**(row0 反例的头部字节即此)

### Phase 3 held 回填(部分完成)
- t9 get/set 分发全提取:get_entry 0x1410668f0(2,975 insns → 52 cases)、set_entry 0x141063f30
- 70 字段记录:**16 container_direct**(如 Cnti:[T9+0xc]/[T9+0x10],VA/insn 三件套)、**24 sub_reader_helper**(更深路由)、12 held_no_offset、18 未分类
- container_offsets 为**内存布局**偏移(T9 对象,data base +0x18),wire 条目偏移映射未做

### Phase 4 双档(数据已集,解释未写)
- `_dual.json`:client/server 全 profile(body 分布直方图、头/尾 hex、ordinal lane)

## 未完(如实列出)
1. helper 路由的 24 字段展开;wire 偏移映射(内存→载荷)
2. row0 反例逐字节对账(反例原文未动)
3. server body 371..36,502 的 211 种长度的结构解释
4. verify.py 仅覆盖 Phase 2 量化项;Phase 3 无量化校验

## 校验(指挥官补写 verify.py,独立实现)
`py -V:3.12 -I -B scratch/t89/out/verify.py` → V1-V6 **7 项全过,0 failure**;`--selftest` PASS。
`scripts/t01_anchors.py` 7/7(验收时复核)。
