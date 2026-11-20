DONE type=t74 status=complete

# t74 交付清单

## 交付物(scratch/t74/out/)
- `frames.json` — 9 表 × client/server = 17 档行框,全部 `verified: true`,`escalations: []`
- `row_widths_{table}_{archive}.csv` — 17 份行长直方图(value→freq,非逐行)
- `identity_width_proof.json` — identity 宽度自证(对齐自证 + footer 唯一性)17 档
- `sensitivity.json` — (W, footer) 敏感性网格 15 点 × 17 档
- `verify.py` — 独立 verifier(不 import builder),95/95 通过
- `REPORT.md` — 结论、逐表语法、冲突与负结果、锚点回归

## Builder(scripts/)
- `scripts/t74_row_frames9.py` — CLI + payload 原语 + 17 档 SPECS,`--help`/`--selftest`,退出码 0/1/2
- `scripts/t74_frames_part2.py` — 行语法模型 + identity-triple 分层 DP(numpy 向量扫描)
- `scripts/t74_frames_part3.py` — 敏感性网格 + fm24_dump 锚点回归

## 验收
- 闭合:17/17 (archive, table),`header + Σrow + footer == payload_len` 逐字节
- identity 宽度:17/17 自证为 13B(唯一 `-13` 偏移对全部行成立;footer=8 唯一)
- bad_identity:0(全部 17 档)
- 锚点回归:6 表 9 项全通过(stadium Scti/Slat/Slon/rdui/duni、award、agreement、lcrg、language suffix)
- `verify.py` 95/95;`t74_row_frames9.py --selftest` 通过;全量运行 17/17

## 关键判定
- t47 header **25 → 14**(H=25 首行 35B 违反 `(len-41)%5==0`,H=14 时 2488/2488 成立)
- t24 未 escalate:server-only、84,507 行、唯一 DP 铺法闭合
- 锚点口径纠正:media `rdui@3/duni@7` 实为 **t6**(t7 在 FIELDS 无条目),负结果保留

## 未解(不阻塞)
- t7 media 中段嵌套结构、t7/t18 的 server 插段语义(数据侧观测已记)
- t27 identity DP 3 路多解(顺序语法已收敛,负结果保留)
