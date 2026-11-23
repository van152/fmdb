DONE type=t138

纯 Python（stdlib + vendored zstandard，运行时零 Unicorn/零 IDA）全量闭合解码 people_db.dat：

- **658,011 / 658,011 行**全部按真实 C 文法解码，**diff == 0**（400,443,970 B 逐字节闭合，
  28 字节 footer 收口：loader 读 2×[4] case-3 表 count + 20 字节 writer-only commit 尾包逐字节断言，
  族尾包文法经 basic_people_db.dat 与 t92 table_9 双实证）。
- 直方图逐型精确：{1: 166064, 2: 476158, 3: 4757, 4: 9839, 5: 1193}。
- 前 3,000 行 oracle（t126 _walk.json）0 mismatch；全量 walk 零 BranchError、无启发式跳过。
- selftest PASS（5 类合成行 exact + 14141E220 定向用例）。
- 产出：直方图、各 ptype body 长度 min/max、Top-20 球员（CA + 54 PDxx + t106 姓名表真名，
  #1–#18 与 t135 Unicorn 验证完全一致）→ people_pure_py_verify.json。

headline: rows=658011 diff=0 bytes=400443970 histogram={1:166064,2:476158,3:4757,4:9839,5:1193} selftest=PASS oracle_mismatches=0
