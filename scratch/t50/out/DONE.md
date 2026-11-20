# t50 — DONE

状态:`partial_data_profile_t9` · 证据等级 **L1 + L2, L3 = 0, L4 = 0** · 纯数据侧。

## 交付清单

| 文件 | 内容 |
|---|---|
| `scratch/t50/out/profile_t9.json` | 4 成员 anchors(entry.offset / packed_size / declared size / member_start / packed SHA / payload SHA)、tad shell、count@8、closure 判定、framing 敏感性表、identity census、行/块长度直方图、样本 |
| `scratch/t50/out/profiles/table_client_9.rows.jsonl` | 251 行:offset/body_offset/len/identity/prefix_probe/raw_hex |
| `scratch/t50/out/profiles/table_server_9.rows.jsonl` | 251 行(同上) |
| `scratch/t50/out/profiles/table_client_extra_9.rows.jsonl` | 251 块:offset/body_offset/len/marker/prefix_probe/raw_hex |
| `scratch/t50/out/profiles/table_server_extra_9.rows.jsonl` | 251 块(同上) |
| `scratch/t50/out/grammar_diff_t9.json` | 双档对比 + 同偏移探针 + t9↔t10 跨表 row_id 阶梯对照 |
| `scratch/t50/out/verify.py` | 独立验证器(不 import builder / t49),`--help` / `--selftest` / `--check`,退出码 0/1/2 |
| `scratch/t50/out/REPORT.md` | 完整报告(含负结果与未解项) |
| `scratch/t50/out/DONE.md` | 本文件 |
| `scripts/t50_nation_t9_profile.py` | builder,`--help` / `--selftest` / `--build`,退出码 0/1/2 |

## 核心结果

1. **4 成员全部独立解码**:单帧 zstd、帧长 == declared size、tad shell + `count@8 == 251` 4/4 成立。
   `table_extra_10.dat` 两档缺失。anchors 与 t47 archive 记录七项逐字节一致。
2. **`table_9` 可由 identity 尾闭合(L1)**:
   client `13 + 31935 + 8 = 31956`;server `13 + 307543 + 8 = 307564`;各 251 行连续铺满。
   DP 计数的完整铺法 = **1**(在"row_id 非零 + 严格递增"规则下),非"挑首个可行解"。
3. **identity census 全通过**:ordinal 序列 0..250、repeated lane 相等、marker 全 0、row_id 唯一且递增、
   末行 row_id == footer `u32@-4 = 82082540`,两档逐行完全一致。
4. **`table_extra_9` 只做到块首(诚实 partial)**:块形 `ordinal|name_len|name`,251 块连续铺满;
   client 1 条铺法 / server 4 条(歧义只在 row 2、row 82 的块内,不影响块首);**块内文法未解**,无独立 footer。
5. **负结果全保留**:t9 identity 判定式套到 `extra_9` 4 变体全 0(row 1 即死);允许 row_id=0 时 server 362 条宽解;
   header 11..15 等价(header 切分不由数据决定);8 vs 9 字节 footer 共用同一字节。

## 边界确认

未读 `editor.exe` / IDA / `fm.i64`;未追 reader/VA;未命名语义字段;未做 target ordinal join;未晋 L3。
未启动游戏/编辑器/IDA;未联网;未读写 `Z:`。未改 `scratch/t49/`、`scratch/t37/`、`scratch/t47/`。
只写 `scratch/t50/` 与 `scripts/t50_*.py`。

## 验收运行

```
py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --selftest          -> PASS (exit 0)
FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scripts/t50_nation_t9_profile.py --build -> exit 0
py -V:3.12 -I -B scratch/t50/out/verify.py --selftest                 -> PASS (exit 0)
FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scratch/t50/out/verify.py --check -> PASS (15 groups, exit 0)
py -V:3.12 -I -B scripts/t01_anchors.py                               -> 7/7
```

对 t49 的用途:本任务是 `table_9` / `table_extra_9` 的**独立 L2 交叉验证**材料 —— 若 t49 的静态/wire 结论给出
不同的行边界或不同的 identity 结构,可直接对撞本目录的 `rows.jsonl` 与 `grammar_diff_t9.json`。
